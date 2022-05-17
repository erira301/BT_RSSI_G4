import re

from numpy import average


def read_file():
    values = {"CB:F8:7D:E4:7C:C2": [[]], "F2:F5:44:0B:A9:B3": [],
              "C9:92:F8:6D:82:7C": [], "F2:72:39:28:5A:9D": []}
    f = open("cutecom.log", "r")
    f.readline()
    f.readline()
    f.readline()
    for line in f:
        search = re.search(
            r"Device found: ([A-Z0-9:]*) \(random\) \(RSSI -([0-9]*)\)", line)
        if search:
            if(search.group(1) == "CB:F8:7D:E4:7C:C2" or search.group(1) == "F2:F5:44:0B:A9:B3" or search.group(1) == "C9:92:F8:6D:82:7C" or search.group(1) == "F2:72:39:28:5A:9D"):
                values[search.group(1)].append(int(search.group(2)))

    print("Dongle: CB:F8:7D:E4:7C:C2")
    print("RSSI:")
    print(values["CB:F8:7D:E4:7C:C2"])
    print("Average: ", average(values["CB:F8:7D:E4:7C:C2"]))
    print("\n")
    print("Dongle: F2:F5:44:0B:A9:B3")
    print("RSSI:")
    print(values["F2:F5:44:0B:A9:B3"])
    print("Average: ", average(values["F2:F5:44:0B:A9:B3"]))
    print("\n")
    print("Dongle: C9:92:F8:6D:82:7C")
    print("RSSI:")
    print(values["C9:92:F8:6D:82:7C"])
    print("Average: ", average(values["C9:92:F8:6D:82:7C"]))
    print("\n")
    print("Dongle: F2:72:39:28:5A:9D")
    print("RSSI:")
    print(values["F2:72:39:28:5A:9D"])
    print("Average: ", average(values["F2:72:39:28:5A:9D"]))


read_file()
