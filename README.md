# BioTools

A collection of bioinformatics tools.

## Contents:

### getfasta

Creates a .fasta file containing the sequence of [PROT_ID], where PROT_ID is a UniProt accession number

    Usage: getfasta [PROT_ID]

### getpdb
 
Creates a .pdb file containing the coordinates of [PROT_ID] atoms, where PROT_ID is a PDB accession number

    Usage: getpdb [PROT_ID]

### pdbrenumber

renumbers residues of a .pdb file. Residues which number is > 10000 are renumbered starting from 1.

```
usage: pdbrenumber [-h] [-b BASE_NUMBER] [-t {atom,het}] [-o1k] pdb

positional arguments:
  pdb                   pdb input file

optional arguments:
  -h, --help            show this help message and exit
  -b BASE_NUMBER, --base-number BASE_NUMBER
                        offset base number from which renumbering starts
  -t {atom,het}, --res-type {atom,het}
                        choose which residues to renumber
  -o1k, --over-1k       if checked, residues > 1000 will not be renumbered
                        from 1
```

### pyAlign
 
Align 2 sequences given as UniProt accession number identifiers.
Alignment score and other informations are printed to stderr, the aligned sequences are printed to stdout in .fasta format.

    Usage:
        pyAlign [-hvr] seq1 seq2 [g_op=[-10] g_ex=[-1] mat=[b62]/pam250/custom]
    Opts:
        h: print this message and return
        v: verbose (display calling configuration in stderr)
        r: remove fasta files

example:

    pyAlign P01308 P01315
    
    [||||||||||||||||||||] 100.00%  line 108 of 109 column 110 of 111
    Identity: 0.8545454545454545
    Score: 484.0
    
    > P01308
    MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN

    > P01315
    MALWTRLLPLLALLALWAPAPAQAFVNQHLCGSHLVEALYLVCGERGFFYTPKARREAENPQAGAVELGG--GLGGLQALALEGPPQKRGIVEQCCTSICSLYQLENYCN

### pyNJ

Draws a phyolegenetic tree using the Neighbour Join methd. It is interactive and user may choose different options.

    Usage:
    $ pyNJ

### pyDotplot

Draws a dot-plot matrix of an alignment, it's interactive.
    
    Usage:
    $ python pyDotplot.py

### cAlign

Perform pairwise alignments using a C backend. Interactive.

    Usage:
    $ python cAlign.py


## SCHRODINGER scripts

### Desmond progress bar

Trace the course of a molecular dynamics using `desmond_progress_bar.sh *.log` into the job directory.

### trj_boxinfo.py

Report box dimensions over simulation time. (useful for (semi-)anisotropic coupling)

### trj_extralc.sh

Pipeline to extract, align and center a MD.

### trj_interactions.py

Track hydrogen bonds and salt bridges over MD simulation.

### trj_query.py

Query basic informations from MD log file.

### trj_fcluster.py

Cluster trajectory frames using scipy

### trj_mindist

Find shortest distance between groups of atoms

### trj_periodic_shortest_distance.py

Find shortest distance between groups of atoms, honor PBCs

### maestro script: Center of Mass

Places a dummy atom at the center of mass of selected atoms.

### maestro script: Transform

Perform workspace cartesian transformations; the tool provides ways to define reference points and axes to rotate or translate selected atoms.

### maestro script: Interacting

Select interacting (hbond or saltbr) residues within groups

### maestro script: B-Select

Select residues which B-factor is above a certain threshold or N residues with the highest B-factor within specified group.

### "$SCHRODINGER/run" completions for zsh

An extensible incipit for the `$SCHRODINGER/run` command tab-completion for zsh. Add it to `$fpath` and make sure completions are enabled. Requires a proxy script named `schrun` in your path: `echo '$SCHRODINGER/run "$@"' > schrun`.

