// Brick occupancy for the ray-marcher's empty-space skipping: one R8UI texel per BxBxB block of
// cubes, non-zero iff any face of any cube in the block is live (in the current or, when asked,
// the previous generation). Rebuilt at most once per displayed frame, only when the state changed.
import { program, FULLSCREEN_VS, intTexture, framebuffer, rawPassState } from './util.js';
import { layoutGLSL } from './layout.js';

export function brickLayout(L) {
  const B = Math.max(L.nx, L.ny, L.nz) > 64 ? 8 : 4;
  const nb = [Math.ceil(L.nx / B), Math.ceil(L.ny / B), Math.ceil(L.nz / B)];
  const tx = Math.max(1, Math.min(nb[2], Math.ceil(Math.sqrt(nb[2] * nb[1] / nb[0]))));
  return { B, nb, TX: tx, width: tx * nb[0], height: Math.ceil(nb[2] / tx) * nb[1] };
}

// GLSL for readers (the ray-marcher).
export function brickGLSL(BL) {
  return `
#define BRICK ${BL.B}
#define NBX ${BL.nb[0]}
#define NBY ${BL.nb[1]}
#define NBZ ${BL.nb[2]}
#define BTX ${BL.TX}
bool brickLive(highp usampler2D Bk, ivec3 b) {
  return texelFetch(Bk, ivec2((b.z % BTX) * NBX + b.x, (b.z / BTX) * NBY + b.y), 0).r != 0u;
}
`;
}

function fs(L, BL) {
  return `#version 300 es
precision highp float; precision highp int; precision highp usampler2D;
${layoutGLSL(L)}
${brickGLSL(BL)}
uniform usampler2D S, P;
uniform bool usePrev;
out uvec4 o;
void main() {
  ivec2 q = ivec2(gl_FragCoord.xy);
  int tx = q.x / NBX, ty = q.y / NBY;
  ivec3 b = ivec3(q.x - tx * NBX, q.y - ty * NBY, ty * BTX + tx);
  if (b.z >= NBZ) { o = uvec4(0u); return; }
  ivec3 c0 = b * BRICK, c1 = min(c0 + BRICK, ivec3(NX, NY, NZ));
  uint any = 0u;
  for (int k = c0.z; k < c1.z && any == 0u; k++)
    for (int j = c0.y; j < c1.y && any == 0u; j++)
      for (int i = c0.x; i < c1.x; i++) {
        uvec3 v = cellBits(S, ivec3(i, j, k));
        if (usePrev) v |= cellBits(P, ivec3(i, j, k));
        if ((v.x | v.y | v.z) != 0u) { any = 1u; break; }
      }
  o = uvec4(any, 0u, 0u, 0u);
}`;
}

export class Bricks {
  constructor(gl, L) {
    this.gl = gl;
    this.layout = brickLayout(L);
    this.tex = intTexture(gl, gl.R8UI, this.layout.width, this.layout.height);
    this.fb = framebuffer(gl, [this.tex]);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    this.prog = program(gl, FULLSCREEN_VS, fs(L, this.layout));
    this.vao = gl.createVertexArray();
  }
  update(stateTex, prevTex, usePrev) {
    const gl = this.gl, u = this.prog.uniforms;
    rawPassState(gl);
    gl.bindFramebuffer(gl.FRAMEBUFFER, this.fb);
    gl.viewport(0, 0, this.layout.width, this.layout.height);
    gl.useProgram(this.prog.program);
    gl.bindVertexArray(this.vao);
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, stateTex);
    gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, prevTex);
    gl.uniform1i(u.S, 0); gl.uniform1i(u.P, 1); gl.uniform1i(u.usePrev, usePrev ? 1 : 0);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
    gl.bindTexture(gl.TEXTURE_2D, null); gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, null);
    gl.bindVertexArray(null);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
  }
  dispose() { const gl = this.gl; gl.deleteTexture(this.tex); gl.deleteFramebuffer(this.fb); gl.deleteProgram(this.prog.program); gl.deleteVertexArray(this.vao); }
}
