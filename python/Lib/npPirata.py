def multMM(m1, m2):
    resultado = [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]

    for i in range(len(m1)):
        for j in range(len(m2[0])):
            for k in range(len(m1[0])):
                resultado[i][j] += m1[i][k] * m2[k][j]

    return resultado

def multMV(m, v):
    resultado = [0, 0, 0, 0]
    for i in range(len(m)):
        for j in range(len(m[0])):
            resultado[i] += m[i][j] * v[j]

    return resultado


mm1 = [[1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 1, 2, 3],
        [4, 5, 6, 7]]

mm2 = [[9, 8, 7, 6],
        [5, 4, 3, 2],
        [1, 9, 8, 7],
        [6, 5, 4, 3]]

v1 = [1, 2, 3, 4]
