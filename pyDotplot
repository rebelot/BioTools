from pyAlign_package import InitMatrix, db

seq_x = input('Enter Accession Number: ')
seq_y = input('Enter Accession Number: ')
x = db.getseq(seq_x)
y = db.getseq(seq_y)

while True:
    mat = input('Select Substitution Matrix [PAM250 = p250 / BLOSUM62 = b62]')
    window = eval(input('Select window length: '))
    if window % 2 == 0:
        print('ERROR: Window must be odd')
        continue
    matches = eval(input('In-Window matches cut-off: '))
    tol = matches/window
    show = str.lower(input('[text] for text matrix output, [plot] for img output: '))
    if show is None: print('Showing default: text')

    InitMatrix.comparison(x, y, mat=mat, window=window, tol=tol, show=show)

    terminate = input('End program? [[y]/any]')
    if terminate in ('y', 'yes'):
        break

db.getseq(seq_x, erase=True)
db.getseq(seq_y, erase=True)
