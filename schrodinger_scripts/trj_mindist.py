from schrodinger.application.desmond.packages import traj_util, topo
from schrodinger.structutils import measure
import numpy as np
import matplotlib.pyplot as plt
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Get the closest distance between selected groups")
    parser.add_argument("cms", help="Input cms file")
    parser.add_argument("g1", help="Define group1 ASL", metavar='ASL')
    parser.add_argument("g2", help="Define group2 ASL", metavar='ASL')
    parser.add_argument("-p", "--plot", help="Plot results")
    parser.add_argument("-o", "--output", help="Output filename")

    args = parser.parse_args()

    msys, cms, trj = traj_util.read_cms_and_traj(args.cms)

    g1_aids = cms.select_atom(args.g1)
    g1_st = cms.extract(g1_aids)
    g1_gids = topo.aids2gids(cms, g1_aids)

    g2_aids = cms.select_atom(args.g2)
    g2_st = cms.extract(g2_aids)
    g2_gids = topo.aids2gids(cms, g2_aids)

    distances = []
    info = []
    for fr in trj:
        g1_st.setXYZ(fr.pos(g1_gids))
        g2_st.setXYZ(fr.pos(g2_gids))
        res = measure.get_shortest_distance(g1_st, st2=g2_st)
        distances.append(res[0])
        a1 = list(g1_st.atom)[res[1]]
        a2 = list(g2_st.atom)[res[2]]
        info.append([f"{a1.pdbres} {a1.resnum}", f"{a2.pdbres} {a2.resnum}"])

    if args.plot:
        plt.plot(distances)
        plt.xlabel("Frame index")
        plt.ylabel("Distance (Å)")
        plt.show(block=False)

    out = args.output if args.output else sys.stdout
    with open(out) as fh:
        for f, d, i in enumerate(zip(distances, info)):
            fh.write(f"{f:<4} {i[0]} - {i[1]}: {d}")

if __name__ == "__main__":
    main()
