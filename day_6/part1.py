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



def get_distance(hold_time: int, max_time: int) -> int:
    remaining = max_time - hold_time
    return remaining * hold_time


def parse(time_in: str, distance_in: str) -> list[Race]:
    _, times_str = time_in.split(":")
    times_str = times_str.strip()
    times = (int(time_str) for time_str in times_str.split())

    _, distances_str = distance_in.split(":")
    distances_str = distances_str.strip()
    distances = (int(distance_str) for distance_str in distances_str.split())

    result: list[Race] = []
    for time, distance in zip(times, distances):
        result.append(Race(time, distance))
    return result


def main(filename: str) -> None:
    with open(filename, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    races = parse(lines[0], lines[1])
    acc = 1
    for race in races:
        ways_to_win = race.count_ways_to_win()
        acc *= ways_to_win 
        print(f"Race {race} has {ways_to_win} ways to win.")
    print(races)
    print(acc)


if __name__ == "__main__":
    main("input.txt")
    main("test.txt")
