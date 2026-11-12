use gump::*;

fn rng(seed: &mut u64) -> u64 {
    *seed = seed.wrapping_add(0x9E3779B97F4A7C15);
    let mut z = *seed;
    z = (z ^ (z >> 30)).wrapping_mul(0xBF58476D1CE4E5B9);
    z = (z ^ (z >> 27)).wrapping_mul(0x94D049BB133111EB);
    z ^ (z >> 31)
}

fn random_cells(geo: &Geometry, density: f64, seed: u64) -> Vec<P3> {
    let mut s = seed;
    let mut v = Vec::new();
    for a in 0..3 {
        for k in 0..geo.n[2] {
            for j in 0..geo.n[1] {
                for i in 0..geo.n[0] {
                    if (rng(&mut s) as f64 / u64::MAX as f64) < density {
                        v.push(geo.to_doubled(a, [i, j, k]));
                    }
                }
            }
        }
    }
    v
}

fn check(geo: Geometry, rule: Rule, density: f64, gens: usize, seed: u64, threads: usize) {
    let cells = random_cells(&geo, density, seed);
    let mut s = ScalarSim::new(geo.clone(), rule);
    let mut f = BitSim::new(geo.clone(), rule).unwrap();
    f.set_threads(threads);
    for &p in &cells {
        assert!(s.set(p, true));
    }
    assert_eq!(f.set_cells(&cells), 0);
    assert_eq!(f.cells(), s.cells());
    for g in 1..=gens {
        s.step();
        f.steps(1);
        let (fc, sc) = (f.cells(), s.cells());
        assert!(fc == sc, "mismatch {:?} {} gen {} (fast {} cells, scalar {})", geo, rule, g, fc.len(), sc.len());
        let acc = f.last_step().unwrap();
        assert_eq!(acc.pop.iter().sum::<u64>(), sc.len() as u64);
        assert_eq!(acc.hash, f.state_hash());
    }
}

#[test]
fn torus_shapes() {
    let dims = [[1, 1, 1], [2, 3, 4], [5, 4, 3], [7, 2, 9], [64, 3, 3], [65, 2, 3], [128, 2, 2], [96, 3, 2], [130, 2, 3], [67, 2, 2], [12, 12, 12]];
    for (t, &n) in dims.iter().enumerate() {
        for rule in [Rule::GUMP, Rule::parse("B4/S34").unwrap(), Rule::parse("B3,5,12/S0,2,4,11").unwrap()] {
            check(Geometry::new(n, [-3, 1, 2], Boundary::Torus), rule, 0.35, 12, t as u64 * 77 + 1, 1);
        }
    }
}

#[test]
fn open_shapes() {
    let dims = [[1, 1, 1], [3, 4, 5], [10, 7, 6], [64, 3, 3], [63, 3, 4], [100, 3, 2], [129, 2, 2], [140, 2, 2], [12, 12, 12]];
    for (t, &n) in dims.iter().enumerate() {
        for rule in [Rule::GUMP, Rule::parse("B456/S2345").unwrap(), Rule::parse("B2/S").unwrap()] {
            check(Geometry::new(n, [5, -7, 0], Boundary::Open), rule, 0.4, 12, t as u64 * 31 + 5, 1);
        }
    }
}

#[test]
fn threaded_matches() {
    check(Geometry::new([128, 9, 17], [0, 0, 0], Boundary::Torus), Rule::GUMP, 0.3, 8, 3, 4);
    check(Geometry::new([40, 11, 13], [0, 0, 0], Boundary::Open), Rule::GUMP, 0.3, 8, 4, 3);
    check(Geometry::new([20, 6, 5], [1, 2, 3], Boundary::Torus), Rule::parse("B4/S34").unwrap(), 0.3, 8, 5, 4);
}

#[test]
fn run_steps_threaded_long() {
    // a persistent team over many generations agrees with single-threaded stepping
    let geo = Geometry::new([64, 24, 24], [0, 0, 0], Boundary::Torus);
    let cells = random_cells(&geo, 0.3, 99);
    let mut a = BitSim::new(geo.clone(), Rule::GUMP).unwrap();
    let mut b = BitSim::new(geo.clone(), Rule::GUMP).unwrap();
    a.set_cells(&cells);
    b.set_cells(&cells);
    b.set_threads(4);
    let mut hashes = Vec::new();
    b.run_steps(50, |s| {
        hashes.push(s.last_step().unwrap().hash);
        true
    });
    for h in hashes {
        a.step();
        assert_eq!(a.last_step().unwrap().hash, h);
    }
    assert!(a.same_state(&b));
}
