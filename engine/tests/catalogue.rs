//! `describe` against the atlas catalogue (research/atlas/catalogue.jsonl): for every
//! object, evolving its phase 0 must give its period, pops, union, symmetry orders, layer
//! spans and neighbour components, and its canonical form must be the stored cells.
use gump::describe::{components, evolve};
use gump::lattice::{layer, P3};
use gump::sym;
use gump::Rule;

fn ints(s: &str) -> Vec<i64> {
    s.split(|c: char| !(c.is_ascii_digit() || c == '-')).filter(|t| !t.is_empty()).filter_map(|t| t.parse().ok()).collect()
}
fn field<'a>(line: &'a str, k: &str) -> &'a str {
    let r = line.split(&format!("\"{k}\":")).nth(1).unwrap();
    let end = if r.starts_with('[') {
        let mut depth = 0;
        let mut e = 0;
        for (i, c) in r.char_indices() {
            if c == '[' {
                depth += 1;
            } else if c == ']' {
                depth -= 1;
                if depth == 0 {
                    e = i + 1;
                    break;
                }
            }
        }
        e
    } else {
        r.find([',', '}']).unwrap()
    };
    &r[..end]
}

#[test]
fn catalogue_objects_described_exactly() {
    let path = concat!(env!("CARGO_MANIFEST_DIR"), "/../research/atlas/catalogue.jsonl");
    let Ok(text) = std::fs::read_to_string(path) else {
        eprintln!("no catalogue at {path}; skipped");
        return;
    };
    let mut n = 0;
    for line in text.lines().filter(|l| !l.is_empty()) {
        let id = field(line, "id");
        let c = ints(field(line, "cells"));
        let cells: Vec<P3> = c.chunks(3).map(|v| [v[0], v[1], v[2]]).collect();
        let o = evolve(&cells, Rule::GUMP, 10_000);
        let period = field(line, "period").parse::<u64>().unwrap();
        assert_eq!(o.cycle_start, Some(0), "{id}: not periodic from phase 0");
        assert_eq!(o.period, Some(period), "{id}");
        let pops: Vec<i64> = ints(field(line, "pops"));
        assert_eq!(o.phases.iter().map(|p| p.len() as i64).collect::<Vec<_>>(), pops, "{id} pops");
        let union: std::collections::BTreeSet<P3> = o.phases.iter().flatten().copied().collect();
        let union: Vec<P3> = union.into_iter().collect();
        assert_eq!(union.len() as i64, field(line, "union").parse::<i64>().unwrap(), "{id} union");
        assert_eq!(sym::stabiliser_order(&o.phases[0]) as i64, field(line, "sym").parse::<i64>().unwrap(), "{id} sym");
        assert_eq!(sym::spacetime_order(&o.phases) as i64, field(line, "spacetime_sym").parse::<i64>().unwrap(), "{id} spacetime_sym");
        // atlas layer order: (1,1,1), (1,1,-1), (1,-1,1), (-1,1,1) = our diagonals 0, 3, 2, 1
        let want = ints(field(line, "layers"));
        for (k, d) in [0usize, 3, 2, 1].iter().enumerate() {
            let s: Vec<i64> = union.iter().map(|&p| layer(p, *d)).collect();
            let nl = (s.iter().max().unwrap() - s.iter().min().unwrap()) / 2 + 1;
            assert_eq!(nl, want[k], "{id} layers");
        }
        assert_eq!(components(&union, 1).len() as i64, field(line, "nbr_components").parse::<i64>().unwrap(), "{id} components");
        assert_eq!(sym::canonical_orbit(&o.phases).0, sym::normalise(&cells), "{id} canonical");
        n += 1;
    }
    eprintln!("checked {n} catalogue objects");
    assert!(n > 1000);
}
