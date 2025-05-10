use std::{env, fs};

fn is_valid_triangle(sides: &[u32; 3]) -> bool {
    let [a, b, c] = *sides;
    a + b > c && a + c > b && b + c > a
}

fn main() {
    let file_path = env::args().nth(1).unwrap();
    let contents = fs::read_to_string(file_path).unwrap();
    let triples: Vec<[u32; 3]> = contents
        .lines()
        .map(|line| {
            let mut iter = line.split_whitespace().map(|s| s.parse::<u32>().unwrap());
            [
                iter.next().unwrap(),
                iter.next().unwrap(),
                iter.next().unwrap(),
            ]
        })
        .collect();

    let part_1 = triples
        .iter()
        .filter(|&sides| is_valid_triangle(sides))
        .count();

    let part_2 = triples
        .chunks(3)
        .flat_map(|chunk| {
            [
                [chunk[0][0], chunk[1][0], chunk[2][0]],
                [chunk[0][1], chunk[1][1], chunk[2][1]],
                [chunk[0][2], chunk[1][2], chunk[2][2]],
            ]
        })
        .filter(is_valid_triangle)
        .count();

    println!("part_1 = {part_1}, part_2 = {part_2}");
}
