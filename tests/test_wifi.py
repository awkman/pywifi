#coding=utf-8
import pywifi
import time
A = 41
n = 3.7
wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]
iface.scan()
result=iface.scan_results()
time.sleep(2)

for i in range(len(result)):
    SSID = result[i].ssid
    SIGNAL = result[i].signal
    RSSI = SIGNAL
    if SSID != "" :
        print(str(SSID) + ' ' + str(SIGNAL) + " %.2f" % length + ' m')