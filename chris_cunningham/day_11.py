from pathlib import Path
from operator import add, mul
from collections import deque

P1_ROUNDS = 20
P2_ROUNDS = 10_000
OPS = {'+': add, '*': mul}

class Monkey(object):
    def __init__(self, data: str):
        self.inspected = 0

        lines = data.splitlines()
        self.id = int(lines[0].split()[-1].replace(':', ''))

        for line in lines[1:]:
            match line.strip().split(':'):
                case["Starting items", items]:
                    self.items = deque([int(i) for i in items.replace(',', '').split()])

                case["Operation", op_val]:
                    _, _, lhs_s, op, rhs_s = op_val.split()

                    def f(w: int):
                        nonlocal lhs_s, op, rhs_s
                        lhs = w if lhs_s == "old" else int(lhs_s)
                        rhs = w if rhs_s == "old" else int(rhs_s)
                        self.inspected += 1
                        return OPS[op](lhs, rhs)

                    self.operation = f

                case["Test", test_val]:
                    self.test = lambda w: self._true if w % int(test_val.split()[-1]) == 0 else self._false

                case["If true", t_val]:
                    self._true = int(t_val.split()[-1])

                case["If false", f_val]:
                    self._false = int(f_val.split()[-1])

    def __repr__(self):
        return f"id: {self.id}, Inspected: {self.inspected} items: {self.items}"

inputs = Path(__file__.replace(".py", ".input")).read_text().split("\n\n")
_test = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1""".split("\n\n")

puzzle = [Monkey(i) for i in _test]

for i in range(P2_ROUNDS):
    if i == P1_ROUNDS:
        part_one = sorted(puzzle, key=lambda x: x.inspected, reverse=True)
        print(f"Part One: {part_one[0].inspected * part_one[1].inspected}")

    for m in puzzle:
        while len(m.items):
            item = m.items.popleft()
            item = m.operation(item)
            item = item // 3
            target = m.test(item)
            puzzle[target].items.append(item)

puzzle = sorted(puzzle, key=lambda x: x.inspected, reverse=True)
print(f"Part Two: {puzzle[0].inspected * puzzle[1].inspected}")
