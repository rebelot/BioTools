import InitMatrix
import sys

def align(seq_j, seq_i, mat='p250', g_op=-12.0, g_ex=-4.0):
    def penalty(ex, g_op=g_op, g_ex=g_ex):
        return g_op + g_ex*(ex - 1)

    init_matrix = InitMatrix.comparison(seq_j, seq_i, mat=mat, show=None)
    init_matrix.insert(0, [0] + [penalty(j) for j in range(1, len(init_matrix[0]) + 1)])
    for i in range(1, len(init_matrix)):
        init_matrix[i].insert(0, penalty(i))

    # for row in range(len(init_matrix)):
    #     for column in range(len(init_matrix[row])):
    #         print("{:5.1f}".format(init_matrix[row][column]), end='')
    #     print()
    cell, square = 0, ((len(init_matrix) - 1) * (len(init_matrix[0]) - 1))
    transform_matrix = init_matrix.copy()
    track = {}       # {child:parent}
    for i in range(1, len(transform_matrix)):
        for j in range(1, len(transform_matrix[0])):
            i_score = max(transform_matrix[i-k][j] + penalty(k) for k in range(1, i+1))
            j_score = max(transform_matrix[i][j-l] + penalty(l) for l in range(1, j+1))
            ij_score = transform_matrix[i - 1][j - 1] + transform_matrix[i][j]
            score = max(ij_score, i_score, j_score)
            if score == ij_score:
                track[(i, j)] = (i - 1, j - 1)

            elif score == i_score:
                for k in range(1, i+1):
                    if score == transform_matrix[i-k][j] + penalty(k):
                        track[(i, j)] = (i - k, j)
                        break

            elif score == j_score:
                for l in range(1, j+1):
                    if score == transform_matrix[i][j-l] + penalty(l):
                        track[(i, j)] = (i, j - l)
                        break

            transform_matrix[i][j] = score
            cell += 1
            progress = 100 * cell / square
            sys.stderr.write(
            '\r[{:20}] {:5.2f}%  line {} of {} column {} of {}'.format('|' * int(progress / 5), progress, i,
                                                                       len(transform_matrix), j,
                                                                       len(transform_matrix[0])))

    # for row in range(len(transform_matrix)):
    #     for column in range(len(transform_matrix[row])):
    #         print("{:6.1f}".format(transform_matrix[row][column]), end='')
    #     print()

    path = []
    step_i, step_j = len(init_matrix) - 1, len(init_matrix[0]) - 1
    while (step_i, step_j) in track.keys():
        path.insert(0, track[(step_i, step_j)])
        step_i, step_j = track[(step_i, step_j)]
    if (0, 0) not in path:
        path.insert(0, (0, 0))
    i_max, j_max = len(init_matrix) - 1, len(init_matrix[0]) - 1
    if (i_max, j_max) not in path:
        path.append((i_max, j_max))
    x = []
    y = []
    n = 1
    for (step_i, step_j) in path:
        if n <= len(path) - 1:
            indel_i = path[n][0] - step_i
            indel_j = path[n][1] - step_j
            if step_j == path[n][1]:
                x.append('-'*indel_i)
                y.append(seq_i[step_i:step_i + indel_i])
            elif step_i == path[n][0]:
                y.append('-'*indel_j)
                x.append(seq_j[step_j:step_j + indel_j])
            else:
                x.append(seq_j[step_j])
                y.append(seq_i[step_i])
        n += 1

    identity = 0
    x = ''.join(x)
    y = ''.join(y)
    for j, i in zip(x, y):
            if j == i:
                identity += 1

    return x, y, float(identity)/max(len(x), len(y)),\
        max(transform_matrix[i][j] for (i, j) in path)

if __name__ == '__main__':
    from db import getseq

    def print_alignment(seq_x, seq_y, identity, max_score, filename='Alignment'):
        ide = []
        for x, y in zip(seq_x, seq_y):
            if x == y:
                ide.append('|')
            elif x != y and x != '-' and y != '-':
                ide.append('.')
            else:
                ide.append(' ')
        ide= ''.join(ide)
        with open('{}.txt'.format(filename), 'x') as file:
            file.write('{:^50}\n'.format(filename))
            file.write('----------------------------------\n')
            file.write('identity: {}/{}: {}%\n'.format(identity*len(al_x), len(al_x), 100*ident))
            file.write('score: {}\n'.format(max_score))
            file.write('----------------------------------\n')
            for chunk in range(0, len(seq_x), 50):
                file.write('{0:5d}    {1}    {2:<3d}\n'.format(chunk+1, seq_x[chunk:chunk+50], chunk + len(seq_x[chunk:chunk+50])))
                file.write('         {0}\n'.format(ide[chunk:chunk+50]))
                file.write('         {0}\n'.format(seq_y[chunk:chunk+50]))

    # P01130 Human LDL Receptor
    # Q99087 Xenopus laevis LDL Receptor 1
    seq_x = getseq('Q59990')
    seq_y = getseq('Q6V0L0')
    # getseq('P01130', erase=True)
    # getseq('Q99087', erase=True)
    #seq_x = 'ADCNYRQCLCRPM'
    #seq_y = 'AYCYNRCKCRDP'
    al_x, al_y, ident, max_score = align(seq_x, seq_y, mat='custom', g_op=-11, g_ex=-2)
    print_alignment(al_x, al_y, ident, max_score, filename='Allineamelo_Hcyp26c1_2ve3_op11_ex2')

    print()
    print(">2VE3")
    print(al_x)
    print(">Cyp26c1")
    print(al_y)
