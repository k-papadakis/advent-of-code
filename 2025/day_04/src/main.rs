use std::error::Error;
use std::{env, fs, iter};

const DIRECTIONS: [(isize, isize); 8] = [
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (-1, -1),
    (0, -1),
    (1, -1),
];

fn parse(contents: impl AsRef<str>) -> Vec<Vec<bool>> {
    contents
        .as_ref()
        .lines()
        .map(|line| {
            line.chars()
                .map(|c| match c {
                    '@' => true,
                    '.' => false,
                    other => panic!("invalid character {other}"),
                })
                .collect()
        })
        .collect()
}

fn get_neighbors(
    grid: &[Vec<bool>],
    (i, j): (usize, usize),
) -> impl Iterator<Item = (usize, usize)> {
    let (m, n) = (grid.len() as isize, grid[0].len() as isize);

    DIRECTIONS.into_iter().filter_map(move |(di, dj)| {
        let (ii, jj) = (i as isize + di, j as isize + dj);

        if (0..m).contains(&ii) && (0..n).contains(&jj) {
            Some((ii as usize, jj as usize))
        } else {
            None
        }
    })
}

fn is_accessible(grid: &[Vec<bool>], (i, j): (usize, usize)) -> bool {
    get_neighbors(grid, (i, j))
        .filter(|&(i, j)| grid[i][j])
        .count()
        < 4
}

fn iter_papers(grid: &[Vec<bool>]) -> impl Iterator<Item = (usize, usize)> {
    let (m, n) = (grid.len(), grid[0].len());

    (0..m)
        .flat_map(move |i| (0..n).map(move |j| (i, j)))
        .filter(|&(i, j)| grid[i][j])
}

fn iter_accessible_papers(grid: &[Vec<bool>]) -> impl Iterator<Item = (usize, usize)> {
    iter_papers(grid).filter(|&pos| is_accessible(grid, pos))
}

fn iter_accessible_paper_removals(grid: &[Vec<bool>]) -> impl Iterator<Item = Vec<(usize, usize)>> {
    let mut grid = grid.to_vec();

    iter::from_fn(move || {
        let accessibles: Vec<_> = iter_accessible_papers(&grid).collect();

        if accessibles.is_empty() {
            return None;
        }

        for (i, j) in accessibles.iter().copied() {
            grid[i][j] = false
        }

        Some(accessibles)
    })
}

fn main() -> Result<(), Box<dyn Error>> {
    let file_path = env::args().nth(1).ok_or("file path not provided")?;
    let contents = fs::read_to_string(file_path)?;
    let grid = parse(contents);

    let part_1 = iter_accessible_papers(&grid).count();
    let part_2: usize = iter_accessible_paper_removals(&grid).map(|v| v.len()).sum();

    println!("Part 1: {part_1}");
    println!("Part 2: {part_2}");

    Ok(())
}
