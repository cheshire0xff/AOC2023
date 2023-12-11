from dataclasses import dataclass
from enum import Enum
import io
from typing import NamedTuple, Optional
import colorama


GOES_NORTH = ("|", "L", "J", "S")
GOES_SOUTH = ("|", "F", "7", "S")
GOES_EAST = ("-", "L", "F", "S")
GOES_WEST = ("-", "7", "J", "S")


class Position(NamedTuple):
    row: int
    column: int


@dataclass
class Tile:
    value: str
    main_loop: bool = False
    right_infect = False
    left_infect = False


class Direction(Enum):
    SOUTH = 1
    NORTH = 2
    WEST = 3
    EAST = 4


class Field:
    def __init__(self, field: list[str]) -> None:
        self.tiles: list[list[Tile]] = []
        for row, line in enumerate(field):
            self.tiles.append([])
            for _, value in enumerate(line):
                self.tiles[row].append(Tile(value))

        self.start_pos = self.find_s()
        self.mark_as_main(self.start_pos)
        self.right_tiles: set[Position] = set()
        self.right_infected = 0
        self.left_tiles: set[Position] = set()
        self.left_infected = 0

    def find_s(self) -> Position:
        for row, line in enumerate(self.tiles):
            for column, tile in enumerate(line):
                if tile.value == "S":
                    return Position(row, column)
        assert False

    def infect(self) -> None:
        reached_end = False
        for position in self.right_tiles:
            reached_end = self.infect_neighbors(position, True)
        if not reached_end:
            print("Right infected count:", self.right_infected)
            return
        for position in self.left_tiles:
            reached_end = self.infect_neighbors(position, False)
        assert not reached_end
        print("Left infected count:", self.left_infected)

    def infect_neighbors(self, position: Position, right: bool) -> bool:
        tile = self.try_get_value(position)
        if tile is None:
            return True
        if tile.main_loop:
            return False
        if tile.left_infect or tile.right_infect:
            return False
        if right:
            self.right_infected += 1
            tile.right_infect = True
        else:
            self.left_infected += 1
            tile.left_infect = True

        for row_offset, column_offset in (
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
        ):
            new_pos = Position(
                position.row + row_offset, position.column + column_offset
            )
            if self.infect_neighbors(new_pos, right):
                return True
        return False

    def go(self) -> None:
        print(f"Starting from {self.start_pos}")
        pos1, _ = self.available_directions(self.start_pos)
        self.mark_as_main(pos1)
        prev1 = self.start_pos
        while True:
            direction = self.get_direction(prev1, pos1)
            tile = self.try_get_value(prev1)
            assert tile is not None
            if direction == Direction.EAST:
                # We go east, right tile is south.
                for pos in (prev1, pos1):
                    self.right_tiles.add(Position(pos.row + 1, pos.column))
                    self.left_tiles.add(Position(pos.row - 1, pos.column))
            elif direction == Direction.WEST:
                # We go west, right tile is north.
                for pos in (prev1, pos1):
                    self.right_tiles.add(Position(pos.row - 1, pos.column))
                    self.left_tiles.add(Position(pos.row + 1, pos.column))
            elif direction == Direction.SOUTH:
                # We go south, right tile is west.
                for pos in (prev1, pos1):
                    self.right_tiles.add(Position(pos.row, pos.column - 1))
                    self.left_tiles.add(Position(pos.row, pos.column + 1))
            elif direction == Direction.NORTH:
                for pos in (prev1, pos1):
                    self.right_tiles.add(Position(pos.row, pos.column + 1))
                    self.left_tiles.add(Position(pos.row, pos.column - 1))
            next1 = self._next(prev1, pos1)
            self.mark_as_main(next1)
            if next1 == self.start_pos:
                break
            prev1 = pos1
            pos1 = next1

    def mark_as_main(self, position: Position) -> None:
        tile = self.try_get_value(position)
        assert tile is not None
        tile.main_loop = True

    def _next(self, prev: Position, current: Position) -> Position:
        pos1, pos2 = self.available_directions(current)
        next_pos = pos1
        if pos1 == prev:
            next_pos = pos2
        return next_pos

    def print(self) -> None:
        stream = io.StringIO()
        for row in self.tiles:
            for tile in row:
                if tile.value == "S":
                    stream.write(
                        f"{colorama.Fore.YELLOW}{tile.value}{colorama.Fore.RESET}"
                    )
                elif tile.main_loop:
                    stream.write(
                        f"{colorama.Fore.RED}{tile.value}{colorama.Fore.RESET}"
                    )
                elif tile.left_infect:
                    stream.write(
                        f"{colorama.Fore.GREEN}{tile.value}{colorama.Fore.RESET}"
                    )
                elif tile.right_infect:
                    stream.write(
                        f"{colorama.Fore.BLUE}{tile.value}{colorama.Fore.RESET}"
                    )
                else:
                    stream.write(tile.value)
            stream.write("\n")

        print(stream.getvalue(), end="\n")

    @staticmethod
    def get_direction(prev: Position, new: Position) -> Direction:
        # row0 | prev
        # row1 V new
        if new.row > prev.row:
            return Direction.SOUTH
        # row0 ^ new
        # row1 | prev
        if prev.row > new.row:
            return Direction.NORTH
        # 0 1
        # ->
        if new.column > prev.column:
            return Direction.EAST
        return Direction.WEST

    def available_directions(self, pos: Position) -> tuple[Position, Position]:
        # test north
        dirs: list[Position] = []

        tile = self.try_get_value(pos)
        assert tile is not None

        if tile.value in GOES_NORTH:
            test_pos = Position(pos.row - 1, pos.column)
            north = self.try_get_value(test_pos)
            assert north is not None
            if north.value in GOES_SOUTH:
                dirs.append(test_pos)

        if tile.value in GOES_SOUTH:
            test_pos = Position(pos.row + 1, pos.column)
            south = self.try_get_value(test_pos)
            assert south is not None
            if south.value in GOES_NORTH:
                dirs.append(test_pos)

        if tile.value in GOES_EAST:
            test_pos = Position(pos.row, pos.column + 1)
            east = self.try_get_value(test_pos)
            assert east is not None
            if east.value in GOES_WEST:
                dirs.append(test_pos)

        if tile.value in GOES_WEST:
            test_pos = Position(pos.row, pos.column - 1)
            west = self.try_get_value(test_pos)
            assert west is not None
            if west.value in GOES_EAST:
                dirs.append(test_pos)
        assert len(dirs) == 2, f"Available positions not 2: {dirs}, from {pos}"
        return (dirs[0], dirs[1])

    def try_get_value(self, pos: Position) -> Optional[Tile]:
        if pos.column >= len(self.tiles[0]) or pos.column < 0:
            return None
        if pos.row >= len(self.tiles) or pos.row < 0:
            return None
        return self.tiles[pos.row][pos.column]


def main(filename: str) -> None:
    with open(filename, mode="r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]
    field = Field(lines)
    field.go()
    field.infect()
    field.print()


if __name__ == "__main__":
    main("input.txt")
    main("test.txt")
