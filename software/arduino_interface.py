#!/usr/bin/python

class RemoteInterface():
    def __init__(self, serial):
        self.serial = serial
        self.preamble = "01000101010101"
        self.on_off_codes = { 0: "1100",
                              1: "0011"
                            }
        self.channel_codes = { 1: "010011",
                               2: "011100",
                               3: "110000",
                               4: "010000",
                               5: "010000"
                             }

    def all_off(self):
        self.set_state([1,2,3,4,5], 0)

    # channel can be an array, or a single element
    def set_state(self, channels, state):
        if type(channels) is not list:
            channels = [channels]

        if state not in self.on_off_codes:
            raise ValueError("invalid state: {}".format(state))

        for channel in channels:
            if channel not in self.channel_codes:
                raise ValueError("invalid channel: {},"
                        " valid channels are [1-5]".format(channel))

            code = self._gen_code(channel, state)

            if self.serial is None:
                print code
            else:
                self.serial.write(code)


    def _gen_code(self, channel, state):
        return self.preamble + \
               self.channel_codes[channel] + \
               self.on_off_codes[state] + \
               "0" + chr(0)

if __name__ == "__main__":
    from serial import Serial
    import time
    s = Serial("/dev/ttyACM0")
    r = RemoteInterface(s)
    r.set_state(1, 1)
    time.sleep(5);
    r.set_state(1, 0)

