# vim: set fileencoding=utf-8

import dbus

from . import wpas_dbus


def fill_bss_info(bssid, ssid, security, freq, signal):

    return {'bssid': bssid, 'ssid': ssid, 'security': security,
            'freq': freq, 'signal': signal}


def scan(obj):
    """Trigger the wifi interface to scan."""

    wpas_dbus.scan(obj['iface'])


def scan_results(obj):
    """Get the AP list after scanning."""

    bss_list = []
    bss_path_list = wpas_dbus.get_wpas_iface_dbus_iface_property(obj[
                                                                 'iface'], 'BSSs')
    for bss_path in bss_path_list:
        bss = wpas_dbus.setup_wpas_bss_dbus_iface(bss_path)
        tmp_bssid = bss.Get(wpas_dbus.WPAS_DBUS_NEW_IFACE_BSS,
                            'BSSID', dbus_interface=dbus.PROPERTIES_IFACE)
        bssid = ':'.join(format(x, '02x') for x in tmp_bssid)

        tmp_ssid = bss.Get(wpas_dbus.WPAS_DBUS_NEW_IFACE_BSS,
                           'SSID', dbus_interface=dbus.PROPERTIES_IFACE)
        ssid_byte_array = [str(x) if x >= 32 and x < 127 else urllib.parse.quote(
            ord(x)) for x in tmp_ssid]
        ssid = ''.join(ssid_byte_array)

        tmp_wpa = bss.Get(wpas_dbus.WPAS_DBUS_NEW_IFACE_BSS,
                          'WPA', dbus_interface=dbus.PROPERTIES_IFACE)
        security = False
        if len(tmp_wpa['KeyMgmt']):
            security = tmp_wpa['KeyMgmt']

        tmp_rsn = bss.Get(wpas_dbus.WPAS_DBUS_NEW_IFACE_BSS,
                          'RSN', dbus_interface=dbus.PROPERTIES_IFACE)
        if len(tmp_rsn['KeyMgmt']):
            security += tmp_rsn['KeyMgmt']

        freq = bss.Get(wpas_dbus.WPAS_DBUS_NEW_IFACE_BSS,
                       'Frequency', dbus_interface=dbus.PROPERTIES_IFACE)
        freq = int(freq)

        signal = bss.Get(wpas_dbus.WPAS_DBUS_NEW_IFACE_BSS,
                         'Signal', dbus_interface=dbus.PROPERTIES_IFACE)
        signal = int(signal)

        bss_list.append(fill_bss_info(bssid, ssid, security, freq, signal))

    return bss_list


def connect(obj, network):
    """Connect to the specified AP."""

    wpas_dbus.select_network(obj['iface'], network['path'])


def disconnect(obj):
    """Disconnect to the specified AP."""

    wpas_dbus.disconnect(obj['iface'])


def add_network_profile(obj, params):
    """Add AP profile for connecting to afterward."""

    if params['key_mgmt'].lower() in ['wpa2psk', 'wpapsk']:
        params['key_mgmt'] = 'WPA-PSK'
    wpas_dbus.add_network(obj['iface'], params)


def network_profiles(obj):
    """Get AP profiles."""

    network_list = []
    network_path_list = wpas_dbus.get_wpas_iface_dbus_iface_property(
        obj['iface'], 'Networks')

    for network_path in network_path_list:
        network = wpas_dbus.setup_wpas_network_dbus_iface(network_path)
        props = network.Get(wpas_dbus.WPAS_DBUS_NEW_IFACE_NETWORK,
                            'Properties', dbus_interface=dbus.PROPERTIES_IFACE)
        profile = {}
        profile['ssid'] = props['ssid'].strip('"')
        if props['key_mgmt'].lower() == 'wpa-psk':
            props['key_mgmt'] = 'wpa2psk'
        profile['key_mgmt'] = props['key_mgmt']
        profile['path'] = network_path
        network_list.append(profile)

    return network_list


def remove_all_network_profiles(obj):
    """Remove all the AP profiles."""

    wpas_dbus.remove_all_networks(obj['iface'])


def status(obj):
    """Get the wifi interface status."""

    return wpas_dbus.status(obj['iface'])


def interfaces():
    """Get the wifi interface lists."""

    ifaces = []
    wpas_dbus.setup_wpas_dbus_iface()
    tmp_ifaces = wpas_dbus.get_wpas_dbus_iface_property('Interfaces')
    for interface in tmp_ifaces:
        iface = {}
        iface['iface_path'] = interface
        iface['iface_obj'], iface['iface'] =\
            wpas_dbus.setup_wpas_iface_dbus_iface_by_obj_path(interface)
        iface['name'] = wpas_dbus.get_wpas_iface_dbus_iface_property(
            iface['iface'], 'Ifname')
        ifaces.append(iface)

    return ifaces
