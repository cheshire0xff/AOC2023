from dataclasses import dataclass
import math
from typing import Generator, NamedTuple, Optional


def parse(line: str) -> tuple[str, tuple[str, str]]:
    key, value = line.split(" = ")
    value = value.strip("()")
    left, right = value.split(", ")
    return (key, (left, right))


def instruction_generator(inst: str) -> Generator[tuple[str, int], None, None]:
    instruction_counter = 0
    while True:
        yield (inst[instruction_counter], instruction_counter)
        instruction_counter += 1
        if instruction_counter >= len(inst):
            instruction_counter = 0


class FinishInfo(NamedTuple):
    instruction_pos: int
    key: str


@dataclass
class Position:
    steps: int = 0
    repeated_at: Optional[int] = None


@dataclass
class ConcurrentRunner:
    def __init__(self, network: dict[str, tuple[str, str]], inst: str) -> None:
        self.network = network
        self.positions = [
            position for position in self.network if position.endswith("A")
        ]
        self.generator = instruction_generator(inst)

    def next_step(self) -> None:
        pass

    def finished(self) -> bool:
        return all(position.endswith("Z") for position in self.positions)

    def follow_through(self) -> None:
        steps_to_finish: dict[str, dict[FinishInfo, Position]] = {
            position: {} for position in self.positions
        }
        cur_pos: dict[str, str] = {position: position for position in self.positions}
        step = 0
        while True:
            step += 1
            inst, inst_counter = next(self.generator)
            value_index = 0 if inst == "L" else 1
            finished = True
            for value in steps_to_finish.values():
                if not value:
                    # Not all paths found finish step.
                    finished = False
                    break
                all_repeated = True
                for position in value.values():
                    if position.repeated_at is None:
                        all_repeated = False
                        break
                if not all_repeated:
                    finished = False
            if finished:
                break
            for start_pos, current_pos in cur_pos.items():
                new_pos = self.network[current_pos][value_index]
                # print(f"S: {start_pos} C: {current_pos} I: {inst} N: {new_pos}")
                cur_pos[start_pos] = new_pos
                if new_pos.endswith("Z"):
                    info = FinishInfo(inst_counter, new_pos)
                    if info in steps_to_finish[start_pos]:
                        if steps_to_finish[start_pos][info].repeated_at is None:
                            steps_to_finish[start_pos][info].repeated_at = step
                    else:
                        steps_to_finish[start_pos][info] = Position(step)
        step_finish_info: dict[str, dict[int, int]] = {}
        greatest: list[int] = []
        for start_pos, infos in steps_to_finish.items():
            for info, position in infos.items():
                assert position.repeated_at is not None
                greatest.append(position.steps)
        gcd = math.gcd(*greatest)
        mul_all = 1
        for start_pos, infos in steps_to_finish.items():
            print(f"start_pos: {start_pos}")
            step_finish_info[start_pos] = {}
            for info, position in infos.items():
                assert position.repeated_at is not None
                print(f"\tPre division {info} {position}")
                position.repeated_at = position.repeated_at // gcd
                position.steps = position.steps // gcd
                mul_all *= position.steps
                print(f"\t{info} {position}")
                step_finish_info[start_pos][position.steps] = position.repeated_at - position.steps
                print(f"\tFinish starts at {position.steps} and repeats every {position.repeated_at - position.steps}")
        print("mull_all", mul_all)
        print("mull_all * gcd", mul_all * gcd)
        
def main(filename: str) -> None:
    with open(filename, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    network: dict[str, tuple[str, str]] = {}
    for line in lines[2:]:
        key, value = parse(line)
        network[key] = value

    runner = ConcurrentRunner(network, lines[0])
    runner.follow_through()


if __name__ == "__main__":
    main("input.txt")
#    main("test2.txt")
