#!/usr/bin/env python3
import signal
import time
import sys
import argparse
import csv
import BattDischarge
import json


def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in input when CTRL+C is pressed, and the signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)
    try:
        if input("\nReally quit? (y/n)> ").lower().startswith('y'):
            cleanup()
            sys.exit(1)
    except KeyboardInterrupt:
        print("Ok ok, quitting")
        cleanup()
        sys.exit(1)
    # restore the exit gracefully handler here
    signal.signal(signal.SIGINT, exit_gracefully)


def cleanup():
    # Turn off all loads and anything else to LJ
    pass


def configure_lj(cfg):
    pass


def run_program(cfg):
    # Print setup, config, etc. Prompt to start or quit.
    while True:
        time.sleep(1)
        print("a")


if __name__ == '__main__':
    # store the original SIGINT handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)

    parser = argparse.ArgumentParser(description='Controls LabJack U3-HV to')
    parser.add_argument('cfg_file', help='configuration file to set up data acquisition')
    parser.add_argument('dischrg_init', nargs='?', default='None', help='file containing previous discharge amounts')
    parser.add_argument('--dry_run', action='store_true', help='option flag to just show output without discharging')
    args = parser.parse_args()

    with open(args.cfg_file) as cfg_file:
        cfg = json.load(cfg_file)
    configure_lj(cfg)
    run_program(cfg)

