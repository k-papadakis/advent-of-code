use std::{env, fs};

fn main() {
    let file_path = env::args().nth(1).unwrap();
    let parens = fs::read_to_string(file_path).unwrap();
    let floors = parens.bytes().map(|c| match c {
        b'(' => 1,
        b')' => -1,
        other => panic!("Unexpected character {:?}", other as char),
    });
    let part_1: i32 = floors.clone().sum();
    let part_2 = floors
        .scan(0, |acc, x| {
            *acc += x;
            Some(*acc)
        })
        .enumerate()
        .find_map(|(i, x)| if x == -1 { Some(i + 1) } else { None })
        .unwrap();

    println!("part_1 = {part_1} part_2 = {part_2}");
}
