#!/opt/schrodinger/suites2018-3/run

from schrodinger.application.desmond.packages import topo, traj_util, traj
from schrodinger.structutils import interactions
from schrodinger.protein.analysis import analyze
import matplotlib.pyplot as plt
import sys
import argparse


def cml():
    parser = argparse.ArgumentParser(
                description="""Calculate all nonbonded interactions within or
                between the specified atoms.  If group2 is given, then this
                script will return interacions between the two groups of
                atoms.  Else, nonbonded interactions within a single group of
                atoms will be returned.""")
    parser.add_argument("cms", help="Input cms file")
    parser.add_argument("-g1", help="define group 1",
                        metavar="ASL", required=1)
    parser.add_argument("-g2", help="define group 2",
                        metavar="ASL", default=None)
    parser.add_argument("-p", "--plot", help="plot bond nr over time",
                        action="store_true")
    parser.add_argument("-o", help="output filename", metavar="FILE")

    args = parser.parse_args()
    return args


def bond_counter(bonds_list):
    # there is one list for each frame, hence n = frames number
    n = len(bonds_list)
    d = {}
    for bonds in bonds_list:
        for bond in bonds:
            d.setdefault(bond, 0)
            d[bond] += 1 / n
    return d


def get_bonds_list(cms, trj, g1, g2=None):

    # Do not extract the full system if not required
    extract_asl = "({}) OR ({})".format(g1, g2) if (g1 and g2) else "all"

    extract_aids = cms.select_atom(extract_asl)
    extract_st = cms.extract(extract_aids)
    extract_gids = topo.aids2gids(cms, extract_aids, include_pseudoatoms=False)

    group1 = cms.select_atom(g1)
    group2 = cms.select_atom(g2) if g2 else g2

    salt_bridges = []
    hydrogen_bonds = []

    fnum = len(trj)

    for fr in trj:
        extract_st.setXYZ(fr.pos(extract_gids))
        saltbr = interactions.get_salt_bridges(
            extract_st, group1=group1, group2=group2)
        hbonds = analyze.hbond.get_hydrogen_bonds(
            extract_st, atoms1=group1, atoms2=group2)

        salt_bridges.append(saltbr)
        hydrogen_bonds.append(hbonds)

        sys.stdout.write('\rframe %4d of %d' % (int(fr.orig_index), fnum))
        sys.stdout.flush()

    return salt_bridges, hydrogen_bonds


def print_output(saltbr_dict, hbonds_dict, fd):

    def atmfmt(atom):
        return "{}{:<4} {} {:>10}".format(
            atom.pdbres, atom.resnum, atom.chain,
            "(" + atom.element + " " + str(atom.index) + ")")

    fd.write("\n")
    fd.write(26 * "-" + " HBONDS " + 26 * "-" + '\n')
    for bond, freq in sorted(hbonds_dict.items(), key=lambda x: x[1], reverse=True):
        fd.write("{}      ---      {}: {:>7.2%}\n".format(
            atmfmt(bond[0]), atmfmt(bond[1]), freq))

    fd.write("\n")
    fd.write(23 * "-" + " SALT BRIDGES " + 23 * "-" + '\n')
    for bond, freq in sorted(saltbr_dict.items(), key=lambda x: x[1], reverse=True):
        fd.write("{}      ---      {}: {:>7.2%}\n".format(
            atmfmt(bond[0]), atmfmt(bond[1]), freq))


def plot_data(salt_bridges, hydrogen_bonds, trj):
    fig, axs = plt.subplots(2, 1)
    axs[0].plot([fr.time for fr in trj], [
                len(bonds) for bonds in salt_bridges])
    axs[0].set_title('salt bridges')
    axs[1].plot([fr.time for fr in trj], [
                len(bonds) for bonds in hydrogen_bonds])
    axs[1].set_title('hydrogen bonds')
    plt.show()


def main():
    args = cml()

    _, cms, trj = traj_util.read_cms_and_traj(args.cms)

    salt_bridges, hydrogen_bonds = get_bonds_list(cms, trj, args.g1, args.g2)

    saltbr_dict = bond_counter(salt_bridges)
    hbonds_dict = bond_counter(hydrogen_bonds)

    fd = open(args.o, 'x') if args.o else sys.stdout
    print_output(saltbr_dict, hbonds_dict, fd)
    fd.close()

    if args.plot:
        plot_data(salt_bridges, hydrogen_bonds, trj)


if __name__ == "__main__":
    main()
