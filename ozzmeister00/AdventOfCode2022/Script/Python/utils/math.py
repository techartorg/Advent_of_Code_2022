"""
Common maths functions and datatypes for solving Advent of Code problems
"""

import math
import functools
import operator

def saturate(value):
    """
    Saturates a value, so it is only ever between 0 and 1

    :param float value: the value to saturate

    :return float: the value, but clamped between 0 and 1
    """
    return clamp(value, 0.0, 1.0)


def clamp(value, minValue, maxValue):
    """
    Returns a value that is no less than the min value, and no more than the max value

    :param float value: the value to clamp
    :param float minValue: the minimum value to return
    :param float maxValue: the maximum value to return

    :return float: the clamped value
    """
    return max(minValue, min(value, maxValue))


def product(iterable):
    """
    Returns the product of an iterable of numbers
    :param list iterable: eg [1, 2, 3, 4, 5]
    :return float: the product of all items in the iterable multiplied together
    """
    return functools.reduce(operator.mul, iterable, 1)



class TwoD(list):
    """
    A TwoD object to make it easier to access and multiply 2-length lists of numbers
    """
    def __init__(self, inV=None, defaultClass=None):
        """
        :param class baseClass: which datatype class to use to instantiate the array
        :param iterable inV: two-length iterable of class defaultClass
        """
        # set up a default input value to instatiate a float 2 to 0,0 automatically
        # because we can't put a [0,0] in the kwargs otherwise it'll be the same
        # for every instance and that's no bueno
        if not inV:
            inV = [defaultClass(), defaultClass()]
        else:
            inV = [defaultClass(v) for v in inV]  # convert our inputData to a list

        self.defaultClass = defaultClass

        super(TwoD, self).__init__(inV)

    def __add__(self, other):
        if isinstance(other, TwoD):
            return self.__class__([self.x + other.x, self.y + other.y], defaultClass=self.defaultClass)
        else:
            return self.__class__([self.x + other, self.y + other], defaultClass=self.defaultClass)

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, TwoD):
            return self.__class__([self.x - other.x, self.y - other.y], defaultClass=self.defaultClass)
        else:
            return self.__class__([self.x - other, self.y - other], defaultClass=self.defaultClass)

    def __isub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__([self.x * other.x, self.y * other.y], defaultClass=self.defaultClass)
        if isinstance(other, int) or isinstance(other, float):
            return self.__class__([self.x * other, self.y * other], defaultClass=self.defaultClass)

    def __imul__(self, other):
        return self.__mul__(other)

    def _div(self, other):
        if isinstance(other, self.__class__):
            return self.__class__([self.x / other.x, self.y / other.y], defaultClass=self.defaultClass)
        if isinstance(other, int) or isinstance(other, float):
            return self.__class__([self.x / other, self.y / other], defaultClass=self.defaultClass)

    def __truediv__(self, other):
        return self._div(other)

    def __itruediv__(self, other):
        return self._div(other)

    def __divmod__(self, other):
        return self._div(other)

    def __idiv__(self, other):
        return self._div(other)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.x == other.x and self.y == other.y:
                return True

        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.x, self.y))

    @property
    def x(self):
        """
        Access the first, X value of the list
        :return float:
        """
        return self[0]

    @x.setter
    def x(self, v):
        self[0] = v

    @property
    def y(self):
        """
        The second, Y value of the list
        :return float:
        """
        return self[1]

    @y.setter
    def y(self, v):
        self[1] = v


class Number2(TwoD):
    """
    Wrapper around numerical two-d classes with common methods shared between them
    """
    def distance(self, other):
        """
        :param Number2 other: the other point to which we want the distance

        :return float: the distance from this point to the input point
        """
        if not issubclass(other.__class__, Number2):
            raise ValueError("{} is not a subclass of Number2 and its distance cannot be computed".format(other.__class__))

        return math.sqrt(((other.x - self.x) ** 2) + ((other.y - self.y) ** 2))

    def direction(self, other):
        """

        :param Number2 other: the other point to which we want to determine the direction

        :return Number2: the direction from this point to the other point
        """
        return (other - self).normalize()

    def normalize(self):
        """
        :return Number2: this number, normalized to its length
        """
        return self / self.length()

    def length(self):
        """
        :return float: the distance from 0,0 to this point
        """
        return self.__class__((0, 0)).distance(self)


class Float2(Number2):
    """
    Float-specific alias for TwoD
    """
    def __init__(self, inV=None, defaultClass=float):
        super(Float2, self).__init__(inV, defaultClass=float)


class Int2(Number2):
    """
    Alias for TwoD
    """
    def __init__(self, inV=None, defaultClass=int):
        super(Int2, self).__init__(inV, defaultClass=int)

    def __truediv__(self, other):
        # if an int2 is divided by a float, return the ceil of that division
        if isinstance(other, float):
            x = self.x / other
            y = self.y / other

            x = math.ceil(x) if x > 0 else math.floor(x)
            y = math.ceil(y) if y > 0 else math.floor(y)

            return Int2((x, y))

        return super(Int2, self).__truediv__(other)

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @x.setter
    def x(self, value):
        self[0] = int(value)

    @y.setter
    def y(self, value):
        self[1] = int(value)


def dot(a, b):
    """
    :param list a: list of numbers
    :param list b: list of numbers equal in length to the first list
    :return float: dot product of n-length lists of numbers
    """
    if len(a) != len(b):
        raise ValueError("Input lists must be of equal length (got {} and {})".format(len(a), len(b)))

    return sum([x * y for x, y in zip(a, b)])


def getBarycentric(p, a, b, c):
    """
    Get the barycentric coordinates of cartesin point a in
    reference frame abc

    :param Float2 p: test point
    :param Float2 a: point A
    :param Float2 b: point B
    :param Float2 c: point C

    :return list: the UVW coordinate of cartesian point P in reference frame created by points ABC
    """
    v0 = b - a  # Vector BA
    v1 = c - a  # Vector CA
    v2 = p - a  # Vector PA
    d00 = dot(v0, v0)  # dot BA . BA
    d01 = dot(v0, v1)  # dot BA . CA
    d11 = dot(v1, v1)  # dot CA . CA
    d20 = dot(v2, v0)  # dot PA . BA
    d21 = dot(v2, v1)  # dot PA . CA

    denom = (d00 * d11) - (d01 * d01)

    v = (d11 * d20 - d01 * d21) / denom
    w = (d00 * d21 - d01 * d20) / denom
    u = 1.0 - v - w

    return u, v, w


class Grid2D(list):
    Up = Int2((0, 1))
    Down = Int2((0, -1))
    Left = Int2((-1, 0))
    Right = Int2((1, 0))

    orthoNeighbors = [Right, Up, Left, Down]

    def __init__(self, width, data=None):
        """
        :param int width: how wide is the 2D Grid
        :param iterable data: a 1d iterable with which to instantiate the grid
        """
        super(Grid2D, self).__init__(data)
        self._width = width

    @property
    def width(self):
        """
        Get the width of the Grid2D
        :return int:
        """
        return self._width

    @width.setter
    def width(self, value):
        """
        Changing the width of the Grid2D will necessarily affect its height (since "height" is just a function
        of how many bits of data are in the grid) BUT it won't fill any gaps created by changing the total area
        of the grid. Changing this value should be done with extreme caution

        TODO: find a way to support grid resizing that pads the data out, or removes data based on the change in area
        """
        self._width = value

    @property
    def height(self):
        """
        Get the height of the Grid2D
        :return int:
        """
        return int(len(self) / self.width)

    @height.setter
    def height(self, value):
        """
        Grid2D doesn't support resizing yet
        """
        raise NotImplementedError("Grid2D's height is a function of its width, and the length of data it contains"
                                  "until I can figure out a good way to pad and clear data as the area of the "
                                  "grid changes.")

    def _coordsToIndex(self, coords):
        """
        :param Int2 or int coords: the 2d coordinates to translate to 1d,
                                    will just pass through coords if it's an integer

        :return int: 1d index
        """
        if isinstance(coords, Int2):
            return coords.y * self.width + coords.x

        return coords

    def coordsToIndex(self, coords):
        """
        Exposing the method this way, because I'm not sure why I needed this
        to be internal only
        """
        self._coordsToIndex(coords)

    def indexToCoords(self, index):
        """
        :param int coords: the 1d coordinate in the grid to seek

        :return Int2: the x/y coordinate of the input index
        """
        if isinstance(index, int):
            return Int2((index % self.width, index / self.width))

        return index

    def coordsInBounds(self, coords):
        """
        Returns true if the input coordinates are within the bounds of this grid
        :param Int2 coords: 2d coordinates to check
        :returns bool: if the input coords are in bounds
        """
        # TODO there will come a day when I need to update this so that Grid2D supports non-0 starting coordinates
        return 0 <= coords.x < self.width and 0 <= coords.y < self.height

    def coordOnEdge(self, coord):
        """
        Return true if the input coordinate is on the edge of the grid

        :param Int2 coord:
        :return bool: if the input coord is on the edge
        """
        return coord.x == 0 or coord.y == 0 or coord.x == self.width-1 or coord.y == self.height - 1
    def enumerateOrthoLocalNeighbors(self, coords):
        """
        Returns a list of tuples of coordinate, value for each valid neighbor
        that is North, South, East, and West of the input coordinate

        :param Int2 coords: the coordinates from which to start
        :yield (coords, object): the next neighbor in the NSEW group around the input coordinate
        """
        for neighbor in Grid2D.orthoNeighbors:
            # TODO figure out why PyCharm thinks Int2 + Int2 returns a list
            localNeighbor = Int2(coords + neighbor)
            if self.coordsInBounds(localNeighbor):
                yield localNeighbor, self[localNeighbor]

    def enumerateNeighborsBox(self, coords, distance):
        """
        Yields all the neighbors in a square pattern that are x distance away from the input coords
        :param Int2 coords: the starting coordinates
        :param int distance: how many points away from the current point to search.
            A distance of 1 will yield up to 8 elements (a box that is 3 x 3)
            A distance of 2 will yield up to 24 elements (a box that is 5 x 5)

        :yields (coords, object): the next neighbor in the box surrounding the input point
        """
        if isinstance(coords, int):
            coords = self.indexToCoords(coords)

        for x in range(coords.x - distance, coords.x + distance + 1):
            for y in range(coords.y - distance, coords.y + distance + 1):
                point = Int2((x, y))
                if self.coordsInBounds(point):
                    yield point, self[point]

    def enumerateRow(self, y, reverse=False):
        """
        Yield the items from left to right in the given row
        :param int y: the row number to extract values from
        :param bool reverse: if True, will instead yield items from right to left
        :return (coords, object): the next item in the input row
        """
        step = 1 if not reverse else -1
        coords = list(range(self.width))
        for x in coords[::step]:
            coord = Int2((x, y))
            yield coord, self[coord]

    def enumerateColumn(self, x, reverse=False):
        """
        Yield the items from top to bottom in the given column

        :param int x: the column number to extract values from
        :param bool reverse: if True, will instead yield items from bottom to top
        :return (coords, object):the next item in the input column
        """
        step = 1 if not reverse else -1
        coords = list(range(self.height))
        for y in coords[::step]:
            coord = Int2((x, y))
            yield coord, self[coord]

    def copy(self):
        """
        Override the built-in copy method so it returns a proper Grid2D

        :returns Grid2D:
        """
        return Grid2D(self.width, data=self)

    def __getitem__(self, coords):
        """
        :param int, Int2 coords: the coordinates of the item to retrieve

        :returns: the item at the input coordinates
        """
        # use slice to get orthogonal lines
        if isinstance(coords, slice):
            if isinstance(coords.start, Int2) and isinstance(coords.stop, Int2):
                step = coords.step if coords.step else 1
                if step < 0:
                    raise ValueError("Grid2D slicing step must be positive")

                # slice in X if the X of start and end points are the same
                if coords.start.x == coords.stop.x:
                    if coords.start.y > coords.stop.y:
                        start = coords.stop.y
                        stop = coords.start.y
                    else:
                        start = coords.start.y
                        stop = coords.stop.y

                    return [self[Int2((coords.start.x, y))] for y in range(start, stop+1, step)]
                elif coords.start.y == coords.stop.y:
                    if coords.start.x > coords.stop.x:
                        start = coords.stop.x
                        stop = coords.start.x
                    else:
                        start = coords.start.x
                        stop = coords.stop.x

                    return [self[Int2((x, coords.start.y))] for x in range(start, stop+1, step)]
                else:
                    raise ValueError("Slicing only supports straight lines. Either Y or X must be the same in start and stop")
            else:
                raise ValueError("Grid2D slicing requires start and stop to be Int2")

        return super(Grid2D, self).__getitem__(self._coordsToIndex(coords))

    def __setitem__(self, coords, value):
        """
        :param Int2 coords: the coordinates of the item to set
        :param value: the value to which to set the coordinates
        """
        super(Grid2D, self).__setitem__(self._coordsToIndex(coords), value)

    def __delitem__(self, coords):
        """
        :param Int2 coords: the coordinates of the item to delete
        """
        super(Grid2D, self).__delitem__(self._coordsToIndex(coords))

    def __str__(self):
        outString = '\n'
        for y in range(self.height):
            for x in range(self.width):
                outString += str(self[Int2((x, y))]) + " "
            outString += '\n'

        return outString







