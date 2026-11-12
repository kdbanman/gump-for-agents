//! Point symmetries of the lattice: the 48 elements of O_h acting on doubled coordinates
//! (coordinate permutations × sign flips, about the origin, a cube centre), named
//! subgroups, canonical forms and stabilisers (the conventions of `research/atlas`).

use crate::lattice::{cell_axis, P3};

/// `g(p)_t = sign[t] · p[perm[t]]`.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Elem {
    pub perm: [usize; 3],
    pub sign: [i64; 3],
}

impl Elem {
    #[inline]
    pub fn apply(&self, p: P3) -> P3 {
        [self.sign[0] * p[self.perm[0]], self.sign[1] * p[self.perm[1]], self.sign[2] * p[self.perm[2]]]
    }
    /// Apply about centre `c` (doubled coordinates).
    #[inline]
    pub fn apply_about(&self, p: P3, c: P3) -> P3 {
        let q = self.apply([p[0] - c[0], p[1] - c[1], p[2] - c[2]]);
        [q[0] + c[0], q[1] + c[1], q[2] + c[2]]
    }
    fn perm_parity(&self) -> i64 {
        let p = self.perm;
        let inv = (p[0] > p[1]) as i64 + (p[0] > p[2]) as i64 + (p[1] > p[2]) as i64;
        if inv % 2 == 0 {
            1
        } else {
            -1
        }
    }
    /// Determinant (+1 rotation, −1 improper).
    pub fn det(&self) -> i64 {
        self.perm_parity() * self.sign[0] * self.sign[1] * self.sign[2]
    }
}

/// All 48 elements of O_h (identity first).
pub fn oh() -> Vec<Elem> {
    let perms = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]];
    let mut v = Vec::with_capacity(48);
    for perm in perms {
        for s in 0..8 {
            let sign = [if s & 1 == 0 { 1 } else { -1 }, if s & 2 == 0 { 1 } else { -1 }, if s & 4 == 0 { 1 } else { -1 }];
            v.push(Elem { perm, sign });
        }
    }
    v
}

/// Named subgroups of O_h (all about the origin; axis-specific ones use z / [111]).
pub const GROUPS: &[(&str, &str)] = &[
    ("oh", "full cubic group, 48"),
    ("o", "rotations of the cube, 24"),
    ("td", "tetrahedral with mirrors (even sign flips x all permutations), 24"),
    ("th", "pyritohedral (cyclic permutations x all sign flips), 24"),
    ("d4h", "square prism about z, 16"),
    ("d3d", "about [111]: permutations x (+++ / ---), 12"),
    ("d2h", "the three coordinate mirror planes, 8"),
    ("c4v", "square pyramid about +z, 8"),
    ("c3v", "about [111]: the six coordinate permutations, 6"),
    ("c3", "cyclic permutations, 3"),
    ("ci", "inversion, 2"),
    ("c1", "trivial, 1"),
];

pub fn group(name: &str) -> Option<Vec<Elem>> {
    let all = oh();
    let keep = |f: &dyn Fn(&Elem) -> bool| all.iter().copied().filter(|e| f(e)).collect::<Vec<_>>();
    let cyclic = |e: &Elem| e.perm_parity() == 1;
    let fixes_z = |e: &Elem| e.perm[2] == 2;
    let flips = |e: &Elem| e.sign.iter().filter(|&&s| s < 0).count();
    Some(match name {
        "oh" => all.clone(),
        "o" => keep(&|e| e.det() == 1),
        "td" => keep(&|e| flips(e) % 2 == 0),
        "th" => keep(&|e| cyclic(e)),
        "d4h" => keep(&|e| fixes_z(e)),
        "d3d" => keep(&|e| e.sign[0] == e.sign[1] && e.sign[1] == e.sign[2]),
        "d2h" => keep(&|e| e.perm == [0, 1, 2]),
        "c4v" => keep(&|e| fixes_z(e) && e.sign[2] == 1),
        "c3v" => keep(&|e| e.sign == [1, 1, 1]),
        "c3" => keep(&|e| e.sign == [1, 1, 1] && cyclic(e)),
        "ci" => keep(&|e| e.perm == [0, 1, 2] && (e.sign == [1, 1, 1] || e.sign == [-1, -1, -1])),
        "c1" => keep(&|e| e.perm == [0, 1, 2] && e.sign == [1, 1, 1]),
        _ => return None,
    })
}

/// Sorted cells after the even translation putting each coordinate's minimum in {0, 1}.
pub fn normalise(cells: &[P3]) -> Vec<P3> {
    if cells.is_empty() {
        return vec![];
    }
    let mut m = [i64::MAX; 3];
    for p in cells {
        for t in 0..3 {
            m[t] = m[t].min(p[t]);
        }
    }
    let sh = [m[0] - m[0].rem_euclid(2), m[1] - m[1].rem_euclid(2), m[2] - m[2].rem_euclid(2)];
    let mut v: Vec<P3> = cells.iter().map(|p| [p[0] - sh[0], p[1] - sh[1], p[2] - sh[2]]).collect();
    v.sort();
    v
}

pub fn transform(cells: &[P3], g: &Elem) -> Vec<P3> {
    cells.iter().map(|&p| g.apply(p)).collect()
}

/// Canonical form: minimum over O_h of `normalise(g(cells))`.
pub fn canonical(cells: &[P3]) -> Vec<P3> {
    oh().iter().map(|g| normalise(&transform(cells, g))).min().unwrap_or_default()
}

/// Canonical form of an orbit (list of phases): minimum over O_h and phases; returns the
/// canonical phase-0 cells and the index of the phase it came from.
pub fn canonical_orbit(phases: &[Vec<P3>]) -> (Vec<P3>, usize) {
    let mut best: Option<(Vec<P3>, usize)> = None;
    for (k, ph) in phases.iter().enumerate() {
        let c = canonical(ph);
        if best.as_ref().is_none_or(|b| c < b.0) {
            best = Some((c, k));
        }
    }
    best.unwrap_or_default()
}

/// Order of the stabiliser of `cells` in translations × O_h.
pub fn stabiliser_order(cells: &[P3]) -> usize {
    let n = normalise(cells);
    oh().iter().filter(|g| normalise(&transform(cells, g)) == n).count()
}

/// Number of pairs (g, k) with g(phase_0) = phase_k up to translation.
pub fn spacetime_order(phases: &[Vec<P3>]) -> usize {
    let norms: Vec<Vec<P3>> = phases.iter().map(|p| normalise(p)).collect();
    let mut n = 0;
    for g in oh() {
        let img = normalise(&transform(&phases[0], &g));
        n += norms.iter().filter(|q| **q == img).count();
    }
    n
}

/// Is `g` about `c` a symmetry of the lattice at `c`'s position (maps cells to cells)?
pub fn maps_cells_to_cells(g: &Elem, c: P3) -> bool {
    // test a few cells of each orientation around c
    for p in [[1, 0, 0], [0, 1, 0], [0, 0, 1], [3, 2, 0], [2, 0, 5], [0, 7, 4]] {
        for q in [p, [p[0] + c[0], p[1] + c[1], p[2] + c[2]]] {
            if cell_axis(q).is_some() && cell_axis(g.apply_about(q, c)).is_none() {
                return false;
            }
        }
    }
    true
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn group_orders() {
        let want = [48, 24, 24, 24, 16, 12, 8, 8, 6, 3, 2, 1];
        for ((name, _), w) in GROUPS.iter().zip(want) {
            let g = group(name).unwrap();
            assert_eq!(g.len(), w, "{name}");
            // closed under composition
            for a in &g {
                for b in &g {
                    let p = [1, 2, 3];
                    let ab = a.apply(b.apply(p));
                    assert!(g.iter().any(|e| e.apply(p) == ab), "{name} not closed");
                }
            }
        }
    }
    #[test]
    fn unit_cube_has_full_symmetry() {
        let cube = crate::seeds::closed_cube(1);
        assert_eq!(stabiliser_order(&cube), 48);
        assert_eq!(canonical(&cube), vec![[1, 2, 2], [2, 1, 2], [2, 2, 1], [2, 2, 3], [2, 3, 2], [3, 2, 2]]);
    }
}
