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
        height = self.get(value) + 1

        for dx, dy in self.directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < sx and 0 <= ny < sy and self.get((nx, ny)) <= height:
                yield nx, ny


def bfs(grid: Grid, start: Pt, end: Pt) -> list[Pt] | None:
    open_nodes = deque([start])
    closed_nodes = {start}
    came_from = {start: None}
    found = False

    while open_nodes:
        current = open_nodes.popleft()
        if current == end:
            found = True
            break

        for n in grid.get_neighbours(current):
            if n in closed_nodes:
                continue

            open_nodes.append(n)
            closed_nodes.add(n)
            came_from[n] = current

    if not found:
        return None

    # Retrace path
    current = end
    path = []
    while current != start:
        path.append(current)
        if current not in came_from:
            break

        current = came_from[current]

    path.reverse()
    return path


def solve() -> tuple[int, int]:
    grid = Grid(inputs)
    p1 = len(bfs(grid, grid.start, grid.end))

    starts = [k for k, v in grid.grid.items() if v == 0]
    paths = [r for i in starts if (r := bfs(grid, i, grid.end))]

    return p1, min(len(i) for i in paths)


part_one, part_two = solve()
print(f"Part One: {part_one}")
print(f"Part Two: {part_two}")
