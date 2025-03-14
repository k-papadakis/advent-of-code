use serde_json::Value;
use std::{env, fs::File, io::BufReader};

fn sum_nums(json: &Value) -> i64 {
    match json {
        Value::Number(number) => number.as_i64().unwrap(),
        Value::Array(values) => values.iter().map(sum_nums).sum(),
        Value::Object(map) => map.values().map(sum_nums).sum(),
        _ => 0,
    }
}

fn sum_nums_non_red(json: &Value) -> i64 {
    match json {
        Value::Number(number) => number.as_i64().unwrap(),
        Value::Array(values) => values.iter().map(sum_nums_non_red).sum(),
        Value::Object(map) => {
            let has_red = map.values().any(|v| v.as_str().is_some_and(|x| x == "red"));
            if has_red {
                0
            } else {
                map.values().map(sum_nums_non_red).sum()
            }
        }
        _ => 0,
    }
}

fn main() {
    let file_path = env::args().nth(1).unwrap();
    let file = File::open(file_path).unwrap();
    let reader = BufReader::new(file);
    let json: Value = serde_json::from_reader(reader).unwrap();
    let part_1 = sum_nums(&json);
    let part_2 = sum_nums_non_red(&json);
    println!("part_1 = {part_1}, part_2 = {part_2}");
}
