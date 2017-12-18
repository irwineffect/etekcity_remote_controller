#!/usr/bin/python
import argparse
import serial
from arduino_interface import RemoteInterface

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="Command line interface for controlling etekcity remote"
            "controlled outlets",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("channel", type=int, help="which channel to control")
    parser.add_argument("state", type=str, help="valid inputs: 1/on, 0/off")
    parser.add_argument("--port", type=str, default="/dev/ttyACM0",
            help="port that arduino is connected")
    args = parser.parse_args()

    channel = args.channel
    state = args.state.upper()

    state_map = { "0": 0,
                  "OFF": 0,

                  "1": 1,
                  "ON": 1
                }

    if state not in state_map:
        print "invalid state: {}".format(state)
        exit(1)
    state = state_map[state]

    serial = serial.Serial(args.port)
    interface = RemoteInterface(serial)

    print "setting channel {} to {}".format(channel, "ON" if state else "OFF")

    interface.set_state(channel, state)
