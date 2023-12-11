from dataclasses import dataclass
from typing import Callable


@dataclass
class Character:
    row: int
    column: int
    value: str


@dataclass
class Number:
    characters: list[Character]

    def __str__(self) -> str:
        return f"Number({self.number_str()})"
    
    def number_str(self) -> str:
        return "".join(char.value for char in self.characters)

    def value(self) -> int:
        return int(self.number_str())



def is_symbol(char: str) -> bool:
    return not char.isdigit() and char != "."


@dataclass
class Schematic:
    lines: list[str]

    def adjacent_to_symbol(self, number: Number) -> bool:
        for char in number.characters:
            for column_offset, row_offset in (
                (-1, -1),
                (-1, 0),
                (-1, 1),
                (0, -1),
                (0, 1),
                (1, -1),
                (1, 0),
                (1, 1),
            ):
                if self.test(char.row + row_offset, char.column + column_offset, is_symbol):
                    return True
        return False

    def test(self, row: int, column: int, check: Callable[[str], bool]) -> bool:
        if row < 0 or row >= len(self.lines):
            return False
        if column < 0 or column >= len(self.lines[0]):
            return False
        return check(self.lines[row][column])


def main(filename: str) -> None:
    with open(filename, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
    acc = 0
    lines = [line.strip() for line in lines]
    schematic = Schematic(lines)
    for row, line in enumerate(lines):
        column = 0
        while column < len(line):
            value = line[column]
            if not value.isdigit():
                column += 1
                continue
            number = Number([])
            number.characters.append(Character(row, column, value))
            while schematic.test(row, column + 1, lambda x : x.isdigit()):
                column += 1
                number.characters.append(Character(row, column, line[column]))
            column += 1
            adjacent = schematic.adjacent_to_symbol(number)
            print(f"{adjacent} - {number} - {number.value()}")
            if adjacent:
                acc += number.value()
    print(acc)


if __name__ == "__main__":
    main("input.txt")
    main("test.txt")
