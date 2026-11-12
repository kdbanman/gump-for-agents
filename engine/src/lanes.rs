//! Ensemble engine: up to `MAX_LANES` independent runs packed side by side in every word
//! (see `BitSim::new_packed`), with halting detection that costs almost nothing per
//! generation:
//!
//! * extinction and still lifes: exact, every generation, from the kernel's per-lane
//!   population and changed bits;
//! * cycles of period ≥ 2: a per-lane state hash every `K` generations ("checkpoints").
//!   The first checkpoint whose hash was seen before identifies a cycle; the exact period
//!   is found by stepping a copy until it returns, and the exact cycle start `μ` by
//!   re-simulating from the last checkpoint before the cycle (kept in a ring of state
//!   snapshots) with two copies `p` generations apart;
//! * at the generation cap, a closing check (step a copy up to `closing` generations)
//!   catches cycles that completed before the cap but after the last useful checkpoint.
//!
//! Results are reported exactly as `run::run` would (cycle start, period, final generation
//! `μ + p`, final state, hash, hull, layer events, peak): the final state is rebuilt in a
//! box of the run's own (natural) geometry. Equivalence with per-generation hashing holds
//! for every period up to `closing` (and up to `window` for cycles caught at checkpoints).

use crate::fast::BitSim;
use crate::instruments::{sample, Halt, LayerTracker, Sample, Status};
use crate::lattice::{Geometry, Hull, P3};
use crate::rule::Rule;
use crate::run::RunResult;
use std::collections::{HashMap, VecDeque};
use std::time::Instant;

#[derive(Clone, Debug)]
pub struct LaneOpts {
    /// generation cap per run (counted from its start)
    pub cap: u64,
    /// checkpoint interval K
    pub check_every: u64,
    /// checkpoints remembered per lane for cycle detection
    pub window: usize,
    /// state snapshots kept (for cycle-start recovery)
    pub ring: usize,
    /// closing check length at the cap
    pub closing: u64,
    /// layer tracker (layer_events / theorem_violations in the summary)
    pub need_layers: bool,
}

impl Default for LaneOpts {
    fn default() -> Self {
        LaneOpts { cap: 1_000_000, check_every: 32, window: 1 << 11, ring: 64, closing: 512, need_layers: true }
    }
}

/// One run to do.
pub struct Job<T> {
    pub cells: Vec<P3>,
    /// the box `run::run` would have used (summary fields refer to it)
    pub natural: Geometry,
    pub start_gen: u64,
    pub tag: T,
}

/// A finished run: its result, and its final state in its natural box.
pub struct Done<T> {
    pub tag: T,
    pub res: RunResult,
    pub sim: BitSim,
}

struct Lane<T> {
    job: Job<T>,
    /// global generation at which the lane started
    start: u64,
    first: Sample,
    peak: (u64, u64),
    seen: HashMap<u64, u64>,
    order: VecDeque<(u64, u64)>,
    t0: Instant,
}

/// Run all jobs that `next_job` yields, `lanes` at a time, in boxes `pack_geo`.
/// Every job's cells must lie in `pack_geo` and its dynamics there must equal its dynamics
/// in `job.natural` (same box, or both open boxes holding its hull with a rule whose min
/// birth is ≥ 4).
pub fn run_lanes<T>(
    pack_geo: &Geometry,
    rule: Rule,
    lanes: usize,
    opts: &LaneOpts,
    mut next_job: impl FnMut() -> Option<Job<T>>,
    mut done: impl FnMut(Done<T>),
) {
    let mut sim = BitSim::new_packed(pack_geo, rule, lanes).expect("lane packing");
    let birth0 = rule.birth & 1 == 1;
    let k = opts.check_every.max(1);
    let mut slots: Vec<Option<Lane<T>>> = (0..lanes).map(|_| None).collect();
    let mut ring: VecDeque<(u64, Vec<u64>)> = VecDeque::new();
    let mut exhausted = false;
    loop {
        // refill free lanes
        let mut changed = false;
        if !exhausted {
            for r in 0..lanes {
                while slots[r].is_none() {
                    let Some(job) = next_job() else {
                        exhausted = true;
                        break;
                    };
                    changed = true;
                    let g = sim.generation();
                    sim.clear_lane(r);
                    sim.set_lane_cells(r, &job.cells);
                    let nat = natural_sim(&job.natural, rule, &job.cells, job.start_gen);
                    let first = sample(&nat, true);
                    let lane = Lane {
                        start: g,
                        peak: (first.pop, job.start_gen),
                        first,
                        seen: HashMap::new(),
                        order: VecDeque::new(),
                        t0: Instant::now(),
                        job,
                    };
                    if lane.first.pop == 0 && !birth0 {
                        let s0 = lane.job.start_gen;
                        finish(lane, Halt { status: Status::Extinct, period: 1, cycle_start: s0, detected: s0 }, vec![], rule, opts, &mut done);
                        sim.clear_lane(r);
                        continue;
                    }
                    slots[r] = Some(lane);
                }
                if exhausted {
                    break;
                }
            }
        }
        if slots.iter().all(|s| s.is_none()) {
            return;
        }
        if changed {
            let hulls: Vec<Option<Hull>> = slots.iter().map(|s| s.as_ref().and_then(|l| l.first.hull())).collect();
            sim.restrict_to_lane_hulls(&hulls);
        }
        // one generation
        sim.step();
        let g = sim.generation();
        let acc = sim.last_step().expect("lane stats");
        for r in 0..lanes {
            let Some(lane) = slots[r].as_mut() else { continue };
            let lg = g - lane.start;
            let abs = lane.job.start_gen + lg;
            let pop = acc.lane_pop[r];
            if pop > lane.peak.0 {
                lane.peak = (pop, abs);
            }
            let halt = if pop == 0 && !birth0 {
                Some((Halt { status: Status::Extinct, period: 1, cycle_start: abs, detected: abs }, vec![]))
            } else if acc.diff & sim.lane_mask(r) == 0 {
                Some((Halt { status: Status::Still, period: 1, cycle_start: abs - 1, detected: abs }, sim.lane_cells(r)))
            } else if lg >= opts.cap {
                Some(closing_check(&sim, r, lane, &ring, rule, opts))
            } else {
                None
            };
            if let Some((h, cells)) = halt {
                let lane = slots[r].take().unwrap();
                if h.status == Status::Running {
                    finish_running(lane, cells, abs, rule, opts, &mut done);
                } else {
                    finish(lane, h, cells, rule, opts, &mut done);
                }
                sim.clear_lane(r);
            }
        }
        // checkpoint
        if g % k == 0 && slots.iter().any(|s| s.is_some()) {
            let hashes = sim.lane_hashes();
            let words = if ring.len() >= opts.ring.max(1) {
                let (_, mut v) = ring.pop_front().unwrap();
                v.clear();
                v.extend_from_slice(&sim_words(&sim));
                v
            } else {
                sim_words(&sim)
            };
            ring.push_back((g, words));
            for r in 0..lanes {
                let Some(lane) = slots[r].as_mut() else { continue };
                let h = hashes[r];
                if let Some(&g0) = lane.seen.get(&h) {
                    if let Some((halt, cells)) = resolve(&sim, r, lane, g0, g, &ring, rule) {
                        let lane = slots[r].take().unwrap();
                        finish(lane, halt, cells, rule, opts, &mut done);
                        sim.clear_lane(r);
                        continue;
                    }
                    lane.seen.remove(&h); // hash collision: forget the old entry
                }
                lane.seen.insert(h, g);
                lane.order.push_back((h, g));
                if lane.order.len() > opts.window.max(1) {
                    let (oh, og) = lane.order.pop_front().unwrap();
                    if lane.seen.get(&oh) == Some(&og) {
                        lane.seen.remove(&oh);
                    }
                }
            }
        }
    }
}

fn sim_words(sim: &BitSim) -> Vec<u64> {
    sim.state_words()
}

fn lane_sim(pack_geo: &Geometry, rule: Rule, cells: &[P3]) -> BitSim {
    let mut s = BitSim::new(pack_geo.clone(), rule).expect("lane box");
    s.set_cells(cells);
    s.stats_mode = crate::fast::StatsMode::None;
    s
}

fn natural_sim(geo: &Geometry, rule: Rule, cells: &[P3], gen: u64) -> BitSim {
    let mut s = BitSim::new(geo.clone(), rule).expect("natural box");
    s.set_cells(cells);
    s.set_generation(gen);
    s
}

/// Smallest `d ≤ max` with state(+d) == state, stepping a copy of `u`.
fn period_of(u: &BitSim, max: u64) -> Option<u64> {
    let mut v = u.clone();
    for d in 1..=max {
        v.step();
        if v.same_state(u) {
            return Some(d);
        }
    }
    None
}

/// Exact cycle start: the smallest lane generation `t ≥ base_lg` with
/// state(t) == state(t + p), by stepping two copies p apart from `base`.
/// Returns (μ in lane generations, state(μ)).
fn cycle_start(base: BitSim, base_lg: u64, p: u64) -> (u64, BitSim) {
    let mut a = base;
    let mut b = a.clone();
    b.steps(p);
    let mut t = base_lg;
    while !a.same_state(&b) {
        a.step();
        b.step();
        t += 1;
    }
    (t, a)
}

/// The latest state known to precede the cycle, as (lane generation, cells): the newest
/// ring snapshot at or before `before` (global gen) not inside the cycle, else the seed.
fn base_state<T>(sim: &BitSim, r: usize, lane: &Lane<T>, ring: &VecDeque<(u64, Vec<u64>)>, before: u64, p: u64, rule: Rule) -> (u64, Vec<P3>) {
    let geo = sim.lane_geometry().unwrap().clone();
    for (gq, words) in ring.iter().rev() {
        if *gq > before || *gq < lane.start {
            continue;
        }
        let cells = sim.lane_cells_in(words, r);
        let u = lane_sim(&geo, rule, &cells);
        let mut v = u.clone();
        v.steps(p);
        if !v.same_state(&u) {
            return (gq - lane.start, cells);
        }
    }
    (0, lane.job.cells.clone())
}

/// A checkpoint hash at global gen `g` repeated the one at `g0`.
fn resolve<T>(sim: &BitSim, r: usize, lane: &Lane<T>, g0: u64, g: u64, ring: &VecDeque<(u64, Vec<u64>)>, rule: Rule) -> Option<(Halt, Vec<P3>)> {
    let geo = sim.lane_geometry().unwrap().clone();
    let u = lane_sim(&geo, rule, &sim.lane_cells(r));
    let p = period_of(&u, g - g0)?;
    // g0 is the first checkpoint inside the cycle, so the cycle starts after g0 - K; the
    // newest snapshot that is not yet periodic is a valid starting point
    let (blg, bcells) = base_state(sim, r, lane, ring, g0, p, rule);
    let (mu, a) = cycle_start(lane_sim(&geo, rule, &bcells), blg, p);
    Some(make_halt(lane, mu, p, a.cells()))
}

fn make_halt<T>(lane: &Lane<T>, mu: u64, p: u64, cells: Vec<P3>) -> (Halt, Vec<P3>) {
    let s0 = lane.job.start_gen;
    let status = if p == 1 { Status::Still } else { Status::Periodic };
    (Halt { status, period: p, cycle_start: s0 + mu, detected: s0 + mu + p }, cells)
}

/// At the cap: did a cycle complete within the cap?
fn closing_check<T>(sim: &BitSim, r: usize, lane: &Lane<T>, ring: &VecDeque<(u64, Vec<u64>)>, rule: Rule, opts: &LaneOpts) -> (Halt, Vec<P3>) {
    let geo = sim.lane_geometry().unwrap().clone();
    let cells = sim.lane_cells(r);
    let lg = sim.generation() - lane.start;
    let running = || (Halt { status: Status::Running, period: 0, cycle_start: 0, detected: 0 }, cells.clone());
    let u = lane_sim(&geo, rule, &cells);
    let Some(p) = period_of(&u, opts.closing.min(lg)) else { return running() };
    let (blg, bcells) = base_state(sim, r, lane, ring, sim.generation(), p, rule);
    let (mu, a) = cycle_start(lane_sim(&geo, rule, &bcells), blg, p);
    if mu + p <= lg {
        make_halt(lane, mu, p, a.cells())
    } else {
        running()
    }
}

fn finish<T>(lane: Lane<T>, h: Halt, cells: Vec<P3>, rule: Rule, opts: &LaneOpts, done: &mut impl FnMut(Done<T>)) {
    let fin_gen = h.detected;
    report(lane, Some(h), cells, fin_gen, rule, opts, done);
}

fn finish_running<T>(lane: Lane<T>, cells: Vec<P3>, gen: u64, rule: Rule, opts: &LaneOpts, done: &mut impl FnMut(Done<T>)) {
    report(lane, None, cells, gen, rule, opts, done);
}

fn report<T>(lane: Lane<T>, h: Option<Halt>, cells: Vec<P3>, fin_gen: u64, rule: Rule, opts: &LaneOpts, done: &mut impl FnMut(Done<T>)) {
    let sim = natural_sim(&lane.job.natural, rule, &cells, fin_gen);
    let fin = sample(&sim, true);
    let mut res = RunResult {
        start_gen: lane.job.start_gen,
        final_gen: fin_gen,
        halt: h,
        seed_pop: lane.first.pop,
        pop: fin.pop,
        pop_axis: fin.pop_axis,
        peak_pop: lane.peak.0,
        peak_gen: lane.peak.1,
        hull_initial: lane.first.hull(),
        hull_final: fin.hull(),
        firewalls_final: fin.firewalls(),
        layer_events: 0,
        theorem_violations: 0,
        hash: sim.state_hash(),
        elapsed: lane.t0.elapsed().as_secs_f64(),
    };
    if opts.need_layers {
        let mut t = LayerTracker::new();
        res.layer_events += t.update(&lane.first).len() as u64;
        if fin_gen != lane.job.start_gen {
            res.layer_events += t.update(&fin).len() as u64;
        }
        res.theorem_violations = t.violations.len() as u64;
    }
    done(Done { tag: lane.job.tag, res, sim });
}
