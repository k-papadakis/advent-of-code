import math
import re
from typing import Iterator, NamedTuple


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


MIN = 1
MAX = 4_000
DEFAULT = range(MIN, MAX + 1)


def split_range(splittee: range, splitter: range) -> tuple[range, range, range]:
    a, b = splittee.start, splittee.stop - 1
    c, d = splitter.start, splitter.stop - 1

    s, t = max(a, c), min(b, d)

    if s <= t:
        return range(a, s), range(s, t + 1), range(t + 1, b + 1)
    else:
        return range(a, t + 1), range(0), range(s, b + 1)


class PartRange(NamedTuple):
    x: range = DEFAULT
    m: range = DEFAULT
    a: range = DEFAULT
    s: range = DEFAULT

    def combinations(self) -> int:
        return math.prod(map(len, self))

    def contains(self, part: Part) -> bool:
        return all(x in r for x, r in zip(part, self))


class Workflow:
    logic_pattern = re.compile(r"(x|m|a|s)(>|<)(\d+):(\w+)")

    def __init__(self, name: str, logic_str: str) -> None:
        self.name = name
        self.logic_str = logic_str
        self.logic = list(self._iter_logic())

    def _iter_logic(self) -> Iterator[tuple[PartRange, str]]:
        *head, else_ret = self.logic_str.split(",")

        for h in head:
            m = safematch(self.logic_pattern, h)
            if_var, op_str, val_str, ret = m.groups()
            thresh = int(val_str)

            rn = range(thresh + 1, MAX + 1) if op_str == ">" else range(MIN, thresh)
            yield PartRange(**{if_var: rn}), ret

        yield PartRange(), else_ret

    def process_part(self, part: Part) -> str:
        return next(r for rn, r in self.logic if rn.contains(part))


def read_input(path: str) -> tuple[dict[str, Workflow], list[Part]]:
    with open(path) as f:
        s = f.read()

    workflows_str, parts_str = s.split("\n\n")

    workflow_pattern = re.compile(r"(?P<name>.*?)\{(?P<logic>.*?)\}")
    system: dict[str, Workflow] = {}
    for workflow_str in workflows_str.splitlines():
        m = safematch(workflow_pattern, workflow_str)
        system[m["name"]] = Workflow(m["name"], m["logic"])

    part_pattern = re.compile(r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}")
    parts: list[Part] = []
    for part_str in parts_str.splitlines():
        m = safematch(part_pattern, part_str)
        parts.append(Part(*map(int, m.groups())))

    return system, parts


def accepts(system: dict[str, Workflow], part: Part) -> bool:
    cur = "in"
    while True:
        cur = system[cur].process_part(part)
        if cur == "R":
            return False
        if cur == "A":
            return True


path = "input.txt"
workflows, parts = read_input(path)
res = sum(sum(part) for part in parts if accepts(workflows, part))
print(res)
