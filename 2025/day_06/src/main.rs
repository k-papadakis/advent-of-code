use std::error::Error;
use std::{env, fs};

#[derive(Clone, Copy, Debug)]
enum Op {
    Add,
    Mul,
}

fn parse(contents: impl AsRef<str>) -> (Vec<Vec<i32>>, Vec<Op>) {
    // TODO: rewrite using itertools
    let rows: Vec<_> = contents
        .as_ref()
        .lines()
        .map(|line| line.split_whitespace())
        .collect();

    let (ops, nums) = rows.split_last().unwrap();

    let nums = nums
        .iter()
        .map(|row| row.clone().map(|s| s.parse().unwrap()).collect());

    let ops = ops.clone().map(|s| match s {
        "+" => Op::Add,
        "*" => Op::Mul,
        other => panic!("invalid op {other}"),
    });

    (nums.collect(), ops.collect())
}

fn main() -> Result<(), Box<dyn Error>> {
    let file_path = env::args().nth(1).ok_or("file path not provided")?;
    let contents = fs::read_to_string(file_path)?;
    let (nums, ops) = parse(contents);

    println!("nums: {nums:?}\nops: {ops:?}");
    Ok(())
}
