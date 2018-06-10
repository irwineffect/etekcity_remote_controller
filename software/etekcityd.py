#!/usr/bin/python
import logging
import time
import serial
from arduino_interface import RemoteInterface
import socket

class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        #self.stderr_path = "/var/log/etekcityd.log"
        self.pidfile_path = '/var/run/etekcityd/etekcityd.pid'
        self.pidfile_timeout = 5

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        #logging = logging.Logger()
        logging.basicConfig(level=logging.DEBUG)
        #self.handler = logging.FileHandler("/var/log/etekcityd.log")
        #self.handler.setFormatter(formatter)
        #logging.addHandler(self.handler)

    def run(self):
        logging.debug("opening serial port")
        s = serial.Serial("/dev/ttyACM0")
        logging.debug("creating arduino interface")
        interface = RemoteInterface(s)
        logging.debug("opening udp socket")
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", 1666))
        logging.info("etekcityd started on port 1666")
        while True:
            logging.debug("waiting to receive UDP data")
            data, addr = s.recvfrom(2)
            logging.debug("received UDP data")
            data = [ord(x) for x in data]
            logging.info("received {}".format(data))
            [channel, state] = data
            logging.debug("calling interface.set_state()")
            interface.set_state(channel, state)
            logging.debug("finished calling interface.set_state()")


if __name__ == "__main__":
    app = App()
    app.run()
