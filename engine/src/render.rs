//! Renderings for agents (text) and humans (PNG).
//!
//! **Text.** A `{111}` layer `s = d·p` is a kagome lattice. Reflect `p` so that `d` becomes
//! `[111]` (`p' = (d_x x, d_y y, d_z z)`); the layer's cells are then all `(x', y')` except
//! `(odd, odd)`, and `(x', y')` projected along `[111]` is a triangular lattice. Drawing
//! site `(x', y')` at column `2x' + y'`, row `y'` puts every site at its true position:
//! even rows are full (`· · · ·`), odd rows hold every other site (`·   ·`), and the blanks
//! between are the hexagon centres:
//!
//! ```text
//!  ● · · ●        s = layer coordinate; ● live, · dead site
//!   ·   ●
//!    · ● · ·
//! ```
//! A small 3D pattern is shown as its stack of layers along one diagonal (all layers share
//! one frame, so vertical alignment is meaningful). Axis-aligned slices draw faces as the
//! segments in which they cut the plane (`|`, `-`) or as squares (`#`) when the plane
//! is the face's own plane.
//!
//! **PNG.** A dependency-free RGB PNG writer (zlib "stored" blocks) and renderers for axis
//! and `[111]` projections, single layers / slabs, slices and kymographs.

use crate::lattice::{cell_axis, layer, P3, DIAGS};
use std::collections::{HashMap, HashSet};

#[derive(Clone, Copy, Debug)]
pub struct Glyphs {
    pub live: [&'static str; 3],
    pub dead: &'static str,
}

impl Glyphs {
    pub fn unicode(orient: bool) -> Glyphs {
        Glyphs { live: if orient { ["x", "y", "z"] } else { ["●", "●", "●"] }, dead: "·" }
    }
    pub fn ascii(orient: bool) -> Glyphs {
        Glyphs { live: if orient { ["x", "y", "z"] } else { ["o", "o", "o"] }, dead: "." }
    }
}

/// `p` reflected so that diagonal `d` becomes `[111]`.
#[inline]
pub fn to_d111(p: P3, d: usize) -> P3 {
    let v = DIAGS[d];
    [v[0] * p[0], v[1] * p[1], v[2] * p[2]]
}

/// Screen position (col, row) of a cell in its layer along `d`.
#[inline]
pub fn kagome_pos(p: P3, d: usize) -> (i64, i64) {
    let q = to_d111(p, d);
    (2 * q[0] + q[1], q[1])
}

/// The cell at screen position (col, row) of layer `s` along `d`, if any.
pub fn kagome_cell(col: i64, row: i64, s: i64, d: usize) -> Option<P3> {
    let y = row;
    if (col - y).rem_euclid(2) != 0 {
        return None;
    }
    let x = (col - y) / 2;
    let z = s - x - y;
    let q = [x, y, z];
    cell_axis(q)?;
    Some(to_d111(q, d)) // the reflection is an involution
}

/// A frame (inclusive screen bounds) for kagome renderings.
#[derive(Clone, Copy, Debug)]
pub struct Frame {
    pub c0: i64,
    pub c1: i64,
    pub r0: i64,
    pub r1: i64,
}

impl Frame {
    pub fn of(cells: &[P3], d: usize, margin: i64) -> Option<Frame> {
        let mut f: Option<Frame> = None;
        for &p in cells {
            let (c, r) = kagome_pos(p, d);
            f = Some(match f {
                None => Frame { c0: c, c1: c, r0: r, r1: r },
                Some(f) => Frame { c0: f.c0.min(c), c1: f.c1.max(c), r0: f.r0.min(r), r1: f.r1.max(r) },
            });
        }
        f.map(|f| Frame { c0: f.c0 - 2 * margin, c1: f.c1 + 2 * margin, r0: f.r0 - margin, r1: f.r1 + margin })
    }
}

/// Text lines for layer `s` along `d` inside `frame`.
pub fn kagome_layer(live: &HashSet<P3>, d: usize, s: i64, frame: Frame, g: Glyphs) -> Vec<String> {
    let mut out = Vec::new();
    for row in frame.r0..=frame.r1 {
        let mut line = String::new();
        for col in frame.c0..=frame.c1 {
            match kagome_cell(col, row, s, d) {
                Some(p) if live.contains(&p) => line.push_str(g.live[cell_axis(p).unwrap()]),
                Some(_) => line.push_str(g.dead),
                None => line.push(' '),
            }
        }
        out.push(line);
    }
    out
}

/// The diagonal along which `cells` spans the fewest layers.
pub fn thinnest_diag(cells: &[P3]) -> usize {
    (0..4)
        .min_by_key(|&d| {
            let s: Vec<i64> = cells.iter().map(|&p| layer(p, d)).collect();
            s.iter().max().unwrap_or(&0) - s.iter().min().unwrap_or(&0)
        })
        .unwrap_or(0)
}

/// A pattern as its stack of layers along `d` (every layer with a live cell, plus the
/// dead layers in between), one shared frame. `title` heads the block.
pub fn layer_stack(cells: &[P3], d: usize, g: Glyphs, title: &str) -> Vec<String> {
    let mut out = vec![title.to_string()];
    if cells.is_empty() {
        out.push("(empty)".into());
        return out;
    }
    let live: HashSet<P3> = cells.iter().copied().collect();
    let frame = Frame::of(cells, d, 0).unwrap();
    let s: Vec<i64> = cells.iter().map(|&p| layer(p, d)).collect();
    let (lo, hi) = (*s.iter().min().unwrap(), *s.iter().max().unwrap());
    let mut sv = lo;
    while sv <= hi {
        let n = s.iter().filter(|&&x| x == sv).count();
        out.push(format!("s={sv} ({n})"));
        out.extend(kagome_layer(&live, d, sv, frame, g));
        sv += 2;
    }
    out
}

/// Place text blocks side by side.
pub fn hjoin(blocks: &[Vec<String>], gap: usize) -> Vec<String> {
    let widths: Vec<usize> = blocks.iter().map(|b| b.iter().map(|l| l.chars().count()).max().unwrap_or(0)).collect();
    let h = blocks.iter().map(|b| b.len()).max().unwrap_or(0);
    let mut out = Vec::with_capacity(h);
    for r in 0..h {
        let mut line = String::new();
        for (b, &w) in blocks.iter().zip(&widths) {
            let s = b.get(r).map(|s| s.as_str()).unwrap_or("");
            line.push_str(s);
            for _ in s.chars().count()..w + gap {
                line.push(' ');
            }
        }
        out.push(line.trim_end().to_string());
    }
    out
}

/// Axis-aligned slice: doubled coordinate `axis` = `c`, drawn over the doubled range
/// `[lo, hi]` of the other two axes (u = first, v = second remaining axis).
/// Even `c`: faces normal to u are `|`, normal to v are `-`, dead faces `·`.
/// Odd `c`: faces normal to `axis` (squares) are `#`, dead `·`.
pub fn slice(live: &HashSet<P3>, axis: usize, c: i64, lo: [i64; 2], hi: [i64; 2], ascii: bool) -> Vec<String> {
    let (u, v) = match axis {
        0 => (1, 2),
        1 => (0, 2),
        _ => (0, 1),
    };
    let mk = |a: i64, b: i64| {
        let mut p = [0i64; 3];
        p[axis] = c;
        p[u] = a;
        p[v] = b;
        p
    };
    let dead = if ascii { "." } else { "·" };
    let mut out = Vec::new();
    if c.rem_euclid(2) == 1 {
        let (u0, v0) = (lo[0] + lo[0].rem_euclid(2), lo[1] + lo[1].rem_euclid(2));
        let mut b = v0;
        while b <= hi[1] {
            let mut line = String::new();
            let mut a = u0;
            while a <= hi[0] {
                line.push_str(if live.contains(&mk(a, b)) { "#" } else { dead });
                line.push(' ');
                a += 2;
            }
            out.push(line.trim_end().to_string());
            b += 2;
        }
    } else {
        for b in lo[1]..=hi[1] {
            let mut line = String::new();
            for a in lo[0]..=hi[0] {
                let p = mk(a, b);
                let g = match cell_axis(p) {
                    Some(ax) if live.contains(&p) => {
                        if ax == u {
                            "|"
                        } else {
                            "-"
                        }
                    }
                    Some(_) => dead,
                    None => " ",
                };
                line.push_str(g);
            }
            out.push(line.trim_end().to_string());
        }
    }
    out
}

// ------------------------------------------------------------------ PNG

fn crc32(data: &[u8]) -> u32 {
    let mut table = [0u32; 256];
    for (n, t) in table.iter_mut().enumerate() {
        let mut c = n as u32;
        for _ in 0..8 {
            c = if c & 1 != 0 { 0xEDB8_8320 ^ (c >> 1) } else { c >> 1 };
        }
        *t = c;
    }
    let mut c = 0xFFFF_FFFFu32;
    for &b in data {
        c = table[((c ^ b as u32) & 0xff) as usize] ^ (c >> 8);
    }
    c ^ 0xFFFF_FFFF
}

/// RGB image.
#[derive(Clone)]
pub struct Image {
    pub w: usize,
    pub h: usize,
    pub px: Vec<[u8; 3]>,
}

impl Image {
    pub fn new(w: usize, h: usize, bg: [u8; 3]) -> Image {
        Image { w, h, px: vec![bg; w * h] }
    }
    pub fn set(&mut self, x: i64, y: i64, c: [u8; 3]) {
        if x >= 0 && y >= 0 && (x as usize) < self.w && (y as usize) < self.h {
            self.px[y as usize * self.w + x as usize] = c;
        }
    }
    pub fn disc(&mut self, cx: f64, cy: f64, r: f64, c: [u8; 3]) {
        let (x0, x1) = ((cx - r).floor() as i64, (cx + r).ceil() as i64);
        let (y0, y1) = ((cy - r).floor() as i64, (cy + r).ceil() as i64);
        for y in y0..=y1 {
            for x in x0..=x1 {
                let (dx, dy) = (x as f64 + 0.5 - cx, y as f64 + 0.5 - cy);
                if dx * dx + dy * dy <= r * r {
                    self.set(x, y, c);
                }
            }
        }
    }
    pub fn rect(&mut self, x0: i64, y0: i64, x1: i64, y1: i64, c: [u8; 3]) {
        for y in y0..y1 {
            for x in x0..x1 {
                self.set(x, y, c);
            }
        }
    }
    /// PNG bytes (8-bit RGB, no compression).
    pub fn png(&self) -> Vec<u8> {
        let mut raw = Vec::with_capacity((self.w * 3 + 1) * self.h);
        for y in 0..self.h {
            raw.push(0);
            for x in 0..self.w {
                raw.extend_from_slice(&self.px[y * self.w + x]);
            }
        }
        // zlib stream with stored blocks
        let mut z = vec![0x78, 0x01];
        let mut chunks = raw.chunks(65535).peekable();
        if chunks.peek().is_none() {
            z.extend_from_slice(&[1, 0, 0, 0xff, 0xff]);
        }
        while let Some(ch) = chunks.next() {
            let last = chunks.peek().is_none();
            z.push(last as u8);
            let n = ch.len() as u16;
            z.extend_from_slice(&n.to_le_bytes());
            z.extend_from_slice(&(!n).to_le_bytes());
            z.extend_from_slice(ch);
        }
        let (mut a, mut b) = (1u32, 0u32);
        for &x in &raw {
            a = (a + x as u32) % 65521;
            b = (b + a) % 65521;
        }
        z.extend_from_slice(&((b << 16) | a).to_be_bytes());
        let mut out = vec![0x89, b'P', b'N', b'G', 0x0D, 0x0A, 0x1A, 0x0A];
        let mut chunk = |ty: &[u8], data: &[u8]| {
            out.extend_from_slice(&(data.len() as u32).to_be_bytes());
            let mut c = ty.to_vec();
            c.extend_from_slice(data);
            out.extend_from_slice(&c);
            out.extend_from_slice(&crc32(&c).to_be_bytes());
        };
        let mut ihdr = Vec::new();
        ihdr.extend_from_slice(&(self.w as u32).to_be_bytes());
        ihdr.extend_from_slice(&(self.h as u32).to_be_bytes());
        ihdr.extend_from_slice(&[8, 2, 0, 0, 0]);
        chunk(b"IHDR", &ihdr);
        chunk(b"IDAT", &z);
        chunk(b"IEND", &[]);
        out
    }
}

/// A perceptually ordered ramp (dark blue → teal → yellow), `t` in [0, 1].
pub fn ramp(t: f64) -> [u8; 3] {
    const STOPS: [[f64; 3]; 5] = [
        [13.0, 8.0, 135.0],
        [84.0, 2.0, 163.0],
        [33.0, 145.0, 140.0],
        [122.0, 209.0, 81.0],
        [253.0, 231.0, 37.0],
    ];
    let t = t.clamp(0.0, 1.0) * 4.0;
    let i = (t.floor() as usize).min(3);
    let f = t - i as f64;
    let mut c = [0u8; 3];
    for k in 0..3 {
        c[k] = (STOPS[i][k] * (1.0 - f) + STOPS[i + 1][k] * f).round() as u8;
    }
    c
}

pub const BG: [u8; 3] = [16, 16, 20];
pub const ORIENT: [[u8; 3]; 3] = [[230, 85, 70], [90, 200, 90], [80, 140, 240]];
pub const DEAD_SITE: [u8; 3] = [60, 60, 70];

/// Projection along a coordinate axis: pixel = number of live cells on the line,
/// one pixel per doubled unit (× `scale`).
pub fn png_axis_projection(cells: &[P3], axis: usize, scale: usize) -> Image {
    let (u, v) = match axis {
        0 => (1, 2),
        1 => (0, 2),
        _ => (0, 1),
    };
    let mut cnt: HashMap<(i64, i64), u32> = HashMap::new();
    for p in cells {
        *cnt.entry((p[u], p[v])).or_default() += 1;
    }
    let (lo, hi) = bounds2(cnt.keys().copied());
    let (w, h) = (((hi.0 - lo.0 + 3) as usize) * scale, ((hi.1 - lo.1 + 3) as usize) * scale);
    let mut img = Image::new(w.max(1), h.max(1), BG);
    let max = cnt.values().copied().max().unwrap_or(1) as f64;
    for (&(a, b), &n) in &cnt {
        let c = ramp((n as f64 / max).sqrt());
        let (x, y) = ((a - lo.0 + 1) as i64 * scale as i64, (hi.1 - b + 1) as i64 * scale as i64);
        img.rect(x, y, x + scale as i64, y + scale as i64, c);
    }
    img
}

fn bounds2(it: impl Iterator<Item = (i64, i64)>) -> ((i64, i64), (i64, i64)) {
    let mut lo = (i64::MAX, i64::MAX);
    let mut hi = (i64::MIN, i64::MIN);
    for (a, b) in it {
        lo = (lo.0.min(a), lo.1.min(b));
        hi = (hi.0.max(a), hi.1.max(b));
    }
    if lo.0 > hi.0 {
        ((0, 0), (0, 0))
    } else {
        (lo, hi)
    }
}

/// True planar position of a cell projected along diagonal `d` (unit = cell spacing).
fn plane_pos(p: P3, d: usize) -> (f64, f64) {
    let q = to_d111(p, d);
    (q[0] as f64 + q[1] as f64 / 2.0, q[1] as f64 * 0.866_025_4)
}

/// Projection along body diagonal `d`: each site coloured by the number of live cells
/// projecting onto it (all layers overlaid).
pub fn png_diag_projection(cells: &[P3], d: usize, scale: f64) -> Image {
    // cells on one line along [111] share (x'-z', y'-z'); planar position in the orthonormal
    // basis (1,-1,0)/√2, (1,1,-2)/√6 of the plane, in units of the in-layer cell spacing (√2)
    let mut cnt: HashMap<(i64, i64), (u32, P3)> = HashMap::new();
    for &p in cells {
        let q = to_d111(p, d);
        cnt.entry((q[0] - q[2], q[1] - q[2])).or_insert((0, q)).0 += 1;
    }
    let max = cnt.values().map(|v| v.0).max().unwrap_or(1) as f64;
    let pts: Vec<(f64, f64, u32)> = cnt
        .values()
        .map(|&(n, q)| {
            let (x, y, z) = (q[0] as f64, q[1] as f64, q[2] as f64);
            ((x - y) / 2.0, (x + y - 2.0 * z) / 12f64.sqrt(), n)
        })
        .collect();
    canvas_points(&pts, scale, 0.22, |n| ramp((n as f64 / max).sqrt()))
}

fn canvas_points(pts: &[(f64, f64, u32)], scale: f64, radius: f64, col: impl Fn(u32) -> [u8; 3]) -> Image {
    let (mut x0, mut x1, mut y0, mut y1) = (f64::MAX, f64::MIN, f64::MAX, f64::MIN);
    for &(x, y, _) in pts {
        x0 = x0.min(x);
        x1 = x1.max(x);
        y0 = y0.min(y);
        y1 = y1.max(y);
    }
    if pts.is_empty() {
        return Image::new(8, 8, BG);
    }
    let m = 1.0;
    let w = ((x1 - x0 + 2.0 * m) * scale).ceil() as usize;
    let h = ((y1 - y0 + 2.0 * m) * scale).ceil() as usize;
    let mut img = Image::new(w.max(1), h.max(1), BG);
    for &(x, y, n) in pts {
        img.disc((x - x0 + m) * scale, (y - y0 + m) * scale, radius * scale, col(n));
        let _ = y1;
    }
    img
}

/// Layers `s_lo..=s_hi` along `d` (one layer if equal): kagome sites of the frame drawn as
/// dots, live cells coloured by orientation (one layer) or by layer (a slab).
pub fn png_layers(cells: &[P3], d: usize, s_lo: i64, s_hi: i64, scale: f64) -> Image {
    let sel: Vec<P3> = cells.iter().copied().filter(|&p| (s_lo..=s_hi).contains(&layer(p, d))).collect();
    let live: HashSet<P3> = sel.iter().copied().collect();
    let Some(fr) = Frame::of(&sel, d, 1) else { return Image::new(8, 8, BG) };
    let mut pts = Vec::new();
    let nl = ((s_hi - s_lo) / 2 + 1).max(1);
    for s in (s_lo..=s_hi).step_by(2) {
        for row in fr.r0..=fr.r1 {
            for col in fr.c0..=fr.c1 {
                if let Some(p) = kagome_cell(col, row, s, d) {
                    let (x, y) = plane_pos(p, d);
                    let code = if live.contains(&p) {
                        if nl == 1 {
                            1 + cell_axis(p).unwrap() as u32
                        } else {
                            10 + ((s - s_lo) / 2) as u32
                        }
                    } else {
                        0
                    };
                    if code > 0 || s == s_lo {
                        pts.push((x, y, code));
                    }
                }
            }
        }
    }
    pts.sort_by_key(|p| p.2); // live on top
    canvas_points(&pts, scale, 0.32, |c| match c {
        0 => DEAD_SITE,
        1..=3 => ORIENT[(c - 1) as usize],
        _ => ramp((c - 10) as f64 / (nl - 1).max(1) as f64),
    })
}

/// Axis-aligned slice as an image: faces cutting the plane as segments, coloured by
/// orientation; faces lying in the plane as squares.
pub fn png_slice(cells: &[P3], axis: usize, c: i64, scale: usize) -> Image {
    let (u, v) = match axis {
        0 => (1, 2),
        1 => (0, 2),
        _ => (0, 1),
    };
    let sel: Vec<P3> = cells.iter().copied().filter(|p| p[axis] == c).collect();
    let (lo, hi) = bounds2(sel.iter().map(|p| (p[u], p[v])));
    let s = scale as i64;
    let (w, h) = ((hi.0 - lo.0 + 4) * s, (hi.1 - lo.1 + 4) * s);
    let mut img = Image::new(w.max(1) as usize, h.max(1) as usize, BG);
    for p in sel {
        let ax = cell_axis(p).unwrap();
        let (x, y) = ((p[u] - lo.0 + 2) * s, (hi.1 - p[v] + 2) * s);
        let col = ORIENT[ax];
        if ax == axis {
            img.rect(x - s + 1, y - s + 1, x + s, y + s, col);
        } else if ax == u {
            img.rect(x - s / 6, y - s, x + s / 6 + 1, y + s, col);
        } else {
            img.rect(x - s, y - s / 6, x + s, y + s / 6 + 1, col);
        }
    }
    img
}

/// Kymograph image: `rows[t] = (gen, counts per layer)` for one axis; `deaths[(layer
/// column)] = gen` marks irreversible deaths (red tick at that time). Time runs downwards,
/// downsampled to at most `max_h` rows (bucket means).
pub fn png_kymo(rows: &[(u64, Vec<f64>)], deaths: &[(usize, u64)], cell_w: usize, max_h: usize) -> Image {
    if rows.is_empty() {
        return Image::new(8, 8, BG);
    }
    let ncol = rows[0].1.len();
    let nb = rows.len().min(max_h.max(1));
    let mut buckets = vec![vec![0f64; ncol]; nb];
    let mut bgen = vec![(u64::MAX, 0u64); nb];
    let mut bn = vec![0usize; nb];
    for (t, (g, c)) in rows.iter().enumerate() {
        let b = t * nb / rows.len();
        for k in 0..ncol {
            buckets[b][k] += c.get(k).copied().unwrap_or(0.0);
        }
        bgen[b] = (bgen[b].0.min(*g), bgen[b].1.max(*g));
        bn[b] += 1;
    }
    let mut max = 0f64;
    for (b, row) in buckets.iter_mut().enumerate() {
        for x in row.iter_mut() {
            *x /= bn[b].max(1) as f64;
            max = max.max(*x);
        }
    }
    let mut img = Image::new(ncol * cell_w, nb, BG);
    for (b, row) in buckets.iter().enumerate() {
        for (k, &x) in row.iter().enumerate() {
            if x > 0.0 {
                let c = ramp((x / max.max(1e-9)).sqrt());
                img.rect((k * cell_w) as i64, b as i64, ((k + 1) * cell_w) as i64, b as i64 + 1, c);
            }
        }
    }
    for &(k, g) in deaths {
        if let Some(b) = bgen.iter().position(|&(g0, g1)| g >= g0 && g <= g1) {
            img.rect((k * cell_w) as i64, b as i64 - 1, ((k + 1) * cell_w) as i64, b as i64 + 2, [255, 40, 40]);
        }
    }
    img
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn kagome_roundtrip() {
        for d in 0..4 {
            for p in crate::seeds::fill_span([-5; 3], [5; 3]) {
                let (c, r) = kagome_pos(p, d);
                assert_eq!(kagome_cell(c, r, layer(p, d), d), Some(p));
            }
        }
    }
    #[test]
    fn png_header() {
        let img = Image::new(3, 2, [1, 2, 3]);
        let b = img.png();
        assert_eq!(&b[1..4], b"PNG");
        assert_eq!(crc32(b"IEND"), 0xAE42_6082);
    }
}
