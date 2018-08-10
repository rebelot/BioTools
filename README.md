# BioTools

A collection of bioinformatics tools written by me.

## Contents:
```
BioTools/
├── README.md
├── cAlign
│   ├── bin
│   │   ├── cAlign.py
│   │   ├── cal.exe
│   │   └── cal_custom.exe
│   ├── src
│   │   ├── main.c
│   │   └── main_custom.c
│   └── tags
├── desmond_progress_bar.sh
├── getfasta
├── getpdb
├── maestro_scripts
│   ├── maestro_dummy_at_center_of_mass.py
│   └── maestro_transform.py
├── pdbrenumber.py
├── pyAlign
├── pyAlign_package
│   ├── Align.py
│   ├── InitMatrix.py
│   ├── NJ.py
│   ├── SubMatrix.py
│   ├── __init__.py
│   ├── db.py
│   ├── fancy_printer.py
│   └── tags
├── pyDotplot.py
└── pyNJ

```

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
  -o1k, --over-1k       if checked, residuse > 1000 will not be renumbered
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

### Desmond progress bar

Trace the course of a molecular dynamics using `desmond_progress_bar.sh *.log` into the job directory.

### maestro script: Center of Mass

Places a dummy atom at the center of mass of selected atoms.

### maestro script: Transform

Perform workspace cartesian transformations; the tool provides ways to define reference points and axes to rotate or translate selected atoms.
