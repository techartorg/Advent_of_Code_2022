"""
Python day09

--- Day 9: Rope Bridge ---
This rope bridge creaks as you walk along it. You aren't sure how old it is, or whether it can even support your weight.

It seems to support the Elves just fine, though. The bridge spans a gorge which was carved out by the massive river far below you.

You step carefully; as you do, the ropes stretch and twist. You decide to distract yourself by modeling rope physics; maybe you can even figure out where not to step.

Consider a rope with a knot at each end; these knots mark the head and the tail of the rope. If the head moves far enough away from the tail, the tail is pulled toward the head.

Due to nebulous reasoning involving Planck lengths, you should be able to model the positions of the knots on a two-dimensional grid. Then, by following a hypothetical series of motions (your puzzle input) for the head, you can determine how the tail will move.

Due to the aforementioned Planck lengths, the rope must be quite short; in fact, the head (H) and tail (T) must always be touching (diagonally adjacent and even overlapping both count as touching):

....
.TH.
....

....
.H..
..T.
....

...
.H. (H covers T)
...
If the head is ever two steps directly up, down, left, or right from the tail, the tail must also move one step in that direction so it remains close enough:

.....    .....    .....
.TH.. -> .T.H. -> ..TH.
.....    .....    .....

...    ...    ...
.T.    .T.    ...
.H. -> ... -> .T.
...    .H.    .H.
...    ...    ...
Otherwise, if the head and tail aren't touching and aren't in the same row or column, the tail always moves one step diagonally to keep up:

.....    .....    .....
.....    ..H..    ..H..
..H.. -> ..... -> ..T..
.T...    .T...    .....
.....    .....    .....

.....    .....    .....
.....    .....    .....
..H.. -> ...H. -> ..TH.
.T...    .T...    .....
.....    .....    .....
You just need to work out where the tail goes as the head follows a series of motions. Assume the head and the tail both start at the same position, overlapping.

For example:

R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
This series of motions moves the head right four steps, then up four steps, then left three steps, then down one step, and so on. After each step, you'll need to update the position of the tail if the step means the head is no longer adjacent to the tail. Visually, these motions occur as follows (s marks the starting position as a reference point):

== Initial State ==

......
......
......
......
H.....  (H covers T, s)

== R 4 ==

......
......
......
......
TH....  (T covers s)

......
......
......
......
sTH...

......
......
......
......
s.TH..

......
......
......
......
s..TH.

== U 4 ==

......
......
......
....H.
s..T..

......
......
....H.
....T.
s.....

......
....H.
....T.
......
s.....

....H.
....T.
......
......
s.....

== L 3 ==

...H..
....T.
......
......
s.....

..HT..
......
......
......
s.....

.HT...
......
......
......
s.....

== D 1 ==

..T...
.H....
......
......
s.....

== R 4 ==

..T...
..H...
......
......
s.....

..T...
...H..
......
......
s.....

......
...TH.
......
......
s.....

......
....TH
......
......
s.....

== D 1 ==

......
....T.
.....H
......
s.....

== L 5 ==

......
....T.
....H.
......
s.....

......
....T.
...H..
......
s.....

......
......
..HT..
......
s.....

......
......
.HT...
......
s.....

......
......
HT....
......
s.....

== R 2 ==

......
......
.H....  (H covers T)
......
s.....

......
......
.TH...
......
s.....
After simulating the rope, you can count up all of the positions the tail visited at least once. In this diagram, s again marks the starting position (which the tail also visited) and # marks other positions the tail visited:

..##..
...##.
.####.
....#.
s###..
So, there are 13 positions the tail visited at least once.

Simulate your complete hypothetical series of motions. How many positions does the tail of the rope visit at least once?
"""
import copy
import math

from utils.math import Grid2D, Int2
from utils.solver import ProblemSolver


class Rope(list):
    def __init__(self, length=2, start=None):
        """
        :param int length: how long the rope is, defaults to 2
        :param Int2 start: where the starting position of the rope is
        """
        super(Rope, self).__init__()
        if not start:
            start = Int2((0, 0))
        for i in range(length):
            self.append(copy.copy(start))

    @property
    def head(self):
        return self[0]

    @head.setter
    def head(self, coords):
        """
        :param Int2 coords: the new position of the head
        """
        self[0] = coords
        # have to actually simulate this motion, since looking up the position of the next coordinate from
        # the previous one doesn't exactly work with longer chains
        for i, coord in enumerate(self[1:], start=1):
            head = self[i-1]
            if math.floor(head.distance(coord)) >= 2:
                self[i] += self[i].direction(head)

    @property
    def tail(self):
        """
        :return Int2: position of the tail
        """
        return self[-1]

    @tail.setter
    def tail(self, value):
        raise NotImplementedError("Rope tail coordinates are not assignable")


class RopeGrid(Grid2D):
    def __init__(self, width, rope):
        data = '.' * (width * width)
        super(RopeGrid, self).__init__(width, data)
        self.rope = rope

    def moveRope(self, direction):
        self.rope.head += direction

        self[self.rope.tail] = 1

    def displayRope(self):
        outString = '\n'
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                curr = Int2((x,y))
                if curr == self.rope.head:
                    outString += 'H'
                elif curr == self.rope.tail:
                    outString += 'T'
                elif curr in self.rope:
                    outString += str(self.rope.index(curr))
                else:
                    outString += '.'
            outString += '\n'

        return outString


class Day09Solver(ProblemSolver):
    def __init__(self):
        super(Day09Solver, self).__init__(9)

        self.testDataAnswersPartOne = [13]
        self.testDataAnswersPartTwo = [1, 36]

    def ProcessInput(self, data=None):
        """
        Take the input data, and figure out 1 how big the grid should be and 2 the move instructions
        turned into int2
        :param str data:
        :returns int, list[Int2]:
        """
        if not data:
            data = self.rawData

        pointer = Int2((0,0))
        maxX = 0
        maxY = 0
        minX = 10000000000
        minY = 10000000000
        instructions = []
        for line in data.splitlines(keepends=False):
            directionString, distance = line.split(' ')
            distance = int(distance)
            # figure out which direction we should be going based off the string
            match directionString:
                case 'R':
                    direction = Grid2D.Right
                case 'L':
                    direction = Grid2D.Left
                case 'U':
                    direction = Grid2D.Up
                case 'D':
                    direction = Grid2D.Down
                case _:
                    raise ValueError(f"Invalid direction string {directionString}")

            # then create discrete move commands for the total distance we're meant to move
            instructions.append((direction, distance))

            # and move the pointer
            pointer += (direction * distance)
            maxX = max(pointer.x, maxX)
            maxY = max(pointer.y, maxY)
            minX = min(pointer.x, minX)
            minY = min(pointer.y, minY)

        # figure out the max size of the grid, since grid coords can't go negative
        width = max(maxX + abs(minX), maxY + abs(minY)) + 1
        # and make the start offset the minX, minY so that we know we can always reach the edge safely
        startOffset = Int2((minX, minY))

        # then return that width, and the pre-parsed instructions
        return width, startOffset, instructions

    def SolvePartOne(self, data=None):
        """
        
        :param data:
        :returns: The solution to today's challenge
        """
        if not data:
            data = copy.deepcopy(self.processed)

        width, startOffset, instructions = data
        # populate the grid

        rope = Rope(length=2, start=startOffset)
        grid = RopeGrid(width, rope)

        for direction, distance in instructions:
            for d in range(distance):
                grid.moveRope(direction)

        return grid.count(1)

    def SolvePartTwo(self, data=None):
        """
        
        :param data:
        :returns: The solution to part two of today's challenge
        """
        if not data:
            data = copy.deepcopy(self.processed)

        width, startOffset, instructions = data

        # populate the grid
        rope = Rope(length=10, start=startOffset)
        grid = RopeGrid(width, rope)

        for direction, distance in instructions:
            for d in range(distance):
                grid.moveRope(direction)

        return grid.count(1)


if __name__ == '__main__':
    day09 = Day09Solver()
    day09.Run()
