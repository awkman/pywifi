#!/usr/bin/env python3
# vim: set fileencoding=utf-8

from ctypes import *
import re

from . import native_wifi as wifiapi

def scan(obj):
    """Trigger the wifi interface to scan."""

    wifiapi.wlan_scan(wifiapi.handle, byref(obj['guid']))


def scan_results(obj):
    """Get the AP list after scanning."""

    bss_list = pointer(wifiapi.WLAN_BSS_LIST())
    wifiapi.wlan_get_network_bss_list(wifiapi.handle,
                                      byref(obj['guid']), byref(bss_list))
    bsses = cast(bss_list.contents.wlanBssEntries,
                 POINTER(wifiapi.WLAN_BSS_ENTRY))

    network_list = []
    for i in range(bss_list.contents.dwNumberOfItems):
        network = {}

        network['ssid'] = ''
        for j in range(bsses[i].dot11Ssid.uSSIDLength):
            network['ssid'] += "%c" % bsses[i].dot11Ssid.ucSSID[j]

        network['bssid'] = ''
        for j in range(6):
            network['bssid'] += "%02x:" % bsses[i].dot11Bssid[j]
        #network['bssid'] = ''.format("%02x:" % chr(c) for c in bsses[i].dot11Bssid)
        #network['ssid'] = ''.format("%c" % c for c in bsses[i].dot11Ssid.ucSSID)
        network['signal'] = bsses[i].lRssi
        network['freq'] = bsses[i].ulChCenterFrequency
        network['security'] = bsses[i].usCapabilityInformation
        network_list.append(network)

    return network_list


def connect(obj, params):
    """Connect to the specified AP."""

    connect_params = wifiapi.WLAN_CONNECTION_PARAMETERS()
    connect_params.wlanConnectionMode = 0  # Profile
    connect_params.dot11BssType = 1  # infra
    profile_name = create_unicode_buffer(params['ssid'])
    #cast(profile_name.value, wifiapi.c_wchar_p)

    connect_params.strProfile = profile_name.value
    ret = wifiapi.wlan_connect(
        wifiapi.handle, obj['guid'], byref(connect_params))
    print('connect result: %d' % ret)


def disconnect(obj):
    """Disconnect to the specified AP."""

    wifiapi.wlan_disconnect(wifiapi.handle, obj['guid'])


def add_network_profile(obj, params):
    """Add AP profile for connecting to afterward."""

    reason_code = wifiapi.DWORD()

    if params['key_mgmt'].lower() == 'wpa2psk':
        params['auth'] = 'WPA2PSK'
        params['encrypt'] = 'AES'
    elif params['key_mgmt'].lower() == 'wpapsk':
        params['auth'] = 'WPAPSK'
        params['encrypt'] = 'TKIP'

    params['protected'] = 'false'
    params['profile_name'] = params['ssid']

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
			</authEncryption>"""

    if params['key_mgmt'].lower() != 'none':
        xml += """<sharedKey>
				<keyType>passPhrase</keyType>
				<protected>{protected}</protected>
				<keyMaterial>{psk}</keyMaterial>
			</sharedKey>
		</security>
	</MSM>"""

    xml += """<MacRandomization xmlns="http://www.microsoft.com/networking/WLAN/profile/v3">
		<enableRandomization>false</enableRandomization>
	</MacRandomization>
</WLANProfile>"""

    xml = xml.format(**params)
    #print(xml)
    status = wifiapi.wlan_set_profile(wifiapi.handle, obj['guid'], xml,
                                      True, byref(reason_code))
    if status != wifiapi.ERROR_SUCCESS:
        print('Status %d:Add profile failed' % status)

    buf_size = wifiapi.DWORD(64)
    buf = create_unicode_buffer(64)
    wifiapi.wlan_reason_code_to_str(reason_code, buf_size, buf)


def network_profile_name_list(obj):
    """Get AP profile names."""

    profile_list = pointer(wifiapi.WLAN_PROFILE_INFO_LIST())
    wifiapi.wlan_get_profile_list(wifiapi.handle,
                                  byref(obj['guid']),
                                  byref(profile_list))
    profiles = cast(profile_list.contents.ProfileInfo,
                    POINTER(wifiapi.WLAN_PROFILE_INFO))

    profile_name_list = []
    for i in range(profile_list.contents.dwNumberOfItems):
        profile_name = ''
        for j in range(len(profiles[i].strProfileName)):
            profile_name += profiles[i].strProfileName[j]
        profile_name_list.append(profile_name)

    return profile_name_list


def network_profiles(obj):
    """Get AP profiles."""

    profile_name_list = network_profile_name_list(obj)

    profile_list = []
    for profile_name in profile_name_list:
        profile = {}
        flags = wifiapi.DWORD()
        access = wifiapi.DWORD()
        xml = wifiapi.LPWSTR()
        wifiapi.wlan_get_profile(wifiapi.handle, obj['guid'],
                                 profile_name, byref(xml), byref(flags),
                                 byref(access))
        # fill profile info
        profile['ssid'] = re.search(r'<name>(.*)</name>', xml.value).group(1)
        profile['key_mgmt'] = re.search(
            r'<authentication>(.*)</authentication>', xml.value).group(1).lower()
        #print(xml.value)

        profile_list.append(profile)

    return profile_list


def remove_all_network_profiles(obj):
    """Remove all the AP profiles."""

    profile_name_list = network_profile_name_list(obj)

    for profile_name in profile_name_list:
        print('delete profile: %s' % profile_name)
        str_buf = create_unicode_buffer(profile_name)
        ret = wifiapi.wlan_delete_profile(wifiapi.handle, obj['guid'], str_buf)
        print('delete result %d' % ret)


def status(obj):
    """Get the wifi interface status."""

    data_size = wifiapi.DWORD()
    data = wifiapi.PDWORD()
    opcode_value_type = wifiapi.DWORD()
    wifiapi.wlan_query_interface(wifiapi.handle, obj['guid'], 6, byref(
        data_size), byref(data), byref(opcode_value_type))
    if data.contents.value == 1:
        return 'connected'
    elif data.contents.value == 4:
        return 'disconnected'


def interfaces():
    """Get the wifi interface lists."""

    ifaces = []

    if wifiapi.wlan_open_handle(wifiapi.client_version,
                                byref(wifiapi.nego_version),
                                byref(wifiapi.handle))\
       is not wifiapi.ERROR_SUCCESS:
        print("Open Handle failed")

    if wifiapi.wlan_enum_interfaces(wifiapi.handle, byref(wifiapi.ifaces))\
       is not wifiapi.ERROR_SUCCESS:
        print("Enum Interface failed")

    for interface in wifiapi.ifaces.contents.InterfaceInfo:
        iface = {}
        iface['guid'] = interface.InterfaceGuid
        iface['name'] = interface.strInterfaceDescription
        ifaces.append(iface)

    return ifaces
