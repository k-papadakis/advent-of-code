use std::{env, fs};

fn parse_marker(s: &str) -> Option<(usize, usize, usize)> {
    if !s.starts_with('(') {
        return None;
    }

    let overhead = s[1..].find(')')? + 2;
    let content = &s[1..overhead - 1];
    let (range, reps) = content.split_once('x')?;

    Some((overhead, range.parse().ok()?, reps.parse().ok()?))
}

fn decompressed_length(content: &str) -> usize {
    let content = content.trim();
    let mut pos = 0usize;
    let mut res = 0usize;

    while pos < content.len() {
        if let Some((overhead, range, reps)) = parse_marker(&content[pos..]) {
            res += reps * range;
            pos += overhead + range;
        } else {
            res += 1;
            pos += 1;
        }
    }

    res
}

fn decompressed_length_v2(content: &str) -> usize {
    let content = content.trim();
    let mut pos = 0usize;
    let mut res = 0usize;

    while pos < content.len() {
        if let Some((overhead, range, reps)) = parse_marker(&content[pos..]) {
            let section = &content[pos + overhead..pos + overhead + range];
            res += reps * decompressed_length(section);
            pos += overhead + range;
        } else {
            res += 1;
            pos += 1;
        }
    }

    res
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file_path = env::args().nth(1).ok_or("file path not provided")?;
    let content = fs::read_to_string(file_path)?;
    let part_1 = decompressed_length(&content);
    let part_2 = decompressed_length_v2(&content);
    println!("part_1 = {part_1}, part_2 = {part_2}");
    Ok(())
}
