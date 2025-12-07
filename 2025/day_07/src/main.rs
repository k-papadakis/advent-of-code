use std::{env, error::Error, fs};

type Grid<T> = Vec<Vec<T>>;
type Pos = (usize, usize);

fn parse(contents: impl AsRef<str>) -> Result<(Grid<bool>, Pos), String> {
    let mut start = None;

    let grid = contents
        .as_ref()
        .lines()
        .enumerate()
        .map(|(i, line)| {
            line.chars()
                .enumerate()
                .map(|(j, c)| match c {
                    '.' => Ok(false),
                    '^' => Ok(true),
                    'S' => {
                        start = Some((i, j));
                        Ok(false)
                    }
                    other => Err(format!("invalid grid symbol {other}")),
                })
                .collect::<Result<_, _>>()
        })
        .collect::<Result<_, _>>();

    Ok((grid?, start.ok_or("start not found")?))
}

fn count_splits_and_paths(grid: &Grid<bool>, start: Pos) -> (usize, usize) {
    let n = grid[0].len();

    let mut nbeams = 0usize;

    let mut npaths = vec![0usize; n];
    npaths[start.1] = 1;

    for row in grid[start.0..].iter() {
        for j in 0..n {
            if row[j] && npaths[j] > 0 {
                if j > 0 {
                    npaths[j - 1] += npaths[j];
                };
                if j + 1 < n {
                    npaths[j + 1] += npaths[j];
                }
                npaths[j] = 0;

                nbeams += 1;
            }
        }
    }

    (nbeams, npaths.iter().sum())
}

fn main() -> Result<(), Box<dyn Error>> {
    let file_path = env::args().nth(1).ok_or("file path not provided")?;
    let contents = fs::read_to_string(file_path)?;
    let (grid, start) = parse(contents)?;

    let (part_1, part_2) = count_splits_and_paths(&grid, start);
    println!("Part 1: {part_1}");
    println!("Part 2: {part_2}");

    Ok(())
}
