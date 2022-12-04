from pathlib import WindowsPath

input_path = WindowsPath(__file__).parent.parent / 'inputs/day03.txt'


def separate_compartments(rucksack: str) -> list[set]:
    return [set(rucksack[:int(len(rucksack) / 2)]), set(rucksack[int(len(rucksack) / 2):])]


def ord_for_letter(letter: str) -> int:
    return (ord(letter) - 96) if letter.islower() else (ord(letter) - 38)


def part_01() -> int:
    rucksacks = [separate_compartments(line) for line in input_path.read_text().splitlines()]
    intersections = [rucksack[0].intersection(rucksack[1]).pop() for rucksack in rucksacks]
    return sum([ord_for_letter(intersection) for intersection in intersections])


def part_02() -> int:
    rucksacks = [line for line in input_path.read_text().splitlines()]
    grps = [[set(grp) for grp in rucksacks[i:i+3]] for i in range(0, len(rucksacks), 3)]
    badges = sum([ord_for_letter(set.intersection(*grp).pop()) for grp in grps])
    return badges


print('Part 01 answer: {}'.format(part_01()))
print('Part 02 answer: {}'.format(part_02()))
