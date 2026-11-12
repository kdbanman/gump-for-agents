//! Property tests: theorems T2/T3, auto-box exactness, snapshots, halting detection.
use gump::instruments::{sample, LayerTracker, Status};
use gump::run::{run, RunOpts, Sinks};
use gump::seeds::{self, Region};
use gump::snapshot::Snapshot;
use gump::*;
use std::collections::HashMap;

fn open_sim(cells: &[P3], margin: usize, rule: Rule) -> BitSim {
    let geo = Geometry::open_for_hull(&Hull::of_cells(cells).unwrap(), margin);
    let mut s = BitSim::new(geo, rule).unwrap();
    assert_eq!(s.set_cells(cells), 0);
    s
}

#[test]
fn t2_hull_never_grows_and_autobox_is_exact() {
    for (i, region) in [
        Region::Oct { center: [0, 0, 0], r: 14 },
        Region::cbox([1, 0, 3], [9, 6, 11]),
        Region::Slab { axis: 2, s0: -3, m: 4, lo: [-12; 3], hi: [12; 3], modulus: None },
    ]
    .iter()
    .enumerate()
    {
        for rule in [Rule::GUMP, Rule::parse("B4567/S2345").unwrap()] {
            let cells = seeds::soup(region, 0.35, 10 + i as u64);
            let mut a = open_sim(&cells, 1, rule);
            assert!(a.restrict_to_hull(Hull::of_cells(&cells).as_ref()));
            let mut b = open_sim(&cells, 6, rule); // much bigger box, no restriction
            let mut hull = Hull::of_cells(&cells).unwrap();
            let mut tracker = LayerTracker::new();
            tracker.update(&sample(&a, true));
            for _ in 0..150 {
                a.step();
                b.step();
                let ca = a.cells();
                assert_eq!(ca, b.cells(), "auto box differs from a padded box");
                if ca.is_empty() {
                    break;
                }
                let h = Hull::of_cells(&ca).unwrap();
                for d in 0..4 {
                    assert!(h.0[d].0 >= hull.0[d].0 && h.0[d].1 <= hull.0[d].1, "hull grew");
                }
                hull = h;
                a.restrict_to_hull(Some(&hull));
                tracker.update(&sample(&a, true));
            }
            assert!(tracker.violations.is_empty(), "proven-dead layer came back: {:?}", tracker.violations);
        }
    }
}

#[test]
fn t3_three_dead_layers_stay_dead() {
    // soups on a 12³ torus (layers mod 24) with a 3-layer gap along each diagonal
    for d in 0..4 {
        for seed in 0..3u64 {
            let geo = Geometry::new([12, 12, 12], [0, 0, 0], Boundary::Torus);
            let all = seeds::soup(&Region::Box { lo: [0; 3], hi: [23; 3] }, 0.35, seed * 7 + d as u64);
            let gap = |p: &P3| {
                let s = gump::lattice::layer(*p, d).rem_euclid(24);
                (5..=9).contains(&s)
            };
            let cells: Vec<P3> = all.into_iter().filter(|p| !gap(p)).collect();
            let mut sim = BitSim::new(geo, Rule::GUMP).unwrap();
            sim.set_cells(&cells);
            let mut tracker = LayerTracker::new();
            tracker.update(&sample(&sim, true));
            for _ in 0..200 {
                sim.step();
                assert!(sim.cells().iter().all(|p| !gap(p)), "firewall breached");
                tracker.update(&sample(&sim, true));
            }
            assert!(tracker.violations.is_empty());
            let l = &sample(&sim, true).layers.unwrap()[d];
            assert!(l.counts[2] == 0 && l.counts[3] == 0 && l.counts[4] == 0);
        }
    }
}

#[test]
fn snapshot_roundtrip() {
    for boundary in [Boundary::Open, Boundary::Torus] {
        let geo = Geometry::new([70, 9, 13], [-3, 4, -20], boundary);
        let cells: Vec<P3> = seeds::soup(&Region::cbox([0, 15, -14], [60, 8, 12]), 0.2, 5)
            .into_iter()
            .filter(|&p| geo.contains_doubled(p))
            .collect();
        let mut sim = BitSim::new(geo.clone(), Rule::parse("B4/S345").unwrap()).unwrap();
        sim.set_cells(&cells);
        sim.steps(3);
        let enc = Snapshot::from_sim(&sim).encode();
        let dec = Snapshot::decode(&enc).unwrap();
        assert_eq!(dec.geo, geo);
        assert_eq!(dec.gen, 3);
        assert_eq!(dec.rule, sim.rule());
        assert_eq!(dec.cells(), sim.cells());
        let mut back = BitSim::new(dec.geo.clone(), dec.rule).unwrap();
        back.set_cells(&dec.cells());
        assert_eq!(back.state_hash(), sim.state_hash());
        assert!(back.same_state(&sim));
    }
}

/// Brute-force (period, cycle_start) by remembering every state.
fn brute_cycle(mut sim: BitSim, max: u64) -> Option<(u64, u64)> {
    let mut seen: HashMap<Vec<P3>, u64> = HashMap::new();
    seen.insert(sim.cells(), 0);
    for g in 1..=max {
        sim.step();
        let c = sim.cells();
        if let Some(&g0) = seen.get(&c) {
            return Some((g - g0, g0));
        }
        seen.insert(c, g);
    }
    None
}

#[test]
fn halting_matches_brute_force() {
    let mut periodic = 0;
    for n in [3usize, 4, 5] {
        for seed in 0..12u64 {
            let geo = Geometry::new([n; 3], [0; 3], Boundary::Torus);
            let cells = seeds::soup(&Region::Box { lo: [0; 3], hi: [2 * n as i64 - 1; 3] }, 0.3, seed);
            let mut sim = BitSim::new(geo, Rule::GUMP).unwrap();
            sim.set_cells(&cells);
            let want = brute_cycle(sim.clone(), 3000);
            let res = run(&mut sim, &RunOpts { max_gens: Some(3000), ..Default::default() }, &mut Sinks::default());
            match (want, res.halt) {
                (None, None) => {}
                (Some((p, mu)), Some(h)) => {
                    assert_eq!((h.period, h.cycle_start), (p, mu), "torus {n} seed {seed}");
                    if p > 1 {
                        periodic += 1;
                        assert_eq!(h.status, Status::Periodic);
                    }
                }
                (w, h) => panic!("torus {n} seed {seed}: brute {:?} vs detector {:?}", w, h),
            }
        }
    }
    eprintln!("periodic cases: {periodic}");
}

#[test]
fn still_life_and_extinction() {
    let mut s = open_sim(&seeds::closed_cube(1), 1, Rule::GUMP);
    let r = run(&mut s, &RunOpts::default(), &mut Sinks::default());
    assert_eq!(r.halt.unwrap().status, Status::Still);
    assert_eq!(r.halt.unwrap().cycle_start, 0);
    let mut s = open_sim(&[[1, 0, 0], [0, 1, 0]], 1, Rule::GUMP);
    let r = run(&mut s, &RunOpts::default(), &mut Sinks::default());
    assert_eq!(r.halt.unwrap().status, Status::Extinct);
    assert_eq!(r.halt.unwrap().cycle_start, 1);
}

#[test]
fn still_life_on_torus_is_still() {
    // a unit cube on a small torus: the halo holds copies of live cells, which must not
    // count as "changed"
    for n in [1usize, 2, 3, 5] {
        let geo = Geometry::new([n, n + 1, n + 2], [0, 0, 0], Boundary::Torus);
        let mut s = BitSim::new(geo, Rule::GUMP).unwrap();
        s.set_cells(&seeds::closed_cube(1));
        s.step();
        let changed = s.cells() != BitSim::new(s.geometry().clone(), Rule::GUMP).map(|mut t| { t.set_cells(&seeds::closed_cube(1)); t.cells() }).unwrap();
        let acc = s.last_step().unwrap();
        assert_eq!(acc.diff != 0, changed, "torus {n}");
        if !changed {
            let mut s2 = BitSim::new(s.geometry().clone(), Rule::GUMP).unwrap();
            s2.set_cells(&seeds::closed_cube(1));
            let r = run(&mut s2, &RunOpts::default(), &mut Sinks::default());
            assert_eq!(r.halt.unwrap().status, Status::Still);
        }
    }
}

#[test]
fn symmetric_soups_density_and_invariance() {
    use gump::sym;
    for (name, _) in sym::GROUPS {
        let group = sym::group(name).unwrap();
        for center in [[0i64, 0, 0], [1, 1, 1]] {
            for torus in [true, false] {
                let p = 0.35;
                let (cells, all, geo) = if torus {
                    let geo = Geometry::new([10, 10, 10], [0, 0, 0], Boundary::Torus);
                    let (lo, hi) = geo.doubled_bounds();
                    let reg = Region::Box { lo, hi };
                    (seeds::soup_sym(&reg, p, 7, &group, center, Some(&geo)), geo.cells(), Some(geo))
                } else {
                    let reg = Region::Oct { center, r: 17 };
                    (seeds::soup_sym(&reg, p, 7, &group, center, None), seeds::soup(&reg, 1.0, 0).len(), None)
                };
                // sampling error: orbits of size <= |G| are the independent units
                let n_orbits = (all as f64 / group.len() as f64).max(1.0);
                let frac = cells.len() as f64 / all as f64;
                let sigma = (p * (1.0 - p) / n_orbits).sqrt();
                assert!((frac - p).abs() < 5.0 * sigma + 0.01, "{name} c={center:?} torus={torus}: density {frac}");
                // exact invariance
                let set: std::collections::HashSet<P3> = cells.iter().copied().collect();
                for g in &group {
                    for &q in &cells {
                        let mut img = g.apply_about(q, center);
                        if let Some(geo) = &geo {
                            let (a, c) = geo.locate(img).unwrap();
                            img = geo.to_doubled(a, c);
                        }
                        assert!(set.contains(&img), "{name} c={center:?} torus={torus}: not invariant");
                    }
                }
            }
        }
    }
}

#[test]
fn occupancy_counts() {
    // period-14 oscillator from a soup: counts over one period sum to the sum of phase pops
    let cells = seeds::soup(&Region::Oct { center: [0, 0, 0], r: 8 }, 0.3, 20);
    let mut sim = open_sim(&cells, 1, Rule::GUMP);
    sim.steps(48);
    let mut pops = 0;
    let mut probe = sim.clone();
    for _ in 0..14 {
        pops += probe.population();
        probe.step();
    }
    let occ = gump::occupancy::Occupancy::accumulate(&mut sim, 14);
    assert_eq!(occ.counts.iter().map(|&c| c as u64).sum::<u64>(), pops);
    assert!(occ.nonzero().iter().all(|&(_, c)| c <= 14));
    // npy header is 64-byte aligned
    let b = occ.npy();
    let hl = u16::from_le_bytes([b[8], b[9]]) as usize;
    assert_eq!((10 + hl) % 64, 0);
    assert_eq!(b.len(), 10 + hl + 4 * occ.counts.len());
}
