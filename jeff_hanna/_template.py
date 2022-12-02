# -*- coding: utf-8 -*-

"""

"""

from contextlib import suppress
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

def process_input(filename: str) -> list:
    filepath = Path(__file__).parent.joinpath(filename)
    raw_input = filepath.read_text().split("\n")

def run(filename: str) -> None:
    inputs = process_input(filename)


if __name__ == '__main__':
    run("day_02_input.txt")