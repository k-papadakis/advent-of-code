use md5::{Digest, Md5};
use std::{array, mem};

fn hash_index_with_salt(index: u32, salt: impl AsRef<[u8]>) -> [u8; 16] {
    let mut hasher = Md5::new();
    hasher.update(salt);
    hasher.update(index.to_string());
    hasher.finalize().into()
}

fn repeat_hash(bytes: [u8; 16], reps: usize) -> [u8; 16] {
    let mut bytes = bytes;
    let mut hasher = Md5::new();
    let mut hash = [0u8; 32];
    for _ in 0..reps {
        hex::encode_to_slice(bytes, &mut hash).unwrap();
        hasher.update(hash);
        bytes = hasher.finalize_reset().into();
    }
    bytes
}

fn to_half_bytes(bytes: [u8; 16]) -> [u8; 32] {
    let half_bytes = bytes.map(|b| [b >> 4, b & 0x0f]);
    unsafe { mem::transmute::<[[u8; 2]; 16], [u8; 32]>(half_bytes) }
}

fn all_eq<T: PartialEq>(v: &[T]) -> bool {
    v.windows(2).all(|w| w[0] == w[1])
}

fn find_64th_key(hash_iter: impl Iterator<Item = [u8; 32]>) -> usize {
    let mut candidates: [Vec<usize>; 16] = array::from_fn(|_| vec![]);
    let mut keys: Vec<usize> = vec![];

    for (i, hash) in hash_iter.enumerate() {
        let streak5 = hash
            .windows(5)
            .filter_map(|w| if all_eq(w) { Some(w[0]) } else { None });

        for t5 in streak5 {
            let (matches, remaining) = candidates[t5 as usize]
                .iter()
                .partition(|&j| i - j <= 1_000);
            candidates[t5 as usize] = remaining;
            keys.extend(matches);
        }

        let first_streak3 = hash
            .windows(3)
            .find_map(|w| if all_eq(w) { Some(w[0]) } else { None });

        if let Some(t3) = first_streak3 {
            candidates[t3 as usize].push(i);
        }

        if keys.len() >= 64 {
            break;
        }
    }
    keys[63]
}

fn main() {
    const SECRET_KEY: &[u8] = b"cuanljph";

    let hash_iter_1 = (0..)
        .map(move |index| hash_index_with_salt(index, SECRET_KEY))
        .map(to_half_bytes);
    let hash_iter_2 = (0..)
        .map(move |index| hash_index_with_salt(index, SECRET_KEY))
        .map(|bytes| repeat_hash(bytes, 2016))
        .map(to_half_bytes);

    let part_1 = find_64th_key(hash_iter_1);
    let part_2 = find_64th_key(hash_iter_2);
    println!("Part 1: {part_1}\nPart 2: {part_2}");
}
