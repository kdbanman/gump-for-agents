// GPU statistics: a reduction over the state atlas, read back asynchronously.
//
// Reduced quantities (doubled coordinates, array frame):
//   per-orientation populations; max of +-x, +-y, +-z (axis-aligned bounding box);
//   max of +-s for the 4 body diagonals d, s = d.p (the diagonal hull, docs/AUTOMATON.md §3).
//   and, for each of those 8 diagonal extremes, the number of live cells *on* it: the population
//   of the outermost layer of each of the 8 hull faces (a max-with-count reduction, exact).
// Maxima are stored as (v + 32768) in 16-bit halves, 0 meaning "no live cell".
// Five RGBA32UI targets (MRT); WebGL2 guarantees 4 draw buffers, every real implementation has 8.
//
// Two ways to use it:
//  - sampled: start(tex, tag) / poll()  — one reduction, read back when ready;
//  - every generation: record(tex, gen) after each step writes the result into slot gen % RING
//    of a ring texture; flush() queues an async readback of the slots written since the last
//    flush; pollRing() returns { gen, stats } for every generation, in order. Nothing is missed
//    as long as fewer than RING generations are recorded between flushes.
import { program, FULLSCREEN_VS, intTexture, framebuffer, rawPassState } from './util.js';
import { layoutGLSL } from './layout.js';
import { Readback } from './readback.js';

const B0 = 8;      // first-pass block (texels per side)
const BMAX = 16;   // a later pass reduces at most BMAX x BMAX per fragment; the last pass all that is left
export const RING = 4096;
const NATT = 5;            // render targets per reduction level
const W = 4 * NATT;        // uints per reduced texel

const COMMON = `
uint popc(uint v) {
  v = v - ((v >> 1) & 0x55555555u);
  v = (v & 0x33333333u) + ((v >> 2) & 0x33333333u);
  v = (v + (v >> 4)) & 0x0f0f0f0fu;
  v = v + (v >> 8); v = v + (v >> 16);
  return v & 0x3fu;
}
int msb(uint v) {
  int r = 0;
  if (v >= 0x10000u) { v >>= 16; r += 16; }
  if (v >= 0x100u) { v >>= 8; r += 8; }
  if (v >= 0x10u) { v >>= 4; r += 4; }
  if (v >= 0x4u) { v >>= 2; r += 2; }
  if (v >= 0x2u) { r += 1; }
  return r;
}
uint maxPacked(uint a, uint b) { return max(a & 0xffff0000u, b & 0xffff0000u) | max(a & 0xffffu, b & 0xffffu); }
// (max, count of cells attaining it) pairs
void maxCount(inout uint m, inout uint c, uint m2, uint c2) {
  if (m2 > m) { m = m2; c = c2; } else if (m2 == m) c += c2;
}
`;

function firstFS(L) {
  return `#version 300 es
precision highp float; precision highp int; precision highp usampler2D;
${layoutGLSL(L)}
${COMMON}
uniform usampler2D S;
uniform ivec2 inSize;
layout(location = 0) out uvec4 o0;
layout(location = 1) out uvec4 o1;
layout(location = 2) out uvec4 o2;
layout(location = 3) out uvec4 o3;
layout(location = 4) out uvec4 o4;
void main() {
  ivec2 base = ivec2(gl_FragCoord.xy) * ${B0};
  uint fm[8], fc[8];              // the 8 diagonal extremes (encoded) and the cells on them
  for (int q = 0; q < 8; q++) { fm[q] = 0u; fc[q] = 0u; }
  uvec3 cnt = uvec3(0u);
  int m[14];
  for (int q = 0; q < 14; q++) m[q] = -32768;
  for (int dy = 0; dy < ${B0}; dy++) for (int dx = 0; dx < ${B0}; dx++) {
    ivec2 p = base + ivec2(dx, dy);
    if (p.x >= inSize.x || p.y >= inSize.y) continue;
    uvec4 t = texelFetch(S, p, 0);
    if ((t.x | t.y | t.z) == 0u) continue;
    int tx = p.x / WN, ty = p.y / NY;
    int w = p.x - tx * WN, j = p.y - ty * NY, k = ty * TILESX + tx;
    for (int a = 0; a < 3; a++) {
      uint v = a == 0 ? t.x : (a == 1 ? t.y : t.z);
      if (v == 0u) continue;
      cnt[a] += popc(v);
      int imax = msb(v) * WN + w, imin = msb(v & (~v + 1u)) * WN + w;
      ivec3 e = ivec3(a == 0 ? 1 : 0, a == 1 ? 1 : 0, a == 2 ? 1 : 0);
      ivec3 hi = ivec3(2 * imax, 2 * j, 2 * k) + e;
      ivec3 lo = ivec3(2 * imin, 2 * j, 2 * k) + e;
      m[0] = max(m[0], hi.x); m[1] = max(m[1], hi.y); m[2] = max(m[2], hi.z);
      m[3] = max(m[3], -lo.x); m[4] = max(m[4], -lo.y); m[5] = max(m[5], -lo.z);
      // d = (1,1,1), (1,1,-1), (1,-1,1), (-1,1,1); max of d.p uses hi.x when d.x > 0.
      m[6]  = max(m[6],   hi.x + hi.y + hi.z);   m[10] = max(m[10], -(lo.x + lo.y + lo.z));
      m[7]  = max(m[7],   hi.x + hi.y - hi.z);   m[11] = max(m[11], -(lo.x + lo.y - lo.z));
      m[8]  = max(m[8],   hi.x - hi.y + hi.z);   m[12] = max(m[12], -(lo.x - lo.y + lo.z));
      m[9]  = max(m[9],  -lo.x + lo.y + lo.z);   m[13] = max(m[13], -(-hi.x + hi.y + hi.z));
      // within one word s = d.p is strictly monotone in the lane, so exactly one cell attains each extreme
      int sx[8] = int[8](hi.x + hi.y + hi.z, hi.x + hi.y - hi.z, hi.x - hi.y + hi.z, -lo.x + lo.y + lo.z,
                         -(lo.x + lo.y + lo.z), -(lo.x + lo.y - lo.z), -(lo.x - lo.y + lo.z), -(-hi.x + hi.y + hi.z));
      for (int q = 0; q < 8; q++) { uint ev = uint(sx[q] + 32768); maxCount(fm[q], fc[q], ev, 1u); }
    }
  }
  uint e[14];
  for (int q = 0; q < 14; q++) e[q] = uint(m[q] + 32768);
  o0 = uvec4(cnt, (e[0] << 16) | e[1]);
  o1 = uvec4((e[2] << 16) | e[3], (e[4] << 16) | e[5], (e[6] << 16) | e[7], (e[8] << 16) | e[9]);
  o2 = uvec4((e[10] << 16) | e[11], (e[12] << 16) | e[13], fc[0], fc[1]);
  o3 = uvec4(fc[2], fc[3], fc[4], fc[5]);
  o4 = uvec4(fc[6], fc[7], 0u, 0u);
}`;
}

const REDUCE_FS = `#version 300 es
precision highp float; precision highp int; precision highp usampler2D;
${COMMON}
uniform usampler2D T0, T1, T2, T3, T4;
uniform ivec2 inSize, block, outOrigin;
layout(location = 0) out uvec4 o0;
layout(location = 1) out uvec4 o1;
layout(location = 2) out uvec4 o2;
layout(location = 3) out uvec4 o3;
layout(location = 4) out uvec4 o4;
uint hiH(uint v) { return v >> 16; }
uint loH(uint v) { return v & 0xffffu; }
void main() {
  ivec2 base = (ivec2(gl_FragCoord.xy) - outOrigin) * block;
  uvec4 a0 = uvec4(0u), a1 = uvec4(0u);
  uint fm[8], fc[8];
  for (int q = 0; q < 8; q++) { fm[q] = 0u; fc[q] = 0u; }
  for (int dy = 0; dy < block.y; dy++) for (int dx = 0; dx < block.x; dx++) {
    ivec2 p = base + ivec2(dx, dy);
    if (p.x >= inSize.x || p.y >= inSize.y) continue;
    uvec4 t0 = texelFetch(T0, p, 0), t1 = texelFetch(T1, p, 0), t2 = texelFetch(T2, p, 0), t3 = texelFetch(T3, p, 0), t4 = texelFetch(T4, p, 0);
    a0 = uvec4(a0.xyz + t0.xyz, maxPacked(a0.w, t0.w));
    a1 = uvec4(maxPacked(a1.x, t1.x), maxPacked(a1.y, t1.y), maxPacked(a1.z, t1.z), maxPacked(a1.w, t1.w));
    // extremes with counts: +s maxima e6..e9 live in t1.z/t1.w, -s maxima e10..e13 in t2.x/t2.y
    uint m[8] = uint[8](hiH(t1.z), loH(t1.z), hiH(t1.w), loH(t1.w), hiH(t2.x), loH(t2.x), hiH(t2.y), loH(t2.y));
    uint c[8] = uint[8](t2.z, t2.w, t3.x, t3.y, t3.z, t3.w, t4.x, t4.y);
    for (int q = 0; q < 8; q++) maxCount(fm[q], fc[q], m[q], c[q]);
  }
  o0 = a0;
  o1 = uvec4(a1.xy, (fm[0] << 16) | fm[1], (fm[2] << 16) | fm[3]);
  o2 = uvec4((fm[4] << 16) | fm[5], (fm[6] << 16) | fm[7], fc[0], fc[1]);
  o3 = uvec4(fc[2], fc[3], fc[4], fc[5]);
  o4 = uvec4(fc[6], fc[7], 0u, 0u);
}`;

// Decode one reduced texel (W uints: attachments 0..NATT-1 x RGBA) at offset `o` of `u`.
export function decodeStats(u, o = 0) {
  const word = (q) => u[o + 3 + (q >> 1)];
  const f = (q) => { const w = word(q); const h = (q & 1) ? (w & 0xffff) : (w >>> 16); return h ? h - 32768 : null; };
  const count = [u[o], u[o + 1], u[o + 2]];
  const pop = count[0] + count[1] + count[2];
  if (!pop) return { pop, count, lo: null, hi: null, loS: null, hiS: null, faceHi: null, faceLo: null };
  const m = Array.from({ length: 14 }, (_, q) => f(q));
  const fc = [u[o + 10], u[o + 11], u[o + 12], u[o + 13], u[o + 14], u[o + 15], u[o + 16], u[o + 17]];
  return {
    pop, count,
    hi: [m[0], m[1], m[2]], lo: [-m[3], -m[4], -m[5]],
    hiS: [m[6], m[7], m[8], m[9]], loS: [-m[10], -m[11], -m[12], -m[13]],
    // live cells on the outermost layer of each hull face: s = hiS[n] and s = loS[n]
    faceHi: fc.slice(0, 4), faceLo: fc.slice(4, 8),
  };
}
// The uints of a texel as read back are attachment-major; regroup per texel.
function regroup(data, n) {
  const out = new Uint32Array(W * n);
  for (let i = 0; i < n; i++) for (let a = 0; a < NATT; a++) for (let c = 0; c < 4; c++)
    out[W * i + 4 * a + c] = data[4 * (a * n + i) + c];
  return out;
}
const ATT = Array.from({ length: NATT }, (_, i) => i);

export class Stats {
  constructor(gl, layout) {
    if (gl.getParameter(gl.MAX_DRAW_BUFFERS) < NATT || gl.getParameter(gl.MAX_COLOR_ATTACHMENTS) < NATT)
      throw new Error(`statistics need ${NATT} draw buffers; this WebGL2 has ${gl.getParameter(gl.MAX_DRAW_BUFFERS)}`);
    this.gl = gl;
    this.layout = layout;
    this.first = program(gl, FULLSCREEN_VS, firstFS(layout));
    this.reduce = program(gl, FULLSCREEN_VS, REDUCE_FS);
    this.vao = gl.createVertexArray();
    this.levels = [];
    let w = Math.ceil(layout.width / B0), h = Math.ceil(layout.height / B0);
    this.levels.push(this._level(w, h, [B0, B0]));
    while (w > 1 || h > 1) {
      const last = w <= BMAX && h <= BMAX;
      const block = last ? [w, h] : [Math.min(BMAX, w), Math.min(BMAX, h)];
      w = Math.ceil(w / block[0]); h = Math.ceil(h / block[1]);
      this.levels.push(this._level(w, h, block));
    }
    this.ringTex = ATT.map(() => intTexture(gl, gl.RGBA32UI, RING, 1));
    this.ringFb = framebuffer(gl, this.ringTex);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    this.rb = new Readback(gl);
    this.ringFrom = null;     // first generation recorded but not yet flushed
    this.ringTo = null;       // one past the last recorded generation
    this.sampled = null;      // pending sampled job
  }
  _level(w, h, block) {
    const tex = ATT.map(() => intTexture(this.gl, this.gl.RGBA32UI, w, h));
    return { w, h, block, tex, fb: framebuffer(this.gl, tex) };
  }
  get passes() { return this.levels.length; }

  // Run the reduction; the final 1x1 result goes to `target` = { fb, x } (default: last level).
  _reduce(stateTex, target) {
    const gl = this.gl;
    rawPassState(gl);
    gl.bindVertexArray(this.vao);
    let prev = null;
    this.levels.forEach((lv, li) => {
      const toRing = target && li === this.levels.length - 1;
      gl.bindFramebuffer(gl.FRAMEBUFFER, toRing ? target.fb : lv.fb);
      gl.viewport(toRing ? target.x : 0, 0, lv.w, lv.h);
      if (!prev) {
        gl.useProgram(this.first.program);
        gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, stateTex);
        gl.uniform1i(this.first.uniforms.S, 0);
        gl.uniform2i(this.first.uniforms.inSize, this.layout.width, this.layout.height);
      } else {
        const u = this.reduce.uniforms;
        gl.useProgram(this.reduce.program);
        prev.tex.forEach((t, i) => { gl.activeTexture(gl.TEXTURE0 + i); gl.bindTexture(gl.TEXTURE_2D, t); });
        ATT.forEach(i => gl.uniform1i(u['T' + i], i));
        gl.uniform2i(u.inSize, prev.w, prev.h);
        gl.uniform2i(u.block, lv.block[0], lv.block[1]);
        gl.uniform2i(u.outOrigin, toRing ? target.x : 0, 0);
      }
      gl.drawArrays(gl.TRIANGLES, 0, 3);
      prev = lv;
    });
    for (let i = NATT - 1; i >= 0; i--) { gl.activeTexture(gl.TEXTURE0 + i); gl.bindTexture(gl.TEXTURE_2D, null); }
    gl.bindVertexArray(null);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
  }

  // A one-level-only reduction needs the first pass to write straight into the ring.
  _single() { return this.levels.length === 1; }

  // Blocking (tests, single steps in tests): decoded stats now.
  computeSync(stateTex) {
    const gl = this.gl;
    this._reduce(stateTex);
    const lv = this.levels[this.levels.length - 1];
    const u = new Uint32Array(W);
    gl.bindBuffer(gl.PIXEL_PACK_BUFFER, null);
    gl.bindFramebuffer(gl.FRAMEBUFFER, lv.fb);
    for (let i = 0; i < NATT; i++) { gl.readBuffer(gl.COLOR_ATTACHMENT0 + i); gl.readPixels(0, 0, 1, 1, gl.RGBA_INTEGER, gl.UNSIGNED_INT, u, 4 * i); }
    gl.readBuffer(gl.COLOR_ATTACHMENT0);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    return decodeStats(u);
  }

  // ---- sampled
  start(stateTex, tag) {
    if (this.sampled) return false;
    this._reduce(stateTex);
    const lv = this.levels[this.levels.length - 1];
    this.sampled = this.rb.start(ATT.map(a => ({ fb: lv.fb, attachment: a, x: 0, y: 0, w: 1, h: 1 })), { kind: 'sample', tag });
    return true;
  }
  get pending() { return this.sampled; }

  // ---- every generation
  record(stateTex, gen) {
    if (this._single()) {                       // tiny atlas: reduce normally, copy the texel over
      this._reduce(stateTex);
      this._copyToRing(gen % RING);
    } else {
      this._reduce(stateTex, { fb: this.ringFb, x: gen % RING });
    }
    if (this.ringFrom === null) this.ringFrom = gen;
    this.ringTo = gen + 1;
  }
  _copyToRing(slot) {
    const gl = this.gl, lv = this.levels[0];
    gl.bindFramebuffer(gl.READ_FRAMEBUFFER, lv.fb);
    for (let a = 0; a < NATT; a++) {
      gl.readBuffer(gl.COLOR_ATTACHMENT0 + a);
      gl.bindTexture(gl.TEXTURE_2D, this.ringTex[a]);
      gl.copyTexSubImage2D(gl.TEXTURE_2D, 0, slot, 0, 0, 0, 1, 1);
    }
    gl.readBuffer(gl.COLOR_ATTACHMENT0);
    gl.bindTexture(gl.TEXTURE_2D, null);
    gl.bindFramebuffer(gl.READ_FRAMEBUFFER, null);
  }
  get unflushed() { return this.ringFrom === null ? 0 : this.ringTo - this.ringFrom; }
  flush() {
    if (this.ringFrom === null) return;
    const g0 = this.ringFrom, n = this.ringTo - this.ringFrom;
    if (n > RING) throw new Error('stats ring overrun');
    const s0 = g0 % RING, n1 = Math.min(n, RING - s0), n2 = n - n1;
    const reads = [];
    for (const [x, w] of [[s0, n1], [0, n2]]) if (w > 0) for (const a of ATT) reads.push({ fb: this.ringFb, attachment: a, x, y: 0, w, h: 1 });
    this.rb.start(reads, { kind: 'ring', g0, n1, n2 });
    this.ringFrom = null;
  }

  // Returns { samples: [{gen, stats}] (every recorded generation, in order), sample: {tag, stats} | null }
  poll() {
    const out = { samples: [], sample: null };
    for (const job of this.rb.poll()) {
      if (job.tag.kind === 'sample') { out.sample = { tag: job.tag.tag, stats: decodeStats(regroup(job.data, 1)) }; this.sampled = null; continue; }
      const { g0, n1, n2 } = job.tag;
      let off = 0, g = g0;
      for (const n of [n1, n2]) {
        if (!n) continue;
        const u = regroup(job.data.subarray(off, off + W * n), n);
        for (let i = 0; i < n; i++) out.samples.push({ gen: g++, stats: decodeStats(u, W * i) });
        off += W * n;
      }
    }
    return out;
  }

  dispose() {
    const gl = this.gl;
    this.rb.dispose();
    for (const lv of this.levels) { lv.tex.forEach(t => gl.deleteTexture(t)); gl.deleteFramebuffer(lv.fb); }
    this.ringTex.forEach(t => gl.deleteTexture(t)); gl.deleteFramebuffer(this.ringFb);
    gl.deleteProgram(this.first.program); gl.deleteProgram(this.reduce.program);
    gl.deleteVertexArray(this.vao);
  }
}
