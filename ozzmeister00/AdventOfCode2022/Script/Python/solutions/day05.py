"""
Python day05

--- Day 5: Supply Stacks ---
The expedition can depart as soon as the final supplies have been unloaded from the ships. Supplies are stored in stacks of marked crates, but because the needed supplies are buried under many other crates, the crates need to be rearranged.

The ship has a giant cargo crane capable of moving crates between stacks. To ensure none of the crates get crushed or fall over, the crane operator will rearrange them in a series of carefully-planned steps. After the crates are rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate procedure, but they forgot to ask her which crate will end up where, and they want to be ready to unload them as soon as possible so they can embark.

They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input). For example:

    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
In this example, there are three stacks of crates. Stack 1 contains two crates: crate Z is on the bottom, and crate N is on top. Stack 2 contains three crates; from bottom to top, they are crates M, C, and D. Finally, stack 3 contains a single crate, P.

Then, the rearrangement procedure is given. In each step of the procedure, a quantity of crates is moved from one stack to a different stack. In the first step of the above rearrangement procedure, one crate is moved from stack 2 to stack 1, resulting in this configuration:

[D]
[N] [C]
[Z] [M] [P]
 1   2   3
In the second step, three crates are moved from stack 1 to stack 3. Crates are moved one at a time, so the first crate to be moved (D) ends up below the second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3
Then, both crates are moved from stack 2 to stack 1. Again, because crates are moved one at a time, crate C ends up below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3
Finally, one crate is moved from stack 1 to stack 2:

        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3
The Elves just need to know which crate will end up on top of each stack; in this example, the top crates are C in stack 1, M in stack 2, and Z in stack 3, so you should combine these together and give the Elves the message CMZ.

After the rearrangement procedure completes, what crate ends up on top of each stack?
"""
import collections

from utils.solver import ProblemSolver


class CargoBay(list):
    def __init__(self, size):
        super(CargoBay, self).__init__()

        # initialize the cargo bay with empty lists for each stack
        for i in range(size):
            self.append([])

    def moveSingle(self, quantity, source, destination):
        """
        Move a set number of boxes from one cargo stack to another
        :param int quantity: how many items to move
        :param int source: the stack from which to move items
        :param int destination: the stack to which to move items
        """
        for i in range(0, quantity):
            self[destination].append(self[source].pop())

    def moveBatch(self, quantity, source, destination):
        """
        Move a group of cargoes from source to destination while maintaining their order

        :param int quantity:
        :param int source:
        :param int destination:
        """
        # pop the quantity we want off the source stack and reverse that list
        packet = [self[source].pop() for i in range(quantity)][::-1]
        # then add the whole packet to the destination stack
        self[destination] += packet

    def add(self, cargo, destination):
        """
        Add a cargo item to the input stack
        :param str cargo: the cargo ID to add
        :param destination the stack to which to add the item:
        """
        self[destination].append(cargo)

    def tops(self):
        """
        :return list[str]: all the values at the tops of each stack
        """
        out = ''
        for i in self:
            if i:
                out += i[-1]
            else:
                out += ' '
        return out

    def __str__(self):
        out = ''
        for i, line in enumerate(self):
            out += f"{i} " + ' '.join(line) + '\n'
        return out


class Day05Solver(ProblemSolver):
    def __init__(self):
        super(Day05Solver, self).__init__(5)

        self.testDataAnswersPartOne = ['CMZ']
        self.testDataAnswersPartTwo = ['MCD']

    def ProcessInput(self, data=None):
        """
        :param str data:
        :returns [CargoStack, [(int, int, int)]: the cargo stack from the input data, and a list of instructions in tuples
        """
        if not data:
            data = self.rawData

        lines = data.splitlines(keepends=False)

        # first, find the dividing line between the stacks and the move set
        index = -1
        i = 0
        while index < 0:
            if not lines[i].strip():
                index = i
            i += 1

        stackLines = lines[:index]

        # storing the index at which a given stack ID appears
        # luckily input data and test data don't exceed single-digit stack IDs
        stackIndexes = {stackLines[-1].index(i): int(i) - 1 for i in stackLines[-1] if i.isdigit()}

        # initialize the cargo bay
        size = max(stackIndexes.values()) + 1
        cargoBay = CargoBay(size)

        # then we can parse each line and match the index of an alpha character to its stack
        # do it from the bottom up so the stacks end up in the correct order
        for line in stackLines[-2::-1]:
            # loop over all the characters in the line
            for i, char in enumerate(line):
                # if the character is a letter
                if char.isalpha():
                    # add it to the cargo bay by looking up the correct
                    # stack ID for the current character's index in the str
                    cargoBay.add(char, stackIndexes[i])

        # translate the move set
        moveSetLines = lines[index+1:]
        moveSet = []
        for line in moveSetLines:
            tokens = line.split(' ')
            # we know the instructions are always of the form "move X from Y to Z" so we can
            # just grab those quantity, to, and from values directly
            # and offset the source and dest by one since the input data is 1-based
            moveSet.append((int(tokens[1]), int(tokens[3])-1, int(tokens[5])-1))

        processed = [cargoBay, moveSet]

        return processed

    def SolvePartOne(self, data=None):
        """
        
        :param data:
        :returns: The solution to today's challenge
        """
        if not data:
            data = self.processed

        cargoBay, moveSet = data
        for quantity, source, destination in moveSet:
            cargoBay.moveSingle(quantity, source, destination)

        return ''.join(cargoBay.tops())

    def SolvePartTwo(self, data=None):
        """
        
        :param data:
        :returns: The solution to part two of today's challenge
        """
        if not data:
            data = self.processed

        cargoBay, moveSet = data
        for quantity, source, destination in moveSet:
            try:
                cargoBay.moveBatch(quantity, source, destination)
            except Exception as e:
                print(quantity, source, destination, '\n', cargoBay)
                print(e)
                break

        return ''.join(cargoBay.tops())

if __name__ == '__main__':
    day05 = Day05Solver()
    day05.Run()
