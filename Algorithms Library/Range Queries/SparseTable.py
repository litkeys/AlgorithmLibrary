# Python implementation of the sparse table data structure
# Mainly used to answer min and max range queries in O(1) time
# For sum and product queries, use other data structures in the same folder

class SparseTable:
    def __init__(self, array: list, defaultvalue = float("inf"), queryfunction = min) -> None: 
        """
        Note that since sparsetables are immutable, an input array is required.
        The current defaultvalue and queryfunction defaults to min queries.
        Change defaultvalue to -float("inf") and queryfunction to lambda x, y: max(x, y) for max queries.
        """
        self.n = len(array)
        self.k = self.n.bit_length() # the smallest power raised by 2 that is larger than n
        self.queryfunction = queryfunction
        self.defaultvalue = defaultvalue
        # precomputing sparse table, which has 2 dimensions for the 1D version
        # first dimension corresponds to the power of 2 range, second dimension corresponds to starting index
        self.table = [array] + [[defaultvalue for i in range(self.n)] for j in range(self.k-1)]
        for k in range(1, self.k+1):
            i = 0
            while i + (1<<k) <= self.n:
                self.table[k][i] = queryfunction(
                    self.table[k-1][i], 
                    self.table[k-1][i + (1<<(k-1))]
                )
                i += 1

    def query(self, ql: int, qr: int): # qr >= ql
        k = (qr-ql+1).bit_length()-1
        return self.queryfunction(
            self.table[k][ql], 
            self.table[k][qr - (1<<k) + 1]
        )
    

# array = [1, 3, 4, 8, 6, 1, 4, 2]
# st = SparseTable(array)
# print(st.query(1, 6))
# print(st.query(2, 2))