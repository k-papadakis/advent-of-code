import re
from collections.abc import Generator
from dataclasses import dataclass


def _assert_match(match: re.Match[str] | None) -> re.Match[str]:
    if not match:
        raise ValueError("Could not match pattern.")
    return match


@dataclass
class CubeSet:
    red: int = 0
    green: int = 0
    blue: int = 0

    @classmethod
    def from_string(cls, s: str) -> "CubeSet":
        pattern = re.compile(r"(?P<num>\d+) (?P<color>red|green|blue)$")
        init_kwargs = {
            m["color"]: int(m["num"])
            for m in map(_assert_match, map(pattern.match, s.split(", ")))
        }
        return cls(**init_kwargs)

    def power(self) -> int:
        return self.red * self.green * self.blue


@dataclass
class Game:
    id: int
    reveals: list[CubeSet]

    @classmethod
    def from_string(cls, s: str) -> "Game":
        game_id_str, reveals_str = _assert_match(
            re.match(r"Game (.*?): (.*)", s)
        ).groups()
        game_id = int(game_id_str)
        reveals = [
            CubeSet.from_string(reveal_str) for reveal_str in reveals_str.split("; ")
        ]

        return cls(id=game_id, reveals=reveals)

    def is_possible(self, red: int, green: int, blue: int) -> bool:
        res = all(
            reveal.red <= red and reveal.green <= green and reveal.blue <= blue
            for reveal in self.reveals
        )
        return res

    def minimal_bag_cubeset(self) -> CubeSet:
        red = 0
        green = 0
        blue = 0

        for reveal in self.reveals:
            red = max(red, reveal.red)
            green = max(green, reveal.green)
            blue = max(blue, reveal.blue)

        return CubeSet(red, green, blue)


def read_data() -> Generator[Game, None, None]:
    with open("input.txt") as f:
        for line in f:
            yield Game.from_string(line.rstrip("\n"))


def main() -> None:
    part_1 = sum(game.id for game in read_data() if game.is_possible(12, 13, 14))
    part_2 = sum(game.minimal_bag_cubeset().power() for game in read_data())

    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
