//! Instruments: measurements taken from a `BitSim` on demand (decoupled from stepping).
//!
//! * [`Sample`]: population (total, per orientation), bounding box, cells changed since
//!   the previous generation, per-layer populations along the 4 body diagonals, the
//!   diagonal hull and firewalls derived from them.
//! * [`LayerTracker`]: per-layer "last seen alive" and the generation at which each layer
//!   became *provably* dead forever (outside the hull: T2; inside a run of ≥ 3 dead layers:
//!   T3), plus a check that proven-dead layers indeed stay dead.
//! * [`HaltDetector`]: extinct / still life / periodic (period, generation the cycle was
//!   entered), from the per-generation state hash computed in the kernel.

use crate::fast::BitSim;
use crate::lattice::{Boundary, Hull, P3, DIAGS};
use std::collections::{HashMap, VecDeque};

/// Per-layer populations along one diagonal axis. `counts[n]` is the number of live cells
/// with layer coordinate `s = s_min + 2n` (torus: `s` reduced mod `modulus`).
#[derive(Clone, Debug, PartialEq)]
pub struct LayerHist {
    pub s_min: i64,
    pub counts: Vec<u64>,
    pub modulus: Option<i64>,
}

impl LayerHist {
    pub fn s_of(&self, n: usize) -> i64 {
        self.s_min + 2 * n as i64
    }
    /// Lowest / highest non-empty layer (open boxes).
    pub fn extent(&self) -> Option<(i64, i64)> {
        let lo = self.counts.iter().position(|&c| c > 0)?;
        let hi = self.counts.iter().rposition(|&c| c > 0)?;
        Some((self.s_of(lo), self.s_of(hi)))
    }
    /// Maximal runs of `>= min_len` consecutive dead layers strictly inside the live
    /// extent (open) or anywhere on the ring (torus). Returned as `(index_first, len)`
    /// (indices into `counts`; on a torus a run may wrap past the end).
    pub fn dead_runs(&self, min_len: usize) -> Vec<(usize, usize)> {
        let n = self.counts.len();
        let mut out = Vec::new();
        if self.counts.iter().all(|&c| c == 0) {
            return out;
        }
        if self.modulus.is_none() {
            let lo = self.counts.iter().position(|&c| c > 0).unwrap();
            let hi = self.counts.iter().rposition(|&c| c > 0).unwrap();
            let mut i = lo;
            while i <= hi {
                if self.counts[i] == 0 {
                    let st = i;
                    while self.counts[i] == 0 {
                        i += 1;
                    }
                    if i - st >= min_len {
                        out.push((st, i - st));
                    }
                } else {
                    i += 1;
                }
            }
        } else {
            // ring: start scanning just after a live layer
            let start = (self.counts.iter().position(|&c| c > 0).unwrap() + 1) % n;
            let mut t = 0;
            while t < n {
                let i = (start + t) % n;
                if self.counts[i] == 0 {
                    let st = t;
                    while t < n && self.counts[(start + t) % n] == 0 {
                        t += 1;
                    }
                    if t - st >= min_len {
                        out.push(((start + st) % n, t - st));
                    }
                } else {
                    t += 1;
                }
            }
        }
        out
    }
    /// Firewalls as inclusive layer-coordinate ranges `(s_first, s_last)`.
    pub fn firewalls(&self) -> Vec<(i64, i64)> {
        let n = self.counts.len();
        self.dead_runs(3)
            .into_iter()
            .map(|(st, len)| {
                let last = (st + len - 1) % n.max(1);
                (self.s_of(st), self.s_of(last))
            })
            .collect()
    }
}

#[derive(Clone, Debug)]
pub struct Sample {
    pub gen: u64,
    pub pop: u64,
    pub pop_axis: [u64; 3],
    /// cells that changed in the step that produced this generation
    pub changed: Option<u64>,
    /// doubled-coordinate bounding box of live cells
    pub bbox: Option<(P3, P3)>,
    pub layers: Option<[LayerHist; 4]>,
}

impl Sample {
    /// Diagonal hull (open boxes only; needs layers).
    pub fn hull(&self) -> Option<Hull> {
        let l = self.layers.as_ref()?;
        if l[0].modulus.is_some() {
            return None;
        }
        let mut h = [(0, 0); 4];
        for d in 0..4 {
            h[d] = l[d].extent()?;
        }
        Some(Hull(h))
    }
    pub fn firewalls(&self) -> Option<[Vec<(i64, i64)>; 4]> {
        let l = self.layers.as_ref()?;
        Some([l[0].firewalls(), l[1].firewalls(), l[2].firewalls(), l[3].firewalls()])
    }
}

/// Measure `sim` now. `layers` adds the per-layer populations (one pass over live cells).
pub fn sample(sim: &BitSim, layers: bool) -> Sample {
    let geo = sim.geometry();
    let (nw, _nb) = sim.packing();
    let mut pop_axis = [0u64; 3];
    let mut lo = [i64::MAX; 3];
    let mut hi = [i64::MIN; 3];
    let modulus = geo.layer_modulus();
    let mut hists: Vec<LayerHist> = (0..4)
        .map(|d| {
            let (smin, smax) = geo.layer_range(d);
            LayerHist { s_min: smin, counts: vec![0; ((smax - smin) / 2 + 1) as usize], modulus }
        })
        .collect();
    let mut changed = 0u64;
    let have_prev = sim.has_prev();
    sim.for_each_word(|a, w, j, k, v, prev| {
        if have_prev {
            changed += (v ^ prev).count_ones() as u64;
        }
        if v == 0 {
            return;
        }
        pop_axis[a] += v.count_ones() as u64;
        // x of bit b: cube i = b*nw + w → doubled 2(i + ox) + [a==0]
        let p0 = geo.to_doubled(a, [w, j, k]); // bit 0
        let b_lo = v.trailing_zeros() as i64;
        let b_hi = 63 - v.leading_zeros() as i64;
        lo[0] = lo[0].min(p0[0] + 2 * nw as i64 * b_lo);
        hi[0] = hi[0].max(p0[0] + 2 * nw as i64 * b_hi);
        for t in 1..3 {
            lo[t] = lo[t].min(p0[t]);
            hi[t] = hi[t].max(p0[t]);
        }
        if layers {
            for d in 0..4 {
                let dv = DIAGS[d];
                let s0 = dv[0] * p0[0] + dv[1] * p0[1] + dv[2] * p0[2];
                let ds = dv[0] * 2 * nw as i64; // change of s per bit
                let h = &mut hists[d];
                let mut x = v;
                match modulus {
                    None => {
                        while x != 0 {
                            let b = x.trailing_zeros() as i64;
                            x &= x - 1;
                            let s = s0 + ds * b;
                            h.counts[((s - h.s_min) / 2) as usize] += 1;
                        }
                    }
                    Some(m) => {
                        while x != 0 {
                            let b = x.trailing_zeros() as i64;
                            x &= x - 1;
                            let s = (s0 + ds * b).rem_euclid(m);
                            h.counts[((s - 1) / 2) as usize] += 1;
                        }
                    }
                }
            }
        }
    });
    let pop = pop_axis.iter().sum();
    let bbox = if pop > 0 { Some((lo, hi)) } else { None };
    let layers = if layers {
        let mut it = hists.into_iter();
        Some([it.next().unwrap(), it.next().unwrap(), it.next().unwrap(), it.next().unwrap()])
    } else {
        None
    };
    Sample { gen: sim.generation(), pop, pop_axis, changed: if have_prev { Some(changed) } else { None }, bbox, layers }
}

/// One irreversible layer death.
#[derive(Clone, Debug, PartialEq)]
pub struct LayerEvent {
    /// generation of the sample at which the layer was first seen provably dead
    pub gen: u64,
    pub axis: usize,
    pub s: i64,
    /// last sampled generation at which the layer had a live cell (None: never seen alive)
    pub last_alive: Option<u64>,
    /// "hull" (outside the diagonal hull, T2) or "firewall" (inside ≥3 dead layers, T3)
    pub cause: &'static str,
}

/// Tracks, per diagonal layer, when it was last seen alive and when it became provably
/// dead forever. Feed it samples with layers, in increasing generation order.
pub struct LayerTracker {
    pub s_min: [i64; 4],
    pub last_alive: [Vec<Option<u64>>; 4],
    pub proven: [Vec<Option<u64>>; 4],
    /// layers that are relevant: inside the first sample's hull (open) / all (torus)
    relevant: [Vec<bool>; 4],
    /// proven-dead layers later found alive (must stay empty: T2/T3)
    pub violations: Vec<(u64, usize, i64)>,
    initialised: bool,
}

impl Default for LayerTracker {
    fn default() -> Self {
        Self::new()
    }
}

impl LayerTracker {
    pub fn new() -> Self {
        LayerTracker {
            s_min: [0; 4],
            last_alive: Default::default(),
            proven: Default::default(),
            relevant: Default::default(),
            violations: Vec::new(),
            initialised: false,
        }
    }

    /// Update with a sample; returns the new irreversible-death events.
    pub fn update(&mut self, s: &Sample) -> Vec<LayerEvent> {
        let layers = s.layers.as_ref().expect("LayerTracker needs samples with layers");
        let mut events = Vec::new();
        for d in 0..4 {
            let h = &layers[d];
            let n = h.counts.len();
            if !self.initialised {
                self.s_min[d] = h.s_min;
                self.last_alive[d] = vec![None; n];
                self.proven[d] = vec![None; n];
                self.relevant[d] = match (h.modulus, h.extent()) {
                    (None, Some((lo, hi))) => (0..n).map(|i| h.s_of(i) >= lo && h.s_of(i) <= hi).collect(),
                    (None, None) => vec![false; n],
                    (Some(_), _) => vec![true; n],
                };
            }
            for i in 0..n {
                if h.counts[i] > 0 {
                    self.last_alive[d][i] = Some(s.gen);
                    if self.proven[d][i].is_some() {
                        self.violations.push((s.gen, d, h.s_of(i)));
                    }
                }
            }
            // provably dead now
            let mut dead = vec![None::<&'static str>; n];
            let all_dead = h.counts.iter().all(|&c| c == 0);
            if all_dead {
                for x in dead.iter_mut() {
                    *x = Some("extinct");
                }
            } else {
                if h.modulus.is_none() {
                    let (lo, hi) = h.extent().unwrap();
                    for (i, x) in dead.iter_mut().enumerate() {
                        let sv = h.s_of(i);
                        if sv < lo || sv > hi {
                            *x = Some("hull");
                        }
                    }
                }
                for (st, len) in h.dead_runs(3) {
                    for t in 0..len {
                        dead[(st + t) % n] = Some("firewall");
                    }
                }
            }
            for i in 0..n {
                if let Some(cause) = dead[i] {
                    if self.proven[d][i].is_none() && self.relevant[d][i] {
                        self.proven[d][i] = Some(s.gen);
                        events.push(LayerEvent {
                            gen: s.gen,
                            axis: d,
                            s: h.s_of(i),
                            last_alive: self.last_alive[d][i],
                            cause,
                        });
                    }
                }
            }
        }
        self.initialised = true;
        events
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Status {
    Running,
    Extinct,
    Still,
    Periodic,
}

impl Status {
    pub fn name(&self) -> &'static str {
        match self {
            Status::Running => "running",
            Status::Extinct => "extinct",
            Status::Still => "still",
            Status::Periodic => "periodic",
        }
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Halt {
    pub status: Status,
    /// period (1 for still lifes and extinction)
    pub period: u64,
    /// first generation of the final cycle (for extinction: first empty generation)
    pub cycle_start: u64,
    /// generation at which the halt was detected
    pub detected: u64,
}

/// Cycle detection from per-generation hashes: the first generation `g` whose state hash
/// equals that of an earlier generation `g'` (within the window) gives period `g − g'` and
/// cycle start `g'` (states before the first repeat are all distinct, so `g'` is exactly
/// the entry generation). The caller then verifies the candidate exactly.
pub struct HaltDetector {
    seen: HashMap<u64, u64>,
    order: VecDeque<(u64, u64)>,
    window: usize,
}

impl HaltDetector {
    pub fn new(window: usize) -> Self {
        HaltDetector { seen: HashMap::new(), order: VecDeque::new(), window: window.max(1) }
    }

    /// Record generation `gen`'s hash. Returns a candidate `(period, cycle_start)`.
    pub fn observe(&mut self, gen: u64, hash: u64) -> Option<(u64, u64)> {
        if let Some(&g0) = self.seen.get(&hash) {
            return Some((gen - g0, g0));
        }
        self.seen.insert(hash, gen);
        self.order.push_back((hash, gen));
        if self.order.len() > self.window {
            let (h, g) = self.order.pop_front().unwrap();
            if self.seen.get(&h) == Some(&g) {
                self.seen.remove(&h);
            }
        }
        None
    }

    /// Forget a hash (after a candidate failed verification).
    pub fn forget(&mut self, hash: u64) {
        self.seen.remove(&hash);
    }

    pub fn reset(&mut self) {
        self.seen.clear();
        self.order.clear();
    }
}


/// Convenience: is the boundary open?
pub fn is_open(sim: &BitSim) -> bool {
    sim.geometry().boundary == Boundary::Open
}
