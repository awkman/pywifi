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
    length = pow(10, ((abs(RSSI) - A) / (10 * n)))
    '''
    if SSID != "NWPU-WLAN":
        if SSID != "NWPU-CHANGAN":
            if SSID != "CMCC-EDU":
                if SSID != "CMCC-xbgy":
                    if SSID != "CMCC-freegame" :
    '''
    if SSID != "" :
        print(str(SSID) + ' ' + str(SIGNAL) + " %.2f" % length + ' m')


    '''length=pow(10,((abs(RSSI) - A) / (10 * n)))
    print(SSID+' '+str(SIGNAL)+" %.2f" % length + ' m')
    #d - 计算所得距离(单位：m)
    #rssi - 接收信号强度
    #A - 发射端和接收端相隔1米时的信号强度
    #n - 环境衰减因子'''
