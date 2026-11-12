//! `gump` command-line interface. Run `gump help` for usage.

use gump::fast::BitSim;
use gump::json::{Obj, Raw, ToJson};
use gump::lattice::{Boundary, Geometry, Hull, P3};
use gump::rule::Rule;
use gump::run::{hull_json, run, Format, RunOpts, RunResult, Sinks};
use gump::seeds::{self, Region};
use gump::snapshot::Snapshot;
use std::collections::BTreeMap;
use std::io::{BufWriter, Write};
use std::process::exit;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Mutex;
use std::time::Instant;

const HELP: &str = r#"gump — fast engine for the gump automaton (faces of the cubic honeycomb, B45/S345)

USAGE
  gump run      [SEED] [SPACE] [RUN OPTIONS] [OUTPUTS]   one run; last stdout line = JSON summary
  gump ensemble [SEED] [SPACE] [RUN OPTIONS] --runs N [--vary KEY=V1,V2,..]  one JSON line per run
  gump info     [SEED] [SPACE]                           seed/box/hull as JSON, no stepping
  gump convert  [SEED] [SPACE] [--snapshot-out F] [--cells-out F]   e.g. snapshot <-> cell list
  gump bench    [--quick]                                performance suite (JSON lines)

SEED (exactly one; coordinates are doubled: a cell has exactly one odd coordinate)
  --cube N                 closed cube of side N cubes, all internal faces live (3N²(N+1) cells)
  --legacy-cube H          the original's closed-cube seed for habitat size H (frame 0..H)
  --legacy-key K [--legacy-h H]   the original's number-key seed (K in 1..9, H default 50)
  --soup P                 random soup, density P, in a region:
      --region oct|box|slab|all   (default: oct if --radius, box if --half, all on a torus)
      --radius R           octahedron sum|p-c| <= R
      --half H | HX,HY,HZ  box |p_t-c_t| <= H_t (also bounds a slab in open space)
      --slab-layers M      slab: M consecutive {111} layers along --diag (default 0 = [111])
      --diag D             diagonal axis 0..3 = [111],[-111],[1-11],[11-1]
      --center X,Y,Z       region centre (default 0,0,0)
      --rng SEED           RNG seed (default 1)
  --cells FILE             cell list: lines "x y z" (doubled coords), '#' comments
  --snapshot FILE          a .gump snapshot (its box/boundary/rule/gen are used unless overridden)

SPACE
  (default) open space: box auto-sized to the seed's diagonal hull (+ --margin M, default 1);
            exact for infinite space by theorem T2
  --torus N | NX,NY,NZ     torus of N³ cubes (doubled period 2N); --origin OX,OY,OZ (cubes)
  --box NX,NY,NZ --origin OX,OY,OZ   explicit open box (dead outside)
  --rule B45/S345          birth/survival sets over counts 0..12 (B4,10/S3,11 style for >9)

RUN OPTIONS
  --gens N                 at most N generations (default: until halt, cap 10^9)
  --no-halt                keep going after extinction/still life/cycle (needs --gens)
  --every K                sample every K generations (time series)
  --layers                 include per-layer populations (4 diagonals) in samples
  --lite                   samples without layer analysis (no hull/firewalls; faster on huge tori)
  --threads T              threads per generation (default: auto, by box size)
  --hash-window N          generations remembered for cycle detection (default 1048576)

OUTPUTS
  --out FILE               time series (default stdout); --format jsonl|csv
  --kymo FILE              kymograph CSV: one row per (sample, axis): gen,axis,count per layer
  --events FILE            JSONL: each layer's irreversible death (hull: T2, firewall: T3)
  --poplog FILE            "generation population" every generation (legacy log format)
  --trace FILE             every generation: "gen x,y,z x,y,z ..." (small patterns only)
  --snapshot-out FILE      final state as a .gump snapshot
  --cells-out FILE         final state as a cell list

ENSEMBLE
  --runs N                 runs per parameter combination (RNG seeds rng, rng+1, ...)
  --vary KEY=V1,V2,...     sweep: density, radius, half, rule, slab-layers (repeatable)
  --threads T              parallel runs (default: all cores)
  --gens N                 cap per run (default 10^6)
"#;

struct Args {
    cmd: String,
    kv: BTreeMap<String, Vec<String>>,
    flags: Vec<String>,
    used: Mutex<std::collections::BTreeSet<String>>,
}

const BOOL_FLAGS: &[&str] = &["no-halt", "layers", "quick", "lite"];

impl Args {
    fn parse() -> Args {
        let mut it = std::env::args().skip(1);
        let cmd = it.next().unwrap_or_else(|| "help".into());
        let mut kv: BTreeMap<String, Vec<String>> = BTreeMap::new();
        let mut flags = Vec::new();
        let rest: Vec<String> = it.collect();
        let mut i = 0;
        while i < rest.len() {
            let a = &rest[i];
            let Some(k) = a.strip_prefix("--") else { die(&format!("unexpected argument '{a}'")) };
            if let Some((k, v)) = k.split_once('=') {
                kv.entry(k.to_string()).or_default().push(v.to_string());
                i += 1;
            } else if BOOL_FLAGS.contains(&k) {
                flags.push(k.to_string());
                i += 1;
            } else {
                let v = rest.get(i + 1).unwrap_or_else(|| die(&format!("--{k} needs a value")));
                kv.entry(k.to_string()).or_default().push(v.clone());
                i += 2;
            }
        }
        Args { cmd, kv, flags, used: Default::default() }
    }
    fn get(&self, k: &str) -> Option<String> {
        self.used.lock().unwrap().insert(k.to_string());
        self.kv.get(k).and_then(|v| v.last().cloned())
    }
    fn all(&self, k: &str) -> Vec<String> {
        self.used.lock().unwrap().insert(k.to_string());
        self.kv.get(k).cloned().unwrap_or_default()
    }
    fn flag(&self, k: &str) -> bool {
        self.flags.iter().any(|f| f == k)
    }
    fn num<T: std::str::FromStr>(&self, k: &str) -> Option<T> {
        self.get(k).map(|v| v.parse::<T>().unwrap_or_else(|_| die(&format!("--{k}: cannot parse '{v}'"))))
    }
    fn check_unused(&self) {
        let used = self.used.lock().unwrap();
        for k in self.kv.keys() {
            if !used.contains(k) {
                die(&format!("unknown or unused option --{k} (see gump help)"));
            }
        }
    }
}

/// Print one line to stdout; exit quietly if the reader went away (e.g. `| head`).
fn out(line: &str) {
    let mut so = std::io::stdout().lock();
    if writeln!(so, "{line}").and_then(|_| so.flush()).is_err() {
        exit(0);
    }
}

fn die(msg: &str) -> ! {
    eprintln!("gump: {msg}");
    exit(2)
}

fn triple(s: &str) -> [i64; 3] {
    let v: Vec<i64> = s.split(',').map(|t| t.trim().parse().unwrap_or_else(|_| die(&format!("bad number in '{s}'")))).collect();
    match v.len() {
        1 => [v[0]; 3],
        3 => [v[0], v[1], v[2]],
        _ => die(&format!("expected N or X,Y,Z, got '{s}'")),
    }
}

fn writer(path: &str) -> Box<dyn Write> {
    if path == "-" {
        Box::new(BufWriter::new(std::io::stdout()))
    } else {
        Box::new(BufWriter::new(std::fs::File::create(path).unwrap_or_else(|e| die(&format!("{path}: {e}")))))
    }
}

/// Seed parameters that an ensemble may vary.
#[derive(Clone, Debug)]
struct SeedParams {
    density: f64,
    radius: Option<i64>,
    half: Option<[i64; 3]>,
    slab_layers: Option<i64>,
    rng: u64,
    rule: Rule,
}

/// A built seed: cells + description + optional preset geometry/gen (from snapshots).
struct Seed {
    cells: Vec<P3>,
    desc: String,
    geo: Option<Geometry>,
    gen: u64,
    rule: Option<Rule>,
}

fn build_space(a: &Args, cells: &[P3], preset: Option<&Geometry>) -> Geometry {
    if let Some(t) = a.get("torus") {
        let n = triple(&t);
        if n.iter().any(|&v| v < 1) {
            die("torus dims must be >= 1");
        }
        let origin = match a.get("origin") {
            Some(o) => triple(&o),
            None => {
                // centre the fundamental domain on the seed's bounding box (presentation only)
                let mut o = [0i64; 3];
                if !cells.is_empty() {
                    for t in 0..3 {
                        let lo = cells.iter().map(|p| p[t]).min().unwrap();
                        let hi = cells.iter().map(|p| p[t]).max().unwrap();
                        o[t] = ((lo + hi) / 2).div_euclid(2) - n[t] / 2;
                    }
                }
                o
            }
        };
        return Geometry::new([n[0] as usize, n[1] as usize, n[2] as usize], origin, Boundary::Torus);
    }
    if let Some(b) = a.get("box") {
        let n = triple(&b);
        let origin = a.get("origin").map(|o| triple(&o)).unwrap_or_else(|| die("--box needs --origin"));
        let (w, bb) = gump::fast::pack_open(n[0] as usize);
        let nx = w * bb;
        return Geometry::new([nx, n[1] as usize, n[2] as usize], origin, Boundary::Open);
    }
    if let Some(g) = preset {
        if a.get("margin").is_none() {
            return g.clone();
        }
    }
    let margin: usize = a.num("margin").unwrap_or(1);
    match Hull::of_cells(cells) {
        Some(h) => Geometry::open_for_hull(&h, margin),
        None => Geometry::new([1, 1, 1], [0, 0, 0], Boundary::Open),
    }
}

fn soup_region(a: &Args, sp: &SeedParams, torus: Option<&Geometry>) -> Region {
    let center = a.get("center").map(|c| triple(&c)).unwrap_or([0, 0, 0]);
    let region = a.get("region").unwrap_or_else(|| {
        if sp.slab_layers.is_some() {
            "slab".into()
        } else if sp.radius.is_some() {
            "oct".into()
        } else if sp.half.is_some() {
            "box".into()
        } else if torus.is_some() {
            "all".into()
        } else {
            die("--soup needs a region: --radius R (octahedron), --half H (box), or a --torus")
        }
    });
    let whole = |g: &Geometry| -> (P3, P3) { g.doubled_bounds() };
    match region.as_str() {
        "oct" => Region::Oct { center, r: sp.radius.unwrap_or_else(|| die("--region oct needs --radius")) },
        "box" => Region::cbox(center, sp.half.unwrap_or_else(|| die("--region box needs --half"))),
        "all" => {
            let (lo, hi) = whole(torus.unwrap_or_else(|| die("--region all needs a --torus")));
            Region::Box { lo, hi }
        }
        "slab" => {
            let m = sp.slab_layers.unwrap_or_else(|| die("--region slab needs --slab-layers M"));
            let axis: usize = a.num("diag").unwrap_or(0);
            if axis > 3 {
                die("--diag must be 0..3");
            }
            let (lo, hi) = match (sp.half, torus) {
                (Some(h), _) => Region::span(center, h),
                (None, Some(g)) => whole(g),
                (None, None) => die("a slab in open space needs --half to bound it"),
            };
            let cs = gump::lattice::layer(center, axis);
            Region::Slab { axis, s0: Region::slab_s0(m, cs), m, lo, hi, modulus: torus.and_then(|g| g.layer_modulus()) }
        }
        r => die(&format!("unknown region '{r}'")),
    }
}

fn seed_params(a: &Args) -> SeedParams {
    SeedParams {
        density: a.num("soup").unwrap_or(0.0),
        radius: a.num("radius"),
        half: a.get("half").map(|h| triple(&h)),
        slab_layers: a.num("slab-layers"),
        rng: a.num("rng").unwrap_or(1),
        rule: a.get("rule").map(|r| Rule::parse(&r).unwrap_or_else(|e| die(&e))).unwrap_or(Rule::GUMP),
    }
}

fn build_seed(a: &Args, sp: &SeedParams) -> Seed {
    let mut n = 0;
    for k in ["cube", "legacy-cube", "legacy-key", "soup", "cells", "snapshot"] {
        if a.kv.contains_key(k) {
            n += 1;
        }
    }
    if n != 1 {
        die("give exactly one seed: --cube, --legacy-cube, --legacy-key, --soup, --cells or --snapshot");
    }
    let plain = |cells: Vec<P3>, desc: String| Seed { cells, desc, geo: None, gen: 0, rule: None };
    if let Some(nn) = a.num::<i64>("cube") {
        if nn < 1 {
            die("--cube must be >= 1");
        }
        return plain(seeds::closed_cube(nn), format!("cube n={nn}"));
    }
    if let Some(h) = a.num::<i64>("legacy-cube") {
        let (lo, hi) = seeds::legacy_cube_span(h);
        return plain(seeds::legacy_cube(h), format!("legacy-cube H={h} span={lo}..{hi}"));
    }
    if let Some(k) = a.num::<i64>("legacy-key") {
        let h: i64 = a.num("legacy-h").unwrap_or(50);
        return plain(seeds::legacy_key(h, k), format!("legacy-key K={k} H={h}"));
    }
    if a.kv.contains_key("soup") {
        // a torus region needs the torus geometry, which needs no cells
        let torus = a.kv.get("torus").map(|_| build_space(a, &[], None));
        let region = soup_region(a, sp, torus.as_ref());
        let cells = seeds::soup(&region, sp.density, sp.rng);
        return plain(cells, format!("soup p={} rng={} {}", sp.density, sp.rng, region.describe()));
    }
    if let Some(f) = a.get("cells") {
        let text = std::fs::read_to_string(&f).unwrap_or_else(|e| die(&format!("{f}: {e}")));
        let cells = seeds::parse_cells(&text).unwrap_or_else(|e| die(&format!("{f}: {e}")));
        return plain(cells, format!("cells file={f}"));
    }
    if let Some(f) = a.get("snapshot") {
        let data = std::fs::read(&f).unwrap_or_else(|e| die(&format!("{f}: {e}")));
        let s = Snapshot::decode(&data).unwrap_or_else(|e| die(&format!("{f}: {e}")));
        return Seed { cells: s.cells(), desc: format!("snapshot file={f}"), geo: Some(s.geo.clone()), gen: s.gen, rule: Some(s.rule) };
    }
    unreachable!()
}

fn auto_threads(geo: &Geometry) -> usize {
    let cores = std::thread::available_parallelism().map(|n| n.get()).unwrap_or(1);
    // below ~1.5M cells a generation takes < ~50 µs: barrier overhead dominates
    let by_size = geo.cells() / 1_500_000;
    by_size.clamp(1, cores)
}

/// Build the simulator for a seed. Returns (sim, seed cells not placed).
fn make_sim(a: &Args, seed: &Seed, rule: Rule) -> (BitSim, usize) {
    let geo = build_space(a, &seed.cells, seed.geo.as_ref());
    let mut sim = BitSim::new(geo, rule).unwrap_or_else(|e| die(&e));
    let lost = sim.set_cells(&seed.cells);
    sim.set_generation(seed.gen);
    (sim, lost)
}

fn summary_json(sim: &BitSim, seed: &Seed, res: &RunResult, extra: Vec<(&str, Raw)>) -> String {
    let geo = sim.geometry();
    let h = res.halt;
    let cu = geo.cells() as f64 * res.gens_run() as f64 / res.elapsed.max(1e-9);
    let mut o = Obj::new()
        .f("type", "summary")
        .f("status", res.status())
        .f("period", &h.map(|h| h.period))
        .f("cycle_start", &h.map(|h| h.cycle_start))
        .f("detected_gen", &h.map(|h| h.detected))
        .f("gen", &res.final_gen)
        .f("gens_run", &res.gens_run())
        .f("pop", &res.pop)
        .f("pop_axis", &res.pop_axis)
        .f("seed_pop", &res.seed_pop)
        .f("peak_pop", &res.peak_pop)
        .f("peak_gen", &res.peak_gen)
        .f("hull_initial", &Raw(hull_json(&res.hull_initial)))
        .f("hull_final", &Raw(hull_json(&res.hull_final)))
        .f("firewalls_final", &Raw(res.firewalls_final.as_ref().map(|f| f.to_vec().json()).unwrap_or("null".into())))
        .f("layer_events", &res.layer_events)
        .f("theorem_violations", &res.theorem_violations)
        .f("hash", &format!("{:016x}", res.hash))
        .f("rule", &sim.rule().to_string())
        .f("seed", &seed.desc)
        .f("boundary", geo.boundary.name())
        .f("dims", &geo.n)
        .f("origin", &geo.origin)
        .f("packing", &[sim.packing().0, sim.packing().1])
        .f("threads", &sim.threads())
        .f("elapsed_s", &res.elapsed)
        .f("gens_per_s", &(res.gens_run() as f64 / res.elapsed.max(1e-9)))
        .f("cell_updates_per_s", &cu);
    for (k, v) in extra {
        o = o.f(k, &v);
    }
    o.end()
}

fn run_opts(a: &Args, default_cap: u64) -> RunOpts {
    let no_halt = a.flag("no-halt");
    let gens: Option<u64> = a.num("gens");
    if no_halt && gens.is_none() {
        die("--no-halt needs --gens");
    }
    RunOpts {
        max_gens: Some(gens.unwrap_or(default_cap)),
        stop_on_halt: !no_halt,
        every: a.num("every").unwrap_or(0),
        layers_in_samples: a.flag("layers"),
        need_layers: !a.flag("lite") || a.flag("layers") || a.get("kymo").is_some() || a.get("events").is_some(),
        hash_window: a.num("hash-window").unwrap_or(1 << 20),
    }
}

fn cmd_run(a: &Args) {
    let sp = seed_params(a);
    let seed = build_seed(a, &sp);
    let rule = if a.get("rule").is_some() { sp.rule } else { seed.rule.unwrap_or(sp.rule) };
    let (mut sim, lost) = make_sim(a, &seed, rule);
    if lost > 0 {
        eprintln!("gump: warning: {lost} seed cells lie outside the box and were dropped");
    }
    let threads: usize = a.num("threads").unwrap_or_else(|| auto_threads(sim.geometry()));
    sim.set_threads(threads);
    let mut opts = run_opts(a, 1_000_000_000);
    let mut sinks = Sinks::default();
    let fmt = match a.get("format").as_deref() {
        None | Some("jsonl") => Format::Jsonl,
        Some("csv") => Format::Csv,
        Some(f) => die(&format!("unknown format {f}")),
    };
    let out = a.get("out");
    if opts.every > 0 {
        sinks.samples = Some((writer(out.as_deref().unwrap_or("-")), fmt));
    } else if out.is_some() {
        die("--out needs --every K");
    }
    if let Some(f) = a.get("kymo") {
        sinks.kymo = Some(writer(&f));
        if opts.every == 0 {
            opts.every = 1;
        }
    }
    if let Some(f) = a.get("events") {
        sinks.events = Some(writer(&f));
        if opts.every == 0 {
            opts.every = 1;
        }
    }
    if let Some(f) = a.get("poplog") {
        sinks.poplog = Some(writer(&f));
    }
    if let Some(f) = a.get("trace") {
        sinks.trace = Some(writer(&f));
    }
    let snap_out = a.get("snapshot-out");
    let cells_out = a.get("cells-out");
    a.get("margin");
    a.get("origin");
    a.check_unused();
    if let (Some(h), Boundary::Open) = (Hull::of_cells(&seed.cells), sim.geometry().boundary) {
        // T2 guarantee: does the open box hold the seed's hull?
        let (lo, hi) = h.doubled_bbox();
        let (blo, bhi) = sim.geometry().doubled_bounds();
        if (0..3).any(|t| lo[t] < blo[t] || hi[t] > bhi[t]) && sim.rule().min_birth().unwrap_or(99) >= 4 {
            eprintln!("gump: warning: the box does not contain the seed's diagonal hull; the dead boundary may change the outcome");
        }
    }
    let res = run(&mut sim, &opts, &mut sinks);
    drop(sinks);
    if let Some(f) = snap_out {
        std::fs::write(&f, Snapshot::from_sim(&sim).encode()).unwrap_or_else(|e| die(&format!("{f}: {e}")));
    }
    if let Some(f) = cells_out {
        let hdr = format!("gen {} rule {} pop {}", sim.generation(), sim.rule(), res.pop);
        std::fs::write(&f, seeds::format_cells(&sim.cells(), &hdr)).unwrap_or_else(|e| die(&format!("{f}: {e}")));
    }
    out(&summary_json(&sim, &seed, &res, vec![("dropped_cells", Raw(lost.to_string()))]));
}

fn cmd_info(a: &Args) {
    let sp = seed_params(a);
    let seed = build_seed(a, &sp);
    let rule = if a.get("rule").is_some() { sp.rule } else { seed.rule.unwrap_or(sp.rule) };
    let (sim, lost) = make_sim(a, &seed, rule);
    a.get("margin");
    a.get("origin");
    a.check_unused();
    let s = gump::instruments::sample(&sim, true);
    let hull = s.hull();
    let o = Obj::new()
        .f("type", "info")
        .f("seed", &seed.desc)
        .f("pop", &s.pop)
        .f("pop_axis", &s.pop_axis)
        .f("bbox", &s.bbox.map(|(a, b)| (a, b)))
        .f("hull", &Raw(hull_json(&hull)))
        .f("hull_cells", &hull.as_ref().map(|h| h.volume()))
        .f("firewalls", &s.firewalls().map(|f| f.to_vec()))
        .f("rule", &sim.rule().to_string())
        .f("boundary", sim.geometry().boundary.name())
        .f("dims", &sim.geometry().n)
        .f("origin", &sim.geometry().origin)
        .f("packing", &[sim.packing().0, sim.packing().1])
        .f("box_cells", &sim.geometry().cells())
        .f("dropped_cells", &lost)
        .f("hash", &format!("{:016x}", sim.state_hash()));
    out(&o.end());
}

fn cmd_convert(a: &Args) {
    let sp = seed_params(a);
    let seed = build_seed(a, &sp);
    let rule = if a.get("rule").is_some() { sp.rule } else { seed.rule.unwrap_or(sp.rule) };
    let (sim, lost) = make_sim(a, &seed, rule);
    let snap_out = a.get("snapshot-out");
    let cells_out = a.get("cells-out");
    a.get("margin");
    a.get("origin");
    a.check_unused();
    if snap_out.is_none() && cells_out.is_none() {
        die("convert needs --snapshot-out and/or --cells-out");
    }
    if let Some(f) = snap_out {
        std::fs::write(&f, Snapshot::from_sim(&sim).encode()).unwrap_or_else(|e| die(&format!("{f}: {e}")));
    }
    if let Some(f) = cells_out {
        let hdr = format!("gen {} rule {}", sim.generation(), sim.rule());
        std::fs::write(&f, seeds::format_cells(&sim.cells(), &hdr)).unwrap_or_else(|e| die(&format!("{f}: {e}")));
    }
    out(&Obj::new().f("type", "convert").f("pop", &sim.population()).f("dropped_cells", &lost).end());
}

fn cmd_ensemble(a: &Args) {
    let base = seed_params(a);
    let runs: u64 = a.num("runs").unwrap_or(1);
    let threads: usize = a.num("threads").unwrap_or_else(|| std::thread::available_parallelism().map(|n| n.get()).unwrap_or(1));
    // parameter grid
    let mut grid: Vec<Vec<(String, String)>> = vec![vec![]];
    for v in a.all("vary") {
        let (k, vals) = v.split_once('=').unwrap_or_else(|| die("--vary KEY=V1,V2,..."));
        if !["density", "radius", "half", "rule", "slab-layers"].contains(&k) {
            die(&format!("--vary: cannot vary '{k}'"));
        }
        let mut ng = Vec::new();
        for g in &grid {
            for val in vals.split(',') {
                let mut g2 = g.clone();
                g2.push((k.to_string(), val.to_string()));
                ng.push(g2);
            }
        }
        grid = ng;
    }
    let opts = run_opts(a, 1_000_000);
    let out = a.get("out");
    // validate the seed options once (also consumes the option names)
    let _ = build_seed(a, &base);
    a.get("margin");
    a.get("origin");
    a.get("format");
    a.check_unused();
    if opts.every > 0 {
        die("ensemble writes summaries only (no --every)");
    }
    let mut jobs = Vec::new();
    for g in &grid {
        for r in 0..runs {
            let mut sp = base.clone();
            sp.rng = base.rng + r;
            for (k, v) in g {
                match k.as_str() {
                    "density" => sp.density = v.parse().unwrap_or_else(|_| die("bad density")),
                    "radius" => sp.radius = Some(v.parse().unwrap_or_else(|_| die("bad radius"))),
                    "half" => sp.half = Some(triple(v)),
                    "slab-layers" => sp.slab_layers = Some(v.parse().unwrap_or_else(|_| die("bad slab-layers"))),
                    "rule" => sp.rule = Rule::parse(v).unwrap_or_else(|e| die(&e)),
                    _ => unreachable!(),
                }
            }
            jobs.push((jobs.len(), g.clone(), sp));
        }
    }
    let next = AtomicUsize::new(0);
    let sink: Mutex<Box<dyn Write + Send>> = Mutex::new(match &out {
        Some(f) => Box::new(BufWriter::new(std::fs::File::create(f).unwrap_or_else(|e| die(&format!("{f}: {e}"))))),
        None => Box::new(std::io::stdout()),
    });
    let t0 = Instant::now();
    let total_gens = AtomicUsize::new(0);
    std::thread::scope(|sc| {
        for _ in 0..threads.max(1) {
            sc.spawn(|| loop {
                let i = next.fetch_add(1, Ordering::Relaxed);
                if i >= jobs.len() {
                    break;
                }
                let (idx, params, sp) = &jobs[i];
                let seed = build_seed(a, sp);
                let (mut sim, lost) = make_sim(a, &seed, sp.rule);
                sim.set_threads(1);
                let mut o2 = opts.clone();
                o2.hash_window = o2.hash_window.min(1 << 16);
                let res = run(&mut sim, &o2, &mut Sinks::default());
                total_gens.fetch_add(res.gens_run() as usize, Ordering::Relaxed);
                let pj: Vec<Raw> = params.iter().map(|(k, v)| Raw(Obj::new().f("key", k).f("value", v).end())).collect();
                let line = summary_json(
                    &sim,
                    &seed,
                    &res,
                    vec![("run", Raw(idx.to_string())), ("rng", Raw(sp.rng.to_string())), ("params", Raw(pj.json())), ("dropped_cells", Raw(lost.to_string()))],
                );
                let mut s = sink.lock().unwrap();
                let _ = writeln!(s, "{line}");
                let _ = s.flush();
            });
        }
    });
    let el = t0.elapsed().as_secs_f64();
    let line = Obj::new()
        .f("type", "ensemble_summary")
        .f("runs", &jobs.len())
        .f("threads", &threads)
        .f("elapsed_s", &el)
        .f("runs_per_s", &(jobs.len() as f64 / el))
        .f("total_gens", &total_gens.load(Ordering::Relaxed))
        .end();
    let mut s = sink.lock().unwrap();
    let _ = writeln!(s, "{line}");
}

fn bench_one(name: &str, mut sim: BitSim, gens: u64, threads: usize) -> String {
    sim.set_threads(threads);
    sim.steps(2.min(gens));
    let t = Instant::now();
    sim.steps(gens);
    let el = t.elapsed().as_secs_f64();
    let cells = sim.geometry().cells() as f64;
    Obj::new()
        .f("type", "bench")
        .f("name", name)
        .f("dims", &sim.geometry().n)
        .f("threads", &threads)
        .f("gens", &gens)
        .f("elapsed_s", &el)
        .f("gens_per_s", &(gens as f64 / el))
        .f("cell_updates_per_s", &(cells * gens as f64 / el))
        .end()
}

fn cmd_bench(a: &Args) {
    let quick = a.flag("quick");
    let threads_list: Vec<usize> = match a.get("threads") {
        Some(t) => t.split(',').map(|x| x.parse().unwrap_or_else(|_| die("bad --threads"))).collect(),
        None => vec![1, std::thread::available_parallelism().map(|n| n.get()).unwrap_or(1)],
    };
    a.check_unused();
    let scale = if quick { 0.2 } else { 1.0 };
    // side-13 closed cube in its hull box (open)
    {
        let cells = seeds::legacy_cube(70);
        let geo = Geometry::open_for_hull(&Hull::of_cells(&cells).unwrap(), 1);
        let mut sim = BitSim::new(geo, Rule::GUMP).unwrap();
        sim.set_cells(&cells);
        sim.steps(2000); // into the chaotic plateau
        out(&bench_one("cube13_hullbox", sim.clone(), (20000.0 * scale) as u64, 1));
        let h = gump::instruments::sample(&sim, true).hull();
        sim.restrict_to_hull(h.as_ref());
        out(&bench_one("cube13_hullbox_restricted", sim, (20000.0 * scale) as u64, 1));
    }
    for &n in &[64usize, 128, 256] {
        let geo = Geometry::new([n; 3], [0; 3], Boundary::Torus);
        let (lo, hi) = geo.doubled_bounds();
        let cells = seeds::soup(&Region::Box { lo, hi }, 0.3, 1);
        let mut base = BitSim::new(geo, Rule::GUMP).unwrap();
        base.set_cells(&cells);
        let gens = ((4.0e9 / (3.0 * (n * n * n) as f64)) * scale).max(10.0) as u64;
        for &t in &threads_list {
            out(&bench_one(&format!("soup0.3_torus{n}"), base.clone(), gens, t));
        }
    }
}

fn main() {
    let a = Args::parse();
    match a.cmd.as_str() {
        "run" => cmd_run(&a),
        "ensemble" => cmd_ensemble(&a),
        "info" => cmd_info(&a),
        "convert" => cmd_convert(&a),
        "bench" => cmd_bench(&a),
        "help" | "--help" | "-h" => print!("{HELP}"),
        c => die(&format!("unknown command '{c}' (try gump help)")),
    }
}
