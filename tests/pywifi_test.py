#!/usr/bin/env python3
# vim: set fileencoding=utf-8

"""
Test cases for pywifi.
"""

import pytest
import sys
import time
import platform
import logging

import pywifi
from pywifi import const

pywifi.set_loglevel(logging.INFO)

def test_interfaces():

    wifi = pywifi.PyWiFi()

    assert wifi.interfaces()

    if platform.system().lower() == 'windows':
        assert wifi.interfaces()[0].name() ==\
            'Intel(R) Dual Band Wireless-AC 7260'
    elif platform.system().lower() == 'linux':
        assert wifi.interfaces()[0].name() == 'wlx000c433243ce'


def test_scan():

    wifi = pywifi.PyWiFi()

    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(5)
    bsses = iface.scan_results()
    assert bsses


def test_add_network_profile():

    wifi = pywifi.PyWiFi()

    iface = wifi.interfaces()[0]

    profile = pywifi.Profile()
    profile.ssid = 'testap'
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = '12345678'

    iface.remove_all_network_profiles()

    assert len(iface.network_profiles()) == 0

    iface.add_network_profile(profile)
    profiles = iface.network_profiles()

    assert profiles is not None
    assert profiles[0].ssid == "testap"
    assert const.AKM_TYPE_WPA2PSK in profiles[0].akm
    assert const.AUTH_ALG_OPEN == profiles[0].auth


def test_status():

    wifi = pywifi.PyWiFi()

    iface = wifi.interfaces()[0]
    iface.disconnect()
    assert iface.status() in\
        [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]


def test_connect():

    wifi = pywifi.PyWiFi()

    iface = wifi.interfaces()[0]

    iface.disconnect()
    time.sleep(1)
    assert iface.status() in\
        [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

    profile = pywifi.Profile()
    profile.ssid = 'testap'
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = '12345678'

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)

    iface.connect(tmp_profile)
    time.sleep(40)
    assert iface.status() == const.IFACE_CONNECTED

    iface.disconnect()
    time.sleep(1)
    assert iface.status() in\
        [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]


def test_connect_open():

    wifi = pywifi.PyWiFi()

    iface = wifi.interfaces()[0]

    iface.disconnect()
    time.sleep(1)
    assert iface.status() in\
        [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

    profile = pywifi.Profile()
    profile.ssid = 'testap'
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_NONE)

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)

    iface.connect(tmp_profile)
    time.sleep(40)
    assert iface.status() == const.IFACE_CONNECTED

    iface.disconnect()
    time.sleep(1)
    assert iface.status() in\
        [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

def test_disconnect():

    wifi = pywifi.PyWiFi()

    iface = wifi.interfaces()[0]
    iface.disconnect()

    assert iface.status() in\
        [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]
