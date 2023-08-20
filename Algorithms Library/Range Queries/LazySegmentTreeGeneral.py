# Python implementation of a general lazy segment tree
# Tree is stored in an array of 2n elements where n is the length of the array
# Supports both range queries and range updates in log n time
# There are two types of range updates: modifying and assigning
# Modifying range update depends on the queryfunction e.g. lambda a, b: a + b where b is the modify_by value
# Note that the z values will be duped not distributed to child nodes
# Also note that assign function is not needed, since update does the same thing when it comes to min and max

class LazySegmentTree:
    def __init__(self, data_array: list = [], queryfunction = lambda x,y: x+y, defaultvalue = 0):
        self.data = data_array # stores the contents of the original input array, does not get updated
        self.height = len(bin(len(data_array)-1)) - 2
        self.size = 2**(self.height) # width of the tree, the next power of 2 after the array size, not the tree size
        self.queryfunction = queryfunction
        self.defaultvaule = defaultvalue
        self.tree = [defaultvalue for i in range(self.size*2)] # s values
        self.lazy = [defaultvalue for i in range(self.size*2)] # z values
        self._init(1, 0, len(self.data) - 1)

    def _init(self, i: int, tl: int, tr: int):
        if tl == tr:
            self.tree[i] = self.data[tl]
            return self.tree[i]
        self.tree[i] = self.queryfunction(
            self._init(i * 2, tl, (tl + tr) // 2),
            self._init(i * 2 + 1, (tl + tr) // 2 + 1, tr)
        )
        return self.tree[i]

    def _update(self, i: int, ql: int, qr: int, modify_by: int, tl: int, tr: int):
        """
        i is the index of the current treenode
        ql and qr represent the query range
        tl and tr represent the current search range, always set tl to 0 and tr to self.size-1
        modify_by represents the value to increase the target range by
        """
        if qr < tl or tr < ql: # [ql, qr] and [tl, tr] don't intersect
            return
        if ql <= tl and tr <= qr: # [ql, qr] includes [tl, tr]
            self.lazy[i] = self.queryfunction(self.lazy[i], modify_by) # update/merge z value
            return
        # [ql, qr] and [tl, tr] partially intersects, propagate lazy update to children
        self.lazy[i * 2] = self.queryfunction(self.lazy[i * 2], self.lazy[i])
        self.lazy[i * 2 + 1] = self.queryfunction(self.lazy[i * 2 + 1], self.lazy[i])
        # increase s value by modify_by * size of intersection
        self.tree[i] = self.queryfunction(self.tree[i], (self.lazy[i] + modify_by) * (min(qr, tr) - max(ql, tl) + 1))
        # reset z value
        self.lazy[i] = 0
        # recursively update left and right children
        self._update(i * 2, ql, qr, modify_by, tl, (tl + tr) // 2)
        self._update(i * 2 + 1, ql, qr, modify_by, (tl + tr) // 2 + 1, tr)

    def _query(self, i: int, ql: int, qr: int, tl: int, tr: int):
        if qr < tl or tr < ql: # [ql, qr] and [tl, tr] don't intersect
            return 0
        if ql <= tl and tr <= qr: # [ql, qr] includes [tl, tr]
            return self.queryfunction(self.tree[i], self.lazy[i] * (tr - tl + 1))
        # [ql, qr] and [tl, tr] partially intersects, propagate lazy update to children
        self.lazy[i * 2] = self.queryfunction(self.lazy[i * 2], self.lazy[i])
        self.lazy[i * 2 + 1] = self.queryfunction(self.lazy[i * 2 + 1], self.lazy[i])
        # increase s value by modify_by * size of intersection
        self.tree[i] = self.queryfunction(self.tree[i], self.lazy[i] * (tr - tl + 1))
        # reset z value
        self.lazy[i] = 0
        # recursively query left and right children, then combine their results
        return (
            self._query(i * 2, ql, qr, tl, (tl + tr) // 2) + 
            self._query(i * 2 + 1, ql, qr, (tl + tr) // 2 + 1, tr)
        )

    def update(self, left: int, right: int, modify_by):
        self._update(1, left, right, modify_by, 0, len(self.data) - 1)

    def query(self, left: int, right: int):
        return self._query(1, left, right, 0, len(self.data) - 1)
    

# Sum queries
# s = LazySegmentTree([5, 8, 6, 3, 2, 7, 2, 6])
# print(s.query(1, 7)) # 34
# s.update(1, 7, 2)
# print(s.query(1, 7)) # 48