import re
import sys
from dataclasses import dataclass


def read_input(file_path: str):
    with open(file_path) as f:
        s = f.read()
    a, b, c, *program = map(int, re.findall(r"\d+", s))
    return a, b, c, program


@dataclass(slots=True)
class Computer:
    a: int
    b: int
    c: int
    out: list[int]
    program: list[int]
    instruction_pointer: int

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
                raise ValueError("Invalid legacy operand 7")
            case _:
                raise ValueError(f"Invalid operand {operand}")

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

    def out_str(self) -> str:
        return ",".join(map(str, self.out))


def main():
    file_path = sys.argv[1]
    a, b, c, program = read_input(file_path)
    computer = Computer(a, b, c, [], program, 0)
    computer.execute_all()
    print(computer.out_str())


if __name__ == "__main__":
    main()
