pub mod combinations;
use std::{array, collections::HashMap, iter, str::FromStr};

type Lights = [u8; 10];

#[derive(Debug, Clone)]
pub struct Machine {
    pub parity: Lights,
    pub buttons: Vec<Lights>,
    pub joltage: Lights,
}

impl Machine {
    pub fn num_presses1(&self) -> Option<usize> {
        iter_button_combos(&self.buttons).find_map(|(combsize, parity, _)| {
            if parity == self.parity {
                Some(combsize)
            } else {
                None
            }
        })
    }

    pub fn num_presses2(&self) -> Option<usize> {
        let mut parity_combs: HashMap<_, Vec<_>> = HashMap::new();
        for (combsize, parity, joltage) in iter_button_combos(&self.buttons) {
            parity_combs
                .entry(parity)
                .or_default()
                .push((combsize, joltage))
        }

        num_presses2(self.joltage, &parity_combs)
    }
}

fn num_presses2(
    rem_joltage: Lights,
    parity_combs: &HashMap<Lights, Vec<(usize, Lights)>>,
) -> Option<usize> {
    if rem_joltage == [0; _] {
        return Some(0);
    }

    let parity = rem_joltage.map(|x| x % 2);
    parity_combs
        .get(&parity)?
        .iter()
        .filter_map(|(combsize, joltage)| {
            if iter::zip(rem_joltage, joltage).all(|(rj, &j)| rj >= j) {
                let new_rem = array::from_fn(|i| (rem_joltage[i] - joltage[i]) / 2);
                Some(combsize + 2 * num_presses2(new_rem, parity_combs)?)
            } else {
                None
            }
        })
        .min()
}

fn iter_button_combos(buttons: &[Lights]) -> impl Iterator<Item = (usize, Lights, Lights)> {
    // representing combinations as integers to avoid heap allocations
    combinations::powerset(buttons.len()).map(|comb_n| {
        let combsize = comb_n.count_ones() as usize;

        let mut joltage = [0; _];
        for button in combinations::parse_combination(comb_n, buttons) {
            for (j, b) in joltage.iter_mut().zip(button) {
                *j += b
            }
        }

        let parity = joltage.map(|x| x % 2);

        (combsize, parity, joltage)
    })
}

impl FromStr for Machine {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut chars = s.chars().filter(|&c| c != ' ');

        let mut parity: Lights = [0; _];
        let mut buttons = Vec::new();
        let mut joltage: Lights = [0; _];

        while let Some(c) = chars.next() {
            match c {
                '[' => {
                    for (i, c) in chars.by_ref().take_while(|&c| c != ']').enumerate() {
                        match c {
                            '#' => parity[i] = 1,
                            '.' => continue,
                            other => return Err(format!("invalid character {other}")),
                        }
                    }
                }
                '(' => {
                    let mut button: Lights = [0; _];
                    let mut n = 0;
                    for c in chars.by_ref().take_while(|&c| c != ')') {
                        match c {
                            ',' => {
                                button[n] = 1;
                                n = 0;
                            }
                            d => {
                                let d = d.to_digit(10).ok_or(format!("invalid character {d}"))?;
                                n = 10 * n + d as usize;
                            }
                        }
                    }
                    button[n] = 1;
                    buttons.push(button);
                }
                '{' => {
                    let mut n = 0;
                    let mut i = 0;
                    for c in chars.by_ref().take_while(|&c| c != '}') {
                        match c {
                            ',' => {
                                joltage[i] = n;
                                n = 0;
                                i += 1;
                            }
                            d => {
                                let d = d.to_digit(10).ok_or(format!("invalid character {d}"))?;
                                n = 10 * n + d as u8;
                            }
                        }
                    }
                    joltage[i] = n;
                }
                ' ' => continue,
                other => return Err(format!("invalid character {other}")),
            }
        }

        Ok(Self {
            parity,
            buttons,
            joltage,
        })
    }
}
