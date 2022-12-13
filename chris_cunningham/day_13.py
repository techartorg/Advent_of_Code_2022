import json
from functools import cmp_to_key
from pathlib import Path
from utils import sign

inputs = Path(__file__.replace(".py", ".input")).read_text().split("\n\n")


def compare(lhs: int | list, rhs: int | list) -> int:
    match lhs, rhs:
        case int(), int():
            return sign(lhs - rhs)

        case int(), list():
            return compare([lhs], rhs)

        case list(), int():
            return compare(lhs, [rhs])

        case list(), list():
            if len(lhs) == len(rhs) == 0:
                return 0

            if len(lhs) == 0:
                return -1

            if len(rhs) == 0:
                return 1

            for l, r in zip(lhs, rhs):
                if (result := compare(l, r)) != 0:
                    return result

            return sign(len(lhs) - len(rhs))


def part_one() -> int:
    result = 0

    for i, section in enumerate(inputs, start=1):
        pair = [json.loads(i) for i in section.splitlines()]
        result += i if compare(*pair) == -1 else 0

    return result


def part_two() -> int:
    added_data = [[[2]], [[6]]]
    data = [*added_data]

    for section in inputs:
        data.extend([json.loads(i) for i in section.splitlines()])

    data.sort(key=cmp_to_key(compare))
    result = (i for i, v in enumerate(data, start=1) if v in added_data)

    return next(result) * next(result)


print(f"Part One: {part_one()}")
print(f"Part Two: {part_two()}")
