"""
Helper classes and functions that have not yet been categorized
"""


class Grid2D(list):
    def __init__(self, width):
        """
        :param int width: size of the grid in X
        """
        super(Grid2D, self).__init__()
        self.width = width

    def get(self, x, y):
        """
        :param int x: the x position of the value to retrieve
        :param int y: the y position of the value to retrieve

        :return: the value at the input coordinates
        """
        return self[x * self.width + y]

    def set(self, x, y, value):
        """
        :param int x: the x position of the value to set
        :param int y: the y position of the value to set
        :param value: the value to store at the desired location
        """
        index = x * self.width + y
        if (index + 1) > len(self):
            self.append(None)

        self[index] = value

    def has(self, value):
        """
        :param value: the value to search for in the grid

        :return bool: if the value was found in the grid
        """
        for i, item in enumerate(self):
            if item == value:
                return True

        return False

    def find(self, value):
        """
        :param value: the value to find
        :return list[tuple]: list of coordinates where the value can be found
        """
        outList = []

        for i, item in enumerate(self):
            if item == value:
                outList.append((i / self.width, i % self.width))

        return outList

    def __str__(self):
        outStr = ''
        rows = int(len(self) / self.width)
        columns = self.width
        for y in range(rows):
            outStr += ','.join(self[y:y+self.width]) + '\n'

        return outStr

