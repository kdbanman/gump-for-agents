//! Snapshot format (`.gump`), version 1.
//!
//! ```text
//! GUMP-SNAPSHOT 1
//! boundary open|torus
//! dims NX NY NZ            box size in cubes
//! origin OX OY OZ          cube (i,j,k) of the box is absolute cube (i+OX, j+OY, k+OZ)
//! rule B45/S345
//! gen G
//! population P
//! encoding rle0
//! bytes N
//!                          (one empty line ends the header)
//! <N payload bytes>
//! ```
//! Local cell `(a, i, j, k)` (face on the `+a` side of cube `(i,j,k)`) has doubled
//! coordinates `2(i+OX, j+OY, k+OZ) + e_a`. The state is the bitmap with bit index
//! `t = ((a·NZ + k)·NY + j)·NX + i`, packed LSB-first into `ceil(3·NX·NY·NZ / 8)` bytes.
//! `rle0` encodes that byte string as repeated records
//! `varint(run of zero bytes) varint(literal count) literal bytes…` (LEB128 varints)
//! until the full length is produced. Unknown header keys are ignored by readers.

use crate::fast::BitSim;
use crate::lattice::{Boundary, Geometry, P3};
use crate::rule::Rule;

pub struct Snapshot {
    pub geo: Geometry,
    pub rule: Rule,
    pub gen: u64,
    pub bitmap: Vec<u8>,
}

fn put_varint(out: &mut Vec<u8>, mut v: u64) {
    loop {
        let b = (v & 0x7f) as u8;
        v >>= 7;
        if v == 0 {
            out.push(b);
            return;
        }
        out.push(b | 0x80);
    }
}

fn get_varint(data: &[u8], pos: &mut usize) -> Result<u64, String> {
    let mut v = 0u64;
    let mut shift = 0;
    loop {
        let b = *data.get(*pos).ok_or("truncated varint")?;
        *pos += 1;
        v |= ((b & 0x7f) as u64) << shift;
        if b & 0x80 == 0 {
            return Ok(v);
        }
        shift += 7;
        if shift > 63 {
            return Err("bad varint".into());
        }
    }
}

pub fn rle0_encode(bytes: &[u8]) -> Vec<u8> {
    let mut out = Vec::new();
    let mut i = 0;
    while i < bytes.len() {
        let z0 = i;
        while i < bytes.len() && bytes[i] == 0 {
            i += 1;
        }
        let zeros = i - z0;
        let l0 = i;
        // literal run: stop at a run of >= 3 zero bytes (or end)
        while i < bytes.len() {
            if bytes[i] == 0 {
                let mut r = i;
                while r < bytes.len() && bytes[r] == 0 {
                    r += 1;
                }
                if r - i >= 3 || r == bytes.len() {
                    break;
                }
                i = r; // short zero run stays inside the literal
            } else {
                i += 1;
            }
        }
        put_varint(&mut out, zeros as u64);
        put_varint(&mut out, (i - l0) as u64);
        out.extend_from_slice(&bytes[l0..i]);
    }
    out
}

pub fn rle0_decode(data: &[u8], len: usize) -> Result<Vec<u8>, String> {
    let mut out = Vec::with_capacity(len);
    let mut pos = 0;
    while out.len() < len {
        let z = get_varint(data, &mut pos)? as usize;
        let l = get_varint(data, &mut pos)? as usize;
        if out.len() + z + l > len || pos + l > data.len() {
            return Err("rle0 payload overruns the bitmap".into());
        }
        out.resize(out.len() + z, 0);
        out.extend_from_slice(&data[pos..pos + l]);
        pos += l;
    }
    Ok(out)
}

impl Snapshot {
    pub fn from_sim(sim: &BitSim) -> Snapshot {
        let geo = sim.geometry().clone();
        let n = geo.n;
        let total = geo.cells();
        let mut bitmap = vec![0u8; total.div_ceil(8)];
        sim.for_each_live(|a, i, j, k| {
            let t = ((a * n[2] + k) * n[1] + j) * n[0] + i;
            bitmap[t / 8] |= 1 << (t % 8);
        });
        Snapshot { geo, rule: sim.rule(), gen: sim.generation(), bitmap }
    }

    pub fn population(&self) -> u64 {
        self.bitmap.iter().map(|b| b.count_ones() as u64).sum()
    }

    pub fn cells(&self) -> Vec<P3> {
        let n = self.geo.n;
        let mut v = Vec::new();
        for (byte_i, &byte) in self.bitmap.iter().enumerate() {
            let mut b = byte;
            while b != 0 {
                let t = byte_i * 8 + b.trailing_zeros() as usize;
                b &= b - 1;
                let i = t % n[0];
                let j = (t / n[0]) % n[1];
                let k = (t / (n[0] * n[1])) % n[2];
                let a = t / (n[0] * n[1] * n[2]);
                v.push(self.geo.to_doubled(a, [i, j, k]));
            }
        }
        v.sort();
        v
    }

    pub fn encode(&self) -> Vec<u8> {
        let payload = rle0_encode(&self.bitmap);
        let g = &self.geo;
        let mut out = format!(
            "GUMP-SNAPSHOT 1\nboundary {}\ndims {} {} {}\norigin {} {} {}\nrule {}\ngen {}\npopulation {}\nencoding rle0\nbytes {}\n\n",
            g.boundary.name(),
            g.n[0], g.n[1], g.n[2],
            g.origin[0], g.origin[1], g.origin[2],
            self.rule,
            self.gen,
            self.population(),
            payload.len()
        )
        .into_bytes();
        out.extend_from_slice(&payload);
        out
    }

    pub fn decode(data: &[u8]) -> Result<Snapshot, String> {
        // header ends at the first "\n\n"
        let end = data.windows(2).position(|w| w == b"\n\n").ok_or("snapshot: no header terminator")?;
        let header = std::str::from_utf8(&data[..end]).map_err(|_| "snapshot header not UTF-8")?;
        let mut lines = header.lines();
        if lines.next() != Some("GUMP-SNAPSHOT 1") {
            return Err("not a GUMP-SNAPSHOT 1 file".into());
        }
        let (mut boundary, mut dims, mut origin, mut rule, mut gen, mut nbytes, mut enc, mut pop) =
            (None, None, None, Rule::GUMP, 0u64, None, String::from("rle0"), None);
        let nums = |v: &str| -> Result<Vec<i64>, String> {
            v.split_whitespace().map(|t| t.parse::<i64>().map_err(|e| format!("snapshot: {e}"))).collect()
        };
        for l in lines {
            let (k, v) = l.split_once(' ').unwrap_or((l, ""));
            match k {
                "boundary" => {
                    boundary = Some(match v {
                        "open" => Boundary::Open,
                        "torus" => Boundary::Torus,
                        _ => return Err(format!("snapshot: unknown boundary {v}")),
                    })
                }
                "dims" => dims = Some(nums(v)?),
                "origin" => origin = Some(nums(v)?),
                "rule" => rule = Rule::parse(v)?,
                "gen" => gen = v.parse().map_err(|_| "snapshot: bad gen")?,
                "bytes" => nbytes = Some(v.parse::<usize>().map_err(|_| "snapshot: bad bytes")?),
                "encoding" => enc = v.to_string(),
                "population" => pop = Some(v.parse::<u64>().map_err(|_| "snapshot: bad population")?),
                _ => {}
            }
        }
        let dims = dims.ok_or("snapshot: missing dims")?;
        let origin = origin.ok_or("snapshot: missing origin")?;
        if dims.len() != 3 || origin.len() != 3 || dims.iter().any(|&d| d < 1) {
            return Err("snapshot: bad dims/origin".into());
        }
        let geo = Geometry::new(
            [dims[0] as usize, dims[1] as usize, dims[2] as usize],
            [origin[0], origin[1], origin[2]],
            boundary.ok_or("snapshot: missing boundary")?,
        );
        let payload = &data[end + 2..];
        let nbytes = nbytes.ok_or("snapshot: missing bytes")?;
        if payload.len() < nbytes {
            return Err("snapshot: truncated payload".into());
        }
        let len = geo.cells().div_ceil(8);
        let bitmap = match enc.as_str() {
            "rle0" => rle0_decode(&payload[..nbytes], len)?,
            "raw" => {
                if nbytes != len {
                    return Err("snapshot: raw payload has wrong length".into());
                }
                payload[..nbytes].to_vec()
            }
            e => return Err(format!("snapshot: unknown encoding {e}")),
        };
        let s = Snapshot { geo, rule, gen, bitmap };
        if let Some(p) = pop {
            if p != s.population() {
                return Err(format!("snapshot: population {} in header but {} in payload", p, s.population()));
            }
        }
        Ok(s)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn rle_roundtrip() {
        let cases: Vec<Vec<u8>> = vec![
            vec![],
            vec![0; 10],
            vec![1, 2, 3],
            vec![0, 0, 5, 0, 0, 0, 0, 7, 0, 8, 0, 0],
            vec![9, 0, 0],
            vec![0, 0, 0, 1],
        ];
        for c in cases {
            assert_eq!(rle0_decode(&rle0_encode(&c), c.len()).unwrap(), c);
        }
    }
}
