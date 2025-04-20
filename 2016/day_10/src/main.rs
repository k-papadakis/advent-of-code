use std::collections::HashMap;

type BotId = u8;
type OutputId = u8;
type Value = u8;
type Bots = HashMap<BotId, Bot>;
type Outputs = HashMap<OutputId, Value>;

#[derive(Debug, Clone, Copy)]
enum Target {
    Bot(BotId),
    Output(OutputId),
}

#[derive(Debug)]
struct Bot {
    low_target: Target,
    high_target: Target,
    low_value: Option<Value>,
    high_value: Option<Value>,
}

impl Bot {
    fn new(low_target: Target, high_target: Target) -> Self {
        Self {
            low_target,
            high_target,
            low_value: None,
            high_value: None,
        }
    }

    fn put_value(&mut self, value: Value) {
        match (self.low_value, self.high_value) {
            (None, None) => {
                self.low_value = Some(value);
            }
            (Some(low), None) => {
                if value >= low {
                    self.high_value = Some(value);
                } else {
                    self.high_value = self.low_value.take();
                    self.low_value = Some(value);
                }
            }
            (None, Some(_)) => {
                unreachable!("If the bot has a single value, it must be a low_value");
            }
            (Some(_), Some(_)) => {
                panic!("Bot already has two values");
            }
        }
    }

    fn is_ready(&self) -> bool {
        self.low_value.is_some() && self.high_value.is_some()
    }
}

fn simulate_bots(bots: &mut Bots, intercept: (Value, Value)) -> (Outputs, BotId) {
    let mut outputs = HashMap::new();
    let mut intercept_bot_id = None;
    let mut ready_bots_stack = bots
        .iter()
        .filter(|(_, bot)| bot.is_ready())
        .map(|(&id, _)| id)
        .collect::<Vec<_>>();

    while let Some(bot_id) = ready_bots_stack.pop() {
        let transfers = {
            let bot = bots.get_mut(&bot_id).unwrap();
            [
                (bot.low_target, bot.low_value.take().unwrap()),
                (bot.high_target, bot.high_value.take().unwrap()),
            ]
        };

        if transfers[0].1 == intercept.0 && transfers[1].1 == intercept.1 {
            intercept_bot_id = Some(bot_id);
        }

        for (target, value) in transfers {
            match target {
                Target::Bot(target_id) => {
                    let target_bot = bots.get_mut(&target_id).unwrap();
                    target_bot.put_value(value);
                    if target_bot.is_ready() {
                        ready_bots_stack.push(target_id);
                    }
                }
                Target::Output(target_id) => {
                    outputs.insert(target_id, value);
                }
            }
        }
    }

    (outputs, intercept_bot_id.unwrap())
}

fn parse_input(contents: String) -> Bots {
    let val_lines = contents
        .lines()
        .filter_map(|line| line.strip_prefix("value"));
    let bot_lines = contents.lines().filter_map(|line| line.strip_prefix("bot"));

    let mut bots: HashMap<BotId, Bot> = bot_lines
        .map(|line| {
            let mut parts = line.split_whitespace();
            let source_bot_id: BotId = parts.next().unwrap().parse().unwrap();
            let low_target_type = parts.nth(3).unwrap();
            let low_target_id: BotId = parts.next().unwrap().parse().unwrap();
            let high_target_type = parts.nth(3).unwrap();
            let high_target_id: BotId = parts.next().unwrap().parse().unwrap();

            let low_target = match low_target_type {
                "bot" => Target::Bot(low_target_id),
                "output" => Target::Output(low_target_id),
                _ => panic!("Unknown target type"),
            };

            let high_target = match high_target_type {
                "bot" => Target::Bot(high_target_id),
                "output" => Target::Output(high_target_id),
                _ => panic!("Unknown target type"),
            };

            (source_bot_id, Bot::new(low_target, high_target))
        })
        .collect();

    for line in val_lines {
        let mut parts = line.split_whitespace();
        let value: Value = parts.next().unwrap().parse().unwrap();
        let bot_id: BotId = parts.nth(3).unwrap().parse().unwrap();
        bots.entry(bot_id).and_modify(|bot| bot.put_value(value));
    }

    bots
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file_path = std::env::args().nth(1).ok_or("No file path provided")?;
    let contents = std::fs::read_to_string(file_path)?;
    let mut bots = parse_input(contents);
    let (outputs, part_1) = simulate_bots(&mut bots, (17, 61));
    let part_2 = *outputs.get(&0).unwrap() as u64
        * *outputs.get(&1).unwrap() as u64
        * *outputs.get(&2).unwrap() as u64;
    println!("part_1 = {part_1}, part_2 = {part_2}");

    Ok(())
}
