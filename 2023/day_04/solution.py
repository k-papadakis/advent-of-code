import re
from collections.abc import Generator, Iterable
from dataclasses import dataclass


@dataclass
class Card:
    id: int
    winning_numbers: set[int]
    numbers: list[int]

    @classmethod
    def from_string(cls, s: str) -> "Card":
        match = re.match(
            r"Card +(?P<id>\d+): +(?P<winning_numbers>.*?) +\| +(?P<numbers>.*)", s
        )
        if not match:
            raise ValueError("Could not match pattern.")

        card_id = int(match["id"])
        winning_numbers = set(map(int, match["winning_numbers"].split()))
        numbers = list(map(int, match["numbers"].split()))

        return cls(card_id, winning_numbers, numbers)

    def is_winning(self, x: int) -> bool:
        return x in self.winning_numbers

    def num_wins(self) -> int:
        return sum(self.is_winning(x) for x in self.numbers)

    def score(self) -> int:
        return 2 ** (n - 1) if (n := self.num_wins()) > 0 else 0


def read_input() -> Generator[Card, None, None]:
    with open("input.txt") as f:
        for line in f:
            yield Card.from_string(line.rstrip("\n"))


def total_score(cards: Iterable[Card]) -> int:
    return sum(card.score() for card in cards)


def total_cards(cards: Iterable[Card]) -> int:
    wins = [card.num_wins() for card in cards]
    n = len(wins)

    card_copies = [1] * n

    for i in range(n):
        for j in range(i + 1, i + wins[i] + 1):
            card_copies[j] += card_copies[i]

    return sum(card_copies)


def main():
    part_1 = total_score(read_input())
    part_2 = total_cards(read_input())

    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
