#!/usr/bin/env python

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = '0.1.0'

setup(
    name='monorpale',
    version=version,
    install_requires=requirements,
    author='Quiche',
    author_email='quiche@frais.se',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Cut PDF with klefki csv',
    entry_points={
        'console_scripts': [
            'monorpale = monorpale.__main__:main',
        ]
    },
    classifiers=[
        'Operating System :: OS Independent',
        'Topic :: Utilities',
    ]
)
