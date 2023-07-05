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
    
    def distance_euclidean(self, other: 'vector2') -> float:
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
    
    def distance_manhattan(self, other: 'vector2') -> float:
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    # bound checking functions is included

    def within_bounds(self, x_bound: int, y_bound: int) -> bool: # assumes that lower bound is 0, excludes upper bound
        return 0 <= self.x < x_bound and 0 <= self.y < y_bound
    
    def within_bounds_inclusive(self, x_bound: int, y_bound: int) -> bool: # assumes that lower bound is 0, includes upper bound
        return 0 <= self.x <= x_bound and 0 <= self.y <= y_bound
    
    def within_bounds_custom(self, x_bound_lower: int, x_bound_upper: int, y_bound_lower: int, y_bound_upper: int) -> bool:
        return x_bound_lower <= self.x < x_bound_upper and y_bound_lower <= self.y < y_bound_upper
    
    def within_bounds_custom_inclusive(self, x_bound_lower: int, x_bound_upper: int, y_bound_lower: int, y_bound_upper: int) -> bool:
        return x_bound_lower <= self.x <= x_bound_upper and y_bound_lower <= self.y <= y_bound_upper
    
    # five identity-returning class functions are included

    def zero() -> 'vector2': 
        return vector2(0, 0)
    
    def left() -> 'vector2':
        return vector2(-1, 0)
    
    def right() -> 'vector2':
        return vector2(1, 0)
    
    def up() -> 'vector2':
        return vector2(0, 1)
    
    def down() -> 'vector2':
        return vector2(0, -1)
    
    # four movement functions are included

    def move_left(self) -> 'vector2':
        return vector2(self.x - 1, self.y)
    
    def move_right(self) -> 'vector2':
        return vector2(self.x + 1, self.y)
    
    def move_up(self) -> 'vector2':
        return vector2(self.x, self.y + 1)
    
    def move_down(self) -> 'vector2':
        return vector2(self.x, self.y - 1)
    
    # two turning functions are included, which assumes that the vector2 holds the direction identities
    # i.e. left, right, up, down

    clockwise_directions = {(1, 0): (0, -1), (0, -1): (-1, 0), (-1, 0): (0, 1), (0, 1): (1, 0)}
    anticlockwise_directions = {(1, 0): (0, 1), (0, 1): (-1, 0), (-1, 0): (0, -1), (0, -1): (1, 0)}

    def turn_left(self, ntimes: int = 1) -> None: # modifies vector2 in-place
        for i in range(ntimes%4):
            self.x, self.y = vector2.anticlockwise_directions[(self.x, self.y)]
    
    def turn_right(self, ntimes: int = 1) -> None: # modifies vector2 in-place
        for i in range(ntimes%4):
            self.x, self.y = vector2.clockwise_directions[(self.x, self.y)]
    
    # functions to get neighbour coordinates, which return tuples (to save memory)

    def neighbours(self) -> tuple['vector2']: # clockwise starting from right, ends at top
        return self.move_right(), self.move_down(), self.move_left(), self.move_up() 
    
    def neighbours_eight(self) -> tuple['vector2']: # clockwise starting from top right, ends at top
        return vector2(self.x+1, self.y+1), self.move_right(), vector2(self.x+1, self.y-1), self.move_down(), vector2(self.x-1, self.y-1), self.move_left(), vector2(self.x-1, self.y+1), self.move_up()
    
    # functions to generate circles using manhattan distance

    def generate_circle_filled(radius: int) -> tuple['vector2']:
        circle_area: set[tuple[int]] = set()
        for i in range(-radius, radius+1):
            for j in range(radius-abs(i)+1):
                circle_area.add((i, j))
                circle_area.add((i, -j))
        return tuple(vector2(x, y) for x, y in circle_area)
    
    def generate_circle_hollow(radius: int) -> tuple['vector2']:
        circle_edge: set[tuple[int]] = set()
        for i in range(-radius, radius+1):
            j = radius-abs(i)
            circle_edge.add((i, j))
            circle_edge.add((i, -j))
        return tuple(vector2(x, y) for x, y in circle_edge)
    
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
    
    # copy method

    def copy(self) -> 'vector2':
        return vector2(self.x, self.y)