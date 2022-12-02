from pathlib import Path

inputs = Path(__file__.replace(".py", ".input")).read_text()
part_one = part_two = 0

for line in inputs.splitlines():
    elf, me = line.split()
    elf = ord(elf) - ord("A")
    me = ord(me) - ord("X")

    part_one += (((me + 1 - elf) % 3) * 3) + me + 1
    part_two += ((elf + me + 2) % 3) + (me * 3 + 1)

print(f"Part One: {part_one}")
print(f"Part two: {part_two}")
