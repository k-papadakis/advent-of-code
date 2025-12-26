use day_10::Machine;
use std::{env, error::Error, fs};

fn parse(contents: impl AsRef<str>) -> Result<Vec<Machine>, String> {
    contents.as_ref().lines().map(|x| x.parse()).collect()
}

fn main() -> Result<(), Box<dyn Error>> {
    let file_path = env::args().nth(1).ok_or("file path not provided")?;
    let contents = fs::read_to_string(file_path)?;
    let machines = parse(contents)?;

    let part_1 = machines
        .iter()
        .map(|m| {
            m.num_presses1().ok_or(format!(
                "impossible to create lights config from buttons for {m:?}"
            ))
        })
        .sum::<Result<usize, _>>()?;
    println!("Part 1: {part_1}");

    // This is easily solveable with Linear Optimization library, but that would be cheating.
    // Instead, here is an ingenious solution from Reddit:
    // https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/
    let part_2 = machines
        .iter()
        .map(|m| {
            m.num_presses2().ok_or(format!(
                "impossible to create joltages config from buttons for {m:?}"
            ))
        })
        .sum::<Result<usize, _>>()?;
    println!("Part 2: {part_2}");

    Ok(())
}
