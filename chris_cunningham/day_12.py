from pathlib import Path
from collections import deque
from typing import Iterator

inputs = Path(__file__.replace(".py", ".input")).read_text()
Pt = tuple[int, int]


class Grid(object):
    directions = ((-1, 0), (1, 0), (0, 1), (0, -1))

    def __init__(self, s: str):
        self.grid: dict[Pt, int] = {}
        self.start = (0, 0)
        self.end = (0, 0)

        x, y = 0, 0
        for y, row in enumerate(s.splitlines()):
            for x, h in enumerate(row):
                self.grid[(x, y)] = self.parse_height(h)
                if h == 'S':
                    self.start = (x, y)
                if h == 'E':
                    self.end = (x, y)

        self.size = (x + 1, y + 1)

    def __repr__(self):
        return f"Grid(size = {self.size})"

    @staticmethod
    def parse_height(s: str) -> int:
        zero = ord('a')
        match s:
            case 'S': return 0
            case 'E': return ord('z') - zero
            case other: return ord(other) - zero

    def get(self, value: Pt) -> int:
        return self.grid[value]

    def get_neighbours(self, value: Pt) -> Iterator[Pt]:
        x, y = value
        sx, sy = self.size
        height = self.get(value)

        for dx, dy in self.directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < sx and 0 <= ny < sy and height - self.get((nx, ny)) <= 1:
                yield nx, ny


def multi_bfs(grid: Grid, start: Pt, ends: list[Pt]) -> list[list[Pt]]:
    ends = set(ends)
    open_nodes = deque([start])
    closed_nodes = {start}
    came_from = {start: None}

    paths = []

    while open_nodes:
        current = open_nodes.popleft()

        if current in ends:
            paths.append(retrace_path(came_from, start, current))

        for n in grid.get_neighbours(current):
            if n in closed_nodes:
                continue

            open_nodes.append(n)
            closed_nodes.add(n)
            came_from[n] = current

    return paths


def retrace_path(came_from: dict[Pt, Pt | None], start: Pt, end: Pt) -> list[Pt]:
    current = end
    path = []

    while current != start:
        path.append(current)
        current = came_from[current]

    return path


def solve() -> tuple[int, int]:
    grid = Grid(inputs)
    p1 = len(multi_bfs(grid, grid.end, [grid.start])[0])

    starts = [k for k, v in grid.grid.items() if v == 0]
    p2 = min(len(i) for i in multi_bfs(grid, grid.end, starts))

    return p1, p2


part_one, part_two = solve()
print(f"Part One: {part_one}")
print(f"Part Two: {part_two}")
