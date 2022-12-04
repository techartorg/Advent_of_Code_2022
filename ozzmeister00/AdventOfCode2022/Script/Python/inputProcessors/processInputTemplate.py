import collections
import random
import itertools

inputFile = r"D:\Advent_of_Code_2020\ozzmeister00\PyAdventOfCode2020\inputs\dayXX.txt"
testFile = r"D:\Advent_of_Code_2020\ozzmeister00\PyAdventOfCode2020\inputs\dayXX_test.txt"

inputFiles = [testFile, inputFile]


def main():
    for filePath in inputFiles:
        with open(filePath, 'r') as fh:
            lines = fh.readlines()

            outCSV = 'RowID,Contents,Parents,Color\n'
            for line in lines:
                pass

            with open(filePath.replace('.txt', '.csv'), 'w') as outFH:
                outFH.write(outCSV)

main()
