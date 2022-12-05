from pathlib import Path
import copy
import re

ins_re = re.compile(r"move (\d+) from (\d+) to (\d+)")

inputs = Path(__file__.replace(".py", ".input")).read_text()

stack_lines, instructions = inputs.split("\n\n", maxsplit=1)
stack_lines = stack_lines.splitlines()
instructions = [(grp[0], grp[1]-1, grp[2]-1) for i in instructions.splitlines() if (grp := [int(g) for g in ins_re.match(i).groups()])]

stacks_char_len = len(stack_lines[0])
stacks = [[] for i in range((stacks_char_len + 1) // 4)]

for line in stack_lines[:-1]:
    for c in range(1, stacks_char_len, 4):
        if line[c].strip():
            stacks[c // 4].append(line[c])

stacks: list[list[str]] = [[*reversed(i)] for i in stacks]


def solve(input_stacks: list[list[str]], part_two: bool = False) -> str:
    stacks = copy.deepcopy(input_stacks)

    for count, start, end in instructions:
        items = stacks[start][-count:]
        stacks[start] = stacks[start][:-count]
        stacks[end].extend(items if part_two else reversed(items))

    return "".join(i.pop() for i in stacks)


print(f"Part One: {solve(stacks)}")
print(f"Part One: {solve(stacks, part_two=True)}")
