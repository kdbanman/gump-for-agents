//! `describe`: what a small pattern is — its evolution to a still life / oscillator,
//! period, symmetry, layer extents, connected pieces, and (optionally) its id in the
//! atlas catalogue (`research/atlas/catalogue.jsonl`, same canonical form).

use crate::fast::BitSim;
use crate::json::{Obj, Raw, ToJson};
use crate::lattice::{layer, offsets, Geometry, Hull, P3, DIAGS};
use crate::rule::Rule;
use crate::run::{run, RunOpts, Sinks};
use crate::sym;
use std::collections::{HashMap, HashSet};

/// The final orbit of a pattern stepped in open space.
pub struct Orbit {
    pub status: &'static str,
    pub period: Option<u64>,
    pub cycle_start: Option<u64>,
    /// phases of the final cycle starting at `cycle_start` (or the last state if running)
    pub phases: Vec<Vec<P3>>,
}

pub fn open_sim(cells: &[P3], rule: Rule) -> Option<BitSim> {
    let h = Hull::of_cells(cells)?;
    let mut sim = BitSim::new(Geometry::open_for_hull(&h, 1), rule).ok()?;
    sim.set_cells(cells);
    Some(sim)
}

/// Step `cells` in open space until it halts (at most `cap` generations).
pub fn evolve(cells: &[P3], rule: Rule, cap: u64) -> Orbit {
    let Some(mut sim) = open_sim(cells, rule) else {
        return Orbit { status: "extinct", period: Some(1), cycle_start: Some(0), phases: vec![vec![]] };
    };
    let res = run(&mut sim, &RunOpts { max_gens: Some(cap), ..Default::default() }, &mut Sinks::default());
    match res.halt {
        Some(h) => {
            // the simulator now holds state(cycle_start + period) = state(cycle_start)
            let mut phases = Vec::new();
            for _ in 0..h.period {
                phases.push(sim.cells());
                sim.step();
            }
            Orbit { status: h.status.name(), period: Some(h.period), cycle_start: Some(h.cycle_start), phases }
        }
        None => Orbit { status: "running", period: None, cycle_start: None, phases: vec![sim.cells()] },
    }
}

/// Connected components under "neighbours" (`reach = 1`) or "neighbours or sharing a
/// neighbour" (`reach = 2`, the atlas's R-connectivity: pieces farther apart than this
/// cannot interact).
pub fn components(cells: &[P3], reach: usize) -> Vec<Vec<P3>> {
    let set: HashSet<P3> = cells.iter().copied().collect();
    let nbrs = |p: P3| -> Vec<P3> {
        let a = crate::lattice::cell_axis(p).unwrap();
        offsets(a).iter().map(|o| [p[0] + o[0], p[1] + o[1], p[2] + o[2]]).collect()
    };
    let mut seen: HashSet<P3> = HashSet::new();
    let mut out = Vec::new();
    let mut sorted: Vec<P3> = cells.to_vec();
    sorted.sort();
    for &p0 in &sorted {
        if seen.contains(&p0) {
            continue;
        }
        let mut comp = vec![];
        let mut stack = vec![p0];
        seen.insert(p0);
        while let Some(p) = stack.pop() {
            comp.push(p);
            let mut cand: Vec<P3> = nbrs(p);
            if reach >= 2 {
                let more: Vec<P3> = cand.iter().flat_map(|&q| nbrs(q)).collect();
                cand.extend(more);
            }
            for q in cand {
                if set.contains(&q) && seen.insert(q) {
                    stack.push(q);
                }
            }
        }
        comp.sort();
        out.push(comp);
    }
    out
}

/// Atlas catalogue: canonical cells → id.
pub fn load_catalogue(path: &str) -> Result<HashMap<Vec<P3>, String>, String> {
    let text = std::fs::read_to_string(path).map_err(|e| format!("{path}: {e}"))?;
    let mut m = HashMap::new();
    for line in text.lines() {
        let id = line.split("\"id\":\"").nth(1).and_then(|r| r.split('"').next());
        let cells = line.split("\"cells\":").nth(1);
        let (Some(id), Some(cells)) = (id, cells) else { continue };
        let end = cells.find("]]").map(|e| e + 2).unwrap_or(cells.len());
        let nums: Vec<i64> = cells[..end]
            .split(|c: char| !(c.is_ascii_digit() || c == '-'))
            .filter(|t| !t.is_empty())
            .filter_map(|t| t.parse().ok())
            .collect();
        let v: Vec<P3> = nums.chunks(3).filter(|c| c.len() == 3).map(|c| [c[0], c[1], c[2]]).collect();
        m.insert(sym::normalise(&v), id.to_string());
    }
    Ok(m)
}

fn layers_json(cells: &[P3]) -> String {
    let v: Vec<Raw> = (0..4)
        .map(|d| {
            let s: Vec<i64> = cells.iter().map(|&p| layer(p, d)).collect();
            let (lo, hi) = (s.iter().min().copied(), s.iter().max().copied());
            Raw(Obj::new()
                .f("dir", &DIAGS[d])
                .f("lo", &lo)
                .f("hi", &hi)
                .f("n", &lo.zip(hi).map(|(a, b)| (b - a) / 2 + 1))
                .end())
        })
        .collect();
    v.json()
}

/// Static facts about one orbit (phase list), as JSON fields.
fn orbit_fields(mut o: Obj, phases: &[Vec<P3>], cat: Option<&HashMap<Vec<P3>, String>>) -> Obj {
    let union: Vec<P3> = {
        let mut s: HashSet<P3> = HashSet::new();
        for ph in phases {
            s.extend(ph.iter().copied());
        }
        let mut v: Vec<P3> = s.into_iter().collect();
        v.sort();
        v
    };
    let (canon, k) = sym::canonical_orbit(phases);
    let id = cat.and_then(|c| c.get(&canon).cloned());
    o = o
        .f("pops", &phases.iter().map(|p| p.len()).collect::<Vec<_>>())
        .f("union", &union.len())
        .f("sym", &sym::stabiliser_order(&phases[k]))
        .f("spacetime_sym", &sym::spacetime_order(phases))
        .f("layers", &Raw(layers_json(&union)))
        .f("nbr_components", &components(&union, 1).len());
    if cat.is_some() {
        o = o.f("catalogue_id", &id);
    }
    o.f("canonical", &canon)
}

/// Full description as one JSON line. `as_is`: describe `cells` without evolving.
pub fn describe(cells: &[P3], rule: Rule, cap: u64, as_is: bool, cat: Option<&HashMap<Vec<P3>, String>>) -> String {
    let mut o = Obj::new().f("type", "describe").f("rule", &rule.to_string()).f("cells", &cells.len());
    let s0: Vec<P3> = {
        let mut v = cells.to_vec();
        v.sort();
        v
    };
    o = o.f("input_sym", &sym::stabiliser_order(&s0)).f("input_layers", &Raw(layers_json(&s0)));
    let orbit = if as_is {
        // still evolve, but only to learn whether the input itself is periodic
        let e = evolve(cells, rule, cap);
        let is_cycle = e.cycle_start == Some(0);
        let ph = if is_cycle { e.phases } else { vec![s0.clone()] };
        Orbit { status: if is_cycle { e.status } else { "not_periodic" }, period: if is_cycle { e.period } else { None }, cycle_start: if is_cycle { Some(0) } else { None }, phases: ph }
    } else {
        evolve(cells, rule, cap)
    };
    o = o.f("status", orbit.status).f("period", &orbit.period).f("cycle_start", &orbit.cycle_start);
    o = orbit_fields(o, &orbit.phases, cat);
    // pieces: R-connected components of the orbit's union, each described as an orbit
    let union: Vec<P3> = {
        let mut s: HashSet<P3> = HashSet::new();
        for ph in &orbit.phases {
            s.extend(ph.iter().copied());
        }
        s.into_iter().collect()
    };
    let pieces = components(&union, 2);
    if pieces.len() > 1 {
        let mut pj = Vec::new();
        for piece in &pieces {
            let ps: HashSet<P3> = piece.iter().copied().collect();
            let phases: Vec<Vec<P3>> = orbit.phases.iter().map(|ph| ph.iter().copied().filter(|p| ps.contains(p)).collect()).collect();
            // independent iff the piece alone reproduces its phases
            let independent = {
                let mut ok = true;
                if let Some(mut sim) = open_sim(&phases[0], rule) {
                    for k in 1..=phases.len() {
                        sim.step();
                        if sim.cells() != phases[k % phases.len()] {
                            ok = false;
                            break;
                        }
                    }
                }
                ok
            };
            // minimal period of the piece itself
            let n = phases.len();
            let pp = (1..=n).find(|&q| n % q == 0 && (0..n).all(|i| phases[i] == phases[(i + q) % n])).unwrap_or(n);
            let po = orbit_fields(Obj::new().f("period", &pp).f("independent", &independent), &phases[..pp], cat);
            pj.push(Raw(po.end()));
        }
        o = o.f("pieces", &pj);
    }
    o.end()
}
