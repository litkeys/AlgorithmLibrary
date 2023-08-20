# Python implementation of an array sum fenwick a.k.a. binary indexed tree
# Efficiently calculates prefix sums, using which range queries can be efficiently answered
# Supports both range queries and single value updates in log n time
# Note that since the set union formula is used, it is only possible to support sum queries
# Also applicable for product queries

class FenwickTree:
    def __init__(self, array: list = []) -> None:
        self.size = len(array)
        self.array = array # necessary for assign operation, 0-indexed
        self.tree = [0 for i in range(self.size+1)] # first element is dummy
        psa = [0 for i in range(self.size+1)] # prefix sum array is used to construct the tree in O(n), first element is dummy
        # building prefix sum array
        s = 0
        for i in range(1, self.size+1):
            s += array[i-1]
            psa[i] = s
        # building fenwick tree
        for i in range(1, self.size+1):
            self.tree[i] = psa[i] - psa[i-(i&-i)]

    def _sum(self, k: int): # prefix sum to k
        k += 1 # adjust to 1-index
        s = 0
        while k:
            s += self.tree[k]
            k -= k&-k
        return s

    def sum_query(self, ql: int, qr: int): # b >= a
        # calculate sum query for [1, a-1]
        sum_a = self._sum(ql-1)
        # calculate sum query for [1, b]
        sum_b = self._sum(qr)
        # calculate sum query for [a, b] using set union formula
        return sum_b - sum_a

    def update(self, index: int, add: int):
        self.array[index] += add
        index += 1 # adjust to 1-index
        while index <= self.size:
            self.tree[index] += add
            index += index&-index

    def assign(self, index: int, new_value: int):
        diff = new_value - self.array[index]
        self.array[index] = new_value
        index += 1 # adjust to 1-index
        while index <= self.size:
            self.tree[index] += diff
            index += index&-index


# array = [1, 3, 4, 8, 6, 1, 4, 2]

# tree = FenwickTree(array)
# print(tree.sum_query(0, 6)) # 27
# tree.update(3, 5)
# print(tree.sum_query(0, 6)) # 32
# tree.assign(7, 10)
# print(tree.sum_query(5, 7)) # 15