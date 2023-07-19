
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