from collections import Counter


def read_input(path: str) -> tuple[list[str], list[int]]:
    with open(path) as f:
        s = f.read()

    hands, bids = zip(*map(str.split, s.splitlines()))
    bids = list(map(int, bids))

    return hands, bids


def hands_comparison_key_1(hand: str):
    card_priority = {x: i for i, x in enumerate("23456789TJQKA")}

    card_counts = sorted(Counter(hand).values(), reverse=True)

    hand_priority = [card_priority[card] for card in hand]

    return card_counts, hand_priority


def hands_comparison_key_2(hand: str):
    card_priority = {x: i for i, x in enumerate("J23456789TQKA")}

    c = Counter(hand)
    if "J" in c and len(c) > 1:
        js = c.pop("J")
        c[c.most_common(1)[0][0]] += js
    card_counts = sorted(c.values(), reverse=True)

    hand_priority = [card_priority[card] for card in hand]

    return card_counts, hand_priority


def total_winnings(hands, bids, hands_comparison_key):
    res = sum(
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
    return res


def main():
    hands, bids = read_input("input.txt")

    part_1 = total_winnings(hands, bids, hands_comparison_key_1)
    part_2 = total_winnings(hands, bids, hands_comparison_key_2)

    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
