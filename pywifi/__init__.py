#!/usr/bin/env python3
# vim: set fileencoding=utf-8

"""
pywifi - a cross-platform wifi library.


This library is made for manipulating wifi device on varient platforms.
"""

import logging

from . import const 
from .wifi import PyWiFi


def set_loglevel(level=logging.NOTSET):

    format_pattern = "%(name)s %(asctime)s %(levelname)s %(message)s"
    logging.basicConfig(format=format_pattern)
    logger = logging.getLogger('pywifi')
    logger.setLevel(level)


set_loglevel()
