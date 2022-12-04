"""
Stores out problem-solver class
"""

import os

from . import constants


class ProblemSolver(object):
    """
    Common class for loading and processing data from each day's challenge
    """
    def __init__(self, day):
        """
        Finds the input data file for this day, and loads the raw contents of that file into
        the rawData property of the instance

        :param int day: the number day for this data
        """
        self.day = day

        # leave this open for later access by process input
        self.processed = None
        self.partOneResult = None
        self.partTwoResult = None

        self.rawData = self.loadDataFromFile(self.makeDayFilePath())
        self.testData = self.loadTestData()

        self.testDataAnswersPartOne = []
        self.testDataAnswersPartTwo = []

    def loadTestData(self):
        """

        :return dict: test data in lists for {'partOne':[testA, testB]}
        """
        dayName = self.makeDayFileName() + '_test'
        testDataFilePaths = []
        for fileName in os.listdir(constants.getInputsFolder()):
            if dayName in fileName:
                testDataFilePaths.append(os.path.join(constants.getInputsFolder(), fileName))

        outDict = {'partOne': [],
                   'partTwo': []}

        for filePath in testDataFilePaths:
            idToken = os.path.split(filePath)[-1].split('_test')[-1]
            if idToken[0] == '1':
                outDict['partOne'].append(self.loadDataFromFile(filePath))
            elif idToken[0] == '2':
                outDict['partTwo'].append(self.loadDataFromFile(filePath))
            else:
                raise ValueError(f"Found a filePath that doesn't have a valid idToken {filePath}."
                                 f"\nIDToken = {idToken}"
                                 f"\nShould contain test1 or test2 after the day")

        return outDict

    def makeDayFileName(self):
        """

        :return str:
        """
        return f'day{str(self.day).zfill(2)}'

    def makeDayFilePath(self):
        """

        :param bool isTest:
        :return str: the full file path to the input data for the day
        """
        fileName = self.makeDayFileName() + '.txt'
        return os.path.join(constants.getInputsFolder(), fileName)

    def loadDataFromFile(self, filePath):
        """

        :param str filePath: full path to the file containing the data
        :return str: raw data from the file
        """
        rawData = ''
        # load in the file's data
        if os.path.exists(filePath):
            with open(filePath, 'r') as fh:
                rawData = fh.read()
        else:
            raise FileNotFoundError("Couldn't find the input file {}".format(filePath))

        return rawData

    def ProcessInput(self, data=None):
        """
        To be implemented by each day's class to process data into a helpful format
        for later handling

        :returns: Processed Input
        """
        raise NotImplementedError()

    def TestAlgorithm(self, algorithm, part=1):
        """
        :param func algorithm: The algorithm function to test on the test data
        :param int part: the part of the day's solution to test

        :returns bool: If the tests passed, otherwise raises exception since we should pass our tests
        """
        testData = []
        answers = []
        if part == 1:
            testData = self.testData['partOne']
            answers = self.testDataAnswersPartOne
        elif part == 2:
            testData = self.testData['partTwo']
            answers = self.testDataAnswersPartTwo
        else:
            raise ValueError(f"Input part {part} is invalid")

        for i, test in enumerate(testData):
            processed = self.ProcessInput(data=test)
            result = algorithm(data=processed)
            message = f"Test on data {processed} returned result {result}"
            if result != answers[i]:
                raise Exception(message)
            else:
                print(message)

        return True

    def SolvePartOne(self, data=None):
        """
        Method to be implemented to solve for part one

        :param object data: optional data to process

        :returns: The solution for part one
        """
        raise NotImplementedError()

    def SolvePartTwo(self, data=None):
        """
        Method to be implemented to solve for part two

        :param object data: optional data to operate on

        :returns: The solution for part two
        """
        raise NotImplementedError()

    def Run(self):
        """
        Run the full suite of testing and processing for this day
        """
        self.processed = self.ProcessInput()
        try:
            print('TestResult:', self.TestAlgorithm(self.SolvePartOne))
            print('Result: ', self.SolvePartOne())
            print('TestResult2:', self.TestAlgorithm(self.SolvePartTwo, part=2))
            print('Result: ', self.SolvePartTwo())
        except NotImplementedError:
            print("Testing not complete due to some parts not being implemented properly")
