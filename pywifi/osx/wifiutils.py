#!/usr/bin/env python3
# vim: set fileencoding=utf-8

from . import osx_wifiutil



def scan(obj):
    """Trigger the wifi interface to scan."""

    osx_wifiutil.scan(obj['name'])


def scan_results(obj):
    """Get the AP list after scanning."""

    return osx_wifiutil.scan_results()


def interfaces():
    """Get the wifi interface lists."""

    ifaces = []
    tmp_ifaces = osx_wifiutil.get_interfaces()
    for interface in tmp_ifaces:
        iface = {}
        iface['name'] = interface
        ifaces.append(iface)

    return ifaces
