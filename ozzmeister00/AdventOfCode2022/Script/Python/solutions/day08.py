"""
Python day08

--- Day 8: Treetop Tree House ---
The expedition comes across a peculiar patch of tall trees all planted carefully in a grid. The Elves explain that a previous expedition planted these trees as a reforestation effort. Now, they're curious if this would be a good location for a tree house.

First, determine whether there is enough tree cover here to keep a tree house hidden. To do this, you need to count the number of trees that are visible from outside the grid when looking directly along a row or column.

The Elves have already launched a quadcopter to generate a map with the height of each tree (your puzzle input). For example:

30373
25512
65332
33549
35390
Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.

A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. Only consider trees in the same row or column; that is, only look up, down, left, or right from any given tree.

All of the trees around the edge of the grid are visible - since they are already on the edge, there are no trees to block the view. In this example, that only leaves the interior nine trees to consider:

The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom since other trees of height 5 are in the way.)
The top-middle 5 is visible from the top and right.
The top-right 1 is not visible from any direction; for it to be visible, there would need to only be trees of height 0 between it and an edge.
The left-middle 5 is visible, but only from the right.
The center 3 is not visible from any direction; for it to be visible, there would need to be only trees of at most height 2 between it and an edge.
The right-middle 3 is visible from the right.
In the bottom row, the middle 5 is visible, but the 3 and 4 are not.
With 16 trees visible on the edge and another 5 visible in the interior, a total of 21 trees are visible in this arrangement.

Consider your map; how many trees are visible from outside the grid?
"""
import copy
import functools
import itertools

from utils.math import Int2, Grid2D, product
from utils.solver import ProblemSolver


class VisibilityGrid(Grid2D):
    def __init__(self, width, defaultVisible=False):
        """
        A Grid2D for tracking visibility. Just ones and zeros.
        :param int width: how wide the grid is
        :param bool defaultVisible: if true, will default visibility to 1
        """
        super(VisibilityGrid, self).__init__(width, data=[1 if defaultVisible else 0]*(width * width))

    def isVisible(self, coord):
        """
        :param Int2 coord: the coordinate to check
        :return bool: if the coordinate is marked as visible
        """
        return bool(self[coord])

    def markVisible(self, coord):
        """
        Mark a coordinate as visible
        :param Int2 coord: the coordinate to mark
        """
        self[coord] = 1

    def markInvisible(self, coord):
        """
        Mark a coordinate as invisible
        :param Int2 coord: the coordinate to mark
        """
        self[coord] = 0

    def getVisibleCoordinates(self):
        """
        :return list[Int2]: the coordinates in the grid that are visible
        """
        return [self.indexToCoords(i) for i, value in enumerate(self) if value]

    def getInvisibleCoordinates(self):
        """
        :return list[Int2]: the coordinates in the grid that aren't visible
        """
        return [self.indexToCoords(i) for i, value in enumerate(self) if not value]

    def getVisibleCount(self):
        """
        :return int: the number of visible coordiantes in the grid
        """
        return self.count(1)


class TreeMap(Grid2D):
    def __init__(self, width, data=None):
        super(TreeMap, self).__init__(width, data=data)

        # initialize the visible grid with all the edges being visible
        self.visibilityGrid = VisibilityGrid(width)

        for x in [0, width - 1]:
            for y in range(width):
                self.visibilityGrid.markVisible(Int2((x, y)))
                self.visibilityGrid.markVisible(Int2((y, x)))

    def _getVisibleTreesInLine(self, enumerateFunction, startingPoint, nextOne, reverse=False):
        """
        Internal method for keeping functionality to parse either rows OR columns for visibility
        frontwards and backwards

        :param func enumerateFunction: the enumerating function to use
        :param int startingPoint: which row or column to parse
        :param Int2 nextOne: how to get to the next coordinate in the row or column

        :return list[Int2]: coordinates that are visible in this line from front and back
        """

        lineSoFar = []  # to keep track of the tree heights we've run into so far
        visibleCoords = []

        for coord, value in enumerateFunction(startingPoint, reverse=reverse):
            # a tree is visible if it's taller than all the other trees in the line
            if all([value > x for x in lineSoFar]):
                self.visibilityGrid.markVisible(coord)
                visibleCoords.append(coord)
            lineSoFar.append(value)

        return visibleCoords

    def getVisibleTreesInRow(self, row):
        """
        Find all the trees that are visible from either side of the input row

        :param int row: the row to test
        :return list[Int2]: coordinates of the trees visible in this row
        """
        visibleCoords = []
        visibleCoords += self._getVisibleTreesInLine(self.enumerateRow, row, Int2((1, 0)), reverse=False)
        visibleCoords += self._getVisibleTreesInLine(self.enumerateRow, row, Int2((-1, 0)), reverse=True)

        return list(set(visibleCoords))

    def getVisibleTreesInColumn(self, column):
        """
        Find all the trees that are visible from either side of the input column

        :param int column: the column to test
        :return list[Int2]: coordinates of the trees visible in this row
        """
        visibleCoords = []
        visibleCoords += self._getVisibleTreesInLine(self.enumerateColumn, column, Int2((0, 1)), reverse=False)
        visibleCoords += self._getVisibleTreesInLine(self.enumerateColumn, column, Int2((0, -1)), reverse=True)

        return list(set(visibleCoords))

    def getVisibleTrees(self):
        """
        Loop through all the trees to find which ones are visible from the edge

        :return list[Int2]: coordinates of visible trees
        """
        for x in range(1, self.width - 1):
            self.getVisibleTreesInColumn(x)

        for y in range(1, self.width - 1):
            self.getVisibleTreesInRow(y)

        return self.visibilityGrid.getVisibleCoordinates()

    def getVisibleTreesFromPoint(self, coords):
        """
        Figure out how many trees are visible from the current point

        :param Int2 coords: the point to test from
        :return int: the number of visible trees
        """
        # get the points that are up, down, left, right to the edge from the current coordinate
        up = Int2((coords.x, 0))
        down = Int2((coords.x, self.width - 1))
        left = Int2((0, coords.y))
        right = Int2((self.width-1, coords.y))

        toUp = list(reversed(self[up:coords]))
        toDown = self[coords:down]
        toLeft = list(reversed(self[left:coords]))
        toRight = self[coords:right]

        visibleTrees = []

        for line in [toUp, toDown, toLeft, toRight]:
            if len(line) > 1:
                i = 0
                currTree = line[i+1]
                while i < len(line) - 1 and currTree < self[coords]:
                    currTree = line[i+1]
                    i += 1
                # special case for when the immediate neighbor tree is a blocker
                if currTree >= self[coords] and i == 0:
                    i += 1
                visibleTrees.append(i)
            else:
                visibleTrees.append(0)

        return product(visibleTrees)


class Day08Solver(ProblemSolver):
    def __init__(self):
        super(Day08Solver, self).__init__(8)

        self.testDataAnswersPartOne = [21]
        self.testDataAnswersPartTwo = [8]

    def ProcessInput(self, data=None):
        """
        
        :param data:
        :returns: processed data for today's challenge
        """
        if not data:
            data = self.rawData

        lines = data.splitlines(keepends=False)
        width = len(lines[0])

        # flatten out the 2d grid
        strippedData = [int(i) for i in data.replace('\n', '')]

        processed = TreeMap(width, data=strippedData)

        return processed

    def SolvePartOne(self, data=None):
        """
        
        :param TreeMap data:
        :returns int: The number of trees visibile from outside the grid
        """
        if not data:
            data = copy.deepcopy(self.processed)

        visibleTrees = data.getVisibleTrees()

        print(data.visibilityGrid)

        return len(visibleTrees)

    def SolvePartTwo(self, data=None):
        """
        
        :param TreeMap data:
        :returns: The solution to part two of today's challenge
        """
        if not data:
            data = copy.deepcopy(self.processed)

        viewScores = []

        # loop over all the trees that aren't on the edge and get their view distances
        # since edge trees will have at least 1 view distance of 0 which will null out its
        # view score
        for x in range(1, data.width - 1):
            for y in range(1, data.width - 1):
                viewScores.append(data.getVisibleTreesFromPoint(Int2((x, y))))

        return max(viewScores)

if __name__ == '__main__':
    day08 = Day08Solver()
    day08.Run()
