import re
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Part:
    x: int
    m: int
    a: int
    s: int

    def sum(self) -> int:
        return self.x + self.m + self.a + self.s


MIN = 1
MAX = 4_000


@dataclass(slots=True, frozen=True)
class PartRange:
    x: tuple[int, int] = (MIN, MAX)
    m: tuple[int, int] = (MIN, MAX)
    a: tuple[int, int] = (MIN, MAX)
    s: tuple[int, int] = (MIN, MAX)

    def __len__(self) -> int:
        return (
            (self.x[1] - self.x[0] + 1)
            * (self.m[1] - self.m[0] + 1)
            * (self.a[1] - self.a[0] + 1)
            * (self.s[1] - self.s[0] + 1)
        )

    def __contains__(self, part: Part) -> bool:
        return (
            self.x[0] <= part.x <= self.x[1]
            and self.m[0] <= part.m <= self.m[1]
            and self.a[0] <= part.a <= self.a[1]
            and self.s[0] <= part.s <= self.s[1]
        )


class Workflow:
    def __init__(self, name: str, logic_str: str) -> None:
        self.name = name
        self.logic_str = logic_str
        self.logic: list[tuple[PartRange, str]] = []

        pattern = re.compile(r"(x|m|a|s)(>|<)(\d+):(\w+)")
        *head, final = self.logic_str.split(",")

        for h in head:
            m = pattern.match(h)
            if not m:
                raise ValueError("Could not match pattern.")

            t, op_str, val_str, r = m.groups()
            val = int(val_str)

            if op_str == ">":
                rn = PartRange(**{t: (val + 1, MAX)})
            else:
                rn = PartRange(**{t: (MIN, val - 1)})

            self.logic.append((rn, r))

        self.logic.append((PartRange(), final))

    def process_part(self, part: Part) -> str:
        for rn, r in self.logic:
            if part in rn:
                return r
        return "error"


def read_input(path: str) -> tuple[dict[str, Workflow], list[Part]]:
    with open(path) as f:
        s = f.read()

    workflows_str, parts_str = s.split("\n\n")

    workflow_pattern = re.compile(r"(?P<name>.*?)\{(?P<logic>.*?)\}")
    system: dict[str, Workflow] = {}
    for workflow_str in workflows_str.splitlines():
        m = workflow_pattern.match(workflow_str)
        if not m:
            raise ValueError("Could not match pattern.")
        system[m["name"]] = Workflow(m["name"], m["logic"])

    part_pattern = re.compile(r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}")
    parts: list[Part] = []
    for part_str in parts_str.splitlines():
        m = part_pattern.match(part_str)
        if not m:
            raise ValueError("Could not match pattern.")
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
res = sum(part.sum() for part in parts if accepts(workflows, part))
print(res)
