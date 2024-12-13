import re
from dataclasses import dataclass, replace
import sys
from typing import Self


@dataclass(slots=True)
class ClawMachine:
    button_a: tuple[int, int]
    button_b: tuple[int, int]
    prize: tuple[int, int]

    def min_winning_coins(self) -> int | None:
        (a11, a21), (a12, a22) = self.button_a, self.button_b
        b1, b2 = self.prize
        det = a11 * a22 - a21 * a12

        if det == 0:
            q, r = divmod(b1, a12)
            if r == 0:
                return q
        else:
            det1 = b1 * a22 - b2 * a12
            det2 = a11 * b2 - a21 * b1
            q1, r = divmod(det1, det)
            q2 = det2 // det
            if r == 0:
                return 3 * q1 + q2

        return None

    def corrected(self) -> Self:
        incr = 10_000_000_000_000
        corrected_prize = (self.prize[0] + incr, self.prize[1] + incr)
        return replace(self, prize=corrected_prize)


def read_input(file_path: str) -> list[ClawMachine]:
    with open(file_path) as f:
        s = f.read()
    p = re.compile(
        r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"
    )
    return [
        ClawMachine(
            button_a=(int(m[1]), int(m[2])),
            button_b=(int(m[3]), int(m[4])),
            prize=(int(m[5]), int(m[6])),
        )
        for m in p.finditer(s)
    ]


def main():
    file_path = sys.argv[1]
    machines = read_input(file_path)
    part_1 = sum(machine.min_winning_coins() or 0 for machine in machines)
    part_2 = sum(machine.corrected().min_winning_coins() or 0 for machine in machines)
    print(f"{part_1 = } {part_2 = }")


if __name__ == "__main__":
    main()
