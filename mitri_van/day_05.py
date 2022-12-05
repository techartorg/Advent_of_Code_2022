#! python3.11
"""
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

Your puzzle answer was FZCMJCRHZ.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
As you watch the crane operator expertly rearrange the crates, you notice the process isn't following your prediction.

Some mud was covering the writing on the side of the crane, and you quickly wipe it away. The crane isn't a CrateMover 9000 - it's a CrateMover 9001.

The CrateMover 9001 is notable for many new and exciting features: air conditioning, leather seats, an extra cup holder, and the ability to pick up and move multiple crates at once.

Again considering the example above, the crates begin in the same configuration:

    [D]
[N] [C]
[Z] [M] [P]
 1   2   3
Moving a single crate from stack 2 to stack 1 behaves the same as before:

[D]
[N] [C]
[Z] [M] [P]
 1   2   3
However, the action of moving three crates from stack 1 to stack 3 means that those three moved crates stay in the same order, resulting in this new configuration:

        [D]
        [N]
    [C] [Z]
    [M] [P]
 1   2   3
Next, as both crates are moved from stack 2 to stack 1, they retain their order as well:

        [D]
        [N]
[C]     [Z]
[M]     [P]
 1   2   3
Finally, a single crate is still moved from stack 1 to stack 2, but now it's crate C that gets moved:

        [D]
        [N]
        [Z]
[M] [C] [P]
 1   2   3
In this example, the CrateMover 9001 has put the crates in a totally different order: MCD.

Before the rearrangement process finishes, update your simulation so that the Elves know where they should stand to be ready
to unload the final supplies. After the rearrangement procedure completes, what crate ends up on top of each stack?

Your puzzle answer was JSDHQMZGF.

Both parts of this puzzle are complete! They provide two gold stars: **

"""
from collections import deque

test_data = '    [D]\n[N] [C]\n[Z] [M] [P]\n 1   2   3\n\nmove 1 from 2 to 1\nmove 3 from 1 to 3\nmove 2 from 2 to 1\nmove 1 from 1 to 2\n'


def parse_stack_data(data):
	i = 0
	string_len = len(data)

	temp_data = deque(data)
	while temp_data[0] != '#'and i < string_len:
		# print(f"{i}: {''.join(temp_data)}")
		if temp_data[0] == ' ':
			for idx in range(0,3):
				temp_data[idx] = '#'
			temp_data.rotate(-4)
		else:
			temp_data.rotate(-4)
		i += 4

	temp_data.rotate(1)
	return ''.join(temp_data)


def parse_data(raw_data):
	data = raw_data.replace('move ', '').replace('from ', '').replace('to ','')
	stack_map, move_list = [x.rstrip().split('\n') for x in data.split('\n\n')]

	stack_map.reverse()

	# Stacks
	for i in range(1, len(stack_map)):
		stack_map[i] = parse_stack_data(stack_map[i])

	# Moves
	move_list = [list(map(int, x.split())) for x in move_list]


	return stack_map, move_list


def initialize_stacks(data):
	stacks = []

	num_stacks = len(data.pop(0).split())
	crates = [x.replace('[','').replace(']','').split() for x in data]

	# Set up the crates
	for i in range(0, num_stacks):
		stacks.append([])

	# Fill the crates
	while crates:
		crates_to_be_sorted = crates.pop(0)

		for i in range(0, num_stacks):
			if crates_to_be_sorted:
				sorted_crate = crates_to_be_sorted.pop(0)
				if sorted_crate != '###':
					stacks[i].append(sorted_crate)
					# print(f'Put crate {sorted_crate} in crate {i+1}')

	return stacks


def crate_mover_9000(stacks, moves):

	for move in moves:
		move_num = move[0]
		start = move[1] - 1
		end = move[2] - 1

		for i in range(0, move_num):
			crate = stacks[start].pop()
			stacks[end].append(crate)

	return stacks


def crate_mover_9001(stacks, moves):
	for move in moves:
		crate_stack = []

		move_num = move[0]
		start = move[1] - 1
		end = move[2] - 1

		for i in range(0, move_num):
			crate = stacks[start].pop()
			crate_stack.append(crate)

		crate_stack.reverse()
		stacks[end].extend(crate_stack)

	return stacks


def main(raw_data):
	crate_stacks = []
	move_list = []
	stack_map = []

	output_string = ''

	stack_map, move_list = parse_data(raw_data)
	crate_stacks = initialize_stacks(stack_map)
	crate_stacks = crate_mover_9000(crate_stacks, move_list)

	for crate_stack in crate_stacks:
		output_string += str(crate_stack[-1])

	print(f'[CrateMover 9000] The top crates for each stack are: {output_string}\n')

	crate_stacks = []
	output_string = ''

	stack_map, move_list = parse_data(raw_data)
	crate_stacks = initialize_stacks(stack_map)
	crate_stacks = crate_mover_9001(crate_stacks, move_list)

	for crate_stack in crate_stacks:
		output_string += str(crate_stack[-1])

	print(f'[CrateMover 9001] The top crates for each stack are: {output_string}\n')



if __name__ == "__main__":
	input = r"D:\Projects\Advent_of_Code\2022\day_05_input.txt"
	raw_data = []

	with open(input, "r") as input_file:
		raw_data = input_file.read()

	# main(test_data)
	main(raw_data)