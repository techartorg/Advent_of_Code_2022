from itertools import tee, islice
from typing import Iterable, Iterator, TypeVar


T = TypeVar('T')


def window(iterable: Iterable[T], n: int) -> Iterator[tuple[T, ...]]:
    slices = (islice(it, i, None) for i, it in enumerate(tee(iterable, n)))
    return zip(*slices)
