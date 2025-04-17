use std::{array, cmp::Reverse, env, fs, str::FromStr};
use thiserror::Error;

#[derive(Debug)]
struct Room {
    name: String,
    id: u32,
    cks: [u8; 5],
}

impl Room {
    fn is_real(&self) -> bool {
        let counter = count_letters(&self.name);
        let top5 = find_top_5(counter);
        top5 == self.cks
    }

    fn decrypt(&self) -> String {
        let bytes = self
            .name
            .bytes()
            .map(|b| {
                if b == b'-' {
                    b' '
                } else if b.is_ascii_lowercase() {
                    (((b - b'a') as u32 + self.id) % 26 + b'a' as u32) as u8
                } else {
                    panic!("Invalid ascii code {b}")
                }
            })
            .collect::<Vec<_>>();

        String::from_utf8(bytes).unwrap()
    }
}

fn count_letters(s: &str) -> [u8; 26] {
    let mut counter = [0; 26];
    for b in s.bytes().filter(u8::is_ascii_lowercase).map(|b| b - b'a') {
        counter[b as usize] += 1
    }
    counter
}

fn find_top_5(counter: [u8; 26]) -> [u8; 5] {
    let mut bytes: [usize; 26] = array::from_fn(|i| i);
    bytes.sort_by_key(|&b| (Reverse(counter[b]), b));
    array::from_fn(|i| b'a' + bytes[i] as u8)
}

impl FromStr for Room {
    type Err = ParseRoomError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (name, right) = s.rsplit_once('-').ok_or(ParseRoomError::MissingHyphen)?;

        let (id, right) = right
            .split_once("[")
            .ok_or(ParseRoomError::MissingOpeningBracket)?;

        let cks = right
            .strip_suffix(']')
            .ok_or(ParseRoomError::MissingClosingBracket)?;

        Ok(Room {
            name: name.into(),
            id: id.parse()?,
            cks: cks
                .as_bytes()
                .try_into()
                .map_err(|_| ParseRoomError::InvalidChecksum)?,
        })
    }
}

#[derive(Error, Debug)]
enum ParseRoomError {
    #[error("missing hyphen separator")]
    MissingHyphen,

    #[error("missing opening bracket")]
    MissingOpeningBracket,

    #[error("missing closing bracket")]
    MissingClosingBracket,

    #[error("failed to parse room ID: {0}")]
    InvalidId(#[from] std::num::ParseIntError),

    #[error("checksum length != 5")]
    InvalidChecksum,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file_path = env::args().nth(1).ok_or("file path not provided")?;
    let contents = fs::read_to_string(file_path)?;
    let rooms = contents
        .lines()
        .map(|line| line.parse().map_err(|e| format!("{e}: {line}")))
        .collect::<Result<Vec<Room>, _>>()?;

    let part_1: u32 = rooms
        .iter()
        .filter(|room| room.is_real())
        .map(|room| room.id)
        .sum();

    let part_2 = rooms
        .iter()
        .find(|room| room.decrypt().contains("north"))
        .ok_or("not room containing the word \"north\"")?
        .id;

    println!("part_1 = {part_1}, part_2 = {part_2}");

    Ok(())
}
