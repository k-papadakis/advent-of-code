use std::error::Error;
use std::{cmp, env, fs};

fn parse(contents: impl AsRef<str>) -> (Vec<(u64, u64)>, Vec<u64>) {
    let (ranges_str, ids_str) = contents.as_ref().split_once("\n\n").unwrap();

    let ranges = ranges_str
        .lines()
        .map(|s| s.split_once('-').unwrap())
        .map(|(start, end)| (start.parse().unwrap(), end.parse().unwrap()));

    let ids = ids_str.lines().map(|s| s.parse().unwrap());

    (ranges.collect(), ids.collect())
}

fn unite_ranges(intervals: &[(u64, u64)]) -> Vec<(u64, u64)> {
    let mut union: Vec<(u64, u64)> = vec![];

    let mut intervals = intervals.to_owned();
    intervals.sort_unstable();

    for (a, b) in intervals.into_iter() {
        if let Some((_, prev_b)) = union.last_mut()
            && *prev_b + 1 >= a
        {
            *prev_b = cmp::max(*prev_b, b)
        } else {
            union.push((a, b))
        }
    }

    union
}

fn main() -> Result<(), Box<dyn Error>> {
    let file_path = env::args().nth(1).ok_or("file path not provided")?;
    let contents = fs::read_to_string(file_path)?;
    let (ranges, ids) = parse(contents);

    let united_ranges = unite_ranges(&ranges);

    let part_1 = ids
        .iter()
        .copied()
        .filter(|id| united_ranges.iter().any(|&(a, b)| (a..=b).contains(id)))
        .count();

    let part_2: u64 = united_ranges.into_iter().map(|(a, b)| b - a + 1).sum();

    println!("Part_1: {part_1}");
    println!("Part_2: {part_2}");

    Ok(())
}
