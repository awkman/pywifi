# PyWiFi

PyWiFi is a module providing APIs to manipulating wifi interface on the platform.

  - Support Windows, Linux now
  - Easy to use
 
### Version
0.9.3

### Tech

PyWifi is developed based on:

* [Wpa_supplicant] - PyWiFi control wifi interface via the dbus service of wpa_supplicant in Linux platform. 
* [Native WiFi API] - PyWiFi adopt the Windows Native WiFi API to manipulating wifi interface

### ToDo

- public to pip
- Add the event-based scan done notification
- Add Apple Mac support

### Example

```python
import pywifi

wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]

profile = {'ssid': 'testap',
           'key_mgmt': 'wpa2psk',
           'psk': 'testap'}

iface.remove_all_network_profiles()
iface.add_network_profile(profile)
networks = iface.network_profiles()

iface.connect(networks[0])
time.sleep(5)
assert iface.status() == 'connected'

iface.disconnect()
```

License
----

MIT
