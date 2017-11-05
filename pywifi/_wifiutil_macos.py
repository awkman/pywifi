#!/usr/bin/env python3
# vim: set fileencoding=utf-8

"""Implementations of wifi functions of Linux."""

import logging
import objc

from .const import *
from .profile import Profile


CWSecurityNone = 0
CWSecurityWPA = 7
CWSecurityWPA2 = 9
CWSecurityWPAPSK = 2
CWSecurityWPA2PSK = 4

kCWInterfaceStateInactive = 0
kCWInterfaceStateScanning = 1
kCWInterfaceStateAuthenticating = 2
kCWInterfaceStateAssociating = 3
kCWInterfaceStateRunning = 4

status_dict = {
    kCWInterfaceStateRunning: IFACE_CONNECTED,
    kCWInterfaceStateInactive: IFACE_INACTIVE,
    kCWInterfaceStateAuthenticating: IFACE_CONNECTING,
    kCWInterfaceStateAssociating: IFACE_CONNECTING,
    kCWInterfaceStateScanning: IFACE_SCANNING,
}

objc.loadBundle('CoreWLAN', bundle_path = '/System/Library/Frameworks/CoreWLAN.framework', module_globals = globals())

class WifiUtil():
    """WifiUtil implements the wifi functions in Linux."""

    _connections = {}
    _logger = logging.getLogger('pywifi')

    def scan(self, obj):
        """Trigger the wifi interface to scan."""

        iface = self._get_interface(obj['name'])
        iface.scanForNetworksWithName_error_(None, None)


    def scan_results(self, obj):
        """Get the AP list after scanning."""

        iface = self._get_interface(obj['name'])
        raw_networks = iface.cachedScanResults()
        bsses = []

        for raw_network in raw_networks:
            bss = Profile()
            bss.bssid = raw_network.bssid()
            bss.freq = raw_network.wlanChannel().channelNumber()
            bss.signal = raw_network.rssiValue()
            bss.ssid = raw_network.ssid()
            bss.akm = []

            if raw_network.supportsSecurity_(CWSecurityWPAPSK):
                bss.akm.append(AKM_TYPE_WPAPSK)
            if raw_network.supportsSecurity_(CWSecurityWPA2PSK):
                bss.akm.append(AKM_TYPE_WPA2PSK)
            if raw_network.supportsSecurity_(CWSecurityWPA):
                bss.akm.append(AKM_TYPE_WPA)
            if raw_network.supportsSecurity_(CWSecurityWPA2):
                bss.akm.append(AKM_TYPE_WPA2)

            bss.auth = AUTH_ALG_OPEN

            bsses.append(bss)

        return bsses

    def connect(self, obj, network):
        """Connect to the specified AP."""

        iface = self._get_interface(obj['name'])
        raw_networks = iface.cachedScanResults()

        for raw_network in raw_networks:
            if raw_network.ssid() == network.ssid:
                result = iface.associateToNetwork_password_error_(raw_network, network.key, None)
                break

    def disconnect(self, obj):
        """Disconnect to the specified AP."""

        iface = self._get_interface(obj['name'])
        iface.disassociate()

    def add_network_profile(self, obj, params):
        """Add an AP profile for connecting to afterward."""

        iface = self._get_interface(obj['name'])
        configuration = iface.configuration()
        orig_profiles = configuration.networkProfiles()
        orig_mutable_profiles = NSMutableOrderedSet.alloc().initWithOrderedSet_(orig_profiles)
        ssid_bytes = str.encode(params.ssid)
        ssid_data = NSData.dataWithBytes_length_(ssid_bytes, len(ssid_bytes))
        profile = CWMutableNetworkProfile.alloc().init()
        profile.setSsidData_(ssid_bytes)
        profile.setSecurity_(4)
        orig_mutable_profiles.addObject_(profile)
        configuration.setNetworkProfiles_(orig_mutable_profiles)
        result = iface.commitConfiguration_authorization_error_(configuration, None, None)

        return params

    def network_profiles(self, obj):
        """Get AP profiles."""

        iface = self._get_interface(obj['name'])
        raw_networks = iface.configuration().networkProfiles()

        bsses = []

        for i in range(0, raw_networks.count()):
            bss = Profile()
            bss.ssid = raw_networks.objectAtIndex_(i).ssid()
            bss.akm = []

            if raw_networks.objectAtIndex_(i).security() == CWSecurityWPAPSK:
                bss.akm.append(AKM_TYPE_WPAPSK)
            if raw_networks.objectAtIndex_(i).security() == CWSecurityWPA2PSK:
                bss.akm.append(AKM_TYPE_WPA2PSK)
            if raw_networks.objectAtIndex_(i).security() == CWSecurityWPA:
                bss.akm.append(AKM_TYPE_WPA)
            if raw_networks.objectAtIndex_(i).security() == CWSecurityWPA2:
                bss.akm.append(AKM_TYPE_WPA2)

            bss.auth = AUTH_ALG_OPEN

            bsses.append(bss)

        return bsses


    def remove_all_network_profiles(self, obj):
        """Remove all the AP profiles."""

        iface = self._get_interface(obj['name'])
        configuration_copy = iface.configuration()
        configuration_copy.setNetworkProfiles_(None)
        result = iface.commitConfiguration_authorization_error_(configuration_copy, None, None)

    def status(self, obj):
        """Get the wifi interface status."""

        iface = self._get_interface(obj['name'])
        return status_dict[iface.interfaceState()]

    def interfaces(self):
        """Get the wifi interface lists."""
        
        ifaces = []
        for f in CWWiFiClient.interfaceNames():
            iface = {}
            iface['name'] = f
            ifaces.append(iface)

        return ifaces

    def _get_interface(self, iface_name):

        return CWInterface.interface()
