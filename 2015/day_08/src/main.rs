use std::{env, fs};

fn num_memory_chars(s: &str) -> usize {
    let mut count: usize = 0;
    let s = s.as_bytes();
    let mut i = 0;
    while i < s.len() {
        if s[i] == b'\\' {
            if i + 1 < s.len() && matches!(s[i + 1], b'\\' | b'"') {
                i += 2;
            } else if i + 3 < s.len()
                && s[i + 1] == b'x'
                && s[i + 2].is_ascii_hexdigit()
                && s[i + 3].is_ascii_hexdigit()
            {
                i += 4;
            }
        } else {
            i += 1;
        }
        count += 1
    }

    count - 2
}

fn main() {
    let file_path = env::args().nth(1).unwrap();
    let data = fs::read_to_string(file_path).unwrap();
    let part_1: usize = data
        .lines()
        .map(|line| line.len() - num_memory_chars(line))
        .sum();
    let part_2: usize = data
        .lines()
        .map(|s| s.chars().filter(|x| matches!(x, '\\' | '"')).count() + 2)
        .sum();

    println!("part_1 = {part_1}, part_2 = {part_2}");
}
