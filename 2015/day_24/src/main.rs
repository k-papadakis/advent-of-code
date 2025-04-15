use std::cmp::Reverse;
use std::error::Error;
use std::{env, fs};

#[derive(Clone)]
struct State<'a> {
    sum: u32,
    product: u64,
    count: u8,
    weights: &'a [u32],
}

impl<'a> State<'a> {
    fn new(weights: &'a [u32]) -> Self {
        State {
            sum: 0,
            product: 1,
            count: 0,
            weights,
        }
    }

    fn skip_weight(&self) -> Option<Self> {
        if self.weights.is_empty() {
            None
        } else {
            Some(State {
                weights: &self.weights[1..],
                ..self.clone()
            })
        }
    }

    fn take_weight(&self) -> Option<Self> {
        if self.weights.is_empty() {
            None
        } else {
            let weight = self.weights[0];
            Some(State {
                sum: self.sum + weight,
                product: self.product * weight as u64,
                count: self.count + 1,
                weights: &self.weights[1..],
            })
        }
    }

    fn reached(&self, target_sum: u32, target_count: u8) -> bool {
        self.count == target_count && self.sum == target_sum
    }

    fn exceeded(&self, target_sum: u32, target_count: u8) -> bool {
        self.count > target_count || self.sum > target_sum
    }
}

fn find_min_entanglement(weights: &[u32], target_sum: u32, target_count: u8) -> Option<u64> {
    let mut min_entanglement: Option<u64> = None;
    let mut stack = Vec::new();

    // Push initial state
    stack.push(State::new(weights));

    while let Some(state) = stack.pop() {
        if state.reached(target_sum, target_count) {
            min_entanglement = min_entanglement.map_or(Some(state.product), |current| {
                Some(current.min(state.product))
            });
            continue;
        }

        if state.exceeded(target_sum, target_count) {
            continue;
        }

        if let Some(state) = state.skip_weight() {
            stack.push(state)
        }

        if let Some(state) = state.take_weight() {
            stack.push(state)
        }
    }

    min_entanglement
}

pub fn first_bucket(weights: &[u32], nbuckets: u8) -> Option<u64> {
    let weights = {
        let mut weights = weights.to_vec();
        weights.sort_unstable_by_key(|&w| Reverse(w));
        weights
    };
    let total_sum: u32 = weights.iter().sum();
    let target_sum = total_sum / nbuckets as u32;
    (1..weights.len())
        .find_map(|target_count| find_min_entanglement(&weights, target_sum, target_count as u8))
}

fn main() -> Result<(), Box<dyn Error>> {
    let file_path = env::args().nth(1).ok_or("No file path specified")?;
    let weights: Vec<u32> = fs::read_to_string(file_path)?
        .lines()
        .map(|line| line.parse())
        .collect::<Result<_, _>>()?;
    let part_1 = first_bucket(&weights, 3).ok_or("Could not find a solution")?;
    let part_2 = first_bucket(&weights, 4).ok_or("Could not find a solution")?;
    println!("part_1 = {part_1}, part_2 = {part_2}");
    Ok(())
}
