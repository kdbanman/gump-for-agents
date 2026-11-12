//! Seeds: closed cubes, legacy seeds, random soups, cell lists.
//! Every seed is produced as a list of live cells in doubled coordinates, independent of
//! the box it will be placed in.

use crate::lattice::{cell_axis, layer, P3, DIAGS};

/// xoshiro256** seeded through splitmix64. Fixed forever: soups are reproducible from
/// `(region, density, seed)`.
#[derive(Clone)]
pub struct Rng {
    s: [u64; 4],
}

impl Rng {
    pub fn new(seed: u64) -> Rng {
        let mut x = seed;
        let mut next = || {
            x = x.wrapping_add(0x9E37_79B9_7F4A_7C15);
            let mut z = x;
            z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
            z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
            z ^ (z >> 31)
        };
        Rng { s: [next(), next(), next(), next()] }
    }

    pub fn next_u64(&mut self) -> u64 {
        let r = self.s[1].wrapping_mul(5).rotate_left(7).wrapping_mul(9);
        let t = self.s[1] << 17;
        self.s[2] ^= self.s[0];
        self.s[3] ^= self.s[1];
        self.s[1] ^= self.s[2];
        self.s[0] ^= self.s[3];
        self.s[2] ^= t;
        self.s[3] = self.s[3].rotate_left(45);
        r
    }

    /// Bernoulli(p) via 64-bit threshold comparison.
    pub fn chance(&mut self, p: f64) -> bool {
        if p >= 1.0 {
            self.next_u64();
            return true;
        }
        if p <= 0.0 {
            self.next_u64();
            return false;
        }
        let thr = (p * 18446744073709551616.0) as u64;
        self.next_u64() < thr
    }
}

/// Every cell whose doubled coordinates all lie in `[lo, hi]` (inclusive).
pub fn fill_span(lo: [i64; 3], hi: [i64; 3]) -> Vec<P3> {
    let mut v = Vec::new();
    for z in lo[2]..=hi[2] {
        for y in lo[1]..=hi[1] {
            for x in lo[0]..=hi[0] {
                if cell_axis([x, y, z]).is_some() {
                    v.push([x, y, z]);
                }
            }
        }
    }
    v
}

/// Closed cube of side `n` cubes with all internal faces live, `3n²(n+1)` cells.
/// Centred on the cube centre 0 (odd n: span `[-n, n]`) or on the vertex (1,1,1)
/// (even n: span `[1-n, 1+n]`).
pub fn closed_cube(n: i64) -> Vec<P3> {
    assert!(n >= 1);
    let (lo, hi) = if n % 2 == 1 { (-n, n) } else { (1 - n, 1 + n) };
    fill_span([lo; 3], [hi; 3])
}

/// The original's `getSeedStart/End` (float32 arithmetic, Java rounding), for `generate`
/// mode 1 with `seedFraction = 0.38`, habitat size `h`.
pub fn legacy_cube_span(h: i64) -> (i64, i64) {
    let f = |v: f32| (v + 0.5f32).floor() as i64;
    let seed_len = h as f32 * 0.38f32;
    let half = (h / 2) as f32;
    let mut lo = f(half - seed_len / 2.0f32);
    if lo % 2 == 0 {
        lo += 1;
    }
    lo = lo.min(h - 1);
    let mut hi = f(half + seed_len / 2.0f32);
    if hi % 2 == 0 {
        hi += 1;
    }
    hi = hi.min(h - 1);
    (lo, hi)
}

/// Legacy closed-cube seed in the original's frame (doubled coordinates `0..h`).
pub fn legacy_cube(h: i64) -> Vec<P3> {
    let (lo, hi) = legacy_cube_span(h);
    fill_span([lo; 3], [hi; 3])
}

/// Legacy number-key seed (`generateFull`, key `k` in 1..=9, habitat `h`, normally 50).
pub fn legacy_key(h: i64, k: i64) -> Vec<P3> {
    let size = k + 8;
    let lo = h / 2 - size / 2;
    fill_span([lo; 3], [lo + size; 3])
}

/// Regions for random soups (all in doubled coordinates).
#[derive(Clone, Debug)]
pub enum Region {
    /// `lo_t ≤ p_t ≤ hi_t` for every t (see [`Region::cbox`] for centre/half-width).
    Box { lo: P3, hi: P3 },
    /// `Σ|p_t − c_t| ≤ r` (an octahedron, the shape of a diagonal hull).
    Oct { center: P3, r: i64 },
    /// `m` consecutive `{111}` layers `s_d ∈ {s0, s0+2, …, s0+2(m−1)}` along diagonal
    /// axis `axis`, intersected with the box `[lo, hi]`. With `modulus` (a torus whose
    /// layers repeat with period `2g`, see `Geometry::layer_modulus`) layers are compared
    /// mod `modulus`, so the slab wraps consistently.
    Slab { axis: usize, s0: i64, m: i64, lo: P3, hi: P3, modulus: Option<i64> },
}

impl Region {
    /// Box `|p_t − c_t| ≤ half_t`.
    pub fn cbox(center: P3, half: [i64; 3]) -> Region {
        let (lo, hi) = Self::span(center, half);
        Region::Box { lo, hi }
    }

    pub fn span(center: P3, half: [i64; 3]) -> (P3, P3) {
        let mut lo = [0; 3];
        let mut hi = [0; 3];
        for t in 0..3 {
            lo[t] = center[t] - half[t];
            hi[t] = center[t] + half[t];
        }
        (lo, hi)
    }

    pub fn bounds(&self) -> (P3, P3) {
        match self {
            Region::Box { lo, hi } | Region::Slab { lo, hi, .. } => (*lo, *hi),
            Region::Oct { center, r } => {
                let mut lo = [0; 3];
                let mut hi = [0; 3];
                for t in 0..3 {
                    lo[t] = center[t] - r;
                    hi[t] = center[t] + r;
                }
                (lo, hi)
            }
        }
    }

    pub fn contains(&self, p: P3) -> bool {
        let (lo, hi) = self.bounds();
        if (0..3).any(|t| p[t] < lo[t] || p[t] > hi[t]) {
            return false;
        }
        match self {
            Region::Box { .. } => true,
            Region::Oct { center, r } => (0..3).map(|t| (p[t] - center[t]).abs()).sum::<i64>() <= *r,
            Region::Slab { axis, s0, m, modulus, .. } => {
                let s = layer(p, *axis);
                match modulus {
                    None => s >= *s0 && s <= s0 + 2 * (m - 1),
                    Some(md) => (s - s0).rem_euclid(*md) <= 2 * (m - 1),
                }
            }
        }
    }

    /// First layer of an `m`-layer slab centred on layer coordinate ≈ `centre_s`.
    pub fn slab_s0(m: i64, centre_s: i64) -> i64 {
        let mut s0 = centre_s - (m - 1);
        if s0.rem_euclid(2) == 0 {
            s0 += 1;
        }
        s0
    }

    pub fn describe(&self) -> String {
        match self {
            Region::Box { lo, hi } => format!("box lo={:?} hi={:?}", lo, hi),
            Region::Oct { center, r } => format!("oct center={:?} r={}", center, r),
            Region::Slab { axis, s0, m, lo, hi, modulus } => {
                format!("slab axis={:?} s0={} m={} box lo={:?} hi={:?} mod={:?}", DIAGS[*axis], s0, m, lo, hi, modulus)
            }
        }
    }
}

/// Random soup: every cell of the region, enumerated in canonical order (z outer, then y,
/// then x, doubled coordinates), draws one value from `Rng::new(seed)` and is live with
/// probability `density`.
pub fn soup(region: &Region, density: f64, seed: u64) -> Vec<P3> {
    let mut rng = Rng::new(seed);
    let (lo, hi) = region.bounds();
    let mut v = Vec::new();
    for z in lo[2]..=hi[2] {
        for y in lo[1]..=hi[1] {
            for x in lo[0]..=hi[0] {
                let p = [x, y, z];
                if cell_axis(p).is_some() && region.contains(p) && rng.chance(density) {
                    v.push(p);
                }
            }
        }
    }
    v
}

/// Symmetric soup: one random draw per orbit of `group` (elements of O_h acting about
/// `center`), so the soup is invariant under the group. Orbits are visited in the same
/// canonical order as [`soup`] (a cell draws when it is the first of its orbit to be
/// visited); every member of a live orbit is live, even if it lies outside the region
/// (use a region symmetric about `center`).
pub fn soup_sym(region: &Region, density: f64, seed: u64, group: &[crate::sym::Elem], center: P3) -> Vec<P3> {
    let mut rng = Rng::new(seed);
    let (lo, hi) = region.bounds();
    let mut done: std::collections::HashSet<P3> = std::collections::HashSet::new();
    let mut v = Vec::new();
    for z in lo[2]..=hi[2] {
        for y in lo[1]..=hi[1] {
            for x in lo[0]..=hi[0] {
                let p = [x, y, z];
                if cell_axis(p).is_none() || !region.contains(p) || done.contains(&p) {
                    continue;
                }
                let orbit: std::collections::BTreeSet<P3> = group.iter().map(|g| g.apply_about(p, center)).collect();
                let live = rng.chance(density);
                for q in orbit {
                    done.insert(q);
                    if live {
                        v.push(q);
                    }
                }
            }
        }
    }
    v.sort();
    v
}

/// Parse a cell list: one cell per line, three integers (doubled coordinates) separated
/// by spaces, tabs or commas; `#` starts a comment.
pub fn parse_cells(text: &str) -> Result<Vec<P3>, String> {
    let mut v = Vec::new();
    for (n, line) in text.lines().enumerate() {
        let line = line.split('#').next().unwrap().trim();
        if line.is_empty() {
            continue;
        }
        let nums: Result<Vec<i64>, _> =
            line.split(|c: char| c == ',' || c.is_whitespace()).filter(|t| !t.is_empty()).map(|t| t.parse::<i64>()).collect();
        let nums = nums.map_err(|e| format!("line {}: {e}", n + 1))?;
        if nums.len() != 3 {
            return Err(format!("line {}: expected 3 coordinates", n + 1));
        }
        let p = [nums[0], nums[1], nums[2]];
        if cell_axis(p).is_none() {
            return Err(format!("line {}: {:?} is not a cell (needs exactly one odd coordinate)", n + 1, p));
        }
        v.push(p);
    }
    Ok(v)
}

pub fn format_cells(cells: &[P3], header: &str) -> String {
    let mut s = String::with_capacity(cells.len() * 12 + header.len() + 64);
    s.push_str("# gump cells v1: one live cell per line, doubled coordinates x y z\n");
    for l in header.lines() {
        s.push_str("# ");
        s.push_str(l);
        s.push('\n');
    }
    for p in cells {
        s.push_str(&format!("{} {} {}\n", p[0], p[1], p[2]));
    }
    s
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn cube_counts() {
        for n in 1..8 {
            assert_eq!(closed_cube(n).len() as i64, 3 * n * n * (n + 1));
        }
    }
    #[test]
    fn legacy_spans() {
        // from docs/AUTOMATON.md table
        assert_eq!(legacy_cube_span(40), (13, 29));
        assert_eq!(legacy_cube_span(50), (17, 35));
        assert_eq!(legacy_cube_span(55), (17, 37));
        assert_eq!(legacy_cube_span(60), (19, 41));
        assert_eq!(legacy_cube_span(65), (21, 45));
        assert_eq!(legacy_cube_span(70), (23, 49));
        assert_eq!(legacy_cube_span(100), (31, 69));
    }
    #[test]
    fn soup_reproducible() {
        let r = Region::Oct { center: [0, 0, 0], r: 9 };
        assert_eq!(soup(&r, 0.3, 7), soup(&r, 0.3, 7));
        assert_ne!(soup(&r, 0.3, 7), soup(&r, 0.3, 8));
        assert!(soup(&r, 1.0, 1).iter().all(|&p| r.contains(p)));
    }
}
