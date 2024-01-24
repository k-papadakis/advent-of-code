#![allow(dead_code)]
#![allow(unused_variables)]

use regex::Regex;
use std::{collections::HashMap, env, fs, ops::Range};

fn main() {
    let mut args = env::args();
    let file_path: String = args.nth(1).expect("File path is required.");
    let (workflows, parts) = read_input(&file_path);
}

fn read_input(file_path: &str) -> (Workflows, Vec<Part>) {
    let data = fs::read_to_string(file_path).expect("Should be able to read from `file_path`.");
    let (workflows, parts) = data
        .split_once("\n\n")
        .expect("Workflows should be followed by an empty line, followed by Parts");

    (parse_workflows(workflows), parse_parts(parts))
}

fn parse_workflows(workflows: &str) -> Workflows {
    let workflow_re = Regex::new(r"(?m)^(?<name>.*?)\{(?<logic>.*?)\}")
        .expect("Hardcoded regex should always be valid.");
    let condition_re = Regex::new(r"(?m)^(?<var>x|m|a|s)(?<op><|>)(?<val>\d+):(?<ret>\w+)")
        .expect("Hardcoded regex should always be valid.");

    Workflows(
        workflow_re
            .captures_iter(workflows)
            .map(|cap| {
                let [name, logic] = cap.extract().1;
                let mut conditions: Vec<_> = logic.split(',').collect();
                let else_ = conditions
                    .pop()
                    .expect("A condition should always contain an `else`.");

                let conditions: Vec<_> = conditions
                    .into_iter()
                    .map(|condition| {
                        let caps = condition_re
                            .captures(condition)
                            .expect("Conditions should always be valid.");
                        let [var, op, val, ret] = caps.extract().1;

                        let var = match var {
                            "x" => Xmas::X,
                            "m" => Xmas::M,
                            "a" => Xmas::A,
                            "s" => Xmas::S,
                            _ => panic!("Var should be in x, m, a, s."),
                        };

                        let op: Op = match op {
                            "<" => Op::Lt,
                            ">" => Op::Gt,
                            _ => panic!("Op should be in >, <."),
                        };

                        let val = val.parse::<u16>().expect("Val should be u16-parseable");

                        let ret = ret.to_owned();

                        Condition { op, var, val, ret }
                    })
                    .collect();

                let name = name.to_owned();

                (
                    name,
                    Workflow {
                        conditions,
                        else_: else_.to_owned(),
                    },
                )
            })
            .collect(),
    )
}

fn parse_parts(parts: &str) -> Vec<Part> {
    let part_re = Regex::new(r"(?m)^\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}")
        .expect("Hardcoded regex should always be valid.");

    part_re
        .captures_iter(parts)
        .map(|cap| {
            let [x, m, a, s] = cap.extract().1.map(|t| {
                t.parse::<u16>()
                    .expect("Part value should be u16-parseable")
            });
            Part { x, m, a, s }
        })
        .collect()
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

#[derive(Debug)]
struct Workflow {
    conditions: Vec<Condition>,
    else_: String,
}

#[derive(Debug)]
struct Workflows(HashMap<String, Workflow>);
