import math
import operator
import re
from dataclasses import dataclass
from typing import Literal, NamedTuple, Self


def safematch[T: (str, bytes)](pattern: re.Pattern[T], s: T) -> re.Match[T]:
    m = pattern.match(s)
    if not m:
        raise ValueError("Could not match pattern.")
    return m


xmas = {"x": 0, "m": 1, "a": 2, "s": 3}
op = {"<": operator.lt, ">": operator.gt}


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


MIN = 1
MAX = 4_000
DEFAULT = range(MIN, MAX + 1)


def split_lt(rn: range, c: int) -> tuple[range, range]:
    a, b = rn.start, rn.stop - 1
    if c < a < b:
        return range(0), rn
    elif a <= c <= b:
        return range(a, c), range(c + 1, b + 1)
    elif a < b < c:
        return rn, range(0)
    else:
        raise ValueError(rn, c)


def split_gt(rn: range, c: int) -> tuple[range, range]:
    p, q = split_lt(rn, c - 1)
    return q, p


class PartRange(NamedTuple):
    x: range = DEFAULT
    m: range = DEFAULT
    a: range = DEFAULT
    s: range = DEFAULT

    def combinations(self) -> int:
        return math.prod(map(len, self))

    def contains(self, part: Part) -> bool:
        return all(x in r for x, r in zip(part, self))


@dataclass
class Condition:
    var: Literal["x", "m", "a", "s"]
    op: Literal[">", "<"]
    val: int
    ret: str

    @classmethod
    def from_string(cls, condition_str: str) -> Self:
        condition_pattern = re.compile(
            r"(?P<var>x|m|a|s)(?P<op><|>)(?P<val>\d+):(?P<ret>\w+)"
        )

        m = safematch(condition_pattern, condition_str)

        return cls(m["var"], m["op"], int(m["val"]), m["ret"])  # type: ignore


@dataclass
class Workflow:
    name: str
    conditions: list[Condition]
    else_: str

    def process(self, part: Part) -> str:
        for c in self.conditions:
            if op[c.op](part[xmas[c.var]], c.val):
                return c.ret
        return self.else_

    @classmethod
    def from_string(cls, workflow_str: str) -> Self:
        workflow_pattern = re.compile(r"(?P<name>.*?)\{(?P<logic>.*?)\}")

        m = safematch(workflow_pattern, workflow_str)
        name = m["name"]
        *condition_strs, else_ = m["logic"].split(",")
        conditions = list(map(Condition.from_string, condition_strs))

        return cls(name, conditions, else_)


class System:
    __slots__ = ["workflows"]

    def __init__(self, workflows: list[Workflow]) -> None:
        self.workflows: dict[str, Workflow] = {w.name: w for w in workflows}

    def accepts(self, part: Part) -> bool:
        name = "in"
        while True:
            if name == "A":
                return True
            if name == "R":
                return False
            name = self.workflows[name].process(part)


def read_input(path: str) -> tuple[System, list[Part]]:
    with open(path) as f:
        s = f.read()

    workflows_str, parts_str = s.split("\n\n")

    workflows = list(map(Workflow.from_string, workflows_str.splitlines()))
    system = System(workflows)

    parts = list(map(Part.from_string, parts_str.splitlines()))

    return system, parts


path = "input.txt"
system, parts = read_input(path)
res = sum(sum(part) for part in parts if system.accepts(part))
print(res)
