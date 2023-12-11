from typing import Generator


def parse(line: str) -> tuple[str, tuple[str, str]]:
    key, value = line.split(" = ")
    value = value.strip("()")
    left, right = value.split(", ")
    return (key, (left, right))

def instruction_generator(inst: str) -> Generator[str, None, None]:
    instruction_counter = 0
    while True:
        yield inst[instruction_counter]
        instruction_counter += 1
        if instruction_counter >= len(inst):
            instruction_counter = 0

def main(filename: str) -> None:
    with open(filename, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    network: dict[str, tuple[str, str]] = {}
    for line in lines[2:]:
        key, value = parse(line)
        network[key] = value
    
    position = "AAA"
    generator = instruction_generator(lines[0])
    steps = 0
    while position != "ZZZ":
        steps += 1
        instruction = next(generator)
        value_index = 0
        if instruction == "R":
            value_index = 1
        position = network[position][value_index]
    print(steps)


if __name__ == "__main__":
    main("input.txt")
    main("test.txt")
