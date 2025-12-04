use std::error::Error;
use std::{env, fs};

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

fn find_accessible(grid: &[Vec<bool>]) -> impl Iterator<Item = (usize, usize)> {
    let (m, n) = (grid.len(), grid[0].len());
    let positions = (0..m)
        .flat_map(move |i| (0..n).map(move |j| (i, j)))
        .filter(|&(i, j)| grid[i][j]);
    positions.filter(|&pos| is_accessible(grid, pos))
}

fn grid_to_str(grid: &[Vec<bool>]) -> String {
    let mut res = String::with_capacity((grid.len()) * (grid[0].len() + 1));
    for row in grid {
        for &b in row {
            let c = if b { '@' } else { '.' };
            res.push(c);
        }
        res.push('\n');
    }
    res
}

fn accessible_grid_to_str(grid: &[Vec<bool>]) -> String {
    let n = grid[0].len();
    let mut grid_str = grid_to_str(grid).into_bytes();
    let accessible_positions = find_accessible(grid);
    for (i, j) in accessible_positions {
        grid_str[i * (n + 1) + j] = b'x';
    }
    String::from_utf8(grid_str).unwrap()
}

fn main() -> Result<(), Box<dyn Error>> {
    let file_path = env::args().nth(1).ok_or("file path not provided")?;
    let contents = fs::read_to_string(file_path)?;
    let grid = parse(contents);

    println!("{}\n{}", grid_to_str(&grid), accessible_grid_to_str(&grid));

    let part_1 = find_accessible(&grid).count();
    println!("Part 1: {part_1}");

    Ok(())
}
