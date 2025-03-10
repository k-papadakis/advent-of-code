use day_11::{Password, PasswordGenerator};
use std::{env, fs};

fn main() {
    let file_path = env::args().nth(1).unwrap();
    let password = fs::read_to_string(file_path).unwrap().trim().to_string();
    let mut password_generator = PasswordGenerator::new(Password::new(password));
    let part_1 = password_generator.next().unwrap();
    let part_2 = password_generator.next().unwrap();
    println!("part_1 = {part_1}, part_2 = {part_2}");
}
