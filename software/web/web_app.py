#!/usr/bin/python
import flask
import socket
app = flask.Flask(__name__)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

@app.route("/", methods=['GET', 'POST'])
def main():
    global s
    print flask.request.method
    if flask.request.method == 'POST':
        channel = flask.request.form.keys()[0]
        state = flask.request.form[channel]
        print "CH{} {}".format(channel, state)
        packet = chr(int(channel)) + chr(1 if state == "ON" else 0)
        s.sendto(packet, ('192.168.1.13', 1666))
    return flask.render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
