from .consts import *
import xml.etree.ElementTree as ET

auth_dict = {
    'OPEN': AUTH_ALG_OPEN,
    'SHARED':AUTH_ALG_SHARED,
    'WPA':AUTH_ALG_WPA,
    'WPAPSK': AUTH_ALG_WPAPSK,
    'WPA2': AUTH_ALG_WPA2,
    'WPA2PSK':AUTH_ALG_WPA2PSK,
    'OTHER': AUTH_ALG_UNKNOWN
}

cryp_dict = {
    'NONE':AUTH_CRYP_NONE,
    'WEP':AUTH_CRYP_WEP,
    'TKIP' : AUTH_CRYP_TKIP,
    'AES' : AUTH_CYPT_AES,
    'OTHER':AUTH_CRYP_UNKOWN
}

class Profile():

    def _init_(self):
        #Set everything to defaults 
        self.auth_type = AUTH_ALG_OPEN
        self.cryp_type = AUTH_CRYP_NONE
        self.ssid = None
        self.bssid = None
        self.sharedkey = None
        
    def set_profile_from_xml(xml):
        tree = ET.from_string(xml)
        
        