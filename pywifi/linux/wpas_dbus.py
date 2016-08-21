#!/usr/bin/env python3
# vim: set fileencoding=utf-8

import dbus
import urllib
from gi.repository import GLib
from threading import Thread
from dbus.mainloop.glib import DBusGMainLoop


WPAS_DBUS_NEW_SERVICE = 'fi.w1.wpa_supplicant1'
WPAS_DBUS_NEW_PATH = '/fi/w1/wpa_supplicant1'
WPAS_DBUS_NEW_INTERFACE = 'fi.w1.wpa_supplicant1'
WPAS_DBUS_NEW_PATH_INTERFACES = WPAS_DBUS_NEW_PATH + '/Interfaces'
WPAS_DBUS_NEW_IFACE_INTERFACE = WPAS_DBUS_NEW_INTERFACE + '.Interface'
WPAS_DBUS_NEW_IFACE_WPS = WPAS_DBUS_NEW_INTERFACE + '.WPS'
WPAS_DBUS_NEW_IFACE_NETWORK = WPAS_DBUS_NEW_INTERFACE + '.Network'
WPAS_DBUS_NEW_IFACE_BSS = WPAS_DBUS_NEW_INTERFACE + '.BSS'


_loop = GLib.MainLoop()
_bus = None
_wpas_obj = None
_wpas = None
_main_loop_thread = None


def setup_wpas_dbus_iface():
    """Setup global wpa_supplicant dbus connection objects."""

    global _loop, _bus, _wpas_obj, _wpas

    if _bus is None:
        _bus = dbus.SystemBus()

    if _wpas_obj is None:
        _wpas_obj = _bus.get_object(WPAS_DBUS_NEW_SERVICE, WPAS_DBUS_NEW_PATH)

    if _wpas is None:
        _wpas = dbus.Interface(_wpas_obj, WPAS_DBUS_NEW_INTERFACE)


def get_dbus_type(value):
    """Type mapping from python built-in types to dbus types."""

    if isinstance(valui, bool):
        return dbus.Boolean
    elif isinstance(value, int):
        return dbus.Int32
    elif isinstance(value, str):
        return dbus.String
    elif isinstance(value, dict):
        return dbus.Dictionary


def get_wpas_dbus_iface_property(name):
    """Get wpa_supplicant property via dbus."""

    return _wpas.Get(WPAS_DBUS_NEW_INTERFACE, name,
                     dbus_interface=dbus.PROPERTIES_IFACE)


def set_wpas_dbus_iface_property(name, value):
    """Set wpa_supplicant property via dbus."""

    func = get_dbus_type(value)
    return _wpas.Set(WPAS_DBUS_NEW_INTERFACE, name,
                     func(value), dbus_interface=dbus.PROPERTIES_IFACE)


def get_wpas_iface_dbus_iface_property(iface, name):
    """Get specific wlan interface property via dbus."""

    return iface.Get(WPAS_DBUS_NEW_IFACE_INTERFACE, name,
                     dbus_interface=dbus.PROPERTIES_IFACE)


def set_wpas_iface_dbus_iface_property(iface, name, value):
    """Set specific wlan interface property via dbus."""

    func = get_dbus_type(value)

    return iface.Set(WPAS_DBUS_NEW_IFACE_INTERFACE, name,
                     func(value), dbus_interface=dbus.PROPERTIES_IFACE)


def setup_wpas_iface_dbus_iface_by_name(wlan_name):
    """Setup wpa_supplicant dbus connection for specific wlan interface."""

    global _wpas, _bus

    iface_path = _wpas.GetInterface(wlan_name)
    iface_obj = _bus.get_object(WPAS_DBUS_NEW_SERVICE, _iface_path)
    iface = dbus.Interface(_iface_obj, WPAS_DBUS_NEW_IFACE_INTERFACE)

    return iface_path, iface_obj, iface


def setup_wpas_bss_dbus_iface(bss_path):
    """Setup wpa_supplicant dbus connection for specific bss."""

    global _bus

    bss_obj = _bus.get_object(WPAS_DBUS_NEW_SERVICE, bss_path)
    bss = dbus.Interface(bss_obj, WPAS_DBUS_NEW_IFACE_BSS)

    return bss


def setup_wpas_network_dbus_iface(network_path):
    """Setup wpa_supplicant dbus connection for specific network."""

    global _bus

    network_obj = _bus.get_object(WPAS_DBUS_NEW_SERVICE, network_path)
    network = dbus.Interface(network_obj, WPAS_DBUS_NEW_IFACE_NETWORK)

    return network


def setup_wpas_iface_dbus_iface_by_obj_path(iface_path):
    """Setup wpa_supplicant dbus connection for specific wlan interface."""

    global _wpas, _bus

    iface_obj = _bus.get_object(WPAS_DBUS_NEW_SERVICE, iface_path)
    iface = dbus.Interface(iface_obj, WPAS_DBUS_NEW_IFACE_INTERFACE)

    return iface_obj, iface


def scan(iface):
    """Run scan on specific wlan."""

    return iface.Scan({'Type': 'active'})


def add_network(iface, params):
    """Add network profile on specific wlan."""

    return iface.AddNetwork(params)


def select_network(iface, path):
    """Connect to specified network via specific wlan."""

    return iface.SelectNetwork(path)


def remove_all_networks(iface):
    """Remove all network profiles of specific wlan."""

    iface.RemoveAllNetworks()


def disconnect(iface):
    """Remove all network profiles of specific wlan."""

    iface.Disconnect()


def status(iface):
    """Remove all network profiles of specific wlan."""
    return get_wpas_iface_dbus_iface_property(iface, 'State')


def wpas_dbus_mainloop():

    DBusGMainLoop(set_as_default=True)
    setup_wpas_dbus_iface()
    _loop.run()


def init(wlan_name):
    """Init function for starting working with wpa_supplicant dbus."""

    _main_loop_thread = Thread(target=wpas_dbus_mainloop)
    _main_loop_thread.start()

    while(_loop.is_running() is False):
        pass


def deinit():
    """Deinit function for stopping working with wpa_supplicant dbus."""

    _loop.quit()


def scanDone(success):
    pass


def bssRemoved(bss):
    pass


def bssAdded(bss, props):
    pass


def register_signals(wlan_name):
    """Register signal handlers for specific wlan."""

    iface_path = _wpas.GetInterface(wlan_name)

    _bus.add_signal_receiver(scanDone,
                             dbus_interface=WPAS_DBUS_NEW_IFACE_INTERFACE,
                             signal_name="ScanDone", path=iface_path)
    _bus.add_signal_receiver(bssRemoved,
                             dbus_interface=WPAS_DBUS_NEW_IFACE_INTERFACE,
                             signal_name="BSSRemoved", path=iface_path)
    _bus.add_signal_receiver(bssAdded,
                             dbus_interface=WPAS_DBUS_NEW_IFACE_INTERFACE,
                             signal_name="BSSAdded", path=iface_path)
