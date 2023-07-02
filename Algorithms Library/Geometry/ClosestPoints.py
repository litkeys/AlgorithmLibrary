"""
Given a set of points, find the closest pair.

The algorithm uses a divide-and-conquer strategy
that splits the points into 2 regions recursively.
The solution lies either in the left region,
the right region, or between the 2 regions.

Therefore, there are three steps in total in
each recursive call:
- Calculate solution to the left region
- Calculate solution to the right region
- Calculate solution to the middle 'strip'

It is proven mathematically that calculating
the solution to the middle 'strip' takes only
O(n), see link below for further explanation:
https://www.cs.cmu.edu/~15451-s20/lectures/lec23-closest-pair.pdf

Therefore, the total time & space complexity is O(n log n)
"""

def distance_euclidean(point1: tuple[float, float], point2: tuple[float, float]) -> float:
    """
    >>> print(distance_euclidean((0, 0), (3, 4)))
    5.0
    """
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5

### Temporarily unneeded ###
# def distance_manhattan(point1: tuple[int, int], point2: tuple[int, int]) -> int:
#     """
#     >>> print(distance_manhattan((0, 0), (3, 4)))
#     7
#     """
#     return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def bruteforce_closest_pair(points: list[tuple[float, float]], min_distance = float("inf")) -> list[tuple[float, float]]:
    """
    Brute force O(n^2) algorithm to find the closest pair of points
    Only called when input size <= 3
    NOTE: Unless intended, do not call this function manually, as it is a helper function
    """
    closest_pair = None
    l = len(points)
    for i in range(l-1): # pick point 1
        for j in range(i+1, l): # pick point 2
            distance = distance_euclidean(points[i], points[j])
            if distance < min_distance:
                min_distance = distance
                closest_pair = [points[i], points[j]]
    return closest_pair

def _closest_pair_in_strip(points: list[tuple[float, float]], min_distance = float("inf")) -> list[tuple[float, float]]:
    """
    Linear O(n) algorithm to find the closest pair of points in a y-sorted 'strip'
    Each inner loop runs in O(1) as at most 7 other points besides or below are checked
    NOTE: DO NOT call this function manually, as it is a helper function
    """
    closest_pair = None
    l = len(points)
    for i in range(1, l): # pick point 1
        for j in range(max(0, i-5), i): # pick point 2
            distance = distance_euclidean(points[i], points[j])
            if distance < min_distance:
                min_distance = distance
                closest_pair = [points[i], points[j]]            
    return closest_pair

def _closest_pair_of_points(points_sorted_on_x: list[tuple[float, float]], points_sorted_on_y: list[tuple[float, float]], points_count: int) -> list[tuple[float, float]]:
    """
    Efficient O(n log n) algorithm for finding the closest pair of points given a sorted list of points
    To find the solution to the left & right regions, points_sorted_on_x are used
    To find the solution to the middle 'strip', points_sorted_on_y are used
    NOTE: DO NOT call this function manually, as it is a helper function
    """

    # base case, bruteforce-able as it cannot be further divided
    if points_count <= 3:
        return bruteforce_closest_pair(points_sorted_on_x)
    
    # divide and conquer with recursion for left and right regions
    m = points_count//2
    left_closest_pair = _closest_pair_of_points(points_sorted_on_x[:m], points_sorted_on_y[:m], m)
    left_distance = distance_euclidean(*left_closest_pair)
    right_closest_pair = _closest_pair_of_points(points_sorted_on_x[m:], points_sorted_on_y[m:], points_count-m)
    right_distance = distance_euclidean(*right_closest_pair)
    if left_distance < right_distance:
        closest_distance = left_distance
        closest_pair = left_closest_pair
    elif right_distance < left_distance:
        closest_distance = right_distance
        closest_pair = right_closest_pair
    else: # this is the default solution, which may need to be modified for specific problem requirements
        closest_distance = left_distance
        closest_pair = left_closest_pair
    
    # middle 'strip' calculation, optimised by ignoring the right half which includes the mth point
    points_in_strip = []
    for point in points_sorted_on_y: # only points from the left region are considered
        if abs(point[0] - points_sorted_on_x[m][0]) < closest_distance:
            points_in_strip.append(point)
    strip_closest_pair = _closest_pair_in_strip(points_in_strip, closest_distance)
    if strip_closest_pair != None:
        strip_distance = distance_euclidean(*strip_closest_pair)
    else:
        strip_distance = float("inf")

    # final solution
    if closest_distance < strip_distance:
        return closest_pair
    elif strip_distance < closest_distance:
        return strip_closest_pair
    else: # this is the default solution, which may need to be modified for specific problem requirements
        return closest_pair

def closest_pair_of_points(points: list[tuple[float, float]]):
    """
    Each point must be represented by a tuple (x, y)
    NOTE: Call this function to get the closest pair of points in an arbitrarily ordered set of points
    """
    points_count = len(points)
    points_sorted_on_x = sorted(points, key = lambda p: p[0])
    points_sorted_on_y = sorted(points, key = lambda p: p[1])
    return _closest_pair_of_points(points_sorted_on_x, points_sorted_on_y, points_count)



# if __name__ == "__main__":
#     points = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
#     closest_pair = closest_pair_of_points(points)
#     print("Distance:", distance_euclidean(*closest_pair))