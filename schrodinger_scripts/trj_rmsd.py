#!/opt/schrodinger/suites2018-4/run

from schrodinger.application.desmond.packages import traj_util, topo
from schrodinger.structutils import rmsd, transform
import argparse
import numpy as np
import matplotlib.pyplot as plt
import sys

def main():
    parser = argparse.ArgumentParser(description="Calculate RMSD of selected atoms over the course of MD simulation.")
    parser.add_argument('cms', help="Input cms file.")
    parser.add_argument('-rmsd', help="Atom selection for RMSD calculation")
    parser.add_argument('-fit', help="Atom selection for superposition")
    parser.add_argument('-o', help="Output filename.")
    parser.add_argument('-p', help="Plot results", action='store_true')
    args = parser.parse_args()

    msys, cms, trj = traj_util.read_cms_and_traj(args.cms)

    rmsd_aids = cms.select_atom(args.rmsd)
    rmsd_gids = topo.aids2gids(cms, rmsd_aids)
    ref_rmsd_st = cms.extract(rmsd_aids)

    fit_aids = cms.select_atom(args.fit)
    fit_gids = topo.aids2gids(cms, fit_aids)
    ref_fit_st = cms.extract(fit_aids)

    cur_rmsd_st = ref_rmsd_st.copy()
    cur_fit_st = ref_fit_st.copy()

    rmsd_atoms = list(range(1, ref_rmsd_st.atom_total + 1))
    fit_atoms = list(range(1, ref_fit_st.atom_total + 1))

    n = len(trj)
    RMSD = []
    for fr in trj:
        cur_rmsd_st.setXYZ(fr.pos(rmsd_gids))
        cur_fit_st.setXYZ(fr.pos(fit_gids))
        if args.fit:
            R = rmsd.get_super_transformation_matrix(ref_fit_st, fit_atoms, cur_fit_st, fit_atoms)
            transform.transform_structure(cur_rmsd_st, R)
        res = rmsd.calculate_in_place_rmsd(ref_rmsd_st, rmsd_atoms, cur_rmsd_st, rmsd_atoms)
        RMSD.append(res)
        sys.stderr.write(f"\rframe {fr.orig_index} of {n}")

    fh = open(args.o + '.dat', 'x') if args.o else sys.stdout

    for fr, r in zip(trj, RMSD):
        fh.write(f"{fr.time} {r}")

    if args.p:
        out = args.o + '.png' if args.o else 'rmsd_calc.png'
        plt.plot([fr.time for fr in trj], RMSD)
        plt.xlabel('time (ps)')
        plt.ylabel('RMSD (Å)')
        plt.savefig(out)


if __name__ == "__main__":
    main()
