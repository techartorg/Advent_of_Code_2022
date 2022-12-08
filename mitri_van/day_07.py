#! python3.11
"""
--- Day 7: No Space Left On Device ---
You can hear birds chirping and raindrops hitting leaves as the expedition proceeds. Occasionally, you can even hear much louder sounds in the distance; how big do the animals get out here, anyway?

The device the Elves gave you has problems with more than just its communication system. You try to run a system update:

$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device

Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the resulting terminal output (your puzzle input). For example:

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

The filesystem consists of a tree of files (plain data) and directories (which can contain other directories or files). The outermost directory is called /. You can navigate around the filesystem, moving into or out of directories and listing the contents of the directory you're currently in.

Within the terminal output, lines that begin with $ are commands you executed, very much like some modern computers:

	cd means change directory. This changes which directory is the current directory, but the specific result depends on the argument:
	cd x moves in one level: it looks in the current directory for the directory named x and makes it the current directory.
	cd .. moves out one level: it finds the directory that contains the current directory, then makes that directory the current directory.
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

Here, there are four directories: / (the outermost directory), a and d (which are in /), and e (which is in a). These directories also contain files of various sizes.

Since the disk is full, your first step should probably be to find directories that are good candidates for deletion. To do this, you need to determine the total size of each directory. The total size of a directory is the sum of the sizes of the files it contains, directly or indirectly. (Directories themselves do not count as having any intrinsic size.)

The total sizes of the directories above can be found as follows:

	The total size of directory e is 584 because it contains a single file i of size 584 and no other directories.
	The directory a has total size 94853 because it contains files f (size 29116), g (size 2557), and h.lst (size 62596), plus file i indirectly (a contains e which contains i).
	Directory d has total size 24933642.
	As the outermost directory, / contains every file. Its total size is 48381165, the sum of the size of every file.

To begin, find all of the directories with a total size of at most 100000, then calculate the sum of their total sizes. In the example above, these directories are a and e; the sum of their total sizes is 95437 (94853 + 584). (As in this example, this process can count files more than once!)

Find all of the directories with a total size of at most 100000. What is the sum of the total sizes of those directories?

Your puzzle answer was 1141028.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
Now, you're ready to choose a directory to delete.

The total disk space available to the filesystem is 70000000. To run the update, you need unused space of at least 30000000. You need to find a directory you can delete that will free up enough space to run the update.

In the example above, the total size of the outermost directory (and thus the total amount of used space) is 48381165; this means that the size of the unused space must currently be 21618835, which isn't quite the 30000000 required by the update. Therefore, the update still requires a directory with total size of at least 8381165 to be deleted before it can run.

To achieve this, you have the following options:

Delete directory e, which would increase unused space by 584.
Delete directory a, which would increase unused space by 94853.
Delete directory d, which would increase unused space by 24933642.
Delete directory /, which would increase unused space by 48381165.

Directories e and a are both too small; deleting them would not free up enough space. However, directories d and / are both big enough! Between these, choose the smallest: d, increasing unused space by 24933642.

Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update. What is the total size of that directory?
"""

test_data = ['$ cd /',
			 '$ ls',
			 'dir a',
			 '14848514 b.txt',
			 '8504156 c.dat',
			 'dir d',
			 '$ cd a',
			 '$ ls',
			 'dir e',
			 '29116 f',
			 '2557 g',
			 '62596 h.lst',
			 '$ cd e',
			 '$ ls',
			 '584 i',
			 '$ cd ..',
			 '$ cd ..',
			 '$ cd d',
			 '$ ls',
			 '4060174 j',
			 '8033020 d.log',
			 '5626152 d.ext',
			 '7214296 k'
			]

test_data = '$ cd /\n$ ls\ndir a\n14848514 b.txt\n8504156 c.dat\ndir d\n$ cd a\n$ ls\ndir e\n29116 f\n2557 g\n62596 h.lst\n$ cd e\n$ ls\n584 i\n$ cd ..\n$ cd ..\n$ cd d\n$ ls\n4060174 j\n8033020 d.log\n5626152 d.ext\n7214296 k\n'

TOTAL_DISK_SPACE = 70000000
TARGET_FREE_SPACE_THE_GREAT_WAR = 30000000

total_disk_usage = 0



class FileObject():

	def __init__(self, file_name, file_size):
		self.name = file_name
		self.size = file_size

	# def __str__(self):
		# return self.name


	def __repr__(self):
		return f"{self.__class__.__name__} object '{self.name}'> size = {self.size}"


	def __eq__(self, other):
		return self.size == other.file_size


	def __lt__(self, other):
		return self.size > other.file_size


	def __gt__(self, other):
		return self.size > other.file_size



class FileDir():

	def __init__(self, dir_name, parent = None, files = {}):
		self.name = dir_name
		self.files = {}
		self.parent = parent


	def __str__(self):
		# output_string = ''

		# output_string == f"['//']: {self.size}\n\t{self.print()}"
		# output_string += self.print()

		return self.name

	def __repr__(self):
		return f"<{self.__class__.__name__} object '{self.name}'> at {hex(id(self))}>"

	@property
	def size(self):
		return self.get_size()

	def get_size(self):
		return sum([self.files[x].size for x in self.files.keys()])

	def get_children(self):
		return str([x for x in self.files.keys()])

	def print(self, depth = ''):
		disk_usage = []
		depth = depth + '\t'

		output_string = f'[{self.name}] : {self.size}\n'
		disk_usage.append(self.size)

		for i in self.files.keys():
			if type(self.files[i]) == FileObject:
				output_string += f'{depth}{self.files[i].name} : {self.files[i].size}\n'
			elif type(self.files[i]) == FileDir:
				result, disk_use = self.files[i].print(depth = depth)

				output_string += depth + result
				disk_usage.append(disk_use)

		return output_string, disk_usage


def parse_data(data, file_system, dir_path = None, current_dir = None):
	for datum in data:
		dir_name =  None
		file_name = ''
		file_size = 0

		if datum == '$ cd /':
			pass

		elif datum == '$ cd ..':
			current_dir = current_dir.parent
			dir_path.pop()

		elif datum.startswith('$ cd '):
			current_path = dir_path[-1]

			dir_name = datum.replace('$ cd ', '')
			dir_path.append(dir_name)

			current_dir = current_dir.files[dir_path[-1]]
			# local_file_system = parse_data(datum, None, dir_path = dir_name, current_dir = new_dir)

		else:
			commands = datum.rstrip().split('\n')
			if commands[0] == '$ ls':
				for cmd in commands[1:]:
					# directory found
					if cmd.startswith('dir '):
						dir_name = cmd.replace('dir ', '')
						if dir_name not in current_dir.files.keys():
							current_dir.files[dir_name] = FileDir(dir_name, parent = current_dir )#dir_path )
						else:
							assert 'Key collision'

					# No matches, datum must be a file
					else:
						file_size, file_name = cmd.split(' ')
						current_dir.files[file_name] = FileObject(file_name, int(file_size))

			else:
				assert commands[0] != '$ ls', 'This should never happen'

	return file_system


def disk_usage_report(file_system, mem_limit = 100000):
	filtered_dirs = []
	global total_disk_usage

	for key, value in file_system.files.items():
		if type(value) is FileObject:
			yield(key, value.size)

		elif type(value.files) is dict:
			dir_size = file_system.files[key].size
			if dir_size <= mem_limit:
				filtered_dirs.append(file_system.files[key].name)
				total_disk_usage += file_system.files[key].size

			# print(f'\t[{file_system.files[key].name}] {file_system.files[key].size}')
			yield from disk_usage_report(value)

		else:
			yield (key, value.size)

	# print(f'Valid directories: {filtered_dirs}')

def parse_disk_usage(data):
	disk_sizes = []
	for x in data:
		if type(x) == int:
			disk_sizes.append(x)

		else:
			disk_sizes.extend(parse_disk_usage(x))

	return disk_sizes


def main(raw_data):
	file_system = {}

	data = raw_data.replace('\n$', '#$').split('#')

	# Set up the root directory
	cwd = '//'
	root_dir = FileDir(cwd)
	file_system = {root_dir.name: root_dir}

	# Run
	file_system = parse_data(data, file_system, dir_path = [cwd], current_dir = file_system[cwd])

	# Generate disk usage
	# print(f'[{file_system[cwd].name}] {file_system[cwd].size}')
	for key, value in disk_usage_report(file_system[cwd]):
		pass
		# print(f'\t\t{key}:  {value}')
	disk_usage_report(file_system[cwd])

	print(f'\nTotal disk usage: {total_disk_usage}\n')

	### Part Two:
	result, disk_usage = file_system['//'].print()
	print(result)

	disk_sizes = sorted(parse_disk_usage(disk_usage))
	descent_free_space = TOTAL_DISK_SPACE - file_system['//'].size


	target_dir = 0
	for disk_size in disk_sizes:
		if disk_size + descent_free_space > TARGET_FREE_SPACE_THE_GREAT_WAR:
			target_dir = disk_size
			break

	print(f'Recommended folder is size {target_dir}\n')



if __name__ == "__main__":
	input = r"D:\Projects\Advent_of_Code\2022\day_07_input.txt"
	raw_data = []

	with open(input, "r") as input_file:
		raw_data = input_file.read()

	# main(test_data)
	main(raw_data)
