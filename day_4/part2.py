import math
from dataclasses import dataclass
from typing import NamedTuple, Optional


class Card(NamedTuple):
    winning_nums: set[int]
    actual: set[int]
    id: int

    def points(self) -> int:
        winning_count = self.winning_count()
        if winning_count == 0:
            return 0
        return int(math.pow(2, winning_count - 1))

    def winning_count(self) -> int:
        return len(self.winning_nums.intersection(self.actual))
        
    @staticmethod
    def parse_line(line: str) -> "Card":
        name_str, numbers_str = line.split(":")
        _, id_str = name_str.split()
        winners_str, actual_str = numbers_str.split("|")
        winners = set(int(num_str) for num_str in winners_str.strip().split())
        actual = set(int(num_str) for num_str in actual_str.strip().split())
        return Card(winners, actual, int(id_str))

@dataclass
class Game:
    all_cards: list[Card]

    def get_cards_won(self, card: Card) -> list[Card]:
        cards_won: list[Card] = []
        winning_count = card.winning_count()
        if winning_count == 0:
            return cards_won
        for offset in range(1, winning_count + 1):
            card_won = self.find_card(card.id + offset)
            cards_won.append(card_won)
            cards_won.extend(self.get_cards_won(card_won))
        return cards_won

    def find_card(self, card_id: int) -> Card:
        index = card_id - 1
        assert 0 <= index < len(self.all_cards), f"Attempting to find card with id {card_id} failed."
        return self.all_cards[index]



def main(filename: str) -> None:
    with open(filename, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    game = Game([])
    for line in lines:
        game.all_cards.append(Card.parse_line(line))


    acc = 0
    for card in game.all_cards:
        cards_won = game.get_cards_won(card)
        print(f"Card {card.id} won {len(cards_won)} cards")
        acc += len(cards_won)
    acc += len(game.all_cards)
    print(acc)

if __name__ == "__main__":
    main("input.txt")
    main("test.txt")
