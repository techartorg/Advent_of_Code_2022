from pathlib import Path
from operator import add, mul
from collections import deque
import math

inputs = Path(__file__.replace(".py", ".input")).read_text().split("\n\n")

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
                    lhs_s, op, rhs_s = op_val.split()[2:]

                    def f(w: int):
                        nonlocal lhs_s, op, rhs_s
                        lhs = w if lhs_s == "old" else int(lhs_s)
                        rhs = w if rhs_s == "old" else int(rhs_s)
                        return OPS[op](lhs, rhs)

                    self.operation = f

                case["Test", test_val]:
                    self.divisor = int(test_val.split()[-1])
                    self.test = lambda w: self._true if w % self.divisor == 0 else self._false

                case["If true", t_val]:
                    self._true = int(t_val.split()[-1])

                case["If false", f_val]:
                    self._false = int(f_val.split()[-1])

    def __repr__(self):
        return f"id: {self.id}, Inspected: {self.inspected} items: {self.items}"

    def inspect(self, div_3: bool, lcm: int | None = None) -> tuple[int, int]:
        self.inspected += 1
        item = self.items.popleft()
        item = self.operation(item)

        if div_3:
            item = item // 3

        if lcm:
            item %= lcm

        target = self.test(item)
        return target, item


def solve(part_two: bool) -> int:
    monkeys = [Monkey(i) for i in inputs]
    lcm = math.lcm(*[m.divisor for m in monkeys]) if part_two else None

    for _ in range(P2_ROUNDS if part_two else P1_ROUNDS):
        for m in monkeys:
            while len(m.items):
                target, item = m.inspect(not part_two, lcm)
                monkeys[target].items.append(item)

    monkeys = sorted(monkeys, key=lambda x: x.inspected, reverse=True)
    return math.prod(i.inspected for i in monkeys[:2])


print(f"Part One: {solve(False)}")
print(f"Part Two: {solve(True)}")
