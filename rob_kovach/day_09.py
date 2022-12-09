test_input = '''R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
'''

test_input2 = '''R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
'''

from math import copysign

puzzle_input = open(__file__.replace('.py', '_input.txt')).read()

class State:
    def __init__(self, knots=2):
        self.visited_locations = set()
        self.knots = [[0, 0]] * knots
    
    def distance_from_neighbor(self, knot):
        currentKnot = self.knots[knot]
        neighbor = self.knots[knot-1]
        return tuple(map(lambda x, y: x - y, neighbor, currentKnot))
    
    def move_head(self, offset):
        self.knots[0] = list(map(lambda x, y: x + y, self.knots[0], offset))
    
    def move_knot(self, knot):
        currentKnot = self.knots[knot]
        offset = [0, 0]
        x_distance, y_distance = self.distance_from_neighbor(knot)

        previousKnot = self.knots[knot-1]

        if abs(x_distance) > 1:
            offset[0] = int(1 * copysign(1, x_distance))
            if abs(y_distance) > 0:
                offset[1] = int(1 * copysign(1, y_distance))
        
        if abs(y_distance) > 1:
            offset[1] = int(1 * copysign(1, y_distance))
            if abs(x_distance) > 0:
                offset[0] = int(1 * copysign(1, x_distance))
        
        self.knots[knot] = list(map(lambda x, y: x + y, currentKnot, offset))

        if knot == len(self.knots) - 1:
            self.visited_locations.add(tuple(self.knots[knot]))

    def parse_input(self, input_):
        self.moves = []
        for l in input_.splitlines():
            dir, distance = l.split(' ')
            for i in range(int(distance)):
                if dir == 'R':
                    self.moves.append([1, 0])
                elif dir == 'L':
                    self.moves.append([-1, 0])
                elif dir == 'U':
                    self.moves.append([0, 1])
                else:
                    self.moves.append([0, -1])
    
    def solve(self, input_):
        self.parse_input(input_)
        for move in self.moves:
            self.move_head(move)
            for i in range(1, len(self.knots)):
                self.move_knot(i)
        return len(sorted(self.visited_locations))


test1 = State(2)
assert test1.solve(test_input) == 13
test2 = State(10)
assert test2.solve(test_input) == 1
test3 = State(10)
assert test3.solve(test_input2) == 36

x = State(2)
print(f'Part One: {x.solve(puzzle_input)}')

x = State(10)
print(f'Part Two: {x.solve(puzzle_input)}')
