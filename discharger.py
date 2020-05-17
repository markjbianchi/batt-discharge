#!/usr/bin/env python3
import signal
import time
import sys
import argparse
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
    bd.disable_all_loads()


def measure_channels(dacq, chan, cfg):
    return [0], [0]


def output_measurements(v, c):
    print('{}'.format(time.time()), end='')
    for vv, cc in zip(v, c):
        print(',{:.3f},{:.3f}'.format(vv, cc), end='')
    print('')


def initialize_configs(cfg_file, drain_file):
    chan = []
    with open(cfg_file) as cfg_file:
        cfg = json.load(cfg_file)
    for dic in cfg.get('channel'):
        chan.append(dict(dic))
    v = [0] * len(chan)
    c = [0] * len(chan)
    if drain_file is not None:
        with open(drain_file) as d:
            drain = json.load(drain_file)
        for idx, d in enumerate(drain.get('channels')):
            c[idx] = d.get('coulombs')
    return chan, v, c, cfg.get('period_secs')


if __name__ == '__main__':
    # store the original SIGINT handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)

    parser = argparse.ArgumentParser(description='Discharges batteries to fixed cutoffs using LabJack U3-HV')
    parser.add_argument('cfg_file', help='configuration file to set up data acquisition')
    parser.add_argument('drain_init', nargs='?', default='None', help='file containing previous drain amounts')
    parser.add_argument('--dry_run', action='store_true', help='option flag to just show output without discharging')
    args = parser.parse_args()

    # Use supplied config file to initialize an array of channel specifiers,
    # and voltage & coulomb counter arrays.
    channels, volts, coulombs, period = initialize_configs(args.cfg_file, args.drain_init)
    num_chan = len(channels)

    bd = BattDischarge.BattDischarge(channels)
    bd.disable_all_loads()

    volts, coulombs = measure_channels(bd, channels, coulombs)
    output_measurements(volts, coulombs)
    if not args.dry_run:
        enable_loads(bd, channels)
    while True:
        time.sleep(period)
        volts, coulombs = measure_channels(bd, channels, coulombs)
        output_measurements(volts, coulombs)
        monitor_cutoffs(bd, channels, volts, coulombs)

