from schrodinger.application.desmond.packages import traj_util, traj, topo
from schrodinger.application.desmond.packages.msys import pfx as pfx_module
from tqdm import tqdm
import typing
import numpy as np
import argparse
from argparse import RawDescriptionHelpFormatter


def main():
    parser = argparse.ArgumentParser(description='''
Get this fancy visualization of stuff interacting with membranes:
 - the protein is centered on the XY plane
 - the membrane layers are pushed at the extremes of the Z dimension
(Note that the output cms will be unchanged, the re-wrapping only affects frames)

        |||||||||||||||||||
        ooooooooooooooooooo

             ~protein~

        oooooooooooooooooooo
        ||||||||||||||||||||''', formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('cms', help='Input cms file')
    parser.add_argument('trj', help='Input trajectory dir')
    parser.add_argument('out', help='output basename')
    parser.add_argument('-asl', help='What should be centered on the XY plane, default is protein', default='protein')
    args = parser.parse_args()

    msys, cms = topo.read_cms(args.cms)
    trj: typing.List[traj.Frame] = traj.read_traj(args.trj)

    pfx = pfx_module.Pfx(msys.glued_topology, fixbonds=True)

    membrane_gids = topo.aids2gids(cms, cms.select_atom('membrane'))
    protein_gids = topo.aids2gids(cms, cms.select_atom(args.asl))

    # 1) center the membrane along Z axis
    topo.center(msys, membrane_gids, trj, dims=[2])

    # 2) center the protein on the XY plane
    topo.center(msys, protein_gids, trj, dims=[0, 1])

    # 3) shift all the atoms in the simulation box up by half the length of the Z axis, then re-wrap
    for fr in tqdm(trj):
        z_mid = fr.box[-1,-1] / 2
        fr.moveby(0, 0, z_mid)
        pfx.apply(fr.pos(), fr.box, fr.vel()) # <- Kung Fu. This also makes the system whole (see topo.make_whole docstring)

    traj.write_traj(trj, args.out + '_trj')
    cms.property['s_chorus_trajectory_file'] = args.out + '_trj'
    cms.write(args.out + '-out.cms')

if __name__ == "__main__":
    main()
