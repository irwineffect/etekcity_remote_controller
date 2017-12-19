#!/usr/bin/python
import logging
from daemon import runner
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

        self.logger = logging.getLogger("DaemonLog")
        self.logger.setLevel(logging.INFO)
        self.handler = logging.FileHandler("/var/log/etekcityd.log")
        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)

    def run(self):
        self.logger.debug("opening serial port")
        s = serial.Serial("/dev/ttyACM0")
        self.logger.debug("creating arduino interface")
        interface = RemoteInterface(s)
        self.logger.debug("opening udp socket")
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", 1666))
        self.logger.info("etekcityd started on port 1666")
        while True:
            data, addr = s.recvfrom(2)
            data = [ord(x) for x in data]
            self.logger.info("received {}".format(data))
            [channel, state] = data
            interface.set_state(channel, state)


if __name__ == "__main__":
    app = App()
    daemon_runner = runner.DaemonRunner(app)
    daemon_runner.daemon_context.files_preserve=[app.handler.stream]
    daemon_runner.do_action()
