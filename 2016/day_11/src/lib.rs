use std::collections::{HashSet, VecDeque};

type Floor = u8;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct Pair {
    pub microchip: Floor,
    pub generator: Floor,
}

#[derive(Debug, Clone, Copy)]
enum ItemType {
    Microchip,
    Generator,
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct State<const NPAIRS: usize> {
    pairs: [Pair; NPAIRS],
    elevator: Floor,
}

impl<const NPAIRS: usize> State<NPAIRS> {
    pub fn new(pairs: [Pair; NPAIRS], elevator: Floor) -> Self {
        let mut state = State { pairs, elevator };
        state.normalize();
        state
    }

    fn is_valid(&self) -> bool {
        !(0..NPAIRS as Floor).any(|floor| {
            self.pairs
                .iter()
                .filter(|pair| pair.microchip == floor)
                .any(|pair| {
                    pair.generator != floor && self.pairs.iter().any(|p| p.generator == floor)
                })
        })
    }

    fn normalize(&mut self) {
        self.pairs.sort_unstable();
    }

    fn is_goal(&self) -> bool {
        self.pairs
            .iter()
            .all(|pair| pair.microchip == 4 as Floor - 1 && pair.generator == 4 as Floor - 1)
    }

    fn next_floors(&self) -> impl Iterator<Item = u8> {
        let f = self.elevator;
        [f.checked_sub(1), if f < 3 { Some(f + 1) } else { None }]
            .into_iter()
            .flatten()
    }

    fn current_floor_indices(&self) -> Vec<(usize, ItemType)> {
        let mut items = Vec::new();
        for (i, pair) in self.pairs.iter().enumerate() {
            if pair.microchip == self.elevator {
                items.push((i, ItemType::Microchip));
            }
            if pair.generator == self.elevator {
                items.push((i, ItemType::Generator));
            }
        }
        items
    }

    fn next_states(&self) -> Vec<Self> {
        let mut states = Vec::new();
        let indices = self.current_floor_indices();

        for next_floor in self.next_floors() {
            for (start, &(idx1, item_type1)) in indices.iter().enumerate() {
                // Move one item
                let mut pairs1 = self.pairs;
                match item_type1 {
                    ItemType::Microchip => pairs1[idx1].microchip = next_floor,
                    ItemType::Generator => pairs1[idx1].generator = next_floor,
                }
                let state = State::new(pairs1, next_floor);
                if state.is_valid() {
                    states.push(state);
                }

                for &(idx2, item_type2) in &indices[start..] {
                    // Move two items
                    let mut pairs2 = pairs1;
                    match item_type2 {
                        ItemType::Microchip => pairs2[idx2].microchip = next_floor,
                        ItemType::Generator => pairs2[idx2].generator = next_floor,
                    }
                    let state = State::new(pairs2, next_floor);
                    if state.is_valid() {
                        states.push(state);
                    }
                }
            }
        }

        states
    }

    pub fn find_min_steps(&self) -> Option<u16> {
        let mut queue = VecDeque::new();
        let mut visited = HashSet::new();

        let mut normalized_state = self.clone();
        normalized_state.normalize();
        queue.push_back((normalized_state.clone(), 0));
        visited.insert(normalized_state);

        while let Some((state, steps)) = queue.pop_front() {
            if state.is_goal() {
                return Some(steps);
            }

            for next_state in state.next_states() {
                if !visited.contains(&next_state) {
                    visited.insert(next_state.clone());
                    queue.push_back((next_state, steps + 1));
                }
            }
        }

        None
    }
}

