# The shoelace algorithm calculates the area of any polygon given its vertices in adjacent order

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

# Point class version
def shoelace(*points: Point) -> int:
    l = len(points)
    result = 0
    for i in range(l):
        x1, y1 = points[i].x, points[i].y
        x2, y2 = points[(i+1)%l].x, points[(i+1)%l].y
        result += x1*y2 - x2*y1
    return abs(result)/2 # absolute value because depending on the processing order, result may be negative

# Tuple version
def shoelace(*points: tuple) -> int:
    l = len(points)
    result = 0
    for i in range(l):
        x1, y1 = points[i][0], points[i][1]
        x2, y2 = points[(i+1)%l][0], points[(i+1)%l][1]
        result += x1*y2 - x2*y1
    return abs(result)/2 # absolute value because depending on the processing order, result may be negative