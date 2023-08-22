# The left turn test determines whether p3 is to the left of the line between p1 and p2, or right, or on the line

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    def __sub__(self, p: 'Point') -> 'Point':
        return Point(self.x+p.x, self.y+p.y)
    def __sub__(self, p: 'Point') -> 'Point':
        return Point(self.x-p.x, self.y-p.y)
    def __mul__(self, p: 'Point') -> int: # cross product
        return self.x*p.y - self.y*p.x
    def __repr__(self) -> str:
        return f"(x: {self.x}, y: {self.y})"

# Point class version
def ltt(p1: Point, p2: Point, p3: Point) -> int:
    result = (p3.x - p2.x) * (p1.y - p2.y) - (p3.y - p2.y) * (p1.x - p2.x)
    if result < 0: 
        return -1 # right turn
    elif result > 0: 
        return 1 # left turn
    else:
        return 0 # collinear, i.e. straight line
    
# Tuple version
def ltt(p1: tuple, p2: tuple, p3: tuple) -> int:
    result = (p3[0] - p2[0]) * (p1[1] - p2[1]) - (p3[1] - p2[1]) * (p1[0] - p2[0])
    if result < 0: 
        return -1 # right turn
    elif result > 0: 
        return 1 # left turn
    else:
        return 0 # collinear, i.e. straight line