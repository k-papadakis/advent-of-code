use md5::{Digest, Md5};
use std::{env, fs};

fn crack_md5(secret_key: &str, res_prefix: &str) -> u32 {
    let mut i: u32 = 0;
    let mut hasher = Md5::new();
    loop {
        hasher.update(secret_key);
        hasher.update(i.to_string());
        let res = hasher.finalize_reset();
        if format!("{res:x}").starts_with(res_prefix) {
            return i;
        } else {
            i += 1
        }
    }
}

fn main() {
    let file_path = env::args().nth(1).unwrap();
    let secret_key_raw = fs::read_to_string(&file_path).unwrap();
    let secret_key = secret_key_raw.strip_suffix('\n').unwrap_or(&secret_key_raw);

    let part_1 = crack_md5(secret_key, "00000");
    let part_2 = crack_md5(secret_key, "000000");
    println!("part_1 = {part_1}, part_2 = {part_2}");
}
