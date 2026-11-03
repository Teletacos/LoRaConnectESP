from time import sleep
from machine import Pin
from lib.ulora import LoRa, ModemConfig, SPIConfig

from classes.lora_packet import LoraPacket
import classes.database.data_handler as data_handler
import classes.database.data_formatter as data_formatter

# Lora Parameters
RFM95_RST = 18
RFM95_SPIBUS = SPIConfig.esp32_1
RFM95_CS = 19
RFM95_INT = 27
RF95_FREQ = 868.0
RF95_POW = 20

# Debug Paramaters
RECV_LED_PIN = 16
SEND_LED_PIN = 17

class LoraSender():
    def __init__(self, sender_id):
        self.lora = LoRa(RFM95_SPIBUS, RFM95_INT, sender_id, RFM95_CS,
                        reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True)
        self.lora.on_recv = self.on_recv
        self.lora.set_mode_rx()
        self.recv_led_pin = Pin(RECV_LED_PIN, Pin.OUT)
        self.send_led_pin = Pin(SEND_LED_PIN, Pin.OUT)
    
    def on_recv(self, payload):
        self.recv_led_pin.value(1)
        sender_id = payload.header_from
        packet = LoraPacket(encoded=payload.message)
        print(packet.message.content)
        data_handler.add_message(packet.message, packet.chat_id)
        print("From:", payload.header_from)
        print("Received:", payload.message)
        print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))
        sleep(1)
        self.recv_led_pin.value(0)

    def send_message(self, message, chat_id, recv_id):
        self.lora.set_mode_tx()
        packet = LoraPacket(message=message, chat_id=chat_id)
        self.send_led_pin.value(1)
        ack = self.lora.send_to_wait(packet.encode(), recv_id)
        if ack:
            print("Ack")
            data_handler.add_message(message, chat_id)
        else:
            print("No Ack")
        self.send_led_pin.value(0)
        self.lora.set_mode_rx()
        return ack