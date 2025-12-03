use std::error::Error;
use std::{env, fs};

fn parse(contents: impl AsRef<str>) -> Vec<Vec<u32>> {
    contents
        .as_ref()
        .lines()
        .map(|s| s.chars().map(|c| c.to_digit(10).unwrap()).collect())
        .collect()
}

fn next_battery(bank: &[u32], remaining: usize) -> (u32, &[u32]) {
    let (i, x) = bank[..=bank.len() - remaining]
        .iter()
        .copied()
        .enumerate()
        .max_by_key(|&(i, x)| (x, -(i as isize)))
        .unwrap();

    (x, &bank[i + 1..])
}

fn max_joltage(bank: &[u32], n: usize) -> u64 {
    let mut res = 0;
    let mut bank = bank;

    for remaining in (1..=n).rev() {
        let (x, new_bank) = next_battery(bank, remaining);

        res = 10 * res + x as u64;
        bank = new_bank;
    }

    res
}

fn main() -> Result<(), Box<dyn Error>> {
    let file_path = env::args().nth(1).ok_or("file path required")?;
    let contents = fs::read_to_string(file_path)?;
    let banks = parse(contents);

    let part_1: u64 = banks.iter().map(|bank| max_joltage(bank, 2)).sum();
    let part_2: u64 = banks.iter().map(|bank| max_joltage(bank, 12)).sum();

    println!("Part 1: {part_1}");
    println!("Part 2: {part_2}");

    Ok(())
}
