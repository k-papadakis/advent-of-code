use std::{collections::HashMap, hash::Hash};

#[derive(Debug)]
struct NodeIndex<T: Eq + Hash> {
    max_id: usize,
    node_index: HashMap<T, usize>,
}

impl<T: Eq + Hash> NodeIndex<T> {
    fn new() -> Self {
        Self {
            max_id: 0,
            node_index: HashMap::new(),
        }
    }
    fn index(&mut self, node: T) -> usize {
        *self.node_index.entry(node).or_insert_with(|| {
            let node_id = self.max_id;
            self.max_id += 1;
            node_id
        })
    }
}

#[derive(Debug)]
pub struct Graph<T: Eq + Hash, W: Clone + Copy> {
    node_index: NodeIndex<T>,
    edges: HashMap<(usize, usize), W>,
}

impl<T: Eq + Hash, W: Clone + Copy> Graph<T, W> {
    pub fn new() -> Self {
        Self {
            node_index: NodeIndex::new(),
            edges: HashMap::new(),
        }
    }

    #[inline]
    pub fn add_edge(&mut self, u: T, v: T, weight: W) {
        let u = self.node_index.index(u);
        let v = self.node_index.index(v);
        self.edges.insert((u, v), weight);
    }

    #[inline]
    pub fn weight(&self, u: usize, v: usize) -> Option<W> {
        self.edges.get(&(u, v)).copied()
    }

    #[inline]
    pub fn num_nodes(&self) -> usize {
        self.node_index.max_id
    }

    #[inline]
    pub fn num_edges(&self) -> usize {
        self.edges.len()
    }
}

impl<T: Eq + Hash, W: Clone + Copy> Default for Graph<T, W> {
    fn default() -> Self {
        Self::new()
    }
}
