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

def test_profile_comparison():

    wifi = pywifi.PyWiFi()

    iface = wifi.interfaces()[0]

    profile1 = pywifi.Profile()
    profile1.ssid = 'testap'
    profile1.auth = const.AUTH_ALG_OPEN
    profile1.akm.append(const.AKM_TYPE_WPA2PSK)
    profile1.cipher = const.CIPHER_TYPE_CCMP
    profile1.key = '12345678'

    profile2 = pywifi.Profile()
    profile2.ssid = 'testap'
    profile2.auth = const.AUTH_ALG_OPEN
    profile2.akm.append(const.AKM_TYPE_WPA2PSK)
    profile2.cipher = const.CIPHER_TYPE_CCMP
    profile2.key = '12345678'

    assert profile1 == profile2

    profile3 = pywifi.Profile()
    profile3.ssid = 'testap'
    profile3.auth = const.AUTH_ALG_OPEN
    profile3.akm.append(const.AKM_TYPE_WPAPSK)
    profile3.cipher = const.CIPHER_TYPE_CCMP
    profile3.key = '12345678'

    assert profile1 == profile3

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

def test_remove_network_profile():

    wifi = pywifi.PyWiFi()

    iface = wifi.interfaces()[0]
    iface.remove_all_network_profiles()

    assert len(iface.network_profiles()) == 0

    profile1 = pywifi.Profile()
    profile1.ssid = 'testap'
    profile1.auth = const.AUTH_ALG_OPEN
    profile1.akm.append(const.AKM_TYPE_WPA2PSK)
    profile1.cipher = const.CIPHER_TYPE_CCMP
    profile1.key = '12345678'
    iface.add_network_profile(profile1)

    profile2 = pywifi.Profile()
    profile2.ssid = 'testap2'
    profile2.auth = const.AUTH_ALG_OPEN
    profile2.akm.append(const.AKM_TYPE_WPA2PSK)
    profile2.cipher = const.CIPHER_TYPE_CCMP
    profile2.key = '12345678'
    iface.add_network_profile(profile2)

    profile3 = pywifi.Profile()
    profile3.ssid = 'testap3'
    profile3.auth = const.AUTH_ALG_OPEN
    profile3.akm.append(const.AKM_TYPE_WPAPSK)
    profile3.cipher = const.CIPHER_TYPE_CCMP
    profile3.key = '12345678'
    iface.add_network_profile(profile3)

    profiles = iface.network_profiles()

    assert len(profiles) == 3

    iface.remove_network_profile(profile2)

    profiles = iface.network_profiles()

    assert len(profiles) == 2
    assert profile2 not in profiles

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
