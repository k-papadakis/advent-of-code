use std::{env, fs, str::FromStr};

type Register = u32;
type RegisterId = usize;
type Offset = isize;

#[derive(Debug)]
enum Instruction {
    Half(RegisterId),
    Triple(RegisterId),
    Increment(RegisterId),
    Jump(Offset),
    JumpIfEven(RegisterId, Offset),
    JumpIfOne(RegisterId, Offset),
}

#[derive(Debug)]
struct ParseInstructionError;

impl FromStr for Instruction {
    type Err = ParseInstructionError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (instr, args) = s.split_once(" ").ok_or(ParseInstructionError)?;
        let mut args = args.split(", ");

        fn parse_register(
            args: &mut std::str::Split<'_, &str>,
        ) -> Result<usize, ParseInstructionError> {
            args.next()
                .ok_or(ParseInstructionError)
                .and_then(|x| match x {
                    "a" => Ok(0),
                    "b" => Ok(1),
                    _ => Err(ParseInstructionError),
                })
        }

        fn parse_offset(
            args: &mut std::str::Split<'_, &str>,
        ) -> Result<isize, ParseInstructionError> {
            args.next()
                .ok_or(ParseInstructionError)
                .and_then(|x| x.parse().map_err(|_| ParseInstructionError))
        }

        match instr {
            "hlf" => Ok(Instruction::Half(parse_register(&mut args)?)),
            "tpl" => Ok(Instruction::Triple(parse_register(&mut args)?)),
            "inc" => Ok(Instruction::Increment(parse_register(&mut args)?)),
            "jmp" => Ok(Instruction::Jump(parse_offset(&mut args)?)),
            "jie" => Ok(Instruction::JumpIfEven(
                parse_register(&mut args)?,
                parse_offset(&mut args)?,
            )),
            "jio" => Ok(Instruction::JumpIfOne(
                parse_register(&mut args)?,
                parse_offset(&mut args)?,
            )),
            _ => Err(ParseInstructionError),
        }
    }
}

struct Program<'a> {
    registers: [Register; 2],        // data
    instructions: &'a [Instruction], // code
    position: isize,
}

impl<'a> Program<'a> {
    fn new(registers: [Register; 2], instructions: &'a Vec<Instruction>) -> Self {
        Self {
            registers,
            instructions,
            position: 0,
        }
    }

    fn step(&mut self) -> bool {
        if self.position < 0 || self.position >= self.instructions.len() as isize {
            return false;
        }

        match self.instructions[self.position as usize] {
            Instruction::Half(i) => {
                self.registers[i] /= 2;
                self.position += 1;
            }
            Instruction::Triple(i) => {
                self.registers[i] *= 3;
                self.position += 1;
            }
            Instruction::Increment(i) => {
                self.registers[i] += 1;
                self.position += 1;
            }
            Instruction::Jump(d) => self.position += d,
            Instruction::JumpIfEven(i, d) => {
                if self.registers[i] % 2 == 0 {
                    self.position += d;
                } else {
                    self.position += 1;
                }
            }
            Instruction::JumpIfOne(i, d) => {
                if self.registers[i] == 1 {
                    self.position += d;
                } else {
                    self.position += 1;
                }
            }
        }

        true
    }

    fn execute(&mut self) -> Register {
        loop {
            if !self.step() {
                return self.registers[1];
            }
        }
    }
}

fn main() {
    let file_path = env::args().nth(1).unwrap();
    let content = fs::read_to_string(file_path).unwrap();
    let instructions: Vec<Instruction> =
        content.lines().map(|line| line.parse().unwrap()).collect();

    let part_1 = Program::new([0, 0], &instructions).execute();
    let part_2 = Program::new([1, 0], &instructions).execute();
    println!("part_1 = {part_1}, part_2 = {part_2}");
}
