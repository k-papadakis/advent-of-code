use regex::Regex;
use std::{collections::HashMap, env, fs};

fn main() {
    let mut args = env::args();
    let file_path: String = args.nth(1).expect("File path is required.");
    let (workflows, parts) = read_input(&file_path);

    let part_1 = parts
        .into_iter()
        .filter(|&part| workflows.accepts_part(part))
        .map(|part| part.sum())
        .sum::<usize>();

    let part_range = PartRange {
        x: ClosedInterval::new(1, 4_000),
        m: ClosedInterval::new(1, 4_000),
        a: ClosedInterval::new(1, 4_000),
        s: ClosedInterval::new(1, 4_000),
    };

    let part_2: usize = workflows
        .accepted_part_ranges(part_range)
        .into_iter()
        .map(|pr| pr.size())
        .sum::<usize>();

    println!("part_1 = {part_1}, part_2 = {part_2}");
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
    fn get(self, var: &Xmas) -> Rating {
        match var {
            Xmas::X => self.x,
            Xmas::M => self.m,
            Xmas::A => self.a,
            Xmas::S => self.s,
        }
    }

    fn sum(self) -> usize {
        self.x as usize + self.m as usize + self.a as usize + self.s as usize
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

    fn split(self, condition: &Condition) -> (Option<Self>, Option<Self>) {
        let iv = self.get(&condition.var);

        let (acc_iv, rej_iv) = match condition.op {
            Op::Lt => iv.split_lt(condition.val),
            Op::Gt => iv.split_gt(condition.val),
        };

        let acc_pr = acc_iv.map(|iv| self.replace(&condition.var, iv));
        let rej_pr = rej_iv.map(|iv| self.replace(&condition.var, iv));

        (acc_pr, rej_pr)
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
    fn process_part(&self, part: Part) -> &str {
        self.conditions
            .iter()
            .filter(|cond| cond.satisfied_by(part.get(&cond.var)))
            .map(|cond| &cond.ret)
            .next()
            .unwrap_or(&self.otherwise)
    }

    fn process_part_range(&self, part_range: PartRange) -> Vec<(PartRange, &str)> {
        let mut pending = vec![(part_range, 0_usize)];
        let mut results: Vec<(PartRange, &str)> = Vec::new();

        while let Some((pr, i)) = pending.pop() {
            if i < self.conditions.len() {
                let condition = &self.conditions[i];
                let (accepted, rejected) = pr.split(condition);

                if let Some(accepted) = accepted {
                    results.push((accepted, &condition.ret));
                }

                if let Some(rejected) = rejected {
                    pending.push((rejected, i + 1))
                }
            } else {
                results.push((pr, &self.otherwise));
            }
        }
        results
    }
}

#[derive(Debug)]
struct Workflows(HashMap<String, Workflow>);

impl Workflows {
    fn accepts_part(&self, part: Part) -> bool {
        let mut name = "in";

        loop {
            name = match name {
                "A" | "R" => return name == "A",
                _ => self
                    .0
                    .get(name)
                    .expect("There should be a workflow with this name.")
                    .process_part(part),
            }
        }
    }

    fn accepted_part_ranges(&self, part_range: PartRange) -> Vec<PartRange> {
        let mut res = Vec::new();
        let mut stack = vec![(part_range, "in")];

        loop {
            match stack.pop() {
                None => return res,
                Some((pr, "A")) => res.push(pr),
                Some((_, "R")) => continue,
                Some((pr, name)) => {
                    let mut processed = self
                        .0
                        .get(name)
                        .expect("There should be a workflow with this name.")
                        .process_part_range(pr);
                    stack.append(&mut processed);
                }
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
