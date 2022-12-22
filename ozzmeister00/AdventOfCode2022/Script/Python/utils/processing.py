"""
Helper functions for processing input data
"""


def commaSeparatedIntegers(inString):
    """
    Converts a comma-separated string of "integers" to a list of actual integers

    :param str inString: comma-separated list of integers in string form

    :return list[int]: that input string converted to integers
    """
    return [int(i) for i in inString.split(',')]
