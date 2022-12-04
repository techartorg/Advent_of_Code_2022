#! python3.11
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

Your puzzle answer was 7446.

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

Your puzzle answer was 2646.

Both parts of this puzzle are complete! They provide two gold stars: **
"""

import difflib

test_data = [ 'vJrwpWtwJgWrhcsFMMfFFhFp',
			  'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL',
			  'PmmdzqPrVvPwwTWBwg',
			  'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn',
			  'ttgJtRGJQctTZtZT',
			  'CrZsJsPPZsGzwwsLwLmpwMDw'
			]


def find_common_item(raw_data):
	compartment_1, compartment_2 = raw_data[:len(raw_data)//2], raw_data[len(raw_data)//2:]
	common_item = list(set(compartment_1).intersection(compartment_2))[0]

	return common_item

def find_common_badge(rucksacks):
	common_item = ''

	result_1 = set(rucksacks[0]).intersection(rucksacks[1])
	common_item = list(result_1.intersection(set(rucksacks[2])))[0]

	return common_item



def get_priority(item):
	priority = 0

	if item.isupper():
		priority = ord(item) - ord('@') + 26

	else:
		priority = ord(item) - ord('`')

	return priority


def main(raw_data):
	priority_sum = 0
	output_string = ''

	for datum in raw_data:
		item = find_common_item(datum)
		priority = get_priority(item)
		priority_sum += priority

		output_string += f'{priority} '

	print(f'The sum of the priorities of: {output_string}\n\tis {priority_sum}.\n')

	# Regroup the list of rucksacks into groups of 3
	groups = [raw_data[i:i+3] for i in range(0, len(raw_data), 3)]
	priority_sum = 0
	output_string = ''

	for group in groups:
		item = find_common_badge(group)
		priority = get_priority(item)
		priority_sum += priority

		output_string += f'{priority} '

	print(f'The sum of the priorities of: {output_string}\n\tis {priority_sum}.')


if __name__ == "__main__":
	input = r"D:\Projects\Advent_of_Code\2022\day_03_input.txt"
	raw_data = []

	with open(input, "r") as input_file:
		raw_data = [ x for x in input_file.read( ).split( ) ]

	# main(test_data)
	main(raw_data)