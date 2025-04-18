use std::{env, fs};

fn to_counts_by_col(data: String) -> Vec<[u16; 26]> {
    let ncols = data.lines().next().unwrap().len();
    let mut counters = vec![[0u16; 26]; ncols];
    for line in data.lines() {
        for (col, b) in line.bytes().enumerate() {
            counters[col][(b - b'a') as usize] += 1
        }
    }
    counters
}

fn decode<F>(counters: &[[u16; 26]], picker: F) -> String
where
    F: Fn(&[u16; 26]) -> usize,
{
    let v = counters
        .iter()
        .map(|counter| {
            let idx = picker(counter);
            idx as u8 + b'a'
        })
        .collect::<Vec<u8>>();
    String::from_utf8(v).unwrap()
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file_path = env::args().nth(1).ok_or("file path not provided")?;
    let contents = fs::read_to_string(file_path)?;
    let counters = to_counts_by_col(contents);
    let part_1 = decode(&counters, |counter| {
        let (idx, _) = counter.iter().enumerate().max_by_key(|&(_, c)| c).unwrap();
        idx
    });
    let part_2 = decode(&counters, |counter| {
        let (idx, _) = counter.iter().enumerate().min_by_key(|&(_, c)| c).unwrap();
        idx
    });
    println!("part_1 = {part_1}, part_2 = {part_2}");

    Ok(())
}
