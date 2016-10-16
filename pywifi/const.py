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
AUTH_ALG_WPAPSK = 2
AUTH_ALG_WPA2PSK = 3

# Define profile types.
PROFILE_USER_ADD = 0
PROFILE_SCANNED = 1
PROFILE_SYSTEM_STORED = 2
