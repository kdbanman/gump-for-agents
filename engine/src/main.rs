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
  gump show     [SEED] [SPACE] [--gens G] [VIEW]          text rendering (kagome layers / slices)
  gump png      [SEED] [SPACE] [--gens G] --view V --out F   PNG image
  gump describe [SEED] [--gens G] [--as-is] [--catalogue F]  period, symmetry, layers, pieces (JSON)

SHOW (text)   default: the pattern as its stack of {111} layers along the diagonal it is
              thinnest in; each layer is a kagome lattice (● live, · dead site, blank =
              hexagon centre / not a cell)
  --orbit                  evolve to the final cycle and show its phases side by side
  --diag D                 layers along diagonal D; --layer S: only layer S
  --slice x|y|z=C          axis-aligned slice (faces as | - in even planes, # in odd planes)
  --orient                 live cells as x/y/z by orientation; --ascii: o and . glyphs
  --max-chars N            refuse bigger renderings (default 20000)
PNG    --view proj-x|proj-y|proj-z|proj-diag [--diag D] | layer --layer S | slab --layers-range S0:S1
              | slice --slice z=C | kymo --kymo F.csv [--events F.jsonl] [--diag D] [--height H]
       --scale N (pixels per unit, default 6)
DESCRIBE  evolves the pattern to its final cycle (cap --cap, default 1e5) and reports
          status, period, pops per phase, union, sym (stabiliser in translations x O_h),
          spacetime_sym, layer extents on the 4 diagonals, nbr_components, canonical cells,
          pieces (R-connected components, each with the same fields); --catalogue
          research/atlas/catalogue.jsonl adds catalogue ids; --as-is describes the input itself

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
      --sym G              symmetric soup: one draw per orbit of point group G about
                           --center (a cube centre or vertex): oh o td th d4h d3d d2h c4v
                           c3v c3 ci c1 (axis-specific groups use z / [111])
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
  --threads T              threads per generation (default 1; for big tori on an idle machine)
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
  (engine) runs whose boxes fit are packed 2-4 per machine word; cycles are found from a
           per-run hash every --check-every K generations (default 32) with the exact
           cycle start recovered by re-simulation; extinction/still lifes are exact every
           generation. Output identical to per-generation hashing (periods <= 512 at the
           cap, <= 2048 elsewhere). --per-gen-hash: the previous engine (one run per
           thread, hash every generation); --no-pack: one run per word.
  --layer-deaths N|all     add "layer_deaths": the first N irreversible layer deaths
                           [{gen, axis, dir, s, cause}] with exact generations (cause hull:
                           outside the hull, T2; firewall: inside >= 3 dead layers, T3), the
                           same events as `run --events F --every 1`
  --hull-at G              add "hull_at": {gen, hull} at generation G
"#;

struct Args {
    cmd: String,
    kv: BTreeMap<String, Vec<String>>,
    flags: Vec<String>,
    used: Mutex<std::collections::BTreeSet<String>>,
}

const BOOL_FLAGS: &[&str] = &["no-halt", "layers", "quick", "lite", "ascii", "orient", "orbit", "as-is", "per-gen-hash", "no-pack"];

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
fn emit_line(line: &str) {
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
        if let Some(gname) = a.get("sym") {
            let group = gump::sym::group(&gname).unwrap_or_else(|| {
                die(&format!("unknown --sym {gname}; groups: {}", gump::sym::GROUPS.iter().map(|g| g.0).collect::<Vec<_>>().join(", ")))
            });
            let center = a.get("center").map(|c| triple(&c)).unwrap_or([0, 0, 0]);
            if let Some(g) = group.iter().find(|g| !gump::sym::maps_cells_to_cells(g, center)) {
                die(&format!("--sym {gname} about {center:?} does not map cells to cells ({g:?}); use a cube centre (all even) or a vertex (all odd)"));
            }
            if let Some(g) = torus.as_ref() {
                if !seeds::torus_admits(&group, g) {
                    die(&format!("--sym {gname} permutes axes of unequal length on torus {:?}", g.n));
                }
            }
            let cells = seeds::soup_sym(&region, sp.density, sp.rng, &group, center, torus.as_ref());
            return plain(cells, format!("soup p={} rng={} sym={} {}", sp.density, sp.rng, gname, region.describe()));
        }
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

fn auto_threads(_geo: &Geometry) -> usize {
    // Threads per generation pay off only for big boxes on an otherwise idle machine
    // (see README); default to 1 and let callers opt in with --threads.
    1
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
    emit_line(&summary_json(&sim, &seed, &res, vec![("dropped_cells", Raw(lost.to_string()))]));
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
    emit_line(&o.end());
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
    emit_line(&Obj::new().f("type", "convert").f("pop", &sim.population()).f("dropped_cells", &lost).end());
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
    let per_gen_hash = a.flag("per-gen-hash");
    let no_pack = a.flag("no-pack");
    let check_every: u64 = a.num("check-every").unwrap_or(32);
    let layer_deaths: Option<usize> = a.get("layer-deaths").map(|v| if v == "all" { usize::MAX } else { v.parse().unwrap_or_else(|_| die("--layer-deaths N|all")) });
    let hull_at: Option<u64> = a.num("hull-at");
    if per_gen_hash && (layer_deaths.is_some() || hull_at.is_some()) {
        die("--layer-deaths / --hull-at need the packed engine (drop --per-gen-hash)");
    }
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
    let sink: Mutex<Box<dyn Write + Send>> = Mutex::new(match &out {
        Some(f) => Box::new(BufWriter::new(std::fs::File::create(f).unwrap_or_else(|e| die(&format!("{f}: {e}"))))),
        None => Box::new(std::io::stdout()),
    });
    let t0 = Instant::now();
    let total_gens = AtomicUsize::new(0);
    let write_line = |line: String| {
        let mut s = sink.lock().unwrap();
        let _ = writeln!(s, "{line}");
        let _ = s.flush();
    };
    let extra = |idx: usize, params: &Vec<(String, String)>, sp: &SeedParams, lost: usize| {
        let pj: Vec<Raw> = params.iter().map(|(k, v)| Raw(Obj::new().f("key", k).f("value", v).end())).collect();
        vec![("run", Raw(idx.to_string())), ("rng", Raw(sp.rng.to_string())), ("params", Raw(pj.json())), ("dropped_cells", Raw(lost.to_string()))]
    };
    if per_gen_hash {
        let next = AtomicUsize::new(0);
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
                    write_line(summary_json(&sim, &seed, &res, extra(*idx, params, sp, lost)));
                });
            }
        });
    } else {
        // Group runs that can share words: same lane box and rule. Soups in open space use
        // the box of their whole region (it holds every soup's hull, so T2 makes it exact).
        use std::collections::{HashMap, VecDeque};
        struct Spec {
            idx: usize,
            params: Vec<(String, String)>,
            sp: SeedParams,
            cells: Vec<P3>,
            desc: String,
            natural: Geometry,
            gen: u64,
            lost: usize,
        }
        let mut groups: Vec<(Geometry, Rule, Mutex<VecDeque<Spec>>)> = Vec::new();
        let mut gindex: HashMap<(Geometry, Rule), usize> = HashMap::new();
        let mut region_box: HashMap<String, Geometry> = HashMap::new();
        let margin: usize = a.num("margin").unwrap_or(1);
        for (idx, params, sp) in &jobs {
            let seed = build_seed(a, sp);
            let (sim, lost) = make_sim(a, &seed, sp.rule);
            let natural = sim.geometry().clone();
            let confined = sp.rule.min_birth().is_none_or(|b| b >= 4);
            let pack = if a.kv.contains_key("soup") && natural.boundary == Boundary::Open && a.get("box").is_none() && confined {
                let region = soup_region(a, sp, None);
                let key = format!("{region:?}");
                region_box
                    .entry(key)
                    .or_insert_with(|| {
                        let full = seeds::soup(&region, 1.0, 0);
                        Hull::of_cells(&full).map(|h| Geometry::open_for_hull(&h, margin)).unwrap_or_else(|| natural.clone())
                    })
                    .clone()
            } else {
                natural.clone()
            };
            let cells = seed.cells.into_iter().filter(|&p| natural.contains_doubled(p)).collect();
            let gi = *gindex.entry((pack.clone(), sp.rule)).or_insert_with(|| {
                groups.push((pack.clone(), sp.rule, Mutex::new(VecDeque::new())));
                groups.len() - 1
            });
            groups[gi].2.lock().unwrap().push_back(Spec { idx: *idx, params: params.clone(), sp: sp.clone(), cells, desc: seed.desc, natural, gen: seed.gen, lost });
        }
        let lopts = gump::lanes::LaneOpts {
            cap: opts.max_gens.unwrap_or(1_000_000),
            check_every: check_every.max(1),
            window: ((1usize << 16) / check_every.max(1) as usize).max(64),
            need_layers: opts.need_layers,
            deaths: layer_deaths,
            hull_at,
            ..Default::default()
        };
        let next_group = AtomicUsize::new(0);
        std::thread::scope(|sc| {
            for _ in 0..threads.max(1) {
                sc.spawn(|| loop {
                    // the next group with work left (round robin)
                    let ng = groups.len();
                    let start = next_group.fetch_add(1, Ordering::Relaxed);
                    let Some(gi) = (0..ng).map(|o| (start + o) % ng).find(|&g| !groups[g].2.lock().unwrap().is_empty()) else { break };
                    let (geo, rule, q) = &groups[gi];
                    let lanes = if no_pack { 1 } else { BitSim::max_lanes(geo.n[0]) };
                    gump::lanes::run_lanes(
                        geo,
                        *rule,
                        lanes,
                        &lopts,
                        || {
                            q.lock().unwrap().pop_front().map(|s| gump::lanes::Job { cells: s.cells.clone(), natural: s.natural.clone(), start_gen: s.gen, tag: s })
                        },
                        |d| {
                            let s = d.tag;
                            total_gens.fetch_add(d.res.gens_run() as usize, Ordering::Relaxed);
                            let seed = Seed { cells: vec![], desc: s.desc.clone(), geo: None, gen: s.gen, rule: None };
                            let mut ex = extra(s.idx, &s.params, &s.sp, s.lost);
                            if layer_deaths.is_some() {
                                let ev: Vec<Raw> = d
                                    .deaths
                                    .iter()
                                    .map(|e| Raw(Obj::new().f("gen", &e.gen).f("axis", &e.axis).f("dir", &gump::lattice::DIAGS[e.axis]).f("s", &e.s).f("cause", e.cause).end()))
                                    .collect();
                                ex.push(("layer_deaths", Raw(ev.json())));
                            }
                            if let Some(g) = hull_at {
                                let v = match &d.hull_at {
                                    Some((gg, h)) => Obj::new().f("gen", gg).f("hull", &Raw(hull_json(h))).end(),
                                    None => Obj::new().f("gen", &g).f("hull", &Raw("null".into())).f("reached", &false).end(),
                                };
                                ex.push(("hull_at", Raw(v)));
                            }
                            write_line(summary_json(&d.sim, &seed, &d.res, ex));
                        },
                    );
                });
            }
        });
    }
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
        emit_line(&bench_one("cube13_hullbox", sim.clone(), (20000.0 * scale) as u64, 1));
        let h = gump::instruments::sample(&sim, true).hull();
        sim.restrict_to_hull(h.as_ref());
        emit_line(&bench_one("cube13_hullbox_restricted", sim, (20000.0 * scale) as u64, 1));
    }
    for &n in &[64usize, 128, 256] {
        let geo = Geometry::new([n; 3], [0; 3], Boundary::Torus);
        let (lo, hi) = geo.doubled_bounds();
        let cells = seeds::soup(&Region::Box { lo, hi }, 0.3, 1);
        let mut base = BitSim::new(geo, Rule::GUMP).unwrap();
        base.set_cells(&cells);
        let gens = ((4.0e9 / (3.0 * (n * n * n) as f64)) * scale).max(10.0) as u64;
        for &t in &threads_list {
            emit_line(&bench_one(&format!("soup0.3_torus{n}"), base.clone(), gens, t));
        }
    }
}

/// Seed → simulator → advanced by --gens. Returns (sim, seed, rule).
fn pattern(a: &Args) -> (BitSim, Seed, Rule) {
    let sp = seed_params(a);
    let seed = build_seed(a, &sp);
    let rule = if a.get("rule").is_some() { sp.rule } else { seed.rule.unwrap_or(sp.rule) };
    let (mut sim, lost) = make_sim(a, &seed, rule);
    if lost > 0 {
        eprintln!("gump: warning: {lost} seed cells lie outside the box and were dropped");
    }
    a.get("margin");
    a.get("origin");
    let g: u64 = a.num("gens").unwrap_or(0);
    let h = gump::instruments::sample(&sim, true).hull();
    sim.restrict_to_hull(h.as_ref());
    sim.steps(g);
    (sim, seed, rule)
}

fn parse_slice(v: &str) -> (usize, i64) {
    let (ax, c) = v.split_once('=').unwrap_or_else(|| die("--slice AXIS=C, e.g. z=0"));
    let ax = match ax {
        "x" => 0,
        "y" => 1,
        "z" => 2,
        _ => die("--slice axis must be x, y or z"),
    };
    (ax, c.parse().unwrap_or_else(|_| die("bad --slice coordinate")))
}

fn cmd_show(a: &Args) {
    use gump::render::*;
    let ascii = a.flag("ascii");
    let g = if ascii { Glyphs::ascii(a.flag("orient")) } else { Glyphs::unicode(a.flag("orient")) };
    let orbit = a.flag("orbit");
    let diag: Option<usize> = a.num("diag");
    let layer_s: Option<i64> = a.num("layer");
    let slice_v = a.get("slice");
    let max_chars: usize = a.num("max-chars").unwrap_or(20_000);
    let cap: u64 = a.num("cap").unwrap_or(100_000);
    let (sim, _seed, rule) = pattern(a);
    a.check_unused();
    let cells = sim.cells();
    // the phases to show
    let (phases, head): (Vec<Vec<P3>>, String) = if orbit {
        let o = gump::describe::evolve(&cells, rule, cap);
        let ph: Vec<Vec<P3>> = o.phases.into_iter().take(16).collect();
        let f = |v: Option<u64>| v.map(|x| x.to_string()).unwrap_or_else(|| "-".into());
        let head = format!("{}, period {}, cycle from gen {}", o.status, f(o.period), f(o.cycle_start.map(|c| c + sim.generation())));
        (ph, head)
    } else {
        (vec![cells.clone()], format!("gen {} pop {}", sim.generation(), cells.len()))
    };
    let mut blocks = Vec::new();
    let union: Vec<P3> = phases.iter().flatten().copied().collect();
    if let Some(v) = slice_v {
        let (ax, c) = parse_slice(&v);
        let (u, w) = match ax {
            0 => (1, 2),
            1 => (0, 2),
            _ => (0, 1),
        };
        let sel: Vec<&P3> = union.iter().filter(|p| p[ax] == c).collect();
        let lo = [sel.iter().map(|p| p[u]).min().unwrap_or(0) - 1, sel.iter().map(|p| p[w]).min().unwrap_or(0) - 1];
        let hi = [sel.iter().map(|p| p[u]).max().unwrap_or(0) + 1, sel.iter().map(|p| p[w]).max().unwrap_or(0) + 1];
        for (k, ph) in phases.iter().enumerate() {
            let live: std::collections::HashSet<P3> = ph.iter().copied().collect();
            let mut b = vec![format!("phase {k}: {}={c} ({}) ", ["x", "y", "z"][ax], ph.iter().filter(|p| p[ax] == c).count())];
            b.extend(slice(&live, ax, c, lo, hi, ascii));
            blocks.push(b);
        }
    } else {
        let d = diag.unwrap_or_else(|| thinnest_diag(&union));
        let frame = Frame::of(&union, d, 0);
        for (k, ph) in phases.iter().enumerate() {
            let title = if phases.len() > 1 { format!("phase {k}") } else { String::new() };
            let mut b = vec![];
            match (layer_s, frame) {
                (Some(sv), _) => {
                    let sel: Vec<P3> = ph.iter().copied().filter(|&p| gump::lattice::layer(p, d) == sv).collect();
                    let fr = Frame::of(&union.iter().copied().filter(|&p| gump::lattice::layer(p, d) == sv).collect::<Vec<_>>(), d, 0);
                    b.push(format!("{title} s={sv} ({})", sel.len()));
                    if let Some(fr) = fr {
                        b.extend(kagome_layer(&sel.iter().copied().collect(), d, sv, fr, g));
                    }
                }
                (None, Some(fr)) => {
                    b.push(title.clone());
                    let live: std::collections::HashSet<P3> = ph.iter().copied().collect();
                    let s: Vec<i64> = union.iter().map(|&p| gump::lattice::layer(p, d)).collect();
                    let (lo, hi) = (*s.iter().min().unwrap(), *s.iter().max().unwrap());
                    for sv in (lo..=hi).step_by(2) {
                        b.push(format!("s={sv} ({})", ph.iter().filter(|&&p| gump::lattice::layer(p, d) == sv).count()));
                        b.extend(kagome_layer(&live, d, sv, fr, g));
                    }
                }
                (None, None) => b.push("(empty)".into()),
            }
            blocks.push(b);
        }
        emit_line(&format!("{head}; layers along {:?} (diag {d})", gump::lattice::DIAGS[d]));
    }
    let lines = if blocks.len() > 1 { hjoin(&blocks, 3) } else { blocks.concat() };
    let n: usize = lines.iter().map(|l| l.len() + 1).sum();
    if n > max_chars {
        die(&format!("rendering is {n} chars (> --max-chars {max_chars}); pick one --layer S or a --slice, or raise --max-chars"));
    }
    for l in lines {
        emit_line(l.trim_end());
    }
}

fn cmd_png(a: &Args) {
    use gump::render::*;
    let out = a.get("out").unwrap_or_else(|| die("png needs --out FILE.png"));
    let view = a.get("view").unwrap_or_else(|| "proj-diag".into());
    let scale: f64 = a.num("scale").unwrap_or(6.0);
    let img = if view == "kymo" {
        let f = a.get("kymo").unwrap_or_else(|| die("--view kymo needs --kymo FILE.csv"));
        let axis: usize = a.num("diag").unwrap_or(0);
        let ev = a.get("events");
        let max_h: usize = a.num("height").unwrap_or(1000);
        a.check_unused();
        let text = std::fs::read_to_string(&f).unwrap_or_else(|e| die(&format!("{f}: {e}")));
        let mut lines = text.lines();
        let header: Vec<i64> = lines.next().unwrap_or("").split(',').skip(2).filter_map(|t| t.parse().ok()).collect();
        let mut rows = Vec::new();
        for l in lines {
            let v: Vec<&str> = l.split(',').collect();
            if v.len() < 2 || v[1].parse::<usize>().ok() != Some(axis) {
                continue;
            }
            let g: u64 = v[0].parse().unwrap_or(0);
            rows.push((g, v[2..].iter().map(|x| x.parse::<f64>().unwrap_or(0.0)).collect::<Vec<f64>>()));
        }
        let mut deaths = Vec::new();
        if let Some(ef) = ev {
            let t = std::fs::read_to_string(&ef).unwrap_or_else(|e| die(&format!("{ef}: {e}")));
            for l in t.lines() {
                let num = |k: &str| l.split(&format!("\"{k}\":")).nth(1).and_then(|r| r.split([',', '}']).next()).and_then(|x| x.trim().parse::<i64>().ok());
                if num("axis") == Some(axis as i64) {
                    if let (Some(s), Some(g)) = (num("s"), num("gen")) {
                        if let Some(col) = header.iter().position(|&h| h == s) {
                            deaths.push((col, g as u64));
                        }
                    }
                }
            }
        }
        png_kymo(&rows, &deaths, scale.max(1.0) as usize, max_h)
    } else {
        let diag: usize = a.num("diag").unwrap_or(0);
        let layer_s: Option<i64> = a.num("layer");
        let layers = a.get("layers-range");
        let slice_v = a.get("slice");
        let (sim, _, _) = pattern(a);
        a.check_unused();
        let cells = sim.cells();
        match view.as_str() {
            "proj-x" => png_axis_projection(&cells, 0, scale as usize),
            "proj-y" => png_axis_projection(&cells, 1, scale as usize),
            "proj-z" => png_axis_projection(&cells, 2, scale as usize),
            "proj-diag" => png_diag_projection(&cells, diag, scale),
            "layer" => {
                let s = layer_s.unwrap_or_else(|| die("--view layer needs --layer S"));
                png_layers(&cells, diag, s, s, scale)
            }
            "slab" => {
                let r = layers.unwrap_or_else(|| die("--view slab needs --layers-range S0:S1"));
                let (x, y) = r.split_once(':').unwrap_or_else(|| die("--layers-range S0:S1"));
                png_layers(&cells, diag, x.parse().unwrap_or_else(|_| die("bad S0")), y.parse().unwrap_or_else(|_| die("bad S1")), scale)
            }
            "slice" => {
                let (ax, c) = parse_slice(&slice_v.unwrap_or_else(|| die("--view slice needs --slice z=C")));
                png_slice(&cells, ax, c, scale as usize)
            }
            v => die(&format!("unknown --view {v} (proj-x|proj-y|proj-z|proj-diag|layer|slab|slice|kymo)")),
        }
    };
    std::fs::write(&out, img.png()).unwrap_or_else(|e| die(&format!("{out}: {e}")));
    emit_line(&Obj::new().f("type", "png").f("out", &out).f("view", &view).f("width", &img.w).f("height", &img.h).end());
}

fn cmd_describe(a: &Args) {
    let cap: u64 = a.num("cap").unwrap_or(100_000);
    let as_is = a.flag("as-is");
    let cat = a.get("catalogue").map(|f| gump::describe::load_catalogue(&f).unwrap_or_else(|e| die(&e)));
    let (sim, _, rule) = pattern(a);
    a.check_unused();
    emit_line(&gump::describe::describe(&sim.cells(), rule, cap, as_is, cat.as_ref()));
}

fn main() {
    let a = Args::parse();
    match a.cmd.as_str() {
        "run" => cmd_run(&a),
        "ensemble" => cmd_ensemble(&a),
        "info" => cmd_info(&a),
        "convert" => cmd_convert(&a),
        "bench" => cmd_bench(&a),
        "show" => cmd_show(&a),
        "png" => cmd_png(&a),
        "describe" => cmd_describe(&a),
        "help" | "--help" | "-h" => print!("{HELP}"),
        c => die(&format!("unknown command '{c}' (try gump help)")),
    }
}
