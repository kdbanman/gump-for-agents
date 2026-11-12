//! Packed lanes: k runs side by side in one word must evolve exactly like k separate runs.
use gump::fast::StatsMode;
use gump::seeds::{self, Region};
use gump::*;

fn check(run_geo: Geometry, rule: Rule, lanes: usize, gens: usize, seed: u64, restrict: bool) {
    let (lo, hi) = run_geo.doubled_bounds();
    let soups: Vec<Vec<P3>> = (0..lanes)
        .map(|r| seeds::soup(&Region::Box { lo, hi }, 0.25 + 0.05 * r as f64, seed + r as u64).into_iter().filter(|&p| run_geo.contains_doubled(p)).collect())
        .collect();
    let mut packed = BitSim::new_packed(&run_geo, rule, lanes).unwrap();
    let mut solo: Vec<BitSim> = soups
        .iter()
        .map(|c| {
            let mut s = BitSim::new(run_geo.clone(), rule).unwrap();
            s.set_cells(c);
            s
        })
        .collect();
    for (r, c) in soups.iter().enumerate() {
        assert_eq!(packed.set_lane_cells(r, c), 0);
        assert_eq!(packed.lane_cells(r), solo[r].cells());
    }
    if restrict {
        let hulls: Vec<Option<Hull>> = soups.iter().map(|c| Hull::of_cells(c)).collect();
        packed.restrict_to_lane_hulls(&hulls);
    }
    for g in 1..=gens {
        packed.step();
        let acc = packed.last_step().unwrap();
        for (r, s) in solo.iter_mut().enumerate() {
            let before = s.cells();
            s.step();
            let c = s.cells();
            assert_eq!(packed.lane_cells(r), c, "{run_geo:?} {rule} lanes {lanes} lane {r} gen {g}");
            assert_eq!(acc.lane_pop[r], c.len() as u64);
            assert_eq!(acc.diff & packed.lane_mask(r) != 0, before != c);
        }
    }
    // lane hashes are per-lane functions of state
    let h = packed.lane_hashes();
    for r in 0..lanes {
        let mut p2 = BitSim::new_packed(&run_geo, rule, lanes).unwrap();
        p2.set_lane_cells(r, &packed.lane_cells(r));
        assert_eq!(p2.lane_hashes()[r], h[r]);
    }
}

#[test]
fn packed_lanes_match_separate_runs() {
    for rule in [Rule::GUMP, Rule::parse("B4/S34").unwrap(), Rule::parse("B35/S236").unwrap()] {
        for boundary in [Boundary::Open, Boundary::Torus] {
            for (n, lanes) in [([5, 4, 3], 4), ([16, 7, 6], 4), ([21, 9, 5], 3), ([30, 5, 6], 2), ([40, 4, 5], 2), ([1, 3, 3], 4)] {
                let geo = Geometry::new(n, [-2, 1, 0], boundary);
                check(geo, rule, lanes, 12, n[0] as u64, false);
            }
        }
    }
    // hull-restricted rows (open, min birth >= 4)
    for (n, lanes) in [([12, 12, 12], 4), ([22, 22, 22], 2)] {
        check(Geometry::new(n, [-6, -6, -6], Boundary::Open), Rule::GUMP, lanes, 30, 9, true);
    }
}

#[test]
fn lane_stats_mode_is_default_for_packed() {
    let s = BitSim::new_packed(&Geometry::new([10, 4, 4], [0; 3], Boundary::Open), Rule::GUMP, 3).unwrap();
    assert_eq!(s.stats_mode, StatsMode::Lanes);
}
