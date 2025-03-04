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

    println!("part_1 = {part_1}");
}
