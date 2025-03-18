use std::{env, fs, iter};

const DIRECTIONS: [(isize, isize); 8] = [
    (0, 1),
    (1, 1),
    (1, 0),
    (-1, 1),
    (-1, 0),
    (-1, -1),
    (0, -1),
    (1, -1),
];

fn gif<const M: usize, const N: usize>(
    grid: [[bool; N]; M],
    broken_grid: bool,
) -> impl Iterator<Item = [[bool; N]; M]> {
    let mut grid = grid;

    iter::from_fn(move || {
        let mut new_grid = [[false; N]; M];

        for i in 0..M as isize {
            for j in 0..N as isize {
                let n_active_nbrs = DIRECTIONS
                    .iter()
                    .map(|(di, dj)| (i + di, j + dj))
                    .filter(|&(ni, nj)| {
                        0 <= ni
                            && ni < M as isize
                            && 0 <= nj
                            && nj < N as isize
                            && grid[ni as usize][nj as usize]
                    })
                    .count();
                new_grid[i as usize][j as usize] = {
                    match (grid[i as usize][j as usize], n_active_nbrs) {
                        (true, 2 | 3) => true,
                        (true, _) => false,
                        (false, 3) => true,
                        (false, _) => false,
                    }
                }
            }
        }

        if broken_grid {
            new_grid[0][0] = true;
            new_grid[0][N - 1] = true;
            new_grid[M - 1][0] = true;
            new_grid[M - 1][N - 1] = true;
        }

        let ret = Some(grid);
        grid = new_grid;
        ret
    })
}

fn read_input<const M: usize, const N: usize>(file_path: String) -> [[bool; N]; M] {
    let contents = fs::read_to_string(&file_path).unwrap();
    let mut grid = [[false; N]; M];
    for (i, line) in contents.lines().enumerate() {
        for (j, c) in line.chars().enumerate() {
            if c == '#' {
                grid[i][j] = true
            }
        }
    }
    grid
}

fn main() {
    let file_path = env::args().nth(1).unwrap();
    let mut grid: [[bool; 100]; 100] = read_input(file_path);
    let part_1 = gif(grid, false)
        .nth(100)
        .unwrap()
        .iter()
        .flatten()
        .filter(|&&x| x)
        .count();

    grid[0][0] = true;
    grid[0][100 - 1] = true;
    grid[100 - 1][0] = true;
    grid[100 - 1][100 - 1] = true;
    let part_2 = gif(grid, true)
        .nth(100)
        .unwrap()
        .iter()
        .flatten()
        .filter(|&&x| x)
        .count();
    println!("part_1 = {part_1}, part_2 = {part_2}");
}
