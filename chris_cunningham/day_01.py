elves: list[list[int]] = []

with open("day_01.input", "r") as f:
    elves.append([])
    elf_id = 0

    for line in f.read().splitlines():
        if not line:
            elves.append([])
            elf_id += 1
            continue

        elves[elf_id].append(int(line))

    sorted_sums = [*reversed(sorted(sum(i) for i in elves))]
    print(f"Part One: {sorted_sums[0]}")
    print(f"Part Two: {sum(sorted_sums[:3])}")
