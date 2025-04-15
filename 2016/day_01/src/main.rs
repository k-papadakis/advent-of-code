use std::{
    collections::HashSet,
    env,
    error::Error,
    fmt, fs,
    ops::{Add, Mul},
};

#[derive(PartialEq, Eq, Hash, Clone, Copy, Debug)]
struct Point(i32, i32);

impl Add for Point {
    type Output = Point;

    fn add(self, rhs: Self) -> Self::Output {
        Point(self.0 + rhs.0, self.1 + rhs.1)
    }
}

impl Mul<i32> for Point {
    type Output = Point;

    fn mul(self, rhs: i32) -> Self::Output {
        Point(self.0 * rhs, self.1 * rhs)
    }
}

impl Mul for Point {
    type Output = Point;

    fn mul(self, rhs: Self) -> Self::Output {
        Point(
            self.0 * rhs.0 - self.1 * rhs.1,
            self.0 * rhs.1 + self.1 * rhs.0,
        )
    }
}

impl Point {
    fn l1(&self) -> u32 {
        self.0.unsigned_abs() + self.1.unsigned_abs()
    }
}

#[derive(Debug)]
enum InputError {
    MissingRotation,
    InvalidRotation(char),
    InvalidMagnitude(String),
}

impl fmt::Display for InputError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::MissingRotation => write!(f, "Missing rotation character"),
            Self::InvalidRotation(c) => write!(f, "Invalid rotation character: {}", c),
            Self::InvalidMagnitude(s) => write!(f, "Invalid magnitude: {}", s),
        }
    }
}

impl Error for InputError {}

fn parse_input(content: String) -> Result<Vec<(Point, i32)>, InputError> {
    content
        .trim_end()
        .split(", ")
        .map(|s| {
            let first_char = s.chars().next().ok_or(InputError::MissingRotation)?;
            let rotation = match first_char {
                'R' => Point(0, 1),
                'L' => Point(0, -1),
                c => return Err(InputError::InvalidRotation(c)),
            };

            let magnitude_str = &s[1..];
            let magnitude = magnitude_str
                .parse()
                .map_err(|_| InputError::InvalidMagnitude(magnitude_str.to_string()))?;

            Ok((rotation, magnitude))
        })
        .collect()
}

fn final_position(instructions: &[(Point, i32)]) -> Point {
    instructions
        .iter()
        .fold((Point(0, 0), Point(1, 0)), |(pos, dir), &(rot, len)| {
            (pos + dir * rot * len, dir * rot)
        })
        .0
}

fn positions_iter(instructions: &[(Point, i32)]) -> impl Iterator<Item = Point> {
    instructions
        .iter()
        .scan((Point(0, 0), Point(1, 0)), |state, &(rot, len)| {
            let pos = state.0;
            let dir = state.1 * rot;

            state.0 = pos + dir * len;
            state.1 = dir;

            Some((1..=len).map(move |i| Point(pos.0 + dir.0 * i, pos.1 + dir.1 * i)))
        })
        .flatten()
}

fn first_duplicate_position(instructions: &[(Point, i32)]) -> Option<Point> {
    let mut visited = HashSet::new();
    visited.insert(Point(0, 0));

    positions_iter(instructions).find(|&point| !visited.insert(point))
}

fn main() -> Result<(), Box<dyn Error>> {
    let file_path = env::args().nth(1).ok_or("File path not provided.")?;
    let content = fs::read_to_string(file_path)?;
    let instructions = parse_input(content)?;

    let part_1 = final_position(&instructions).l1();
    let part_2 = first_duplicate_position(&instructions)
        .ok_or("No duplicate position found.")?
        .l1();

    println!("part_1 = {part_1}, part_2 = {part_2}");

    Ok(())
}
