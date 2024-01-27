use regex::Regex;
use std::{
    collections::HashMap,
    env, fs,
    ops::{Index, IndexMut},
};

const ACCEPT: &str = "A";
const REJECT: &str = "R";
const INPUT: &str = "in";

type Rating = u16;

fn main() {
    let mut args = env::args();
    let file_path: String = args.nth(1).expect("File path is required.");
    let (workflows, parts) = read_input(&file_path);

    let part_1 = parts
        .into_iter()
        .filter(|&part| workflows.accepts_part(part))
        .map(|part| part.sum())
        .sum::<isize>();

    let partrange = PartRange {
        x: ClosedInterval::new(1, 4_000),
        m: ClosedInterval::new(1, 4_000),
        a: ClosedInterval::new(1, 4_000),
        s: ClosedInterval::new(1, 4_000),
    };

    let part_2 = workflows
        .accepted_partranges(partrange)
        .map(|pr| pr.size())
        .sum::<usize>();

    println!("part_1 = {part_1}, part_2 = {part_2}");
}

#[derive(Debug, Copy, Clone)]
struct ClosedInterval {
    start: Rating,
    stop: Rating,
}

impl ClosedInterval {
    fn new(start: Rating, stop: Rating) -> Self {
        if start > stop {
            panic!("`start` should be <= `stop`");
        }
        Self { start, stop }
    }

    fn size(self) -> usize {
        (self.stop - self.start + 1).into()
    }

    fn split_lt(self, x: Rating) -> (Option<Self>, Option<Self>) {
        if x <= self.start {
            (None, Some(self))
        } else if self.stop < x {
            (Some(self), None)
        } else {
            (
                Some(Self::new(self.start, x - 1)),
                Some(Self::new(x, self.stop)),
            )
        }
    }

    fn split_gt(self, x: Rating) -> (Option<Self>, Option<Self>) {
        let (p, q) = self.split_lt(x + 1);
        (q, p)
    }
}

#[derive(Debug, Copy, Clone)]
struct Part {
    x: Rating,
    m: Rating,
    a: Rating,
    s: Rating,
}

impl Part {
    fn sum(self) -> isize {
        self.x as isize + self.m as isize + self.a as isize + self.s as isize
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
    fn size(self) -> usize {
        self.x.size() * self.m.size() * self.a.size() * self.s.size()
    }

    fn replace(mut self, var: Xmas, interval: ClosedInterval) -> Self {
        self[var] = interval;
        self
    }
}

#[derive(Debug, Copy, Clone)]
enum Xmas {
    X,
    M,
    A,
    S,
}

impl Index<Xmas> for Part {
    type Output = Rating;

    fn index(&self, index: Xmas) -> &Self::Output {
        match index {
            Xmas::X => &self.x,
            Xmas::M => &self.m,
            Xmas::A => &self.a,
            Xmas::S => &self.s,
        }
    }
}

impl Index<Xmas> for PartRange {
    type Output = ClosedInterval;

    fn index(&self, index: Xmas) -> &Self::Output {
        match index {
            Xmas::X => &self.x,
            Xmas::M => &self.m,
            Xmas::A => &self.a,
            Xmas::S => &self.s,
        }
    }
}

impl IndexMut<Xmas> for PartRange {
    fn index_mut(&mut self, index: Xmas) -> &mut Self::Output {
        match index {
            Xmas::X => &mut self.x,
            Xmas::M => &mut self.m,
            Xmas::A => &mut self.a,
            Xmas::S => &mut self.s,
        }
    }
}

#[derive(Debug)]
enum Op {
    Lt,
    Gt,
}

#[derive(Debug)]
struct Condition {
    var: Xmas,
    op: Op,
    val: Rating,
    ret: String,
}

impl Condition {
    fn satisfied_by(&self, part: Part) -> bool {
        match self.op {
            Op::Lt => part[self.var] < self.val,
            Op::Gt => part[self.var] > self.val,
        }
    }

    fn split(&self, partrange: PartRange) -> (Option<PartRange>, Option<PartRange>) {
        let (acc, rej) = match self.op {
            Op::Lt => partrange[self.var].split_lt(self.val),
            Op::Gt => partrange[self.var].split_gt(self.val),
        };

        let embed = |iv| partrange.replace(self.var, iv);

        (acc.map(embed), rej.map(embed))
    }
}

#[derive(Debug)]
struct Workflow {
    conditions: Vec<Condition>,
    otherwise: String,
}

#[derive(Debug)]
struct Workflows(HashMap<String, Workflow>);

impl Workflows {
    fn accepts_part(&self, part: Part) -> bool {
        let mut name = INPUT;

        loop {
            name = match name {
                ACCEPT | REJECT => return name == ACCEPT,
                _ => {
                    let workflow = self
                        .0
                        .get(name)
                        .expect("There should be a workflow with this name.");

                    workflow
                        .conditions
                        .iter()
                        .filter(|cond| cond.satisfied_by(part))
                        .map(|cond| &cond.ret)
                        .next()
                        .unwrap_or(&workflow.otherwise)
                }
            }
        }
    }

    fn accepted_partranges(&self, partrange: PartRange) -> PartRangeProcessor {
        let init = (
            partrange,
            self.0
                .get(INPUT)
                .expect("There should be a workflow with this name."),
            0,
        );
        PartRangeProcessor {
            workflows: self,
            pending: vec![init],
        }
    }
}

struct PartRangeProcessor<'a> {
    workflows: &'a Workflows,
    pending: Vec<(PartRange, &'a Workflow, usize)>,
}

impl Iterator for PartRangeProcessor<'_> {
    type Item = PartRange;

    fn next(&mut self) -> Option<Self::Item> {
        loop {
            let (partrange, workflow, i) = self.pending.pop()?;

            let (res, to) = if i < workflow.conditions.len() {
                let condition = &workflow.conditions[i];

                let (valid, invalid) = condition.split(partrange);

                if let Some(invalid) = invalid {
                    self.pending.push((invalid, workflow, i + 1))
                }

                match valid {
                    None => continue,
                    Some(valid) => (valid, condition.ret.as_ref()),
                }
            } else {
                (partrange, workflow.otherwise.as_ref())
            };

            match to {
                ACCEPT => return Some(res),
                REJECT => continue,
                _ => self.pending.push((
                    res,
                    self.workflows
                        .0
                        .get(to)
                        .expect("There should be a workflow with this name."),
                    0,
                )),
            }
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
                let otherwise = conditions
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
                        otherwise: otherwise.to_string(),
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
