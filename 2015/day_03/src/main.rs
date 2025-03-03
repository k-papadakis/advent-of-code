use std::collections::HashSet;
use std::ops::Add;
use std::{env, fs};

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub struct Point(pub i32, pub i32);

impl Add for Point {
    type Output = Self;

    fn add(self, rhs: Self) -> Self::Output {
        Self(self.0 + rhs.0, self.1 + rhs.1)
    }
}

impl Point {
    pub fn from_char(c: char) -> Self {
        match c {
            '>' => Self(0, 1),
            '^' => Self(-1, 0),
            '<' => Self(0, -1),
            'v' => Self(1, 0),
            other => panic!("Cannot create a Point from {other:?}"),
        }
    }
}

fn path_from_directions<'a>(directions: impl Iterator<Item = &'a Point>) -> Vec<Point> {
    let mut path = Vec::new();
    let mut cur = Point(0, 0);
    path.push(cur);
    for d in directions {
        cur = cur + *d;
        path.push(cur);
    }
    path
}

fn read_input(file_path: &str) -> Vec<Point> {
    fs::read_to_string(file_path)
        .expect("should be able to read from file path")
        .trim_end()
        .chars()
        .map(Point::from_char)
        .collect()
}

fn main() {
    let file_path = env::args().nth(1).expect("file path should be present");
    let directions = read_input(&file_path);

    let part_1 = path_from_directions(directions.iter())
        .into_iter()
        .collect::<HashSet<_>>()
        .len();

    let mut visited: HashSet<Point> = HashSet::new();
    visited.extend(path_from_directions(directions.iter().step_by(2)));
    visited.extend(path_from_directions(directions.iter().skip(1).step_by(2)));
    let part_2 = visited.len();

    println!("part_1 = {part_1}, part_2 = {part_2}");
}
