#!/usr/bin/python
import flask
import socket
import subprocess
app = flask.Flask(__name__)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

@app.route("/", methods=['GET', 'POST'])
def main():
    global s
    print(flask.request.method)
    if flask.request.method == 'POST':
        request = list(flask.request.form.keys())[0]
        request_parts = request.split(":")
        request_type = request_parts[0]
        if request_type == "etekcity":
            channel = int(request_parts[1])
            state = flask.request.form[request]
            print("CH{} {}".format(channel, state))
            packet = chr(int(channel)) + chr(1 if state == "ON" else 0)
            s.sendto(packet.encode("ascii"), ('localhost', 1666))
        if request_type == "livingroomtv":
            action = request_parts[1]
            if action == "power_all":
                command = "irsend --address=charmander.lan SEND_ONCE emerson KEY_POWER".split(" ")
                subprocess.run(command)

                command = "irsend --address=charmander.lan SEND_ONCE isymphony KEY_POWER".split(" ")
                subprocess.run(command)

            if action == "power_tv":
                command = "irsend --address=charmander.lan SEND_ONCE emerson KEY_POWER".split(" ")
                subprocess.run(command)

            if action == "power_stereo":
                command = "irsend --address=charmander.lan SEND_ONCE isymphony KEY_POWER".split(" ")
                subprocess.run(command)

            if action == "volumeup":
                command = "irsend --address=charmander.lan SEND_ONCE isymphony KEY_VOLUMEUP".split(" ")
                subprocess.run(command)

            if action == "volumedown":
                command = "irsend --address=charmander.lan SEND_ONCE isymphony KEY_VOLUMEDOWN".split(" ")
                subprocess.run(command)

    return flask.render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
