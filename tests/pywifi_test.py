import pytest
import sys
import time
import platform

sys.path.append('../pywifi')
import pywifi


def test_interfaces():

    wifi = pywifi.PyWiFi()
    assert wifi.interfaces()
    if platform.system().lower() == 'windows':
        assert wifi.interfaces()[0].name(
        ) == 'Intel(R) Dual Band Wireless-AC 7260'
    elif platform.system().lower() == 'linux':
        assert wifi.interfaces()[0].name() == 'wlx000c433243ce'


def test_scan():

    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    bsses = iface.scan_results()
    assert bsses

    for bss in bsses:
        print("BSSID: " + bss['bssid'])
        print("SSID: " + bss['ssid'])
        print("Security: " + str(bss['security']))
        print("FREQ: " + str(bss['freq']))
        print("SIGNAL: " + str(bss['signal']))


def test_add_network_profile():

    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    profile = {'ssid': 'testap',
               'key_mgmt': 'wpa2psk',
               'psk': '12345678'}

    iface.remove_all_network_profiles()

    assert len(iface.network_profiles()) == 0

    iface.add_network_profile(profile)
    profiles = iface.network_profiles()

    assert profiles is not None
    assert profiles[0]['ssid'] == "testap"
    assert profiles[0]['key_mgmt'] == 'wpa2psk'


def test_status():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    assert iface.status() == 'disconnected'


def test_connect():

    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    iface.disconnect()
    time.sleep(1)
    assert iface.status() == 'disconnected'

    profile = {'ssid': 'testap',
               'key_mgmt': 'wpa2psk',
               'psk': '12345678'}

    iface.remove_all_network_profiles()
    iface.add_network_profile(profile)
    networks = iface.network_profiles()

    assert len(networks) == 1

    iface.connect(networks[0])
    time.sleep(5)
    assert iface.status() == 'connected'

    iface.disconnect()
    time.sleep(1)
    assert iface.status() == 'disconnected'


def test_disconnect():

    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.disconnect()
