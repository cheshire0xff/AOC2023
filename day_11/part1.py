from bisect import insort, bisect
import re
from dataclasses import dataclass
from typing import NamedTuple
from itertools import combinations

@dataclass
class Galaxy:
    row: int
    column: int

def calc_distance(expanded_space: list[int], val1: int, val2: int) -> int:
    smaller = min(val1, val2)
    larger = max(val1, val2)
    smaller_pos = bisect(expanded_space, smaller)
    if smaller_pos > len(expanded_space):
        # No expansion between these points.
        return larger - smaller
    larger_pos = bisect(expanded_space, larger)
    expansion = (larger_pos - smaller_pos)
    # print(f"There are {expansion} points between {smaller} and {larger} inside {expanded_space}")
    return larger - smaller + expansion


    

def main(filename: str) -> None:
    with open(filename, mode="r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]
    empty_rows: list[int] = []
    galaxies: list[Galaxy] = []
    for row, line in enumerate(lines):
        row_empty = True
        for column, tile in enumerate(line):
            if tile == "#":
                row_empty = False
                galaxies.append(Galaxy(row, column))
        if row_empty:
            insort(empty_rows, row)

    empty_columns: list[int] = []
    for column in range(len(lines)):
        empty_column = True
        for row in range(len(lines[0])):
            if lines[row][column] == "#":
                empty_column = False
                break
        if empty_column:
            insort(empty_columns, column)

    acc = 0
    for galaxy1, galaxy2 in combinations(galaxies, 2):
        horizontal = calc_distance(empty_columns, galaxy1.column, galaxy2.column)
        vertical = calc_distance(empty_rows, galaxy1.row, galaxy2.row)
        acc += horizontal + vertical
    print(acc)



if __name__ == "__main__":
    main("input.txt")
    main("test.txt")
