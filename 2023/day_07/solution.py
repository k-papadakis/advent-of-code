from collections import Counter
from enum import IntEnum, auto
from functools import cached_property


class HandType(IntEnum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()


class Hand:
    card_pool = "A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"

    def __init__(self, cards: str, bid: int):
        assert len(cards) == 5 and set(cards) <= set(self.card_pool)
        assert bid >= 0
        self.cards = cards
        self.bid = bid

    @cached_property
    def type(self) -> HandType:
        # counter: dict[str, int] = dict.fromkeys(self.card_pool, 0)
        # for card in self.cards:
        #     counter[card] += 1
        match sorted(Counter(self.cards).values()):
            case [1, 1, 1, 1, 1]:
                return HandType.HIGH_CARD
            case [2, 1, 1, 1]:
                return HandType.ONE_PAIR
            case [2, 2, 1]:
                return HandType.ONE_PAIR
            case [3, 1, 1]:
                return HandType.THREE_OF_A_KIND
            case [3, 2]:
                return HandType.FULL_HOUSE
            case [4, 1]:
                return HandType.FOUR_OF_A_KIND
            case [5]:
                return HandType.FIVE_OF_A_KIND
            case _:
                raise ValueError(f"Could not match hand type for cards {self.cards}.")

    # def __eq__self()


def read_input() -> tuple[list[str], list[int]]:
    with open("input.txt") as f:
        s = f.read()
    hands, bids = zip(*map(str.split, s.splitlines()))
    bids = list(map(int, bids))
    return hands, bids


def card_counts(cards: str) -> list[int]:
    return sorted(Counter(cards).values())


CARD_PRIORITY = {x: i for i, x in enumerate("23456789TJQKA")}


def hands_comparison_key(hand: str):
    card_counts = sorted(Counter(hand).values(), reverse=True)
    hand_priority = [CARD_PRIORITY[card] for card in hand]
    return card_counts, hand_priority


def main():
    hands, bids = read_input()
    part_1 = sum(
        i * bid
        for i, (_, bid) in enumerate(
            sorted(
                zip(
                    hands,
                    bids,
                ),
                key=lambda t: hands_comparison_key(t[0]),
            ),
            1,
        )
    )

    print(f"{part_1 = }")


if __name__ == "__main__":
    main()
