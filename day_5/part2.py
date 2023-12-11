from typing import NamedTuple, Optional
from dataclasses import dataclass
import logging


class Mapping(NamedTuple):
    destination: int
    source: int
    range: int

    @staticmethod
    def from_line(line: str) -> "Mapping":
        nums = (int(num_str) for num_str in line.split())
        return Mapping(*nums)

    def try_get_dest(self, src: int) -> Optional[int]:
        if src >= self.source + self.range:
            return None
        if src < self.source:
            return None
        offset = src - self.source
        return self.destination + offset

    def try_get_src(self, dst: int) -> Optional[int]:
        if dst < self.destination:
            return None
        if dst >= self.destination + self.range:
            return None
        offset = dst - self.destination
        return self.source + offset


@dataclass
class Map:
    mappings: list[Mapping]
    prev: Optional["Map"]

    def get_mapped_value(self, index: int) -> int:
        if self.prev is not None:
            index = self.prev.get_mapped_value(index)
        for mapping in self.mappings:
            found_index = mapping.try_get_dest(index)
            if found_index is not None:
                logging.debug("Mapped %d -> %d, using %s", index, found_index, mapping)
                return found_index
        logging.debug("No mapping found for %d, using %s", index, self.mappings)
        return index

    def get_source(self, index: int) -> int:
        found = False
        for mapping in self.mappings:
            found_index = mapping.try_get_src(index)
            if found_index is not None:
                logging.debug(
                    "Got source of %d -> %d, using %s", index, found_index, mapping
                )
                index = found_index
                found = True
                break
        if not found:
            logging.debug("No mapping found for %d, using %s", index, self.mappings)
        if self.prev is not None:
            index = self.prev.get_source(index)
        return index


SeedsType = list[tuple[int, int]]
def get_seeds(line: str) -> SeedsType:
    _, nums_str = line.split(":")
    nums_str = nums_str.strip()
    nums = [int(num_str) for num_str in nums_str.split()]
    return list(zip(nums[::2], nums[1::2]))

def is_inrange(seed: int, seeds: SeedsType) -> bool:
    for start, offset in seeds:
        if seed >= start and seed < start + offset:
            return True
    return False

def main(filename: str) -> None:
    logging.basicConfig(level=logging.INFO)
    with open(filename, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    conversion_map: Optional[Map] = None
    for line in lines[1:]:
        if ":" in line:
            conversion_map = Map([], conversion_map)
        elif line:
            assert conversion_map is not None
            conversion_map.mappings.append(Mapping.from_line(line))
    seeds = get_seeds(lines[0])
    assert conversion_map is not None
    guess = 0
    while True:
        source = conversion_map.get_source(guess)
        if is_inrange(source, seeds):
            print(f"Guessed location {guess} can be achieved from seed {source} found in range!")
            return
        guess += 1


if __name__ == "__main__":
    main("input.txt")
    main("test.txt")
