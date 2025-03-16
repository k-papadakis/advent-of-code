use regex::Regex;
use std::ops::{Add, Mul};
use std::{
    cmp, env,
    fs::File,
    io::{BufRead, BufReader},
};

#[derive(Clone, Copy, Debug)]
struct Ingredient {
    capacity: i32,
    durability: i32,
    flavor: i32,
    texture: i32,
    calories: i32,
}

impl Mul<i32> for Ingredient {
    type Output = Ingredient;

    fn mul(self, rhs: i32) -> Ingredient {
        Ingredient {
            capacity: self.capacity * rhs,
            durability: self.durability * rhs,
            flavor: self.flavor * rhs,
            texture: self.texture * rhs,
            calories: self.calories * rhs,
        }
    }
}

impl Add for Ingredient {
    type Output = Ingredient;

    fn add(self, rhs: Ingredient) -> Ingredient {
        Ingredient {
            capacity: self.capacity + rhs.capacity,
            durability: self.durability + rhs.durability,
            flavor: self.flavor + rhs.flavor,
            texture: self.texture + rhs.texture,
            calories: self.calories + rhs.calories,
        }
    }
}

fn highest_total_score(ingredients: &[Ingredient], calories: Option<u32>) -> u32 {
    let n = 100;
    let mut max_score: u32 = 0;
    for i in 0..=n {
        for j in 0..=(n - i) {
            for k in 0..=(n - i - j) {
                let l = n - i - j - k;
                let s = ingredients[0] * i
                    + ingredients[1] * j
                    + ingredients[2] * k
                    + ingredients[3] * l;

                if calories.is_some_and(|c| s.calories != c as i32) {
                    continue;
                }

                let capacity = cmp::max(0, s.capacity) as u32;
                let durability = cmp::max(0, s.durability) as u32;
                let flavor = cmp::max(0, s.flavor) as u32;
                let texture = cmp::max(0, s.texture) as u32;

                let score = capacity * durability * flavor * texture;
                max_score = cmp::max(max_score, score);
            }
        }
    }
    max_score
}

fn read_input(file_path: &str) -> [Ingredient; 4] {
    let file = File::open(file_path).unwrap();
    let reader = BufReader::new(file);
    let re = Regex::new(r"^\w+: capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)$").unwrap();
    let ingredients: Vec<_> = reader
        .lines()
        .map(|line| {
            let line = line.unwrap();
            let (_, caps) = re.captures(&line).unwrap().extract();
            let [capacity, durability, flavor, texture, calories] =
                caps.map(|c| c.parse().unwrap());
            Ingredient {
                capacity,
                durability,
                flavor,
                texture,
                calories,
            }
        })
        .collect();
    ingredients
        .try_into()
        .expect("There should be exactly 4 ingredients")
}

fn main() {
    let file_path = env::args().nth(1).unwrap();
    let ingredients = read_input(&file_path);
    let part_1 = highest_total_score(&ingredients, None);
    let part_2 = highest_total_score(&ingredients, Some(500));
    println!("part_1 = {part_1}, part_2 = {part_2}");
}
