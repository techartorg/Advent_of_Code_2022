puzzle_input = open(__file__.replace('.py', '_input.txt')).read()

test_input = '''$ cd /
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
'''

class Folder:
    def __init__(self, name, parent):
        self.name = name
        self.files = []
        self.folders = []
        self.parent = parent
    
    def size(self):
        return sum([f.size for f in self.files])
    
    def __repr__(self):
        return f'Folder: {self.name}'


class File:
    def __init__(self, name, size, parent):
        self.name = name
        self.size = int(size)
        self.parent = parent
    
    def __repr__(self):
        return f'File: {self.name}'


def run(input_):
    
    folders = []
    currentFolder = None

    # parse the folder and file structure and store all the folders in a list.
    commands = input_.splitlines()
    for i, cmd in enumerate(commands):

        if cmd.startswith('$ cd'):
            foldername = cmd.split(' ')[-1]

            if foldername == '/':
                root = Folder(r'/', None)
                folders.append(root)
                currentFolder = root

            elif foldername == '..':
                parent = currentFolder.parent
                currentFolder = parent
            
            else:
                m = [x for x in currentFolder.folders if x.name == foldername][0]
                currentFolder = m
        
        elif cmd.startswith('$ ls'):
            pass
        
        elif cmd.startswith('dir'):
            typ, name = cmd.split(' ')
            f = Folder(name, currentFolder)
            currentFolder.folders.append(f)
            folders.append(f)
        
        else:
            size, filename = cmd.split(' ')
            file = File(filename, size, currentFolder)
            currentFolder.files.append(file)

    # recursive function to gather the total size of all sub-folders.
    def folder_size(folder):
        size = folder.size()
        sub_folders = folder.folders
        for s in sub_folders:
            size += folder_size(s)
        return size
    
    # Solve for part 1 and 2.
    usedspace = (folder_size(root))
    totalspace = 70000000
    freespace = totalspace - usedspace
    diff = 30000000 - freespace

    foldersToConsider = []
    sum = 0

    for folder in folders:
        size = folder_size(folder)
        if size <= 100000:
            sum += size
        if size > diff:
            foldersToConsider.append(size)
    
    return (sum, min(foldersToConsider))

a, b = run(puzzle_input)
print(f'Part One: {a}, Part Two: {b}')
