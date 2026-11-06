from time import sleep
from machine import Pin
from lib.ulora import LoRa, ModemConfig, SPIConfig

from classes.database.message import Message
from classes.lora_packet import LoraPacket
import classes.database.data_handler as data_handler
import classes.database.data_formatter as data_formatter

# Lora Parameters
RFM95_RST = 18
RFM95_SPIBUS = SPIConfig.esp32_1
RFM95_CS = 19
RFM95_INT = 27
RF95_FREQ = 868.0
RF95_POW = 5

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
        try:
            packet = LoraPacket(encoded=payload.message)
        except Exception as e:
            packet = None
            print("Failed to decode message")

        if packet:
            message = Message({
                "id": packet.message_id,
                "sender_id": sender_id,
                "content": packet.content,
                "status": Message.RECEIVED,
            })
            data_handler.add_message(message, packet.chat_id)
            print("Writing:", packet.message.content)
            sleep(1)
            self.recv_led_pin.value(0)
        else:
            print("Not writing message")
        

    def send_message(self, message, chat_id, recv_id):
        self.lora.set_mode_tx()
        self.send_led_pin.value(1)
        packet = LoraPacket(message.id, chat_id, message.content)
        ack = self.lora.send_to_wait(packet.encode(), recv_id)
        if ack:
            print("ACK")
            message.status = Message.SENT
            data_handler.add_message(message, chat_id)
        else:
            print("NO ACK")
            message.status = Message.FAILED
            data_handler.add_message(message, chat_id)
        self.send_led_pin.value(0)
        self.lora.set_mode_rx()
        return ack