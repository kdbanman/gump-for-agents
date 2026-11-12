// GPU statistics: a multi-pass reduction over the state atlas followed by an *asynchronous*
// readback (readPixels into a PIXEL_PACK_BUFFER + fenceSync, polled from the frame loop), so
// gathering statistics never stalls stepping or rendering.
//
// Reduced quantities (doubled coordinates, array frame):
//   per-orientation populations; max of +-x, +-y, +-z (axis-aligned bounding box);
//   max of +-s for the 4 body diagonals d, s = d.p (the diagonal hull, docs/AUTOMATON.md §3).
// Maxima are stored as (v + 32768) in 16-bit halves, 0 meaning "no live cell".
import { program, FULLSCREEN_VS, intTexture, framebuffer, rawPassState } from './util.js';
import { layoutGLSL } from './layout.js';

const B0 = 8;   // first-pass block (texels per side)
const B = 4;    // later passes

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
void main() {
  ivec2 base = ivec2(gl_FragCoord.xy) * ${B0};
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
    }
  }
  uint e[14];
  for (int q = 0; q < 14; q++) e[q] = uint(m[q] + 32768);
  o0 = uvec4(cnt, (e[0] << 16) | e[1]);
  o1 = uvec4((e[2] << 16) | e[3], (e[4] << 16) | e[5], (e[6] << 16) | e[7], (e[8] << 16) | e[9]);
  o2 = uvec4((e[10] << 16) | e[11], (e[12] << 16) | e[13], 0u, 0u);
}`;
}

const REDUCE_FS = `#version 300 es
precision highp float; precision highp int; precision highp usampler2D;
${COMMON}
uniform usampler2D T0, T1, T2;
uniform ivec2 inSize;
layout(location = 0) out uvec4 o0;
layout(location = 1) out uvec4 o1;
layout(location = 2) out uvec4 o2;
void main() {
  ivec2 base = ivec2(gl_FragCoord.xy) * ${B};
  uvec4 a0 = uvec4(0u), a1 = uvec4(0u), a2 = uvec4(0u);
  for (int dy = 0; dy < ${B}; dy++) for (int dx = 0; dx < ${B}; dx++) {
    ivec2 p = base + ivec2(dx, dy);
    if (p.x >= inSize.x || p.y >= inSize.y) continue;
    uvec4 t0 = texelFetch(T0, p, 0), t1 = texelFetch(T1, p, 0), t2 = texelFetch(T2, p, 0);
    a0 = uvec4(a0.xyz + t0.xyz, maxPacked(a0.w, t0.w));
    a1 = uvec4(maxPacked(a1.x, t1.x), maxPacked(a1.y, t1.y), maxPacked(a1.z, t1.z), maxPacked(a1.w, t1.w));
    a2 = uvec4(maxPacked(a2.x, t2.x), maxPacked(a2.y, t2.y), 0u, 0u);
  }
  o0 = a0; o1 = a1; o2 = a2;
}`;

function decode(u) {
  const f = (q) => { const word = u[[3, 4, 5, 6, 7, 8, 9, 10][q >> 1]]; const h = (q & 1) ? (word & 0xffff) : (word >>> 16); return h ? h - 32768 : null; };
  const count = [u[0], u[1], u[2]];
  const pop = count[0] + count[1] + count[2];
  if (!pop) return { pop, count, lo: null, hi: null, loS: null, hiS: null };
  const m = Array.from({ length: 14 }, (_, q) => f(q));
  return {
    pop, count,
    hi: [m[0], m[1], m[2]], lo: [-m[3], -m[4], -m[5]],
    hiS: [m[6], m[7], m[8], m[9]], loS: [-m[10], -m[11], -m[12], -m[13]],
  };
}

export class Stats {
  constructor(gl, layout) {
    this.gl = gl;
    this.layout = layout;
    this.first = program(gl, FULLSCREEN_VS, firstFS(layout));
    this.reduce = program(gl, FULLSCREEN_VS, REDUCE_FS);
    this.vao = gl.createVertexArray();
    this.levels = [];
    let w = Math.ceil(layout.width / B0), h = Math.ceil(layout.height / B0);
    for (;;) {
      const tex = [0, 1, 2].map(() => intTexture(gl, gl.RGBA32UI, w, h));
      this.levels.push({ w, h, tex, fb: framebuffer(gl, tex) });
      if (w === 1 && h === 1) break;
      w = Math.ceil(w / B); h = Math.ceil(h / B);
    }
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    this.pending = null;   // { sync, tag }
  }

  _reduce(stateTex) {
    const gl = this.gl;
    rawPassState(gl);
    gl.bindVertexArray(this.vao);
    let prev = null;
    for (const lv of this.levels) {
      gl.bindFramebuffer(gl.FRAMEBUFFER, lv.fb);
      gl.viewport(0, 0, lv.w, lv.h);
      if (!prev) {
        gl.useProgram(this.first.program);
        gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, stateTex);
        gl.uniform1i(this.first.uniforms.S, 0);
        gl.uniform2i(this.first.uniforms.inSize, this.layout.width, this.layout.height);
      } else {
        gl.useProgram(this.reduce.program);
        prev.tex.forEach((t, i) => { gl.activeTexture(gl.TEXTURE0 + i); gl.bindTexture(gl.TEXTURE_2D, t); });
        gl.uniform1i(this.reduce.uniforms.T0, 0); gl.uniform1i(this.reduce.uniforms.T1, 1); gl.uniform1i(this.reduce.uniforms.T2, 2);
        gl.uniform2i(this.reduce.uniforms.inSize, prev.w, prev.h);
      }
      gl.drawArrays(gl.TRIANGLES, 0, 3);
      prev = lv;
    }
    for (let i = 2; i >= 0; i--) { gl.activeTexture(gl.TEXTURE0 + i); gl.bindTexture(gl.TEXTURE_2D, null); }
    gl.bindVertexArray(null);
    return prev; // the 1x1 level, still bound as framebuffer
  }

  _readTo(dst) {
    const gl = this.gl;
    for (let i = 0; i < 3; i++) {
      gl.readBuffer(gl.COLOR_ATTACHMENT0 + i);
      if (dst) gl.readPixels(0, 0, 1, 1, gl.RGBA_INTEGER, gl.UNSIGNED_INT, dst, i * 4);
      else gl.readPixels(0, 0, 1, 1, gl.RGBA_INTEGER, gl.UNSIGNED_INT, i * 16);
    }
    gl.readBuffer(gl.COLOR_ATTACHMENT0);
  }

  // Blocking variant (tests, single-step): returns decoded stats now.
  computeSync(stateTex) {
    const gl = this.gl;
    this._reduce(stateTex);
    gl.bindBuffer(gl.PIXEL_PACK_BUFFER, null);
    const u = new Uint32Array(12);
    this._readTo(u);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    return decode(u);
  }

  // Asynchronous variant: start if nothing is in flight. Returns true if started.
  start(stateTex, tag) {
    if (this.pending) return false;
    const gl = this.gl;
    this._reduce(stateTex);
    // A fresh buffer per readback: Chrome keeps a client-side shadow of READ buffers and warns
    // (and drops the shadow) if one is rewritten; buffers are tiny, so never reuse them.
    const pbo = gl.createBuffer();
    gl.bindBuffer(gl.PIXEL_PACK_BUFFER, pbo);
    gl.bufferData(gl.PIXEL_PACK_BUFFER, 48, gl.STREAM_READ);
    this._readTo(null);
    gl.bindBuffer(gl.PIXEL_PACK_BUFFER, null);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    this.pending = { sync: gl.fenceSync(gl.SYNC_GPU_COMMANDS_COMPLETE, 0), tag, pbo };
    gl.flush();
    return true;
  }

  // Non-blocking: returns { tag, stats } once the readback has landed, else null.
  poll() {
    if (!this.pending) return null;
    const gl = this.gl;
    const st = gl.getSyncParameter(this.pending.sync, gl.SYNC_STATUS);
    if (st !== gl.SIGNALED) return null;
    gl.deleteSync(this.pending.sync);
    const u = new Uint32Array(12);
    gl.bindBuffer(gl.PIXEL_PACK_BUFFER, this.pending.pbo);
    gl.getBufferSubData(gl.PIXEL_PACK_BUFFER, 0, u);
    gl.bindBuffer(gl.PIXEL_PACK_BUFFER, null);
    gl.deleteBuffer(this.pending.pbo);
    const tag = this.pending.tag;
    this.pending = null;
    return { tag, stats: decode(u) };
  }

  dispose() {
    const gl = this.gl;
    if (this.pending) { gl.deleteSync(this.pending.sync); gl.deleteBuffer(this.pending.pbo); }
    for (const lv of this.levels) { lv.tex.forEach(t => gl.deleteTexture(t)); gl.deleteFramebuffer(lv.fb); }
    gl.deleteProgram(this.first.program); gl.deleteProgram(this.reduce.program);
    gl.deleteVertexArray(this.vao);
  }
}
