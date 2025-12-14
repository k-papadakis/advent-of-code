use std::cmp::Reverse;
use std::error::Error;
use std::{cmp, env, fs, iter};

type Point = [i64; 2];

#[derive(Debug, Clone, Copy)]
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
        let a = 1 + self.max[0] - self.min[0];
        let b = 1 + self.max[1] - self.min[1];
        (a * b) as u64
    }

    fn contains(&self, other: &Self) -> bool {
        self.min[0] <= other.min[0]
            && self.max[0] >= other.max[0]
            && self.min[1] <= other.min[1]
            && self.max[1] >= other.max[1]
    }

    fn strictly_overlaps(&self, other: &Self) -> bool {
        let x_overlap = self.min[0] < other.max[0] && self.max[0] > other.min[0];
        let y_overlap = self.min[1] < other.max[1] && self.max[1] > other.min[1];
        x_overlap && y_overlap
    }

    fn crosses(&self, other: &Self) -> bool {
        self.strictly_overlaps(other) && !other.contains(self)
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
    let curve = parse(contents)?;

    let mut rectangles: Vec<Rectangle> = curve
        .iter()
        .enumerate()
        .flat_map(|(i, u)| curve[i + 1..].iter().map(move |v| Rectangle::new(*u, *v)))
        .collect();
    rectangles.sort_unstable_by_key(|r| Reverse(r.area()));

    let part_1 = rectangles.first().ok_or("empty contents")?.area();
    println!("Part 1: {part_1}");

    // Got stuck on part 2 and peeked at a solution on reddit
    let lines: Vec<Rectangle> = curve
        .windows(2)
        .map(|w| Rectangle::new(w[0], w[1]))
        .chain(iter::once(Rectangle::new(
            *curve.first().ok_or("empty curve")?,
            *curve.last().ok_or("empty curve")?,
        )))
        .collect();

    let part_2 = rectangles
        .iter()
        .find(|rect| lines.iter().all(|line| !rect.crosses(line)))
        .ok_or("could not find the rectangle of part 2")?
        .area();

    println!("Part 2: {part_2}");

    Ok(())
}
