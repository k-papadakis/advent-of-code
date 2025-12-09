use std::{env, error::Error, fs};

fn parse(contents: impl AsRef<str>) -> Result<Vec<[i64; 2]>, String> {
    contents
        .as_ref()
        .lines()
        .enumerate()
        .map(|(i, line)| {
            let i = i + 1;
            let (x, y) = line
                .split_once(',')
                .ok_or(format!("not enough coordinates on line {i}"))?;
            Ok([
                x.parse()
                    .map_err(|e| format!("invalid first coordinate on line {i}: {e}"))?,
                y.parse()
                    .map_err(|e| format!("invalid second coordinate on line {i}: {e}"))?,
            ])
        })
        .collect()
}

fn main() -> Result<(), Box<dyn Error>> {
    let file_path = env::args().nth(1).ok_or("file path not provided")?;
    let contents = fs::read_to_string(file_path)?;
    let points = parse(contents)?;

    let part_1 = points
        .iter()
        .enumerate()
        .flat_map(|(i, u)| points[i + 1..].iter().map(move |v| (u, v)))
        .map(|(u, v)| (u[0] - v[0] + 1).abs() * (u[1] - v[1] + 1).abs())
        .max()
        .ok_or("empty contents")?;

    println!("Part 1: {part_1}");

    Ok(())
}
