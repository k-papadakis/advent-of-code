use std::collections::{HashSet, VecDeque};

fn is_open(x: u32, y: u32, num: u32) -> bool {
    let n = x * x + 3 * x + 2 * x * y + y + y * y + num;
    n.count_ones() % 2 == 0
}

fn min_steps(start: (u32, u32), end: (u32, u32), num: u32) -> Option<u32> {
    let mut visited = HashSet::new();
    let mut queue = VecDeque::new();
    queue.push_back((start, 0));

    while let Some(((x, y), steps)) = queue.pop_front() {
        if (x, y) == end {
            return Some(steps);
        }

        if visited.contains(&(x, y)) {
            continue;
        }
        visited.insert((x, y));

        for (dx, dy) in [(0, 1), (1, 0), (0, -1), (-1, 0)] {
            let new_x = x as i32 + dx;
            let new_y = y as i32 + dy;

            if new_x >= 0 && new_y >= 0 && is_open(new_x as u32, new_y as u32, num) {
                queue.push_back(((new_x as u32, new_y as u32), steps + 1));
            }
        }
    }
    None
}

fn coverage(start: (u32, u32), num: u32, max_steps: u32) -> usize {
    let mut visited = HashSet::new();
    let mut queue = VecDeque::new();
    queue.push_back((start, 0));

    while let Some(((x, y), steps)) = queue.pop_front() {
        if visited.contains(&(x, y)) {
            continue;
        }
        visited.insert((x, y));

        if steps >= max_steps {
            continue;
        }

        for (dx, dy) in [(0, 1), (1, 0), (0, -1), (-1, 0)] {
            let new_x = x as i32 + dx;
            let new_y = y as i32 + dy;

            if new_x >= 0 && new_y >= 0 && is_open(new_x as u32, new_y as u32, num) {
                queue.push_back(((new_x as u32, new_y as u32), steps + 1));
            }
        }
    }
    visited.len()
}

fn main() {
    const FAVORITE_NUMBER: u32 = 1352;
    let part_1 = min_steps((1, 1), (31, 39), FAVORITE_NUMBER).unwrap();
    let part_2 = coverage((1, 1), FAVORITE_NUMBER, 50);
    println!("Part 1: {part_1}\nPart 2: {part_2}");
}
