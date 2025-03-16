use std::{env, fs};

/// Returns `comb` where `comb[n][i]` is the number of ways to make `i` using the `n` parts.
fn combinations(target: u32, parts: &[u32]) -> Vec<Vec<u64>> {
    let mut comb = vec![vec![0u64; parts.len()]; (target + 1) as usize];
    comb[0][0] = 1;

    for &part in parts {
        for i in (part..=target).rev() {
            for n in 1..parts.len() {
                comb[i as usize][n] += comb[(i - part) as usize][n - 1]
            }
        }
    }

    comb
}

fn main() {
    let file_path = env::args().nth(1).unwrap();
    let parts: Vec<u32> = fs::read_to_string(file_path)
        .unwrap()
        .lines()
        .map(|s| s.parse().unwrap())
        .collect();

    let comb = combinations(150, &parts);
    let part_1: u64 = comb[150].iter().sum();
    let part_2 = *comb[150].iter().find(|&&x| x > 0).unwrap();
    println!("part_1 = {part_1}, part_2 = {part_2}");
}
