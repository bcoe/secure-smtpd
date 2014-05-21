#!/usr/bin/env python
#from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name="secure-smtpd",
    version="2.0.0",
    description="Adds support for SSL, AUTH, and other goodies, to Petri Lehtinen's SMTPD library.",
    author="Benjamin Coe",
    author_email="bencoe@gmail.com",
    url="https://github.com/bcoe/secure-smtpd",
    packages = find_packages(),
    install_requires = [
        'argparse'
    ],
    tests_require=[
        'nose'
    ]
)
