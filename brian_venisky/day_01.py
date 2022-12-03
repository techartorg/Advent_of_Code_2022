# Import modules
import sys


def sort_calories():
    input_file = "/".join((sys.path[0], "input.txt"))
    with open(input_file) as input:
        lines = input.readlines()

    sorted_calories = []
    calorie_group = []
    for line in lines:
        if not line == "\n":
            calorie_group.append(int(line.strip("\n")))
        else:
            sorted_calories.append(calorie_group)
            calorie_group = []

    sorted_elves = [sum(elf) for elf in sorted_calories]

    return sorted_elves


def part_one(sorted_elves):
    return max(sorted_elves)


def part_two(sorted_elves):
    highest_total = max(sorted_elves)
    sorted_elves.remove(highest_total)
    second_highest_total = max(sorted_elves)
    sorted_elves.remove(second_highest_total)
    third_highest_total = max(sorted_elves)

    return sum((highest_total, second_highest_total, third_highest_total))


if __name__ == "__main__":
    sorted_elves = sort_calories()
    highest_total = part_one(sorted_elves)
    three_highest_totals = part_two(sorted_elves)

    print(highest_total)
    print(three_highest_totals)
