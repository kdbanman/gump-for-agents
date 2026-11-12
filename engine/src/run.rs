//! The run driver: steps a `BitSim`, detects halting, takes samples every K generations,
//! tracks layer deaths, and writes the time series / kymograph / events / population log.

use crate::fast::BitSim;
use crate::instruments::{sample, Halt, HaltDetector, LayerTracker, Sample, Status};
use crate::json::{Obj, ToJson};
use crate::lattice::{Hull, DIAGS};
use std::io::Write;
use std::time::Instant;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Format {
    Jsonl,
    Csv,
}

#[derive(Clone, Debug)]
pub struct RunOpts {
    /// stop after this many generations (counted from the start); None = until halt
    pub max_gens: Option<u64>,
    /// stop as soon as extinction / still life / a cycle is detected
    pub stop_on_halt: bool,
    /// sample every K generations (0 = only the initial and final state)
    pub every: u64,
    /// include the full per-layer populations in sample records
    pub layers_in_samples: bool,
    /// compute layers at sample points (hull, firewalls, kymograph, layer events)
    pub need_layers: bool,
    /// detect cycles by hashing every generation (window = hashes kept)
    pub hash_window: usize,
    /// write a snapshot to this file every N generations (atomically: tmp + rename)
    pub checkpoint: Option<(String, u64)>,
}

impl Default for RunOpts {
    fn default() -> Self {
        RunOpts { max_gens: None, stop_on_halt: true, every: 0, layers_in_samples: false, need_layers: false, hash_window: 1 << 20, checkpoint: None }
    }
}

#[derive(Default)]
pub struct Sinks {
    pub samples: Option<(Box<dyn Write>, Format)>,
    pub kymo: Option<Box<dyn Write>>,
    pub events: Option<Box<dyn Write>>,
    pub poplog: Option<Box<dyn Write>>,
    pub trace: Option<Box<dyn Write>>,
}

#[derive(Clone, Debug)]
pub struct RunResult {
    pub start_gen: u64,
    pub final_gen: u64,
    pub halt: Option<Halt>,
    pub seed_pop: u64,
    pub pop: u64,
    pub pop_axis: [u64; 3],
    pub peak_pop: u64,
    pub peak_gen: u64,
    pub hull_initial: Option<Hull>,
    pub hull_final: Option<Hull>,
    pub firewalls_final: Option<[Vec<(i64, i64)>; 4]>,
    pub layer_events: u64,
    pub theorem_violations: u64,
    pub hash: u64,
    pub elapsed: f64,
}

impl RunResult {
    pub fn gens_run(&self) -> u64 {
        self.final_gen - self.start_gen
    }
    pub fn status(&self) -> &'static str {
        self.halt.map(|h| h.status.name()).unwrap_or(Status::Running.name())
    }
}

pub fn hull_json(h: &Option<Hull>) -> String {
    match h {
        Some(h) => h.0.to_vec().json(),
        None => "null".into(),
    }
}

fn sample_json(s: &Sample, with_layers: bool, hash: u64) -> String {
    let mut o = Obj::new()
        .f("type", "sample")
        .f("gen", &s.gen)
        .f("hash", &format!("{hash:016x}"))
        .f("pop", &s.pop)
        .f("pop_axis", &s.pop_axis)
        .f("changed", &s.changed)
        .f("bbox", &s.bbox.map(|(a, b)| (a, b)));
    if s.layers.is_some() {
        o = o.f("hull", &crate::json::Raw(hull_json(&s.hull()))).f("firewalls", &s.firewalls().unwrap().to_vec());
        if with_layers {
            let l = s.layers.as_ref().unwrap();
            let v: Vec<crate::json::Raw> = l
                .iter()
                .map(|h| crate::json::Raw(Obj::new().f("s_min", &h.s_min).f("counts", &h.counts).end()))
                .collect();
            o = o.f("layers", &v);
        }
    }
    o.end()
}

const CSV_HEADER: &str = "gen,pop,pop_x,pop_y,pop_z,changed,bbox_xlo,bbox_ylo,bbox_zlo,bbox_xhi,bbox_yhi,bbox_zhi,\
hull0_lo,hull0_hi,hull1_lo,hull1_hi,hull2_lo,hull2_hi,hull3_lo,hull3_hi,firewalls0,firewalls1,firewalls2,firewalls3";

fn sample_csv(s: &Sample) -> String {
    let opt = |v: Option<i64>| v.map(|x| x.to_string()).unwrap_or_default();
    let mut f: Vec<String> = vec![
        s.gen.to_string(),
        s.pop.to_string(),
        s.pop_axis[0].to_string(),
        s.pop_axis[1].to_string(),
        s.pop_axis[2].to_string(),
        s.changed.map(|c| c.to_string()).unwrap_or_default(),
    ];
    for i in 0..6 {
        f.push(opt(s.bbox.map(|(a, b)| if i < 3 { a[i] } else { b[i - 3] })));
    }
    let hull = s.hull();
    for d in 0..4 {
        f.push(opt(hull.as_ref().map(|h| h.0[d].0)));
        f.push(opt(hull.as_ref().map(|h| h.0[d].1)));
    }
    let fw = s.firewalls();
    for d in 0..4 {
        f.push(fw.as_ref().map(|w| w[d].len().to_string()).unwrap_or_default());
    }
    f.join(",")
}

struct Kymo {
    out: Box<dyn Write>,
    /// layer-coordinate columns
    s_lo: i64,
    s_hi: i64,
}

impl Kymo {
    fn new(mut out: Box<dyn Write>, first: &Sample) -> Kymo {
        let l = first.layers.as_ref().unwrap();
        let (s_lo, s_hi) = if l[0].modulus.is_some() {
            (1, l[0].modulus.unwrap() - 1)
        } else {
            let mut lo = i64::MAX;
            let mut hi = i64::MIN;
            for h in l.iter() {
                if let Some((a, b)) = h.extent() {
                    lo = lo.min(a);
                    hi = hi.max(b);
                }
            }
            if lo > hi {
                (1, 1)
            } else {
                (lo, hi)
            }
        };
        let cols: Vec<String> = (0..=((s_hi - s_lo) / 2)).map(|n| (s_lo + 2 * n).to_string()).collect();
        let _ = writeln!(out, "gen,axis,{}", cols.join(","));
        Kymo { out, s_lo, s_hi }
    }
    fn row(&mut self, s: &Sample) {
        let l = s.layers.as_ref().unwrap();
        for (d, h) in l.iter().enumerate() {
            let mut line = format!("{},{}", s.gen, d);
            let mut sv = self.s_lo;
            while sv <= self.s_hi {
                let idx = (sv - h.s_min) / 2;
                let c = if idx >= 0 && (idx as usize) < h.counts.len() { h.counts[idx as usize] } else { 0 };
                line.push(',');
                line.push_str(&c.to_string());
                sv += 2;
            }
            let _ = writeln!(self.out, "{line}");
        }
    }
}

/// Run `sim` according to `opts`, writing to `sinks`.
pub fn run(sim: &mut BitSim, opts: &RunOpts, sinks: &mut Sinks) -> RunResult {
    let t0 = Instant::now();
    let start = sim.generation();
    let birth0 = sim.rule().birth & 1 == 1;
    let need_layers = opts.need_layers || sinks.kymo.is_some() || sinks.events.is_some();

    let first = sample(sim, true);
    let mut restricted_hull = first.hull();
    sim.restrict_to_hull(restricted_hull.as_ref());
    let mut res = RunResult {
        start_gen: start,
        final_gen: start,
        halt: None,
        seed_pop: first.pop,
        pop: first.pop,
        pop_axis: first.pop_axis,
        peak_pop: first.pop,
        peak_gen: start,
        hull_initial: first.hull(),
        hull_final: None,
        firewalls_final: None,
        layer_events: 0,
        theorem_violations: 0,
        hash: sim.state_hash(),
        elapsed: 0.0,
    };

    let mut tracker = if need_layers { Some(LayerTracker::new()) } else { None };
    let mut kymo = sinks.kymo.take().map(|o| Kymo::new(o, &first));
    let mut csv_header_done = false;

    // emit one sample (and its derived records)
    let mut emit = |s: &Sample, hash: u64, sinks: &mut Sinks, res: &mut RunResult, tracker: &mut Option<LayerTracker>, kymo: &mut Option<Kymo>| {
        if let Some(t) = tracker.as_mut() {
            let ev = t.update(s);
            res.layer_events += ev.len() as u64;
            res.theorem_violations = t.violations.len() as u64;
            if let Some(out) = sinks.events.as_mut() {
                for e in ev {
                    let _ = writeln!(
                        out,
                        "{}",
                        Obj::new()
                            .f("type", "layer_death")
                            .f("gen", &e.gen)
                            .f("axis", &e.axis)
                            .f("dir", &DIAGS[e.axis])
                            .f("s", &e.s)
                            .f("last_alive", &e.last_alive)
                            .f("cause", e.cause)
                            .end()
                    );
                }
            }
        }
        if let Some(k) = kymo.as_mut() {
            k.row(s);
        }
        if let Some((out, fmt)) = sinks.samples.as_mut() {
            match fmt {
                Format::Jsonl => {
                    let _ = writeln!(out, "{}", sample_json(s, opts.layers_in_samples, hash));
                }
                Format::Csv => {
                    if !csv_header_done {
                        let _ = writeln!(out, "{CSV_HEADER}");
                        csv_header_done = true;
                    }
                    let _ = writeln!(out, "{}", sample_csv(s));
                }
            }
        }
    };

    let sampling = opts.every > 0;
    if sampling || need_layers {
        emit(&first, res.hash, sinks, &mut res, &mut tracker, &mut kymo);
    }
    if let Some(out) = sinks.poplog.as_mut() {
        let _ = writeln!(out, "{} {}", start, first.pop);
    }
    if let Some(out) = sinks.trace.as_mut() {
        write_trace(out.as_mut(), start, sim);
    }

    let mut det = if opts.hash_window > 0 { Some(HaltDetector::new(opts.hash_window)) } else { None };
    if let Some(d) = det.as_mut() {
        d.observe(start, res.hash);
    }
    if first.pop == 0 && !birth0 {
        res.halt = Some(Halt { status: Status::Extinct, period: 1, cycle_start: start, detected: start });
    }
    let mut last_sampled = start;

    if !(res.halt.is_some() && opts.stop_on_halt) {
        let max = opts.max_gens.unwrap_or(u64::MAX);
        sim.run_steps(max, |sim| {
            let g = sim.generation();
            let acc = sim.last_step().expect("kernel stats are required by the runner");
            let pop: u64 = acc.pop.iter().sum();
            if pop > res.peak_pop {
                res.peak_pop = pop;
                res.peak_gen = g;
            }
            if let Some(out) = sinks.poplog.as_mut() {
                let _ = writeln!(out, "{g} {pop}");
            }
            if let Some(out) = sinks.trace.as_mut() {
                write_trace(out.as_mut(), g, sim);
            }
            if res.halt.is_none() {
                if pop == 0 && !birth0 {
                    res.halt = Some(Halt { status: Status::Extinct, period: 1, cycle_start: g, detected: g });
                } else if acc.diff == 0 {
                    res.halt = Some(Halt { status: Status::Still, period: 1, cycle_start: g - 1, detected: g });
                } else if let Some(d) = det.as_mut() {
                    if let Some((p, mu)) = d.observe(g, acc.hash) {
                        // verify exactly: advance a copy p generations and compare
                        let mut c = sim.clone();
                        c.steps(p);
                        if c.same_state(sim) {
                            res.halt = Some(Halt { status: Status::Periodic, period: p, cycle_start: mu, detected: g });
                        } else {
                            d.forget(acc.hash);
                            d.observe(g, acc.hash);
                        }
                    }
                }
            }
            if let Some((path, n)) = &opts.checkpoint {
                if *n > 0 && g % n == 0 {
                    let tmp = format!("{path}.tmp");
                    if std::fs::write(&tmp, crate::snapshot::Snapshot::from_sim(sim).encode()).is_ok() {
                        let _ = std::fs::rename(&tmp, path);
                    }
                }
            }
            if sampling && (g - start) % opts.every == 0 {
                let s = sample(sim, need_layers);
                // the hull only shrinks (T2): tighten the kernel's work region
                if let (Some(h), Some(old)) = (s.hull(), restricted_hull.as_ref()) {
                    if h != *old {
                        sim.restrict_to_hull(Some(&h));
                        restricted_hull = Some(h);
                    }
                }
                emit(&s, acc.hash, sinks, &mut res, &mut tracker, &mut kymo);
                last_sampled = g;
            }
            !(res.halt.is_some() && opts.stop_on_halt)
        });
    }

    let fin = sample(sim, true);
    let fin_hash = sim.state_hash();
    if (sampling || need_layers) && last_sampled != sim.generation() {
        emit(&fin, fin_hash, sinks, &mut res, &mut tracker, &mut kymo);
    }
    res.final_gen = sim.generation();
    res.pop = fin.pop;
    res.pop_axis = fin.pop_axis;
    res.hull_final = fin.hull();
    res.firewalls_final = fin.firewalls();
    res.hash = fin_hash;
    res.elapsed = t0.elapsed().as_secs_f64();
    for o in [sinks.samples.as_mut().map(|x| &mut x.0), sinks.events.as_mut(), sinks.poplog.as_mut(), sinks.trace.as_mut()]
        .into_iter()
        .flatten()
    {
        let _ = o.flush();
    }
    if let Some(mut k) = kymo {
        let _ = k.out.flush();
    }
    res
}

fn write_trace(out: &mut dyn Write, g: u64, sim: &BitSim) {
    let cells = sim.cells();
    let mut line = g.to_string();
    for p in cells {
        line.push_str(&format!(" {},{},{}", p[0], p[1], p[2]));
    }
    let _ = writeln!(out, "{line}");
}
