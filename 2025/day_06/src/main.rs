use std::error::Error;
use std::str::FromStr;
use std::{env, fs};

#[derive(Clone, Copy, Debug)]
enum Op {
    Add,
    Mul,
}

impl FromStr for Op {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "+" => Ok(Self::Add),
            "*" => Ok(Self::Mul),
            other => Err(format!("invalid op {other}")),
        }
    }
}

struct Problem {
    operator: Op,
    operands: Vec<u64>,
}

impl Problem {
    fn solve(&self) -> u64 {
        match self.operator {
            Op::Add => self.operands.iter().sum(),
            Op::Mul => self.operands.iter().product(),
        }
    }
}

fn parse1(contents: impl AsRef<str>) -> Vec<Problem> {
    let lines: Vec<_> = contents.as_ref().lines().collect();

    let (ops_line, nums_lines) = lines.split_last().unwrap();

    let ops = ops_line.split_whitespace().map(|s| s.parse().unwrap());

    // Create an iterator of words on each row and advance them in lockstep.
    let mut nums_iters: Vec<_> = nums_lines.iter().map(|s| s.split_whitespace()).collect();
    let num_words = ops_line.split_whitespace().count();
    let nums = (0..num_words).map(|_| {
        nums_iters
            .iter_mut()
            .map(|it| it.next().unwrap().parse().unwrap())
            .collect()
    });

    nums.zip(ops)
        .map(|(operands, operator)| Problem { operator, operands })
        .collect()
}

fn parse2(contents: impl AsRef<str>) -> Vec<Problem> {
    let lines: Vec<_> = contents.as_ref().lines().collect();

    let (ops_line, nums_lines) = lines.split_last().unwrap();

    let ops = ops_line.split_whitespace().map(|s| s.parse().unwrap());

    // Create an iterator of characters on each row and advance them in lockstep.
    // Each advancement results into Some(number) if the advancement returned any digits, otherwise None
    // Then we split on None like so:
    // Some(1), Some(23), None, Some(456), None, Some(7), Some(8)
    // -> [1, 23], [456], [7, 8]
    let mut digit_iters: Vec<_> = nums_lines.iter().map(|s| s.chars()).collect();
    let num_chars = ops_line.chars().count();
    let nums_opts: Vec<_> = (0..num_chars)
        .map(|_| {
            digit_iters
                .iter_mut()
                .map(|it| it.next().unwrap())
                .filter_map(|c| c.to_digit(10).map(|x| x as u64))
                .reduce(|x, y| 10 * x + y)
        })
        .collect();
    let nums = nums_opts
        .split(|x| x.is_none())
        .map(|x| x.iter().flatten().copied().collect());

    nums.zip(ops)
        .map(|(operands, operator)| Problem { operator, operands })
        .collect()
}

fn main() -> Result<(), Box<dyn Error>> {
    let file_path = env::args().nth(1).ok_or("file path not provided")?;
    let contents = fs::read_to_string(file_path)?;
    let problems1 = parse1(&contents);
    let problems2 = parse2(contents);

    let part_1: u64 = problems1.iter().map(|problem| problem.solve()).sum();
    let part_2: u64 = problems2.iter().map(|problem| problem.solve()).sum();

    println!("Part 1: {part_1}");
    println!("Part 2: {part_2}");

    Ok(())
}
