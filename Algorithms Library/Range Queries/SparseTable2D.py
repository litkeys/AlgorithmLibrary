# Python implementation of the 2D sparse table data structure
# Mainly used to answer min and max range queries in O(1) time
# For sum and product queries, use other data structures in the same folder

class SparseTable2D:
    def __init__(self, matrix: list, defaultvalue = float("inf"), queryfunction = min) -> None: 
        """
        Note that since sparsetables are immutable, an input matrix is required.
        The current defaultvalue and queryfunction defaults to min queries.
        Change defaultvalue to -float("inf") and queryfunction to lambda x, y: max(x, y) for max queries.
        """
        self.n, self.m = len(matrix), len(matrix[0])
        self.k, self.l = self.n.bit_length(), self.m.bit_length() # smallest power raise by 2 that does not exceeed n or m
        self.queryfunction = queryfunction
        self.defaultvalue = defaultvalue
        # precomputing sparse table, which has 4 dimensions for the 2D version
        # nothing but a sparse table of sparse tables, i.e. range -> (y) index -> range -> (x) index
        self.table = [[
            [[defaultvalue for i in range(self.m)] for j in range(self.l)] 
            for k in range(self.n)] for l in range(self.k)]
        # copy original values as base (for single value queries)
        for i in range(self.n):
            for j in range(self.m):
                self.table[0][i][0][j] = matrix[i][j] 
        # build inner sparse tables
        for l in range(1, self.l+1):
            for i in range(self.n):
                for j in range(self.m - (1<<l) + 1):
                    self.table[0][i][l][j] = self.queryfunction(
                        self.table[0][i][l-1][j],
                        self.table[0][i][l-1][j + (1<<(l-1))]
                    )
        # build rest of the table
        for k in range(1, self.k+1):
            for i in range(self.n - (1<<k) + 1):
                for l in range(1, self.l+1):
                    for j in range(self.m - (1<<l) + 1):
                        self.table[k][i][l][j] = self.queryfunction(
                            self.table[k-1][i][l][j],
                            self.table[k-1][i + (1<<(k-1))][l][j]
                        )

    def query(self, x1: int, y1: int, x2: int, y2: int): # x1 <= x2 and y1 <= y2
        k, l = (x2-x1+1).bit_length()-1, (y2-y1+1).bit_length()-1
        return self.queryfunction(
            self.table[k][x1][l][y1],
            self.table[k][x1][l][y2 - (1<<l) + 1],
            self.table[k][x2 - (1<<k) + 1][l][y1],
            self.table[k][x2 - (1<<k) + 1][l][y2 - (1<<l) + 1]
        )
    

# matrix = [
#     [3, 1, 5, 2],
#     [4, 2, 7, 3],
#     [0, 3, 2, 1]
# ]
# st = SparseTable2D(matrix)
# print(st.query(0, 0, 1, 1))
# print(st.query(0, 2, 0, 3))
# print(st.query(1, 1, 2, 3))
# print(st.query(1, 0, 2, 2))