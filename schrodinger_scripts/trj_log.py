#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, time, re

def main():
    LOGFILE = sys.argv[1]

    try:
        fh = open(LOGFILE, 'r')
        LOG = fh.readlines()
    except FileNotFoundError:
        print(LOGFILE, 'does not exist')

    m = re.findall(r'last_time.*=.*\d', ' '.join(LOG))[0]
    TIME = float(m.split()[-1].replace('"', '')) / 1000

    while True:
        # fh = open(LOGFILE, 'r')
        LOG = fh.readlines()
        try:
            current_line = re.match('Chemical time:', LOG[-1])
            if current_line:
                line = LOG[-1].split()
                CT = float(line[2])/1000
                V = float(line[-1])
                COMP = CT/TIME
                SEC_LEFT = round(24 * 3600 * (TIME - CT)/V)
                DAY = SEC_LEFT/86400
                HRS = SEC_LEFT/2600%24
                MIN = SEC_LEFT%3600/60
                SEC = SEC_LEFT%60
                ETA = f'{DAY:02.0f}d:{HRS:02.0f}h:{MIN:02.0f}m:{SEC:02.0f}s'
                print(f'Completion: {CT:.2f} of {TIME} ns ({COMP:.2%})  @ {V} ns/day     ETA: {ETA:15s}\r', end='')
        except IndexError:
            continue

        time.sleep(1)

if __name__ == "__main__":
    main()
