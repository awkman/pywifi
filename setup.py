#!/usr/bin/env python

import platform
import sys
import os
from setuptools import setup, find_packages

# 'setup.py publish' shortcut.
if sys.argv[-1].startswith('publish'):
    os.system('rm -rf build dist pywifi.egg-info')
    os.system('python setup.py sdist bdist_wheel')
    if 'test' in sys.argv[-1]:
        os.system('twine upload --repository-url '\
                  'https://test.pypi.org/legacy/ dist/*')
    else:
        os.system('twine upload dist/*')
    sys.exit()

with open('README.md', 'r') as f:
    readme = f.read()

if platform.system().lower() == 'windows':
    requires = ['comtypes']
else:
    requires = []

test_requires = [
    'pytest>=3.3.0'
]

setup(
    name='pywifi',
    version='1.1.12',
    author='Jiang Sheng-Jhih',
    author_email='shengjhih@gmail.com',
    description="A cross-platform module for manipulating WiFi devices.",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requires,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    url='https://github.com/awkman/pywifi', 
    license='MIT',
    download_url='https://github.com/awkman/pywifi/archive/master.zip', 
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords=['wifi', 'wireless', 'Linux', 'Windows'], 
)
