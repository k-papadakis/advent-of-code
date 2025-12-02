use std::collections::HashSet;
use std::{env, fs, iter};

fn parse(s: impl AsRef<str>) -> Vec<(u64, u64)> {
    s.as_ref()
        .trim()
        .split(',')
        .map(|s| s.split_once('-').unwrap())
        .map(|(a, b)| (a.parse().unwrap(), b.parse().unwrap()))
        .collect()
}

fn trunc(x: u64, ndigits: u32) -> u64 {
    let max_num = 10u64.pow(ndigits);
    let mut res = x;
    while res >= max_num {
        res /= 10;
    }
    res
}

fn ndigits(x: u64) -> u32 {
    let mut res = 0;
    let mut t = x;
    while t != 0 {
        t /= 10;
        res += 1;
    }
    res
}

fn concat(x: u64, y: u64) -> u64 {
    x * 10u64.pow(ndigits(y)) + y
}

fn repeat(x: u64, n: usize) -> u64 {
    iter::repeat_n(x, n).reduce(concat).expect(">0 reps")
}

fn iter_invalid_ids((a, b): (u64, u64), reps: usize) -> impl Iterator<Item = u64> {
    let start = trunc(a, ndigits(a).div_ceil(reps as u32));
    let end = trunc(b, ndigits(b).div_ceil(reps as u32));
    (start..=end)
        .map(move |x| repeat(x, reps))
        .filter(move |x| (a..=b).contains(x))
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file_path = env::args().nth(1).ok_or("file path required")?;
    let contents = fs::read_to_string(file_path)?;
    let id_ranges = parse(contents);

    let part_1: u64 = id_ranges
        .iter()
        .copied()
        .flat_map(|r| iter_invalid_ids(r, 2))
        .sum();

    let invalids_v2: HashSet<_> = id_ranges
        .iter()
        .copied()
        .flat_map(|(a, b)| {
            (2..=ndigits(b)).flat_map(move |reps| iter_invalid_ids((a, b), reps as usize))
        })
        .collect();
    let part_2: u64 = invalids_v2.iter().sum();

    println!("Part 1: {part_1}");
    println!("Part 2: {part_2}");

    Ok(())
}
