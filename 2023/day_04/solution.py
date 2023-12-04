import re
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
            raise ValueError("Could not match pattern")

        card_id = int(match["id"])
        winning_numbers = set(map(int, match["winning_numbers"].split()))
        numbers = list(map(int, match["numbers"].split()))

        return cls(card_id, winning_numbers, numbers)

    def score(self) -> int:
        num_winners = sum(x in self.winning_numbers for x in self.numbers)
        return 2 ** (num_winners - 1) if num_winners > 0 else 0


def read_input():
    with open("input.txt") as f:
        for line in f:
            yield Card.from_string(line.rstrip("\n"))


def main():
    part_1 = sum(card.score() for card in read_input())

    print(f"{part_1 = }")


if __name__ == "__main__":
    main()
