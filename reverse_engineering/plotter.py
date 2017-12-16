#!/usr/bin/python

class plotter():
    def __init__(self):
        self.o1 = list()
        self.o2 = list()
        self.o3 = list()
        self.o4 = list()

    def _clear_lines(self):
        self.o1 = list()
        self.o2 = list()
        self.o3 = list()
        self.o4 = list()

    def _insert_null(self):
        self.o1.append("      ")
        self.o2.append("      ")
        self.o3.append("      ")
        self.o4.append("______")

    def plot(self, pattern):
        self._clear_lines()
        self._insert_null()
        for i in pattern:
            if i == 's':
                self.o1.append(" _    ")
                self.o2.append("| |   ")
                self.o3.append("| |   ")
                self.o4.append("| |___")
            elif i == 'w':
                self.o1.append(" ___  ")
                self.o2.append("|   | ")
                self.o3.append("|   | ")
                self.o4.append("|   |_")

        self._insert_null()
        print "{}\n{}\n{}\n{}".format("".join(self.o1),
                                      "".join(self.o2),
                                      "".join(self.o3),
                                      "".join(self.o4))


if __name__ == "__main__":
    p = plotter()
    p.plot("swssswswswswswwwsssswwsss")

