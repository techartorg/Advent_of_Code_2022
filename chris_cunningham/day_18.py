from __future__ import annotations

from pathlib import Path
from typing import NamedTuple, Iterator

inputs = Path(__file__.replace(".py", ".input")).read_text().splitlines()


class Point(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other: Point) -> Point:
        return Point(*[l + r for l, r in zip(self, other)])

    def __mul__(self, other: Point) -> Point:
        return Point(*[l * r for l, r in zip(self, other)])

    @property
    def neighbours(self) -> Iterator[Point]:
        for d in [Point(0, 1, 0), Point(0, -1, 0), Point(-1, 0, 0), Point(1, 0, 0), Point(0, 0, 1), Point(0, 0, -1)]:
            yield self + d


class Bounds(NamedTuple):
    min: Point
    max: Point

    def contains_point(self, point: Point) -> bool:
        return all(r >= l for l, r in zip(self.min, point)) and all(r <= l for l, r in zip(self.max, point))


directions = [Point(0, 1, 0), Point(0, -1, 0), Point(-1, 0, 0), Point(1, 0, 0), Point(0, 0, 1), Point(0, 0, -1)]
lava_set = set(Point(*[int(i) for i in line.split(",")]) for line in inputs)

surface_area = sum(n not in lava_set for p in lava_set for n in p.neighbours)
print(f"Part One: {surface_area}")

bounds = Bounds(
    Point(*[min(p[c] for p in lava_set) for c in range(3)]),
    Point(*[max(p[c] for p in lava_set) for c in range(3)])
)


def is_interior(point: Point) -> bool:
    if point in lava_set:
        return False

    hit_count = 0

    for d in directions:
        pt = point
        while bounds.contains_point(pt):
            if pt in lava_set:
                hit_count += 1
                break

            pt += d

    return hit_count == 6


air_pockets = set()
for x in range(bounds.min.x, bounds.max.x + 1):
    for y in range(bounds.min.y, bounds.max.y + 1):
        for z in range(bounds.min.z, bounds.max.z + 1):
            if is_interior(pt := Point(x, y, z)):
                air_pockets.add(pt)

air_surface_area = sum(n not in air_pockets for p in air_pockets for n in p.neighbours)

print(f"Part Two: {surface_area - air_surface_area}")
