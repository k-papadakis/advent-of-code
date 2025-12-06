use std::error::Error;
use std::{env, fs};

#[derive(Clone, Copy, Debug)]
enum Op {
    Add,
    Mul,
}

fn parse(contents: impl AsRef<str>) -> (Vec<Vec<u64>>, Vec<Vec<u64>>, Vec<Op>) {
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

    // Create an iterator of words on each row and advance them in lockstep.
    let mut nums1_iters: Vec<_> = nums_lines.iter().map(|s| s.split_whitespace()).collect();
    let nums1 = (0..ops.len())
        .map(|_| {
            nums1_iters
                .iter_mut()
                .map(|it| it.next().unwrap().parse().unwrap())
                .collect()
        })
        .collect();

    // Create an iterator of characters on each row and advance them in lockstep.
    // Each advancement results into Some(number) if the advancement returned any digits, otherwise None
    // Then we split on None like so:
    // Some(1), Some(23), None, Some(456), None, Some(7), Some(8)
    // -> [[1, 23], [456], [7, 8]]
    let mut digit_iters: Vec<_> = nums_lines.iter().map(|s| s.chars()).collect();
    let nums2_opts: Vec<_> = (0..ops_line.len())
        .map(|_| {
            digit_iters
                .iter_mut()
                .map(|it| it.next().unwrap())
                .filter_map(|c| c.to_digit(10).map(|x| x as u64))
                .reduce(|x, y| 10 * x + y)
        })
        .collect();
    let nums2 = nums2_opts
        .split(|x| x.is_none())
        .map(|x| x.iter().flatten().copied().collect())
        .collect();

    (nums1, nums2, ops)
}

fn solve(xs: &[u64], op: Op) -> u64 {
    match op {
        Op::Add => xs.iter().sum(),
        Op::Mul => xs.iter().product(),
    }
}

fn solve_sum(nums: &[Vec<u64>], ops: &[Op]) -> u64 {
    nums.iter().zip(ops).map(|(xs, &op)| solve(xs, op)).sum()
}

fn main() -> Result<(), Box<dyn Error>> {
    let file_path = env::args().nth(1).ok_or("file path not provided")?;
    let contents = fs::read_to_string(file_path)?;
    let (nums1, nums2, ops) = parse(contents);

    let part_1 = solve_sum(&nums1, &ops);
    let part_2 = solve_sum(&nums2, &ops);

    println!("Part 1: {part_1}");
    println!("Part 2: {part_2}");

    Ok(())
}
