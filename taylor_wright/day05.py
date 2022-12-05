from pathlib import WindowsPath
from collections import deque

input_path = WindowsPath(__file__).parent.parent / 'inputs/day05.txt'


def make_stack_lists():
    crate_deques = [deque() for i in range(9)]
    crates = list(reversed([list(crate) for crate in input_path.read_text().split('\n\n')[0].splitlines()]))
    crate_inds = [ind for ind, char in enumerate(crates[0]) if char.isdigit()]
    for ind, index in enumerate(crate_inds):
        for crate in crates[1:]:
            try:
                if crate[index].isalpha():
                    crate_deques[ind].append(crate[index])
            except IndexError:
                continue
    return crate_deques


def make_instructions():
    lines = [[int(char) for char in line.split(' ') if char.isdigit()] for line in input_path.read_text().split('\n\n')[1].splitlines()]
    return lines


def solve(part01: bool):
    stacks = make_stack_lists()
    instructions = make_instructions()
    for instruction in instructions:
        num_to_move = instruction[0]
        move_from = instruction[1]-1
        move_to = instruction[2]-1
        if part01:
            for i in range(num_to_move):
                crate_pulled = stacks[move_from].pop()
                stacks[move_to].append(crate_pulled)
        else:
            pulled_crates = []
            for i in range(num_to_move):
                pulled_crates.append(stacks[move_from].pop())
            stacks[move_to].extend(reversed(pulled_crates))
    return ''.join([stack[-1] for stack in stacks])


print('Part 01 answer: {}'.format(solve(True)))
print('Part 02 answer: {}'.format(solve(False)))
