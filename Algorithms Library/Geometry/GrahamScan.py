# Graham scan constructs the convex hull of a set of points in n log n time

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

def grahamScanIncludeCollinear(points: list[Point]) -> list[Point]:
    # Computes the cross product of vectors p1p2 and p2p3
    # value of 0 means points are colinear; < 0, cw; > 0, ccw
    def cross(p1, p2, p3):
        return (p2.x - p1.x)*(p3.y - p1.y) - (p2.y - p1.y)*(p3.x - p1.x)

    # Computes slope of line between p1 and p2
    def slope(p1, p2):
        return 1.0*(p1.y-p2.y)/(p1.x-p2.x) if p1.x != p2.x else float('inf')

    # distance of p1 and p2
    def dis(p1, p2):
        return ((p1.x-p2.x)**2+(p1.y-p2.y)**2)**0.5
    
    # Find the smallest left point and remove it from points
    start = min(points, key=lambda p: (p.x, p.y))
    points.pop(points.index(start))

    # Sort points so that traversal is from start in a ccw circle.
    points_slopes = [(p, slope(p, start)) for p in points]
    points_slopes.sort(key=lambda e: e[1])
    points = []
    i = 0
    for j in range(1,len(points_slopes)):
        if points_slopes[j][1] != points_slopes[i][1]:
            if j-i == 1:
                points.append(points_slopes[i])
            else:
                points_cl = sorted(points_slopes[i:j], key=lambda e: dis(start, e[0]))
                points.extend(points_cl)
            i = j
    points_cl = sorted(points_slopes[i:], key=lambda e: -dis(start, e[0]))
    points.extend(points_cl)
    points = [p[0] for p in points]

    # Add each point to the convex hull.
    # If the last 3 points make a cw turn, the second to last point is wrong. 
    ans = [start]
    for p in points:
        ans.append(p)
        while len(ans) > 2 and cross(ans[-3], ans[-2], ans[-1]) < 0:
            ans.pop(-2)
    return ans


def grahamScanExcludeCollinear(points: list[Point]) -> list[Point]:
    # Computes the cross product of vectors p1p2 and p2p3
    # value of 0 means points are colinear; < 0, cw; > 0, ccw
    def cross(p1, p2, p3):
        return (p2.x - p1.x)*(p3.y - p1.y) - (p2.y - p1.y)*(p3.x - p1.x)

    # Computes slope of line between p1 and p2
    def slope(p1, p2):
        return 1.0*(p1.y-p2.y)/(p1.x-p2.x) if p1.x != p2.x else float('inf')
        
    # Find the smallest left point and remove it from points
    start = min(points, key=lambda p: (p.x, p.y))
    points.pop(points.index(start))
    
    # Sort points so that traversal is from start in a ccw circle.
    points.sort(key=lambda p: (slope(p, start), -p.y, p.x))
    
    # Add each point to the convex hull.
    # If the last 3 points make a cw turn, the second to last point is wrong. 
    ans = [start]
    for p in points:
        ans.append(p)
        while len(ans) > 2 and cross(ans[-3], ans[-2], ans[-1]) < 0:
            ans.pop(-2)
    
    return ans


# points = [Point(x, y) for x, y in [[0,0],[1,1],[2,2],[3,3],[1,2]]]
# print(grahamScanIncludeCollinear(points)) # [[0,0],[1,1],[2,2],[3,3],[1,2]]
# print(grahamScanExcludeCollinear(points)) # [[0,0],[3,3],[1,2]]
