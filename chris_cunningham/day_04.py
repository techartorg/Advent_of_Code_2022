from pathlib import Path

inputs = Path(__file__.replace(".py", ".input")).read_text().splitlines()


def parse_line(input_str: str) -> (range, range):
    return tuple(range(int(rs[0]), int(rs[1]) + 1) for i in input_str.split(',') if (rs := i.split('-')))


data = [parse_line(i) for i in inputs]

part_one = sum(all(i in b for i in a) or all(i in a for i in b) for a, b in data)
print(f"Part One: {part_one}")

part_two = sum(any(i in b for i in a) for a, b in data)
print(f"Part Two: {part_two}")
