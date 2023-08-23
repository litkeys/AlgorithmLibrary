# Python implementation of Kadane's algorithm for finding min/max subarray sum in O(n)
# This can then be applied to find min/max submatrix sum in O(n^3)

def kadanesMax(array: list[int]) -> int:
    best, s = 0
    l, r = 0, 0 # pointers to the current subarray range
    bl, br = None, None # pointers to the best subarray range
    for i in range(len(array)):
        if array[i] > s + array[i]: # better to start a new subarray with a single element
            l, r = i, i
            s = array[i]
        else: # better to extend the existing subarray
            r = i
            s += array[i]
        if s > best: # update best
            bl, br = l, r
            best = s
    # return l, r if the exact indices are needed
    return best

def kadanesMin(array: list[int]) -> int:
    best, s = 0
    l, r = 0, 0 # pointers to the current subarray range
    bl, br = None, None # pointers to the best subarray range
    for i in range(len(array)):
        if array[i] < s + array[i]: # better to start a new subarray with a single element
            l, r = i, i
            s = array[i]
        else: # better to extend the existing subarray
            r = i
            s += array[i]
        if s < best: # update best
            bl, br = l, r
            best = s
    # return l, r if the exact indices are needed
    return best