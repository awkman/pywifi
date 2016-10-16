PyWiFi
======

PyWiFi provides a cross-platform Python module for manipulating wireless
interfaces.

* Easy to use
* Supports Windows and Linux

Prerequisites
-------------

On Linux, you will need to install GLib_, which provides PyGI and
GObject-Introspection in order to query DBus to determine wireless interfaces.

On Windows, the `Native Wifi`_ component comes with Windows versions greater
than Windows XP SP2.

Installation
------------

After installing the prerequisites listed above for your platform, you can
use pip to install from source:

::

    cd pywifi/
    pip install .
    
Example
-------------

::

    import pywifi

    wifi = pywifi.PyWiFi()

    iface = wifi.interfaces()[0]

    iface.disconnect()
    time.sleep(1)
    assert iface.status() in\
        [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

    profile = {'ssid': 'testap',
               'key_mgmt': pywifi.const.AUTH_ALG_WPA2PSK,
               'psk': '12345678'}

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)

    iface.connect(tmp_profile)
    time.sleep(30)
    assert iface.status() == const.IFACE_CONNECTED

    iface.disconnect()
    time.sleep(1)
    assert iface.status() in\
        [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

    
\(C) Jiang Sheng-Jhih 2016, `MIT License`_.

.. _GLib: https://developer.gnome.org/glib/
.. _Native Wifi: https://msdn.microsoft.com/en-us/library/windows/desktop/ms706556.aspx
.. _MIT License: https://opensource.org/licenses/MIT
