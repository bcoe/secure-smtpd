#!/usr/bin/env python
#from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name="secure-smtpd",
    version="0.0.1",
    description="Extension to Pythons standard SMTP server. Adding support for various extensions to the protocol..",
    author="Benjamin Coe",
    author_email="bencoe@gmail.com",
    url="https://github.com/bcoe/secure-smtpd",
    packages = find_packages(),
    install_requires = [],
    tests_require=[
        'nose'
    ]
)