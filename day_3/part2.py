from dataclasses import dataclass
from typing import Callable, Optional


@dataclass(frozen=True)
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

    def adjacent_numbers(self, column: int, row: int) -> list[Number]:
        numbers: list[Number] = []
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
            if number := self.get_number(row + row_offset, column + column_offset):
                if number not in numbers:
                    numbers.append(number)
        return numbers
    
    def get_number(self, row: int, column: int) -> Optional[Number]:
        if not self.test(row, column, lambda x : x.isdigit()):
            return None
        number = Number([])
        number.characters.append(Character(row, column, self.lines[row][column]))
        # Try grow to the right.
        test_column = column
        while self.test(row, test_column + 1, lambda x : x.isdigit()):
            test_column += 1
            number.characters.append(Character(row, test_column, self.lines[row][test_column]))
        # Try grow to the left.
        test_column = column
        while self.test(row, test_column - 1, lambda x : x.isdigit()):
            test_column -= 1
            number.characters.insert(0, Character(row, test_column, self.lines[row][test_column]))
        return number

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
            if not value == "*":
                column += 1
                continue
            numbers = schematic.adjacent_numbers(column, row)
            column += 1
            gear_ratio = 0
            if len(numbers) == 2:
                gear_ratio = numbers[0].value() * numbers[1].value()
            acc += gear_ratio
            print(f"{gear_ratio}\t- {[str(number) for number in numbers]}")
    print(acc)


if __name__ == "__main__":
    main("input.txt")
    main("test.txt")
