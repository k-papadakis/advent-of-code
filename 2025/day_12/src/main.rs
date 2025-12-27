use std::{env, error::Error, fs, iter};

type Shape = Vec<Vec<bool>>;
type Quantity = (u32, u32, Vec<u32>);

fn parse(contents: impl AsRef<str>) -> Result<(Vec<Shape>, Vec<Quantity>), String> {
    let parts: Vec<_> = contents.as_ref().split("\n\n").collect();
    let (regions, shapes) = parts.split_last().ok_or("empty contents")?;

    let shapes = shapes
        .iter()
        .enumerate()
        .map(|(i, shapestr)| {
            shapestr
                .lines()
                .skip(1)
                .map(|line| {
                    line.chars()
                        .map(|c| match c {
                            '#' => Ok(true),
                            '.' => Ok(false),
                            other => Err(format!("invalid shape character {other} on shape {}", i)),
                        })
                        .collect::<Result<_, _>>()
                })
                .collect::<Result<_, _>>()
        })
        .collect::<Result<_, _>>()?;

    let regions = regions
        .lines()
        .enumerate()
        .map(|(i, line)| {
            let i = i + 1;
            let (s, t) = line
                .split_once(':')
                .ok_or(format!("character `:` not found on quantity {}", i))?;
            let (w, h) = s
                .split_once('x')
                .ok_or(format!("character `x` not found on quantity {}", i))?;
            let quantities = t
                .split_whitespace()
                .map(|x| {
                    x.parse()
                        .map_err(|e| format!("could not parse quantity {}: {}", i, e))
                })
                .collect::<Result<_, _>>()?;
            Ok((
                w.parse()
                    .map_err(|e| format!("could not parse width on quanitity {}: {}", i, e))?,
                h.parse()
                    .map_err(|e| format!("could not parse height on quanitity {}: {}", i, e))?,
                quantities,
            ))
        })
        .collect::<Result<_, String>>()?;

    Ok((shapes, regions))
}

fn main() -> Result<(), Box<dyn Error>> {
    let file_path = env::args().nth(1).ok_or("file path not provided")?;
    let contents = fs::read_to_string(file_path)?;
    let (shapes, regions) = parse(contents)?;
    let shape_areas: Vec<_> = shapes
        .iter()
        .map(|shape| shape.iter().flatten().filter(|&&b| b).count())
        .collect();

    let part_1 = regions
        .iter()
        .filter(|(w, h, qs)| {
            let perfect_fit_area: u32 = iter::zip(qs, &shape_areas)
                .map(|(&q, &a)| q * a as u32)
                .sum();
            perfect_fit_area < w * h
        })
        .count();

    println!("Part 1: {part_1}");

    Ok(())
}
