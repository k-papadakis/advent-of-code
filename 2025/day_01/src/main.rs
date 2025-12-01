fn parse(contents: &str) -> Vec<i32> {
    contents
        .lines()
        .map(|line| line.split_at(1))
        .map(|(x, y)| {
            let sgn = match x {
                "L" => -1,
                "R" => 1,
                _ => panic!("bad input"),
            };
            let len = y.parse::<i32>().unwrap();

            sgn * len
        })
        .collect()
}

fn iter_positions(deltas: &[i32], start: i32, len: i32) -> impl Iterator<Item = i32> {
    let head = std::iter::once(start);
    let tail = deltas.iter().scan(start, move |p, &d| {
        *p = (*p + d).rem_euclid(len);
        Some(*p)
    });
    head.chain(tail)
}

fn count_passes_over_zero(start: i32, delta: i32, len: i32) -> i32 {
    if delta < 0 {
        return count_passes_over_zero((len - start) % len, -delta, len);
    }
    let t = start + delta;
    if t >= len { 1 + (t - len) / len } else { 0 }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file_path = std::env::args().nth(1).ok_or("file path not provided")?;
    let contents = std::fs::read_to_string(file_path)?;
    let deltas = parse(&contents);

    let part_1 = iter_positions(&deltas, 50, 100).filter(|&p| p == 0).count();

    let part_2: i32 = iter_positions(&deltas, 50, 100)
        .zip(&deltas)
        .map(|(start, &delta)| count_passes_over_zero(start, delta, 100))
        .sum();

    println!("Part 1: {part_1}\nPart 2: {part_2}");

    Ok(())
}
