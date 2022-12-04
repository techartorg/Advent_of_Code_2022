"""
--- Day 2: Rock Paper Scissors ---
The Elves begin to set up camp on the beach. To decide whose tent gets to be closest to the snack storage, a giant Rock
 Paper Scissors tournament is already in progress.

Rock Paper Scissors is a game between two players. Each game contains many rounds; in each round, the players each
simultaneously choose one of Rock, Paper, or Scissors using a hand shape. Then, a winner for that round is selected
: Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock. If both players choose the same shape, the
round instead ends in a draw.

Appreciative of your help yesterday, one Elf gives you an encrypted strategy guide (your puzzle input) that they say
 will be sure to help you win. "The first column is what your opponent is going to play: A for Rock, B for Paper,
 and C for Scissors. The second column--" Suddenly, the Elf is called away to help with someone's tent.

The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for Scissors.
 Winning every time would be suspicious, so the responses must have been carefully chosen.

The winner of the whole tournament is the player with the highest score. Your total score is the sum of your scores for
each round. The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper,
and 3 for Scissors) plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw,
and 6 if you won).

Since you can't be sure if the Elf is trying to help you or trick you, you should calculate the score you would
 get if you were to follow the strategy guide.

For example, suppose you were given the following strategy guide:

A Y
B X
C Z
This strategy guide predicts and recommends the following:

In the first round, your opponent will choose Rock (A), and you should choose Paper (Y). This ends in a win for you
 with a score of 8 (2 because you chose Paper + 6 because you won).
In the second round, your opponent will choose Paper (B), and you should choose Rock (X). This ends in a loss for you
with a score of 1 (1 + 0).
The third round is a draw with both players choosing Scissors, giving you a score of 3 + 3 = 6.
In this example, if you were to follow the strategy guide, you would get a total score of 15 (8 + 1 + 6).

What would your total score be if everything goes exactly according to your strategy guide?
"""

from utils.solver import ProblemSolver
import utils.math


class Shapes(object):
    Rock = 1
    Paper = 2
    Scissors = 3


OpponentPlays = {'A': Shapes.Rock,
                 'B': Shapes.Paper,
                 'C': Shapes.Scissors}


YourPlays = {'X': Shapes.Rock,
             'Y': Shapes.Paper,
             'Z': Shapes.Scissors}


# map an input move to the move it defeats
RockPaperScissors = {Shapes.Rock: Shapes.Scissors,
                     Shapes.Scissors: Shapes.Paper,
                     Shapes.Paper: Shapes.Rock}

# invert the mapping so we can find the move that would defeat the key
ScissorsPaperRock = {v: k for k, v in RockPaperScissors.items()}


class TurnResults(object):
    YouWin = 6
    YouLose = 0
    Draw = 3


YourResults = {1: TurnResults.YouLose,
               2: TurnResults.Draw,
               3: TurnResults.YouWin}


def EvaluateTurn(opponentPlay, yourPlay):
    """
    Based on the input played shapes, compare them to determine if you drew, lost, or won
    :param int opponentPlay: the shape they played
    :param yourPlay: the shape you played
    :return int: the point result of the turn
    """
    result = 0
    if opponentPlay == yourPlay:
        result = TurnResults.Draw
    elif RockPaperScissors[opponentPlay] == yourPlay:
        result = TurnResults.YouLose
    else:
        result = TurnResults.YouWin

    return result + yourPlay


def FindDesiredMove(opponentPlay, yourResult):
    """
    Based on your opponents move and the desired outcome of the round, return the shape you should play
    :param int opponentPlay: which shape your opponent played
    :param int yourResult: what result you want out of the turn

    :return int: which shape you should play to achieve the desired outcome
    """
    if yourResult == TurnResults.Draw:
        return opponentPlay
    elif yourResult == TurnResults.YouWin:
        return ScissorsPaperRock[opponentPlay]
    else:
        return RockPaperScissors[opponentPlay]


class Day02Solver(ProblemSolver):
    def __init__(self):
        super(Day02Solver, self).__init__(2)

        self.testDataAnswersPartOne = [15]
        self.testDataAnswersPartTwo = [12]

    def ProcessInput(self, data=None):
        """
        Takes the input test string and turns the strings into integers

        :param string data:
        :returns list[int]: processed data for today's challenge
        """
        if not data:
            data = self.rawData

        processed = []
        for line in data.split('\n'):
            theirs, yours = line.split(' ')
            if not (theirs in OpponentPlays and yours in YourPlays):
                raise ValueError(f"Input strategy {line} is not supported")
            processed.append((OpponentPlays[theirs], YourPlays[yours]))

        return processed

    def SolvePartOne(self, data=None):
        """
        :param list data: list of calorie counts

        :returns int: The solution to today's challenge
        """
        if not data:
            data = self.processed

        score = 0
        for theirs, yours in data:
            score += EvaluateTurn(theirs, yours)

        return score

    def SolvePartTwo(self, data=None):
        """
        :param list data: list of calorie counts

        :returns int: The solution to today's challenge
        """
        if not data:
            data = self.processed

        score = 0
        for theirs, result in data:
            yours = FindDesiredMove(theirs, YourResults[result])
            score += EvaluateTurn(theirs, yours)

        return score


if __name__ == '__main__':
    day02 = Day02Solver()
    day02.Run()
