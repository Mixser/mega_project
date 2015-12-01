from operator import mul


def copy_list(l):
    result = []
    for item in l:
        if isinstance(item, (list, tuple)):
            result.append(copy_list(item))
        else:
            result.append(item)
    return result


class Matrix(object):
    def __init__(self, data=None, n=None, m=None):
        if isinstance(data, Matrix):
            self._data = copy_list(data._data)
            self._n = data.rows_count
            self._m = data.cols_count
        elif isinstance(data, (list, tuple)):
            self._data = data
            self._n = len(data)
            self._m = len(data[0])
        elif n and m:
            self._data = [[0] * m for i in xrange(n)]
            self._n = n
            self._m = m

    @property
    def rows_count(self):
        return self._n

    @property
    def cols_count(self):
        return self._m

    def row(self, i):
        return self._data[i]

    def col(self, j):
        return [self._data[i][j] for i in xrange(self.rows_count)]

    def copy(self):
        return Matrix(self)

    def __getitem__(self, item):
        return self._data[item]

    def __str__(self):

        return str(self._data)

    def __mul__(self, matrix):
        """
        :param matrix: Matrix
        :type matrix: Matrix
        :rtype: Matrix
        """
        if self._m != matrix.cols_count:
            raise ValueError("The count of coulumns at the first matrix must be equal to count of rows at the second matrix.")
        result = Matrix(n=self.rows_count, m=matrix.cols_count)

        for i in xrange(result.rows_count):
            for j in xrange(result.cols_count):
                result[i][j] = reduce(lambda x, y: x + mul(*y), zip(self.row(i), matrix.col(j)), 0)
        return result

    def __pow__(self, n):
        """
        :param n:
        :rtype: Matrix
        """
        def __power(matrix, n):
            if n < 2:
                return matrix
            if n % 2 == 0:
                return __power(matrix * matrix, n / 2)
            else:
                return matrix * __power(matrix * matrix, (n - 1)/ 2)

        return __power(self, n)

N = 100
m = Matrix([[1, 1],[1, 0]])
fib = m ** N
print fib[0][0]




