#!/usr/bin/env python
try:
    import os
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    name='pywifi',
    version='1.1.10',
    author='Jiang Sheng-Jhih',
    author_email='shengjhih@gmail.com',
    description="A cross-platform module for manipulating WiFi devices.",
    packages=find_packages(),
    install_requires=[
        'comtypes'
    ],
    url='https://github.com/awkman/pywifi', 
    license='MIT',
    download_url='https://github.com/awkman/pywifi/archive/master.zip', 
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 2.7',
    ],
    keywords=['wifi', 'wireless', 'Linux', 'Windows'], 
)
