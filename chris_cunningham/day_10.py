from pathlib import Path

inputs = Path(__file__.replace(".py", ".input")).read_text().splitlines()

WIDTH = 40
HEIGHT = 6
CHECK_CYCLES = [20, 60, 100, 140, 180, 220]


def solve() -> tuple[int, list[list[bool]]]:
    cycle = 0
    register = 1
    strength = 0

    lines = [[False for _ in range(WIDTH)] for _ in range(HEIGHT)]

    def next_cycle():
        nonlocal cycle, register, strength
        x = cycle % WIDTH
        y = cycle // WIDTH

        for i, c in enumerate(CHECK_CYCLES):
            if cycle + 1 == c:
                strength += register * (cycle + 1)

        lines[y][x] = abs(x - register) < 2

        cycle += 1

    for i in inputs:
        next_cycle()

        if len(inst := i.split()) == 2:
            next_cycle()
            register += int(inst[1])

    return strength, lines


def render(lines: list[list[bool]]):
    print(f'┌{"".join("─" for _ in range(WIDTH))}┐')
    for row in lines:
        print(f'│{"".join("█" if i else " " for i in row)}│')
    print(f'└{"".join("─" for _ in range(WIDTH))}┘')


part_one, part_two = solve()
print(f"Part One: {part_one}")
print("Part Two:")
render(part_two)

