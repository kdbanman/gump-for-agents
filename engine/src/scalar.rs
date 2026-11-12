//! A plain, obviously-correct stepper, written straight from the doubled-coordinate
//! definition: for every cell, add its 12 neighbour offsets, locate each neighbour in the
//! box (wrapping on a torus, dead outside an open box), count, apply the rule.
//! It shares nothing with the bit-sliced engine except `Geometry::locate` / `offsets`.
//! Used as the reference in tests; slow (~10⁷ cell-updates/s).

use crate::lattice::{offsets, Geometry, P3};
use crate::rule::Rule;

pub struct ScalarSim {
    pub geo: Geometry,
    pub rule: Rule,
    state: Vec<bool>,
    pub gen: u64,
}

impl ScalarSim {
    pub fn new(geo: Geometry, rule: Rule) -> Self {
        let n = geo.cells();
        ScalarSim { geo, rule, state: vec![false; n], gen: 0 }
    }

    #[inline]
    fn idx(&self, a: usize, c: [usize; 3]) -> usize {
        let n = self.geo.n;
        (((a * n[2] + c[2]) * n[1] + c[1]) * n[0]) + c[0]
    }

    pub fn get(&self, p: P3) -> bool {
        match self.geo.locate(p) {
            Some((a, c)) => self.state[self.idx(a, c)],
            None => false,
        }
    }

    /// Set a cell given in doubled coordinates. Returns false if it is not a cell or lies
    /// outside an open box.
    pub fn set(&mut self, p: P3, v: bool) -> bool {
        match self.geo.locate(p) {
            Some((a, c)) => {
                let i = self.idx(a, c);
                self.state[i] = v;
                true
            }
            None => false,
        }
    }

    pub fn step(&mut self) {
        let n = self.geo.n;
        let mut next = vec![false; self.state.len()];
        for a in 0..3 {
            let offs = offsets(a);
            for k in 0..n[2] {
                for j in 0..n[1] {
                    for i in 0..n[0] {
                        let c = [i, j, k];
                        let p = self.geo.to_doubled(a, c);
                        let mut cnt = 0u32;
                        for o in offs.iter() {
                            if self.get([p[0] + o[0], p[1] + o[1], p[2] + o[2]]) {
                                cnt += 1;
                            }
                        }
                        let alive = self.state[self.idx(a, c)];
                        next[self.idx(a, c)] = self.rule.next(alive, cnt);
                    }
                }
            }
        }
        self.state = next;
        self.gen += 1;
    }

    /// Live cells in doubled coordinates, sorted.
    pub fn cells(&self) -> Vec<P3> {
        let n = self.geo.n;
        let mut v = Vec::new();
        for a in 0..3 {
            for k in 0..n[2] {
                for j in 0..n[1] {
                    for i in 0..n[0] {
                        if self.state[self.idx(a, [i, j, k])] {
                            v.push(self.geo.to_doubled(a, [i, j, k]));
                        }
                    }
                }
            }
        }
        v.sort();
        v
    }

    pub fn population(&self) -> u64 {
        self.state.iter().filter(|&&b| b).count() as u64
    }
}
