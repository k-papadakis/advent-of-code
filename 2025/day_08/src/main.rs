// TODO: improve code quality and efficiency

use std::cmp::Reverse;
use std::collections::HashMap;
use std::error::Error;
use std::{env, fs};

use petgraph::unionfind::UnionFind;

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

fn main() -> Result<(), Box<dyn Error>> {
    let file_path = env::args().nth(1).ok_or("file path not provided")?;
    let contents = fs::read_to_string(file_path)?;
    let coords = parse(contents)?;

    let edges = get_sorted_edges(&coords);

    let mut uf = UnionFind::<usize>::new(coords.len());
    for &(i, j) in &edges[..1_000] {
        uf.union(i, j);
    }
    let mut counts = HashMap::new();
    for r in uf.into_labeling() {
        counts.entry(r).and_modify(|c| *c += 1).or_insert(1);
    }
    let mut counts: Vec<_> = counts.into_iter().collect();
    counts.sort_unstable_by_key(|&(_, count)| Reverse(count));
    let part_1: usize = counts.iter().take(3).map(|(_, count)| count).product();
    println!("Part 1: {part_1}");

    //

    let mut uf = UnionFind::<usize>::new(coords.len());
    let mut last = None;
    for (i, j) in edges {
        if uf.union(i, j) {
            last = Some((i, j));
        }
    }
    let (i, j) = last.unwrap();
    let part_2 = coords[i][0] * coords[j][0];
    println!("Part 2: {part_2}");

    // let graph = get_graph(&coords, 1_000);

    Ok(())
}
