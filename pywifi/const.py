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
AUTH_ALG_WPA = 2
AUTH_ALG_WPAPSK = 3
AUTH_ALG_WPA2 = 4
AUTH_ALG_WPA2PSK = 5
AUTH_ALG_UNKNOWN = 6

# Define auth encryptions.
AUTH_CRYP_NONE = 0
AUTH_CRYP_WEP = 1
AUTH_CRYP_TKIP = 2
AUTH_CRYP_AES = 3
AUTH_CRYP_UNKNOWN = 4

KEY_TYPE_NETWORKKEY = 0
KEY_TYPE_PASSPHRASE = 1


# Define profile types.
PROFILE_USER_ADD = 0
PROFILE_SCANNED = 1
PROFILE_SYSTEM_STORED = 2
