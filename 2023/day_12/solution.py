# Props to this: https://alexoxorn.github.io/posts/aoc-day12-regular_languages/

from collections import defaultdict
from collections.abc import Generator, Sequence
from dataclasses import dataclass
from enum import StrEnum
from itertools import repeat


class Symbol(StrEnum):
    UNBROKEN = "."
    BROKEN = "#"
    UNKNOWN = "?"


def read_input(
    path: str, unfold: int = 1
) -> Generator[tuple[str, list[int]], None, None]:
    """Yields a symbol sequence and a pattern, for each line in the file at `path`."""
    with open(path) as f:
        for line in f:
            string, pattern_str = line.split()
            pattern = list(map(int, pattern_str.split(",")))
            if unfold > 1:
                string = "?".join(repeat(string, unfold))
                pattern = pattern * unfold
            yield string, pattern


@dataclass(slots=True)
class State:
    """Points to positions of other states in a StateMachine."""

    unbroken: int | None = None
    broken: int | None = None


class StateMachine(Sequence[State]):
    def __init__(self, pattern: Sequence[int]) -> None:
        self.pattern = pattern
        self.states: list[State] = [State() for _ in range(len(self))]
        self._connect_states()

    def __getitem__(self, index: int):  # type: ignore
        """Returns the state at `index`"""
        return self.states[index]

    def __len__(self) -> int:
        """Returns the number of states"""
        return sum(self.pattern) + len(self.pattern)

    def _connect_states(self) -> None:
        """Connects the states according to the rules of `pattern`."""
        # (Initial) either state
        self[0].unbroken = 0
        self[0].broken = 1

        i = 1
        for num_broken in self.pattern:
            # broken states
            for _ in range(num_broken - 1):
                self[i].broken = i + 1
                i += 1

            if i < len(self) - 2:  # not the end of the final broken-chain
                # unbroken state
                self[i].unbroken = i + 1
                i += 1
                # either state
                self[i].unbroken = i
                self[i].broken = i + 1

            i += 1

        # (Final) unbroken state
        self[len(self) - 1].unbroken = len(self) - 1

    def move(self, heads: dict[int, int], symbol: Symbol) -> dict[int, int]:
        """Move the heads by feeding `symbol` to the state machine."""
        new_heads: dict[int, int] = defaultdict(int)

        for i, n in heads.items():
            if symbol != Symbol.BROKEN and self[i].unbroken is not None:
                new_heads[self[i].unbroken] += n  # type: ignore
            if symbol != Symbol.UNBROKEN and self[i].broken is not None:
                new_heads[self[i].broken] += n  # type: ignore

        return new_heads

    def num_matches(self, string: str) -> int:
        """Find the number of possible pattern matches,
        if we were to replace Symbol.UKNOWN with a different Symbol
        """
        symbols = [Symbol(s) for s in string]
        # Number of heads at a state's index
        heads: dict[int, int] = {0: 1}
        for symbol in symbols:
            heads = self.move(heads, symbol)
        return heads[len(self.states) - 1]


def main() -> None:
    """Main function."""
    path = "input.txt"
    part_1 = sum(
        StateMachine(pattern).num_matches(s) for s, pattern in read_input(path)
    )
    part_2 = sum(
        StateMachine(pattern).num_matches(s)
        for s, pattern in read_input(path, unfold=5)
    )

    print(f"{part_1 = }, {part_2 = }")


if __name__ == "__main__":
    main()
