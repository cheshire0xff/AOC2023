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
    
    def try_map(self, index: int) -> Optional[int]:
        if index >= self.source + self.range:
            return None
        if index < self.source:
            return None
        offset = index - self.source
        return self.destination + offset

@dataclass
class Map:
    mappings: list[Mapping]
    prev: Optional["Map"]

    def get_mapped_value(self, index: int) -> int:
        if self.prev is not None:
            index = self.prev.get_mapped_value(index)
        for mapping in self.mappings:
            if found := mapping.try_map(index):
                logging.debug("Mapped %d -> %d", index, found)
                return found
        logging.debug("No mapping found for %d", index)
        return index

def get_seeds(line: str) -> list[int]:
    _, nums = line.split(":")
    nums = nums.strip()
    return [int(num_str) for num_str in nums.split()]

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
    lowest: Optional[int] = None
    for seed in seeds:
        assert conversion_map is not None
        mapped = conversion_map.get_mapped_value(seed)
        print(f"Mapped {seed} -> {mapped}")
        if lowest is None:
            lowest = mapped
        else:
            lowest = min(lowest, mapped)
    print(f"Seeds: {seeds}")
    print(lowest)


if __name__ == "__main__":
    main("input.txt")
    main("test.txt")
