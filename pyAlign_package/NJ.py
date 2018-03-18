def pairwise_alignment_initializer(ids_sequences):
    """
    Creates a distance matrix using the identity score returned
    by dynamic alignment for every pair of taxa.
    The Align algorithm is called by a nested function to produce a triangular matrix, which is then filled.

    :param ids_sequences: Dict in the form Taxa: Sequence
    :return: Dict distance matrix in the form (taxa_i, taxa_j): Distance
    """

    from pyAlign_package.Align import align
 
    def distance_initializer(i, j):
        """
        Calls the dynamic alignment algorithm.

        :param i: Str sequence
        :param j: Str sequence
        :return: Float distance
        """
        _, _, identity, _ = align(i, j)
        return 1 - identity

    triangular_distance_matrix = {}
    distance_matrix = {}
    for i in sorted(ids_sequences):
        for j in sorted(ids_sequences):
            if i != j and (j, i) not in distance_matrix:
                triangular_distance_matrix[(i, j)] = distance_initializer(ids_sequences[i], ids_sequences[j])
    for (i, j) in triangular_distance_matrix:
        distance_matrix[(i, j)] = triangular_distance_matrix[(i, j)]
        distance_matrix[(j, i)] = triangular_distance_matrix[(i, j)]
        distance_matrix[(i, i)] = 0.0
        distance_matrix[(j, j)] = 0.0
    return distance_matrix


def aminoacidic_composition_initializer(ids_sequences):
    """
    Creates a distance matrix considering the aminoacidic composition for every pair of taxa.
    Distance as the sum of the differences in content for a given aminoacid over its mean content in both sequences
    Dij = Sum[aa = 1, aa = 20]( |aa_i - aa_j| / 0.5*(aa_i + aa_j) )

    :param ids_sequences: Dict in the form Taxa: Sequence
    :return: Dict distance matrix in the form (taxa_i, taxa_j): Distance
    """
    def distance_initializer(i, j):
        """
        Returns a distance as the sum, for every aminoacid, of:
        the difference in aminoacidic composition for a given aminoacid between the two sequences,
        over the mean content of the given aminoacid in the two sequences.

        Dij = Sum[aa = 1, aa = 20]( |aa_i - aa_j| / 0.5*(aa_i + aa_j) )

        :param i: Str sequence
        :param j: Str sequence
        :return: Float distance
        """
        aminoacids = (
            'D', 'T', 'S', 'E',
            'P', 'G', 'A', 'C',
            'V', 'M', 'I', 'L',
            'Y', 'F', 'H', 'K',
            'R', 'W', 'Q', 'N',
            )
        a2a = 0
        tot = 0
        for aa in aminoacids:
            i_counts = i.count(aa)
            j_counts = j.count(aa)
            a2a += abs(i_counts - j_counts)
            tot += (i_counts + j_counts)/2
        return a2a/tot

    distance_matrix = {}
    for i in sorted(ids_sequences):
        for j in sorted(ids_sequences):
            distance_matrix[(i, j)] = distance_initializer(ids_sequences[i], ids_sequences[j])
    return distance_matrix


def msa_distance_initializer(ids_sequences):
    """
    Creates a distance matrix considering the number of mismatches for every pair of taxa in a multiple sequence
    alignment, over the number of residues evaluated, without considering indels.

    :param ids_sequences: Dict in the form Taxa: Sequence
    :return: Dict distance matrix in the form (taxa_i, taxa_j): Distance
    """
    def distance_initializer(i, j):
        mismatch, indel = 0, 0
        for aa_i, aa_j in zip(i,j):
            if aa_i != aa_j and '-' not in (aa_i, aa_j):
                mismatch += 1
            elif '-' in (aa_i, aa_j):
                indel += 1
        return mismatch/(max(len(i), len(j)) - indel)

    distance_matrix = {}
    for i in sorted(ids_sequences):
        for j in sorted(ids_sequences):
            distance_matrix[(i, j)] = distance_initializer(ids_sequences[i], ids_sequences[j])
    return distance_matrix


def calculate_Qmatrix(distance_matrix, nodes):
    """
    Returns the Q value for every pair of taxa.
    The Q value is proportional to the length the tree would be if ij are paired to a new node.
    (i.e. S_12 from Saitou's original algorithm).

    Qij = Dij - (ri + rj); where ri = sum[for every taxa (k)](Dik)/(n-2)
    the term n-2 is constant, therefore ...

    :param distance_matrix: Dict distance matrix in the form (taxa_i, taxa_j): Distance
    :param nodes: List of current active nodes
    :return: Dict Q Matrix in the form (taxa_i, taxa_j): Qij
    """
    n = len(nodes)
    Qmatrix = {}
    for i in nodes:
        for j in nodes:
            if i != j:
                Dij = distance_matrix[(i, j)]
                ri = sum(distance_matrix[(i, k)] for k in nodes)
                rj = sum(distance_matrix[(j, k)] for k in nodes)
                Qmatrix[(i, j)] = (n-2)*Dij - ri - rj
    return Qmatrix


def find_neighbours(Qmatrix):
    """
    Finds the the pair of taxa f, g to be joined, so that they have the minimum Q value.
    where f != g (but it's not a problem since the diagonal in not evaluated by calculate_Qmatrix func)

    :param Qmatrix: Dict Q Matrix in the form (taxa_i, taxa_j): Qij
    :return: Str taxa i, Str taxa j
    """
    minimum = min(Qmatrix.values())
    #print('MINIMUM VALUE: ', minimum)
    for (i, j) in sorted(Qmatrix):
        if Qmatrix[(i, j)] == minimum:
            #print('PAIRED: ', i, j)
            #print()
            return i, j


def paired_to_node_length(distance_matrix, f, g, nodes):
    """
    Calculates the length of the branches that connect each of the paired leaves f, g to their node u = '(f, g)'.
    Dfu = 0.5*Dfg + (Dfk - Dgk)/(2*(n-2))
    Dgu = Dfg - Dfu

    :param distance_matrix: Dict distance matrix in the form (taxa_i, taxa_j): Distance
    :param f: Str the paired taxa f
    :param g: Str the paired taxa g
    :param nodes: List of current active nodes
    :return: float Distance of each of the paired taxa from the new node: Dgu, Dfu
    """
    n = len(nodes)
    Dfg = distance_matrix[(f, g)]
    Dfk = sum(distance_matrix[(f, k)] for k in nodes)
    Dgk = sum(distance_matrix[(g, k)] for k in nodes)
    Dfu = 0.5*Dfg + (Dfk - Dgk)/(2*(n-2))
    Dgu = Dfg - Dfu
    return Dfu, Dgu


def update_distance_matrix(old_distance_matrix, f, g, new_node, nodes):
    """
    Updates the distance matrix: the paired nodes f and g are removed from the matrix, and in their place
    the new node (f, g) is considered.
    To calculate the distance from the other nodes (k) to the new node u = (f, g):
    Duk = 0.5*(Dfk + Dgk - Dfg)
    The new matrix is built as to be specular.

    :param old_distance_matrix: Dict distance matrix in the form (taxa_i, taxa_j): Distance
    :param f: Str the paired taxa f
    :param g: Str the paired taxa g
    :param new_node: Str the last defined node (f, g)
    :param nodes: List of current active nodes
    :return: Dict updated distance matrix in the form (taxa_i, taxa_j): Distance
    """
    # the new matrix won't consider f and g since they were removed from the list of nodes in tree_maker func,
    new_distance_matrix = {(i, j): old_distance_matrix[(i, j)] for i in nodes for j in nodes}
    # now the distance from every other node k to the new node is calculated
    for k in nodes:
        new_distance_matrix[(new_node, k)] = 0.5*(old_distance_matrix[(f, k)] +
                                                  old_distance_matrix[(g, k)] -
                                                  old_distance_matrix[(f, g)])

        new_distance_matrix[(k, new_node)] = 0.5*(old_distance_matrix[(f, k)] +
                                                  old_distance_matrix[(g, k)] -
                                                  old_distance_matrix[(f, g)])
    new_distance_matrix[(new_node, new_node)] = 0.0
    return new_distance_matrix


def tree_maker(distance_matrix):    # Main function
    """
        I    Initialize the Distance Matrix (input)
        II   Define the initial nodes (equal to the number of sequences) --> "star tree"
        ---------- ITERATION -------------------------------------------------------------------------------------------
        III  Calculate Q Matrix from the Distance Matrix (i.e. same as the length the tree would be if ij are joined)
        IV   Select the nodes f, g for which Qfg is the lowest value in the Q Matrix, that will form a new node "(f, g)"
        V    Calculate and record the length of the branches from each of the paired nodes to the newly defined node
        VI   Remove the paired nodes from the list of nodes
        VII  Add the new node to the list of nodes and update the distance matrix
        ---------- WHEN THE DISTANCE MATRIX CONTAINS ONLY ONE NON-JOINED NODE: STOP ITERATION ---------------------------
        VIII Complete the tree joining the last two non-joined nodes u, K with distance == DuK

    :param distance_matrix: Dict in the form (taxa_i, taxa_j): distance
    :return: Str representing the tree in Newick format
    """

    #   (ii)
    nodes = list(set(taxa[0] for taxa in distance_matrix))

    #   START ITERATION
    N = len(nodes)
    counter = 0
    while counter <= N - 3: # same as: while len(nodes) > 2:

        #print('DISTANCE MATRIX')
        #print('{:7}'.format(''), end='')
        #for j in nodes:
        #    print('{:7}'.format(j), end='')
        #print()
        #for i in nodes:
        #    print('{:.6}'.format(i), end='')
        #    for j in nodes:
        #        print('{:7.2f}'.format(distance_matrix[(i, j)]), end='')
        #    print()
        #print()

        #   (iii)
        Qmatrix = calculate_Qmatrix(distance_matrix, nodes)

        #print('QMATRIX')
        #print('{:7}'.format(''), end='')
        #for j in nodes:
        #    print('{:7}'.format(j), end='')
        #print()
        #for i in nodes:
        #    print('{:.6}'.format(i), end='')
        #    for j in nodes:
        #        if i != j:
        #            print('{:7.2f}'.format(Qmatrix[(i, j)]), end='')
        #        else:
        #            print('{:7}'.format(''), end='')
        #    print()
        #print()

        #   (iv)
        f, g = find_neighbours(Qmatrix)

        #   (v)
        Dfu, Dgu = paired_to_node_length(distance_matrix, f, g, nodes)
        new_node = '(i{0}:{2}i,i{1}:{3}i)'.format(f, g, Dfu, Dgu)
        #print('====> NEW NODE: ', new_node)

        #   (vi)
        nodes.remove(f)
        nodes.remove(g)

        #   (vii)
        distance_matrix = update_distance_matrix(distance_matrix, f, g, new_node, nodes)
        nodes.append(new_node)  # the new node is added to the list after calling the function for simplicity.

        #print('NODES: ', nodes)
        #print()

        counter += 1

        #print('END OF ITERATION: ',counter)
        #print()
    #   STOP ITERATION
    #   (viii)

    #print('DISTANCE MATRIX')
    #print('{:7}'.format(''), end='')
    #for j in nodes:
    #    print('{:7}'.format(j), end='')
    #print()
    #for i in nodes:
    #    print('{:.6}'.format(i), end='')
    #    for j in nodes:
    #        print('{:7.2f}'.format(distance_matrix[(i, j)]), end='')
    #    print()
    #print()

    #print('NODES: ', nodes)

    nodes.remove(new_node) # obsolete, the new node is always appended, but "just to be sure"
    u, K = new_node, nodes[0] # K is the last unpaired node in the list
    tree = '(i{0}i,i{1}:{2}i)i;'.format(u, K, distance_matrix[(K, u)])
    #print('TREE: ', tree)

    return tree.replace('i','\n')

if __name__ == '__main__':

    import Bio.Phylo
    import matplotlib.pyplot as plt

    sequences_raw = {                        # raw sequences
            'P02754': 'MKCLLLALALTCGAQALIVTQTMKGLDIQKVAGTWYSLAMAASDISLLDAQSAPLRVY'
                      'VEELKPTPEGDLEILLQKWENGECAQKKIIAEKTKIPAVFKIDALNENKVLVLDTDYKKY'
                      'LLFCMENSAEPEQSLACQCLVRTPEVDDEALEKFDKALKALPMHIRLSFNPTQLEEQCHI',
            'P02758': 'MKCLLLALGLALMCGIQATNIPQTMQDLDLQEVAGKWHSVAMAASDISLLDSESAPLRVY'
                      'IEKLRPTPEDNLEIILREGENKGCAEKKIFAEKTESPAEFKINYLDEDTVFALDTDYKNY'
                      'LFLCMKNAATPGQSLVCQYLARTQMVDEEIMEKFRRALQPLPGRVQIVPDLTRMAERCRI',
            'P67976': 'MKCLLLALGLALACGVQAIIVTQTMKGLDIQKVAGTWHSLAMAASDISLLDAQSAPLRVY'
                      'VEELKPTPEGNLEILLQKWENGECAQKKIIAEKTKIPAVFKIDALNENKVLVLDTDYKKY'
                      'LLFCMENSAEPEQSLACQCLVRTPEVDNEALEKFDKALKALPMHIRLAFNPTQLEGQCHV',
            'P02756': 'MKCLLLALGLALACGIQAIIVTQTMKGLDIQKVAGTWYSLAMAASDISLLDAQSAPLRVY'
                      'VEELKPTPEGNLEILLQKWENGECAQKKIIAEKTKIPAVFKIDALNENKVLVLDTDYKKY'
                      'LLFCMENSAEPEQSLACQCLVRTPEVDKEALEKFDKALKALPMHIRLAFNPTQLEGQCHV',
            'P04119': 'MRCLLLTLGLALLCGVQAVEVTPIMTELDTQKVAGTWHTVAMAVSDVSLLDAKSSPLKAY'
                      'VEGLKPTPEGDLEILLQKRENDKCAQEVLLAKKTDIPAVFKINALDENQLFLLDTDYDSH'
                      'LLLCMENSASPEHSLVCQSLARTLEVDDQIREKFEDALKTLSVPMRILPAQLEEQCRV'
            }
    sequences_msa = {                        # CLUSTAL-O MSA
            'P02754': 'MKCLLLA--LALTCGAQALIVTQTMKGLDIQKVAGTWYSLAMAASDISLLDAQSAPLRVY'
                      'VEELKPTPEGDLEILLQKWENGECAQKKIIAEKTKIPAVFKIDALNENKVLVLDTDYKKY'
                      'LLFCMENSAEPEQSLACQCLVRTPEVDDEALEKFDKALKALPMHIRLSFNPTQLEEQCHI',
            'P02758': 'MKCLLLALGLALMCGIQATNIPQTMQDLDLQEVAGKWHSVAMAASDISLLDSESAPLRVY'
                      'IEKLRPTPEDNLEIILREGENKGCAEKKIFAEKTESPAEFKINYLDEDTVFALDTDYKNY'
                      'LFLCMKNAATPGQSLVCQYLARTQMVDEEIMEKFRRALQPLPGRVQIVPDLTRMAERCRI',
            'P67976': 'MKCLLLALGLALACGVQAIIVTQTMKGLDIQKVAGTWHSLAMAASDISLLDAQSAPLRVY'
                      'VEELKPTPEGNLEILLQKWENGECAQKKIIAEKTKIPAVFKIDALNENKVLVLDTDYKKY'
                      'LLFCMENSAEPEQSLACQCLVRTPEVDNEALEKFDKALKALPMHIRLAFNPTQLEGQCHV',
            'P02756': 'MKCLLLALGLALACGIQAIIVTQTMKGLDIQKVAGTWYSLAMAASDISLLDAQSAPLRVY'
                      'VEELKPTPEGNLEILLQKWENGECAQKKIIAEKTKIPAVFKIDALNENKVLVLDTDYKKY'
                      'LLFCMENSAEPEQSLACQCLVRTPEVDKEALEKFDKALKALPMHIRLAFNPTQLEGQCHV',
            'P04119': 'MRCLLLTLGLALLCGVQAVEVTPIMTELDTQKVAGTWHTVAMAVSDVSLLDAKSSPLKAY'
                      'VEGLKPTPEGDLEILLQKRENDKCAQEVLLAKKTDIPAVFKINALDENQLFLLDTDYDSH'
                      'LLLCMENSASPEHSLVCQSLARTLEVDDQIREKFEDALKTLSVPMR--ILPAQLEEQCRV'
            }
    # Produces 3 Trees, for which different methods to produce a distance matrix are used
    print('Calculating Tree...')

    mat1 = aminoacidic_composition_initializer(sequences_raw)
    mat2 = pairwise_alignment_initializer(sequences_raw)    # Takes a while...
    mat3 = msa_distance_initializer(sequences_msa)

    TREE1 = tree_maker(mat1)
    TREE2 = tree_maker(mat2)
    TREE3 = tree_maker(mat3)

    filenames = ['aa_comp_tree', 'consensus_tree', 'msa_tree']
    TREES = [TREE1, TREE2, TREE3]
    for filename, TREE in zip(filenames, TREES):
        with open(filename+'.dnd', 'x') as tree_txt:
            tree_txt.write(TREE)
        tree = Bio.Phylo.read(filename+'.dnd', format='newick')
        Bio.Phylo.draw(tree, do_show=False)
        plt.savefig(filename+'.pdf')
    # per aggiungere un tocco di professionalità...
    print('TAAAC')
