#!/usr/bin/env python
#from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name="secure-smtpd",
    version="2.1.1",
    description="Adds support for SSL, AUTH, and other goodies, to Petri Lehtinen's SMTPD library.",
    long_description=open('README.markdown').read(),
    author="Benjamin Coe",
    author_email="bencoe@gmail.com",
    url="https://github.com/bcoe/secure-smtpd",
    keywords='secure ssl auth smtp smtpd server',
    license='ISC',
    packages = find_packages(),
    install_requires = [
        'argparse'
    ],
    tests_require=[
        'nose'
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[ # See: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Topic :: Communications :: Email :: Mail Transport Agents',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: ISC License (ISCL)',
    ],
)
