import regex
import argparse
import math


def parse_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("logfile", help="MD logfile")
    parser.add_argument("-t", "--time", default=-1, type=float,
                        help="Return the left-closest frame to time TIME")
    parser.add_argument("-f", "--frame", default=-1, type=int,
                        help="Return the time of the given FRAME")
    return parser.parse_args()


def logparser(logfile):
    with open(logfile, 'r') as lf:
        log = [line.strip() for line in lf.readlines()]

    last_time = 1
    elapsed_time = 0
    step = 'none'
    intraj = False

    for line in log:

        if 'last_time =' in line:
            last_time = float(regex.search(
                r'last_time = "(.*)"', line).group(1))

        if 'elapsed_time =' in line:
            elapsed_time = float(regex.search(
                r'elapsed_time = "(.*)"', line).group(1))

        if 'trajectory = {' in line:
            intraj = True

        if intraj and 'interval =' in line:
            step = float(regex.search(r'interval = "(.*)"', line).group(1))

        if intraj and '}' in line:
            intraj = False

    frames = math.ceil((last_time - elapsed_time) / step)

    return last_time, elapsed_time, step, frames


def main():
    args = parse_input()
    last_time, elapsed_time, step, frames = logparser(args.logfile)
    print()
    print('LAST_TIME    = ', last_time)
    print('ELAPSED_TIME = ', elapsed_time)
    print('STEP         = ', step)
    print('FRAMES       = ', frames)
    print()

    # t = t0 + dt * f
    # frames = (te - t0) / dt
    # dt = (te - t0) / frames
    # f = (t - t0) / dt

    if args.time >= 0:
        print('Nearest frame to time %.2f ps is %d'
              % (args.time, math.floor((args.time - elapsed_time) / step)))

    if args.frame >= 0:
        print('Chemical time of frame %d is %.2f ps'
              % (args.frame, elapsed_time + step * args.frame))

    print()

if __name__ == "__main__":
    main()
