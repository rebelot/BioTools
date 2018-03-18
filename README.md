# BioTools

A collection of useful bioinformatics tools written by me.

## Contents:

    .
    ├── getfasta
    ├── getpdb
    ├── pyAlign
    ├── pyAlign_package
    │   ├── Align.py
    │   ├── InitMatrix.py
    │   ├── NJ.py
    │   ├── SubMatrix.py
    │   ├── __init__.py
    │   ├── db.py
    │   └── fancy_printer.py
    ├── pyDotplot
    └── pyNJ

### getfasta

Creates a .fasta file containing the sequence of [PROT_ID], where PROT_ID is a UniProt accession number

    Usage: getfasta [PROT_ID]

### getpdb
 
Creates a .pdb file containing the coordinates of [PROT_ID] atoms, where PROT_ID is a PDB accession number

    Usage: getpdb [PROT_ID]

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

