use std::error::Error;
use std::{env, fs};

#[derive(Debug, Clone, Copy)]
enum Direction {
    Up,
    Down,
    Left,
    Right,
}

#[rustfmt::skip]
const NUMPAD1: [[char; 3]; 3] = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
];

const NUMPAD2: [[char; 5]; 5] = [
    [' ', ' ', '1', ' ', ' '],
    [' ', '2', '3', '4', ' '],
    ['5', '6', '7', '8', '9'],
    [' ', 'A', 'B', 'C', ' '],
    [' ', ' ', 'D', ' ', ' '],
];

fn step1(pos: (u8, u8), dir: Direction) -> (u8, u8) {
    match dir {
        Direction::Up => (pos.0.saturating_sub(1), pos.1),
        Direction::Down => ((pos.0 + 1).min(2), pos.1),
        Direction::Left => (pos.0, pos.1.saturating_sub(1)),
        Direction::Right => (pos.0, (pos.1 + 1).min(2)),
    }
}

fn step2(pos: (u8, u8), dir: Direction) -> (u8, u8) {
    let cand = match dir {
        Direction::Up => (pos.0.saturating_sub(1), pos.1),
        Direction::Down => ((pos.0 + 1).min(4), pos.1),
        Direction::Left => (pos.0, pos.1.saturating_sub(1)),
        Direction::Right => (pos.0, (pos.1 + 1).min(4)),
    };
    let dist = (cand.0 as i16 - 2).abs() + (cand.1 as i16 - 2).abs();
    if dist <= 2 { cand } else { pos }
}

fn pressing_positions(
    instructions: &[Vec<Direction>],
    start: (u8, u8),
    step_fn: fn((u8, u8), Direction) -> (u8, u8),
) -> impl Iterator<Item = (u8, u8)> {
    instructions.iter().scan(start, move |state, batch| {
        *state = batch.iter().fold(*state, |pos, &dir| step_fn(pos, dir));
        Some(*state)
    })
}

fn main() -> Result<(), Box<dyn Error>> {
    let file_path = env::args().nth(1).ok_or("No file path provided")?;
    let content = fs::read_to_string(file_path)?;
    let instructions = content
        .lines()
        .map(|line| {
            line.chars()
                .map(|c| match c {
                    'U' => Ok(Direction::Up),
                    'D' => Ok(Direction::Down),
                    'L' => Ok(Direction::Left),
                    'R' => Ok(Direction::Right),
                    other => Err(format!("Invalid dir character: {}", other)),
                })
                .collect()
        })
        .collect::<Result<Vec<Vec<_>>, _>>()?;

    let part_1: String = pressing_positions(&instructions, (1, 1), step1)
        .map(|p| NUMPAD1[p.0 as usize][p.1 as usize])
        .collect();

    let part_2: String = pressing_positions(&instructions, (1, 1), step2)
        .map(|p| NUMPAD2[p.0 as usize][p.1 as usize])
        .collect();

    println!("part_1 = {part_1}, part_2 = {part_2}");

    Ok(())
}
