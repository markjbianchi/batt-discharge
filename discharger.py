import signal
import time
import sys
import argparse
import csv
import labjackU3
import json


def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)
    try:
        if input("\nReally quit? (y/n)> ").lower().startswith('y'):
            sys.exit(1)
    except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)
    # restore the exit gracefully handler here
    signal.signal(signal.SIGINT, exit_gracefully)


def configure_lj(cfg):
    pass


def run_program(cfg):
    '''
    Print setup, config, etc. Prompt to start or quit.
    '''
    while True:
        time.sleep(1)
        print("a")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Controls LabJack U3-HV to')
    # store the original SIGINT handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    with open('default_cfg.json') as cfg_file:
        cfg = json.load(cfg_file)
    configure_lj(cfg)
    run_program(cfg)

