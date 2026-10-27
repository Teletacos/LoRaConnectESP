import network
import config

def run():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=config.WIFI_SSID, password=config.WIFI_PASS, hidden=False, max_clients=1, channel=6)

    while not ap.active():
        pass

    print('Wi-Fi Connection successful')
    print(ap.ifconfig())