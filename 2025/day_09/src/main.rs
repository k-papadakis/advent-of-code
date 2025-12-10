use std::cmp::Reverse;
use std::error::Error;
use std::{cmp, env, fs};

type Point = [u64; 2];
type Horizontal = (u64, Point);

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
        a * b
    }

    fn iter_perimeter(&self) -> impl Iterator<Item = Point> {
        // TODO: avoid duplicates
        let (min, max) = (self.min, self.max);
        let a = (min[0]..=max[0]).map(move |i| [i, min[1]]); // left, top->down
        let b = (min[0]..=max[0]).map(move |i| [i, max[1]]); // right, top->down
        let c = (min[1]..=max[1]).map(move |j| [min[0], j]); // top, left->right
        let d = (min[1]..=max[1]).map(move |j| [max[0], j]); // down, left->right
        a.chain(b).chain(c).chain(d)
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

fn get_horizontals(curve: &[Point]) -> Vec<Horizontal> {
    let mut horizontals: Vec<_> = curve
        .windows(2)
        .filter(|w| w[0][0] == w[1][0])
        .map(|w| {
            let (u, v) = (w[0], w[1]);
            let a = cmp::min(u[1], v[1]);
            let b = cmp::max(u[1], v[1]);
            (u[0], [a, b])
        })
        .collect();
    horizontals.sort_unstable_by_key(|&(a, _)| a);
    horizontals
}

fn raycast_down(point: Point, horizontals: &[Horizontal]) -> usize {
    let p = horizontals.partition_point(|&(h, _)| h <= point[0]);
    horizontals[..p]
        .iter()
        .filter(|&&(_, [a, b])| (a..=b).contains(&point[1]))
        .count()
}

fn is_in_curve(point: Point, horizontals: &[Horizontal]) -> bool {
    raycast_down(point, horizontals) % 2 == 1
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

    let horizontals = get_horizontals(&curve);
    let best_rect = rectangles
        .iter()
        .find(|r| r.iter_perimeter().all(|p| is_in_curve(p, &horizontals)));

    println!("Best rect: {best_rect:?}");

    Ok(())
}
