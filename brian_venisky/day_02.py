from pathlib import Path

"""
Opponent:
A = Rock
B = Paper
C = Scissors

Me:
X = Rock
Y = Paper
Z = Scissors

Points:
Rock = 1
Paper = 2
Scissors = 3
Win = 6
Tie = 3
Loss = 0
"""

WTL_CODEC = {
    "A": {"X": "Tie", "Y": "Win", "Z": "Loss"},
    "B": {"X": "Loss", "Y": "Tie", "Z": "Win"},
    "C": {"X": "Win", "Y": "Loss", "Z": "Tie"},
}

SHAPE_CODEC = {
    "X": {"A": "Z", "B": "X", "C": "Y"},
    "Y": {"A": "X", "B": "Y", "C": "Z"},
    "Z": {"A": "Y", "B": "Z", "C": "X"},
}

POINTS = {
    "X": 1,
    "Y": 2,
    "Z": 3,
    "Win": 6,
    "Tie": 3,
    "Loss": 0,
}


def rps_shoot():
    rounds = [
        round.split(" ")
        for round in Path(__file__).parent.joinpath("input.txt").read_text().split("\n")
    ]

    part_one_total = calculate_score(rounds)
    part_two_total = calculate_score(rounds, is_part_two=True)

    return part_one_total, part_two_total


def calculate_score(rounds, is_part_two=False):
    """ """
    total = 0
    for round in rounds:
        opponent = round[0]
        me = round[1]
        if is_part_two:
            me = SHAPE_CODEC[me][opponent]
        result = WTL_CODEC[opponent][me]
        round_total = POINTS[me] + POINTS[result]
        total += round_total

    return total


if __name__ == "__main__":
    part_one_total, part_two_total = rps_shoot()
    print("Part 1: {}".format(part_one_total))
    print("Part 2: {}".format(part_two_total))
