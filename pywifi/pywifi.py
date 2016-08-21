#!/usr/bin/env python3
# vim: set fileencoding=utf-8

import platform
from .iface import Interface

if platform.system().lower() == 'windows':
    from .win import wifiutils
elif platform.system().lower() == 'linux':
    from .linux import wifiutils


class PyWiFi:
    """PyWiFi provides operations to manipulate wifi devices."""

    __ifaces = []

    def interfaces(self):
        """Collect the available wlan interfaces."""

        __ifaces = []

        for interface in wifiutils.interfaces():
            iface = Interface(interface)
            self.__ifaces.append(iface)

        return self.__ifaces
