from operator import gt, lt
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


@dataclass(slots=True, frozen=True)
class Workflow:
    name: str
    logic: str

    def __call__(self, part: Part) -> str:
        *head, final = self.logic.split(",")
        pattern = re.compile(r"(x|m|a|s)(>|<)(\d+):(\w+)")

        for h in head:
            m = pattern.match(h)
            if not m:
                raise ValueError("Could not match pattern.")
            t, op_str, val_str, r = m.groups()
            op = gt if op_str == ">" else lt
            val = int(val_str)

            if op(getattr(part, t), val):
                return r

        return final
    

def read_input(path: str) -> tuple[dict[str, Workflow], list[Part]]:
    with open(path) as f:
        s = f.read()

    workflows_str, parts_str = s.split("\n\n")

    workflow_pattern = re.compile(r"(?P<name>.*?)\{(?P<logic>.*?)\}")
    workflows: dict[str, Workflow] = {}
    for workflow_str in workflows_str.splitlines():
        m = workflow_pattern.match(workflow_str)
        if not m:
            raise ValueError("Could not match pattern.")
        workflows[m["name"]] = Workflow(m["name"], m["logic"])

    part_pattern = re.compile(r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}")
    parts: list[Part] = []
    for part_str in parts_str.splitlines():
        m = part_pattern.match(part_str)
        if not m:
            raise ValueError("Could not match pattern.")
        parts.append(Part(*map(int, m.groups())))

    return workflows, parts



    
def accept(part: Part, workflows: dict[str, Workflow]) -> bool:
    cur = "in"
    while True:
        cur = workflows[cur](part)
        if cur == "R":
            return False
        if cur == "A":
            return True
        

        
path = "input.txt"
workflows, parts = read_input(path)
res = sum(part.sum() for part in parts if accept(part, workflows))
print(res)
