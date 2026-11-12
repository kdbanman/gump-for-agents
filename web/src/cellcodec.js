// Compact URL encoding of a cell set (doubled coordinates).
//
// Short sets: "x,y,z;x,y,z;..." (the `cells=` parameter). Long sets: `cz=` = base64url of
// deflate-raw of:  'G' 1 | origin cube (3 x int16) | size in cubes (3 x uint16) |
// one byte per cube (bits 0/1/2 = X/Y/Z faces), x fastest.  Cube c owns cells 2c + e_a.

const b64u = {
  enc(bytes) { let s = ''; for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode(...bytes.subarray(i, i + 0x8000)); return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, ''); },
  dec(str) { const s = atob(str.replace(/-/g, '+').replace(/_/g, '/')); const b = new Uint8Array(s.length); for (let i = 0; i < s.length; i++) b[i] = s.charCodeAt(i); return b; },
};
async function pipe(bytes, stream) {
  const out = await new Response(new Blob([bytes]).stream().pipeThrough(stream)).arrayBuffer();
  return new Uint8Array(out);
}

const axisOf = (x, y, z) => (x & 1) ? 0 : (y & 1) ? 1 : 2;

export function cellsToText(pts) {
  const out = [];
  for (let q = 0; q < pts.length; q += 3) out.push(`${pts[q]},${pts[q + 1]},${pts[q + 2]}`);
  return out.join(';');
}

export async function encodeCells(pts) {
  if (!pts.length) return '';
  const lo = [Infinity, Infinity, Infinity], hi = [-Infinity, -Infinity, -Infinity];
  const cube = (q) => { const a = axisOf(pts[q], pts[q + 1], pts[q + 2]); return [0, 1, 2].map(t => (pts[q + t] - (t === a ? 1 : 0)) / 2); };
  for (let q = 0; q < pts.length; q += 3) { const c = cube(q); for (let t = 0; t < 3; t++) { lo[t] = Math.min(lo[t], c[t]); hi[t] = Math.max(hi[t], c[t]); } }
  const size = [0, 1, 2].map(t => hi[t] - lo[t] + 1);
  const head = new DataView(new ArrayBuffer(13));
  head.setUint8(0, 1);
  for (let t = 0; t < 3; t++) { head.setInt16(1 + 2 * t, lo[t]); head.setUint16(7 + 2 * t, size[t]); }
  const body = new Uint8Array(size[0] * size[1] * size[2]);
  for (let q = 0; q < pts.length; q += 3) {
    const c = cube(q), a = axisOf(pts[q], pts[q + 1], pts[q + 2]);
    body[(c[0] - lo[0]) + size[0] * ((c[1] - lo[1]) + size[1] * (c[2] - lo[2]))] |= 1 << a;
  }
  const raw = new Uint8Array(13 + body.length); raw.set(new Uint8Array(head.buffer)); raw.set(body, 13);
  return b64u.enc(await pipe(raw, new CompressionStream('deflate-raw')));
}

export async function decodeCells(str) {
  const raw = await pipe(b64u.dec(str), new DecompressionStream('deflate-raw'));
  const dv = new DataView(raw.buffer, raw.byteOffset, raw.byteLength);
  if (dv.getUint8(0) !== 1) throw new Error('unknown cell encoding');
  const lo = [0, 1, 2].map(t => dv.getInt16(1 + 2 * t)), size = [0, 1, 2].map(t => dv.getUint16(7 + 2 * t));
  const pts = [];
  for (let k = 0; k < size[2]; k++) for (let j = 0; j < size[1]; j++) for (let i = 0; i < size[0]; i++) {
    const v = raw[13 + i + size[0] * (j + size[1] * k)];
    if (!v) continue;
    for (let a = 0; a < 3; a++) if ((v >> a) & 1) { const p = [2 * (lo[0] + i), 2 * (lo[1] + j), 2 * (lo[2] + k)]; p[a]++; pts.push(...p); }
  }
  return Int32Array.from(pts);
}
