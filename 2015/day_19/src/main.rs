use std::{collections::HashSet, env, fs};

fn replace_molecule(molecule: &str, pat: &str, to: &str) -> impl Iterator<Item = String> {
    molecule.match_indices(pat).map(|(start, _)| {
        let res = String::with_capacity(molecule.len() + to.len() - pat.len());
        res + &molecule[0..start] + to + &molecule[start + pat.len()..]
    })
}

fn read_input(file_path: String) -> (Vec<(String, String)>, String) {
    let contents = fs::read_to_string(file_path).unwrap();
    let (rules, molecule) = contents.trim_end().split_once("\n\n").unwrap();
    let rules = rules
        .lines()
        .map(|line| {
            let (from, to) = line.split_once(" => ").unwrap();
            (from.into(), to.into())
        })
        .collect();
    (rules, molecule.into())
}

fn main() {
    let file_path = env::args().nth(1).unwrap();
    let (rules, molecule) = read_input(file_path);

    let part_1 = rules
        .iter()
        .flat_map(|(pat, to)| replace_molecule(&molecule, pat, to))
        .collect::<HashSet<_>>()
        .len();

    // See https://www.reddit.com/r/adventofcode/comments/3xflz8/comment/cy4etju
    let molecule_length = molecule.matches(char::is_uppercase).count();
    let num_parentheses = molecule.matches("Rn").count(); // `( = Rn` and `) = Ar`
    let num_commas = molecule.matches("Y").count(); // `, = Y`
    let part_2 = molecule_length - 2 * num_parentheses - 2 * num_commas - 1;

    println!("part_1 = {part_1}, part_2 = {part_2}");
}
