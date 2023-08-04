"""
 Universidad del Valle de Guatemala
  Facultad de Ingenieria
  Departamento de Ciencia de la Computacion.
  Graficas por Computadora.
  Sección: 20

  Tarea 1 - Lines & Obj Models

  @version 1.0
  @author Adrian Fulladolsa Palma | Carne 21592
"""
from math import isclose
class Matrix:
    def __init__(self, arr):
        self.mat = arr

    def __add__(self, other):
        if len(self.mat) != len(other.mat) or len(self.mat[0]) != len(other.mat[0]):
            raise ValueError("Nel, no se puede sumar dos matrices con dimesiones distintas")
        result = [[self.mat[i][j] + other.mat[i][j] for j in range(len(self.mat[0]))] for i in
                  range(len(self.mat))]
        return Matrix(result)

    def __sub__(self, other):
        if len(self.mat) != len(other.mat) or len(self.mat[0]) != len(other.mat[0]):
            raise ValueError("Nel, no se puede restar dos matrices con dimesiones distintas")
        result = [[self.mat[i][j] - other.mat[i][j] for j in range(len(self.mat[0]))] for i in
                  range(len(self.mat))]
        return Matrix(result)

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if len(self.mat[0]) != len(other.mat):
                raise ValueError("The number of columns in the first matrix must match the number of rows in the second matrix for multiplication.")
            result = [[sum([self.mat[i][k] * other.mat[k][j] for k in range(len(other.mat))]) for j in range(len(other.mat[0]))] for i in range(len(self.mat))]
            return Matrix(result)
        elif isinstance(other, (int, float)):
            result = [[cell * other for cell in row] for row in self.mat]
            return Matrix(result)
        elif isinstance(other, list) and all(isinstance(item, (int, float)) for item in other):
            if len(other) != len(self.mat[0]):
                raise ValueError("The length of the array must match the number of columns in the matrix for multiplication.")
            result = [sum([self.mat[i][j] * other[j] for j in range(len(other))]) for i in range(len(self.mat))]
            return result
        else:
            raise TypeError("Unsupported operand type for multiplication.")

    def __matmul__(self, other):
        return self.__mul__(other)
    def transpose(self):
        result = [[self.mat[j][i] for j in range(len(self.mat))] for i in range(len(self.mat[0]))]
        return Matrix(result)
    
def bcCoords(A, B, C, P):
    BCP = abs((P[0] * C[1] + C[0] * B[1] + B[0] * P[1]) - (P[1] * C[0] + C[1] * B[0] + B[1] * P[0]))
    CAP = abs((A[0] * C[1] + C[0] * P[1] + P[0] * A[1]) - (A[1] * C[0] + C[1] * P[0] + P[1] * A[0]))
    ABP = abs((A[0] * B[1] + B[0] * P[1] + P[0] * A[1]) - (A[1] * B[0] + B[1] * P[0] + P[1] * A[0]))
    
    ABC = abs((A[0] * B[1] + B[0] * C[1] + C[0] * A[1]) - (A[1] * B[0] + B[1] * C[0] + C[1] * A[0]))

    """ BCP = (B[1] - C[1]) * (P[0] - C[0]) + (C[0] - B[0]) * (P[1] - C[1])
    CAP = (C[1] - A[1]) * (P[0] - C[0]) + (A[0] - C[0]) * (P[1] - C[1])
    #ABP = (A[1] - B[1]) * (P[0] - C[0]) + (B[0] - A[0]) * (P[1] - C[1])
    
    ABC = (B[1] - C[1]) * (A[0] - C[0]) + (C[0] - B[0]) * (A[1] - C[1]) """

    if ABC == 0:
        return None

    u = BCP / ABC
    v = CAP / ABC
    w = ABP / ABC
    #w = 1 - u - v

    if (0 <= u <= 1) and (0 <= v <= 1) and (0 <= w <= 1) and isclose(u + v + w, 1.0):
        return u, v, w
    else:
        return None