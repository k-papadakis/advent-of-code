#![allow(dead_code)]
#![allow(unused_variables)]

//TODO: Optimize parsing. Build regexes once.

use regex::Regex;
use std::{
    collections::HashMap,
    env,
    fs::File,
    io::{BufRead, BufReader},
    ops::Range,
    str::FromStr,
};

fn main() {
    let mut args = env::args();
    let file_path: String = args.nth(1).unwrap();
    let (system, parts) = read_input(&file_path);
    println!("{:?}", &parts[0])
}

fn read_input(file_path: &str) -> (System, Vec<Part>) {
    let file = File::open(file_path).unwrap();
    let reader = BufReader::new(file);
    let mut lines = reader.lines();

    lines.next();

    let workflows = lines
        .by_ref()
        .take_while(|line| line.as_ref().unwrap() != "")
        .map(|s| Workflow::from_str(&s.unwrap()))
        .collect::<Result<Vec<Workflow>, _>>()
        .unwrap();

    let parts: Vec<_> = lines
        .map(|s| Part::from_str(&s.unwrap()).unwrap())
        .collect();

    (System::from(workflows), parts)
}

#[derive(Debug)]
struct Part {
    x: u16,
    m: u16,
    a: u16,
    s: u16,
}

#[derive(Debug)]
enum Op {
    Lt,
    Gt,
}

#[derive(Debug)]
enum Xmas {
    X,
    M,
    A,
    S,
}

#[derive(Debug)]
struct PartRange {
    x: Range<u16>,
    m: Range<u16>,
    a: Range<u16>,
    s: Range<u16>,
}

#[derive(Debug)]
struct Condition {
    var: Xmas,
    op: Op,
    val: u16,
    ret: String,
}

struct Workflow {
    name: String,
    conditions: Vec<Condition>,
    else_: String,
}

struct System(HashMap<String, Workflow>);

impl From<Vec<Workflow>> for System {
    fn from(workflows: Vec<Workflow>) -> Self {
        System(
            workflows
                .into_iter()
                .map(|w| (w.name.clone(), w))
                .collect::<HashMap<_, _>>(),
        )
    }
}

// Input Parsing

// enum ParseInputError {
//     RegexError(regex::Error),
//     NoMatch,
//     ParseInt(ParseIntError),
//     InvalidOp,
//     InvalidXmas,
// }

impl FromStr for Part {
    type Err = regex::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let re = Regex::new(r"^\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}")?;
        let caps = re.captures(s).unwrap();
        let [x, m, a, s] = caps.extract().1.map(|t| t.parse::<u16>().unwrap());

        Ok(Part { x, m, a, s })
    }
}

impl FromStr for Op {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "<" => Ok(Op::Lt),
            ">" => Ok(Op::Gt),
            _ => Err(String::from("Invalid op-string")),
        }
    }
}

impl FromStr for Xmas {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "x" => Ok(Xmas::X),
            "m" => Ok(Xmas::M),
            "a" => Ok(Xmas::A),
            "s" => Ok(Xmas::S),
            _ => Err(String::from("Invalid xmas")),
        }
    }
}

impl FromStr for Condition {
    type Err = regex::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let re = Regex::new(r"(?<var>x|m|a|s)(?<op><|>)(?<val>\d+):(?<ret>\w+)")?;
        let caps = re.captures(s).unwrap();
        let [var, op, val, ret] = caps.extract().1;

        Ok(Condition {
            var: Xmas::from_str(var).unwrap(),
            op: Op::from_str(op).unwrap(),
            val: val.parse::<u16>().unwrap(),
            ret: ret.into(),
        })
    }
}
impl FromStr for Workflow {
    type Err = regex::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let re = Regex::new(r"(?<name>.*?)\{(?<logic>.*?)\}").unwrap();
        let caps = re.captures(s).unwrap();
        let [name, logic] = caps.extract().1;
        let mut logic: Vec<_> = logic.split(',').collect();
        let else_ = logic.pop().unwrap();
        let conditions: Vec<Condition> = logic
            .into_iter()
            .map(Condition::from_str)
            .collect::<Result<Vec<Condition>, _>>()?;
        Ok(Workflow {
            name: name.into(),
            conditions,
            else_: else_.into(),
        })
    }
}
