#!/usr/bin/env python3
import argparse
import csv


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Filters battery discharge log, outputting reduced data set')
    parser.add_argument('csv_file', help='discharger log file to filter')
    parser.add_argument('--line_skips', type=int, default=0, help='number of input lines skipped per output line')
    parser.add_argument('--volts_only', action='store_true', help='strips out coulomb data')
    args = parser.parse_args()

    skip = args.line_skips + 1
    with open(args.csv_file, newline='') as csv_file:
        reader = csv.reader(csv_file)
        for count, row in enumerate(reader, start=1):
            if count % skip == 0:
                if args.volts_only:
                    print(', '.join([row[0]] + row[1::2]))
                else:
                    print(', '.join(row))

