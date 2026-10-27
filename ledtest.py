import time
from machine import Pin
recv_pin = Pin(16, Pin.OUT)
send_pin = Pin(17, Pin.OUT)

while True:
    recv_pin.value(1)
    send_pin.value(0)
    time.sleep(1)
    recv_pin.value(0)
    send_pin.value(1)
    time.sleep(1)