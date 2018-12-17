import sys
import os
from pathlib import Path
from functools import reduce
import json
import csv
import re

import unidecode
from PyPDF2 import PdfFileReader, PdfFileWriter

from argparse import FileType
from .myargparser import MyParser

def main():
    parser = MyParser()

    parser.add_argument("--prix", type=int, default=5)
    parser.add_argument("--csv", type=FileType('r'), default=sys.stdin)
    parser.add_argument("--pdf", type=FileType('rb'), required=True)

    args = parser.parse_args()

    prix_place = args.prix 

    achats = []
    nb_place_total = 0
    
    reader = csv.reader(args.csv, delimiter=',')
    for row in reader:
        nom = row[1]
        mail = row[2]
        nb_place = float(float(row[5])/prix_place)

        if int(nb_place) != nb_place:
            print("error: nb de place impossible pour %s %s => %f" % (nom, mail, nb_place))
            sys.exit(5)

        nb_place = int(nb_place)
        nb_place_total = nb_place_total + nb_place


        achats.append({
            "nom": nom,
            "mail": mail,
            "nb_place": nb_place
        })

    pdfobj = PdfFileReader(args.pdf)
    nb_place_pdf = pdfobj.getNumPages()
    if nb_place_total < nb_place_pdf:
        print("warning: nb de place dans le pdf, supérieur aux commandes ( %i > %i ) " % (nb_place_pdf, nb_place_total))
    if nb_place_total > nb_place_pdf:
        print("error: nb de place insuffisant dans le pdf ( %i < %i )" % (nb_place_pdf, nb_place_total))
        sys.exit(5)

    next_place_page = 0

    for achat in achats:
        nb_place = achat["nb_place"]
        pdf_writer = PdfFileWriter()
        
        for p in range(nb_place):
            place = pdfobj.getPage(next_place_page)
            pdf_writer.insertPage(place)
            next_place_page = next_place_page + 1

        clean_name = re.sub('[^\w]+','_', unidecode.unidecode(achat["nom"]))
        pdf_client_path = os.path.join(os.getcwd(), "%s.pdf" % clean_name)
        with open(pdf_client_path, "wb") as pdfclient:
            print("Writing PDF to %s" % pdf_client_path) 
            pdf_writer.write(pdfclient)

        achat["pdf"] = os.path.basename(pdf_client_path)
        achat["prix_place"] = prix_place
        achat["prix_total"] = prix_place * nb_place
        
        json_client_path = os.path.join(os.getcwd(), "%s.json" % clean_name)
        with open(json_client_path, 'w') as fp:
            print("Writing metadata to %s" % json_client_path) 
            json.dump(achat, fp, indent=4)



if __name__ == '__main__':
    main()