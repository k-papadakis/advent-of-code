use std::{collections::HashSet, env, fs};

fn supports_tls(ip: &str) -> bool {
    let ip = ip.as_bytes();
    let mut res = false;
    let mut in_brackets = false;

    for i in 0..(ip.len() - 3) {
        if ip[i] == b'[' {
            in_brackets = true;
            continue;
        } else if ip[i] == b']' {
            in_brackets = false;
            continue;
        }

        if ip[i] == ip[i + 3] && ip[i + 1] == ip[i + 2] && ip[i] != ip[i + 1] {
            if in_brackets {
                return false;
            }
            res = true;
        }
    }

    res
}

fn supports_ssl(ip: &str) -> bool {
    let ip = ip.as_bytes();
    let mut bracketed = HashSet::new();
    let mut unbracketed = HashSet::new();
    let mut in_brackets = false;

    for i in 0..(ip.len() - 2) {
        if ip[i] == b'[' {
            in_brackets = true;
            continue;
        } else if ip[i] == b']' {
            in_brackets = false;
            continue;
        }

        if ip[i] == ip[i + 2] && ip[i] != ip[i + 1] {
            if in_brackets {
                if unbracketed.contains(&(ip[i + 1], ip[i])) {
                    return true;
                }
                bracketed.insert((ip[i], ip[i + 1]));
            } else {
                if bracketed.contains(&(ip[i + 1], ip[i])) {
                    return true;
                }
                unbracketed.insert((ip[i], ip[i + 1]));
            }
        }
    }

    false
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file_path = env::args().nth(1).ok_or("file path not provided")?;
    let contents = fs::read_to_string(file_path)?;
    let part_1 = contents.lines().filter(|&line| supports_tls(line)).count();
    let part_2 = contents.lines().filter(|&line| supports_ssl(line)).count();
    println!("part_1 = {part_1}, part_2 = {part_2}");
    Ok(())
}
