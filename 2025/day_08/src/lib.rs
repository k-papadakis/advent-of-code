use std::cmp::Ordering;

pub struct UnionFind {
    parents: Vec<usize>,
    ranks: Vec<usize>,
}

impl UnionFind {
    pub fn new(n: usize) -> Self {
        Self {
            parents: (0..n).collect(),
            ranks: vec![0; n],
        }
    }

    pub fn find(&mut self, x: usize) -> usize {
        if self.parents[x] == x {
            x
        } else {
            self.parents[x] = self.find(self.parents[x]);
            self.parents[x]
        }
    }

    pub fn union(&mut self, x: usize, y: usize) -> bool {
        let x = self.find(x);
        let y = self.find(y);

        if x == y {
            return false;
        }

        let rx = self.ranks[x];
        let ry = self.ranks[y];

        match rx.cmp(&ry) {
            Ordering::Less => {
                self.parents[x] = y;
            }
            Ordering::Greater => {
                self.parents[y] = x;
            }
            Ordering::Equal => {
                self.parents[y] = x;
                self.ranks[x] += 1;
            }
        }
        true
    }

    pub fn labels(&mut self) -> &[usize] {
        for i in 0..self.parents.len() {
            self.find(i);
        }
        &self.parents
    }
}
