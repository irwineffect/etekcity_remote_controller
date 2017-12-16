#!/usr/bin/python

if __name__ == "__main__":
    f = open("remote_raw", "r")

    line = f.readline()
    while line:
        if (line[0] == '>'):
            p1 = f.readline()
            p2 = f.readline()
            if(p1 != p2):
                print "\"{}\" does not match!".format(line[1:].rstrip('\n'))
        line = f.readline()

    f.close()
