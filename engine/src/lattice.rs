//! Lattice geometry: doubled coordinates, cube-index coordinates, neighbourhoods,
//! body diagonals, and the simulation box (torus or open/dead-outside).
//!
//! See `docs/AUTOMATON.md`. A cell is a face of the cubic honeycomb. In *doubled
//! coordinates* it is a point `p ∈ Z³` with exactly one odd coordinate (its normal axis).
//! In *cube-index coordinates* it is `(a, i, j, k)`: the face on the `+a` side of cube
//! `(i, j, k)`, i.e. doubled `2(i,j,k) + e_a`.

/// A point in doubled coordinates.
pub type P3 = [i64; 3];

/// The four body-diagonal axes used for layer analysis. Layer coordinate is `s = d·p`
/// (always odd for a cell). Axis 0 is `[111]`, axis 1 `[-1,1,1]`, axis 2 `[1,-1,1]`,
/// axis 3 `[1,1,-1]`.
pub const DIAGS: [[i64; 3]; 4] = [[1, 1, 1], [-1, 1, 1], [1, -1, 1], [1, 1, -1]];

/// Layer coordinate of `p` along body-diagonal axis `d` (index into [`DIAGS`]).
#[inline]
pub fn layer(p: P3, d: usize) -> i64 {
    let v = DIAGS[d];
    v[0] * p[0] + v[1] * p[1] + v[2] * p[2]
}

/// The normal axis of a cell, or `None` if `p` is not a cell (not exactly one odd coordinate).
#[inline]
pub fn cell_axis(p: P3) -> Option<usize> {
    let odd = [p[0] & 1 != 0, p[1] & 1 != 0, p[2] & 1 != 0];
    match (odd[0] as u8) + (odd[1] as u8) + (odd[2] as u8) {
        1 => Some(odd.iter().position(|&o| o).unwrap()),
        _ => None,
    }
}

/// The 12 neighbour offsets (doubled coordinates) of a face whose normal is `axis`,
/// written directly from the definition (same construction as `reference/oracle.py`).
pub fn offsets(axis: usize) -> [P3; 12] {
    let a = axis;
    let others: Vec<usize> = (0..3).filter(|&t| t != a).collect();
    let (b, c) = (others[0], others[1]);
    let mut out = [[0i64; 3]; 12];
    let mut n = 0;
    for sb in [2, -2] {
        for sc in [2, -2] {
            // coplanar faces touching only at a corner
            out[n][b] = sb;
            out[n][c] = sc;
            n += 1;
        }
    }
    for sa in [1, -1] {
        for t in [b, c] {
            for st in [1, -1] {
                // perpendicular faces sharing an edge
                out[n][a] = sa;
                out[n][t] = st;
                n += 1;
            }
        }
    }
    out
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub enum Boundary {
    /// Periodic in all three directions with period `2·n[t]` in doubled coordinates.
    Torus,
    /// Everything outside the box is dead (forced). With the box containing the seed's
    /// diagonal hull this is exactly infinite open space (theorem T2).
    Open,
}

impl Boundary {
    pub fn name(&self) -> &'static str {
        match self {
            Boundary::Torus => "torus",
            Boundary::Open => "open",
        }
    }
}

/// The simulation box: `n` cubes per direction, cube `(i,j,k)` (local, `0 ≤ i < n[0]` …)
/// is absolute cube `(i,j,k) + origin`.
#[derive(Clone, Debug, PartialEq, Eq, Hash)]
pub struct Geometry {
    pub n: [usize; 3],
    pub origin: [i64; 3],
    pub boundary: Boundary,
}

impl Geometry {
    pub fn new(n: [usize; 3], origin: [i64; 3], boundary: Boundary) -> Self {
        assert!(n.iter().all(|&v| v >= 1), "box dimensions must be >= 1");
        Geometry { n, origin, boundary }
    }

    pub fn cubes(&self) -> usize {
        self.n[0] * self.n[1] * self.n[2]
    }

    /// Number of cells (faces) in the box: 3 per cube.
    pub fn cells(&self) -> usize {
        3 * self.cubes()
    }

    /// Doubled coordinates of local cell `(a, c)`.
    #[inline]
    pub fn to_doubled(&self, a: usize, c: [usize; 3]) -> P3 {
        let mut p = [0i64; 3];
        for t in 0..3 {
            p[t] = 2 * (c[t] as i64 + self.origin[t]) + (t == a) as i64;
        }
        p
    }

    /// Local `(axis, cube)` of doubled point `p`. Torus: wraps. Open: `None` outside the box.
    /// Also `None` if `p` is not a cell.
    #[inline]
    pub fn locate(&self, p: P3) -> Option<(usize, [usize; 3])> {
        let a = cell_axis(p)?;
        let mut c = [0usize; 3];
        for t in 0..3 {
            let cube_abs = (p[t] - (t == a) as i64).div_euclid(2);
            let local = cube_abs - self.origin[t];
            let n = self.n[t] as i64;
            c[t] = match self.boundary {
                Boundary::Torus => local.rem_euclid(n) as usize,
                Boundary::Open => {
                    if local < 0 || local >= n {
                        return None;
                    }
                    local as usize
                }
            };
        }
        Some((a, c))
    }

    /// Inclusive doubled-coordinate range covered by the box along each axis.
    pub fn doubled_bounds(&self) -> ([i64; 3], [i64; 3]) {
        let mut lo = [0; 3];
        let mut hi = [0; 3];
        for t in 0..3 {
            lo[t] = 2 * self.origin[t];
            hi[t] = 2 * (self.origin[t] + self.n[t] as i64 - 1) + 1;
        }
        (lo, hi)
    }

    /// Torus only: layers along every diagonal are taken modulo `2g`, `g = gcd(n)`.
    pub fn layer_modulus(&self) -> Option<i64> {
        match self.boundary {
            Boundary::Torus => {
                let g = gcd(gcd(self.n[0], self.n[1]), self.n[2]);
                Some(2 * g as i64)
            }
            Boundary::Open => None,
        }
    }

    /// Range of layer coordinates `[s_min, s_max]` (both odd) a cell in the box can have
    /// along diagonal `d` (open boxes); for tori `[1, 2g-1]` (layer coords reduced mod 2g).
    pub fn layer_range(&self, d: usize) -> (i64, i64) {
        if let Some(m) = self.layer_modulus() {
            return (1, m - 1);
        }
        let (lo, hi) = self.doubled_bounds();
        let v = DIAGS[d];
        let mut smin = 0;
        let mut smax = 0;
        for t in 0..3 {
            smin += (v[t] * lo[t]).min(v[t] * hi[t]);
            smax += (v[t] * lo[t]).max(v[t] * hi[t]);
        }
        if smin.rem_euclid(2) == 0 {
            smin -= 1;
        }
        if smax.rem_euclid(2) == 0 {
            smax += 1;
        }
        (smin, smax)
    }

    pub fn contains_doubled(&self, p: P3) -> bool {
        self.locate(p).is_some()
    }

    /// Smallest open box (plus `margin` cubes on every side) holding every cell of the
    /// diagonal hull `hull[d] = (lo_d, hi_d)`; `nx` is rounded up so the bit engine can
    /// pack it (see [`crate::fast::pack_open`]).
    pub fn open_for_hull(hull: &Hull, margin: usize) -> Geometry {
        let (lo, hi) = hull.doubled_bbox();
        let mut n = [0usize; 3];
        let mut origin = [0i64; 3];
        for t in 0..3 {
            // cells with doubled coordinate x in [lo, hi] live in cubes floor((x-1)/2)..=floor(x/2)
            let c0 = (lo[t] - 1).div_euclid(2) - margin as i64;
            let c1 = hi[t].div_euclid(2) + margin as i64;
            origin[t] = c0;
            n[t] = (c1 - c0 + 1) as usize;
        }
        n[0] = crate::fast::pack_open(n[0]).0 * crate::fast::pack_open(n[0]).1;
        Geometry::new(n, origin, Boundary::Open)
    }
}

pub fn gcd(a: usize, b: usize) -> usize {
    if b == 0 {
        a
    } else {
        gcd(b, a % b)
    }
}

/// The diagonal hull of a finite pattern: for each diagonal axis `d`, the inclusive range
/// `[lo_d, hi_d]` of layer coordinates `d·p` over live cells. The hull (intersection of the
/// 8 half-spaces) can only shrink under the dynamics (T2).
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Hull(pub [(i64, i64); 4]);

impl Hull {
    pub fn of_cells(cells: &[P3]) -> Option<Hull> {
        if cells.is_empty() {
            return None;
        }
        let mut h = [(i64::MAX, i64::MIN); 4];
        for &p in cells {
            for d in 0..4 {
                let s = layer(p, d);
                h[d].0 = h[d].0.min(s);
                h[d].1 = h[d].1.max(s);
            }
        }
        Some(Hull(h))
    }

    /// Is `p` inside all 8 half-spaces?
    pub fn contains(&self, p: P3) -> bool {
        (0..4).all(|d| {
            let s = layer(p, d);
            s >= self.0[d].0 && s <= self.0[d].1
        })
    }

    /// Doubled-coordinate bounding box of the hull polytope (a bound, possibly loose by
    /// one unit).
    pub fn doubled_bbox(&self) -> (P3, P3) {
        let h = &self.0;
        // 2x = s0 - s1 = s2 + s3 ; 2y = s0 - s2 = s1 + s3 ; 2z = s0 - s3 = s1 + s2
        let xhi = ((h[0].1 - h[1].0).min(h[2].1 + h[3].1)).div_euclid(2);
        let xlo = -((-(h[0].0 - h[1].1)).min(-(h[2].0 + h[3].0))).div_euclid(2);
        let yhi = ((h[0].1 - h[2].0).min(h[1].1 + h[3].1)).div_euclid(2);
        let ylo = -((-(h[0].0 - h[2].1)).min(-(h[1].0 + h[3].0))).div_euclid(2);
        let zhi = ((h[0].1 - h[3].0).min(h[1].1 + h[2].1)).div_euclid(2);
        let zlo = -((-(h[0].0 - h[3].1)).min(-(h[1].0 + h[2].0))).div_euclid(2);
        ([xlo, ylo, zlo], [xhi, yhi, zhi])
    }

    /// Number of cells inside the hull (brute force over its bounding box).
    pub fn volume(&self) -> u64 {
        let (lo, hi) = self.doubled_bbox();
        let mut n = 0;
        for z in lo[2]..=hi[2] {
            for y in lo[1]..=hi[1] {
                for x in lo[0]..=hi[0] {
                    let p = [x, y, z];
                    if cell_axis(p).is_some() && self.contains(p) {
                        n += 1;
                    }
                }
            }
        }
        n
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn t1_layer_histogram() {
        for a in 0..3 {
            for d in 0..4 {
                let mut h = std::collections::BTreeMap::new();
                for o in offsets(a) {
                    *h.entry(layer(o, d)).or_insert(0) += 1;
                }
                let h: Vec<(i64, i32)> = h.into_iter().collect();
                assert_eq!(h, vec![(-4, 1), (-2, 2), (0, 6), (2, 2), (4, 1)]);
            }
        }
    }

    #[test]
    fn locate_roundtrip() {
        for boundary in [Boundary::Open, Boundary::Torus] {
            let g = Geometry::new([3, 4, 5], [-1, 2, -3], boundary);
            for a in 0..3 {
                for k in 0..5 {
                    for j in 0..4 {
                        for i in 0..3 {
                            let p = g.to_doubled(a, [i, j, k]);
                            assert_eq!(cell_axis(p), Some(a));
                            assert_eq!(g.locate(p), Some((a, [i, j, k])));
                        }
                    }
                }
            }
        }
    }

    #[test]
    fn hull_bbox_contains_hull() {
        let cells = vec![[1, 0, 0], [-5, 2, 4], [3, 7, -2], [0, 0, -9]];
        let h = Hull::of_cells(&cells).unwrap();
        let (lo, hi) = h.doubled_bbox();
        for p in &cells {
            for t in 0..3 {
                assert!(p[t] >= lo[t] && p[t] <= hi[t]);
            }
        }
        // every hull cell inside bbox; check bbox is tight-ish by brute force over a larger region
        for z in -30..=30 {
            for y in -30..=30 {
                for x in -30..=30 {
                    let p = [x, y, z];
                    if cell_axis(p).is_some() && h.contains(p) {
                        for t in 0..3 {
                            assert!(p[t] >= lo[t] && p[t] <= hi[t], "{:?} outside {:?} {:?}", p, lo, hi);
                        }
                    }
                }
            }
        }
    }
}
