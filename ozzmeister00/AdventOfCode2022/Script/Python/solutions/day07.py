"""
Python day07

--- Day 7: No Space Left On Device ---
You can hear birds chirping and raindrops hitting leaves as the expedition proceeds.
 Occasionally, you can even hear much louder sounds in the distance; how big do the animals get out here, anyway?

The device the Elves gave you has problems with more than just its communication system.
You try to run a system update:

$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device
Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the resulting
terminal output (your puzzle input). For example:

$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
The filesystem consists of a tree of files (plain data) and directories (which can contain other directories or files).
The outermost directory is called /. You can navigate around the filesystem, moving into or out of directories and
listing the contents of the directory you're currently in.

Within the terminal output, lines that begin with $ are commands you executed, very much like some modern computers:

cd means change directory. This changes which directory is the current directory, but the specific result depends on
the argument:
cd x moves in one level: it looks in the current directory for the directory named x and makes it the current directory.
cd .. moves out one level: it finds the directory that contains the current directory, then makes that directory the
current directory.
cd / switches the current directory to the outermost directory, /.
ls means list. It prints out all of the files and directories immediately contained by the current directory:
123 abc means that the current directory contains a file named abc with size 123.
dir xyz means that the current directory contains a directory named xyz.
Given the commands and output in the example above, you can determine that the filesystem looks visually like this:

- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)
Here, there are four directories: / (the outermost directory), a and d (which are in /), and e (which is in a).
These directories also contain files of various sizes.

Since the disk is full, your first step should probably be to find directories that are good candidates for deletion.
 To do this, you need to determine the total size of each directory. The total size of a directory is the sum of the
 sizes of the files it contains, directly or indirectly. (Directories themselves do not count as having any
 intrinsic size.)

The total sizes of the directories above can be found as follows:

The total size of directory e is 584 because it contains a single file i of size 584 and no other directories.
The directory a has total size 94853 because it contains files f (size 29116), g (size 2557), and h.lst (size 62596),
 plus file i indirectly (a contains e which contains i).
Directory d has total size 24933642.
As the outermost directory, / contains every file. Its total size is 48381165, the sum of the size of every file.
To begin, find all of the directories with a total size of at most 100000, then calculate the sum of their total sizes.
In the example above, these directories are a and e; the sum of their total sizes is 95437 (94853 + 584).
(As in this example, this process can count files more than once!)

Find all of the directories with a total size of at most 100000. What is the sum of the
total sizes of those directories?
"""
import copy
import os

from utils.solver import ProblemSolver

LIST_COMMAND = '$ ls'
CHANGE_DIRECTORY = '$ cd'
UP_DIRECTORY = '..'
ROOTDIR_NAME = 'ROOT:'
SIZE_CAP = 100000
MAX_DISK_SIZE = 70000000
FREE_SIZE = 30000000


class Directory(list):
    """
    A container for representing a directory and its structure
    (mostly for helping with visualization)
    """
    def __init__(self, name):
        super(Directory, self).__init__()
        self.name = name
        self.childDirs = []

    @staticmethod
    def MakeFromStdout(stdout, dirName):
        """
        Create a Directory pre-populated with files using the stdout spew and the name of the directory

        :param list[str] stdout: list of strings of the $ ls dirname
        :param str dirName: the name of the current directory
        :return Directory, list[str]: the directory with file contents, the names of the directories contained in this one
        """
        directories = []
        currDir = Directory(dirName)

        for line in stdout:
            # if it's a directory, just add its name to the list
            # so that we can build the mapping later
            if 'dir' in line:
                childDir = os.path.join(dirName, line.split(' ')[-1])
                directories.append(childDir)
            # otherwise, make a file and add it to the directory
            elif '$' not in line:
                size, fileExt = line.split(' ')
                if '.' in fileExt:
                    fileName, ext = fileExt.split('.')
                else:
                    fileName = fileExt
                    ext = ''
                currDir.append(File(fileName, ext, size))

            if '$' in line:
                message = 'Improperly formatted stdout input:\n' + '\n'.join(stdout)
                raise ValueError(message)

        currDir.childDirs = directories

        return currDir

    @property
    def size(self):
        """
        :return int: the size (in bytes) of this directory and all its contents
        """
        return sum([i.size for i in self])

    @property
    def directories(self):
        """
        :return list[Directory]: all the directories contained in this one
        """
        return [i for i in self if isinstance(i, Directory)]

    @property
    def files(self):
        """
        :return list[File]: all the files contained in this directory
        """
        return [i for i in self if isinstance(i, File)]

    def __str__(self):
        out = f' - {self.name} (dir, size={self.size})\n'
        for i in self:
            out += '    ' + str(i) + '\n'
        return out


class File(object):
    def __init__(self, name, extension, size):
        """
        Represents a file, includes info on size and extension

        :param str name: name of the file
        :param str extension: the extension of the file
        :param int size: how many bytes this file
        """
        super(File, self).__init__()
        self.name = name
        self.extension = extension
        self.size = int(size)

    def __repr__(self):
        return f'File({self.name}, {self.extension}, {self.size})'

    def __str__(self):
        extension = f'.{self.extension}' if self.extension else ''
        return f'- {self.name}{extension} (file, size={self.size})'


def getSubdirectorySize(currDir, sizeList):
    """
    Recurse through the directory tree to get the sizes of all directories

    :param Directory currDir: the active directory we're dealing with
    :param list[(str, int)] sizeList: the current list of directory sizes
    :return list[(str, int)]: list of directory names, sizes
    """
    sizeList.append((currDir.name, currDir.size))
    for subDir in currDir.directories:
        sizeList = getSubdirectorySize(subDir, sizeList)

    return sizeList


class Day07Solver(ProblemSolver):
    def __init__(self):
        super(Day07Solver, self).__init__(7)

        self.testDataAnswersPartOne = [95437]
        self.testDataAnswersPartTwo = [24933642]

    def ProcessInput(self, data=None):
        """
        :param str data:
        :returns: processed data for today's challenge
        """
        if not data:
            data = self.rawData

        dataLines = data.splitlines(keepends=False)

        directories = {}

        # first make all the directories with their raw file contents
        currentDirectory = ''
        for i, line in enumerate(dataLines):
            # if the command is a cd
            if line.startswith(CHANGE_DIRECTORY):
                dirName = line.split(' ')[-1]
                # quick little override for the input data root name
                if dirName == '/':
                    dirName = ROOTDIR_NAME
                # if the command is to go up a directory, change
                # our current directory to  that
                if dirName == UP_DIRECTORY:
                    currentDirectory = os.path.dirname(currentDirectory)
                else:
                    currentDirectory = os.path.join(currentDirectory, dirName)

            # if the line is a list command, then we can make a directory
            elif line == LIST_COMMAND:
                stdout = []
                j = i
                bailOut = False
                while not bailOut:
                    j += 1
                    if j > len(dataLines) - 1:
                        bailOut = True
                    else:
                        currLine = dataLines[j]
                        if '$' not in currLine:
                            stdout.append(currLine)
                        else:
                            bailOut = True

                directories[currentDirectory] = Directory.MakeFromStdout(stdout, currentDirectory)

        # then append the child directories for each dir into its parent directory
        for dirName in directories:
            for childDir in directories[dirName].childDirs:
                directories[dirName].append(directories[childDir])

        return directories[ROOTDIR_NAME]

    def SolvePartOne(self, data=None):
        """
        Find the sum of all the directories with a size greater than 100000

        :param Directory data:
        :returns int: The solution to today's challenge
        """
        if not data:
            data = copy.deepcopy(self.processed)

        sizeList = []
        sizeList = getSubdirectorySize(data, sizeList)

        return sum([size for name, size in sizeList if size <= SIZE_CAP])

    def SolvePartTwo(self, data=None):
        """

        :param data:
        :returns: The solution to part two of today's challenge
        """
        if not data:
            data = copy.deepcopy(self.processed)

        sizeList = []
        sizeList = getSubdirectorySize(data, sizeList)

        rootSize = sizeList[0][-1]

        currFreeSpace = MAX_DISK_SIZE - rootSize
        remainingSpaceNeeds = FREE_SIZE - currFreeSpace

        print(MAX_DISK_SIZE, currFreeSpace, FREE_SIZE, remainingSpaceNeeds)

        # choose the smallest directory to delete that is big enough to free up enough space
        # to clear up the space we need
        candidateDirs = [size for name, size in sizeList if size >= remainingSpaceNeeds]
        candidateDirs.sort()

        return candidateDirs[0]


if __name__ == '__main__':
    day07 = Day07Solver()
    day07.Run()
