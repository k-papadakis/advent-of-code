use regex::Regex;
use std::{
    cmp, env,
    fs::File,
    io::{BufRead, BufReader},
};

#[derive(Clone, Copy, Debug)]
struct Reindeer {
    speed: u32,
    flying: u32,
    resting: u32,
}

impl Reindeer {
    fn distance_covered(self, time: u32) -> u32 {
        let q = time / (self.flying + self.resting);
        let r = time % (self.flying + self.resting);
        let final_flight = cmp::min(r, self.flying);

        (q * self.flying + final_flight) * self.speed
    }
}

fn read_input(file_path: &str) -> Vec<Reindeer> {
    let file = File::open(file_path).unwrap();
    let reader = BufReader::new(file);
    let re = Regex::new(
        r"^\w+ can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds\.$",
    )
    .unwrap();

    reader
        .lines()
        .map(|line| {
            let line = line.unwrap();
            let (_, caps) = re.captures(&line).unwrap().extract();
            let [speed, active, inactive] = caps.map(|x| x.parse().unwrap());
            Reindeer {
                speed,
                flying: active,
                resting: inactive,
            }
        })
        .collect()
}

fn winning_distance(reindeers: &[Reindeer], time: u32) -> u32 {
    reindeers
        .iter()
        .map(|r| r.distance_covered(time))
        .max()
        .unwrap()
}

fn winning_points(reindeers: &[Reindeer], time: u32) -> u32 {
    let mut points = vec![0; reindeers.len()];

    for t in 1..=time {
        let dists: Vec<_> = reindeers.iter().map(|r| r.distance_covered(t)).collect();
        let max_dist = *dists.iter().max().unwrap();

        let winners = dists
            .into_iter()
            .enumerate()
            .filter_map(|(i, d)| if d == max_dist { Some(i) } else { None });

        for winner in winners {
            points[winner] += 1;
        }
    }

    points.into_iter().max().unwrap()
}

fn main() {
    let file_path = env::args().nth(1).unwrap();
    let reindeers = read_input(&file_path);
    let time: u32 = 2503;

    let part_1 = winning_distance(&reindeers, time);
    let part_2 = winning_points(&reindeers, time);

    println!("part_1 = {part_1}, part_2 = {part_2}");
}
