use std::{env, fs, iter};

type Digit = u8;

fn iter_digits(num: u16) -> impl Iterator<Item = Digit> {
    let mut num = num;
    iter::from_fn(move || {
        if num == 0 {
            None
        } else {
            let digit = num % 10;
            num /= 10;
            Some(digit as Digit)
        }
    })
}

fn grouped_count(digits: &[Digit]) -> impl Iterator<Item = (u16, Digit)> {
    let mut it = digits.iter().peekable();
    iter::from_fn(move || {
        let &digit = it.next()?;
        let mut count = 1;
        while it.peek() == Some(&&digit) {
            it.next();
            count += 1;
        }
        Some((count, digit))
    })
}

fn compress(digits: &[Digit]) -> Vec<Digit> {
    grouped_count(digits)
        .flat_map(|(count, digit)| iter_digits(count).chain(iter::once(digit)))
        .collect()
}

fn main() {
    let file_path = env::args().nth(1).unwrap();
    let digits: Vec<_> = fs::read_to_string(file_path)
        .unwrap()
        .trim()
        .chars()
        .map(|c| c.to_digit(10).unwrap() as Digit)
        .collect();

    let part_1 = (0..40).fold(digits.clone(), |acc, _| compress(&acc)).len();
    let part_2 = (0..50).fold(digits, |acc, _| compress(&acc)).len();
    println!("part_1 = {part_1}, part_2 = {part_2}");
}
