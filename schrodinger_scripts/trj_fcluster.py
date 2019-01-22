from schrodinger.application.desmond.packages import topo, traj, traj_util, analysis
from schrodinger.structure import StructureWriter
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
import numpy as np
from scipy.spatial.distance import pdist
import argparse
import sys

def main():
    args = argparse.ArgumentParser(description="Perform RMSD-based clustering of a Desmond MD")
    args.add_argument('cms', help="Cms input file")
    args.add_argument('out', help="Output base name")
    args.add_argument('rmsd', help="Define ASL for RMSD calculation")
    args.add_argument('-fit', help="Define ASL for fitting")
    args.add_argument('-n', help="Max number of clusters")
    args.add_argument('-s', help="Split trajectory in sub trajectories containing frames of each cluster", action="store_true")
    args.add_argument('-pre', help="Speed up calculation if using prealigned (fitted) traj, or if fitting is not required", action="store_true")
    args.add_argument('-tree', help="View cluster dendrogram and exit", action="store_true")
    args.add_argument('-save', help="Store intermediate distance matrix", default=False)
    args.add_argument('-restore', help="Load intermediate distance matrix from file", default=False)
    args = args.parse_args()

    # read trajectory
    msys, cms, trj = traj_util.read_cms_and_traj(args.cms)

    # specify atoms to consider form rmsd calc and fitting
    rmsd_aids = cms.select_atom(args.rmsd)
    rmsd_gids = topo.aids2gids(cms, rmsd_aids, include_pseudoatoms=False)

    system_asl = cms.select_atom('all')
    system_gids = topo.aids2gids(cms, system_asl, include_pseudoatoms=False)

    # calc. distance matrix
    if args.restore:
        rmsd_matrix = np.fromfile(args.restore)
        rmsd_matrix.reshape(int(np.sqrt(len(rmsd_matrix))), int(np.sqrt(len(rmsd_matrix))))

    elif args.pre:
        f = len(traj)
        rmsd_matrix = np.empty((f,f))
        pos = np.array([fr.pos(rmsd_gids) for fr in traj])
        tot = f * (f - 1) / 2
        c = 0
        for i in range(f):
            ref = pos[i]
            for j in range(i):
                rmsd_matrix[i,j] = np.sqrt(np.sum(pdist(ref - pos[j])))
                rmsd_matrix[j,i] = rmsd_matrix[i,j]
                c += 1
                sys.stderr.write(f"\r{c}/{tot} ({c/tot:.5%})")

    else:
        fit_aids = cms.select_atom(args.fit)
        fit_gids = topo.aids2gids(cms, fit_aids, include_pseudoatoms=False)
        rmsd_matrix = analysis.rmsd_matrix(msys, trj, rmsd_gids, fit_gids)

    if args.save:
        rmsd_matrix.tofile(args.save)

    # Clustering with scipy
    y = squareform(rmsd_matrix)
    Z = linkage(y, method='complete')
    labels = fcluster(Z, args.n, 'maxclust')
    
    if args.tree:
        dendrogram(Z)
        return

    clusters = []
    centroids = []
    for i in range(1, args.n + 1):
        # Get the frame indexes from cluster labels
        elements = np.where(labels == i)[0]

        # Avoid storing empty lists
        if len(elements) > 0:
            clusters.append(elements)
            # Get the centroids by individuating the element with the minimum distance to
            # every other element of the same cluster
            c = np.argmin(np.sum(rmsd_matrix[elements, :][elements], axis=1))
            centroids.append(elements[c])

    for i,elements in enumerate(clusters):
        traj.write_traj(trj[elements], f"{args.out}_{i}_trj")

    for i,centroid in enumerate(centroids):
        cms.setXYZ(trj[centroid].getpos()).write("f{args.out}_{i}-out.mae")
        

if __name__ == "__main__":
    main()
