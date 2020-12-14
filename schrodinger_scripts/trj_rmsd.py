#!/opt/schrodinger/suites2019-3/run

from schrodinger.application.desmond.packages import traj_util, topo, traj, analysis
from schrodinger.structutils import rmsd, transform
import argparse
import numpy as np
import matplotlib.pyplot as plt
import sys

def main():
    parser = argparse.ArgumentParser(description="Calculate RMSD of selected atoms over the course of MD simulation.")
    parser.add_argument('cms', help="Input cms file.")
    parser.add_argument('trj', help="Input trajectory dir")
    parser.add_argument('-mode', help="RMSD or RMSF, default RMSD", default='RMSD')
    parser.add_argument('-s', help='Slice trajectory [START:END:STEP]')
    parser.add_argument('-rmsd', help="Atom selection for RMSD calculation, default 'a.pt CA'", default='a.pt CA')
    parser.add_argument('-fit', help="Atom selection for superposition, defaults to 'rmsd' selection")
    parser.add_argument('-ref', help="Reference frame (default 0) OR structure filename (not implemented yet)")
    parser.add_argument('-o', help="Output filename.")
    parser.add_argument('-p', help="Plot results", action='store_true')
    args = parser.parse_args()

    msys, cms = topo.read_cms(args.cms)
    trj = traj.read_traj(args.trj)

    if args.s:
        start, end, step = args.s.split(':')
        start = int(start) if start else None
        end = int(end) if end else None
        step = int(step) if step else None
        slicer = slice(start, end, step)
    else:
        slicer = slice(None)

    if args.mode.lower() == 'rmsd':
        analyzer_class = analysis.RMSD
    elif args.mode.lower() == 'rmsf':
        analyzer_class = analysis.RMSF
    else:
        raise ValueError('Unrecognized mode, specify one of (RMSD, RMSF)')

    rmsd_aids = cms.select_atom(args.rmsd)
    rmsd_gids = topo.aids2gids(cms, rmsd_aids, include_pseudoatoms=False)
    rmsd_ref_pos = trj[int(args.ref)].pos(rmsd_gids)

    fit_aids = cms.select_atom(args.fit)
    fit_gids = topo.aids2gids(cms, fit_aids, include_pseudoatoms=False)
    fit_ref_pos = trj[int(args.ref)].pos(fit_gids)

    analyzer = analyzer_class(msys, cms, rmsd_aids, rmsd_ref_pos, fit_aids, fit_ref_pos)
    res = analysis.analyze(trj[slicer], analyzer)

    fh = open(args.o + '.dat', 'x') if args.o else sys.stdout

    for fr, r in zip(trj[slicer], res):
        fh.write(f"{fr.time} {r}\n")

    if args.p:
        out = args.o + '.png' if args.o else f'{args.mode}_calc.png'
        if args.mode.lower() == 'rmsd'
            plt.plot([fr.time for fr in trj[slicer]], res)
        else: # assume RMSD
            plt.plot(res)
        plt.xlabel('time (ps)')
        plt.ylabel(f'{args.mode} (Å)')
        plt.savefig(out)


if __name__ == "__main__":
    main()
