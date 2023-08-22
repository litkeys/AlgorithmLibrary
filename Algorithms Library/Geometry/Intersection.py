# The function pointSide determines whether a given point is on the left or right side of a line, or on the line
# Using this function, it is possible to check whether two lines intersect with each other
# Using all of the above functions, it is possible to check whether a given point lies within a polygon

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
    
def pointSide(s1: Point, s2: Point, p: Point):
    result = (p-s1)*(p-s2)
    if result < 0: 
        return -1 # right side
    elif result > 0: 
        return 1 # left side
    else:
        return 0 # collinear, i.e. p is on the line s1s2
    
def pointOnLine(s1: Point, s2: Point, p: Point):
    return (p-s1)*(p-s2) == 0 and sorted((s1, s2, p), key=lambda x: (x.x, x.y))[1] == p
    
def lineIntersection(l1p1: Point, l1p2: Point, l2p1: Point, l2p2: Point):
    # Case 1: line segment overlap
    if pointSide(l1p1, l1p2, l2p1) == 0 and pointSide(l1p1, l1p2, l2p2) == 0:
        points = sorted([l1p1, l2p2, l2p1, l2p2], key = lambda p: (p.x, p.y))
        if set(points[:2]) not in ({l1p1, l2p2}, {l2p1, l2p2}):
            return True
    # Case 2: single point overlap
    if l1p1 == l2p1 or l1p1 == l2p2 or l1p2 == l2p1 or l1p2 == l2p2:
        return True
    # Case 3: line intersection overlap
    if pointSide(l1p1, l1p2, l2p1) != pointSide(l1p1, l1p2, l2p2) and pointSide(l2p1, l2p2, l1p1) != pointSide(l2p1, l2p2, l1p2):
        return True
    return False

def insidePolygon(polygon: list[Point], p: Point):
    """
    Determine whether p is within polygon by sending a horizontal ray to the right
    If the number of intersections is odd, then p is within polygon; otherwise, it is outside
    Two special cases must be handled: ray crossing vertices and ray overlapping with edges
    For a vertex to count, its neighbouring vertices must lie on different sides of the ray
    For a side to count, their neighbouring vertices must be on different sides of the ray
    NOTE: There cannot be more than 2 collinear vertices on the same edge, those must be removed
    """
    rayend = max(v.x for v in polygon)
    if rayend < p.x:
        return False # p obviously lies outside of polygon
    ray = Point(rayend, p.y)
    polygon = [polygon[-1]] + polygon + [polygon[0], polygon[1]] # extending list for special case handling
    crosscount = 0 # number of intersections/crosses the ray made with the polygon
    for i in range(1, len(polygon)-2):
        if pointOnLine(polygon[i], polygon[i+1], p): # p lies on an edge
            return True
        if pointOnLine(p, ray, polygon[i]): # crossing vertex 1
            if pointOnLine(p, ray, polygon[i+1]): # crossing vertex 2, overlapping edge
                if lineIntersection(p, ray, polygon[i-1], polygon[i+2]): # neighbouring vertices on different sides
                    crosscount += 1
            else: # one vertex crossed only
                if lineIntersection(p, ray, polygon[i-1], polygon[i+1]): # neighbouring vertices on different sides
                    crosscount += 1
        else: # no vertex crossed
            if lineIntersection(p, ray, polygon[i], polygon[i+1]): # ray intersects with edge
                crosscount += 1
    if crosscount % 2:
        return True
    else:
        return False 

    
# print(pointSide(Point(0, 0), Point(1, 2), Point(0, 1))) # left
# print(lineIntersection(Point(0, 0), Point(2, 0), Point(1, 1), Point(1, -1))) # true
# print(lineIntersection(Point(0, 0), Point(2, 0), Point(1, 3), Point(1, 1))) # false
# print(lineIntersection(Point(0, 0), Point(2, 0), Point(1, 1), Point(1, 0))) # true

# print(insidePolygon([Point(0, 0), Point(10, 0), Point(10, 10), Point(0, 10)], Point(5, 3))) # true
# print(insidePolygon([Point(0, 0), Point(10, 0), Point(10, 10), Point(0, 10)], Point(0, 11))) # false
# print(insidePolygon([Point(0, 0), Point(10, 0), Point(10, 10), Point(0, 10)], Point(11, 11))) # false
# print(insidePolygon([Point(0, 0), Point(10, 0), Point(10, 10), Point(0, 10)], Point(5, 10))) # true
# print(insidePolygon([Point(0, 0), Point(10, 0), Point(10, 10), Point(0, 10)], Point(0, 0))) # true