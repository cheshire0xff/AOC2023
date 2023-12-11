import re
from typing import NamedTuple


DIGITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

class Token(NamedTuple):
    value: int
    raw: str

def tokenize(data: str) -> list[Token]:
    tokens = []
    pos = 0
    while pos < len(data):
        chunk = data[pos:]
        if match := re.search(r"^\d", chunk):
            tokens.append(Token(value=int(chunk[:match.end()]), raw=chunk[:match.end()]))
            pos += 1
            continue
        for name, value in DIGITS.items():
            if match := re.search(r"^" + name, chunk):
                tokens.append(Token(value=value, raw=chunk[:match.end()]))
                break
        pos += 1
    return tokens

def main(filename: str) -> None:
    with open(filename, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
    acc = 0
    for line in lines:
        line = line.strip()
        tokens = tokenize(line)
        assert tokens
        calibration = tokens[0].value * 10 + tokens[-1].value
        print(f"Extracted {calibration} from line '{line}'", tokens)
        acc += calibration
    print(acc)


if __name__ == "__main__":
    main("input.txt")
    main("test.txt")
