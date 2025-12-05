use std::error::Error;
use std::ops::RangeInclusive;
use std::{env, fs};

fn parse(contents: impl AsRef<str>) -> (Vec<RangeInclusive<u64>>, Vec<u64>) {
    let (ranges_str, ids_str) = contents.as_ref().split_once("\n\n").unwrap();

    let ranges = ranges_str
        .lines()
        .map(|s| s.split_once('-').unwrap())
        .map(|(start, end)| (start.parse().unwrap(), end.parse().unwrap()))
        .map(|(start, stop)| start..=stop);

    let ids = ids_str.lines().map(|s| s.parse().unwrap());

    (ranges.collect(), ids.collect())
}

fn main() -> Result<(), Box<dyn Error>> {
    let file_path = env::args().nth(1).ok_or("file path not provided")?;
    let contents = fs::read_to_string(file_path)?;
    let (ranges, ids) = parse(contents);

    let part_1 = ids
        .iter()
        .copied()
        .filter(|id| ranges.iter().any(|range| range.contains(id)))
        .count();

    println!("Part_1: {part_1}");

    Ok(())
}
