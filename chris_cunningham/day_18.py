from __future__ import annotations

from pathlib import Path
from collections import deque
from typing import NamedTuple, Iterator

inputs = Path(__file__.replace(".py", ".input")).read_text().splitlines()


class Point(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other: Point) -> Point:
        return Point(*[l + r for l, r in zip(self, other)])

    def __sub__(self, other: Point) -> Point:
        return Point(*[l - r for l, r in zip(self, other)])

    @property
    def neighbours(self) -> Iterator[Point]:
        for d in [Point(0, 1, 0), Point(0, -1, 0), Point(-1, 0, 0), Point(1, 0, 0), Point(0, 0, 1), Point(0, 0, -1)]:
            yield self + d


class Bounds(NamedTuple):
    min: Point
    max: Point

    def contains_point(self, point: Point) -> bool:
        return all(r >= l for l, r in zip(self.min, point)) and all(r <= l for l, r in zip(self.max, point))

    def expand(self, n: int = 1) -> Bounds:
        return Bounds(self.min - Point(n, n, n), self.max + Point(n, n, n))

    @property
    def points(self) -> Iterator[Point]:
        for x in range(self.min.x, self.max.x + 1):
            for y in range(self.min.y, self.max.y + 1):
                for z in range(self.min.z, self.max.z + 1):
                    yield Point(x, y, z)


def calc_surface_area(points: set[Point]) -> int:
    return sum(n not in points for p in points for n in p.neighbours)


def find_exterior(solid: set[Point], bounds: Bounds) -> set[Point]:
    bounds = bounds.expand(1)
    start = bounds.min

    open_points = deque([start])
    closed_points = {start}

    exterior = {start}

    while open_points:
        current = open_points.popleft()

        for n in current.neighbours:
            if n in closed_points or not bounds.contains_point(n) or n in solid:
                continue

            open_points.append(n)
            closed_points.add(n)
            exterior.add(n)

    return exterior


lava_set = set(Point(*[int(i) for i in line.split(",")]) for line in inputs)

surface_area = calc_surface_area(lava_set)
print(f"Part One: {surface_area}")

# find exterior
bounds = Bounds(
    Point(*[min(p[c] for p in lava_set) for c in range(3)]),
    Point(*[max(p[c] for p in lava_set) for c in range(3)])
)

exterior_set = find_exterior(lava_set, bounds)
all_set = set(bounds.points)
interior_surface_area = calc_surface_area(all_set - exterior_set - lava_set)
print(f"Part Two: {surface_area - interior_surface_area}")
