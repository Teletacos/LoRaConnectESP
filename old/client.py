import json
from time import sleep
from lib.ulora import LoRa, ModemConfig, SPIConfig

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
lora = LoRa(RFM95_SPIBUS, RFM95_INT, CLIENT_ADDRESS, RFM95_CS,
            reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True)
        

# loop and send data
while True:
    data = {"first": 2, "second": 3}
    encode_data = json.dumps(data).encode('utf-8')
    lora.send_to_wait(encode_data, SERVER_ADDRESS)
    print("sent")
    sleep(10)