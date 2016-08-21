#!/usr/bin/env python

import ez_setup
ez_setup.use_setuptools(version="24")

from setuptools import setup, find_packages
import platform

def read(filename):
    with open(filename) as fp:
        return fp.read()

setup(
    name='pywifi',
    version='0.9.6',
    author='Jiang Shengh-Jhih',
    author_email='shengjhih@gmail.com',
    description="A cross-platform module for manipulating WiFi devices.",
    long_description=read("README.rst"),
    packages=find_packages(),
    url='https://github.com/awkman/pywifi', 
    license='MIT',
    install_requires=[
        'comtypes>=1.1'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet',
        'Topic :: Utilities'
    ],
    keywords=['wifi', 'wireless', 'Linux', 'Windows'], 
)
