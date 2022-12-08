from pathlib import Path
from typing import Callable

inputs = Path(__file__.replace(".py", ".input")).read_text().splitlines()

Grid = list[list[int]]
Pt = tuple[int, int]


def find_visible(data: Grid) -> set[Pt]:
    cols = len(data[0])
    rows = len(data)
    seen: set[tuple[int, int]] = set()

    for y in range(rows):
        for it in [range(cols), reversed(range(cols))]:
            highest_seen = -1

            for x in it:
                if data[y][x] <= highest_seen:
                    continue

                highest_seen = data[y][x]
                seen.add((x, y))

    for x in range(cols):
        for it in [range(rows), reversed(range(rows))]:
            highest_seen = -1

            for y in it:
                if data[y][x] <= highest_seen:
                    continue

                highest_seen = data[y][x]
                seen.add((x, y))

    return seen


def calc_scenic_score(data: Grid, point: Pt) -> int:
    x, y = point
    height = data[y][x]
    rows = len(data)
    cols = len(data[0])

    def find(r: range, get_height: Callable[[int], int]) -> int:
        v = 0
        for c, i in enumerate(r):
            v = c + 1
            if get_height(i) >= height:
                break
        return v

    right = find(range(x + 1, cols), lambda it: data[y][it])
    left = find(range(x - 1, -1, -1), lambda it: data[y][it])
    down = find(range(y + 1, rows), lambda it: data[it][x])
    up = find(range(y - 1, -1, -1), lambda it: data[it][x])

    return right * left * down * up


grid = [[int(col) for col in row] for row in inputs]

visible_trees = find_visible(grid)
print(f"Part One: {len(visible_trees)}")

scenic_scores = [calc_scenic_score(grid, i) for i in visible_trees]
print(f"Part Two: {max(scenic_scores)}")
