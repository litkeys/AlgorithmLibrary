# 2D vector
class vector2:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vector2(x: {self.x}, y: {self.y})"
    
    def __add__(self, other: 'vector2') -> 'vector2':
        return vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'vector2') -> 'vector2':
        return vector2(self.x - other.x, self.y - other.y)
    
    # other operations such as dot product will be implemented later if needed
    # for now this class is made solely for easier handling of 2D coordinates
    
    def swap(self) -> 'vector2': # swaps x for y and y for x, different from c++'s swap
        return vector2(self.y, self.x)
    
    def distance_euclidean(self, other: 'vector2') -> 'vector2':
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
    
    def distance_manhattan(self, other: 'vector2') -> 'vector2':
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    # four movement functions are included

    def left(self) -> 'vector2':
        return vector2(self.x - 1, self.y)
    
    def right(self) -> 'vector2':
        return vector2(self.x + 1, self.y)
    
    def up(self) -> 'vector2':
        return vector2(self.x, self.y + 1)
    
    def down(self) -> 'vector2':
        return vector2(self.x, self.y - 1)
    
    # functions to get neighbour coordinates, which return tuples (to save memory)

    def neighbours(self) -> 'vector2': # clockwise starting from right, ends at top
        return self.right(), self.down, self.left, self.up() 
    
    def neighbours_eight(self) -> 'vector2': # clockwise starting from top right, ends at top
        return vector2(self.x+1, self.y+1), self.right(), vector2(self.x+1, self.y-1), self.down, vector2(self.x-1, self.y-1), self.left, vector2(self.x-1, self.y+1), self.up()
    
    # below are comparison methods that firstly compares x then y
    
    def __eq__(self, other: 'vector2') -> bool:
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other: 'vector2') -> bool:
        return not self.__eq__(other)
    
    def __gt__(self, other: 'vector2') -> bool:
        return (self.x, self.y) > (other.x, other.y)
    
    def __lt__(self, other: 'vector2') -> bool:
        return (self.x, self.y) < (other.x, other.y)
    
    def __ge__(self, other: 'vector2') -> bool:
        return (self.x, self.y) >= (other.x, other.y)
    
    def __le__(self, other: 'vector2') -> bool:
        return (self.x, self.y) <= (other.x, other.y)