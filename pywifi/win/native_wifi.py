#!/usr/bin/env python3
# vim: set fileencoding=utf-8

"""
The basic wifi function of Windows platform from Window Native WiFi API.
For more information, please refer to 
https://msdn.microsoft.com/en-us/library/windows/desktop/ms706556(v=vs.85).aspx
"""

from enum import Enum
from ctypes import *
from ctypes.wintypes import *
from comtypes import GUID
import platform
import time

native_wifi = windll.wlanapi
client_version = 2
nego_version = DWORD()
handle = HANDLE()

ERROR_SUCCESS = 0
WLAN_MAX_PHY_TYPE_NUMBER = 8
DOT11_MAC_ADDRESS = c_ubyte * 6


class WLAN_INTERFACE_STATE(Enum):
    wlan_interface_state_not_ready = 0,
    wlan_interface_state_connected = 1,
    wlan_interface_state_ad_hoc_network_formed = 2,
    wlan_interface_state_disconnecting = 3,
    wlan_interface_state_disconnected = 4,
    wlan_interface_state_associating = 5,
    wlan_interface_state_discovering = 6,
    wlan_interface_state_authenticating = 7


class DOT11_BSS_TYPE(Enum):
    dot11_BSS_type_infrastructure = 1,
    dot11_BSS_type_independent = 2,
    dot11_BSS_type_any = 3


class DOT11_PHY_TYPE(Enum):
    dot11_phy_type_unknown = 0,
    dot11_phy_type_any = 0,
    dot11_phy_type_fhss = 1,
    dot11_phy_type_dsss = 2,
    dot11_phy_type_irbaseband = 3,
    dot11_phy_type_ofdm = 4,
    dot11_phy_type_hrdsss = 5,
    dot11_phy_type_erp = 6,
    dot11_phy_type_ht = 7,
    dot11_phy_type_vht = 8,
    dot11_phy_type_IHV_start = 0x80000000,
    dot11_phy_type_IHV_end = 0xffffffff


class DOT11_AUTH_ALGORITHM(Enum):
    DOT11_AUTH_ALGO_80211_OPEN = 1,
    DOT11_AUTH_ALGO_80211_SHARED_KEY = 2,
    DOT11_AUTH_ALGO_WPA = 3,
    DOT11_AUTH_ALGO_WPA_PSK = 4,
    DOT11_AUTH_ALGO_WPA_NONE = 5,
    DOT11_AUTH_ALGO_RSNA = 6,
    DOT11_AUTH_ALGO_RSNA_PSK = 7,
    DOT11_AUTH_ALGO_IHV_START = 0x80000000,
    DOT11_AUTH_ALGO_IHV_END = 0xffffffff


class DOT11_CIPHER_ALGORITHM(Enum):
    DOT11_CIPHER_ALGO_NONE = 0x00,
    DOT11_CIPHER_ALGO_WEP40 = 0x01,
    DOT11_CIPHER_ALGO_TKIP = 0x02,
    DOT11_CIPHER_ALGO_CCMP = 0x04,
    DOT11_CIPHER_ALGO_WEP104 = 0x05,
    DOT11_CIPHER_ALGO_WPA_USE_GROUP = 0x100,
    DOT11_CIPHER_ALGO_RSN_USE_GROUP = 0x100,
    DOT11_CIPHER_ALGO_WEP = 0x101,
    DOT11_CIPHER_ALGO_IHV_START = 0x80000000,
    DOT11_CIPHER_ALGO_IHV_END = 0xffffffff


class WLAN_CONNECTION_MODE(Enum):
    wlan_connection_mode_profile = 0,
    wlan_connection_mode_temporary_profile = 1,
    wlan_connection_mode_discovery_secure = 2,
    wlan_connection_mode_discovery_unsecure = 3,
    wlan_connection_mode_auto = 4,
    wlan_connection_mode_invalid = 5


class WLAN_INTERFACE_INFO(Structure):
    _fields_ = [("InterfaceGuid", GUID),
                ("strInterfaceDescription", c_wchar * 256),
                ("isState", c_uint)]


class WLAN_INTERFACE_INFO_LIST(Structure):
    _fields_ = [("dwNumberOfItems", DWORD),
                ("dwIndex", DWORD),
                ("InterfaceInfo", WLAN_INTERFACE_INFO * 1)]


class DOT11_SSID(Structure):
    _fields_ = [("uSSIDLength", c_ulong),
                ("ucSSID", c_char * 32)]


class WLAN_RATE_SET(Structure):
    _fields_ = [("uRateSetLength", c_ulong),
                ("usRateSet", c_ushort * 126)]


class WLAN_RAW_DATA(Structure):
    _fields_ = [("dwDataSize", DWORD),
                ("DataBlob", c_byte * 1)]


class WLAN_AVAILABLE_NETWORK(Structure):
    _fields_ = [("strProfileName", c_wchar * 256),
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
                ("dwReserved", DWORD)]


class WLAN_AVAILABLE_NETWORK_LIST(Structure):
    _fields_ = [("dwNumberOfItems", DWORD),
                ("dwIndex", DWORD),
                ("Network", WLAN_AVAILABLE_NETWORK * 1)]


class WLAN_BSS_ENTRY(Structure):
    _fields_ = [("dot11Ssid", DOT11_SSID),
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
                ("ulIeSize", c_ulong)]


class WLAN_BSS_LIST(Structure):
    _fields_ = [("dwTotalSize", DWORD),
                ("dwNumberOfItems", DWORD),
                ("wlanBssEntries", WLAN_BSS_ENTRY * 1)]


class NDIS_OBJECT_HEADER(Structure):
    _fields_ = [("Type", c_ubyte),
                ("Revision", c_ubyte),
                ("Size", c_ushort)]


class DOT11_BSSID_LIST(Structure):
    _fields_ = [("Header", NDIS_OBJECT_HEADER),
                ("uNumOfEntries", c_ulong),
                ("uTotalNumOfEntries", c_ulong),
                ("BSSIDs", DOT11_MAC_ADDRESS * 1)]


class WLAN_CONNECTION_PARAMETERS(Structure):
    _fields_ = [("wlanConnectionMode", c_uint),
                ("strProfile", c_wchar_p),
                ("pDot11Ssid", POINTER(DOT11_SSID)),
                ("pDesiredBssidList", POINTER(DOT11_BSSID_LIST)),
                ("dot11BssType", c_uint),
                ("dwFlags", DWORD)]


class WLAN_PROFILE_INFO(Structure):
    _fields_ = [("strProfileName", c_wchar * 256),
                ("dwFlags", DWORD)]


class WLAN_PROFILE_INFO_LIST(Structure):
    _fields_ = [("dwNumberOfItems", DWORD),
                ("dwIndex", DWORD),
                ("ProfileInfo", WLAN_PROFILE_INFO * 1)]


ifaces = pointer(WLAN_INTERFACE_INFO_LIST())

if platform.release().lower() == 'xp':
    if platform.win32_ver()[2].lower() in ['sp2', 'sp3']:
        client_version = 1


def wlan_open_handle(client_version, nego_version, handle):

    func = native_wifi.WlanOpenHandle
    func.argtypes = [DWORD, c_void_p, POINTER(DWORD), POINTER(HANDLE)]
    func.restypes = [DWORD]
    return func(client_version, None, nego_version, handle)


def wlan_close_handle(handle):

    func = native_wifi.WlanCloseHandle
    func.argtypes = [HANDLE, c_void_p]
    func.restypes = [DWORD]
    return func(handle, None)


def wlan_enum_interfaces(handle, ifaces):

    func = native_wifi.WlanEnumInterfaces
    func.argtypes = [HANDLE, c_void_p, POINTER(
        POINTER(WLAN_INTERFACE_INFO_LIST))]
    func.restypes = [DWORD]
    return func(handle, None, ifaces)


def wlan_get_available_network_list(handle, iface_guid, flags, network_list):

    func = native_wifi.WlanGetAvailableNetworkList
    func.argtypes = [HANDLE, POINTER(GUID), DWORD, c_void_p, POINTER(
        POINTER(WLAN_AVAILABLE_NETWORK_LIST))]
    func.restypes = [DWORD]
    return func(handle, iface_guid, flags, None, network_list)


def wlan_get_network_bss_list(handle, iface_guid, bss_list):

    func = native_wifi.WlanGetNetworkBssList
    func.argtypes = [HANDLE, POINTER(GUID), POINTER(
        DOT11_SSID), c_uint, c_bool, c_void_p, POINTER(POINTER(WLAN_BSS_LIST))]
    func.restypes = [DWORD]
    return func(handle, iface_guid, None, 1, False, None, bss_list)


def wlan_scan(handle, iface_guid):

    func = native_wifi.WlanScan
    func.argtypes = [HANDLE, POINTER(GUID), POINTER(
        DOT11_SSID), POINTER(WLAN_RAW_DATA), c_void_p]
    func.restypes = [DWORD]
    return func(handle, iface_guid, None, None, None)


def wlan_connect(handle, iface_guid, params):

    func = native_wifi.WlanConnect
    func.argtypes = [HANDLE, POINTER(GUID), POINTER(
        WLAN_CONNECTION_PARAMETERS), c_void_p]
    func.restypes = [DWORD]
    return func(handle, iface_guid, params, None)


def wlan_set_profile(handle, iface_guid, xml, overwrite, reason_code):

    func = native_wifi.WlanSetProfile
    func.argtypes = [HANDLE, POINTER(
        GUID), DWORD, c_wchar_p, c_wchar_p, c_bool, c_void_p, POINTER(DWORD)]
    func.restypes = [DWORD]
    return func(handle, iface_guid, 2, xml, None, overwrite, None, reason_code)


def wlan_reason_code_to_str(reason_code, buf_size, buf):

    func = native_wifi.WlanReasonCodeToString
    func.argtypes = [DWORD, DWORD, PWCHAR, c_void_p]
    func.restypes = [DWORD]
    return func(reason_code, buf_size, buf, None)


def wlan_get_profile_list(handle, iface_guid, profile_list):

    func = native_wifi.WlanGetProfileList
    func.argtypes = [HANDLE, POINTER(GUID), c_void_p, POINTER(
        POINTER(WLAN_PROFILE_INFO_LIST))]
    func.restypes = [DWORD]
    return func(handle, iface_guid, None, profile_list)


def wlan_get_profile(handle, iface_guid, profile_name, xml, flags, access):

    func = native_wifi.WlanGetProfile
    func.argtypes = [HANDLE, POINTER(GUID), c_wchar_p, c_void_p, POINTER(
        c_wchar_p), POINTER(DWORD), POINTER(DWORD)]
    func.restypes = [DWORD]
    return func(handle, iface_guid, profile_name, None, xml, flags, access)


def wlan_delete_profile(handle, iface_guid, profile_name):

    func = native_wifi.WlanDeleteProfile
    func.argtypes = [HANDLE, POINTER(GUID), c_wchar_p, c_void_p]
    func.restypes = [DWORD]
    return func(handle, iface_guid, profile_name, None)


def wlan_query_interface(handle, iface_guid, opcode, data_size, data, opcode_value_type):

    func = native_wifi.WlanQueryInterface
    func.argtypes = [HANDLE, POINTER(GUID), DWORD, c_void_p, POINTER(
        DWORD), POINTER(POINTER(DWORD)), POINTER(DWORD)]
    func.restypes = [DWORD]
    return func(handle, iface_guid, opcode, None, data_size, data, opcode_value_type)


def wlan_disconnect(handle, iface_guid):

    func = native_wifi.WlanDisconnect
    func.argtypes = [HANDLE, POINTER(GUID), c_void_p]
    func.restypes = [DWORD]
    return func(handle, iface_guid, None)
