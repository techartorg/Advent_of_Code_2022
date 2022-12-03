from pathlib import WindowsPath

input_path = WindowsPath(__file__).parent.parent / 'inputs/day01.txt'


def cal_totals():
    return [sum((int(cal) for cal in (line.split('\n')))) for line in input_path.read_text().split('\n\n')]


def part_01():
    return max(cal_totals())


def part_02():
    return sum(sorted(cal_totals())[-3:])


print(cal_totals())
print('Part 01 answer: {}'.format(part_01()))
print('Part 02 answer: {}'.format(part_02()))
