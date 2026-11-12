// Orbit size histogram of point groups acting on an N^3 torus (cross-check with research/phase/sym.py).
fn main() {
    let n: usize = std::env::args().nth(1).unwrap().parse().unwrap();
    for name in ["oh", "th", "td", "d2h"] {
        let g = gump::sym::group(name).unwrap();
        let geo = gump::Geometry::new([n; 3], [0; 3], gump::Boundary::Torus);
        let (lo, hi) = geo.doubled_bounds();
        // density 1 soup lists every cell once; count orbits via the draw structure
        let mut seen = std::collections::HashSet::new();
        let mut hist = std::collections::BTreeMap::new();
        for p in gump::seeds::fill_span(lo, hi) {
            if seen.contains(&p) { continue; }
            let orb: std::collections::BTreeSet<_> = g.iter().map(|e| { let q = e.apply(p); let (a, c) = geo.locate(q).unwrap(); geo.to_doubled(a, c) }).collect();
            *hist.entry(orb.len()).or_insert(0) += 1;
            seen.extend(orb);
        }
        println!("{name} {} {:?}", hist.values().sum::<i32>(), hist);
    }
}
