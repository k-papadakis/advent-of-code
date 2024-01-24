#![allow(dead_code)]
#![allow(unused_variables)]

use regex::Regex;
use std::{collections::HashMap, env, fs};

fn main() {
    let mut args = env::args();
    let file_path: String = args.nth(1).expect("File path is required.");
    let (workflows, parts) = read_input(&file_path);

    let part_1: isize = parts
        .iter()
        .filter(|part| workflows.accepts_part(part))
        .map(|part| part.sum())
        .sum();

    println!("{}", part_1);
}

type Rating = u16;

#[derive(Debug, Copy, Clone)]
struct Part {
    x: Rating,
    m: Rating,
    a: Rating,
    s: Rating,
}

impl Part {
    fn get(&self, var: &Xmas) -> Rating {
        match var {
            Xmas::X => self.x,
            Xmas::M => self.m,
            Xmas::A => self.a,
            Xmas::S => self.s,
        }
    }

    fn sum(&self) -> isize {
        self.x as isize + self.m as isize + self.a as isize + self.s as isize
    }
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

#[derive(Debug, Copy, Clone, Default)]
struct ClosedInterval {
    start: Rating,
    stop: Rating,
}

impl ClosedInterval {
    fn is_empty(&self) -> bool {
        self.start > self.stop
    }

    fn size(&self) -> usize {
        if self.is_empty() {
            0
        } else {
            (self.stop - self.start + 1) as usize
        }
    }

    fn split_lt(self, x: Rating) -> (Self, Self) {
        if self.is_empty() {
            (self, Self::default())
        } else if x < self.start {
            (Self::default(), self)
        } else if self.stop < x {
            (self, Self::default())
        } else {
            (
                Self {
                    start: self.start,
                    stop: x - 1,
                },
                Self {
                    start: x,
                    stop: self.stop,
                },
            )
        }
    }

    fn split_gt(self, x: Rating) -> (Self, Self) {
        let (p, q) = self.split_lt(x + 1);
        (q, p)
    }
}

#[derive(Debug, Copy, Clone)]
struct PartRange {
    x: ClosedInterval,
    m: ClosedInterval,
    a: ClosedInterval,
    s: ClosedInterval,
}

impl PartRange {
    fn size(&self) -> usize {
        self.x.size() * self.m.size() * self.a.size() * self.s.size()
    }

    fn get(self, var: &Xmas) -> ClosedInterval {
        match var {
            Xmas::X => self.x,
            Xmas::M => self.m,
            Xmas::A => self.a,
            Xmas::S => self.s,
        }
    }

    fn replace(self, var: &Xmas, iv: ClosedInterval) -> Self {
        match var {
            Xmas::X => Self { x: iv, ..self },
            Xmas::M => Self { m: iv, ..self },
            Xmas::A => Self { a: iv, ..self },
            Xmas::S => Self { s: iv, ..self },
        }
    }

    fn split(self, condition: &Condition) -> (Self, Self) {
        let iv = self.get(&condition.var);

        let (acc_iv, rej_iv) = match condition.op {
            Op::Lt => iv.split_lt(condition.val),
            Op::Gt => iv.split_gt(condition.val),
        };

        let acc = self.replace(&condition.var, acc_iv);
        let rej = self.replace(&condition.var, rej_iv);

        (acc, rej)
    }
}

#[derive(Debug)]
struct Condition {
    var: Xmas,
    op: Op,
    val: Rating,
    ret: String,
}

impl Condition {
    fn satisfied_by(&self, x: Rating) -> bool {
        match self.op {
            Op::Lt => x < self.val,
            Op::Gt => x > self.val,
        }
    }
}

#[derive(Debug)]
struct Workflow {
    conditions: Vec<Condition>,
    otherwise: String,
}

impl Workflow {
    fn process_part(&self, part: &Part) -> &str {
        self.conditions
            .iter()
            .filter(|cond| cond.satisfied_by(part.get(&cond.var)))
            .map(|cond| &cond.ret)
            .next()
            .unwrap_or(&self.otherwise)
    }
}

#[derive(Debug)]
struct Workflows(HashMap<String, Workflow>);

impl Workflows {
    fn accepts_part(&self, part: &Part) -> bool {
        let mut name = "in";

        loop {
            if name == "A" {
                return true;
            }
            if name == "R" {
                return false;
            }
            let workflow = self
                .0
                .get(name)
                .expect("Workflows should contain this name");
            name = workflow.process_part(part);
        }
    }
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

                        let val = val.parse::<Rating>().expect("Val should be parseable");

                        let ret = ret.to_owned();

                        Condition { op, var, val, ret }
                    })
                    .collect();

                (
                    name.to_string(),
                    Workflow {
                        conditions,
                        otherwise: else_.to_string(),
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
            let [x, m, a, s] = cap
                .extract()
                .1
                .map(|t| t.parse::<Rating>().expect("Part value should be parseable"));
            Part { x, m, a, s }
        })
        .collect()
}
