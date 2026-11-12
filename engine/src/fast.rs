//! The fast engine: bit-sliced stepping of the three cube-index bit-volumes X, Y, Z.
//!
//! # Layout
//! The box has `nx × ny × nz` cubes. Along `x` the cubes are packed into `W` words per row
//! with an *interleaved* assignment: bit `b` of word-plane `w` holds cube `i = b·W + w`
//! (`B = nx / W ≤ 64` bits used per word). Each orientation volume is stored as `W`
//! word-planes; a word-plane is a `(ny+2) × (nz+2)` array of `u64` (j fastest) with a
//! one-word halo on each side in `j` and `k`. Consequences:
//!
//! * `j ± 1` and `k ± 1` are fixed word offsets (`±1`, `±(ny+2)`) — no shifts;
//! * `i ± 1` is the *same* word position in plane `w ± 1` — no shifts either — except
//!   across the seam `w = W−1 → 0`, where it is plane 0 shifted by one bit (a rotate on a
//!   torus). Those seam planes are precomputed once per generation (5 planes).
//!
//! So the kernel is a pure element-wise loop over words with constant offsets; LLVM
//! vectorises it to AVX-512 (`target-cpu=native`). The 12 neighbour bits of 64 cells are
//! summed with a carry-save adder tree (8 full adders + 2 half adders → 4 count bits) and
//! the rule is a boolean function of the count bits and the centre bit.
//!
//! On a torus the halo is refreshed each generation by copying; in an open box it stays
//! zero (dead outside). A torus needs `nx = B·W` exactly, `B ≤ 64`: the smallest such `W`
//! is chosen (prime `nx > 64` degrades to `B = 1`, correct but slow).

use crate::lattice::{Boundary, Geometry, P3};
use crate::rule::Rule;

/// `(W, B)` for an open box needing at least `nx` cubes along x: the box is then rounded
/// up to `nx' = W·B ≥ nx`.
pub fn pack_open(nx: usize) -> (usize, usize) {
    let w = nx.div_ceil(64);
    let b = nx.div_ceil(w);
    (w, b)
}

/// `(W, B)` with `W·B == nx` exactly and `B ≤ 64`, smallest `W`.
pub fn pack_torus(nx: usize) -> (usize, usize) {
    let mut w = nx.div_ceil(64);
    while nx % w != 0 {
        w += 1;
    }
    (w, nx / w)
}

const HK1: u64 = 0x9E37_79B9_7F4A_7C15;
const HK2: u64 = 0xD6E8_FEB8_6659_FD93;

#[inline(always)]
fn hmix(v: u64, gi: u64) -> u64 {
    // zero words contribute nothing, so the hash does not depend on how the index range
    // is split between threads (halo positions are always zero in the kernel output)
    let x = (v ^ gi.wrapping_mul(HK1)).wrapping_mul(HK2);
    if v != 0 {
        x ^ (x >> 32)
    } else {
        0
    }
}

#[inline(always)]
fn fa(a: u64, b: u64, c: u64) -> (u64, u64) {
    let t = a ^ b;
    (t ^ c, (a & b) | (t & c))
}

#[inline(always)]
fn ha(a: u64, b: u64) -> (u64, u64) {
    (a ^ b, a & b)
}

/// 12 one-bit inputs per lane → 4-bit count `[c0, c1, c2, c3]`.
#[inline(always)]
fn count12(v: [u64; 12]) -> [u64; 4] {
    let (s1, k1) = fa(v[0], v[1], v[2]);
    let (s2, k2) = fa(v[3], v[4], v[5]);
    let (s3, k3) = fa(v[6], v[7], v[8]);
    let (s4, k4) = fa(v[9], v[10], v[11]);
    let (t1, m1) = fa(s1, s2, s3);
    let (c0, m2) = ha(t1, s4);
    let (u1, n1) = fa(k1, k2, k3);
    let (u2, n2) = fa(k4, m1, m2);
    let (c1, n3) = ha(u1, u2);
    let (c2, c3) = fa(n1, n2, n3);
    [c0, c1, c2, c3]
}

/// A rule as a boolean function of (centre, count bits), applied to 64 lanes at once.
pub trait RuleKernel: Copy + Send + Sync {
    fn apply(&self, alive: u64, c: [u64; 4]) -> u64;
}

/// Hand-specialised B45/S345: born iff count ∈ {4,5}; survive iff count ∈ {3,4,5}.
#[derive(Clone, Copy)]
pub struct GumpRule;
impl RuleKernel for GumpRule {
    #[inline(always)]
    fn apply(&self, alive: u64, c: [u64; 4]) -> u64 {
        // 4 = 0100, 5 = 0101, 3 = 0011
        !c[3] & ((c[2] & !c[1]) | (alive & !c[2] & c[1] & c[0]))
    }
}

/// Any rule: a 5-variable multiplexer tree over constant leaves.
#[derive(Clone, Copy)]
pub struct GenericRule {
    leaves: [[u64; 16]; 2],
}
impl GenericRule {
    pub fn new(r: Rule) -> Self {
        let mut leaves = [[0u64; 16]; 2];
        for n in 0..16 {
            leaves[0][n] = if n <= 12 && r.next(false, n as u32) { !0 } else { 0 };
            leaves[1][n] = if n <= 12 && r.next(true, n as u32) { !0 } else { 0 };
        }
        GenericRule { leaves }
    }
}
#[inline(always)]
fn sel(s: u64, a: u64, b: u64) -> u64 {
    (a & !s) | (b & s)
}
impl RuleKernel for GenericRule {
    #[inline(always)]
    fn apply(&self, alive: u64, c: [u64; 4]) -> u64 {
        let mut f = [0u64; 2];
        for (al, l) in self.leaves.iter().enumerate() {
            let mut m = [0u64; 8];
            for t in 0..8 {
                m[t] = sel(c[0], l[2 * t], l[2 * t + 1]);
            }
            let mut n = [0u64; 4];
            for t in 0..4 {
                n[t] = sel(c[1], m[2 * t], m[2 * t + 1]);
            }
            let o0 = sel(c[2], n[0], n[1]);
            let o1 = sel(c[2], n[2], n[3]);
            f[al] = sel(c[3], o0, o1);
        }
        sel(alive, f[0], f[1])
    }
}

/// Per-generation reductions computed inside the kernel (when enabled).
#[derive(Clone, Copy, Default, Debug)]
pub struct StepAcc {
    pub hash: u64,
    pub pop: [u64; 3],
    pub diff: u64,
}

impl StepAcc {
    fn merge(&mut self, o: &StepAcc) {
        self.hash = self.hash.wrapping_add(o.hash);
        for a in 0..3 {
            self.pop[a] += o.pop[a];
        }
        self.diff |= o.diff;
    }
}

/// The eight input planes for one word-plane `w`, plus the validity mask plane.
#[derive(Clone, Copy)]
struct Ins<'a> {
    xc: &'a [u64], xm: &'a [u64],
    yc: &'a [u64], yp: &'a [u64], ym: &'a [u64],
    zc: &'a [u64], zp: &'a [u64], zm: &'a [u64],
    vm: &'a [u64],
}

/// Lane-block width: 8 × u64 = one AVX-512 register.
const LANES: usize = 8;

#[inline(always)]
unsafe fn ld<const L: usize>(s: &[u64], i: usize) -> [u64; L] {
    std::ptr::read_unaligned(s.as_ptr().add(i) as *const [u64; L])
}

/// Compute `L` consecutive words at padded plane index `i` for all three orientations.
/// SAFETY: `i - 1 - s ≥ 0` and `i + L + s < plane`.
#[inline(always)]
unsafe fn block<R: RuleKernel, const L: usize>(rule: R, p: Ins, i: usize, s: usize) -> [[u64; L]; 6] {
    let xc = ld::<L>(p.xc, i);
    let yc = ld::<L>(p.yc, i);
    let zc = ld::<L>(p.zc, i);
    let xm = ld::<L>(p.xm, i);
    let vm = ld::<L>(p.vm, i);
    let x_a = ld::<L>(p.xc, i - 1 - s);
    let x_b = ld::<L>(p.xc, i + 1 - s);
    let x_c = ld::<L>(p.xc, i - 1 + s);
    let x_d = ld::<L>(p.xc, i + 1 + s);
    let yc_m1 = ld::<L>(p.yc, i - 1);
    let yp0 = ld::<L>(p.yp, i);
    let yp_m1 = ld::<L>(p.yp, i - 1);
    let zc_ms = ld::<L>(p.zc, i - s);
    let zp0 = ld::<L>(p.zp, i);
    let zp_ms = ld::<L>(p.zp, i - s);
    let ym_ms = ld::<L>(p.ym, i - s);
    let ym_ps = ld::<L>(p.ym, i + s);
    let yp_ms = ld::<L>(p.yp, i - s);
    let yp_ps = ld::<L>(p.yp, i + s);
    let zc_p1 = ld::<L>(p.zc, i + 1);
    let zc_p1ms = ld::<L>(p.zc, i + 1 - s);
    let xm_p1 = ld::<L>(p.xm, i + 1);
    let xc_p1 = ld::<L>(p.xc, i + 1);
    let zm_m1 = ld::<L>(p.zm, i - 1);
    let zm_p1 = ld::<L>(p.zm, i + 1);
    let zp_m1 = ld::<L>(p.zp, i - 1);
    let zp_p1 = ld::<L>(p.zp, i + 1);
    let xc_ps = ld::<L>(p.xc, i + s);
    let xm_ps = ld::<L>(p.xm, i + s);
    let yc_ps = ld::<L>(p.yc, i + s);
    let yc_psm1 = ld::<L>(p.yc, i + s - 1);
    let mut nx = [0u64; L];
    let mut ny = [0u64; L];
    let mut nz = [0u64; L];
    for l in 0..L {
        let cx = count12([
            x_a[l], x_b[l], x_c[l], x_d[l],
            yc[l], yc_m1[l], yp0[l], yp_m1[l],
            zc[l], zc_ms[l], zp0[l], zp_ms[l],
        ]);
        nx[l] = rule.apply(xc[l], cx) & vm[l];
        let cy = count12([
            ym_ms[l], ym_ps[l], yp_ms[l], yp_ps[l],
            zc[l], zc_ms[l], zc_p1[l], zc_p1ms[l],
            xc[l], xm[l], xc_p1[l], xm_p1[l],
        ]);
        ny[l] = rule.apply(yc[l], cy) & vm[l];
        let cz = count12([
            zm_m1[l], zm_p1[l], zp_m1[l], zp_p1[l],
            xc[l], xm[l], xc_ps[l], xm_ps[l],
            yc[l], yc_m1[l], yc_ps[l], yc_psm1[l],
        ]);
        nz[l] = rule.apply(zc[l], cz) & vm[l];
    }
    [nx, ny, nz, xc, yc, zc]
}

#[derive(Clone, Copy)]
struct Accum<const L: usize> {
    hash: [u64; L],
    pop: [[u64; L]; 3],
    diff: [u64; L],
}

impl<const L: usize> Accum<L> {
    fn new() -> Self {
        Accum { hash: [0; L], pop: [[0; L]; 3], diff: [0; L] }
    }
    #[inline(always)]
    fn add(&mut self, r: &[[u64; L]; 6], i: usize, hbase: [u64; 3]) {
        for l in 0..L {
            let gi = (i + l) as u64;
            for a in 0..3 {
                self.hash[l] = self.hash[l].wrapping_add(hmix(r[a][l], gi + hbase[a]));
                self.pop[a][l] += r[a][l].count_ones() as u64;
            }
            self.diff[l] |= (r[0][l] ^ r[3][l]) | (r[1][l] ^ r[4][l]) | (r[2][l] ^ r[5][l]);
        }
    }
    fn into_acc(self, acc: &mut StepAcc) {
        for l in 0..L {
            acc.hash = acc.hash.wrapping_add(self.hash[l]);
            for a in 0..3 {
                acc.pop[a] += self.pop[a][l];
            }
            acc.diff |= self.diff[l];
        }
    }
}

/// Word-plane `w`, padded rows `k0..k1`, all three orientations, as one flat loop over
/// plane indices `[k0·sj + 1, k1·sj − 1)` (ghost columns included; the validity mask
/// zeroes them). Outputs are the row range `k0..k1` of the output planes.
#[allow(clippy::too_many_arguments)]
#[inline(always)]
fn kernel_rows<R: RuleKernel, const STATS: bool>(
    rule: R,
    p: Ins,
    ox: &mut [u64], oy: &mut [u64], oz: &mut [u64],
    k0: usize, k1: usize, sj: usize,
    hbase: [u64; 3],
    rows: Option<&[(u32, u32)]>,
    acc: &mut StepAcc,
) {
    let plane = p.xc.len();
    for q in [p.xm, p.yc, p.yp, p.ym, p.zc, p.zp, p.zm, p.vm] {
        assert_eq!(q.len(), plane);
    }
    assert!(k0 >= 1 && k1 > k0 && (k1 + 1) * sj <= plane);
    let orows = (k1 - k0) * sj;
    assert!(ox.len() == orows && oy.len() == orows && oz.len() == orows);
    let lo = k0 * sj + 1;
    let hi = k1 * sj - 1;
    let obase = k0 * sj;
    let mut a8 = Accum::<LANES>::new();
    let mut a1 = Accum::<1>::new();
    // Compute words [from, to) (to ≤ hi) in blocks of LANES; if `round_up`, the last
    // block may run past `to` (but not past `hi`): the extra words are dead forever
    // (outside the hull) or halo, so they write 0 over 0 and add nothing to the stats.
    let mut span = |from: usize, to: usize, round_up: bool| -> usize {
        let mut i = from;
        // SAFETY: for lo ≤ i and i + L ≤ hi: i - 1 - sj ≥ (k0-1)·sj ≥ 0 and
        // i + L - 1 + 1 + sj ≤ (k1+1)·sj - 1 < plane; outputs i - obase + L ≤ orows.
        unsafe {
            while i + LANES <= hi && (i + LANES <= to || (round_up && i < to)) {
                let r = block::<R, LANES>(rule, p, i, sj);
                let o = i - obase;
                std::ptr::write_unaligned(ox.as_mut_ptr().add(o) as *mut [u64; LANES], r[0]);
                std::ptr::write_unaligned(oy.as_mut_ptr().add(o) as *mut [u64; LANES], r[1]);
                std::ptr::write_unaligned(oz.as_mut_ptr().add(o) as *mut [u64; LANES], r[2]);
                if STATS {
                    a8.add(&r, i, hbase);
                }
                i += LANES;
            }
            while i < to {
                let r = block::<R, 1>(rule, p, i, sj);
                let o = i - obase;
                ox[o] = r[0][0];
                oy[o] = r[1][0];
                oz[o] = r[2][0];
                if STATS {
                    a1.add(&r, i, hbase);
                }
                i += 1;
            }
        }
        i
    };
    match rows {
        None => {
            span(lo, hi, false);
        }
        Some(rows) => {
            // only the j-range of each row that intersects the (convex) diagonal hull
            let mut pos = lo;
            for k in k0..k1 {
                let (jl, jh) = rows[k];
                if jl > jh {
                    continue;
                }
                let from = (k * sj + jl as usize).max(pos);
                let to = k * sj + jh as usize + 1;
                if from < to {
                    pos = span(from, to, true);
                }
            }
        }
    }
    if STATS {
        a8.into_acc(acc);
        a1.into_acc(acc);
    }
}

/// Bit-sliced simulator. See module docs for the layout.
pub struct BitSim {
    geo: Geometry,
    rule: Rule,
    /// words per row (= number of word-planes per orientation)
    nw: usize,
    /// bits used per word
    nb: usize,
    mask: u64,
    /// row stride (ny + 2)
    sj: usize,
    /// words per padded plane ((ny+2)(nz+2))
    plane: usize,
    cur: Vec<u64>,
    nxt: Vec<u64>,
    /// per-thread seam planes: [X(i-1) for w=0, Y(i-1) for w=0, Y(i+1) for w=W-1,
    /// Z(i-1) for w=0, Z(i+1) for w=W-1]; each thread fills the rows it needs
    seams: Vec<Vec<u64>>,
    /// `cur`'s torus halo needs a refresh (after edits); steps keep it fresh themselves
    halo_dirty: bool,
    /// validity mask per padded plane position: B-bit mask inside, 0 on the halo
    vmask: Vec<u64>,
    gen: u64,
    /// `nxt` holds the previous generation (valid right after a step, until the next edit)
    prev_valid: bool,
    /// stats of the most recent step (if computed in-kernel)
    last: Option<StepAcc>,
    /// compute hash / population / changed flag inside the kernel
    pub kernel_stats: bool,
    threads: usize,
    /// open boxes: per padded k, the padded j-range meeting the diagonal hull
    rows: Option<Vec<(u32, u32)>>,
}

impl BitSim {
    pub fn new(geo: Geometry, rule: Rule) -> Result<BitSim, String> {
        let (nw, nb) = match geo.boundary {
            Boundary::Torus => pack_torus(geo.n[0]),
            Boundary::Open => {
                let (w, b) = pack_open(geo.n[0]);
                if w * b != geo.n[0] {
                    // any W with nx % W == 0 and nx/W <= 64 works for an open box too
                    pack_torus(geo.n[0])
                } else {
                    (w, b)
                }
            }
        };
        assert_eq!(nw * nb, geo.n[0]);
        let sj = geo.n[1] + 2;
        let plane = sj * (geo.n[2] + 2);
        let len = 3 * nw * plane;
        let mask = if nb == 64 { !0 } else { (1u64 << nb) - 1 };
        let mut vmask = vec![0u64; plane];
        for k in 1..=geo.n[2] {
            for j in 1..=geo.n[1] {
                vmask[k * sj + j] = mask;
            }
        }
        Ok(BitSim {
            vmask,
            geo,
            rule,
            nw,
            nb,
            mask,
            sj,
            plane,
            cur: vec![0; len],
            nxt: vec![0; len],
            seams: vec![vec![0; 5 * plane]],
            halo_dirty: true,
            gen: 0,
            prev_valid: false,
            last: None,
            kernel_stats: true,
            threads: 1,
            rows: None,
        })
    }

    pub fn geometry(&self) -> &Geometry {
        &self.geo
    }
    pub fn rule(&self) -> Rule {
        self.rule
    }
    pub fn generation(&self) -> u64 {
        self.gen
    }
    pub fn set_generation(&mut self, g: u64) {
        self.gen = g;
    }
    /// `(W, B)`: words per row and bits used per word.
    pub fn packing(&self) -> (usize, usize) {
        (self.nw, self.nb)
    }
    /// Threads used per generation (1 = single-threaded). Only worthwhile for big boxes.
    pub fn set_threads(&mut self, t: usize) {
        self.threads = t.max(1);
    }
    pub fn threads(&self) -> usize {
        self.threads
    }
    /// Stats of the last step computed in-kernel (hash, per-orientation population,
    /// changed flag); `None` before the first step or after an edit.
    pub fn last_step(&self) -> Option<StepAcc> {
        self.last
    }

    #[inline]
    fn word_index(&self, a: usize, c: [usize; 3]) -> (usize, u32) {
        let w = c[0] % self.nw;
        let b = (c[0] / self.nw) as u32;
        ((a * self.nw + w) * self.plane + (c[2] + 1) * self.sj + (c[1] + 1), b)
    }

    pub fn get(&self, p: P3) -> bool {
        match self.geo.locate(p) {
            Some((a, c)) => {
                let (i, b) = self.word_index(a, c);
                (self.cur[i] >> b) & 1 == 1
            }
            None => false,
        }
    }

    /// Set a cell (doubled coordinates). False if not a cell or outside an open box.
    pub fn set(&mut self, p: P3, v: bool) -> bool {
        match self.geo.locate(p) {
            Some((a, c)) => {
                let (i, b) = self.word_index(a, c);
                if v {
                    self.cur[i] |= 1 << b;
                } else {
                    self.cur[i] &= !(1 << b);
                }
                self.prev_valid = false;
                self.last = None;
                self.halo_dirty = true;
                true
            }
            None => false,
        }
    }

    /// Set every listed cell live; returns how many could not be placed.
    pub fn set_cells(&mut self, cells: &[P3]) -> usize {
        cells.iter().filter(|&&p| !self.set(p, true)).count()
    }

    pub fn clear(&mut self) {
        self.cur.iter_mut().for_each(|w| *w = 0);
        self.halo_dirty = true;
        self.prev_valid = false;
        self.last = None;
    }

    /// Call `f(axis, i, j, k)` (local cube coordinates) for every live cell, in storage order.
    pub fn for_each_live(&self, mut f: impl FnMut(usize, usize, usize, usize)) {
        let (ny, nz) = (self.geo.n[1], self.geo.n[2]);
        for a in 0..3 {
            for w in 0..self.nw {
                let base = (a * self.nw + w) * self.plane;
                for k in 0..nz {
                    let row = base + (k + 1) * self.sj + 1;
                    for j in 0..ny {
                        let mut v = self.cur[row + j];
                        while v != 0 {
                            let b = v.trailing_zeros() as usize;
                            v &= v - 1;
                            f(a, b * self.nw + w, j, k);
                        }
                    }
                }
            }
        }
    }

    /// Iterate over interior words: `f(axis, w, j, k, word_cur, word_nxt)`.
    pub fn for_each_word(&self, mut f: impl FnMut(usize, usize, usize, usize, u64, u64)) {
        let (ny, nz) = (self.geo.n[1], self.geo.n[2]);
        for a in 0..3 {
            for w in 0..self.nw {
                let base = (a * self.nw + w) * self.plane;
                for k in 0..nz {
                    let row = base + (k + 1) * self.sj + 1;
                    for j in 0..ny {
                        f(a, w, j, k, self.cur[row + j], self.nxt[row + j]);
                    }
                }
            }
        }
    }

    /// Live cells in doubled coordinates, sorted.
    pub fn cells(&self) -> Vec<P3> {
        let mut v = Vec::new();
        self.for_each_live(|a, i, j, k| v.push(self.geo.to_doubled(a, [i, j, k])));
        v.sort();
        v
    }

    pub fn population_by_axis(&self) -> [u64; 3] {
        let mut p = [0u64; 3];
        self.for_each_word(|a, _, _, _, c, _| p[a] += c.count_ones() as u64);
        p
    }

    pub fn population(&self) -> u64 {
        self.population_by_axis().iter().sum()
    }

    /// Does the spare buffer hold the previous generation (so `changed_cells` works)?
    pub fn has_prev(&self) -> bool {
        self.prev_valid
    }

    /// Number of cells that changed in the last step (None if unknown).
    pub fn changed_cells(&self) -> Option<u64> {
        if !self.prev_valid {
            return None;
        }
        let mut n = 0u64;
        self.for_each_word(|_, _, _, _, c, p| n += (c ^ p).count_ones() as u64);
        Some(n)
    }

    /// Order-independent 64-bit hash of the state (same function the kernel accumulates:
    /// a sum over the kernel's flat index range, halo columns contributing `hmix(0, ·)`).
    pub fn state_hash(&self) -> u64 {
        let nz = self.geo.n[2];
        let mut h = 0u64;
        for pl in 0..3 * self.nw {
            let base = pl * self.plane;
            for i in self.sj + 1..(nz + 1) * self.sj - 1 {
                h = h.wrapping_add(hmix(self.cur[base + i] & self.vmask[i], (i + base) as u64));
            }
        }
        h
    }

    /// Raw access for snapshots: does local cell (a, i, j, k) live?
    pub fn get_local(&self, a: usize, c: [usize; 3]) -> bool {
        let (i, b) = self.word_index(a, c);
        (self.cur[i] >> b) & 1 == 1
    }

    fn fill_halo(&mut self) {
        if self.geo.boundary != Boundary::Torus {
            return;
        }
        let (ny, nz, sj) = (self.geo.n[1], self.geo.n[2], self.sj);
        for pl in 0..3 * self.nw {
            let p = &mut self.cur[pl * self.plane..(pl + 1) * self.plane];
            for k in 1..=nz {
                let r = k * sj;
                p[r] = p[r + ny];
                p[r + ny + 1] = p[r + 1];
            }
            p.copy_within(nz * sj..(nz + 1) * sj, 0);
            p.copy_within(sj..2 * sj, (nz + 1) * sj);
        }
    }

    /// Raw kernel context for the current buffers.
    fn ctx(&mut self) -> Ctx {
        Ctx {
            cur: self.cur.as_ptr(),
            nxt: self.nxt.as_mut_ptr(),
            vmask: self.vmask.as_ptr(),
            nw: self.nw,
            nb: self.nb,
            mask: self.mask,
            plane: self.plane,
            sj: self.sj,
            ny: self.geo.n[1],
            nz: self.geo.n[2],
            torus: self.geo.boundary == Boundary::Torus,
            stats: self.kernel_stats,
            generic: if self.rule.is_gump() { None } else { Some(GenericRule::new(self.rule)) },
            rows: self.rows.as_ref().map(|r| (r.as_ptr(), r.len())),
        }
    }

    fn prepare(&mut self) {
        if self.halo_dirty {
            self.fill_halo();
            self.halo_dirty = false;
        }
    }

    fn finish(&mut self, acc: StepAcc) {
        std::mem::swap(&mut self.cur, &mut self.nxt);
        self.gen += 1;
        self.prev_valid = true;
        self.last = if self.kernel_stats { Some(acc) } else { None };
    }

    /// Advance one generation (single-threaded; see [`BitSim::run_steps`] for threads).
    pub fn step(&mut self) {
        self.prepare();
        let ctx = self.ctx();
        let mut acc = StepAcc::default();
        let seam = self.seams[0].as_mut_ptr();
        // SAFETY: ctx points at live buffers of self; rows 1..=nz written by this call only.
        unsafe { ctx.run(1, self.geo.n[2] + 1, seam, &mut acc) };
        self.finish(acc);
    }

    /// Advance `n` generations (uses the configured thread count).
    pub fn steps(&mut self, n: u64) {
        self.run_steps(n, |_| true);
    }

    /// Advance up to `max` generations, calling `f(self)` after each one; stop early when
    /// it returns false. Returns the number of generations advanced. With `threads > 1`
    /// a team of threads persists for the whole call and splits every generation by
    /// rows, synchronised by a spin barrier; `f` runs on the calling thread while the
    /// workers wait.
    pub fn run_steps(&mut self, max: u64, mut f: impl FnMut(&mut BitSim) -> bool) -> u64 {
        let t = self.threads.min(self.geo.n[2]).max(1);
        if t == 1 || max == 0 {
            for g in 0..max {
                self.step();
                if !f(self) {
                    return g + 1;
                }
            }
            return max;
        }
        let nz = self.geo.n[2];
        // chunks of rows handed out dynamically: a descheduled thread (oversubscribed
        // machine) delays nobody, the others just take its chunks
        let rows_per_chunk = (nz / (4 * t)).max(4);
        let chunks: Vec<(usize, usize)> =
            (1..=nz).step_by(rows_per_chunk).map(|k0| (k0, (k0 + rows_per_chunk).min(nz + 1))).collect();
        while self.seams.len() < t {
            self.seams.push(vec![0; 5 * self.plane]);
        }
        let seam_ptrs: Vec<SeamPtr> = self.seams.iter_mut().map(|v| SeamPtr(v.as_mut_ptr())).collect();
        let team = Team::new(t, chunks);
        let mut done = 0u64;
        std::thread::scope(|sc| {
            for ti in 1..t {
                let (team, sp) = (&team, seam_ptrs[ti]);
                sc.spawn(move || {
                    let mut seen = 0u64;
                    while team.wait_epoch(&mut seen) {
                        team.work(ti, seen, sp.get());
                    }
                });
            }
            let mut go = true;
            let mut epoch = 0u64;
            while go && done < max {
                self.prepare();
                epoch += 1;
                team.publish(self.ctx(), epoch);
                team.work(0, epoch, seam_ptrs[0].get());
                let acc = team.finish();
                self.finish(acc);
                done += 1;
                go = f(self);
            }
            team.quit();
        });
        done
    }

    /// Open boxes, rules with min birth ≥ 4: compute only rows that meet the diagonal hull
    /// `hull` (which must contain every live cell; by T2 nothing outside it ever lives).
    /// About 2× fewer words for octahedral hulls. `None` (or a torus, or a rule with
    /// births below 4) computes everything. Returns whether a restriction is active.
    pub fn restrict_to_hull(&mut self, hull: Option<&crate::lattice::Hull>) -> bool {
        let ok = self.geo.boundary == Boundary::Open && self.rule.min_birth().is_none_or(|b| b >= 4);
        let Some(h) = hull.filter(|_| ok) else {
            self.rows = None;
            return false;
        };
        debug_assert!(self.cells().iter().all(|&p| h.contains(p)));
        let (nx, ny, nz) = (self.geo.n[0], self.geo.n[1], self.geo.n[2]);
        let mut rows = vec![(1u32, 0u32); nz + 2];
        for k in 0..nz {
            let mut jl = u32::MAX;
            let mut jh = 0u32;
            for j in 0..ny {
                let hit = (0..3).any(|a| (0..nx).any(|i| h.contains(self.geo.to_doubled(a, [i, j, k]))));
                if hit {
                    jl = jl.min(j as u32 + 1);
                    jh = jh.max(j as u32 + 1);
                }
            }
            if jl <= jh {
                rows[k + 1] = (jl, jh);
            }
        }
        // Words the kernel no longer computes must be 0 in both buffers. `cur` is (all
        // live cells are inside the hull); the spare buffer may still hold an older,
        // larger pattern, so clear it there.
        for pl in 0..3 * self.nw {
            for (k, &(jl, jh)) in rows.iter().enumerate() {
                let row = pl * self.plane + k * self.sj;
                for j in 0..self.sj {
                    if !(jl as usize..=jh as usize).contains(&j) {
                        debug_assert_eq!(self.cur[row + j] & self.vmask[k * self.sj + j], 0);
                        self.nxt[row + j] = 0;
                    }
                }
            }
        }
        self.prev_valid = false;
        self.rows = Some(rows);
        true
    }

    /// Fraction of padded rows' words the kernel computes (1.0 without a restriction).
    pub fn work_fraction(&self) -> f64 {
        match &self.rows {
            None => 1.0,
            Some(r) => {
                let n: usize = r.iter().map(|&(a, b)| if a <= b { (b - a + 1) as usize } else { 0 }).sum();
                n as f64 / (self.geo.n[1] * self.geo.n[2]) as f64
            }
        }
    }

    /// Exact state equality (same geometry assumed).
    pub fn same_state(&self, other: &BitSim) -> bool {
        if self.geo != other.geo {
            return false;
        }
        let mut eq = true;
        let o = &other.cur;
        self.for_each_word_index(|i| eq &= self.cur[i] == o[i]);
        eq
    }

    fn for_each_word_index(&self, mut f: impl FnMut(usize)) {
        let (ny, nz) = (self.geo.n[1], self.geo.n[2]);
        for pl in 0..3 * self.nw {
            for k in 1..=nz {
                let row = pl * self.plane + k * self.sj;
                for j in 1..=ny {
                    f(row + j);
                }
            }
        }
    }
}

impl Clone for BitSim {
    fn clone(&self) -> Self {
        BitSim {
            geo: self.geo.clone(),
            rule: self.rule,
            nw: self.nw,
            nb: self.nb,
            mask: self.mask,
            sj: self.sj,
            plane: self.plane,
            cur: self.cur.clone(),
            nxt: self.nxt.clone(),
            seams: vec![self.seams[0].clone()],
            halo_dirty: self.halo_dirty,
            vmask: self.vmask.clone(),
            gen: self.gen,
            prev_valid: self.prev_valid,
            last: self.last,
            kernel_stats: self.kernel_stats,
            threads: 1,
            rows: self.rows.clone(),
        }
    }
}

#[derive(Clone, Copy)]
struct SeamPtr(*mut u64);
unsafe impl Send for SeamPtr {}
unsafe impl Sync for SeamPtr {}
impl SeamPtr {
    fn get(self) -> *mut u64 {
        self.0
    }
}

#[repr(align(128))]
struct PaddedAcc(std::cell::UnsafeCell<StepAcc>);
unsafe impl Sync for PaddedAcc {}
/// A team of threads stepping one simulation: the main thread publishes a generation
/// (epoch); every thread, main included, claims row chunks with a CAS on
/// `(epoch << 32) | next_chunk`; the main thread waits until all chunks are done. Idle
/// workers spin briefly, then sleep on a condition variable. A descheduled worker (on an
/// oversubscribed machine) therefore never stalls a generation.
struct Team {
    epoch_chunk: std::sync::atomic::AtomicU64,
    done: std::sync::atomic::AtomicUsize,
    quit: std::sync::atomic::AtomicBool,
    sleepers: std::sync::atomic::AtomicUsize,
    ctx: std::cell::UnsafeCell<Option<Ctx>>,
    chunks: Vec<(usize, usize)>,
    accs: Vec<PaddedAcc>,
    lock: std::sync::Mutex<()>,
    cv: std::sync::Condvar,
}
unsafe impl Sync for Team {}

impl Team {
    fn new(threads: usize, chunks: Vec<(usize, usize)>) -> Team {
        use std::sync::atomic::*;
        Team {
            epoch_chunk: AtomicU64::new(0),
            done: AtomicUsize::new(0),
            quit: AtomicBool::new(false),
            sleepers: AtomicUsize::new(0),
            ctx: std::cell::UnsafeCell::new(None),
            chunks,
            accs: (0..threads).map(|_| PaddedAcc(std::cell::UnsafeCell::new(StepAcc::default()))).collect(),
            lock: std::sync::Mutex::new(()),
            cv: std::sync::Condvar::new(),
        }
    }

    /// Main thread: start generation `epoch` with `ctx`.
    fn publish(&self, ctx: Ctx, epoch: u64) {
        use std::sync::atomic::Ordering::*;
        for a in &self.accs {
            // SAFETY: every chunk of the previous epoch is done; nobody writes accs now.
            unsafe { *a.0.get() = StepAcc::default() };
        }
        self.done.store(0, Relaxed);
        unsafe { *self.ctx.get() = Some(ctx) };
        self.epoch_chunk.store(epoch << 32, SeqCst);
        if self.sleepers.load(SeqCst) > 0 {
            let _g = self.lock.lock().unwrap();
            self.cv.notify_all();
        }
    }

    /// Worker: wait for an epoch newer than `seen` (updated). False when quitting.
    fn wait_epoch(&self, seen: &mut u64) -> bool {
        use std::sync::atomic::Ordering::*;
        let newer = |s: &Self| (s.epoch_chunk.load(SeqCst) >> 32) > *seen || s.quit.load(SeqCst);
        let mut spins = 0u32;
        while !newer(self) {
            if spins < 20_000 {
                std::hint::spin_loop();
                spins += 1;
            } else {
                self.sleepers.fetch_add(1, SeqCst);
                let mut g = self.lock.lock().unwrap();
                while !newer(self) {
                    g = self.cv.wait(g).unwrap();
                }
                drop(g);
                self.sleepers.fetch_sub(1, SeqCst);
            }
        }
        if self.quit.load(SeqCst) {
            return false;
        }
        *seen = self.epoch_chunk.load(SeqCst) >> 32;
        true
    }

    /// Claim and run chunks of `epoch` until none are left.
    fn work(&self, ti: usize, epoch: u64, seam: *mut u64) {
        use std::sync::atomic::Ordering::*;
        loop {
            let cur = self.epoch_chunk.load(Acquire);
            if cur >> 32 != epoch {
                return;
            }
            let idx = (cur & 0xffff_ffff) as usize;
            if idx >= self.chunks.len() {
                return;
            }
            if self.epoch_chunk.compare_exchange_weak(cur, cur + 1, AcqRel, Relaxed).is_err() {
                continue;
            }
            // SAFETY: the epoch cannot end before this claimed chunk is done, so the main
            // thread does not touch ctx/accs meanwhile; chunks are disjoint row ranges.
            let ctx = unsafe { (*self.ctx.get()).unwrap() };
            let (k0, k1) = self.chunks[idx];
            let mut acc = StepAcc::default();
            unsafe { ctx.run(k0, k1, seam, &mut acc) };
            unsafe { (*self.accs[ti].0.get()).merge(&acc) };
            self.done.fetch_add(1, Release);
        }
    }

    /// Main thread: wait for all chunks, return the merged reductions.
    fn finish(&self) -> StepAcc {
        use std::sync::atomic::Ordering::*;
        let mut spins = 0u32;
        while self.done.load(Acquire) < self.chunks.len() {
            if spins < 50_000 {
                std::hint::spin_loop();
                spins += 1;
            } else {
                std::thread::yield_now();
            }
        }
        let mut acc = StepAcc::default();
        for a in &self.accs {
            acc.merge(unsafe { &*a.0.get() });
        }
        acc
    }

    fn quit(&self) {
        use std::sync::atomic::Ordering::SeqCst;
        self.quit.store(true, SeqCst);
        let _g = self.lock.lock().unwrap();
        self.cv.notify_all();
    }
}

/// Raw pointers + parameters for running the kernel on a row range.
#[derive(Clone, Copy)]
struct Ctx {
    cur: *const u64,
    nxt: *mut u64,
    vmask: *const u64,
    nw: usize,
    nb: usize,
    mask: u64,
    plane: usize,
    sj: usize,
    ny: usize,
    nz: usize,
    torus: bool,
    stats: bool,
    generic: Option<GenericRule>,
    /// per padded k: inclusive padded j-range to compute (None: everything)
    rows: Option<(*const (u32, u32), usize)>,
}
unsafe impl Send for Ctx {}
unsafe impl Sync for Ctx {}

impl Ctx {
    /// One generation for padded rows `k0..k1`: build this thread's seam rows
    /// `k0-1..=k1` (from `cur`, whose halo is complete), run the kernel into `nxt`, then
    /// (torus) refresh `nxt`'s halo for the rows written — so the next generation needs no
    /// serial preparation.
    /// SAFETY: pointers valid for the buffers' lengths; `seam` private to the caller (5
    /// planes); no concurrent writer to `cur`; rows `k0..k1` of `nxt` (plus halo row 0 if
    /// `k1 == nz+1`, halo row nz+1 if `k0 == 1`) written by this call only.
    unsafe fn run(&self, k0: usize, k1: usize, seam: *mut u64, acc: &mut StepAcc) {
        if k0 >= k1 {
            return;
        }
        self.seam_rows(seam, k0 - 1, k1);
        match (self.generic, self.stats) {
            (None, true) => self.run_impl::<GumpRule, true>(GumpRule, k0, k1, seam, acc),
            (None, false) => self.run_impl::<GumpRule, false>(GumpRule, k0, k1, seam, acc),
            (Some(g), true) => self.run_impl::<GenericRule, true>(g, k0, k1, seam, acc),
            (Some(g), false) => self.run_impl::<GenericRule, false>(g, k0, k1, seam, acc),
        }
        if self.torus {
            self.halo_rows(k0, k1);
        }
    }

    /// Seam planes, padded rows `r0..=r1`.
    unsafe fn seam_rows(&self, seam: *mut u64, r0: usize, r1: usize) {
        let (nw, plane, sj, nb, mask) = (self.nw, self.plane, self.sj, self.nb as u32, self.mask);
        let first = |a: usize| (a * nw) * plane;
        let last = |a: usize| (a * nw + nw - 1) * plane;
        // (source plane, towards higher i?)
        let jobs = [(last(0), true), (last(1), true), (first(1), false), (last(2), true), (first(2), false)];
        let (lo, n) = (r0 * sj, (r1 + 1 - r0) * sj);
        for (t, &(src, up)) in jobs.iter().enumerate() {
            let s = std::slice::from_raw_parts(self.cur.add(src + lo), n);
            let d = std::slice::from_raw_parts_mut(seam.add(t * plane + lo), n);
            match (up, self.torus) {
                // plane 0 at i-1: bit b <- bit b-1 of plane W-1; bit 0 <- bit B-1 (torus)
                (true, true) => d.iter_mut().zip(s).for_each(|(o, &v)| *o = ((v << 1) & mask) | ((v >> (nb - 1)) & 1)),
                (true, false) => d.iter_mut().zip(s).for_each(|(o, &v)| *o = (v << 1) & mask),
                // plane W-1 at i+1: bit b <- bit b+1 of plane 0; bit B-1 <- bit 0 (torus)
                (false, true) => d.iter_mut().zip(s).for_each(|(o, &v)| *o = (v >> 1) | ((v & 1) << (nb - 1))),
                (false, false) => d.iter_mut().zip(s).for_each(|(o, &v)| *o = v >> 1),
            }
        }
    }

    /// Torus halo of `nxt` for rows `k0..k1` (j columns), plus the k halo rows owned by
    /// the first / last row block.
    unsafe fn halo_rows(&self, k0: usize, k1: usize) {
        let (ny, nz, sj) = (self.ny, self.nz, self.sj);
        for pl in 0..3 * self.nw {
            let p = std::slice::from_raw_parts_mut(self.nxt.add(pl * self.plane), self.plane);
            for k in k0..k1 {
                let r = k * sj;
                p[r] = p[r + ny];
                p[r + ny + 1] = p[r + 1];
            }
            if k0 == 1 {
                p.copy_within(sj..2 * sj, (nz + 1) * sj);
            }
            if k1 == nz + 1 {
                p.copy_within(nz * sj..(nz + 1) * sj, 0);
            }
        }
    }

    unsafe fn run_impl<R: RuleKernel, const STATS: bool>(&self, rule: R, k0: usize, k1: usize, seam: *mut u64, acc: &mut StepAcc) {
        let (nw, plane, sj) = (self.nw, self.plane, self.sj);
        let pl = |a: usize, w: usize| std::slice::from_raw_parts(self.cur.add((a * nw + w) * plane), plane);
        let seam = |t: usize| std::slice::from_raw_parts(seam.add(t * plane) as *const u64, plane);
        let vm = std::slice::from_raw_parts(self.vmask, plane);
        let rows = (k1 - k0) * sj;
        let rr = self.rows.map(|(p, n)| std::slice::from_raw_parts(p, n));
        for w in 0..nw {
            let ins = Ins {
                xc: pl(0, w),
                xm: if w > 0 { pl(0, w - 1) } else { seam(0) },
                yc: pl(1, w),
                ym: if w > 0 { pl(1, w - 1) } else { seam(1) },
                yp: if w + 1 < nw { pl(1, w + 1) } else { seam(2) },
                zc: pl(2, w),
                zm: if w > 0 { pl(2, w - 1) } else { seam(3) },
                zp: if w + 1 < nw { pl(2, w + 1) } else { seam(4) },
                vm,
            };
            let o = |a: usize| std::slice::from_raw_parts_mut(self.nxt.add((a * nw + w) * plane + k0 * sj), rows);
            let hb = [(w * plane) as u64, ((nw + w) * plane) as u64, ((2 * nw + w) * plane) as u64];
            kernel_rows::<R, STATS>(rule, ins, o(0), o(1), o(2), k0, k1, sj, hb, rr, acc);
        }
    }
}
