use std::{env, error::Error, fs};

type Grid = Vec<Vec<bool>>;
type Pos = (usize, usize);

fn parse(contents: impl AsRef<str>) -> Result<(Grid, Pos), String> {
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

fn count_splits(grid: Grid, start: Pos) -> usize {
    let n = grid[0].len();

    let mut beams = vec![false; n];
    beams[start.1] = true;

    let mut res = 0;

    for row in grid[start.0..].iter() {
        for j in 0..n {
            if row[j] && beams[j] {
                if j > 0 {
                    beams[j - 1] = true;
                };
                if j + 1 < n {
                    beams[j + 1] = true;
                }
                beams[j] = false;
                res += 1;
            }
        }
    }

    res
}

fn main() -> Result<(), Box<dyn Error>> {
    let file_path = env::args().nth(1).ok_or("file path not provided")?;
    let contents = fs::read_to_string(file_path)?;
    let (grid, start) = parse(contents)?;

    let part_1 = count_splits(grid, start);
    println!("Part 1: {part_1}");

    Ok(())
}
