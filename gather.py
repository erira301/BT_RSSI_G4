import os
import re
import math
import pickle


class Position:
    """Parent class to hold all data."""

    def __init__(self):
        """Class constructor."""
        self.x = 0
        self.y = 0
        self.devices = []

    def fill_device(self, address, arr):
        """Get data from parsing and fill object."""
        aux = Device()
        aux.address = address
        aux.dongle_positions()
        aux.data.values = arr
        self.devices.append(aux)
        self.calculate_angle()
        self.calculate_distance()

    def calculate_angle(self):
        """Calculate angle based on device and dongle position."""
        for dongle in self.devices:
            x = self.x - dongle.dongle_x
            y = self.y - dongle.dongle_y
            if x == 0 and y > 0:
                angle = 90
            elif x == 0 and y < 0:
                angle = 270
            else:
                angle = math.degrees(math.atan(y/x))
            if x < 0:
                angle += 180
            dongle.data.angle = angle

    def calculate_distance(self):
        """Calcualate distance from dongle to device."""
        for dongle in self.devices:
            x = self.x - dongle.dongle_x
            y = self.y - dongle.dongle_y
            distance = math.sqrt((x * x) + (y * y))
            dongle.data.distance = distance


class Device:
    """Stores address of beacon and data gathered by it."""

    def __init__(self):
        """Class constructor."""
        self.address = ""
        self.dongle_x = 0
        self.dongle_y = 0
        self.data = Data()

    def dongle_positions(self):
        """Give dongles their position."""
        if("C7:BA:15:02:28:C8" in self.address):
            self.dongle_x = 0
            self.dongle_y = 0
        if("FE:02:1F:D7:24:3B" in self.address):
            self.dongle_x = 300
            self.dongle_y = 0
        if("E6:46:27:42:FE:55" in self.address):
            self.dongle_x = 0
            self.dongle_y = 300
        if("E4:FA:69:C7:1B:EF" in self.address):
            self.dongle_x = 300
            self.dongle_y = 300


class Data:
    """Stores RSSI values, similates AoA and stores it."""

    def __init__(self):
        """Class constructor."""
        self.values = []
        self.angle = 0
        self.disance = 0


def get_object(fullobject):
    """TODO will be used to send filled object to other python files or just to save into a doc format."""
    return fullobject


def line_to_array(line):
    """Change the incoming string of RSSI values into an array of ints."""
    aux = line.split(",")
    if "\n" in aux[-1]:
        aux[-1] = aux[-1][:-1]
    aux = list(map(int, aux))
    aux = [i * -1 for i in aux]
    aux = [aux[i:i + 50] for i in range(0, len(aux), 50)]
    return aux


def read_file(file_path, file_name):
    """Read data off the file puts it into Position object."""
    aux_pos = Position()
    re_search = re.search("x([0-9]*)y([0-9]*).*", file_name)
    if re_search:
        aux_pos.x = int(re_search.group(1))
        aux_pos.y = int(re_search.group(2))
    f = open(file_path, "r")
    for i in range(4):
        addr = f.readline()  # address
        values = f.readline()  # rssi array
        aux_array = line_to_array(values)
        aux_pos.fill_device(addr, aux_array)
    return aux_pos


positions = []


def main():
    """Program main function."""
    print("1: Log data \n2: View data  \n0: Exit")
    op = input()
    while op != "0":
        if op == "1":
            aux_position = Position()
            for file_name in os.listdir("Processed"):
                file_path = os.path.join("Processed", file_name)
                if os.path.isfile(file_path):
                    aux_position = read_file(file_path, file_name[:-4])
                    positions.append(aux_position)
            print("\n1: Log data \n2: View data  \n0: Exit")
            op = input()

        if op == "2":
            print("")
            for pos in positions:
                print("---------")
                print("Position: X =", pos.x, "Y = ", pos.y)
                print("Devices:")
                for device in pos.devices:
                    print(device.address, "X: ", device.dongle_x,
                          " Y: ", device.dongle_y)
                    print("Angle: ", device.data.angle)
                    print("Distance from device: ", device.data.distance)
                    # print(device.data.values)

            print("\n1: Log data \n2: View data  \n0: Exit")
            op = input()
        if op == "3":
            with open("test.txt", "wb") as out_file:
                pickle.dump(positions, out_file)

            with open('test.txt', 'rb') as in_file:
                positions2 = pickle.load(in_file)
            if(positions == positions2):
                print("success")

            print("\n1: Log data \n2: View data  \n0: Exit")
            op = input()
        if op == "0":
            break


main()
