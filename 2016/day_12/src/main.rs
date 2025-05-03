use std::str::FromStr;
use thiserror::Error;

type MachineInt = i32;

struct Machine<'a> {
    registers: [MachineInt; 4],
    instructions: &'a [Instruction],
    instruction_pointer: usize,
}

impl<'a> Machine<'a> {
    fn new(instructions: &'a [Instruction], registers: [MachineInt; 4]) -> Self {
        Self {
            registers,
            instructions,
            instruction_pointer: 0,
        }
    }

    fn step(&mut self) -> bool {
        let &instruction = match self.instructions.get(self.instruction_pointer) {
            Some(instruction) => instruction,
            None => return false,
        };

        match instruction {
            Instruction::CopyRegister {
                source_reg,
                target_reg,
            } => {
                self.registers[target_reg] = self.registers[source_reg];
                self.instruction_pointer += 1;
            }
            Instruction::CopyValue { val, target_reg } => {
                self.registers[target_reg] = val;
                self.instruction_pointer += 1;
            }
            Instruction::Increment { reg } => {
                self.registers[reg] += 1;
                self.instruction_pointer += 1;
            }
            Instruction::Decrement { reg } => {
                self.registers[reg] -= 1;
                self.instruction_pointer += 1;
            }
            Instruction::JumpNoZeroRegister { reg, offset } => {
                if self.registers[reg] != 0 {
                    self.instruction_pointer = self
                        .instruction_pointer
                        .checked_add_signed(offset)
                        .expect("the instruction pointer should never overflow");
                } else {
                    self.instruction_pointer += 1;
                }
            }
            Instruction::JumpNoZeroValue { val, offset } => {
                if val != 0 {
                    self.instruction_pointer = self
                        .instruction_pointer
                        .checked_add_signed(offset)
                        .expect("the instruction pointer should never overflow");
                } else {
                    self.instruction_pointer += 1;
                }
            }
        }

        true
    }

    fn run(&mut self) {
        loop {
            let stepped = self.step();
            if !stepped {
                break;
            }
        }
    }
}

#[derive(Debug, Clone, Copy)]
enum Instruction {
    CopyRegister {
        source_reg: usize,
        target_reg: usize,
    },
    CopyValue {
        val: MachineInt,
        target_reg: usize,
    },
    Increment {
        reg: usize,
    },
    Decrement {
        reg: usize,
    },
    JumpNoZeroRegister {
        reg: usize,
        offset: isize,
    },
    JumpNoZeroValue {
        val: MachineInt,
        offset: isize,
    },
}

#[derive(Error, Debug)]
enum ParseInstructionError {
    #[error("invalid instruction type")]
    InvalidType,
    #[error("Invalid register name")]
    InvalidRegister,
    #[error("Invalid offset: {0}")]
    ParseInt(#[from] std::num::ParseIntError),
    #[error("Missing instruction parts")]
    MissingParts,
}

#[inline]
fn reg_to_i(reg: &str) -> Result<usize, ParseInstructionError> {
    match reg {
        "a" => Ok(0),
        "b" => Ok(1),
        "c" => Ok(2),
        "d" => Ok(3),
        _ => Err(ParseInstructionError::InvalidRegister),
    }
}

impl FromStr for Instruction {
    type Err = ParseInstructionError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut parts = s.split_whitespace();
        let mut next_part = || parts.next().ok_or(ParseInstructionError::MissingParts);

        match next_part()? {
            "cpy" => {
                let arg1 = next_part()?;
                let arg2 = next_part()?;
                let target_reg = reg_to_i(arg2)?;

                match arg1.parse::<MachineInt>() {
                    Ok(val) => Ok(Instruction::CopyValue { val, target_reg }),
                    Err(_) => Ok(Instruction::CopyRegister {
                        source_reg: reg_to_i(arg1)?,
                        target_reg,
                    }),
                }
            }
            "inc" => {
                let arg1 = next_part()?;
                Ok(Instruction::Increment {
                    reg: reg_to_i(arg1)?,
                })
            }
            "dec" => {
                let arg1 = next_part()?;
                Ok(Instruction::Decrement {
                    reg: reg_to_i(arg1)?,
                })
            }
            "jnz" => {
                let arg1 = next_part()?;
                let arg2 = next_part()?;
                let offset = arg2.parse::<isize>()?;

                match arg1.parse::<MachineInt>() {
                    Ok(value) => Ok(Instruction::JumpNoZeroValue { val: value, offset }),
                    Err(_) => Ok(Instruction::JumpNoZeroRegister {
                        reg: reg_to_i(arg1)?,
                        offset,
                    }),
                }
            }
            _ => Err(ParseInstructionError::InvalidType),
        }
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file_path = std::env::args().nth(1).ok_or("file path not provided")?;
    let contents = std::fs::read_to_string(file_path)?;
    let instructions: Vec<Instruction> = contents
        .lines()
        .map(|line| line.parse().map_err(|e| format!("{e}: {line}")))
        .collect::<Result<Vec<_>, _>>()?;

    let mut machine = Machine::new(&instructions, [0; 4]);
    machine.run();
    let part_1 = machine.registers[0];

    let mut machine = Machine::new(&instructions, [0, 0, 1, 0]);
    machine.run();
    let part_2 = machine.registers[0];

    println!("Part 1: {part_1}\nPart 2: {part_2}");

    Ok(())
}
