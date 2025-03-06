use std::{env, fs};

fn contains_two_in_a_row(s: &str) -> bool {
    s.chars().zip(s.chars().skip(1)).any(|(a, b)| a == b)
}

fn contains_at_least_three_vowels(s: &str) -> bool {
    s.chars().filter(|&c| "aeiou".contains(c)).count() >= 3
}
fn contains_prohibited(s: &str) -> bool {
    s.chars()
        .zip(s.chars().skip(1))
        .any(|(a, b)| [('a', 'b'), ('c', 'd'), ('p', 'q'), ('x', 'y')].contains(&(a, b)))
}

fn contains_pair_twice_without_overlap(s: &str) -> bool {
    let mut windows = s.as_bytes().windows(2);
    while let Some(u) = windows.next() {
        if windows.clone().skip(1).any(|v| u == v) {
            return true;
        }
    }
    false
}

fn contains_repeated_with_one_intermediary(s: &str) -> bool {
    s.as_bytes().windows(3).any(|window| window[0] == window[2])
}

fn main() {
    let file_path = env::args().nth(1).unwrap();
    let s = fs::read_to_string(file_path).unwrap();

    let part_1 = s
        .lines()
        .filter(|&line| {
            contains_two_in_a_row(line)
                && contains_at_least_three_vowels(line)
                && !contains_prohibited(line)
        })
        .count();

    let part_2 = s
        .lines()
        .filter(|&line| {
            contains_pair_twice_without_overlap(line)
                && contains_repeated_with_one_intermediary(line)
        })
        .count();

    println!("part_1 = {part_1}, part_2 = {part_2}");
}
