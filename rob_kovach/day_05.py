from collections import defaultdict
import re

test_input = '''    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''

puzzle_input = open(__file__.replace('.py', '_input.txt')).read()
moves = re.compile(r'\d+')

def part_one(input_, flip=True):
    stacks = defaultdict(list)
    lines = input_.splitlines()
    for l in lines:
        if '[' not in l:
            continue
        indices = [x for x, v in enumerate(l) if v == '[']
        for i in indices:
            stacks[(i//4+1)].append(l[i+1])

    for l in lines:
        if not l.startswith('move'):
            continue

        num, c1, c2 = [int(x) for x in moves.findall(l)]
        crates = stacks[c1][:num]

        if flip:
            crates.reverse()
        
        stacks[c1] = stacks[c1][num:]
        stacks[c2] = crates + stacks[c2]
    
    top = [stacks[x][0] for x in sorted(stacks.keys())]
    return "".join(top)

print(f'Part One: {part_one(puzzle_input)}.')
print(f'Part Two: {part_one(puzzle_input, flip=False)}.')