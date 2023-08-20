# Python implementation of a general heap
# Functions as a priority queue that supports custom comparators

class Heap:
    def __init__(self, array = None, comparator = None) -> None:
        if comparator == None:
            raise ValueError("comparator is undefined")
        self.heap = [None] # 0th element is a placeholder
        self.comparator = comparator # must take two arguments, return True if left arg has higher priority than right arg
        self.size = 0 # size of the heap
        if array:
            for element in array:
                self.push(element)

    def peek(self): # returns the top element
        return self.heap[1] if self.size else None    

    def push(self, element): # inserts an element into the heap
        self.heap.append(element)
        self.size += 1
        # rest is heapify up
        current_index = self.size
        parent_index = current_index >> 1 # bit manip for floor dividing by 2
        while current_index > 1 and self.comparator(self.heap[current_index], self.heap[parent_index]): # swap if better than parent
            self.heap[current_index], self.heap[parent_index] = self.heap[parent_index], self.heap[current_index]
            current_index = parent_index
            parent_index = current_index >> 1 # bit manip for floor dividing by 2

    def pop(self): # removes the top element from the heap
        if self.size == 0: # does nothing if heap is already empty
            return None        
        removed_element = self.heap[1] # store the removed element
        self.heap[1] = self.heap[-1] # this is done in two steps in case the heap consist of only one element
        self.heap.pop() # to avoid indexerror
        self.size -= 1
        # rest is heapify down
        current_index = 1
        leftchild_index = current_index << 1 # bit manip for multiplying by 2
        while leftchild_index <= self.size:
            best = leftchild_index # set the best child to left initially
            rightchild_index = best + 1
            if rightchild_index <= self.size and self.comparator(self.heap[rightchild_index], self.heap[best]):
                best = rightchild_index # set the best child to right if right exists and is better
            if self.comparator(self.heap[best], self.heap[current_index]): # swap if best child is better
                self.heap[current_index], self.heap[best] = self.heap[best], self.heap[current_index]
                current_index = best
                leftchild_index = current_index << 1 # bit manip for multiplying by 2
            else:
                break
        return removed_element # returns the removed element
    
    def ntop(self, n: int): # returns the n top elements in the heap in n log n time
        if n == 1:
            return self.peek()
        if n > self.size:
            raise ValueError("n larger than heap size")
        heapcopy = self.heap.copy() # makes a copy of the original heap in n time
        return [heapcopy.pop() for i in range(n)] # obtain top n elements in n log n time
    

# def min_comparator(a, b):
#     return a < b

# def max_comparator(a, b):
#     return a > b

# test = Heap(min_comparator)
# #test = Heap(max_comparator)
# test.push(1)
# test.push(5)
# test.push(6)
# #print(test.heap)
# test.push(3)
# #print(test.heap)
# test.push(2)
# print(test.heap)

# for i in range(5):
#     print(test.peek())
#     test.pop()


# array = [1, 3, 5, 4, 2]
# test = Heap(max_comparator, array)
# print(test.heap)
# for i in range(5):
#     print(test.peek())
#     test.pop()