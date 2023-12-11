from typing import NamedTuple


GOES_NORTH = ("|", "L", "J", "S")
GOES_SOUTH = ("|", "F", "7", "S")
GOES_EAST = ("-", "L", "F", "S")
GOES_WEST = ("-", "7", "J", "S")

class Position(NamedTuple):
    row: int
    column: int

class Field:
    def __init__(self, field: list[str]) -> None:
        self.field = field
        self.start_pos = self.find_s()

    def find_s(self) -> Position:
        for row, line in enumerate(self.field):
            for column, value in enumerate(line):
                if value == "S":
                    return Position(row, column)
        assert False
    
    def go(self) -> None:
        print(f"Starting from {self.start_pos}")
        pos1, pos2 = self.available_directions(self.start_pos)
        prev1 = self.start_pos
        prev2 = self.start_pos
        steps = 1
        while True:
            steps += 1
            next1 = self._next(prev1, pos1)
            print(f"Moving from {pos1} to {next1}")
            if next1 == pos2:
                break
            prev1 = pos1
            pos1 = next1

            next2 = self._next(prev2, pos2)
            print(f"Moving from {pos2} to {next2}")
            if next2 == pos1:
                break
            prev2 = pos2
            pos2 = next2
        print(f"Took {steps} steps.")

    def _next(self, prev: Position, current: Position) -> Position:
        pos1, pos2 = self.available_directions(current)
        if pos1 == prev:
            return pos2
        return pos1

    
    
    def available_directions(self, pos: Position) -> tuple[Position, Position]:
        # test north
        dirs: list[Position] = []

        value = self.try_get_value(pos)

        if value in GOES_NORTH:
            test_pos = Position(pos.row - 1, pos.column)
            north = self.try_get_value(test_pos)
            if north in GOES_SOUTH:
                dirs.append(test_pos)

        if value in GOES_SOUTH:
            test_pos = Position(pos.row + 1, pos.column)
            south = self.try_get_value(test_pos)
            if south in GOES_NORTH:
                dirs.append(test_pos)

        if value in GOES_EAST:
            test_pos = Position(pos.row, pos.column + 1)
            east = self.try_get_value(test_pos)
            if east in GOES_WEST:
                dirs.append(test_pos)

        if value in GOES_WEST:
            test_pos = Position(pos.row, pos.column - 1)
            west = self.try_get_value(test_pos)
            if west in GOES_EAST:
                dirs.append(test_pos)
        assert len(dirs) == 2, f"Available positions not 2: {dirs}, from {pos}"
        return (dirs[0], dirs[1])
    
    def try_get_value(self, pos: Position) -> str:
        if pos.column >= len(self.field[0]) or pos.column < 0:
            return ""
        if pos.row >= len(self.field) or pos.row < 0:
            return ""
        return self.field[pos.row][pos.column]


def main(filename: str) -> None:
    with open(filename, mode="r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]
    field = Field(lines)
    field.go()


if __name__ == "__main__":
    main("input.txt")
    main("test.txt")
