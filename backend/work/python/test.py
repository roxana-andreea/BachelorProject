#!/usr/bin/python3
# comment

import serial
import time
import logging

class MyModem():
    def __init__(self, pin):
        self.pin = pin
        self.timeout = 2

    def sendAT(self, cmd, expect, timeout)


    def powerOn():


    def start(self):
        # logging.debug("Starting...")
        time.sleep(3)


class MySmsClass:
    def __init__(self, recipient, message):
        self.recipient = recipient
        self.message = message

    def connect(self):
        # - Speed (baud rate): 115200
        # - Bits: 8
        # - Parity: None
        # - Stop Bits: 1
        # - Flow Control: None
        self.ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=5, xonxoff=False, rtscts=False, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
        time.sleep(1)

    def status(self):
        self.ser.write(bytes('AT\r', 'UTF-8'))
#        reply=self.
        print(reply)

    def debug(self):
        print("A SMS will be sent to %s with the content: '%s'" % (self.recipient, self.message))

logging.basicConfig(filename='test.log',level=logging.DEBUG)
sms = MySmsClass("1234", "Hello, this is a snippet.")
sms.debug()
sms.connect()
sms.status()
