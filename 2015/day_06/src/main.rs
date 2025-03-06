use regex::Regex;
use std::{env, fs};

const N: usize = 1_000;

type Point = (usize, usize);

#[derive(Debug, Clone, Copy)]
struct Rectangle(Point, Point);

impl Rectangle {
    fn points(&self) -> impl Iterator<Item = Point> {
        (self.0.0..=self.1.0).flat_map(|i| (self.0.1..=self.1.1).map(move |j| (i, j)))
    }
}

impl<'a> IntoIterator for &'a Rectangle {
    type Item = Point;
    type IntoIter = Box<dyn Iterator<Item = Self::Item> + 'a>;

    fn into_iter(self) -> Self::IntoIter {
        Box::new(self.points())
    }
}

#[derive(Debug, Clone, Copy)]
enum Instruction {
    On(Rectangle),
    Off(Rectangle),
    Toggle(Rectangle),
}

impl Instruction {
    fn execute(&self, arr: &mut [bool]) {
        match self {
            Instruction::On(rectangle) => {
                for (i, j) in rectangle {
                    arr[i * N + j] = true;
                }
            }
            Instruction::Off(rectangle) => {
                for (i, j) in rectangle {
                    arr[i * N + j] = false;
                }
            }
            Instruction::Toggle(rectangle) => {
                for (i, j) in rectangle {
                    arr[i * N + j] = !arr[i * N + j];
                }
            }
        }
    }

    fn execute2(&self, arr: &mut [u32]) {
        match self {
            Instruction::On(rectangle) => {
                for (i, j) in rectangle {
                    arr[i * N + j] += 1;
                }
            }
            Instruction::Off(rectangle) => {
                for (i, j) in rectangle {
                    arr[i * N + j] = arr[i * N + j].saturating_sub(1);
                }
            }
            Instruction::Toggle(rectangle) => {
                for (i, j) in rectangle {
                    arr[i * N + j] += 2;
                }
            }
        }
    }
}

fn read_input(file_path: &str) -> Vec<Instruction> {
    let data = fs::read_to_string(file_path).unwrap();
    let re =
        Regex::new(r"(?m)^(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)$").unwrap();
    re.captures_iter(&data)
        .map(|cap| {
            let x1: usize = cap.get(2).unwrap().as_str().parse().unwrap();
            let y1: usize = cap.get(3).unwrap().as_str().parse().unwrap();
            let x2: usize = cap.get(4).unwrap().as_str().parse().unwrap();
            let y2: usize = cap.get(5).unwrap().as_str().parse().unwrap();
            let rectangle = Rectangle((x1, y1), (x2, y2));

            match cap.get(1).unwrap().as_str() {
                "turn on" => Instruction::On(rectangle),
                "turn off" => Instruction::Off(rectangle),
                "toggle" => Instruction::Toggle(rectangle),
                other => panic!("Invalid instruction {other:?}"),
            }
        })
        .collect()
}

fn main() {
    let file_path = env::args().nth(1).unwrap();
    let instructions = read_input(&file_path);

    let mut arr = [false; N * N];
    for instruction in &instructions {
        instruction.execute(&mut arr);
    }
    let part_1: u32 = arr.iter().map(|&x| x as u32).sum();

    let mut arr = [0; N * N];
    for instruction in &instructions {
        instruction.execute2(&mut arr);
    }
    let part_2: u32 = arr.iter().sum();

    println!("part_1 = {part_1}, part_2 = {part_2}");
}
