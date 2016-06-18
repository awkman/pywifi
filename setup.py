#!/usr/bin/env python
try:
  import os
  from setuptools import setup, find_packages
except ImportError:
  from distutils.core import setup

setup(
  name = 'pywifi',
  version = '0.9.2',
  author = 'Jiang Shengh-Jhih',
  author_email = 'shengjhih@gmail.com',
  description = "A cross-platform module for manipulating WiFi devices.",
  url = 'https://github.com/awkman/pywifi', 
  license = 'MIT',
  download_url = 'https://github.com/awkman/pywifi/archive/master.zip', 
  classifiers = [
      'Intended Audience :: Developers',
      'Topic :: Utilities',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3.5',
  ],
  keywords = ['wifi', 'wireless', 'Linux', 'Windows'], 
)
