from bisect import insort, bisect
from dataclasses import dataclass
from itertools import combinations


@dataclass
class Galaxy:
    row: int
    column: int


def calc_distance(
    expanded_space: list[int], val1: int, val2: int, *, expansion: int
) -> int:
    smaller = min(val1, val2)
    larger = max(val1, val2)
    smaller_pos = bisect(expanded_space, smaller)
    if smaller_pos > len(expanded_space):
        # No expansion between these points.
        return larger - smaller
    larger_pos = bisect(expanded_space, larger)
    expansion = (larger_pos - smaller_pos) * expansion - (larger_pos - smaller_pos)
    return larger - smaller + expansion


def main(filename: str, expansion_rate: int) -> None:
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
        horizontal = calc_distance(
            empty_columns, galaxy1.column, galaxy2.column, expansion=expansion_rate
        )
        vertical = calc_distance(
            empty_rows, galaxy1.row, galaxy2.row, expansion=expansion_rate
        )
        acc += horizontal + vertical
    print(acc)


if __name__ == "__main__":
    main("input.txt", 1_000_000)
    main("test.txt", 100)
    main("test.txt", 10)
