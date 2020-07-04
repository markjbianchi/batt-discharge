#!/usr/bin/env python3
import argparse
import csv
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import datetime as dt

parser = argparse.ArgumentParser(description='Plots battery discharge CSV log')
parser.add_argument('csv_file', help='discharger log file to plot')
parser.add_argument('--line_skips', type=int, default=0, help='number of input lines skipped per output line')
parser.add_argument('--volts_only', action='store_true', help='strips out coulomb data')
parser.add_argument('--yaxis', type=str, help='comma-separated list of battery numbers to plot (e.g., --yaxis=0,2,5)')
args = parser.parse_args()

if args.yaxis is None:
    yaxis = [i for i in range(8)]
else:
    yaxis = [int(i) for i in args.yaxis.split(',')]
in_data = np.genfromtxt(args.csv_file, delimiter=',')
epoch_converter = np.vectorize(dt.datetime.fromtimestamp)
time = epoch_converter(in_data[1:, 0])
skip = args.line_skips + 1
volts = in_data[1::skip, 1:17:2]
coulombs = in_data[1::skip, 2:17:2]

with open(args.csv_file, newline='') as csv_file:
    row = next(csv.reader(csv_file))
    legend_t = row[0]
    legend_v = row[1:17:2]
    legend_c = row[2:17:2]

fig = plt.figure()
if args.volts_only:
    gs = fig.add_gridspec(1, 1)
else:
    gs = fig.add_gridspec(2, 1)

axv = fig.add_subplot(gs[0, 0])
for i, (col, leg) in enumerate(zip(volts.T, legend_v)):
    if i in yaxis:
        axv.plot(time, col, label=leg)
axv.set_title('CR2450 Discharge Curves')
axv.set_ylabel('Battery Voltage (V)')
axv.set_ylim(ymin=1.9, ymax=3.1)
axv.legend(loc='best')
axv.grid(True)

if not args.volts_only:
    axc = fig.add_subplot(gs[1, 0])     # , sharex=True)
    for i, (col, leg) in enumerate(zip(coulombs.T, legend_c)):
        if i in yaxis:
            axc.plot(time, col, label=leg)
    axc.set_ylabel('Battery Charge (C)')
    axc.set_xlabel('Date')
    axc.legend(loc='best')
    axc.grid(True)

style.use('ggplot')
fig.tight_layout()
plt.show()
