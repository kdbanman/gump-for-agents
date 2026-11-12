//! Time-averaged occupancy: per-cell live counts accumulated over a window of generations.

use crate::fast::BitSim;
use crate::lattice::{layer, Geometry, Hull, P3, DIAGS};
use crate::render::{kagome_cell, kagome_pos, Frame, Image, BG, DEAD_SITE};

/// Live counts per local cell `(a, i, j, k)`, index `((a·NZ + k)·NY + j)·NX + i` (the
/// snapshot bitmap order), over `frames` generations.
pub struct Occupancy {
    pub geo: Geometry,
    pub counts: Vec<u32>,
    pub frames: u64,
    pub from: u64,
}

impl Occupancy {
    /// Count the current state and the next `frames − 1` generations (`frames` states).
    pub fn accumulate(sim: &mut BitSim, frames: u64) -> Occupancy {
        let geo = sim.geometry().clone();
        let n = geo.n;
        let mut counts = vec![0u32; geo.cells()];
        let from = sim.generation();
        for f in 0..frames {
            sim.for_each_live(|a, i, j, k| counts[((a * n[2] + k) * n[1] + j) * n[0] + i] += 1);
            if f + 1 < frames {
                sim.step();
            }
        }
        Occupancy { geo, counts, frames, from }
    }

    pub fn get(&self, p: P3) -> Option<u32> {
        let (a, c) = self.geo.locate(p)?;
        let n = self.geo.n;
        Some(self.counts[((a * n[2] + c[2]) * n[1] + c[1]) * n[0] + c[0]])
    }

    pub fn frac(&self, p: P3) -> f64 {
        self.get(p).unwrap_or(0) as f64 / self.frames.max(1) as f64
    }

    /// Cells with a nonzero count, (doubled coords, count).
    pub fn nonzero(&self) -> Vec<(P3, u32)> {
        let n = self.geo.n;
        let mut v = Vec::new();
        for (t, &c) in self.counts.iter().enumerate() {
            if c > 0 {
                let i = t % n[0];
                let j = (t / n[0]) % n[1];
                let k = (t / (n[0] * n[1])) % n[2];
                let a = t / (n[0] * n[1] * n[2]);
                v.push((self.geo.to_doubled(a, [i, j, k]), c));
            }
        }
        v
    }

    /// The sites of layer `s` along `d` inside `hull` (or every site with a nonzero count).
    pub fn layer_sites(&self, d: usize, s: i64, hull: Option<&Hull>) -> Vec<P3> {
        let nz: Vec<P3> = self.nonzero().into_iter().map(|x| x.0).filter(|&p| layer(p, d) == s).collect();
        let Some(h) = hull else { return nz };
        let Some(fr) = Frame::of(&nz, d, 6) else { return vec![] };
        let mut v = Vec::new();
        for row in fr.r0..=fr.r1 {
            for col in fr.c0..=fr.c1 {
                if let Some(p) = kagome_cell(col, row, s, d) {
                    if h.contains(p) {
                        v.push(p);
                    }
                }
            }
        }
        v
    }

    /// Text map of layer `s` along `d`: each site is a digit `⌊10·f⌋` (9 = 90–100% of the
    /// generations live), `·` for a site never live; kagome layout as in `gump show`.
    pub fn layer_text(&self, d: usize, s: i64, sites: &[P3]) -> Vec<String> {
        let Some(fr) = Frame::of(sites, d, 0) else { return vec!["(no sites)".into()] };
        let set: std::collections::HashSet<P3> = sites.iter().copied().collect();
        let mut out = Vec::new();
        for row in fr.r0..=fr.r1 {
            let mut line = String::new();
            for col in fr.c0..=fr.c1 {
                match kagome_cell(col, row, s, d) {
                    Some(p) if set.contains(&p) => {
                        let f = self.frac(p);
                        if f == 0.0 {
                            line.push('·');
                        } else {
                            line.push(char::from(b'0' + ((f * 10.0).floor() as u8).min(9)));
                        }
                    }
                    _ => line.push(' '),
                }
            }
            out.push(line.trim_end().to_string());
        }
        out
    }

    /// PNG of layer `s` along `d`: discs coloured by occupancy (ramp from 0 to `vmax`).
    pub fn layer_png(&self, d: usize, _s: i64, sites: &[P3], scale: f64, vmax: f64) -> Image {
        let pts: Vec<(f64, f64, f64)> = sites
            .iter()
            .map(|&p| {
                let (c, r) = kagome_pos(p, d);
                (c as f64 / 2.0, r as f64 * 0.866_025_4, self.frac(p))
            })
            .collect();
        if pts.is_empty() {
            return Image::new(8, 8, BG);
        }
        let x0 = pts.iter().map(|p| p.0).fold(f64::MAX, f64::min) - 1.0;
        let x1 = pts.iter().map(|p| p.0).fold(f64::MIN, f64::max) + 1.0;
        let y0 = pts.iter().map(|p| p.1).fold(f64::MAX, f64::min) - 1.0;
        let y1 = pts.iter().map(|p| p.1).fold(f64::MIN, f64::max) + 1.0;
        let bar = 14.0;
        let w = ((x1 - x0) * scale).ceil() as usize;
        let h = ((y1 - y0) * scale + bar).ceil() as usize;
        let mut img = Image::new(w, h, BG);
        for &(x, y, f) in &pts {
            let c = if f == 0.0 { DEAD_SITE } else { crate::render::ramp(f / vmax.max(1e-9)) };
            img.disc((x - x0) * scale, (y - y0) * scale, 0.42 * scale, c);
        }
        // colour bar 0 .. vmax along the bottom
        for x in 0..w {
            let c = crate::render::ramp(x as f64 / w as f64);
            img.rect(x as i64, (h as f64 - bar + 3.0) as i64, x as i64 + 1, h as i64 - 2, c);
        }
        img
    }

    /// Mean occupancy of layer sites binned by in-plane distance from the layer's point
    /// on the diagonal through the origin (doubled units, bins of width 2):
    /// `(bin centre, mean, sites)`.
    pub fn radial_profile(&self, d: usize, sites: &[P3], center: [f64; 3]) -> Vec<(f64, f64, usize)> {
        let v = DIAGS[d];
        let mut bins: std::collections::BTreeMap<i64, (f64, usize)> = std::collections::BTreeMap::new();
        for &p in sites {
            let q = [p[0] as f64 - center[0], p[1] as f64 - center[1], p[2] as f64 - center[2]];
            let along = (q[0] * v[0] as f64 + q[1] * v[1] as f64 + q[2] * v[2] as f64) / 3.0;
            let r2 = (0..3).map(|t| (q[t] - along * v[t] as f64).powi(2)).sum::<f64>();
            let b = (r2.sqrt() / 2.0).floor() as i64;
            let e = bins.entry(b).or_insert((0.0, 0));
            e.0 += self.frac(p);
            e.1 += 1;
        }
        bins.into_iter().map(|(b, (s, n))| (2.0 * b as f64 + 1.0, s / n as f64, n)).collect()
    }

    /// `.npy` (NumPy v1.0) of the counts, dtype `<u4`, shape `(3, NZ, NY, NX)`.
    pub fn npy(&self) -> Vec<u8> {
        let n = self.geo.n;
        let mut header = format!("{{'descr': '<u4', 'fortran_order': False, 'shape': (3, {}, {}, {}), }}", n[2], n[1], n[0]);
        while (10 + header.len() + 1) % 64 != 0 {
            header.push(' ');
        }
        header.push('\n');
        let mut out = b"\x93NUMPY\x01\x00".to_vec();
        out.extend_from_slice(&(header.len() as u16).to_le_bytes());
        out.extend_from_slice(header.as_bytes());
        for c in &self.counts {
            out.extend_from_slice(&c.to_le_bytes());
        }
        out
    }
}
