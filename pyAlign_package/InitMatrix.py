from pyAlign_package import SubMatrix


def comparison(seq_x, seq_y, mat='b62', window=1, tol=0, show=None):
    lx = len(seq_x)
    ly = len(seq_y)
    rx = range(lx)
    ry = range(ly)
    g = window // 2
    dots = 0
    matrix = [[0 for _ in rx] for _ in ry]

    if mat == 'b62': score_matrix = SubMatrix.b62
    if mat == 'p250': score_matrix = SubMatrix.p250
    if mat == 'custom': score_matrix = SubMatrix.cyps

    def score(x, y):
        i = 0
        average = 0
        match = 0
        for h in range(-g, g + 1):
            if 0 <= x + h < lx and 0 <= y + h < ly:
                i += 1
                average += score_matrix[(seq_x[x+h], seq_y[y+h])]
                if seq_x[x+h] == seq_y[y+h]:
                    match += 1
        return average / i, match / i

    for x in rx:
        for y in ry:
            average, avg_match = score(x, y)
            if avg_match >= tol:
                matrix[y][x] = average
                dots += 1

    if show == 'text':
        print('   ', '   '.join(list(seq_x)))
        for row in range(len(seq_y)):
            print(seq_y[row], end=' ')
            for column in range(len(seq_x)):
                print("{:5.1f}".format(matrix[row][column]), end='')
            print()

    if show == 'plot':
        import matplotlib.pyplot as plt
        import numpy as np
        a = np.array(matrix)
        plt.imshow(a, cmap='Greys', interpolation='nearest')
        plt.colorbar()
        plt.show()

    if show is None:
        pass

    return matrix

if __name__ == '__main__':
    seq_x = 'ADCNYRQCLCRPM'
    seq_y = 'AYCYNRCKCRDP'
    comparison(seq_x, seq_y, 'b62', 1, 0, show= 'text')
    comparison(seq_x, seq_y, 'p250', 5, 3/5, show= 'plot')
    matrix = comparison(seq_x, seq_y, 'p250', show= 'text')
    # print(matrix)
