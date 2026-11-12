// GPU stepper: one fragment = one texel = LANES cubes x 3 planes, advanced by one generation
// with bitwise carry-save counting. See layout.js for the storage layout.
import { program, FULLSCREEN_VS, intTexture, framebuffer, rawPassState } from './util.js';
import { makeLayout, layoutGLSL, packCells, unpackCells } from './layout.js';

function stepFS(L) {
  return `#version 300 es
precision highp float;
precision highp int;
precision highp usampler2D;
${layoutGLSL(L)}
uniform usampler2D S;
out uvec4 o;
int w, j, k;

uvec4 F(int ww, int jj, int kk) { return texelFetch(S, atlasOrigin(kk) + ivec2(ww, jj), 0); }

// Row (j+dj, k+dk): false if it lies outside a dead-outside volume.
bool rowAt(int dj, int dk, out int jj, out int kk) {
  jj = j + dj; kk = k + dk;
#if TORUS
  jj = jj < 0 ? jj + NY : (jj >= NY ? jj - NY : jj);
  kk = kk < 0 ? kk + NZ : (kk >= NZ ? kk - NZ : kk);
  return true;
#else
  return jj >= 0 && jj < NY && kk >= 0 && kk < NZ;
#endif
}
// Same i (C), i+1 (P), i-1 (M) of row (dj,dk); bit b of the result is the state of cube b*WN+w (+-1).
uvec4 C(int dj, int dk) { int jj, kk; return rowAt(dj, dk, jj, kk) ? F(w, jj, kk) : uvec4(0u); }
uvec4 P(int dj, int dk) {
  int jj, kk;
  if (!rowAt(dj, dk, jj, kk)) return uvec4(0u);
  uvec4 v = w < WN - 1 ? F(w + 1, jj, kk) : F(0, jj, kk) >> 1u;
#if TORUS
  if (w == WEND) v |= (F(0, jj, kk) & 1u) << uint(LANES - 1);
#endif
  return v;
}
uvec4 M(int dj, int dk) {
  int jj, kk;
  if (!rowAt(dj, dk, jj, kk)) return uvec4(0u);
  if (w > 0) return F(w - 1, jj, kk);
  uvec4 v = F(WN - 1, jj, kk) << 1u;
#if TORUS
  v |= (F(WEND, jj, kk) >> uint(LANES - 1)) & 1u;
#endif
  return v;
}

void fa(uvec3 a, uvec3 b, uvec3 c, out uvec3 s, out uvec3 cy) { uvec3 t = a ^ b; s = t ^ c; cy = (a & b) | (c & t); }

void main() {
  ivec2 p = ivec2(gl_FragCoord.xy);
  int tx = p.x / WN, ty = p.y / NY;
  w = p.x - tx * WN; j = p.y - ty * NY; k = ty * TILESX + tx;
  if (k >= NZ) { o = uvec4(0u); return; }

  uvec4 C00 = C(0, 0), P00 = P(0, 0), M00 = M(0, 0);
  uvec4 Cp0 = C(1, 0), Pp0 = P(1, 0), Mp0 = M(1, 0);
  uvec4 Cm0 = C(-1, 0), Pm0 = P(-1, 0), Mm0 = M(-1, 0);
  uvec4 C0p = C(0, 1), P0p = P(0, 1), M0p = M(0, 1);
  uvec4 C0m = C(0, -1), P0m = P(0, -1), M0m = M(0, -1);
  uvec4 Cpp = C(1, 1), Cpm = C(1, -1), Cmp = C(-1, 1), Cmm = C(-1, -1);

  // The 12 neighbours of the X, Y, Z cell of each cube (components x, y, z),
  // transcribed from the cube-index table in docs/AUTOMATON.md §2.
  uvec3 n0  = uvec3(Cpp.x, P0p.y, Pp0.z);
  uvec3 n1  = uvec3(Cpm.x, M0p.y, Mp0.z);
  uvec3 n2  = uvec3(Cmp.x, P0m.y, Pm0.z);
  uvec3 n3  = uvec3(Cmm.x, M0m.y, Mm0.z);
  uvec3 n4  = uvec3(C00.y, C00.z, C00.x);
  uvec3 n5  = uvec3(Cm0.y, C0m.z, M00.x);
  uvec3 n6  = uvec3(P00.y, Cp0.z, C0p.x);
  uvec3 n7  = uvec3(Pm0.y, Cpm.z, M0p.x);
  uvec3 n8  = uvec3(C00.z, C00.x, C00.y);
  uvec3 n9  = uvec3(C0m.z, M00.x, Cm0.y);
  uvec3 n10 = uvec3(P00.z, Cp0.x, C0p.y);
  uvec3 n11 = uvec3(P0m.z, Mp0.x, Cmp.y);

  // Carry-save sum of 12 one-bit inputs per lane -> 4-bit count (b3 b2 b1 b0).
  uvec3 s0, c0, s1, c1, s2, c2, s3, c3;
  fa(n0, n1, n2, s0, c0);
  fa(n3, n4, n5, s1, c1);
  fa(n6, n7, n8, s2, c2);
  fa(n9, n10, n11, s3, c3);
  uvec3 t, u, b0, v;
  fa(s0, s1, s2, t, u);
  b0 = t ^ s3; v = t & s3;                 // weight 1 done; u, v carry weight 2
  uvec3 pp, q0, rr, q1, b1, q2;
  fa(c0, c1, c2, pp, q0);
  fa(c3, u, v, rr, q1);
  b1 = pp ^ rr; q2 = pp & rr;              // weight 2 done; q0, q1, q2 carry weight 4
  uvec3 b2, b3;
  fa(q0, q1, q2, b2, b3);

  uvec3 alive = C00.xyz;
  // B45/S345: n in {4,5} -> 010x; n == 3 -> 0011.
  uvec3 nxt = ~b3 & ((b2 & ~b1) | (alive & ~b2 & b1 & b0));

  uint m = LANES == 32 ? 0xffffffffu : ((1u << uint(LANES)) - 1u);
  if (w > WEND) m &= ~(1u << uint(LANES - 1));
  o = uvec4(nxt & uvec3(m), 0u);
}`;
}

export class Sim {
  // opts: { torus, maxLanes (1 = plain one-texel-per-cube layout), maxTex }
  constructor(gl, nx, ny, nz, opts = {}) {
    this.gl = gl;
    this.opts = { ...opts };
    this.layout = makeLayout(nx, ny, nz, { maxTex: gl.getParameter(gl.MAX_TEXTURE_SIZE), ...opts });
    const L = this.layout;
    this.internalFormat = L.plain ? gl.RGBA8UI : gl.RGBA32UI;
    this.tex = [intTexture(gl, this.internalFormat, L.width, L.height), intTexture(gl, this.internalFormat, L.width, L.height)];
    this.fb = this.tex.map(t => framebuffer(gl, [t]));
    this.prog = program(gl, FULLSCREEN_VS, stepFS(L));
    this.vao = gl.createVertexArray();
    this.cur = 0;
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
  }
  get texture() { return this.tex[this.cur]; }
  get dims() { return [this.layout.nx, this.layout.ny, this.layout.nz]; }

  upload(cells) {
    const gl = this.gl, L = this.layout;
    const words = packCells(L, cells, new Uint32Array(L.width * L.height * 4));
    rawPassState(gl);
    gl.bindTexture(gl.TEXTURE_2D, this.tex[this.cur]);
    const data = L.plain ? Uint8Array.from(words) : words;
    gl.texSubImage2D(gl.TEXTURE_2D, 0, 0, 0, L.width, L.height, gl.RGBA_INTEGER, L.plain ? gl.UNSIGNED_BYTE : gl.UNSIGNED_INT, data);
  }

  // Blocking readback; for tests, resizing and snapshots, never the frame loop.
  readTexels() {
    const gl = this.gl, L = this.layout;
    const out = new Uint32Array(L.width * L.height * 4);
    rawPassState(gl);
    gl.bindBuffer(gl.PIXEL_PACK_BUFFER, null);
    gl.bindFramebuffer(gl.FRAMEBUFFER, this.fb[this.cur]);
    gl.readBuffer(gl.COLOR_ATTACHMENT0);
    gl.readPixels(0, 0, L.width, L.height, gl.RGBA_INTEGER, gl.UNSIGNED_INT, out);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    return out;
  }
  // Wait for all queued work (reads one texel). Benchmarks only.
  sync() {
    const gl = this.gl, px = new Uint32Array(4);
    gl.bindFramebuffer(gl.FRAMEBUFFER, this.fb[this.cur]);
    gl.readPixels(0, 0, 1, 1, gl.RGBA_INTEGER, gl.UNSIGNED_INT, px);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
  }
  download() { return unpackCells(this.layout, this.readTexels()); }

  step(n = 1) {
    const gl = this.gl, L = this.layout;
    rawPassState(gl);
    gl.useProgram(this.prog.program);
    gl.bindVertexArray(this.vao);
    gl.viewport(0, 0, L.width, L.height);
    gl.uniform1i(this.prog.uniforms.S, 0);
    gl.activeTexture(gl.TEXTURE0);
    for (let s = 0; s < n; s++) {
      gl.bindFramebuffer(gl.FRAMEBUFFER, this.fb[1 - this.cur]);
      gl.bindTexture(gl.TEXTURE_2D, this.tex[this.cur]);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
      this.cur = 1 - this.cur;
    }
    gl.bindTexture(gl.TEXTURE_2D, null);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    gl.bindVertexArray(null);
  }

  dispose() {
    const gl = this.gl;
    this.tex.forEach(t => gl.deleteTexture(t));
    this.fb.forEach(f => gl.deleteFramebuffer(f));
    gl.deleteProgram(this.prog.program);
    gl.deleteVertexArray(this.vao);
  }
}
