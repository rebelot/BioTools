#!/usr/bin/env python

import sys
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdb", help="pdb input file")
    parser.add_argument("-b", "--base-number", type=int, default=0,
                        help="offset base number from which renumbering starts")
    parser.add_argument("-t", "--res-type",
                        choices=["atom", "het"], default="atom",
                        help="choose which residues to renumber")
    parser.add_argument("-o1k", "--over-1k", action="store_true", help="if checked, \
                        residuse > 1000 will not be renumbered from 1")

    args = parser.parse_args()

    pdbin = args.pdb
    basenum = args.base_number
    restype = args.res_type
    o1k = args.over_1k

    pdbin = open(pdbin, 'r')

    if restype == "atom":
        restype = "ATOM"
    elif restype == "het":
        restype = "HETA"
    elif restype == "all":
        restype = ("ATOM", "HETA")

    newresnum = basenum
    oldresnum = 0

    firsresidue = True
    for line in pdbin.readlines():
        if line[0:4] in restype:
            resnum = int(line[22:26])

            if firsresidue:
                oldresnum = resnum
                firsresidue = False

            if resnum != oldresnum:
                newresnum += 1
                oldresnum = resnum

            if newresnum > 9999:
                sys.stderr.write("WARNING: residues > 10000")
                newresnum = resnum if o1k else 0

            sys.stdout.write(line[:22] + "{:>4}".format(newresnum) + line[26:])

        else:
            sys.stdout.write(line)


if __name__ == '__main__':
    main()
