from pathlib import Path

inputs = Path(__file__.replace(".py", ".input")).read_text().splitlines()
_test = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop""".splitlines()


def part_one() -> int:
    cycle = 1
    signal = 1

    check_cycles = [20, 60, 100, 140, 180, 220]
    cycle_strengths = [0 for _ in range(len(check_cycles))]

    def next_cycle():
        nonlocal cycle

        for i, c in enumerate(check_cycles):
            if cycle == c:
                cycle_strengths[i] = signal * cycle

        cycle += 1

    for i in inputs:
        match i.split():
            case ["noop"]:
                next_cycle()
            case ["addx", value]:
                next_cycle()
                next_cycle()
                signal += int(value)
    return sum(cycle_strengths)


def part_two():
    cycle = 1
    signal = 1
    lines = []
    current_line = [' ' for _ in range(40)]

    def next_cycle():
        nonlocal cycle, signal

        cycle += 1

    for i in inputs:
        match i.split():
            case ["noop"]:
                next_cycle()
            case ["addx", value]:
                next_cycle()
                next_cycle()
                signal += int(value)


print(f"Part One: {part_one()}")
print("Part Two:")
part_two()
