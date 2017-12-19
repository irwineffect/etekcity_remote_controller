#!/usr/bin/python
import argparse
import socket

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="Command line interface for controlling etekcity remote"
            "controlled outlets. Interfaces with etekcityd server.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("channel", type=int, help="which channel to control")
    parser.add_argument("state", type=str, help="valid inputs: 1/on, 0/off")
    parser.add_argument("--ip", type=str, default="192.168.1.13",
            help="ip address of etekcityd server")
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

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print "setting channel {} to {}".format(channel, "ON" if state else "OFF")
    packet = chr(channel) + chr(state)
    s.sendto(packet, (args.ip, 1666))
