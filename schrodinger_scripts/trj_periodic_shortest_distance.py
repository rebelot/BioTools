#!/opt/schrodinger/suites2018-4/run

from schrodinger.application.desmond.packages import traj_util, topo
from scipy.spatial import distance_matrix
from schrodinger.structutils.measure import get_shortest_distance
from itertools import product
import numpy as np
import matplotlib.pyplot as plt
import sys
import argparse


def main():
    args = argparse.ArgumentParser(description='Compute the shortest distance between two sets of atoms across orthorombic PBC')
    args.add_argument('cms', help='cms input file')
    args.add_argument('-g1', help='Define first group of atoms', metavar='ASL', required=True)
    args.add_argument('-g2', help='Define second gruoup of atoms', metavar='ASL')
    args.add_argument('-o', help='Save results in file', metavar='FILE')
    args.add_argument('-p', help='Create plot')
    args.parse_args()

    msys, cms, trj = traj_util.read_cms_and_traj(args.cms)

    g1_aids = cms.select_atom(args.g1)
    g1_gids = topo.aids2gids(cms, g1_aids)
    g1_st = cms.extract(g1_aids)
    g1_atoms = list(g1_st.atom)

    g2_aids = cms.select_atom(args.g2)
    g2_gids = topo.aids2gids(cms, g2_aids)
    g2_st = cms.extract(g2_aids)
    g2_atoms = list(g2_st.atom)

    i = (-1, 1, 0)
    c = np.array(list(product(i, i, i)))


    def get_periodic_images(P, c, box):
        for c in c * box:
            yield P + c

    dist = []
    n = len(trj)
    for fr in trj:
        g1_st.setXYZ(fr.pos(g1_gids))
        dist_imgs = []
        for g2_image in get_periodic_images(fr.pos(g2_gids), fr.box.diagonal(), c):
            g2_st.setXYZ(g2_image)
            dist_imgs.append(get_shortest_distance(g1_st, st2=g2_st))
        dist.append(min(dist_imgs))
        sys.stdout.write(f'\rFrame {fr.orig_index} of {n}')

    dist = np.array(dist)
    
    out = sys.stdout if not args.o else args.o + '.dat'
    with open(out) as fh:
        for d in dist:
            fh.write(f'{d[0]} {g1_atoms[d[1]].pdbres}{g1_atoms[d[1]].resnum} {g2_atoms[d[2]].pdbres}{g2_atoms[d[2]].resnum}\n')

    if args.p:
        o = args.o if args.o else 'trj_shortes_periodic_distance'
        plt.plot([fr.time for fr in trj], dist[:,0])
        plt.xlabel('time (ps)')
        plt.ylabel('distance (Å)')
        plt.savefig(o + '.png')

if __name__ == "__main__":
    main()
