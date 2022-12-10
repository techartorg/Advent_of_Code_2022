"""
Python day04.py

--- Day 4: Camp Cleanup ---
Space needs to be cleared before the last supplies can be unloaded from the ships, and so several Elves have been assigned the job of cleaning up sections of the camp. Every section has a unique ID number, and each Elf is assigned a range of section IDs.

However, as some of the Elves compare their section assignments with each other, they've noticed that many of the assignments overlap. To try to quickly find overlaps and reduce duplicated effort, the Elves pair up and make a big list of the section assignments for each pair (your puzzle input).

For example, consider the following list of section assignment pairs:

2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
For the first few pairs, this list means:

Within the first pair of Elves, the first Elf was assigned sections 2-4 (sections 2, 3, and 4), while the second Elf was assigned sections 6-8 (sections 6, 7, 8).
The Elves in the second pair were each assigned two sections.
The Elves in the third pair were each assigned three sections: one got sections 5, 6, and 7, while the other also got 7, plus 8 and 9.
This example list uses single-digit section IDs to make it easier to draw; your actual list might contain larger numbers. Visually, these pairs of section assignments look like this:

.234.....  2-4
.....678.  6-8

.23......  2-3
...45....  4-5

....567..  5-7
......789  7-9

.2345678.  2-8
..34567..  3-7

.....6...  6-6
...456...  4-6

.23456...  2-6
...45678.  4-8
Some of the pairs have noticed that one of their assignments fully contains the other. For example, 2-8 fully contains 3-7, and 6-6 is fully contained by 4-6. In pairs where one assignment fully contains the other, one Elf in the pair would be exclusively cleaning sections their partner will already be cleaning, so these seem like the most in need of reconsideration. In this example, there are 2 such pairs.

In how many assignment pairs does one range fully contain the other?
"""

from utils.solver import ProblemSolver


class Day04Solver(ProblemSolver):
    def __init__(self):
        super(Day04Solver, self).__init__(4)

        self.testDataAnswersPartOne = [2]
        self.testDataAnswersPartTwo = [4]

    def ProcessInput(self, data=None):
        """
        
        :param data:
        :returns: processed data for today's challenge
        """
        if not data:
            data = self.rawData

        processed = []
        for line in data.splitlines(keepends=False):
            # set up a list for our pairs to land in
            pair = []
            # loop over the pairs
            for assignment in line.split(','):
                # get the start and end of the assignment
                start, end = assignment.split('-')
                # if start is the same as end, just add that to the pairs as a set
                if start == end:
                    pair.append({int(start)})
                # otherwise, add a set from start to end (inclusive)
                else:
                    pair.append(set(range(int(start), int(end) + 1)))

            processed.append(pair)

        return processed

    def SolvePartOne(self, data=None):
        """
        
        :param data:
        :returns: The solution to today's challenge
        """
        if not data:
            data = self.processed

        count = 0
        for a, b in data:
            # if a is a subset of b, that means b wholly contains a, and we can increment the count
            if a.issubset(b):
                count += 1
            # otherwise, if a is a superset of b, that means b is wholly contained by a,
            # and we can increment the count
            elif a.issuperset(b):
                count += 1

        return count

    def SolvePartTwo(self, data=None):
        """
        
        :param data:
        :returns: The solution to part two of today's challenge
        """
        if not data:
            data = self.processed

        count = 0
        # loop over all the data
        for a, b in data:
            # if there's any overlap between a and b, increment the count
            if a.intersection(b):
                count += 1

        return count


if __name__ == '__main__':
    day04 = Day04Solver()
    day04.Run()
