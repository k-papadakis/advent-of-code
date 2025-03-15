use day_13::Graph;
use itertools::Itertools;
use regex::Regex;
use std::{env, fs, iter};

fn read_input(file_path: &str) -> Graph<String, i32> {
    let data = fs::read_to_string(file_path).unwrap();
    let re =
        Regex::new(r"^(\w+) would (lose|gain) (\d+) happiness units by sitting next to (\w+).$")
            .unwrap();
    let mut graph = Graph::new();
    for cap in data.lines().map(|line| re.captures(line).unwrap()) {
        let sgn = match &cap[2] {
            "lose" => -1,
            "gain" => 1,
            _ => panic!(),
        };
        let abs: i32 = cap[3].parse().unwrap();
        let weight = sgn * abs;
        graph.add_edge(cap[1].into(), cap[4].into(), weight);
    }
    graph
}

fn maximize_happiness(graph: &Graph<String, i32>) -> i32 {
    let num_nodes = graph.num_nodes();
    (1..num_nodes)
        .permutations(num_nodes - 1)
        .map(|p| {
            iter::once(0)
                .chain(p)
                .chain(iter::once(0))
                .tuple_windows()
                .map(|(u, v)| graph.weight(u, v).unwrap() + graph.weight(v, u).unwrap())
                .sum()
        })
        .max()
        .unwrap()
}

fn maximize_happiness_with_me(graph: &Graph<String, i32>) -> i32 {
    let num_nodes = graph.num_nodes();
    (0..num_nodes)
        .permutations(num_nodes)
        .map(|p| {
            p.into_iter()
                .tuple_windows()
                .map(|(u, v)| graph.weight(u, v).unwrap() + graph.weight(v, u).unwrap())
                .sum()
        })
        .max()
        .unwrap()
}

fn main() {
    let file_path = env::args().nth(1).unwrap();
    let graph = read_input(&file_path);
    let part_1 = maximize_happiness(&graph);
    let part_2 = maximize_happiness_with_me(&graph);

    println!("part_1 = {part_1}, part_2 = {part_2}");
}
