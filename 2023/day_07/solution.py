from collections import Counter


def read_input(path: str) -> tuple[list[str], list[int]]:
    with open(path) as f:
        s = f.read()

    hands, bids = zip(*map(str.split, s.splitlines()))
    bids = list(map(int, bids))

    return hands, bids


def create_hands_key(use_j: bool):
    card_priority = {
        x: i for i, x in enumerate("J23456789TQKA" if use_j else "23456789TJQKA")
    }

    def hands_key(hand: str) -> tuple[list[int], list[int]]:
        c = Counter(hand)

        if use_j and "J" in c and len(c) > 1:
            js = c.pop("J")
            c[c.most_common(1)[0][0]] += js

        card_counts = sorted(c.values(), reverse=True)
        hand_priority = [card_priority[card] for card in hand]

        return card_counts, hand_priority

    return hands_key


def total_winnings(hands: list[str], bids: list[int], hands_key) -> int:
    res = sum(
        i * bid
        for i, (_, bid) in enumerate(
            sorted(zip(hands, bids), key=lambda t: hands_key(t[0])),
            start=1,
        )
    )
    return res


def main() -> None:
    hands, bids = read_input("input.txt")

    part_1 = total_winnings(hands, bids, create_hands_key(use_j=False))
    part_2 = total_winnings(hands, bids, create_hands_key(use_j=True))

    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
