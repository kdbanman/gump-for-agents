use gump::*;
use std::time::Instant;
fn main() {
    let args: Vec<String> = std::env::args().collect();
    let n: usize = args[1].parse().unwrap();
    let threads: usize = args[2].parse().unwrap();
    let stats: bool = args[3] == "1";
    let gens: u64 = args[4].parse().unwrap();
    let geo = Geometry::new([n, n, n], [0, 0, 0], Boundary::Torus);
    let mut f = BitSim::new(geo.clone(), Rule::GUMP).unwrap();
    f.set_threads(threads);
    f.stats_mode = if stats { gump::fast::StatsMode::Full } else { gump::fast::StatsMode::None };
    let mut s = 12345u64;
    for a in 0..3 { for k in 0..n { for j in 0..n { for i in 0..n {
        s ^= s << 13; s ^= s >> 7; s ^= s << 17;
        if s % 10 < 3 { f.set(geo.to_doubled(a, [i, j, k]), true); }
    }}}}
    f.steps(3);
    let t = Instant::now();
    f.steps(gens);
    let dt = t.elapsed().as_secs_f64();
    let cu = geo.cells() as f64 * gens as f64 / dt;
    println!("n={n} threads={threads} stats={stats}: {:.1} gen/s, {:.3e} cell-updates/s, pop {}", gens as f64 / dt, cu, f.population());
}
