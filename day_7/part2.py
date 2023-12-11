from enum import Enum
from bisect import insort


class HandType(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7


def get_card_value(card: str) -> int:
    if card.isdigit():
        return int(card)
    match card:
        case "T":
            return 10
        case "J":
            return 1
        case "Q":
            return 12
        case "K":
            return 13
        case "A":
            return 14
    raise RuntimeError(f"Unknown card: {card}!")


class Hand:
    def __str__(self) -> str:
        return (
            f"Hand(cards={self.cards}, hand_type={self.hand_type.name}, bid={self.bid})"
        )

    def __init__(self, cards: str, bid: int):
        self.cards = cards
        card_map: dict[str, int] = {}
        self.bid = bid
        for card in cards:
            if card not in card_map:
                card_map[card] = 0
            card_map[card] += 1
        wildcards = 0
        if "J" in card_map:
            wildcards = card_map["J"]
            card_map.pop("J")
        self.hand_type = HandType.HIGH_CARD
        counts: dict[int, int] = {}
        for card, count in card_map.items():
            if count == 0:
                continue
            if count not in counts:
                counts[count] = 0
            counts[count] += 1
        if wildcards == 5:
            self.hand_type = HandType.FIVE_OF_A_KIND
            return
        if wildcards != 0:
            largest_count = sorted(counts, reverse=True)[0]
            if largest_count + wildcards not in counts:
                counts[largest_count + wildcards] = 0
            counts[largest_count + wildcards] += 1
            counts[largest_count] -= 1
        if counts.get(5):
            self.hand_type = HandType.FIVE_OF_A_KIND
            return
        if counts.get(4):
            self.hand_type = HandType.FOUR_OF_A_KIND
            return
        if counts.get(2) == 1 and counts.get(3) == 1:
            self.hand_type = HandType.FULL_HOUSE
        elif counts.get(3) == 1:
            self.hand_type = HandType.THREE_OF_A_KIND
        elif counts.get(2) == 2:
            self.hand_type = HandType.TWO_PAIR
        elif counts.get(2) == 1:
            self.hand_type = HandType.ONE_PAIR

    def better_than(self, other: "Hand") -> bool:
        if self.hand_type.value > other.hand_type.value:
            return True
        elif self.hand_type.value < other.hand_type.value:
            return False
        for our_card, their_card in zip(self.cards, other.cards):
            if get_card_value(our_card) > get_card_value(their_card):
                return True
            if get_card_value(our_card) < get_card_value(their_card):
                return False
        return False

    def __ge__(self, other: "Hand") -> bool:
        if self.cards == other.cards:
            return True
        return self.better_than(other)

    def __le__(self, other: "Hand") -> bool:
        if self.cards == other.cards:
            return True
        return not self.better_than(other)

    def __gt__(self, other: "Hand") -> bool:
        return self.better_than(other)

    def __lt__(self, other: "Hand") -> bool:
        return not self.better_than(other)


def get_distance(hold_time: int, max_time: int) -> int:
    remaining = max_time - hold_time
    return remaining * hold_time


def parse(line: str) -> Hand:
    cards, bid_str = line.split()
    return Hand(cards, int(bid_str))


def main(filename: str) -> None:
    with open(filename, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    hands: list[Hand] = []
    for line in lines:
        hand = parse(line)
        insort(hands, hand)
    acc = 0
    for rank, hand in enumerate(hands, 1):
        print(hand)
        acc += rank * hand.bid
    print(acc)


if __name__ == "__main__":
    main("input.txt")
    main("test.txt")
