# vim: set fileencoding=utf-8

import platform
from iface import Interface

if platform.system().lower() == 'windows':
    import win.wifiutils as wifiutils
elif platform.system().lower() == 'linux':
    import linux.wifiutils as wifiutils


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
