"""
 Universidad del Valle de Guatemala
  Facultad de Ingenieria
  Departamento de Ciencia de la Computacion.
  Graficas por Computadora.
  Sección: 20

  Tarea 3 - Camaras

  @version 1.0
  @author Adrian Fulladolsa Palma | Carne 21592
"""
from math import isclose ,sqrt
import numpy
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
    # Se saca el área de los subtriángulos y del triángulo
    # mayor usando el Shoelace Theorem, una fórmula que permite
    # sacar el área de un polígono de cualquier cantidad de vértices.

    areaPCB = abs((P[0]*C[1] + C[0]*B[1] + B[0]*P[1]) - 
                  (P[1]*C[0] + C[1]*B[0] + B[1]*P[0]))

    areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) - 
                  (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))

    areaABP = abs((A[0]*B[1] + B[0]*P[1] + P[0]*A[1]) - 
                  (A[1]*B[0] + B[1]*P[0] + P[1]*A[0]))

    areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) - 
                  (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))

    # Si el área del triángulo es 0, retornar nada para
    # prevenir división por 0.
    if areaABC == 0:
        return None

    # Determinar las coordenadas baricéntricas dividiendo el 
    # área de cada subtriángulo por el área del triángulo mayor.
    u = areaPCB / areaABC
    v = areaACP / areaABC
    w = areaABP / areaABC

    # Si cada coordenada está entre 0 a 1 y la suma de las tres
    # es igual a 1, entonces son válidas.
    if 0<=u<=1 and 0<=v<=1 and 0<=w<=1 and isclose(u+v+w, 1.0):
        return (u, v, w)
    else:
        return None
    
def sub(v1, v2):
        if len(v1) != len(v2):
            raise ValueError("Tuples must have the same length.")
        
        subtracted_tuple = tuple(a - b for a, b in zip(v1, v2))
        return subtracted_tuple
        
        return result

def norm(x, ord=None, axis=None, keepdims=False):
        if axis is not None:
            raise ValueError("Axis argument is not supported.")
        
        if ord is None or ord == 2:
            squared_sum = sum(v ** 2 for v in x)
            norm = sqrt(squared_sum)
            return norm
        else:
            raise ValueError("Only Euclidean norm (ord=2) is supported.")
        
def divTF(t, d):
    if d != 0:
        divided_tuple = tuple(value / d for value in t)
        return divided_tuple
    else:
        return t
    
def cross(v1, v2):
    if len(v1) != 3 or len(v2) != 3:
        raise ValueError("Tuples must be 3-dimensional.")
    
    cross_product = [
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    ]
    return cross_product

def inv(matrix):
        if len(matrix) != len(matrix[0]):
            raise ValueError("Matrix must be square for inversion.")
        
        n = len(matrix)
        augmented_matrix = [row + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
        
        # Perform Gauss-Jordan elimination
        for i in range(n):
            pivot_row = augmented_matrix[i]
            pivot_element = pivot_row[i]
            
            if pivot_element == 0:
                raise ValueError("Matrix is singular, cannot be inverted.")
            
            pivot_row_normalized = [elem / pivot_element for elem in pivot_row]
            augmented_matrix[i] = pivot_row_normalized
            
            for k in range(n):  # Use k instead of j
                if k != i:
                    factor = augmented_matrix[k][i]
                    row_to_subtract = [elem * factor for elem in pivot_row_normalized]
                    augmented_matrix[k] = [x - y for x, y in zip(augmented_matrix[k], row_to_subtract)]
        
        inverse_matrix = [row[n:] for row in augmented_matrix]
        return inverse_matrix




