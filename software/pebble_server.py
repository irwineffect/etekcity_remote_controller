#!/usr/bin/env python

"""
A simple echo server
"""

import socket

host = ''
port = 5000
backlog = 5
size = 1024
current_channel = 1

def extract_button(msg):
    button_line = msg.split('\n')[-1]
    if "button=" in button_line:
        if "undefined" in button_line:
            return 0
        return int(button_line[-1])
    else:
        return None

def process_message(msg, sender):
    global current_channel
    button = extract_button(msg)
    if button == 0:
        current_channel = 1
        print "current channel: {}".format(current_channel)
    elif button == 2:
        current_channel += 1
        print "current channel: {}".format(current_channel)
    elif button == 1:
        packet = chr(current_channel) + chr(1)
        print "setting channel {} to {}".format(current_channel, "ON")
        sender.sendto(packet, ('192.168.1.13', 1666))
    elif button == 3:
        packet = chr(current_channel) + chr(0)
        print "setting channel {} to {}".format(current_channel, "OFF")
        sender.sendto(packet, ('192.168.1.13', 1666))
    else:
        print "malformed packet:\n{}".format(msg)
        return

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host,port))
    s.listen(backlog)

    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print "pebble controller server initialized"

    while 1:
        client, address = s.accept()
        #print "got a connection"
        data = client.recv(size)
        if data:
            """
            print "----"
            print data
            print "----"
            """
            process_message(data, sender)


        client.close()
