from time import sleep
import gc
from machine import Pin
from lib.ulora import LoRa, ModemConfig, SPIConfig
import asyncio

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
        self.queue = []
        self.queue_running = False
    
    def on_recv(self, payload):
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
            print("Writing:", packet.content)
        else:
            print("Not writing message")

        gc.collect()

    def transmit_message(self, message, chat_id, recv_id):
        self.lora.set_mode_tx()
        packet = LoraPacket(message.id, chat_id, message.content)
        ack = self.lora.send_to_wait(packet.encode(), recv_id)
        if ack:
            print("Ack")
            message.status = Message.SENT
            data_handler.set_message(message, chat_id)
        self.lora.set_mode_rx()
        return ack
        
    def send_message(self, message, chat_id, recv_id):
        data_handler.add_message(message, chat_id)
        self.queue.append([message, chat_id, recv_id, 0])

    async def send_queue(self):
        while True:
            if len(self.queue) > 0:
                message, chat_id, recv_id, counter = self.queue[0]
                ack = self.transmit_message(message, chat_id, recv_id)
                if ack:
                    self.queue.pop(0)
                else:
                    self.queue[0] = [message, chat_id, recv_id, counter+1]
                    print("Retrying: ", counter+1)
                await asyncio.sleep(5 * pow(2, counter))
            else:
                await asyncio.sleep_ms(100)