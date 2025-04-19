use std::{env, fmt::Display, str::FromStr};
use thiserror::Error;

struct Screen<const W: usize, const H: usize> {
    pixels: [[bool; W]; H],
}

impl<const W: usize, const H: usize> Screen<W, H> {
    fn new() -> Self {
        Self {
            pixels: [[false; W]; H],
        }
    }

    fn apply_instruction(&mut self, instruction: Instruction) {
        match instruction {
            Instruction::Rect { width, height } => {
                for row in &mut self.pixels[..height] {
                    for pixel in &mut row[..width] {
                        *pixel = true;
                    }
                }
            }
            Instruction::RotateRow { row, amount } => {
                let mut new_row = [false; W];
                for (i, value) in self.pixels[row].iter().enumerate() {
                    new_row[(i + amount) % W] = *value;
                }
                self.pixels[row] = new_row;
            }
            Instruction::RotateColumn { col, amount } => {
                let mut new_col = [false; H];
                for (i, value) in self.pixels.iter().map(|row| &row[col]).enumerate() {
                    new_col[(i + amount) % H] = *value
                }
                for (i, value) in new_col.iter().enumerate() {
                    self.pixels[i][col] = *value;
                }
            }
        }
    }

    fn count_lit_pixels(&self) -> usize {
        self.pixels
            .iter()
            .flat_map(|row| row.iter())
            .filter(|&&pixel| pixel)
            .count()
    }
}

impl<const W: usize, const H: usize> Display for Screen<W, H> {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        for row in &self.pixels {
            for &pixel in row {
                write!(f, "{}", if pixel { '#' } else { '.' })?;
            }
            writeln!(f)?;
        }
        Ok(())
    }
}

#[derive(Debug)]
enum Instruction {
    Rect { width: usize, height: usize },
    RotateRow { row: usize, amount: usize },
    RotateColumn { col: usize, amount: usize },
}

impl FromStr for Instruction {
    type Err = ParseInstructionError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let instruction_types = ["rect ", "rotate row ", "rotate column "];
        let args = instruction_types
            .iter()
            .enumerate()
            .find_map(|(i, t)| Some(i).zip(s.strip_prefix(t)))
            .ok_or(ParseInstructionError::InvalidType)?;

        match args {
            (0, args) => {
                let (width, height) = args
                    .split_once('x')
                    .ok_or(ParseInstructionError::InvalidArgument)?;
                Ok(Instruction::Rect {
                    width: width.parse()?,
                    height: height.parse()?,
                })
            }
            (1, args) => {
                let (row, amount) = args
                    .strip_prefix("y=")
                    .and_then(|s| s.split_once(" by "))
                    .ok_or(ParseInstructionError::InvalidArgument)?;
                Ok(Instruction::RotateRow {
                    row: row.parse()?,
                    amount: amount.parse()?,
                })
            }
            (2, args) => {
                let (col, amount) = args
                    .strip_prefix("x=")
                    .and_then(|s| s.split_once(" by "))
                    .ok_or(ParseInstructionError::InvalidArgument)?;
                Ok(Instruction::RotateColumn {
                    col: col.parse()?,
                    amount: amount.parse()?,
                })
            }
            _ => Err(ParseInstructionError::InvalidType),
        }
    }
}

#[derive(Error, Debug)]
enum ParseInstructionError {
    #[error("invalid instruction type")]
    InvalidType,
    #[error("failed to parse integer: {0}")]
    ParseInt(#[from] std::num::ParseIntError),
    #[error("invalid instruction argument")]
    InvalidArgument,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file_path = env::args().nth(1).ok_or("file path not found")?;
    let contents = std::fs::read_to_string(file_path)?;
    let instructions = contents
        .lines()
        .map(|line| {
            line.parse()
                .map_err(|e| format!("failed to parse '{line}': {e}"))
        })
        .collect::<Result<Vec<Instruction>, _>>()?;

    let mut screen = Screen::<50, 6>::new();
    for instruction in instructions {
        screen.apply_instruction(instruction);
    }
    println!("Part 1: {}\nPart 2:\n{}", screen.count_lit_pixels(), screen);

    Ok(())
}
