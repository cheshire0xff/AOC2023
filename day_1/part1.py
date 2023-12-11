def main():
    with open("input.txt", mode="r", encoding="utf-8") as file:
        lines = file.readlines()
    acc = 0
    for line in lines:
        line = line.strip()
        first = ""
        last = ""
        for char in line:
            if char.isdigit():
                if not first:
                    first = char
                last = char
        calibration = int(first + last)
        acc += int(first + last)
        print(f"Extracted {calibration} from line '{line}'")
    print(acc)

if __name__ == "__main__":
    main()