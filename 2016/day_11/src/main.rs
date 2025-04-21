use day_11::{Pair, State};
use thiserror::Error;

#[derive(Error, Debug)]
pub enum Error {
    #[error("file path not provided")]
    MissingFilePath,
    #[error("invalid microchip-generator pairing")]
    InvalidPairing,
}

fn parse(contents: String) -> Result<Vec<Pair>, Error> {
    let mut microchips = Vec::new();
    let mut generators = Vec::new();

    for (floor, line) in contents.lines().enumerate() {
        let mut tokens = line.split_whitespace().peekable();

        while let Some(t) = tokens.next() {
            if let Some(microchip) = t.strip_suffix("-compatible") {
                microchips.push((microchip, floor));
            } else if let Some("generator") = tokens.peek().and_then(|x| x.strip_suffix([',', '.']))
            {
                generators.push((t, floor));
            }
        }
    }

    if microchips.len() != generators.len() {
        return Err(Error::InvalidPairing);
    }

    microchips.sort_unstable();
    generators.sort_unstable();

    microchips
        .iter()
        .zip(generators.iter())
        .map(|(&(m, mf), &(g, gf))| {
            if m != g {
                Err(Error::InvalidPairing)
            } else {
                Ok(Pair {
                    microchip: mf as u8,
                    generator: gf as u8,
                })
            }
        })
        .collect::<Result<_, _>>()
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file_path = std::env::args().nth(1).ok_or(Error::MissingFilePath)?;
    let contents = std::fs::read_to_string(file_path)?;
    let mut pairs = parse(contents)?;

    let state_1 = State::<5>::new(pairs.as_slice().try_into()?, 0);
    let part_1 = state_1.find_min_steps().ok_or("No solution found!")?;

    pairs.push(Pair {
        microchip: 0,
        generator: 0,
    });
    pairs.push(Pair {
        microchip: 0,
        generator: 0,
    });
    let state_2 = State::<7>::new(pairs.as_slice().try_into()?, 0);
    let part_2 = state_2.find_min_steps().ok_or("No solution found!")?;

    println!("Part 1: {part_1}\nPart 2: {part_2}");

    Ok(())
}
