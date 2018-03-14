#!/usr/bin/env python3
# vim: set fileencoding=utf-8

"""Implementations of wifi functions of Linux."""

import re
import platform
import time
import logging
from ctypes import *
from ctypes.wintypes import *
from comtypes import GUID

from .const import *
from .profile import Profile


if platform.release().lower() == 'xp':
    if platform.win32_ver()[2].lower() in ['sp2', 'sp3']:
        CLIENT_VERSION = 1
else:
    CLIENT_VERSION = 2

"""
Some types does not exist in python2 ctypes.wintypes so we fake them
using how its defined in python3 ctypes.wintypes.
"""
if not "PDWORD" in dir():
    PDWORD = POINTER(DWORD)

if not "PWCHAR" in dir():
    PWCHAR= POINTER(WCHAR)

ERROR_SUCCESS = 0
WLAN_MAX_PHY_TYPE_NUMBER = 8
DOT11_MAC_ADDRESS = c_ubyte * 6


native_wifi = windll.wlanapi

status_dict = [
    IFACE_INACTIVE,
    IFACE_CONNECTED,
    IFACE_CONNECTED,
    IFACE_DISCONNECTED,
    IFACE_DISCONNECTED,
    IFACE_CONNECTING,
    IFACE_CONNECTING,
    IFACE_CONNECTING
]

auth_value_to_str_dict = {
    AUTH_ALG_OPEN: 'open',
    AUTH_ALG_SHARED: 'shared'
}

auth_str_to_value_dict = {
    'open': AUTH_ALG_OPEN,
    'shared': AUTH_ALG_SHARED
}

akm_str_to_value_dict = {
    'NONE': AKM_TYPE_NONE,
    'WPA': AKM_TYPE_WPA,
    'WPAPSK': AKM_TYPE_WPAPSK,
    'WPA2': AKM_TYPE_WPA2,
    'WPA2PSK': AKM_TYPE_WPA2PSK,
    'OTHER': AKM_TYPE_UNKNOWN
}

akm_value_to_str_dict = {
    AKM_TYPE_NONE: 'NONE',
    AKM_TYPE_WPA: 'WPA',
    AKM_TYPE_WPAPSK: 'WPAPSK',
    AKM_TYPE_WPA2: 'WPA2',
    AKM_TYPE_WPA2PSK: 'WPA2PSK',
    AKM_TYPE_UNKNOWN: 'OTHER'
}

cipher_str_to_value_dict = {
    'NONE': CIPHER_TYPE_NONE,
    'WEP': CIPHER_TYPE_WEP,
    'TKIP': CIPHER_TYPE_TKIP,
    'AES': CIPHER_TYPE_CCMP,
    'OTHER': CIPHER_TYPE_UNKNOWN
}

cipher_value_to_str_dict = {
    CIPHER_TYPE_NONE: 'NONE',
    CIPHER_TYPE_WEP: 'WEP',
    CIPHER_TYPE_TKIP: 'TKIP',
    CIPHER_TYPE_CCMP: 'AES',
    CIPHER_TYPE_UNKNOWN: 'UNKNOWN'
}

class WLAN_INTERFACE_INFO(Structure):

    _fields_ = [
        ("InterfaceGuid", GUID),
        ("strInterfaceDescription", c_wchar * 256),
        ("isState", c_uint)
    ]


class WLAN_INTERFACE_INFO_LIST(Structure):

    _fields_ = [
        ("dwNumberOfItems", DWORD),
        ("dwIndex", DWORD),
        ("InterfaceInfo", WLAN_INTERFACE_INFO * 1)
    ]


class DOT11_SSID(Structure):

    _fields_ = [("uSSIDLength", c_ulong),
                ("ucSSID", c_char * 32)]


class WLAN_RATE_SET(Structure):

    _fields_ = [
        ("uRateSetLength", c_ulong),
        ("usRateSet", c_ushort * 126)
    ]


class WLAN_RAW_DATA(Structure):

    _fields_ = [
        ("dwDataSize", DWORD),
        ("DataBlob", c_byte * 1)
    ]


class WLAN_AVAILABLE_NETWORK(Structure):

    _fields_ = [
        ("strProfileName", c_wchar * 256),
        ("dot11Ssid", DOT11_SSID),
        ("dot11BssType", c_uint),
        ("uNumberOfBssids", c_ulong),
        ("bNetworkConnectable", c_bool),
        ("wlanNotConnectableReason", c_uint),
        ("uNumberOfPhyTypes", c_ulong * WLAN_MAX_PHY_TYPE_NUMBER),
        ("dot11PhyTypes", c_uint),
        ("bMorePhyTypes", c_bool),
        ("wlanSignalQuality", c_ulong),
        ("bSecurityEnabled", c_bool),
        ("dot11DefaultAuthAlgorithm", c_uint),
        ("dot11DefaultCipherAlgorithm", c_uint),
        ("dwFlags", DWORD),
        ("dwReserved", DWORD)
    ]


class WLAN_AVAILABLE_NETWORK_LIST(Structure):

    _fields_ = [
        ("dwNumberOfItems", DWORD),
        ("dwIndex", DWORD),
        ("Network", WLAN_AVAILABLE_NETWORK * 1)
    ]


class WLAN_BSS_ENTRY(Structure):

    _fields_ = [
        ("dot11Ssid", DOT11_SSID),
        ("uPhyId", c_ulong),
        ("dot11Bssid", DOT11_MAC_ADDRESS),
        ("dot11BssType", c_uint),
        ("dot11BssPhyType", c_uint),
        ("lRssi", c_long),
        ("uLinkQuality", c_ulong),
        ("bInRegDomain", c_bool),
        ("usBeaconPeriod", c_ushort),
        ("ullTimestamp", c_ulonglong),
        ("ullHostTimestamp", c_ulonglong),
        ("usCapabilityInformation", c_ushort),
        ("ulChCenterFrequency", c_ulong),
        ("wlanRateSet", WLAN_RATE_SET),
        ("ulIeOffset", c_ulong),
        ("ulIeSize", c_ulong)
    ]


class WLAN_BSS_LIST(Structure):

    _fields_ = [
        ("dwTotalSize", DWORD),
        ("dwNumberOfItems", DWORD),
        ("wlanBssEntries", WLAN_BSS_ENTRY * 1)
    ]


class NDIS_OBJECT_HEADER(Structure):

    _fields_ = [
        ("Type", c_ubyte),
        ("Revision", c_ubyte),
        ("Size", c_ushort)
    ]


class DOT11_BSSID_LIST(Structure):

    _fields_ = [
        ("Header", NDIS_OBJECT_HEADER),
        ("uNumOfEntries", c_ulong),
        ("uTotalNumOfEntries", c_ulong),
        ("BSSIDs", DOT11_MAC_ADDRESS * 1)
    ]


class WLAN_CONNECTION_PARAMETERS(Structure):

    _fields_ = [
        ("wlanConnectionMode", c_uint),
        ("strProfile", c_wchar_p),
        ("pDot11Ssid", POINTER(DOT11_SSID)),
        ("pDesiredBssidList", POINTER(DOT11_BSSID_LIST)),
        ("dot11BssType", c_uint),
        ("dwFlags", DWORD)
    ]


class WLAN_PROFILE_INFO(Structure):

    _fields_ = [
        ("strProfileName", c_wchar * 256),
        ("dwFlags", DWORD)
    ]


class WLAN_PROFILE_INFO_LIST(Structure):

    _fields_ = [
        ("dwNumberOfItems", DWORD),
        ("dwIndex", DWORD),
        ("ProfileInfo", WLAN_PROFILE_INFO * 1)
    ]


class WifiUtil():
    """WifiUtil implements the wifi functions in Windows."""

    _nego_version = DWORD()
    _handle = HANDLE()
    _ifaces = pointer(WLAN_INTERFACE_INFO_LIST())
    _logger = logging.getLogger('pywifi')

    def scan(self, obj):
        """Trigger the wifi interface to scan."""

        self._wlan_scan(self._handle, byref(obj['guid']))

    def scan_results(self, obj):
        """Get the AP list after scanning."""

        avail_network_list = pointer(WLAN_AVAILABLE_NETWORK_LIST())
        self._wlan_get_available_network_list(self._handle,
            byref(obj['guid']), byref(avail_network_list))
        networks = cast(avail_network_list.contents.Network,
                     POINTER(WLAN_AVAILABLE_NETWORK))

        self._logger.debug("Scan found %d networks.",
            avail_network_list.contents.dwNumberOfItems)

        network_list = []
        for i in range(avail_network_list.contents.dwNumberOfItems):

            if networks[i].dot11BssType == 1 and networks[i].bNetworkConnectable :

                ssid = ''
                for j in range(networks[i].dot11Ssid.uSSIDLength):

                    if networks[i].dot11Ssid.ucSSID != b'':
                        ssid += "%c" % networks[i].dot11Ssid.ucSSID[j]

                bss_list = pointer(WLAN_BSS_LIST())
                self._wlan_get_network_bss_list(self._handle,
                    byref(obj['guid']), byref(bss_list), networks[i].dot11Ssid, networks[i].bSecurityEnabled)
                bsses = cast(bss_list.contents.wlanBssEntries,
                             POINTER(WLAN_BSS_ENTRY))

                if networks[i].bSecurityEnabled:
                    akm = self._get_akm(networks[i].dot11DefaultCipherAlgorithm)
                    auth_alg = self._get_auth_alg(networks[i].dot11DefaultAuthAlgorithm)
                else:
                    akm = [AKM_TYPE_NONE]
                    auth_alg = [AUTH_ALG_OPEN]

                for j in range(bss_list.contents.dwNumberOfItems):
                    network = Profile()

                    network.ssid = ssid

                    network.bssid = ''
                    for k in range(6):
                        network.bssid += "%02x:" % bsses[j].dot11Bssid[k]

                    network.signal = bsses[j].lRssi
                    network.freq = bsses[j].ulChCenterFrequency
                    network.auth = auth_alg
                    network.akm = akm
                    network_list.append(network)

        return network_list

    def connect(self, obj, params):
        """Connect to the specified AP."""

        connect_params = WLAN_CONNECTION_PARAMETERS()
        connect_params.wlanConnectionMode = 0  # Profile
        connect_params.dot11BssType = 1  # infra
        profile_name = create_unicode_buffer(params.ssid)

        connect_params.strProfile = profile_name.value
        ret = self._wlan_connect(
            self._handle, obj['guid'], byref(connect_params))
        self._logger.debug('connect result: %d', ret)

    def disconnect(self, obj):
        """Disconnect to the specified AP."""

        self._wlan_disconnect(self._handle, obj['guid'])

    def add_network_profile(self, obj, params):
        """Add an AP profile for connecting to afterward."""

        reason_code = DWORD()

        params.process_akm()
        profile_data = {}
        profile_data['ssid'] = params.ssid

        if AKM_TYPE_NONE in params.akm:
            profile_data['auth'] = auth_value_to_str_dict[params.auth]
            profile_data['encrypt'] = "none"
        else:
            profile_data['auth'] = akm_value_to_str_dict[params.akm[-1]]
            profile_data['encrypt'] = cipher_value_to_str_dict[params.cipher]

        profile_data['key'] = params.key

        profile_data['protected'] = 'false'
        profile_data['profile_name'] = params.ssid

        xml = """<?xml version="1.0"?>
        <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
            <name>{profile_name}</name>
            <SSIDConfig>
                <SSID>
                    <name>{ssid}</name>
                </SSID>
            </SSIDConfig>
            <connectionType>ESS</connectionType>
            <connectionMode>manual</connectionMode>
            <MSM>
                <security>
                    <authEncryption>
                        <authentication>{auth}</authentication>
                        <encryption>{encrypt}</encryption>
                        <useOneX>false</useOneX>
                    </authEncryption>
        """

        if AKM_TYPE_NONE not in params.akm:
            xml += """<sharedKey>
                        <keyType>passPhrase</keyType>
                        <protected>{protected}</protected>
                        <keyMaterial>{key}</keyMaterial>
                    </sharedKey>"""

        xml += """
                </security>
            </MSM>"""

        xml += """<MacRandomization xmlns="http://www.microsoft.com/networking/WLAN/profile/v3">
                <enableRandomization>false</enableRandomization>
            </MacRandomization>
        </WLANProfile>
        """

        xml = xml.format(**profile_data)

        status = self._wlan_set_profile(self._handle, obj['guid'], xml,
                                        True, byref(reason_code))
        if status != ERROR_SUCCESS:
            self._logger.debug("Status %d: Add profile failed", status)

        buf_size = DWORD(64)
        buf = create_unicode_buffer(64)
        self._wlan_reason_code_to_str(reason_code, buf_size, buf)
        
        return params

    def network_profile_name_list(self, obj):
        """Get AP profile names."""

        profile_list = pointer(WLAN_PROFILE_INFO_LIST())
        self._wlan_get_profile_list(self._handle,
                                    byref(obj['guid']),
                                    byref(profile_list))
        profiles = cast(profile_list.contents.ProfileInfo,
                        POINTER(WLAN_PROFILE_INFO))

        profile_name_list = []
        for i in range(profile_list.contents.dwNumberOfItems):
            profile_name = ''
            for j in range(len(profiles[i].strProfileName)):
                profile_name += profiles[i].strProfileName[j]
            profile_name_list.append(profile_name)

        return profile_name_list

    def network_profiles(self, obj):
        """Get AP profiles."""

        profile_name_list = self.network_profile_name_list(obj)

        profile_list = []
        for profile_name in profile_name_list:
            profile = Profile()
            flags = DWORD()
            access = DWORD()
            xml = LPWSTR()
            self._wlan_get_profile(self._handle, obj['guid'],
                                   profile_name, byref(xml), byref(flags),
                                   byref(access))
            # fill profile info
            profile.ssid = re.search(r'<name>(.*)</name>', xml.value).group(1)
            auth = re.search(r'<authentication>(.*)</authentication>',
                                 xml.value).group(1).upper()

            profile.akm = []
            if auth not in akm_str_to_value_dict:
                if auth not in auth_str_to_value_dict:
                    profile.auth = AUTH_ALG_OPEN
                else:
                    profile.auth = auth_str_to_value_dict[auth]
                    profile.akm.append(AKM_TYPE_NONE)
            else:
                    profile.auth = AUTH_ALG_OPEN
                    profile.akm.append(akm_str_to_value_dict[auth])

            profile_list.append(profile)

        return profile_list

    def remove_all_network_profiles(self, obj):
        """Remove all the AP profiles."""

        profile_name_list = self.network_profile_name_list(obj)

        for profile_name in profile_name_list:
            self._logger.debug("delete profile: %s", profile_name)
            str_buf = create_unicode_buffer(profile_name)
            ret = self._wlan_delete_profile(self._handle, obj['guid'], str_buf)
            self._logger.debug("delete result %d", ret)

    def status(self, obj):
        """Get the wifi interface status."""

        data_size = DWORD()
        data = PDWORD()
        opcode_value_type = DWORD()
        self._wlan_query_interface(self._handle, obj['guid'], 6,
                                   byref(data_size), byref(data),
                                   byref(opcode_value_type))

        return status_dict[data.contents.value]

    def interfaces(self):
        """Get the wifi interface lists."""

        ifaces = []

        if self._wlan_open_handle(CLIENT_VERSION,
                                  byref(self._nego_version),
                                  byref(self._handle)) \
           is not ERROR_SUCCESS:
            self._logger.error("Open handle failed!")

        if self._wlan_enum_interfaces(self._handle, byref(self._ifaces)) \
           is not ERROR_SUCCESS:
            self._logger.error("Enum interface failed!")

        for interface in self._ifaces.contents.InterfaceInfo:
            iface = {}
            iface['guid'] = interface.InterfaceGuid
            iface['name'] = interface.strInterfaceDescription
            ifaces.append(iface)

        return ifaces

    def _wlan_open_handle(self, client_version, _nego_version, handle):

        func = native_wifi.WlanOpenHandle
        func.argtypes = [DWORD, c_void_p, POINTER(DWORD), POINTER(HANDLE)]
        func.restypes = [DWORD]
        return func(client_version, None, _nego_version, handle)

    def _wlan_close_handle(self, handle):

        func = native_wifi.WlanCloseHandle
        func.argtypes = [HANDLE, c_void_p]
        func.restypes = [DWORD]
        return func(handle, None)

    def _wlan_enum_interfaces(self, handle, ifaces):

        func = native_wifi.WlanEnumInterfaces
        func.argtypes = [HANDLE, c_void_p, POINTER(
            POINTER(WLAN_INTERFACE_INFO_LIST))]
        func.restypes = [DWORD]
        return func(handle, None, ifaces)

    def _wlan_get_available_network_list(self, handle,
                                         iface_guid,
                                         network_list):

        func = native_wifi.WlanGetAvailableNetworkList
        func.argtypes = [HANDLE, POINTER(GUID), DWORD, c_void_p, POINTER(
            POINTER(WLAN_AVAILABLE_NETWORK_LIST))]
        func.restypes = [DWORD]
        return func(handle, iface_guid, 2, None, network_list)

    def _wlan_get_network_bss_list(self, handle, iface_guid, bss_list, ssid = None, security = False):

        func = native_wifi.WlanGetNetworkBssList
        func.argtypes = [HANDLE, POINTER(GUID), POINTER(
            DOT11_SSID), c_uint, c_bool, c_void_p, POINTER(POINTER(WLAN_BSS_LIST))]
        func.restypes = [DWORD]
        return func(handle, iface_guid, ssid, 1, security, None, bss_list)

    def _wlan_scan(self, handle, iface_guid):

        func = native_wifi.WlanScan
        func.argtypes = [HANDLE, POINTER(GUID), POINTER(
            DOT11_SSID), POINTER(WLAN_RAW_DATA), c_void_p]
        func.restypes = [DWORD]
        return func(handle, iface_guid, None, None, None)

    def _wlan_connect(self, handle, iface_guid, params):

        func = native_wifi.WlanConnect
        func.argtypes = [HANDLE, POINTER(GUID), POINTER(
            WLAN_CONNECTION_PARAMETERS), c_void_p]
        func.restypes = [DWORD]
        return func(handle, iface_guid, params, None)

    def _wlan_set_profile(self, handle, iface_guid, xml, overwrite, reason_code):

        func = native_wifi.WlanSetProfile
        func.argtypes = [HANDLE, POINTER(
            GUID), DWORD, c_wchar_p, c_wchar_p, c_bool, c_void_p, POINTER(DWORD)]
        func.restypes = [DWORD]
        return func(handle, iface_guid, 2, xml, None, overwrite, None, reason_code)

    def _wlan_reason_code_to_str(self, reason_code, buf_size, buf):

        func = native_wifi.WlanReasonCodeToString
        func.argtypes = [DWORD, DWORD, PWCHAR, c_void_p]
        func.restypes = [DWORD]
        return func(reason_code, buf_size, buf, None)

    def _wlan_get_profile_list(self, handle, iface_guid, profile_list):

        func = native_wifi.WlanGetProfileList
        func.argtypes = [HANDLE, POINTER(GUID), c_void_p, POINTER(
            POINTER(WLAN_PROFILE_INFO_LIST))]
        func.restypes = [DWORD]
        return func(handle, iface_guid, None, profile_list)

    def _wlan_get_profile(self, handle, iface_guid, profile_name, xml, flags, access):

        func = native_wifi.WlanGetProfile
        func.argtypes = [HANDLE, POINTER(GUID), c_wchar_p, c_void_p, POINTER(
            c_wchar_p), POINTER(DWORD), POINTER(DWORD)]
        func.restypes = [DWORD]
        return func(handle, iface_guid, profile_name, None, xml, flags, access)

    def _wlan_delete_profile(self, handle, iface_guid, profile_name):

        func = native_wifi.WlanDeleteProfile
        func.argtypes = [HANDLE, POINTER(GUID), c_wchar_p, c_void_p]
        func.restypes = [DWORD]
        return func(handle, iface_guid, profile_name, None)

    def _wlan_query_interface(self, handle, iface_guid, opcode, data_size, data, opcode_value_type):

        func = native_wifi.WlanQueryInterface
        func.argtypes = [HANDLE, POINTER(GUID), DWORD, c_void_p, POINTER(
            DWORD), POINTER(POINTER(DWORD)), POINTER(DWORD)]
        func.restypes = [DWORD]
        return func(handle, iface_guid, opcode, None, data_size, data, opcode_value_type)

    def _wlan_disconnect(self, handle, iface_guid):

        func = native_wifi.WlanDisconnect
        func.argtypes = [HANDLE, POINTER(GUID), c_void_p]
        func.restypes = [DWORD]
        return func(handle, iface_guid, None)

    def _get_auth_alg(self, auth_val):

        auth_alg = []
        if auth_val in [1, 3, 4, 6, 7]:
            auth_alg.append(AUTH_ALG_OPEN)
        elif auth_val == 2:
            auth_alg.append(AUTH_ALG_SHARED)

        return auth_alg

    def _get_akm(self, akm_val):

        akm = []
        if akm_val == 2:
            akm.append(AKM_TYPE_WPAPSK)
        elif akm_val == 4:
            akm.append(AKM_TYPE_WPA2PSK)

        return akm
