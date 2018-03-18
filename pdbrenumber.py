#!/usr/bin/env python

import sys
import os

def main():
    try:                                                # check if there are arguments
        pdbin_name = sys.argv[1]
        if pdbin_name in ("-h", "--help", "-help"):
            print("pdbrenumber source.pdb [out.pdb]")
            return 0
    except:                                             # if no arguments, return usage
        print("pdbrenumber source.pdb [out.pdb]")
        return 1

    pdbin = open(pdbin_name, 'r')                       # open pdb for reading

    try:                                                # check for output name in arguments
        pdbout_name = sys.argv[2]
        try:                                                # try to create the given filename
            pdbout = open(pdbout_name, 'x')
        except FileExistsError:                             # if file already exists, erase it and replace it
            os.remove(pdbout_name)
            pdbout = open(pdbout_name, 'x')

    except IndexError:                                  # if no output filename is given, write to stdout
        pdbout = sys.stdout

    newresnum = 0
    oldresnum = 0

    firsresidue = True
    for line in pdbin.readlines():
        if 'ATOM' == line[0:4]:                         # select ATOM coordinates lines
            resnum = line[22:26]

            if firsresidue:                             # executed only for the first loop cycle
                oldresnum = resnum                      # initialize oldresnum with the first residue number
                firsresidue = False

            if resnum != oldresnum:                     # if the current residue number is different from the previous
                newresnum += 1                          # then a new residue is encountered and oldresnum is updated
                oldresnum = resnum

            if newresnum > 9999:                        # if more than 10000 residues are encountered, start renumbering
                print("WARNING: residues > 10000")
                newresnum = 0

            pdbout.write(line[:22] + "{:>4}".format(newresnum) + line[26:])

        else:
            pdbout.write(line)

if __name__ == '__main__':
    main()