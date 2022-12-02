from pathlib import WindowsPath

ROCK = 1
PAPER = 2
SCISSORS = 3
LOST = 0
DRAW = 3
WIN = 6

input_path = WindowsPath(__file__).parent.parent / 'inputs/day02.txt'


def part_01() -> int:
    score = 0
    lines = [''.join((line.split(' '))) for line in input_path.read_text().split('\n')]
    for line in lines:
        match line:
            case 'AX':
                score += (ROCK + DRAW)
                continue
            case 'AY':
                score += (PAPER + WIN)
                continue
            case 'AZ':
                score += (SCISSORS + LOST)
                continue
            case 'BX':
                score += (ROCK + LOST)
                continue
            case 'BY':
                score += (PAPER + DRAW)
                continue
            case 'BZ':
                score += (SCISSORS + WIN)
                continue
            case 'CX':
                score += (ROCK + WIN)
                continue
            case 'CY':
                score += (PAPER + LOST)
                continue
            case 'CZ':
                score += (SCISSORS + DRAW)
                continue
    return score


def part_02() -> int:
    score = 0
    lines = [(line.split(' ')) for line in input_path.read_text().split('\n')]
    for line in lines:
        match line[0]:
            case 'A':
                match line[1]:
                    case 'X':  # need to lose against rock
                        score += (SCISSORS + LOST)
                        continue
                    case 'Y':  # need to draw against rock
                        score += (ROCK + DRAW)
                        continue
                    case 'Z':  # need to win against rock
                        score += (PAPER + WIN)
                        continue
            case 'B':
                match line[1]:
                    case 'X':  # need to lose against paper
                        score += (ROCK + LOST)
                        continue
                    case 'Y':  # need to draw against paper
                        score += (PAPER + DRAW)
                        continue
                    case 'Z':  # need to win against paper
                        score += (SCISSORS + WIN)
                        continue
            case 'C':
                match line[1]:
                    case 'X':  # need to lose against scissors
                        score += (PAPER + LOST)
                        continue
                    case 'Y':  # need to draw against scissors
                        score += (SCISSORS + DRAW)
                        continue
                    case 'Z':  # need to win against scissors
                        score += (ROCK + WIN)
                        continue
    return score


print('Part 01 answer: {}'.format(part_01()))
print('Part 02 answer: {}'.format(part_02()))
