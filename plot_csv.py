#!/usr/bin/env python3
import argparse
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

parser = argparse.ArgumentParser(description='Plots battery discharge CSV log')
parser.add_argument('csv_file', help='discharger log file to plot')
args = parser.parse_args()

in_data = np.genfromtxt(args.csv_file, delimiter=',')
epoch_converter = np.vectorize(dt.datetime.fromtimestamp)
time = epoch_converter(in_data[:, 0])
volts = in_data[:, 1:16:2]
coulombs = in_data[:, 1:16:2]

plt.plot(time, volts, label='Channel x')
plt.xlabel('Date')
plt.ylabel('Battery Voltage (V)')
plt.title('Panasonic CR2450 Discharge')
plt.legend()
plt.show()
