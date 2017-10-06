# pywifi

pywifi provides a cross-platform Python module for manipulating wireless
interfaces.

* Easy to use
* Supports Windows and Linux

Now pywifi runs under python 2.7 & 3.5

## Prerequisites

On Linux, you will need to run wpa_supplicant to manipulate the wifi devices,
and then pywifi can communicate with wpa_supplicant through socket.


On Windows, the [Native Wifi] component comes with Windows versions greater
than Windows XP SP2.

## Installation

After installing the prerequisites listed above for your platform, you can
use pip to install from source:

    cd pywifi/
    pip install .

## Documentation

For the details of pywifi, please refer to [Documentation].

## Example

    import pywifi

    wifi = pywifi.PyWiFi()

    iface = wifi.interfaces()[0]

    iface.disconnect()
    time.sleep(1)
    assert iface.status() in\
        [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

    profile = pywifi.Profile()
    profile.ssid = 'testap'
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = '12345678'

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)

    iface.connect(tmp_profile)
    time.sleep(30)
    assert iface.status() == const.IFACE_CONNECTED

    iface.disconnect()
    time.sleep(1)
    assert iface.status() in\
        [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

## How to Contribute/ToDo

Following items may be done in the future:

* OS-X Support

(C) Jiang Sheng-Jhih 2017, [MIT License].

[Native Wifi]: https://msdn.microsoft.com/en-us/library/windows/desktop/ms706556.aspx
[MIT License]: https://opensource.org/licenses/MIT
[Documentation]: https://github.com/awkman/pywifi/blob/master/DOC.md
