# Python implementation of a matrix sum fenwick a.k.a. binary indexed tree
# Efficiently calculates prefix sums, using which range queries can be efficiently answered
# Supports both range queries and single value updates in log n log m time
# Note that since the set union formula is used, it is only possible to support sum queries
# Also applicable for product queries

class FenwickTree2D:
    def __init__(self, matrix: list = []) -> None:
        self.size = (len(matrix), len(matrix[0]))
        self.matrix = matrix # necessary for assign operation, 0-indexed
        self.tree = [[0 for j in range(self.size[1]+1)] for i in range(self.size[0]+1)] # first element of each row/col is dummy
        # building prefix sum for x axis
        psa = [[0 for j in range(self.size[1]+1)] for i in range(self.size[0]+1)] # prefix sum matrix is used to construct the tree in O(nm), first element of each row/col is dummy
        for i in range(1, self.size[0]+1):
            s = 0
            for j in range(1, self.size[1]+1):
                s += matrix[i-1][j-1]
                psa[i][j] = s
        # constructing fenwick tree for x axis
        for i in range(1, self.size[0]+1):
            for j in range(1, self.size[1]+1):
                self.tree[i][j] = psa[i][j] - psa[i][j-(j&-j)]
        # building prefix sum for y axis
        psa2 = [[0 for j in range(self.size[1]+1)] for i in range(self.size[0]+1)] # prefix sum matrix is used to construct the tree in O(nm), first element of each row/col is dummy
        for j in range(1, self.size[1]+1):
            s = 0
            for i in range(1, self.size[0]+1):
                s += self.tree[i][j]
                psa2[i][j] = s
        # constructing fenwick tree for y axis
        for j in range(1, self.size[1]+1):
            for i in range(1, self.size[0]+1):
                self.tree[i][j] = psa2[i][j] - psa2[i-(i&-i)][j]

    def _sum(self, x: int, y: int): # prefix sum to [x, y]
        xr, yr = x+1, y+1 # adjust to 1-index
        s = 0
        x, y = xr, yr
        while x:
            y = yr
            while y:
                s += self.tree[x][y]
                y -= y&-y
            x -= x&-x
        return s

    def sum_query(self, x1: int, y1: int, x2: int, y2: int): # x1 <= x2 and y1 <= y2
        # calculate sum query for [[1, 1], [x1, y1]]
        sum_x1y1 = self._sum(x1-1, y1-1)
        # calculate sum query for [[1, 1], [x2, y1]]
        sum_x2y1 = self._sum(x2, y1-1)
        # calculate sum query for [[1, 1], [x1, y2]]
        sum_x1y2 = self._sum(x1-1, y2)
        # calculate sum query for [[1, 1], [x2, y2]]
        sum_x2y2 = self._sum(x2, y2)
        # calculate sum query for [[x1, y1], [x2, y2]] using set union formula
        return sum_x2y2 - sum_x2y1 - sum_x1y2 + sum_x1y1

    def update(self, x: int, y: int, add: int):
        self.matrix[x][y] += add
        # adjust to 1-index
        x += 1
        while x <= self.size[0]:
            ny = y+1
            while ny <= self.size[1]:
                self.tree[x][ny] += add
                ny += ny&-ny
            x += x&-x

    def assign(self, x: int, y: int, new_value: int):
        diff = new_value - self.matrix[x][y]
        self.matrix[x][y] = new_value
        # adjust to 1-index
        x += 1
        while x <= self.size[0]:
            ny = y+1
            while ny <= self.size[1]:
                self.tree[x][ny] += diff
                ny += ny&-ny
            x += x&-x


# matrix = [
#     [7, 6, 1, 6],
#     [8, 7, 5, 2],
#     [3, 9, 7, 1], 
#     [8, 5, 3, 8]
# ]

# tree = FenwickTree2D(matrix)
# print(tree.sum_query(1, 1, 2, 2)) # 28
# print(tree.sum_query(1, 2, 2, 3)) # 15
# for i in range(tree.size[0]+1):
#     print(tree.tree[i])
# tree.update(2, 2, 2)
# print(tree.sum_query(1, 1, 2, 2)) # 30
# print(tree.sum_query(1, 2, 2, 3)) # 17

# tree.assign(1, 2, 10)
# for i in range(tree.size[0]):
#     print(tree.matrix[i])
# print(tree.sum_query(1, 2, 1, 2)) # 10
# for i in range(tree.size[0]+1):
#     print(tree.tree[i])
# print(tree.sum_query(1, 2, 2, 2)) # 19

# print(tree.sum_query(0, 0, 3, 3))
# print(tree.tree)
# tree.assign(1, 2, 10)
# print(tree.sum_query(0, 0, 3, 3))
# print(tree.tree)

# print(tree.sum_query(1, 1, 2, 2)) # 35
# print(tree.sum_query(1, 2, 2, 3)) # 22


# matrix = [
#     [1, 1, 1, 1],
#     [1, 1, 1, 1],
#     [1, 1, 1, 1],
#     [1, 1, 1, 1]
# ]

# tree = FenwickTree2D(matrix)
# for i in range(tree.size[0]+1):
#     print(tree.tree[i])