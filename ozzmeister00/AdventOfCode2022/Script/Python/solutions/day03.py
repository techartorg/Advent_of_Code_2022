"""
--- Day 3: Rucksack Reorganization ---
One Elf has the important job of loading all of the rucksacks with supplies for the jungle journey. Unfortunately, that Elf didn't quite follow the packing instructions, and so a few items now need to be rearranged.

Each rucksack has two large compartments. All items of a given type are meant to go into exactly one of the two compartments. The Elf that did the packing failed to follow this rule for exactly one item type per rucksack.

The Elves have made a list of all of the items currently in each rucksack (your puzzle input), but they need your help finding the errors. Every item type is identified by a single lowercase or uppercase letter (that is, a and A refer to different types of items).

The list of items for each rucksack is given as characters all on a single line. A given rucksack always has the same number of items in each of its two compartments, so the first half of the characters represent items in the first compartment, while the second half of the characters represent items in the second compartment.

For example, suppose you have the following list of contents from six rucksacks:

vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
The first rucksack contains the items vJrwpWtwJgWrhcsFMMfFFhFp, which means its first compartment contains the items vJrwpWtwJgWr, while the second compartment contains the items hcsFMMfFFhFp. The only item type that appears in both compartments is lowercase p.
The second rucksack's compartments contain jqHRNqRjqzjGDLGL and rsFMfFZSrLrFZsSL. The only item type that appears in both compartments is uppercase L.
The third rucksack's compartments contain PmmdzqPrV and vPwwTWBwg; the only common item type is uppercase P.
The fourth rucksack's compartments only share item type v.
The fifth rucksack's compartments only share item type t.
The sixth rucksack's compartments only share item type s.
To help prioritize item rearrangement, every item type can be converted to a priority:

Lowercase item types a through z have priorities 1 through 26.
Uppercase item types A through Z have priorities 27 through 52.
In the above example, the priority of the item type that appears in both compartments of each rucksack is 16 (p), 38 (L), 42 (P), 22 (v), 20 (t), and 19 (s); the sum of these is 157.

Find the item type that appears in both compartments of each rucksack. What is the sum of the priorities of those item types?

--- Part Two ---
As you finish identifying the misplaced items, the Elves come to you with another issue.

For safety, the Elves are divided into groups of three. Every Elf carries a badge that identifies their group. For efficiency, within each group of three Elves, the badge is the only item type carried by all three Elves. That is, if a group's badge is item type B, then all three Elves will have item type B somewhere in their rucksack, and at most two of the Elves will be carrying any other item type.

The problem is that someone forgot to put this year's updated authenticity sticker on the badges. All of the badges need to be pulled out of the rucksacks so the new authenticity stickers can be attached.

Additionally, nobody wrote down which item type corresponds to each group's badges. The only way to tell which item type is the right one is by finding the one item type that is common between all three Elves in each group.

Every set of three lines in your list corresponds to a single group, but each group can have a different badge item type. So, in the above example, the first group's rucksacks are the first three lines:

vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
And the second group's rucksacks are the next three lines:

wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
In the first group, the only item type that appears in all three rucksacks is lowercase r; this must be their badges. In the second group, their badge item type must be Z.

Priorities for these items must still be found to organize the sticker attachment efforts: here, they are 18 (r) for the first group and 52 (Z) for the second group. The sum of these is 70.

Find the item type that corresponds to the badges of each three-Elf group. What is the sum of the priorities of those item types?
"""
import string

from utils.solver import ProblemSolver
import utils.math

# just go ahead and convert upper and lowercase letters to strings for simplicity
UPPER_CASE = set(string.ascii_uppercase)
lower_case = set(string.ascii_lowercase)

# and also pre-create the list of priority scoring so we don't have to do a bunch of
# string lookups later on and can instead just hash it out... so to speak
PRIORITIES = {i: string.ascii_letters.index(i) + 1 for i in string.ascii_letters}


class Day03Solver(ProblemSolver):
    def __init__(self):
        super(Day03Solver, self).__init__(3)

        self.testDataAnswersPartOne = [157]
        self.testDataAnswersPartTwo = [70]

    def ProcessInput(self, data=None):
        """
        Takes the input string and turns it into a list of tuples representing the contents
        of each half of the rucksack

        :param string data:
        :returns list[int]: processed data for today's challenge
        """
        if not data:
            data = self.rawData

        processed = []
        for line in data.split('\n'):
            half = int(len(line.strip()) / 2)
            # since both parts ended up needing sets, just go ahead and
            # convert them to sets in input processing instead of having each day part do that work
            processed.append((set(line[:half]), set(line[half:])))

        return processed

    def SolvePartOne(self, data=None):
        """
        :param list[(set, set)] data: list of rucksack halves

        :returns int: The solution to today's challenge
        """
        if not data:
            data = self.processed

        priorityScore = 0

        for left, right in data:
            intersection = left.intersection(right)
            if len(intersection) > 1:
                raise ValueError(f"There are more than one common items ({intersection}) between each half of the rucksack {left}/{right}")

            priorityScore += PRIORITIES[intersection.pop()]

        return priorityScore

    def ProcessGroup(self, inElves):
        """
        Figure out the common item between all three elves in an input group and return their priority based on their
        badge identifier
        :param list[(set[str], set[str])] inElves:
        :return int:
        """
        sets = [a.union(b) for a, b in inElves]
        common = sets[0]
        for i in range(1, len(sets)):
            common.intersection_update(sets[i])

        if len(common) > 1:
            raise ValueError(f"Multiple common items {common} for elf grouping {inElves}")

        return PRIORITIES[common.pop()]

    def SolvePartTwo(self, data=None):
        """
        :param list data: list of sets of rucksack halves

        :returns int: The priority score for each elf 
        """
        if not data:
            data = self.processed

        priorityScore = 0

        for i in range(0, len(data), 3):
            priorityScore += self.ProcessGroup(data[i:i+3])

        return priorityScore


if __name__ == '__main__':
    day03 = Day03Solver()
    day03.Run()
