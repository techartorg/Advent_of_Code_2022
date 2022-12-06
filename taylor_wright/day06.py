from pathlib import WindowsPath
from itertools import islice

input_path = WindowsPath(__file__).parent.parent / 'inputs/day06.txt'


def sliding_window(itr, window_size=4):
    vals = tuple(islice(itr, window_size))
    if len(vals) == window_size:
        yield vals
    for val in itr:
        vals = vals[1:] + (val,)
        yield vals


def solve(window_size: int) -> int:
    ind = window_size - 1
    input_iter = iter([line for line in input_path.read_text()])
    slide = sliding_window(input_iter, window_size=window_size)
    while slide:
        ind += 1
        if len(set(next(slide))) == window_size:
            return ind
    return -1


print('Part 01 answer: {}'.format(solve(4)))
print('Part 02 answer: {}'.format(solve(14)))
