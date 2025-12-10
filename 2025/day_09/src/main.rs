use std::cmp::Reverse;
use std::error::Error;
use std::{cmp, env, fs, iter};

type Point = [u64; 2];

struct Rectangle {
    min: Point,
    max: Point,
}

impl Rectangle {
    fn new(u: Point, v: Point) -> Self {
        let min = [cmp::min(u[0], v[0]), cmp::min(u[1], v[1])];
        let max = [cmp::max(u[0], v[0]), cmp::max(u[1], v[1])];
        Self { min, max }
    }

    fn area(&self) -> u64 {
        iter::zip(self.min, self.max)
            .map(|(a, b)| a.abs_diff(b) + 1)
            .product()
    }
}

fn parse(contents: impl AsRef<str>) -> Result<Vec<Point>, String> {
    contents
        .as_ref()
        .lines()
        .enumerate()
        .map(|(i, line)| {
            let i = i + 1;
            let (x, y) = line
                .split_once(',')
                .ok_or(format!("not enough coordinates on line {i}"))?;
            Ok([
                x.parse()
                    .map_err(|e| format!("invalid first coordinate on line {i}: {e}"))?,
                y.parse()
                    .map_err(|e| format!("invalid second coordinate on line {i}: {e}"))?,
            ])
        })
        .collect()
}

fn main() -> Result<(), Box<dyn Error>> {
    let file_path = env::args().nth(1).ok_or("file path not provided")?;
    let contents = fs::read_to_string(file_path)?;
    let points = parse(contents)?;

    let mut rectangles: Vec<Rectangle> = points
        .iter()
        .enumerate()
        .flat_map(|(i, u)| points[i + 1..].iter().map(move |v| Rectangle::new(*u, *v)))
        .collect();
    rectangles.sort_unstable_by_key(|r| Reverse(r.area()));

    let part_1 = rectangles.first().ok_or("empty contents")?.area();

    println!("Part 1: {part_1}");

    Ok(())
}
