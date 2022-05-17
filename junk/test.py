#!/usr/bin/env python3
import pickle
from gather import Position
from gather import Device
from gather import Data

with open('test.txt', 'rb') as in_file:
    positions = pickle.load(in_file)
print(positions)
