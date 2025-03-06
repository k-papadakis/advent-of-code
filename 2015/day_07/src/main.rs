use std::{
    collections::{HashMap, VecDeque},
    env,
    fs::File,
    io::{BufRead, BufReader},
};

type Graph = HashMap<String, Vec<String>>;

#[derive(Debug, Clone, Copy)]
enum Op {
    Pass,
    LastBit,
    Not,
    And,
    Or,
    Lshift(u8),
    Rshift(u8),
}

fn inverse_graph(graph: &Graph) -> HashMap<&str, Vec<&str>> {
    graph
        .iter()
        .flat_map(|(parent, children)| children.iter().map(move |child| (child, parent)))
        .fold(HashMap::new(), |mut acc, (child, parent)| {
            acc.entry(child).or_default().push(parent);
            acc
        })
}

fn evaluate(
    graph: &Graph,
    ops: &HashMap<String, Op>,
    vals: HashMap<String, u16>,
) -> HashMap<String, u16> {
    let mut vals = vals;
    let inv = inverse_graph(graph);
    let mut indegree: HashMap<_, _> = inv
        .iter()
        .map(|(&node, parents)| (node, parents.len()))
        .collect();
    let mut ready: VecDeque<_> = vals.keys().cloned().collect();

    while let Some(parent) = ready.pop_front() {
        if let Some(children) = graph.get(&parent) {
            for child in children {
                let d = indegree.get_mut(child.as_str()).unwrap();
                *d -= 1;
                if *d != 0 {
                    continue;
                }

                let op = ops
                    .get(child)
                    .expect("Nodes with parents should have an operation");
                let pval = |i: usize| {
                    let parents = inv.get(child.as_str()).unwrap();
                    let parent = parents[i];
                    let val = vals.get(parent).unwrap();
                    *val
                };
                let val = match op {
                    Op::Pass => pval(0),
                    Op::LastBit => pval(0) & 1,
                    Op::Not => !pval(0),
                    Op::And => pval(0) & pval(1),
                    Op::Or => pval(0) | pval(1),
                    Op::Lshift(s) => pval(0) << s,
                    Op::Rshift(s) => pval(0) >> s,
                };
                vals.insert(child.into(), val);
                ready.push_back(child.into());
            }
        }
    }
    vals
}

fn read_input(file_path: &str) -> (Graph, HashMap<String, Op>, HashMap<String, u16>) {
    // TODO: Keep all nodes in a Vec and use references in the other data structures
    let file = File::open(file_path).unwrap();
    let reader = BufReader::new(file);

    let mut graph: Graph = HashMap::new();
    let mut ops: HashMap<String, Op> = HashMap::new();
    let mut vals: HashMap<String, u16> = HashMap::new();

    let mut add_edge = |x: &str, r: &str| {
        graph.entry(x.into()).or_default().push(r.into());
    };

    for line in reader.lines() {
        let line = line.unwrap();
        if line.contains("NOT") {
            let (x, r) = line
                .strip_prefix("NOT ")
                .unwrap()
                .split_once(" -> ")
                .unwrap();
            ops.insert(r.into(), Op::Not);
            add_edge(x, r);
        } else if line.contains("AND") {
            let (left, r) = line.split_once(" -> ").unwrap();
            let (x, y) = left.split_once(" AND ").unwrap();
            if x == "1" {
                ops.insert(r.into(), Op::LastBit);
                add_edge(y, r);
            } else {
                ops.insert(r.into(), Op::And);
                add_edge(x, r);
                add_edge(y, r);
            }
        } else if line.contains("OR") {
            let (left, r) = line.split_once(" -> ").unwrap();
            let (x, y) = left.split_once(" OR ").unwrap();
            ops.insert(r.into(), Op::Or);
            add_edge(x, r);
            add_edge(y, r);
        } else if line.contains("LSHIFT") {
            let (left, r) = line.split_once(" -> ").unwrap();
            let (x, s) = left.split_once(" LSHIFT ").unwrap();
            ops.insert(r.into(), Op::Lshift(s.parse().unwrap()));
            add_edge(x, r);
        } else if line.contains("RSHIFT") {
            let (left, r) = line.split_once(" -> ").unwrap();
            let (x, s) = left.split_once(" RSHIFT ").unwrap();
            ops.insert(r.into(), Op::Rshift(s.parse().unwrap()));
            add_edge(x, r);
        } else {
            let (x, r) = line.split_once(" -> ").unwrap();
            if let Ok(x) = x.parse() {
                vals.insert(r.into(), x);
            } else {
                ops.insert(r.into(), Op::Pass);
                add_edge(x, r);
            }
        }
    }
    (graph, ops, vals)
}

fn main() {
    let file_path = env::args().nth(1).unwrap();
    let (graph, ops, mut vals) = read_input(&file_path);

    let part_1 = *evaluate(&graph, &ops, vals.clone()).get("a").unwrap();

    vals.insert("b".into(), part_1);
    let part_2 = *evaluate(&graph, &ops, vals.clone()).get("a").unwrap();

    println!("part_1 = {part_1}, part_2 = {part_2}");
}
