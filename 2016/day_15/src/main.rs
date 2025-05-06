use thiserror::Error;

pub fn bezout_coefficients(a: i32, b: i32) -> (i32, i32) {
    if a == 0 {
        (0, 1)
    } else {
        let (x, y) = bezout_coefficients(b.rem_euclid(a), a);
        (y - b.div_euclid(a) * x, x)
    }
}

pub fn mod_inverse(a: i32, m: i32) -> Option<i32> {
    let (x, y) = bezout_coefficients(a, m);
    if x * a + y * m == 1 {
        Some(x.rem_euclid(m))
    } else {
        None
    }
}

pub fn chinese_remainder(equations: &[(i32, i32)]) -> i32 {
    let product = equations.iter().map(|(n, _)| n).product();
    equations
        .iter()
        .map(|&(m, a)| {
            let n = product / m;
            let inv = mod_inverse(n, m).unwrap();
            (a * n * inv).rem_euclid(product)
        })
        .sum::<i32>()
        .rem_euclid(product)
}

fn get_disk_equations(disks: &[(i32, i32)]) -> Vec<(i32, i32)> {
    // t0 + t + p_i = 0 (mod n_i); for i in {1, ..., num_disks}
    // t0 = -t - p_i (mod n_i); for i in {1, ..., num_disks}
    // n_i are assumed to be pairwise coprime
    disks
        .iter()
        .enumerate()
        .map(|(i, &(n, p))| (n, (-p - (i + 1) as i32).rem_euclid(n)))
        .collect()
}

fn find_time(disks: &[(i32, i32)]) -> i32 {
    let equations = get_disk_equations(disks);
    chinese_remainder(&equations)
}

#[derive(Error, Debug)]
pub enum ParseError {
    #[error("missing word at position {0}")]
    MissingWord(usize),

    #[error("failed to parse integer: {0}")]
    ParseInt(#[from] std::num::ParseIntError),
}

fn parse(line: &str) -> Result<(i32, i32), ParseError> {
    let mut parts = line.split_whitespace();

    let modulo = parts.nth(3).ok_or(ParseError::MissingWord(3))?.parse()?;
    let position = parts
        .nth(7)
        .ok_or(ParseError::MissingWord(11))?
        .trim_end_matches('.')
        .parse()?;

    Ok((modulo, position))
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file_path = std::env::args().nth(1).ok_or("file path not provided")?;

    let mut disks = std::fs::read_to_string(file_path)?
        .lines()
        .map(|line| parse(line).map_err(|e| format!("{e} in '{line}'")))
        .collect::<Result<Vec<_>, _>>()?;

    let part_1 = find_time(&disks);

    disks.push((11, 0));
    let part_2 = find_time(&disks);

    println!("Part 1: {part_1}\nPart 2: {part_2}");

    Ok(())
}
