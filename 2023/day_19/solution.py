import math
import re
from dataclasses import dataclass
from typing import Generator, Iterator, Literal, NamedTuple, Self

type Xmas = Literal["x", "m", "a", "s"]
type Op = Literal["<", ">"]

XMAS = {"x": 0, "m": 1, "a": 2, "s": 3}


def safematch[T: (str, bytes)](pattern: re.Pattern[T], s: T) -> re.Match[T]:
    m = pattern.match(s)
    if not m:
        raise ValueError("Could not match pattern.")
    return m


class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int

    @classmethod
    def from_string(cls, part_str: str) -> Self:
        part_pattern = re.compile(r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}")
        m = safematch(part_pattern, part_str)
        return cls(*map(int, m.groups()))


def split_lt(rn: range, val: int) -> tuple[range, range]:
    a, b = rn.start, rn.stop - 1

    if val < a < b:
        accepted, rejected = range(0), rn
    elif a <= val <= b:
        accepted, rejected = range(a, val), range(val, b + 1)
    elif a < b < val:
        accepted, rejected = rn, range(0)
    else:
        raise ValueError(a, b, val)

    return accepted, rejected


def split_gt(rn: range, val: int) -> tuple[range, range]:
    p, q = split_lt(rn, val + 1)
    return q, p


class PartRange(NamedTuple):
    x: range
    m: range
    a: range
    s: range

    def size(self) -> int:
        return math.prod(map(len, self))

    def split(self, var: Xmas, val: int, op: Op) -> tuple[Self, Self]:
        rn = self[XMAS[var]]

        if op == "<":
            accepted_range, rejected_range = split_lt(rn, val)
        elif op == ">":
            accepted_range, rejected_range = split_gt(rn, val)
        else:
            raise ValueError(f"Invalid op {op}")

        accepted_part_range = self._replace(**{var: accepted_range})
        rejected_part_range = self._replace(**{var: rejected_range})

        return accepted_part_range, rejected_part_range


@dataclass(slots=True)
class Condition:
    var: Xmas
    op: Op
    val: int
    ret: str

    def is_valid(self, x: int) -> bool:
        if self.op == "<":
            return x < self.val
        elif self.op == ">":
            return x > self.val
        else:
            raise ValueError(f"Invalid op: {self.op}")

    @classmethod
    def from_string(cls, condition_str: str) -> Self:
        condition_pattern = re.compile(
            r"(?P<var>x|m|a|s)(?P<op><|>)(?P<val>\d+):(?P<ret>\w+)"
        )

        m = safematch(condition_pattern, condition_str)

        return cls(m["var"], m["op"], int(m["val"]), m["ret"])  # type: ignore


@dataclass(slots=True)
class Workflow:
    name: str
    conditions: list[Condition]
    else_: str

    def process_part(self, part: Part) -> str:
        return next(
            (c.ret for c in self.conditions if c.is_valid(part[XMAS[c.var]])),
            self.else_,
        )

    def process_part_range(
        self, part_range: PartRange, condition_index: int = 0
    ) -> Iterator[tuple[PartRange, str]]:
        if condition_index < len(self.conditions):
            c = self.conditions[condition_index]
            accepted, rejected = part_range.split(c.var, c.val, c.op)

            if accepted:
                yield accepted, c.ret

            if rejected:
                yield from self.process_part_range(
                    rejected, condition_index=condition_index + 1
                )
        else:
            yield part_range, self.else_

    @classmethod
    def from_string(cls, workflow_str: str) -> Self:
        workflow_pattern = re.compile(r"(?P<name>.*?)\{(?P<logic>.*?)\}")

        m = safematch(workflow_pattern, workflow_str)
        name = m["name"]
        *condition_strs, else_ = m["logic"].split(",")
        conditions = list(map(Condition.from_string, condition_strs))

        return cls(name, conditions, else_)


class System:
    def __init__(self, workflows: list[Workflow]) -> None:
        self.workflows: dict[str, Workflow] = {w.name: w for w in workflows}

    def accepts_part(self, part: Part, name: str = "in") -> bool:
        if name == "A":
            return True
        if name == "R":
            return False

        next_name = self[name].process_part(part)
        return self.accepts_part(part, next_name)

    def accepted_part_ranges(
        self, part_range: PartRange, name: str = "in"
    ) -> Generator[PartRange, None, None]:
        if name == "A":
            yield part_range
            return

        if name == "R":
            return

        for next_part_range, next_name in self[name].process_part_range(part_range):
            yield from self.accepted_part_ranges(next_part_range, next_name)

    def __getitem__(self, key: str) -> Workflow:
        return self.workflows[key]


def read_input(path: str) -> tuple[System, list[Part]]:
    with open(path) as f:
        s = f.read()

    workflows_str, parts_str = s.split("\n\n")

    workflows = list(map(Workflow.from_string, workflows_str.splitlines()))
    system = System(workflows)

    parts = list(map(Part.from_string, parts_str.splitlines()))

    return system, parts


def main():
    path = "input.txt"

    system, parts = read_input(path)

    part_1 = sum(sum(part) for part in parts if system.accepts_part(part))

    part_range = PartRange(
        range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001)
    )
    part_2 = sum(
        part_range.size() for part_range in system.accepted_part_ranges(part_range)
    )

    print(f"{part_1 = }, {part_2}")


if __name__ == "__main__":
    main()
