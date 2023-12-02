import re
from dataclasses import dataclass


@dataclass
class GameReveal:
    red: int = 0
    green: int = 0
    blue: int = 0

    @classmethod
    def from_string(cls, reveal_str: str) -> "GameReveal":
        pattern = re.compile(r"(?P<num>\d+) (?P<color>red|green|blue)")
        init_kwargs = {
            m.group("color"): int(m.group("num"))
            for m in map(pattern.match, reveal_str.split(", "))
        }
        return cls(**init_kwargs)

    def power(self):
        return self.red * self.green * self.blue


@dataclass
class Game:
    id: int
    reveals: list[GameReveal]

    @classmethod
    def from_string(cls, game_str: str) -> "Game":
        game_id_str, reveals_str = re.match(r"Game (.*?): (.*)", game_str).groups()
        game_id = int(game_id_str)
        reveals = [
            GameReveal.from_string(reveal_str) for reveal_str in reveals_str.split("; ")
        ]

        return cls(id=game_id, reveals=reveals)

    def is_possible(self, max_red: int, max_green: int, max_blue: int) -> bool:
        res = all(
            reveal.red <= max_red
            and reveal.green <= max_green
            and reveal.blue <= max_blue
            for reveal in self.reveals
        )
        return res

    def min_possible_cubes(self):
        min_red = 0
        min_green = 0
        min_blue = 0

        for reveal in self.reveals:
            min_red = max(min_red, reveal.red)
            min_green = max(min_green, reveal.green)
            min_blue = max(min_blue, reveal.blue)

        return min_red, min_green, min_blue

    def min_possible_reveal(self):
        red, green, blue = self.min_possible_cubes()
        return GameReveal(red=red, green=green, blue=blue)

    def min_posible_power(self):
        return self.min_possible_reveal().power()


def read_data():
    with open("input.txt") as f:
        for line in f:
            yield Game.from_string(line.rstrip("\n"))


def main() -> None:
    part_1 = sum(
        game.id
        for game in read_data()
        if game.is_possible(max_red=12, max_green=13, max_blue=14)
    )
    part_2 = sum(game.min_posible_power() for game in read_data())

    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
