"""
Constants and constant generators
"""

import os

INPUTS_FOLDER_NAME = "inputData"


def getInputsFolder():
    """

    :return str: the absolute path on the file system to the inputData folder, which should be relative to this package
    """
    # figure out where we are
    utilsFolder = os.path.dirname(os.path.abspath(__file__))

    # go up one folder
    sourceFolder = os.path.split(utilsFolder)[0]

    return os.path.join(sourceFolder, INPUTS_FOLDER_NAME)
