import math
from typing import NamedTuple


class Race(NamedTuple):
    allowed_time: int
    record_distance: int

    def count_ways_to_win(self) -> int:
        count = 0
        for guess in range(1, self.allowed_time):
            if get_distance(guess, self.allowed_time) > self.record_distance:
                count += 1
        return count

    def count_ways_to_win_opt(self) -> int:
        first = 0
        last = 0
        # Distance formula:
        # y = x(M - x) - R
        # y = -x^2 + Mx - R
        # where:
        #   M - max time
        #   x - hold time
        #   R - record distance
        x1, x2 = get_solutions(-1, self.allowed_time, -self.record_distance)
        first = math.ceil(x1)
        last = math.floor(x2)
        return last - first + 1


def get_distance(hold_time: int, max_time: int) -> int:
    remaining = max_time - hold_time
    return remaining * hold_time


def get_discriminant(a: int, b: int, c: int) -> float:
    return b * b - 4 * a * c


def get_solutions(a: int, b: int, c: int) -> tuple[float, float]:
    disc_sqrt = math.sqrt(get_discriminant(a, b, c))
    assert disc_sqrt > 0 and a != 0
    x_1 = (-b + disc_sqrt) / (2 * a)
    x_2 = (-b - disc_sqrt) / (2 * a)
    return x_1, x_2


def parse(number_in: str) -> int:
    _, numbers_str = number_in.split(":")
    numbers_str = numbers_str.replace(" ", "")
    return int(numbers_str)



def main(filename: str) -> None:
    with open(filename, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    race = Race(parse(lines[0]), parse(lines[1]))
    ways_to_win = race.count_ways_to_win_opt()
    print(f"{race} has {ways_to_win} ways to win.")


if __name__ == "__main__":
    main("input.txt")
    main("test.txt")
