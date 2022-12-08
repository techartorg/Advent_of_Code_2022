from pathlib import Path

inputs = Path(__file__.replace(".py", ".input")).read_text().splitlines()
_test = """30373
25512
65332
33549
35390""".splitlines()

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

    right = 0
    for c, i in enumerate(range(x + 1, cols)):
        right = c + 1
        if data[y][i] >= height:
            break

    left = 0
    for c, i in enumerate(range(x - 1, -1, -1)):
        left = c + 1
        if data[y][i] >= height:
            break

    down = 0
    for c, i in enumerate(range(y + 1, rows)):
        down = c + 1
        if data[i][x] >= height:
            break

    up = 0
    for c, i in enumerate(range(y - 1, -1, -1)):
        up = c + 1
        if data[i][x] >= height:
            break

    return right * left * down * up


grid = [[int(col) for col in row] for row in inputs]

visible_trees = find_visible(grid)
print(f"Part One: {len(visible_trees)}")

scenic_scores = [calc_scenic_score(grid, i) for i in visible_trees]
print(f"Part Two: {max(scenic_scores)}")
