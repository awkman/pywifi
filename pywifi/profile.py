#!/usr/bin/env python3
# vim: set fileencoding=utf-8

"""Define WiFi Profile."""

from .const import *


class Profile():

    def __init__(self, auth=AUTH_ALG_OPEN, akm=[AKM_TYPE_NONE], cipher=CIPHER_TYPE_NONE, ssid=None, bssid=None, key=None):

        self.auth = auth
        self.akm = akm
        self.cipher = cipher
        self.ssid = ssid
        self.bssid = bssid
        self.key = key

    def process_akm(self):

        if len(self.akm) > 1:
            self.akm = self.akm[-1:]
