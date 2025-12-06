use std::error::Error;
use std::{env, fs};

#[derive(Clone, Copy, Debug)]
enum Op {
    Add,
    Mul,
}

fn parse(contents: impl AsRef<str>) -> (Vec<Vec<i64>>, Vec<Op>) {
    let lines: Vec<_> = contents.as_ref().lines().collect();

    let (ops_line, nums_lines) = lines.split_last().unwrap();

    let ops: Vec<Op> = ops_line
        .split_whitespace()
        .map(|s| match s {
            "+" => Op::Add,
            "*" => Op::Mul,
            other => panic!("invalid op {other}"),
        })
        .collect();

    let mut nums_iters: Vec<_> = nums_lines.iter().map(|s| s.split_whitespace()).collect();
    let nums = (0..ops.len())
        .map(|_| {
            nums_iters
                .iter_mut()
                .map(|it| it.next().unwrap().parse().unwrap())
                .collect()
        })
        .collect();

    (nums, ops)
}

fn main() -> Result<(), Box<dyn Error>> {
    let file_path = env::args().nth(1).ok_or("file path not provided")?;
    let contents = fs::read_to_string(file_path)?;
    let (nums, ops) = parse(contents);

    let part_1: i64 = nums
        .iter()
        .zip(ops)
        .map(|(xs, op)| {
            xs.iter()
                .copied()
                .reduce(|x, y| match op {
                    Op::Mul => x * y,
                    Op::Add => x + y,
                })
                .unwrap()
        })
        .sum();

    println!("Part 1: {part_1}");

    Ok(())
}
