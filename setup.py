#!/usr/bin/env python
try:
  import os
  from setuptools import setup, find_packages
except ImportError:
  from distutils.core import setup

setup(
  name = 'pywifi',
  version = '0.9.1',
  author = 'Jiang Shengh-Jhih',
  author_email = 'shengjhih@gmail.com',
  description = "A cross-platform module for manipulating WiFi devices.",
  url = '', 
  license = 'MIT',
  download_url = '', 
  classifiers = [
      'Intended Audience :: Developers',
      'Topic :: Utilities',
      'License :: OSI Approved :: MIT License',

      'Programming Language :: Python :: 3.5',
  ],
  keywords = ['wifi', 'wireless', 'Linux', 'Windows'], 
)
