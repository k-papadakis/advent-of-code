import re
import sys
from dataclasses import dataclass, field


def read_input(file_path: str) -> tuple[int, int, int, list[int]]:
    with open(file_path) as f:
        s = f.read()
    a, b, c, *program = map(int, re.findall(r"\d+", s))
    return a, b, c, program


@dataclass(slots=True)
class Computer:
    a: int
    b: int
    c: int
    program: list[int]
    instruction_pointer: int = 0
    out: list[int] = field(default_factory=list)

    def combo_operand(self, operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case 7:
                raise ValueError("Invalid legacy operand 7.")
            case _:
                raise ValueError(f"Invalid operand {operand}.")

    def execute_step(self) -> None:
        opcode = self.program[self.instruction_pointer]
        operand = self.program[self.instruction_pointer + 1]
        match opcode:
            case 0:
                self.a = self.a >> self.combo_operand(operand)
            case 1:
                self.b = self.b ^ operand
            case 2:
                self.b = self.combo_operand(operand) & 0b111
            case 3:
                if self.a != 0:
                    self.instruction_pointer = operand
                    return
            case 4:
                self.b = self.b ^ self.c
            case 5:
                self.out.append(self.combo_operand(operand) & 0b111)
            case 6:
                self.b = self.a >> self.combo_operand(operand)
            case 7:
                self.c = self.a >> self.combo_operand(operand)
            case _:
                raise ValueError(f"Invalid opcode {opcode}.")

        self.instruction_pointer += 2

    def execute_all(self) -> None:
        while self.instruction_pointer < len(self.program):
            self.execute_step()

    def execute_until_jump(self) -> None:
        while self.program[self.instruction_pointer] != 3:
            self.execute_step()

    def out_str(self) -> str:
        return ",".join(map(str, self.out))


def find_a(b: int, c: int, program: list[int]) -> int | None:
    # The input has the following properties:
    # The only pointer reset is at the final instruction,
    # and it always resets back to the first instruction.
    # Registers B and C on each iteration are expressions
    # that depend completely on the current value of register A.
    # A changes only at the end of each iteration,
    # by being shifted 3 bits to the right.
    # There is a single print on each iteration,
    # right before shifting A.
    stack = [(0, len(program) - 1)]
    min_a: int | None = None
    while stack:
        a, pos = stack.pop()
        if pos == -1:
            min_a = min(min_a, a) if min_a is not None else a
        for i in range(1 << 3):
            cand_a = (a << 3) | i
            computer = Computer(cand_a, b, c, program)
            computer.execute_until_jump()
            assert len(computer.out) == 1
            if computer.out[0] == program[pos]:
                stack.append((cand_a, pos - 1))
    return min_a


def main():
    file_path = sys.argv[1]
    a, b, c, program = read_input(file_path)

    computer = Computer(a, b, c, program)
    computer.execute_all()
    part_1 = computer.out_str()

    part_2 = find_a(b, c, program)

    print(f"part_1 = {part_1} part_2 = {part_2}")


if __name__ == "__main__":
    main()
