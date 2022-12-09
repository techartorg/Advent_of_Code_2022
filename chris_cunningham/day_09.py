from pathlib import Path

inputs = Path(__file__.replace(".py", ".input")).read_text().splitlines()

directions = {'L': -1, 'R': 1, "U": 1j, "D": -1j}
data = [(directions[s[0]], int(s[1])) for i in inputs if (s := i.split())]


def sign(x: int) -> int:
    return 0 if x == 0 else x // abs(x)


def solve(count: int) -> int:
    rope = [0 for _ in range(count)]
    visited = set()

    for d, l in data:
        for _ in range(l):
            rope[0] += d

            for i in range(1, count):
                dist = rope[i-1] - rope[i]

                if max(abs(dist.real), abs(dist.imag)) > 1:
                    rope[i] += sign(dist.real) + 1j * sign(dist.imag)

            visited.add(rope[-1])

    return len(visited)


print(f"Part One: {solve(2)}")
print(f"Part Two: {solve(10)}")
