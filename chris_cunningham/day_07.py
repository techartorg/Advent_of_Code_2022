from __future__ import annotations
from pathlib import Path

MAX_DIR_SIZE = 100000
DISK_SPACE = 70000000
NEEDED_SPACE = 30000000
inputs = Path(__file__.replace(".py", ".input")).read_text().splitlines()


class File(object):
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size


class Directory(object):
    def __init__(self, name: str):
        self.name = name
        self.files: list[File] = []
        self.directories: list[Directory] = []

    @property
    def size(self) -> int:
        return sum(i.size for i in self.files) + sum(i.size for i in self.directories)


root = Directory("/")
cwd: Directory | None = root
path = Path("/")
dir_map: dict[str, Directory] = {str(path): root}

for line in inputs[1:]:
    match line.split():
        case["$", "cd", ".."]:
            path = path.parent
            cwd = dir_map[str(path)]

        case["$", "cd", new_cwd]:
            path = path / new_cwd

            if str(path) in dir_map:
                cwd = dir_map[str(path)]
            else:
                cwd = Directory(new_cwd)
                dir_map[str(path)] = cwd

        case["$", "ls"]:
            continue

        case["dir", d]:
            new_dir = Directory(d)
            dir_map[str(path / d)] = new_dir
            cwd.directories.append(new_dir)

        case[size, file_name]:
            cwd.files.append(File(file_name, int(size)))

part_one = sum(i.size for i in dir_map.values() if i.size <= MAX_DIR_SIZE)
print(f"Part One: {part_one}")

space_left = DISK_SPACE - root.size
part_two = sorted(i.size for i in dir_map.values() if space_left + i.size >= NEEDED_SPACE)[0]
print(f"Part Two: {part_two}")
