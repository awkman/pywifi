# vim: set fileencoding=utf-8

import platform

if platform.system().lower() == 'windows':
    import win.wifiutils as wifiutils
elif platform.system().lower() == 'linux':
    import linux.wifiutils as wifiutils


class Interface:
    """Interface provides basic methods for manipulating wifi interfaces."""

    """
    For encapsulating os dependent behavior, we declare __raw_obj here for
    storing some common attribute (e.g. name) and os attributes (e.g. dbus
    objects for linux)
    """
    __raw_obj = {}

    def __init__(self, raw_obj):

        self.__raw_obj = raw_obj

    def name(self):
        """"Get the name of the wifi interfacce."""

        return self.__raw_obj['name']

    def scan(self):
        """Trigger the wifi interface to scan."""

        wifiutils.scan(self.__raw_obj)

    def scan_results(self):
        """Return the scan result."""

        return wifiutils.scan_results(self.__raw_obj)

    def add_network_profile(self, params):
        """Add the info of the AP for connecting afterward."""

        wifiutils.add_network_profile(self.__raw_obj, params)

    def remove_network_profile(self, **kwargs):
        """Remove the specified AP settings."""

        wifiutils.remove_network_profile(self.__raw_obj, kwargs)

    def remove_all_network_profiles(self):
        """Remove all the AP settings."""

        wifiutils.remove_all_network_profiles(self.__raw_obj)

    def network_profiles(self):
        """Get all the AP profiles."""

        return wifiutils.network_profiles(self.__raw_obj)

    def connect(self, params):
        """Connect to the specified AP."""

        wifiutils.connect(self.__raw_obj, params)

    def disconnect(self):
        """Disconnect from the specified AP."""

        wifiutils.disconnect(self.__raw_obj)

    def status(self):
        """Get the status of the wifi interface."""

        return wifiutils.status(self.__raw_obj)
