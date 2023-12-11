import math
from typing import NamedTuple


class Card(NamedTuple):
    winners: set[int]
    actual: set[int]
    id: int

    def points(self) -> int:
        common = self.winners.intersection(self.actual)
        winning_count = len(common)
        if winning_count == 0:
            return 0
        return int(math.pow(2, winning_count - 1))
        
    @staticmethod
    def parse_line(line: str) -> "Card":
        name_str, numbers_str = line.split(":")
        _, id_str = name_str.split()
        winners_str, actual_str = numbers_str.split("|")
        winners = set(int(num_str) for num_str in winners_str.strip().split())
        actual = set(int(num_str) for num_str in actual_str.strip().split())
        return Card(winners, actual, int(id_str))


def main(filename: str) -> None:
    with open(filename, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
    acc = 0
    lines = [line.strip() for line in lines]
    for line in lines:
        card = Card.parse_line(line)
        acc += card.points()
        print(card)
    print(acc)


if __name__ == "__main__":
    main("input.txt")
    main("test.txt")
