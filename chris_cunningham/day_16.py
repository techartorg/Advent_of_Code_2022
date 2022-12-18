import re
from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict
from itertools import permutations

valves_pattern = re.compile(r"([A-Z]{2})")
flow_pattern = re.compile(r"=(-?\d+)")
inputs = Path(__file__.replace(".py", ".input")).read_text().splitlines()
_test = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II""".splitlines()


@dataclass
class Valve(object):
    name: str
    rate: int
    edges: list[str]

    def __hash__(self):
        return hash(self.name)


def parse_input(line: str) -> Valve:
    name, *edges = valves_pattern.findall(line)
    rate = int(flow_pattern.findall(line)[0])
    return Valve(name, rate, edges)


valves = [parse_input(i) for i in inputs]


def floyd_warshall(valves: list[Valve]) -> dict[Valve, dict[Valve, int]]:
    graph = defaultdict(dict)

    for v1, v2 in permutations(valves, 2):
        if v1 is v2:
            graph[v1][v2] = 0
        elif v2.name in v1.edges:
            graph[v1][v2] = 1
        else:
            graph[v1][v2] = 0xff

    for i, j, k in permutations(valves, 3):
        if graph[i][j] > (v := graph[i][k] + graph[k][j]):
            graph[i][j] = v

    return graph


graph = floyd_warshall(valves)

# pick valves with flow to start
worth_it = [i for i in valves if i.rate > 0 or i.name == "AA"]

# assign bits
bit_field = {v: 1 << i for i, v in enumerate(worth_it)}

# find start
start = next(bit_field[i] for i in worth_it if i.name == "AA")

# list for fast edge lookup
bitgraphs = [0] * 0xffff
for v1, v2 in permutations(worth_it, 2):
    bitgraphs[bit_field[v1] | bit_field[v2]] = graph[v1][v2]


def dfs(target: int, pressure: int, minute: int, on: int, node) -> int:
    max_pressure = pressure

    for bits, rate in ((bit_field[i], i.rate) for i in worth_it):
        if node == bits or bits == start or (bits & on) != 0:
            continue

        l = bitgraphs[node | bits] + 1
        if minute + l > target:
            continue

        if (n := dfs(target, pressure + (target - minute - l) * rate, minute + l, on | bits, bits)) > max_pressure:
            max_pressure = n

    return max_pressure


# 1831 too low
print(f"Part One: {dfs(30, 0, 0, 0, start)}")
