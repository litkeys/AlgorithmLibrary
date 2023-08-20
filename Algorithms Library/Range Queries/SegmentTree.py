# Python implementation of a general segment tree
# Tree is stored in an array of 2n elements where n is the length of the array
# Insertion and Deletion are NOT supported, only range queries and single value updates

class SegmentTree:
    def __init__(self, data_array: list = [], queryfunction = lambda x,y: x+y, defaultvalue = 0) -> None:
        self.data = data_array # stores the contents of the original input array, does not get updated
        self.height = len(bin(len(data_array)-1)) - 2
        self.size = 2**(self.height) # width of the tree, the next power of 2 after the array size, not the tree size
        self.queryfunction = queryfunction
        self.defaultvalue = defaultvalue

        self.tree = [defaultvalue for i in range(self.size*2)] 
        for i in range(len(data_array)):
            self.update(i, data_array[i])
        
    def update(self, index: int, modify_by: int) -> None:
        index += self.size
        self.tree[index] = self.queryfunction(self.tree[index], modify_by)
        while index > 1:
            index //= 2
            self.tree[index] = self.queryfunction(self.tree[index*2], self.tree[index*2+1])
        
    def assign(self, index: int, newvalue: int) -> None:
        index += self.size
        self.tree[index] = newvalue
        while index > 1:
            index //= 2
            self.tree[index] = self.queryfunction(self.tree[index*2], self.tree[index*2+1])

    def query(self, ql: int, qr: int): # bottom up approach, always use this as it requires less params
        """
        ql and qr represent the query range
        """
        ql += self.size
        qr += self.size
        result = self.defaultvalue
        while ql <= qr:
            if ql % 2 == 1:
                result = self.queryfunction(result, self.tree[ql])
                ql += 1
            if qr % 2 == 0:
                result = self.queryfunction(result, self.tree[qr])
                qr -= 1
            ql //= 2
            qr //= 2
        return result

    def query_topdown(self, ql: int, qr: int, k: int, tl: int, tr: int): # top down approach, avoid using this
        """
        k here represents the current position in the tree, set to 1 - the (index of the) top node
        ql and qr represent the query range
        tl and tr represent the current search range, always set tl to 0 and tr to self.size-1
        """
        if qr < tl or ql > tr: # [ql, qr] and [tl, tr] don't intersect
            return self.defaultvalue
        if ql <= tl and tr <= qr: # [ql, qr] includes [tl, tr]
            return self.tree[k]
        d = (tl+tr)//2
        return self.queryfunction(self.query_topdown(ql, qr, k*2, tl, d), self.query_topdown(ql, qr, k*2+1, d+1, tr))


def queryfunction(x, y): # This needs to be implemented if it is to be used
    raise NotImplementedError


# Sum queries
# s = SegmentTree([5, 8, 6, 3, 2, 7, 2, 6])
# print(s.query(1, 7)) # 34
# print(s.query_topdown(1, 7, 1, 0, s.size-1)) # 34
# s.update(1, 10)
# print(s.query(1, 7)) # 44
# s.assign(1, 10)
# print(s.query(1, 7)) # 36

# Min queries
# s = SegmentTree([5, 8, 6, 3, 1, 7, 2, 6], min, defaultvalue=float("inf"))
# print(s.query(0, 4)) # 1
# print(s.query_topdown(0, 4, 1, 0, s.size-1)) # 1

# Max queries
# s = SegmentTree([5, 8, 6, 3, 1, 7, 2, 6], max, defaultvalue=-float("inf"))
# print(s.query(2, 5)) # 7
# print(s.query_topdown(2, 5, 1, 0, s.size-1)) # 7
# s.update(4, 10)
# print(s.query(2, 5)) # 10