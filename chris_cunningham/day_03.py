from pathlib import Path

inputs = Path(__file__.replace(".py", ".input")).read_text().splitlines()


def priority(char: str) -> int:
    return (ord(char) - ord('A')) + 27 if char.isupper() else (ord(char) - ord('a')) + 1


def distinct(*args: str) -> str:
    r = set(args[0])
    for i in args[1:]:
        r &= set(i)
    return r.pop()


part_one = sum(priority(distinct(i[:len(i)//2], i[len(i)//2:])) for i in inputs)
print(f"Part One: {part_one}")

groups = [inputs[i:i+3] for i in range(0, len(inputs), 3)]
part_two = sum(priority(distinct(*i)) for i in groups)
print(f"Part Two: {part_two}")
