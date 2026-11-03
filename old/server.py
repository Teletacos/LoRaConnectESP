import json
from time import sleep
from lib.ulora import LoRa, ModemConfig, SPIConfig
from machine import UART

# This is our callback function that runs when a message is received
def on_recv(payload):
    print("From:", payload.header_from)
    print("Received:", payload.message)
    encoded_data = payload.message
    data = json.loads(encoded_data)
    print(data)
    print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))

# Lora Parameters
RFM95_RST = 18
RFM95_SPIBUS = SPIConfig.esp32_1
RFM95_CS = 19
RFM95_INT = 27
RF95_FREQ = 868.0
RF95_POW = 20
CLIENT_ADDRESS = 1
SERVER_ADDRESS = 2

# initialise radio
lora = LoRa(RFM95_SPIBUS, RFM95_INT, SERVER_ADDRESS, RFM95_CS, 
            reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True)

# set callback
lora.on_recv = on_recv

# set to listen continuously
lora.set_mode_rx()

# loop and wait for data
while True:
    sleep(0.1)