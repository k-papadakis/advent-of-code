use md5::{Digest, Md5};

fn compute_md5_hash(index: u32, secret_key: impl AsRef<[u8]>) -> [u8; 16] {
    let mut hasher = Md5::new();
    hasher.update(secret_key);
    hasher.update(index.to_string());
    hasher.finalize().into()
}

fn get_password_digit(hash: [u8; 16]) -> Option<u8> {
    if hash[0] == 0 && hash[1] == 0 && hash[2] & 0xf0 == 0 {
        Some(hash[2] & 0x0f)
    } else {
        None
    }
}

fn get_ordered_password_digit(hash: [u8; 16]) -> Option<(u8, u8)> {
    if hash[0] == 0 && hash[1] == 0 && hash[2] & 0xf0 == 0 && hash[2] & 0x0f < 8 {
        Some((hash[2] & 0x0f, hash[3] >> 4))
    } else {
        None
    }
}

fn find_password_1(secret_key: impl AsRef<[u8]>) -> String {
    let password = (0..)
        .map(|index| compute_md5_hash(index, &secret_key))
        .filter_map(get_password_digit)
        .take(8)
        .fold(0u32, |pass, x| (pass << 4) | x as u32);
    format!("{password:08x}")
}

fn find_password_2(secret_key: impl AsRef<[u8]>) -> String {
    let mut bitset = 0u8;
    let password = (0..)
        .map(|index| compute_md5_hash(index, &secret_key))
        .filter_map(get_ordered_password_digit)
        .filter(|(pos, _)| {
            if bitset & (1 << pos) != 0 {
                false
            } else {
                bitset |= 1 << pos;
                true
            }
        })
        .take(8)
        .fold(0u32, |pass, (pos, digit)| {
            pass | ((digit as u32) << (4 * (7 - pos)))
        });
    format!("{password:08x}")
}

fn main() {
    let secret_key = b"abbhdwsy";
    let part_1 = find_password_1(secret_key);
    let part_2 = find_password_2(secret_key);
    println!("part_1 = {part_1}, part_2 = {part_2}");
}
