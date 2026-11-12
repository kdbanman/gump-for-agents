// Storage layout of the automaton state on the GPU.
//
// Cube-index coordinates (docs/AUTOMATON.md §1): cube (i,j,k) owns three cells, X/Y/Z = its
// +x/+y/+z faces. A texel holds one *word* per plane in its R/G/B channels (A unused).
//
// Bit packing along i ("strided lanes"): with WN words per row and LANES lanes per word,
// lane b of word w holds cube i = b*WN + w. A shift by one cube in i is then "the next word",
// except at the row ends, where it is a 1-bit shift of the first/last word — cheap and exact
// for any NX, torus or not. LANES = 1 is the plain one-texel-per-cube layout (WN = NX).
// The lane holding i = NX-1 is lane LANES-1 of word WEND; lane LANES-1 of words > WEND is unused
// and always zero.
//
// z-slices (each WN x NY texels) are tiled into a 2D atlas, TILESX tiles per atlas row, so one
// draw call advances the whole volume by one generation.

export function makeLayout(nx, ny, nz, { torus = false, maxLanes = 32, maxTex = 8192 } = {}) {
  if (!(nx >= 1 && ny >= 1 && nz >= 1)) throw new Error('bad dims');
  maxLanes = Math.max(1, Math.min(32, maxLanes | 0));
  const WN = Math.ceil(nx / maxLanes);
  const LANES = Math.ceil(nx / WN);
  const WEND = nx - 1 - (LANES - 1) * WN;
  let best = null;
  for (let tx = 1; tx <= nz; tx++) {
    const w = tx * WN, h = Math.ceil(nz / tx) * ny;
    if (w > maxTex || h > maxTex) continue;
    const score = Math.max(w, h) * 4 + w * h / Math.max(w, h); // prefer square, then small
    if (!best || score < best.score) best = { tx, w, h, score };
  }
  if (!best) throw new Error(`volume ${nx}x${ny}x${nz} does not fit in a ${maxTex}^2 atlas`);
  return {
    nx, ny, nz, torus, WN, LANES, WEND,
    TILESX: best.tx, TILESY: Math.ceil(nz / best.tx),
    width: best.w, height: best.h,
    plain: LANES === 1,
  };
}

// GLSL ES 3.00 declarations shared by every shader that reads the state texture.
export function layoutGLSL(L) {
  return `
#define NX ${L.nx}
#define NY ${L.ny}
#define NZ ${L.nz}
#define WN ${L.WN}
#define LANES ${L.LANES}
#define WEND ${L.WEND}
#define TILESX ${L.TILESX}
#define TORUS ${L.torus ? 1 : 0}
ivec2 atlasOrigin(int k) { return ivec2((k % TILESX) * WN, (k / TILESX) * NY); }
// The three face bits (X,Y,Z) of cube c, which must be inside the volume.
uvec3 cellBits(highp usampler2D S, ivec3 c) {
  int b = c.x / WN;
  int w = c.x - b * WN;
  uvec4 v = texelFetch(S, atlasOrigin(c.z) + ivec2(w, c.y), 0);
  return (v.xyz >> uint(b)) & 1u;
}
`;
}

// CPU packing between the dense cell array (Uint8Array, index i + nx*(j + ny*k), bits 0/1/2 =
// X/Y/Z faces) and the atlas texel array (4 channels per texel).
export function packCells(L, cells, out) {
  out.fill(0);
  const { nx, ny, nz, WN, TILESX } = L;
  for (let k = 0; k < nz; k++) {
    const ox = (k % TILESX) * WN, oy = Math.floor(k / TILESX) * ny;
    for (let j = 0; j < ny; j++) {
      const row = nx * (j + ny * k);
      for (let i = 0; i < nx; i++) {
        const c = cells[row + i];
        if (!c) continue;
        const b = Math.floor(i / WN), w = i - b * WN;
        const t = 4 * ((oy + j) * L.width + ox + w);
        const bit = (1 << b) >>> 0;
        if (c & 1) out[t] = (out[t] | bit) >>> 0;
        if (c & 2) out[t + 1] = (out[t + 1] | bit) >>> 0;
        if (c & 4) out[t + 2] = (out[t + 2] | bit) >>> 0;
      }
    }
  }
  return out;
}

export function unpackCells(L, texels, cells = new Uint8Array(L.nx * L.ny * L.nz)) {
  const { nx, ny, nz, WN, TILESX } = L;
  for (let k = 0; k < nz; k++) {
    const ox = (k % TILESX) * WN, oy = Math.floor(k / TILESX) * ny;
    for (let j = 0; j < ny; j++) {
      const row = nx * (j + ny * k);
      for (let i = 0; i < nx; i++) {
        const b = Math.floor(i / WN), w = i - b * WN;
        const t = 4 * ((oy + j) * L.width + ox + w);
        cells[row + i] = ((texels[t] >>> b) & 1) | (((texels[t + 1] >>> b) & 1) << 1) | (((texels[t + 2] >>> b) & 1) << 2);
      }
    }
  }
  return cells;
}
