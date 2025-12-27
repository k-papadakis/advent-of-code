use std::{collections::HashMap, env, error::Error, fs};

type Graph = Vec<Vec<usize>>;

fn parse(contents: &str) -> Result<(Graph, HashMap<&str, usize>), String> {
    let mut index = HashMap::new();
    let mut insert = |k| {
        let n = index.len();
        *index.entry(k).or_insert(n)
    };

    let mut edges = Vec::new();
    for (i, line) in contents.lines().enumerate() {
        let (u, vs) = line
            .split_once(':')
            .ok_or(format!("Missing `:` on line {}", i + 1))?;
        let u = insert(u.trim());
        for v in vs.split_whitespace() {
            let v = insert(v);
            edges.push((u, v))
        }
    }

    let mut graph = vec![vec![]; index.len()];
    for (u, v) in edges.into_iter() {
        graph[u].push(v);
    }

    Ok((graph, index))
}

fn compute_indegree(graph: &Graph) -> Vec<usize> {
    let mut indegree = vec![0; graph.len()];
    for vs in graph {
        for &v in vs {
            indegree[v] += 1;
        }
    }
    indegree
}

fn count_paths(graph: &Graph, source: usize) -> Vec<usize> {
    let mut indegree = compute_indegree(graph);
    let mut paths = vec![0usize; graph.len()];
    paths[source] = 1;

    let mut nodes: Vec<_> = indegree
        .iter()
        .enumerate()
        .filter_map(|(u, &d)| if d == 0 { Some(u) } else { None })
        .collect();

    while let Some(u) = nodes.pop() {
        for &v in &graph[u] {
            paths[v] += paths[u];
            indegree[v] -= 1;
            if indegree[v] == 0 {
                nodes.push(v)
            }
        }
    }

    paths
}

fn main() -> Result<(), Box<dyn Error>> {
    let file_path = env::args().nth(1).ok_or("file path not provided")?;
    let contents = fs::read_to_string(file_path)?;
    let (graph, index) = parse(&contents)?;

    let get = |name| {
        index
            .get(name)
            .copied()
            .ok_or(format!("`{name}` node not found"))
    };

    let you = get("you")?;
    let out = get("out")?;
    let part_1 = count_paths(&graph, you)[out];
    println!("Part 1: {part_1}");

    let svr = get("svr")?;
    let fft = get("fft")?;
    let dac = get("dac")?;
    let out = get("out")?;
    let part_2 = count_paths(&graph, svr)[fft]
        * count_paths(&graph, fft)[dac]
        * count_paths(&graph, dac)[out];
    println!("Part 2: {part_2}");

    Ok(())
}
