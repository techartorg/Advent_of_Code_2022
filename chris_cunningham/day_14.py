from pathlib import Path
from enum import Enum
from collections import defaultdict
from utils import window
from typing import Iterator
from utils import sign

inputs = Path(__file__.replace(".py", ".input")).read_text().splitlines()

Pt = tuple[int, int]


class TileState(Enum):
    Air = ' '
    Rock = '#'
    Sand = 'o'
    Source = '+'


class Grid(object):
    falling_dirs = ((0, 1), (-1, 1), (1, 1))

    def __init__(self, lines: list[str]):
        self.data: defaultdict[Pt, TileState] = defaultdict(lambda: TileState.Air)

        for line in lines:
            points = (tuple(int(j) for j in i.strip().split(',')) for i in line.split("->"))

            for prev, current in window(points, 2):
                for x in line_iter(prev[0], current[0]):
                    for y in line_iter(prev[1], current[1]):
                        self.set((x, y), TileState.Rock)

        self.min = (min(i[0] for i in self.data.keys()), min(i[1] for i in self.data.keys()))
        self.max = (max(i[0] + 1 for i in self.data.keys()), max(i[1] for i in self.data.keys()))

    def set(self, point: Pt, state: TileState):
        self.data[point] = state

    def get(self, point: Pt) -> TileState:
        return self.data[point]

    def next_spot(self, point: Pt) -> Pt | None:
        x, y = point

        for step_x, step_y in self.falling_dirs:
            new_point = (x + step_x, y + step_y)

            if new_point[1] == self.max[1] + 2:
                return None

            if self.get(new_point) == TileState.Air and new_point[0]:
                return new_point

        return None

    def __str__(self) -> str:
        self.min = (min(i[0] for i in self.data.keys()), min(i[1] for i in self.data.keys()))
        self.max = (max(i[0] for i in self.data.keys()), max(i[1] for i in self.data.keys()))

        lines = [f"Min: {self.min}, Max: {self.max}, Len: {len(self.data)}", f'┌{"".join("─" for _ in range(self.min[0], self.max[0]))}┐']

        for y in range(self.min[1], self.max[1]):
            lines.append(f'│{"".join(self.data[(x, y)].value for x in range(self.min[0], self.max[0]))}│')

        lines.append(f'└{"".join("─" for _ in range(self.min[0], self.max[0]))}┘')

        return "\n".join(lines)


def line_iter(start: int, end: int) -> Iterator[int]:
    direction = sign(end - start)
    current = start

    while current != end:
        yield current
        current += direction

    yield current


def add_sand(grid: Grid, start: Pt) -> Pt | None:
    current_point = start

    while point := grid.next_spot(current_point):
        current_point = point

    return current_point


def solve() -> Iterator[int]:
    source_pt = (500, 0)
    grid = Grid(inputs)

    count = 0
    while (point := add_sand(grid, source_pt)) and point[1] <= grid.max[1]:
        grid.set(point, TileState.Sand)
        count += 1

    yield count

    while point := add_sand(grid, source_pt):
        grid.set(point, TileState.Sand)
        count += 1

        if point == source_pt:
            break

    yield count


results = solve()
print(f"Part One: {next(results)}")
print(f"Part Two: {next(results)}")
