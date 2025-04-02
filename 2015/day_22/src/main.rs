use std::{env, fs};

struct GameState {
    player_hp: u16,
    player_mp: u16,
    player_spent_mp: u16,
    player_armor: u16,
    boss_hp: u16,
    boss_dmg: u16,
    shield_ticks: u8,
    poison_ticks: u8,
    recharge_ticks: u8,
}

impl GameState {
    fn new(boss_hp: u16, boss_dmg: u16) -> Self {
        GameState {
            player_hp: 50,
            player_mp: 500,
            player_spent_mp: 0,
            player_armor: 0,
            boss_hp,
            boss_dmg,
            shield_ticks: 0,
            poison_ticks: 0,
            recharge_ticks: 0,
        }
    }

    fn cast_magic_missile(&self) -> Option<GameState> {
        let cost = 53;
        if self.player_mp < cost {
            None
        } else {
            Some(GameState {
                player_mp: self.player_mp - cost,
                player_spent_mp: self.player_spent_mp + cost,
                boss_hp: self.boss_hp.saturating_sub(4),
                ..*self
            })
        }
    }

    fn cast_drain(&self) -> Option<GameState> {
        let cost = 73;
        if self.player_mp < cost {
            None
        } else {
            Some(GameState {
                player_mp: self.player_mp - cost,
                player_spent_mp: self.player_spent_mp + cost,
                boss_hp: self.boss_hp.saturating_sub(2),
                player_hp: (self.player_hp + 2).min(50),
                ..*self
            })
        }
    }

    fn cast_shield(&self) -> Option<GameState> {
        let cost = 113;
        if self.player_mp < cost || self.shield_ticks > 0 {
            None
        } else {
            Some(GameState {
                player_mp: self.player_mp - cost,
                player_spent_mp: self.player_spent_mp + cost,
                shield_ticks: 6,
                ..*self
            })
        }
    }

    fn cast_poison(&self) -> Option<GameState> {
        let cost = 173;
        if self.player_mp < cost || self.poison_ticks > 0 {
            None
        } else {
            Some(GameState {
                player_mp: self.player_mp - cost,
                player_spent_mp: self.player_spent_mp + cost,
                poison_ticks: 6,
                ..*self
            })
        }
    }

    fn cast_recharge(&self) -> Option<GameState> {
        let cost = 229;
        if self.player_mp < cost || self.recharge_ticks > 0 {
            None
        } else {
            Some(GameState {
                player_mp: self.player_mp - cost,
                player_spent_mp: self.player_spent_mp + cost,
                recharge_ticks: 5,
                ..*self
            })
        }
    }

    fn apply_effects(&mut self) {
        if self.shield_ticks > 0 {
            self.player_armor = 7;
            self.shield_ticks -= 1;
        } else {
            self.player_armor = 0;
        }
        if self.poison_ticks > 0 {
            self.boss_hp = self.boss_hp.saturating_sub(3);
            self.poison_ticks -= 1;
        }
        if self.recharge_ticks > 0 {
            self.player_mp += 101;
            self.recharge_ticks -= 1;
        }
    }

    fn boss_attack(&mut self) {
        let damage = if self.player_armor > self.boss_dmg {
            1
        } else {
            self.boss_dmg - self.player_armor
        };
        self.player_hp = self.player_hp.saturating_sub(damage);
    }

    fn hard_mode_penalty(&mut self) {
        self.player_hp = self.player_hp.saturating_sub(1);
    }

    fn player_won(&self) -> bool {
        self.boss_hp == 0
    }

    fn player_lost(&self) -> bool {
        self.player_hp == 0
    }
}

fn dfs(initial_state: GameState, hard_mode: bool) -> Option<u16> {
    let mut stack = vec![initial_state];
    let mut min_mana: Option<u16> = None;

    fn update_min(min_mana: &mut Option<u16>, state: &GameState) {
        *min_mana = Some(min_mana.map_or(state.player_spent_mp, |m| m.min(state.player_spent_mp)));
    }

    while let Some(mut state) = stack.pop() {
        // PLAYER TURN
        if hard_mode {
            state.hard_mode_penalty();
            if state.player_lost() {
                continue;
            }
        }

        state.apply_effects();

        // Unnecessary to check because the Player hp is not affected by the specified effects
        // if state.player_lost() {
        //     continue;
        // }

        if state.player_won() {
            update_min(&mut min_mana, &state);
            continue;
        }

        // Pruning
        if let Some(min_mana) = min_mana {
            if state.player_spent_mp >= min_mana {
                continue;
            }
        }

        for mut next_state in [
            state.cast_magic_missile(),
            state.cast_drain(),
            state.cast_shield(),
            state.cast_poison(),
            state.cast_recharge(),
        ]
        .into_iter()
        .flatten()
        {
            // BOSS TURN
            next_state.apply_effects();
            if next_state.player_won() {
                update_min(&mut min_mana, &next_state);
                continue;
            }
            next_state.boss_attack();
            if !next_state.player_lost() {
                stack.push(next_state);
            }
        }
    }

    min_mana
}

fn read_input(file_path: String) -> (u16, u16) {
    let s = fs::read_to_string(file_path).unwrap();
    let mut boss_attributes = s
        .lines()
        .map(|line| line.rsplit(": ").next().unwrap().parse().unwrap());
    let boss_hp = boss_attributes.next().unwrap();
    let boss_dmg = boss_attributes.next().unwrap();
    (boss_hp, boss_dmg)
}

fn main() {
    let file_path = env::args().nth(1).unwrap();
    let (boss_hp, boss_dmg) = read_input(file_path);
    let part_1 = dfs(GameState::new(boss_hp, boss_dmg), false).unwrap();
    let part_2 = dfs(GameState::new(boss_hp, boss_dmg), true).unwrap();
    println!("part_1 = {part_1}, part_2 = {part_2}");
}
