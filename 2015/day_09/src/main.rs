use day_09::Graph;
use itertools::Itertools;
use std::{
    env,
    fs::File,
    io::{BufRead, BufReader},
};

fn read_input(file_path: &str) -> Graph<String, i32> {
    let file = File::open(file_path).unwrap();
    let reader = BufReader::new(file);
    let mut graph = Graph::new();
    for line in reader.lines() {
        let line = line.unwrap();
        let parsed = line.split_once(" to ").and_then(|(u, s)| {
            s.split_once(" = ")
                .and_then(|(v, weight)| weight.parse().ok().map(|w| (u, v, w)))
        });
        let (u, v, weight) = parsed.unwrap();
        graph.add_edge(u.into(), v.into(), weight);
        graph.add_edge(v.into(), u.into(), weight);
    }
    graph
}

fn main() {
    let file_path = env::args().nth(1).unwrap();
    let graph = read_input(&file_path);
    let n = graph.num_nodes();
    let dist_iter = (0..n).permutations(n).map(|perm| {
        perm.iter()
            .tuple_windows()
            .map(|(&u, &v)| graph.weight(u, v).unwrap())
            .sum::<i32>()
    });
    let (part_1, part_2) = dist_iter
        .map(|d| (d, d))
        .reduce(|(min, max), (d_min, d_max)| (d_min.min(min), d_max.max(max)))
        .unwrap();

    println!("part_1 = {part_1}, part_2 = {part_2}");
}
