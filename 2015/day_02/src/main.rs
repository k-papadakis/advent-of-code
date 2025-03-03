use day_02::Prism;
use std::{
    env, fs,
    io::{BufRead, BufReader},
};

fn read_input(file_path: &str) -> Vec<Prism> {
    let file = fs::File::open(file_path).unwrap();
    let reader = BufReader::new(file);
    reader
        .lines()
        .map(|line| {
            let dim: Vec<u32> = line
                .unwrap()
                .splitn(3, 'x')
                .map(|s| s.parse().unwrap())
                .collect();
            Prism {
                l: dim[0],
                w: dim[1],
                h: dim[2],
            }
        })
        .collect()
}

fn main() {
    let file_path = env::args().nth(1).unwrap();
    let prisms = read_input(&file_path);
    let part_1 = prisms.iter().map(Prism::required_paper).sum::<u32>();
    let part_2 = prisms.iter().map(Prism::required_ribbon).sum::<u32>();
    println!("part_1 = {part_1}, part_2 = {part_2}");
}
