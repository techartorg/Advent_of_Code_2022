test_input = r'''2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
'''

puzzle_input = open(__file__.replace('.py', '_input.txt')).read()

import re
ranges = re.compile(r'\d+')

def part_one(input_):
    count = 0
    sections = input_.splitlines()
    for s in sections:
        m = [int(x) for x in ranges.findall(s)]
        min1, max1, min2, max2 = m[0], m[1], m[2], m[3]
        if min2 >= min1 and max2 <= max1:
            count += 1
            continue
        if min1 >= min2 and max1 <= max2:
            count += 1
            continue
    return count

def part_two(input_):
    count = 0
    sections = input_.splitlines()
    for s in sections:
        m = [int(x) for x in ranges.findall(s)]
        min1, max1, min2, max2 = m[0], m[1], m[2], m[3]
        if min2 <= max1 and max2 >= min1:
            count += 1
            continue
        if min1 <= max2 and max1 >= min2:
            count += 1
            continue
    return count

assert (part_one(test_input)) == 2
assert (part_two(test_input)) == 4

print(f'Part One: {part_one(puzzle_input)}')
print(f'Part Two: {part_two(puzzle_input)}')
