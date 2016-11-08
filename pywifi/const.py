#!/usr/bin/env python3
# vim: set fileencoding=utf-8

"""Constants used in pywifi library define here."""

# Define interface status.
IFACE_DISCONNECTED = 0
IFACE_SCANNING = 1
IFACE_INACTIVE = 2
IFACE_CONNECTING = 3
IFACE_CONNECTED = 4

# Define auth algorithms.
AUTH_ALG_OPEN = 0
AUTH_ALG_SHARED = 1

# Define auth key mgmt types.
AKM_TYPE_NONE = 0
AKM_TYPE_WPA = 1
AKM_TYPE_WPAPSK = 2
AKM_TYPE_WPA2 = 3
AKM_TYPE_WPA2PSK = 4
AKM_TYPE_UNKNOWN = 5

# Define ciphers.
CIPHER_TYPE_NONE = 0
CIPHER_TYPE_WEP = 1
CIPHER_TYPE_TKIP = 2
CIPHER_TYPE_CCMP = 3
CIPHER_TYPE_UNKNOWN = 4

KEY_TYPE_NETWORKKEY = 0
KEY_TYPE_PASSPHRASE = 1
