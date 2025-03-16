use std::{env, fs};

const MFCSAM: Analysis = Analysis {
    children: Some(3),
    cats: Some(7),
    samoyeds: Some(2),
    pomeranians: Some(3),
    akitas: Some(0),
    vizslas: Some(0),
    goldfish: Some(5),
    trees: Some(3),
    cars: Some(2),
    perfumes: Some(1),
};

#[derive(Clone, Copy, Debug, Default)]
struct Analysis {
    children: Option<u8>,
    cats: Option<u8>,
    samoyeds: Option<u8>,
    pomeranians: Option<u8>,
    akitas: Option<u8>,
    vizslas: Option<u8>,
    goldfish: Option<u8>,
    trees: Option<u8>,
    cars: Option<u8>,
    perfumes: Option<u8>,
}

#[inline]
fn eq(a: Option<u8>, b: Option<u8>) -> bool {
    a.is_none() || b.is_none() || a == b
}

#[inline]
fn lt(a: Option<u8>, b: Option<u8>) -> bool {
    a.is_none() || b.is_none() || a < b
}

#[inline]
fn gt(a: Option<u8>, b: Option<u8>) -> bool {
    a.is_none() || b.is_none() || a > b
}

impl Analysis {
    fn matches(&self, other: &Self) -> bool {
        eq(self.children, other.children)
            && eq(self.cats, other.cats)
            && eq(self.samoyeds, other.samoyeds)
            && eq(self.pomeranians, other.pomeranians)
            && eq(self.akitas, other.akitas)
            && eq(self.vizslas, other.vizslas)
            && eq(self.goldfish, other.goldfish)
            && eq(self.trees, other.trees)
            && eq(self.cars, other.cars)
            && eq(self.perfumes, other.perfumes)
    }

    fn matches2(&self, other: &Self) -> bool {
        eq(self.children, other.children)
            && gt(self.cats, other.cats)
            && eq(self.samoyeds, other.samoyeds)
            && lt(self.pomeranians, other.pomeranians)
            && eq(self.akitas, other.akitas)
            && eq(self.vizslas, other.vizslas)
            && lt(self.goldfish, other.goldfish)
            && gt(self.trees, other.trees)
            && eq(self.cars, other.cars)
            && eq(self.perfumes, other.perfumes)
    }
}

fn find_match(analyses: &[Analysis], target: Analysis) -> Option<usize> {
    analyses
        .iter()
        .enumerate()
        .find(|(_, analysis)| analysis.matches(&target))
        .map(|(i, _)| i + 1)
}

fn find_match2(analyses: &[Analysis], target: Analysis) -> Option<usize> {
    analyses
        .iter()
        .enumerate()
        .find(|(_, analysis)| analysis.matches2(&target))
        .map(|(i, _)| i + 1)
}

fn parse_input(contents: String) -> Vec<Analysis> {
    contents
        .lines()
        .map(|line| {
            let (_, r) = line.split_once(": ").unwrap();
            let kvs = r.split(", ").map(|x| {
                let (a, b) = x.split_once(": ").unwrap();
                let b = b.parse().unwrap();
                (a, b)
            });

            let mut analysis = Analysis::default();
            for (key, value) in kvs {
                match key {
                    "children" => analysis.children = Some(value),
                    "cats" => analysis.cats = Some(value),
                    "samoyeds" => analysis.samoyeds = Some(value),
                    "pomeranians" => analysis.pomeranians = Some(value),
                    "akitas" => analysis.akitas = Some(value),
                    "vizslas" => analysis.vizslas = Some(value),
                    "goldfish" => analysis.goldfish = Some(value),
                    "trees" => analysis.trees = Some(value),
                    "cars" => analysis.cars = Some(value),
                    "perfumes" => analysis.perfumes = Some(value),
                    _ => panic!("Invalid key {key}"),
                }
            }
            analysis
        })
        .collect()
}

fn main() {
    let file_path = env::args().nth(1).unwrap();
    let contents = fs::read_to_string(file_path).unwrap();
    let analyses = parse_input(contents);
    let part_1 = find_match(&analyses, MFCSAM).unwrap();
    let part_2 = find_match2(&analyses, MFCSAM).unwrap();
    println!("part_1 = {part_1}, part_2 = {part_2}");
}
