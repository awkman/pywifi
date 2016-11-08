#!/usr/bin/env python3
# vim: set fileencoding=utf-8

"""Define WiFi Profile."""

from .const import *


class Profile():

    def __init__(self):

        self.auth = AUTH_ALG_OPEN
        self.akm = [AKM_TYPE_NONE]
        self.cipher = CIPHER_TYPE_NONE
        self.ssid = None
        self.bssid = None
        self.key = None

    def process_akm(self):

        if len(self.akm) > 1:
            self.akm = self.akm[-1:]
