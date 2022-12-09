from pathlib import Path
from math import prod
from typing import Iterator

inputs = Path(__file__.replace(".py", ".input")).read_text().splitlines()

Point = tuple[int, int]
Grid = dict[Point, int]
directions = ((-1, 0), (1, 0), (0, 1), (0, -1))

grid = {(x, y): height for y, row in enumerate(inputs) for x, height in enumerate(row)}


def ray(start: Point, direction: Point) -> Iterator[Point]:
    x, y = start
    step_x, step_y = direction
    while (x := x + step_x, y := y + step_y) in grid:
        yield x, y


def is_visible(start: Point) -> bool:
    return any(all(grid[p] < grid[start] for p in ray(start, d)) for d in directions)


def view(start: Point, direction: Point) -> int:
    v = 0
    for i, p in enumerate(ray(start, direction)):
        v = i + 1
        if grid[p] >= grid[start]:
            break
    return v


def score(point: Point) -> int:
    return prod(view(point, d) for d in directions)


visible_trees = [p for p in grid if is_visible(p)]
print(f"Part One: {len(visible_trees)}")
print(f"Part Two: {max(score(p) for p in visible_trees)}")
