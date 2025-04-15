use std::error::Error;
use std::{env, fs};

fn read_input(content: String) -> Result<(u64, u64), String> {
    let mut tokens = content.split_whitespace().rev();
    let column: u64 = tokens
        .next()
        .and_then(|s| s.strip_suffix("."))
        .and_then(|s| s.parse().ok())
        .ok_or("Failed to parse column")?;
    tokens.next();
    let row: u64 = tokens
        .next()
        .and_then(|s| s.strip_suffix(","))
        .and_then(|s| s.parse().ok())
        .ok_or("Failed to parse row")?;
    Ok((row, column))
}

fn pos_to_ord(row: u64, col: u64) -> u64 {
    let diag = row + col - 1;
    (diag - 1) * diag / 2 + col
}

fn main() -> Result<(), Box<dyn Error>> {
    let file_path = env::args().nth(1).ok_or("No file path provided")?;
    let content = fs::read_to_string(file_path)?;
    let (row, col) = read_input(content)?;
    let ord = pos_to_ord(row, col);
    let part_1: u64 = (1..ord).fold(20151125, |acc, _| (acc * 252533) % 33554393);
    println!("part_1 = {part_1}");
    Ok(())
}
