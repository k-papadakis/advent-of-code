use std::{cmp, env, fs, iter};

#[derive(Debug)]
struct Item {
    cost: u16,
    damage: u16,
    armor: u16,
}

const NO_ITEM: Item = Item {
    cost: 0,
    damage: 0,
    armor: 0,
};

#[derive(Debug)]
struct Monster {
    hit_points: u16,
    damage: u16,
    armor: u16,
}

impl Monster {
    fn can_beat(&self, other: &Self) -> bool {
        let self_dps = cmp::max(self.damage.saturating_sub(other.armor), 1);
        let other_dps = cmp::max(other.damage.saturating_sub(self.armor), 1);
        let self_win_t = other.hit_points.div_ceil(self_dps);
        let other_win_t = self.hit_points.div_ceil(other_dps);
        self_win_t <= other_win_t
    }
}

struct Vendor {
    weapons: Vec<Item>,
    armors: Vec<Item>,
    rings: Vec<Item>,
}

impl Vendor {
    #[rustfmt::skip]
    fn make() -> Self {
        Self {
            weapons : vec![
                Item { cost: 8, damage: 4, armor: 0 },
                Item { cost: 10, damage: 5, armor: 0 },
                Item { cost: 25, damage: 6, armor: 0 },
                Item { cost: 40, damage: 7, armor: 0 },
                Item { cost: 74, damage: 8, armor: 0 },
            ],
            armors : vec![
                Item { cost: 13, damage: 0, armor: 1 },
                Item { cost: 31, damage: 0, armor: 2 },
                Item { cost: 53, damage: 0, armor: 3 },
                Item { cost: 75, damage: 0, armor: 4 },
                Item { cost: 102, damage: 0, armor: 5 },
            ],
            rings : vec![
                Item { cost: 25, damage: 1, armor: 0 },
                Item { cost: 50, damage: 2, armor: 0 },
                Item { cost: 100, damage: 3, armor: 0 },
                Item { cost: 20, damage: 0, armor: 1 },
                Item { cost: 40, damage: 0, armor: 2 },
                Item { cost: 80, damage: 0, armor: 3 },
            ],
    }
    }

    fn iter_specs(&self, player_hp: u16) -> impl Iterator<Item = (u16, Monster)> {
        self.weapons
            .iter()
            .flat_map(|w| {
                self.armors
                    .iter()
                    .chain(iter::once(&NO_ITEM))
                    .map(move |a| (w, a))
            })
            .flat_map(move |(w, a)| {
                iter::once(&NO_ITEM)
                    .chain(self.rings.iter())
                    .enumerate()
                    .flat_map(move |(i, r1)| {
                        self.rings[i..]
                            .iter()
                            .chain(iter::once(&NO_ITEM))
                            .map(move |r2| {
                                let player = Monster {
                                    hit_points: player_hp,
                                    armor: w.armor + a.armor + r1.armor + r2.armor,
                                    damage: w.damage + a.damage + r1.damage + r2.damage,
                                };
                                let cost = w.cost + a.cost + r1.cost + r2.cost;
                                (cost, player)
                            })
                    })
            })
    }
}

fn read_input(file_path: String) -> Monster {
    let s = fs::read_to_string(file_path).unwrap();
    let mut attributes = s
        .lines()
        .map(|line| line.rsplit(": ").next().unwrap().parse().unwrap());
    Monster {
        hit_points: attributes.next().unwrap(),
        damage: attributes.next().unwrap(),
        armor: attributes.next().unwrap(),
    }
}

fn main() {
    let file_path = env::args().nth(1).unwrap();
    let boss = read_input(file_path);
    let vendor = Vendor::make();

    let part_1 = vendor
        .iter_specs(100)
        .filter(|(_, player)| player.can_beat(&boss))
        .map(|(cost, _)| cost)
        .min()
        .unwrap();

    let part_2 = vendor
        .iter_specs(100)
        .filter(|(_, player)| !player.can_beat(&boss))
        .map(|(cost, _)| cost)
        .max()
        .unwrap();

    println!("part_1 = {part_1}, part_2 = {part_2}");
}
