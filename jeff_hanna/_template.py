# -*- coding: utf-8 -*-

"""

"""

from contextlib import suppress
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

def process_input(filename: str):
    filepath = Path(__file__).parent.joinpath(filename)
    raw_input = filepath.read_text().split("\n")

def run() -> None:
    inputs = process_input("day_##_input.txt")


if __name__ == '__main__':
    run()