import re
from dataclasses import dataclass
from typing import NamedTuple


@dataclass
class BallCount:
    red: int = 0
    green: int = 0
    blue: int = 0


@dataclass
class Game:
    id: int
    reveals: list[BallCount]

    @staticmethod
    def from_string(data: str) -> "Game":
        game_str, reveals_str = data.split(":")
        game = Game(0, [])
        game.id = int(game_str.split()[1])
        for reveal_str in reveals_str.split(";"):
            reveal = BallCount()
            for ball_str in reveal_str.split(","):
                ball_str = ball_str.strip()
                count_str, name_str = ball_str.split()
                if name_str == "green":
                    reveal.green = int(count_str)
                elif name_str == "blue":
                    reveal.blue = int(count_str)
                elif name_str == "red":
                    reveal.red = int(count_str)
            game.reveals.append(reveal)
        return game

    def is_possible(self, count: BallCount) -> bool:
        for reveal in self.reveals:
            if reveal.red > count.red:
                return False
            if reveal.green > count.green:
                return False
            if reveal.blue > count.blue:
                return False
        return True


AVAILABLE = BallCount(12, 13, 14)


def main(filename: str) -> None:
    with open(filename, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
    acc = 0
    for line in lines:
        line = line.strip()
        game = Game.from_string(line)
        possible = game.is_possible(AVAILABLE)
        print(f"Possible: {possible} {game}")
        if possible:
            acc += game.id
    print(acc)


if __name__ == "__main__":
    main("input.txt")
    main("test.txt")
