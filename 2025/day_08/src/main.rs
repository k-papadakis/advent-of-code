// TODO: improve code quality and efficiency

use day_08::UnionFind;
use std::collections::HashMap;
use std::error::Error;
use std::{env, fs};

type Point = [u64; 3];

fn parse(contents: impl AsRef<str>) -> Result<Vec<Point>, String> {
    contents
        .as_ref()
        .lines()
        .map(|line| {
            let mut it = line.splitn(3, ',');
            let mut parse = || {
                it.next()
                    .ok_or("not enough coordinates".to_string())?
                    .parse()
                    .map_err(|e| format!("invalid coordinate: {e}"))
            };
            Ok([parse()?, parse()?, parse()?])
        })
        .collect()
}

fn sqrdist(u: Point, v: Point) -> u64 {
    u.into_iter()
        .zip(v)
        .map(|(x, y)| (x as i64 - y as i64).pow(2) as u64)
        .sum()
}

fn get_sorted_edges(coords: &[Point]) -> Vec<(usize, usize)> {
    let n = coords.len();
    let mut edges = Vec::with_capacity(n * (n + 1) / 2 - n);
    for i in 0..n {
        for j in i + 1..n {
            edges.push((i, j))
        }
    }
    edges.sort_unstable_by_key(|&(i, j)| sqrdist(coords[i], coords[j]));

    edges
}

fn circuit_sizes_desc(uf: &mut UnionFind) -> Vec<usize> {
    let mut counts = HashMap::new();
    for r in uf.labels() {
        counts.entry(r).and_modify(|c| *c += 1).or_insert(1);
    }
    let mut counts: Vec<_> = counts.into_values().collect();
    counts.sort();
    counts.reverse();
    counts
}

fn main() -> Result<(), Box<dyn Error>> {
    let file_path = env::args().nth(1).ok_or("file path not provided")?;
    let contents = fs::read_to_string(file_path)?;
    let coords = parse(contents)?;

    const N: usize = 1_000;

    let edges = get_sorted_edges(&coords);

    // Apply the first N connections
    let mut uf = UnionFind::new(coords.len());
    for &(i, j) in &edges[..N] {
        uf.union(i, j);
    }
    let part_1: usize = circuit_sizes_desc(&mut uf)[..3].iter().product();
    println!("Part 1: {part_1}");

    // Apply the rest of the connections
    let mut last = None;
    for &(i, j) in &edges[N + 1..] {
        if uf.union(i, j) {
            last = Some((i, j));
        }
    }
    let (i, j) = last.expect("should always be found given that we have all edges");
    let part_2 = coords[i][0] * coords[j][0];
    println!("Part 2: {part_2}");

    Ok(())
}
