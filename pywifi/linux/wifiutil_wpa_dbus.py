#!/usr/bin/env python3
# vim: set fileencoding=utf-8

"""Implementations of wifi functions of Linux."""

import dbus
import urllib
import copy
from gi.repository import GLib
from threading import Thread
from dbus.mainloop.glib import DBusGMainLoop

from ..wifiutil_abc import WifiUtilABC
from ..const import *

WPAS_DBUS_NEW_SERVICE = 'fi.w1.wpa_supplicant1'
WPAS_DBUS_NEW_PATH = '/fi/w1/wpa_supplicant1'
WPAS_DBUS_NEW_INTERFACE = 'fi.w1.wpa_supplicant1'
WPAS_DBUS_NEW_PATH_INTERFACES = WPAS_DBUS_NEW_PATH + '/Interfaces'
WPAS_DBUS_NEW_IFACE_INTERFACE = WPAS_DBUS_NEW_INTERFACE + '.Interface'
WPAS_DBUS_NEW_IFACE_WPS = WPAS_DBUS_NEW_INTERFACE + '.WPS'
WPAS_DBUS_NEW_IFACE_NETWORK = WPAS_DBUS_NEW_INTERFACE + '.Network'
WPAS_DBUS_NEW_IFACE_BSS = WPAS_DBUS_NEW_INTERFACE + '.BSS'

status_dict = {
    'completed': IFACE_CONNECTED,
    'inactive': IFACE_INACTIVE,
    'authenticating': IFACE_CONNECTING,
    'associating': IFACE_CONNECTING,
    'associated': IFACE_CONNECTING,
    '4way_handshake': IFACE_CONNECTING,
    'group_handshake': IFACE_CONNECTING,
    'interface_disabled': IFACE_INACTIVE,
    'disconnected': IFACE_DISCONNECTED,
    'scanning': IFACE_SCANNING
}

key_mgmt_dict = {
    'wpa-psk': AUTH_ALG_WPAPSK,
    'wpa2-psk': AUTH_ALG_WPA2PSK
}


class WifiUtil(WifiUtilABC):
    """WifiUtil implements the wifi functions in Linux."""

    _bus = None
    _wpas_obj = None
    _wpas = None

    def __init__(self):
        self._setup_wpas_dbus_iface()

    def scan(self, obj):
        """Trigger the wifi interface to scan."""

        obj['iface'].Scan({'Type': 'active'})

    def scan_results(self, obj):
        """Get the AP list after scanning."""

        bss_list = []
        bss_path_list = self._get_wpas_iface_dbus_iface_property(
            obj['iface'], 'BSSs')

        for bss_path in bss_path_list:
            bss = self._setup_wpas_bss_dbus_iface(bss_path)
            tmp_bssid = bss.Get(WPAS_DBUS_NEW_IFACE_BSS,
                                'BSSID', dbus_interface=dbus.PROPERTIES_IFACE)
            bssid = ':'.join(format(x, '02x') for x in tmp_bssid)

            tmp_ssid = bss.Get(WPAS_DBUS_NEW_IFACE_BSS,
                               'SSID', dbus_interface=dbus.PROPERTIES_IFACE)
            ssid_byte_array = [
                str(x) if x >= 32 and x < 127 else urllib.parse.quote(
                    ord(x)) for x in tmp_ssid
            ]
            ssid = ''.join(ssid_byte_array)

            security = []
            tmp_wpa = bss.Get(WPAS_DBUS_NEW_IFACE_BSS,
                              'WPA', dbus_interface=dbus.PROPERTIES_IFACE)

            for item in tmp_wpa['KeyMgmt']:
                if item.lower() == 'wpa-psk':
                    security.append(AUTH_ALG_WPAPSK)

            tmp_rsn = bss.Get(WPAS_DBUS_NEW_IFACE_BSS,
                              'RSN', dbus_interface=dbus.PROPERTIES_IFACE)
            for item in tmp_rsn['KeyMgmt']:
                if item.lower() == 'wpa-psk':
                    security.append(AUTH_ALG_WPA2PSK)

            freq = bss.Get(WPAS_DBUS_NEW_IFACE_BSS,
                           'Frequency', dbus_interface=dbus.PROPERTIES_IFACE)
            freq = int(freq)

            signal = bss.Get(WPAS_DBUS_NEW_IFACE_BSS,
                             'Signal', dbus_interface=dbus.PROPERTIES_IFACE)
            signal = int(signal)

            bss_list.append(self._fill_bss_info(
                bssid, ssid, security, freq, signal))

        return bss_list

    def connect(self, obj, network):
        """Connect to the specified AP."""

        obj['iface'].SelectNetwork(network['path'])

    def disconnect(self, obj):
        """Disconnect to the specified AP."""

        if self.status(obj) in [IFACE_CONNECTING, IFACE_CONNECTED]:
            obj['iface'].Disconnect()

    def add_network_profile(self, obj, params):
        """Add an AP profile for connecting to afterward."""

        profile = copy.deepcopy(params)
        if params['key_mgmt'] in [AUTH_ALG_WPAPSK, AUTH_ALG_WPA2PSK]:
            params['key_mgmt'] = 'WPA-PSK'

        profile['path'] = obj['iface'].AddNetwork(params)
        return profile

    def network_profiles(self, obj):
        """Get AP profiles."""

        network_list = []
        network_path_list = self._get_wpas_iface_dbus_iface_property(
            obj['iface'], 'Networks')

        for network_path in network_path_list:
            network = self._setup_wpas_network_dbus_iface(network_path)
            props = network.Get(WPAS_DBUS_NEW_IFACE_NETWORK,
                                'Properties',
                                dbus_interface=dbus.PROPERTIES_IFACE)

            profile = {}
            profile['ssid'] = props['ssid'].strip('"')

            profile['key_mgmt'] = []
            if props['key_mgmt'].lower() == 'wpa-psk':
                profile['key_mgmt'].append(AUTH_ALG_WPAPSK)
                if 'rsn' in props['proto'].lower():
                    profile['key_mgmt'].append(AUTH_ALG_WPA2PSK)
            if not props['key_mgmt']:
                profile['key_mgmt'].append(AUTH_ALG_OPEN)

            profile['path'] = network_path
            network_list.append(profile)

        return network_list

    def remove_all_network_profiles(self, obj):
        """Remove all the AP profiles."""

        obj['iface'].RemoveAllNetworks()

    def status(self, obj):
        """Get the wifi interface status."""

        status = self._get_wpas_iface_dbus_iface_property(
            obj['iface'], 'State').lower()

        return status_dict[status]

    def interfaces(self):
        """Get the wifi interface lists."""

        ifaces = []
        tmp_ifaces = self._get_wpas_dbus_iface_property('Interfaces')
        for interface in tmp_ifaces:
            iface = {}
            iface['iface_path'] = interface
            iface['iface_obj'], iface['iface'] = \
                self._setup_wpas_iface_dbus_iface_by_obj_path(interface)
            iface['name'] = str(self._get_wpas_iface_dbus_iface_property(
                iface['iface'], 'Ifname'))
            ifaces.append(iface)

        return ifaces

    def _get_wpas_iface_dbus_iface_property(self, iface, name):
        """Get specific wlan interface property via dbus."""

        return iface.Get(WPAS_DBUS_NEW_IFACE_INTERFACE, name,
                         dbus_interface=dbus.PROPERTIES_IFACE)

    def _get_wpas_dbus_iface_property(self, name):
        """Get wpa_supplicant property via dbus."""

        return self._wpas.Get(WPAS_DBUS_NEW_INTERFACE, name,
                              dbus_interface=dbus.PROPERTIES_IFACE)

    def _set_wpas_dbus_iface_property(self, name, value):
        """Set wpa_supplicant property via dbus."""

        func = self._get_dbus_type(value)
        return _wpas.Set(WPAS_DBUS_NEW_INTERFACE, name,
                         func(value), dbus_interface=dbus.PROPERTIES_IFACE)

    def _set_wpas_iface_dbus_iface_property(self, iface, name, value):
        """Set specific wlan interface property via dbus."""

        func = self._get_dbus_type(value)

        return iface.Set(WPAS_DBUS_NEW_IFACE_INTERFACE, name,
                         func(value), dbus_interface=dbus.PROPERTIES_IFACE)

    def _setup_wpas_iface_dbus_iface_by_name(self, wlan_name):
        """Setup wpa_supplicant dbus connection for specific iface."""

        iface_path = self._wpas.GetInterface(wlan_name)
        iface_obj = self._bus.get_object(WPAS_DBUS_NEW_SERVICE, _iface_path)
        iface = dbus.Interface(_iface_obj, WPAS_DBUS_NEW_IFACE_INTERFACE)

        return iface_path, iface_obj, iface

    def _setup_wpas_bss_dbus_iface(self, bss_path):
        """Setup wpa_supplicant dbus connection for specific bss."""

        bss_obj = self._bus.get_object(WPAS_DBUS_NEW_SERVICE, bss_path)
        bss = dbus.Interface(bss_obj, WPAS_DBUS_NEW_IFACE_BSS)

        return bss

    def _setup_wpas_network_dbus_iface(self, network_path):
        """Setup wpa_supplicant dbus connection for specific network."""

        network_obj = self._bus.get_object(WPAS_DBUS_NEW_SERVICE, network_path)
        network = dbus.Interface(network_obj, WPAS_DBUS_NEW_IFACE_NETWORK)

        return network

    def _setup_wpas_iface_dbus_iface_by_obj_path(self, iface_path):
        """Setup wpa_supplicant dbus connection for specific iface."""

        iface_obj = self._bus.get_object(WPAS_DBUS_NEW_SERVICE, iface_path)
        iface = dbus.Interface(iface_obj, WPAS_DBUS_NEW_IFACE_INTERFACE)

        return iface_obj, iface

    def _setup_wpas_dbus_iface(self):
        """Setup global wpa_supplicant dbus connection objects."""

        if self._bus is None:
            self._bus = dbus.SystemBus()

        if self._wpas_obj is None:
            self._wpas_obj = self._bus.get_object(
                WPAS_DBUS_NEW_SERVICE, WPAS_DBUS_NEW_PATH)

        if self._wpas is None:
            self._wpas = dbus.Interface(
                self._wpas_obj, WPAS_DBUS_NEW_INTERFACE)

    def _get_dbus_type(self, value):
        """Type mapping from python built-in types to dbus types."""

        if isinstance(valui, bool):
            return dbus.Boolean
        elif isinstance(value, int):
            return dbus.Int32
        elif isinstance(value, str):
            return dbus.String
        elif isinstance(value, dict):
            return dbus.Dictionary

    def _fill_bss_info(self, bssid, ssid, security, freq, signal):

        return {'bssid': bssid, 'ssid': ssid, 'key_mgmt': security,
                'freq': freq, 'signal': signal}
