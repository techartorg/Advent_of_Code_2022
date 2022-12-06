from pathlib import Path
from utils import window


inputs = Path(__file__.replace(".py", ".input")).read_text()


def solve(data: str, length: int) -> int:
    return next(i + length for i, item in enumerate(window(data, length)) if len(set(item)) == length)


print(f"Part One: {solve(inputs, 4)}")
print(f"Part Two: {solve(inputs, 14)}")
