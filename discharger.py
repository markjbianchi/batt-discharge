#!/usr/bin/env python3
import signal
import sys
import argparse
import time
import json
import BattDischarge


def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in input when CTRL+C is pressed, and the signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)
    try:
        print("\nReally quit? (y/n) ", end='', file=sys.stderr)
        if input().lower().startswith('y'):
            cleanup()
            sys.exit(1)
    except KeyboardInterrupt:
        print("Ok ok, quitting", file=sys.stderr)
        cleanup()
        sys.exit(1)
    # restore the exit gracefully handler here
    signal.signal(signal.SIGINT, exit_gracefully)


def cleanup():
    # Turn off all loads and anything else to LJ
    bd.disable_all_loads()
    bd.close()


def enable_loads(dacq, chan):
    for idx, dic in enumerate(chan):
        if dic.get('enabled'):
            dacq.enable_load(idx)


def measure_channels(dacq, chan, secs, coul):
    volt = []
    for idx, dic in enumerate(chan):
        v, i = dacq.measure_channel(idx)
        volt.append(v)
        coul[idx] += i * secs
    return volt, coul


def monitor_cutoffs(dacq, chan, v, coul):
    for idx, dic in enumerate(chan):
        if v[idx] < dic.get('cutoff_v') or coul[idx] > dic.get('cutoff_c'):
            dacq.disable_load(idx)


def output_measurements(v, c):
    print('{}'.format(int(time.time())), end='')
    for vv, cc in zip(v, c):
        print(',{:.3f},{:.3f}'.format(vv, cc), end='')
    print('')
    sys.stdout.flush()


def initialize_configs(cfg_file, drain_file):
    chan = []
    with open(cfg_file) as cf:
        cfg = json.load(cf)
    for dic in cfg.get('channels'):
        chan.append(dict(dic))
    c = [0] * len(chan)
    if drain_file is not None:
        with open(drain_file) as df:
            drain = json.load(df)
        for idx, cc in enumerate(drain.get('coulombs')):
            c[idx] = cc
    return chan, c, cfg.get('period_secs')


if __name__ == '__main__':
    # store the original SIGINT handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)

    parser = argparse.ArgumentParser(description='Discharges batteries to fixed cutoffs using LabJack U3-HV')
    parser.add_argument('cfg_file', help='configuration file to set up data acquisition')
    parser.add_argument('drain_init', nargs='?', help='file containing previous drain amounts')
    parser.add_argument('--dry_run', action='store_true', help='option flag to just show output without discharging')
    args = parser.parse_args()

    # Use supplied config file to initialize an array of channel specifiers,
    # and coulomb counter array.
    channels, coulombs, period = initialize_configs(args.cfg_file, args.drain_init)
    num_chan = len(channels)

    bd = BattDischarge.BattDischarge(channels)
    bd.disable_all_loads()

    # Take an initial measurement and print it; if not a dry run, enable the loads.
    # Then enter loop which measures V & I and computes cumulative charge drawn.
    volts, coulombs = measure_channels(bd, channels, 0, coulombs)
    output_measurements(volts, coulombs)
    if not args.dry_run:
        enable_loads(bd, channels)
    while True:
        time.sleep(period)
        volts, coulombs = measure_channels(bd, channels, period, coulombs)
        output_measurements(volts, coulombs)
        monitor_cutoffs(bd, channels, volts, coulombs)
