import re
from pathlib import Path

from shapely.ops import unary_union, clip_by_rect
from shapely.geometry import Polygon, LineString

CHECK_Y = 2_000_000
LIMIT = 4_000_000
pattern = re.compile(r".+x=(-?\d+), y=(-?\d+).+x=(-?\d+), y=(-?\d+)")
inputs = Path(__file__.replace(".py", ".input")).read_text().splitlines()

upoly = Polygon()

for line in inputs:
    sx, sy, bx, by = [int(i) for i in pattern.match(line).groups()]
    md = abs(sx - bx) + abs(sy - by)
    upoly = unary_union([upoly, Polygon([(sx, sy + md), (sx - md, sy), (sx, sy - md), (sx + md, sy)])])

bounds = upoly.bounds
line = LineString([(bounds[0], CHECK_Y), (bounds[2], CHECK_Y)])
no_beacon = [i[0] for i in upoly.intersection(line).coords[:]]
print(f"Part One: {round(no_beacon[1] - no_beacon[0])}")

interior = clip_by_rect(upoly, 0, 0, LIMIT, LIMIT).interiors[0]
x, y = [round(i) for i in interior.centroid.coords[:][0]]
print(f"Part Two: {x * LIMIT + y}")
