"""
Python day10
"""
import copy

from utils.solver import ProblemSolver


class Commands(object):
    noop = 'noop'
    addx = 'addx'


class Day10Solver(ProblemSolver):
    def __init__(self):
        super(Day10Solver, self).__init__(10)

        self.testDataAnswersPartOne = [13140]
        self.testDataAnswersPartTwo = ['''##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....''']
        self.cycleTargets = [20, 60, 100, 140, 180, 220]

    def ProcessInput(self, data=None):
        """

        :param data:
        :returns: processed data for today's challenge
        """
        if not data:
            data = self.rawData

        processed = []
        for line in data.splitlines(keepends=False):
            if line == Commands.noop:
                processed.append((line, 0))
            else:
                command, value = line.split(' ')
                value = int(value)
                processed.append((command, value))

        return processed

    def fillBuffer(self, operations):
        """
        Fill a buffer will the register values during each cycle
        :param list[(str, int)] operations: the list of operations to fill the buffer
        :return list[int]: register values during each cycle
        """
        register = 1
        values = [register]

        for command, value in operations:
            values.append(register)
            if command == Commands.addx:
                values.append(register)
                register += value

        return values

    def SolvePartOne(self, data=None):
        """

        :param data:
        :returns: The solution to today's challenge
        """
        if not data:
            data = copy.deepcopy(self.processed)

        buffer = self.fillBuffer(data)

        cycleChecks = [buffer[i] * i for i in self.cycleTargets]

        return sum(cycleChecks)

    def SolvePartTwo(self, data=None):
        """

        :param data:
        :returns: The solution to part two of today's challenge
        """
        if not data:
            data = copy.deepcopy(self.processed)

        buffer = self.fillBuffer(data)

        outString = ''
        for i, value in enumerate(buffer):
            if i % 40 == 0:
                outString += '\n'

            left = i - 1
            right = i + 1
            # if we're bang-on the middle of the sprite
            if buffer[i] % i == 0:
                outString += '#'
            elif 0 <= left < len(buffer):
                if buffer[left] % i == 0:
                    outString += '#'
                else:
                    outString += '.'
            elif 0 <= right < len(buffer):
                if buffer[right] % i == 0:
                    outString += '#'
                else:
                    outString += '.'
            else:
                outString += '.'

        print(outString)
        return outString


if __name__ == '__main__':
    day10 = Day10Solver()
    day10.Run()
