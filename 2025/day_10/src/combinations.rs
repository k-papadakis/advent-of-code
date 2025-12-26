use std::iter;

fn gospers_hack(x: usize) -> usize {
    let lowbit = x & x.wrapping_neg();
    let increment = x + lowbit;
    (((increment ^ x) >> 2) / lowbit) | increment
}

pub fn combinations(n: usize, k: usize) -> impl Iterator<Item = usize> {
    let mut comb = (1 << k) - 1;
    iter::from_fn(move || {
        if comb < 1 << n {
            let t = comb;
            comb = gospers_hack(comb);
            Some(t)
        } else {
            None
        }
    })
}

pub fn powerset(n: usize) -> impl Iterator<Item = usize> {
    iter::chain(iter::once(0), (1..=n).flat_map(move |k| combinations(n, k)))
}

pub fn parse_combination<T>(c: usize, v: &[T]) -> impl Iterator<Item = &T> {
    (0..v.len())
        .filter(move |i| c & (1 << i) != 0)
        .map(|i| &v[i])
}
