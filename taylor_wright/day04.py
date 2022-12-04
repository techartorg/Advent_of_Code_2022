from pathlib import WindowsPath

input_path = WindowsPath(__file__).parent.parent / 'inputs/day04.txt'


def part_01(first_part: bool) -> int:
    overlaps = 0
    pairs = [(line.split(',')) for line in input_path.read_text().splitlines()]
    ranges = [[(int(ind[0]), int(ind[1])) for ind in [pair[0].split('-'), pair[1].split('-')]] for pair in pairs]
    for r in ranges:
        first_range = set(range(r[0][0], r[0][1] + 1))
        second_range = set(range(r[1][0], r[1][1] + 1))
        if first_part:
            if first_range.issubset(second_range) or second_range.issubset(first_range):
                overlaps += 1
        else:
            if not first_range.isdisjoint(second_range):
                overlaps += 1
    return overlaps


print('Part 01 answer: {}'.format(part_01(True)))
print('Part 02 answer: {}'.format(part_01(False)))
