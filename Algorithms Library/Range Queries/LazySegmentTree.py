# Python implementation of a sum lazy segment tree
# Tree is stored in an array of 2n elements where n is the length of the array
# Supports both range queries and range updates in log n time
# There are two types of range updates: modifying and assigning
# Note that the z values will be duped not distributed to child nodes
# Do not use LazySegmentTreeGeneral for sum range assignments, only ever use this

class LazySegmentTree:
    def __init__(self, data_array: list = [], defaultvalue = 0):
        self.data = data_array # stores the contents of the original input array, does not get updated
        self.height = len(bin(len(data_array)-1)) - 2
        self.size = 2**(self.height) # width of the tree, the next power of 2 after the array size, not the tree size
        self.defaultvalue = defaultvalue
        self.tree = [defaultvalue for i in range(self.size*2)] # s values
        self.lazy = [defaultvalue for i in range(self.size*2)] # z values
        self.overwrite = [False for i in range(self.size*2)] # lazy assignment
        self._init(1, 0, len(self.data) - 1)

    def _init(self, i: int, tl: int, tr: int):
        if tl == tr:
            self.tree[i] = self.data[tl]
            return self.tree[i]
        self.tree[i] = (
            self._init(i * 2, tl, (tl + tr) // 2) +
            self._init(i * 2 + 1, (tl + tr) // 2 + 1, tr)
        )
        return self.tree[i]

    def _update(self, i: int, ql: int, qr: int, add: int, tl: int, tr: int):
        """
        i is the index of the current treenode
        ql and qr represent the query range
        tl and tr represent the current search range, always set tl to 0 and tr to self.size-1
        add represents the value to increase the target range by
        """
        if qr < tl or tr < ql:  # [ql, qr] and [tl, tr] don't intersect
            return
        if ql <= tl and tr <= qr:  # [ql, qr] includes [tl, tr]
            self.lazy[i] += add # update/merge z value
            return
        # [ql, qr] and [tl, tr] partially intersects, propagate lazy assignments & updates to children
        if self.overwrite[i] == True:
            new_child_value = self.tree[i] // 2
            self.tree[i * 2] = new_child_value
            self.lazy[i * 2] = self.defaultvalue
            if i * 2 < self.size:
                self.overwrite[i * 2] = True
            self.tree[i * 2 + 1] = new_child_value
            self.lazy[i * 2 + 1] = self.defaultvalue            
            if i * 2 + 1 < self.size:
                self.overwrite[i * 2 + 1] = True
            self.overwrite[i] = False
        else:
            self.lazy[i * 2] += self.lazy[i]
            self.lazy[i * 2 + 1] += self.lazy[i]
        # increase s value by new lazy update * size of intersection
        self.tree[i] += (self.lazy[i] + add) * (min(qr, tr) - max(ql, tl) + 1)
        # reset z value
        self.lazy[i] = 0
        # recursively update left and right children
        self._update(i * 2, ql, qr, add, tl, (tl + tr) // 2)
        self._update(i * 2 + 1, ql, qr, add, (tl + tr) // 2 + 1, tr)

    def _assign(self, i: int, ql: int, qr: int, new_value: int, tl: int, tr: int):
        """
        i is the index of the current treenode
        ql and qr represent the query range
        tl and tr represent the current search range, always set tl to 0 and tr to self.size-1
        new_value represents the value to increase the target range by
        """
        if qr < tl or tr < ql:  # [ql, qr] and [tl, tr] don't intersect
            return self.defaultvalue
        if ql <= tl and tr <= qr:  # [ql, qr] includes [tl, tr]
            diff = new_value * (tr - tl + 1) - self.tree[i]
            self.tree[i] = new_value * (tr - tl + 1)
            self.lazy[i] = self.defaultvalue
            self.overwrite[i] = True # mark node for lazy assignment propagation
            return diff # propagate diff upwards
        # [ql, qr] and [tl, tr] partially intersects, propagate lazy assignments & updates to children
        if self.overwrite[i] == True:
            new_child_value = self.tree[i] // 2
            self.tree[i * 2] = new_child_value
            self.lazy[i * 2] = self.defaultvalue
            if i * 2 < self.size:
                self.overwrite[i * 2] = True
            self.tree[i * 2 + 1] = new_child_value
            self.lazy[i * 2 + 1] = self.defaultvalue            
            if i * 2 + 1 < self.size:
                self.overwrite[i * 2 + 1] = True
            self.overwrite[i] = False
        else:
            self.lazy[i * 2] += self.lazy[i]
            self.lazy[i * 2 + 1] += self.lazy[i]
        # calculate diff by merging the assignment diffs of left and right children
        ldiff = self._assign(i * 2, ql, qr, new_value, tl, (tl + tr) // 2)
        rdiff = self._assign(i * 2 + 1, ql, qr, new_value, (tl + tr) // 2 + 1, tr)
        diff = ldiff + rdiff
        # increase s value by lazy update + diff
        self.tree[i] += self.lazy[i] + diff
        # reset z value
        self.lazy[i] = 0
        # propagate diff upwards
        return diff        

    def _query(self, i, ql, qr, tl, tr):
        if qr < tl or tr < ql:  # [ql, qr] and [tl, tr] don't intersect
            return 0
        if ql <= tl and tr <= qr:  # [ql, qr] includes [tl, tr]
            return self.tree[i] + self.lazy[i] * (tr - tl + 1)
        # [ql, qr] and [tl, tr] partially intersects, propagate lazy assignments & updates to children
        if self.overwrite[i] == True:
            new_child_value = self.tree[i] // 2
            self.tree[i * 2] = new_child_value
            self.lazy[i * 2] = self.defaultvalue
            if i * 2 < self.size:
                self.overwrite[i * 2] = True
            self.tree[i * 2 + 1] = new_child_value
            self.lazy[i * 2 + 1] = self.defaultvalue            
            if i * 2 + 1 < self.size:
                self.overwrite[i * 2 + 1] = True
            self.overwrite[i] = False
        else:
            self.lazy[i * 2] += self.lazy[i]
            self.lazy[i * 2 + 1] += self.lazy[i]        
        # increase s value by lazy update * size of intersection
        self.tree[i] += self.lazy[i] * (tr - tl + 1)
        # reset z value
        self.lazy[i] = 0
        # recursively query left and right children, then combine their results
        return (
            self._query(i * 2, ql, qr, tl, (tl + tr) // 2) + 
            self._query(i * 2 + 1, ql, qr, (tl + tr) // 2 + 1, tr)
        )

    def update(self, left: int, right: int, add): # strictly for updating NOT assigning
        self._update(1, left, right, add, 0, len(self.data) - 1)

    def assign(self, left: int, right: int, new_value): # strictly for assigning/overwriting
        self._assign(1, left, right, new_value, 0, len(self.data) - 1)

    def query(self, left: int, right: int):
        return self._query(1, left, right, 0, len(self.data) - 1)
    

# Sum queries
# s = LazySegmentTree([5, 8, 6, 3, 2, 7, 2, 6])
# print(s.query(1, 7)) # 34
# s.update(1, 7, 2)
# print(s.query(1, 7)) # 48
# s.assign(1, 7, 2)
# print(s.tree)
# print(s.lazy)
# print(s.overwrite)
# print(s.query(1, 7)) # 14
# print(s.query(1, 2)) # 4
# print(s.query(0, 1)) # 7
# print(s.query(5, 7)) # 6
# print(s.query(7, 7)) # 2
# print(s.tree)
# print(s.lazy)
# print(s.overwrite)