use std::{env, fs};

fn first_house(
    min_presents: usize,
    presents_per_elf: usize,
    deliveries_per_elf: usize,
) -> Option<usize> {
    let min_presents =
        min_presents / presents_per_elf + (min_presents % presents_per_elf != 0) as usize;

    let mut presents = vec![0; min_presents + 1];

    for i in 1..(presents.len() + 1) / 2 {
        for j in (i..presents.len()).step_by(i).take(deliveries_per_elf) {
            presents[j] += i;
        }
    }

    presents.into_iter().position(|p| p >= min_presents)
}

fn main() {
    let file_path = env::args().nth(1).unwrap();
    let min_presents: usize = fs::read_to_string(file_path)
        .unwrap()
        .trim()
        .parse()
        .unwrap();
    let part_1 = first_house(min_presents, 10, usize::MAX).unwrap();
    let part_2 = first_house(min_presents, 11, 50).unwrap();
    println!("part_1 = {part_1} part_2 = {part_2}");
}
