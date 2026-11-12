// three.js views of the live faces, all reading the simulation textures directly
// (THREE.ExternalTexture around the sim's WebGLTextures; no CPU readback):
//
//  - "quads": 6 vertices per cell slot pulled from gl_VertexID (no attributes); the vertex
//    shader fetches the cell and collapses hidden ones. Cost ~ volume.
//  - "instanced": the same with one instance per cell slot (kept for comparison).
//  - "raymarch": a box whose fragment shader walks the cube grid with a 3D DDA. Each DDA step in
//    a cubic grid crosses exactly one face, i.e. one cell: a step is one bit test. Rays are
//    clipped to the diagonal hull and to the {111} slice, and skip empty bricks.
//
// Shared by all: the {111} slicer (show only layers sliceLo <= d.p <= sliceHi), colour modes
// (orientation / layer ABC along a diagonal / change since the previous generation), and, for
// the quads only, the editor's categories (edit set opaque, its dead slots and everything else
// translucent).
//
// World space = cube space shifted so the volume is centred on the origin; cube (i,j,k)
// spans [i,i+1]x[j,j+1]x[k,k+1] before the shift. Face X[i,j,k] sits on the plane x = i+1.
import * as THREE from 'three';
import { layoutGLSL } from './gl/layout.js';
import { brickGLSL } from './gl/bricks.js';

export const PALETTE = {
  x: [117, 149, 172], y: [107, 126, 81], z: [245, 153, 78], background: '#484340',
  abc: [[214, 96, 77], [86, 168, 160], [228, 196, 92]],
  born: [255, 238, 150], died: [150, 52, 46],
};
const v3 = (c) => new THREE.Vector3(c[0] / 255, c[1] / 255, c[2] / 255);
export const COLOR_MODES = ['orientation', 'layer', 'change'];

const CELL_GLSL = `
uniform usampler2D S, P;
uniform vec3 colX, colY, colZ, colA, colB, colC, colBorn, colDied, bg;
uniform int colorMode;
uniform bool sliceOn;
uniform vec3 sliceD;
uniform float sliceLo, sliceHi;
uniform int editKind, editAxis;
uniform float editCoord, editS;
uniform vec3 editD;
uniform float faceScale;

uint comp(uvec3 v, int a) { return a == 0 ? v.x : (a == 1 ? v.y : v.z); }
bool inEditSet(vec3 p, int a) {
  if (editKind == 1) return a == editAxis && p[a] == editCoord;
  if (editKind == 2) return dot(p, editD) == editS;
  return true;
}
// Cell (cube c, axis a): is it drawn, its base colour, its face scale and 'live' flag.
// cat: 0 hidden, 1 live (opaque), 2 dead slot of the edit set (ghost), 3 live outside the edit set (faint)
int cellCat(ivec3 c, int a, out vec3 base, out float scale) {
  uint now = comp(cellBits(S, c), a);
  uint before = colorMode == 2 ? comp(cellBits(P, c), a) : now;
  vec3 p = vec3(2 * c); p[a] += 1.0;
  if (sliceOn) { float s = dot(p, sliceD); if (s < sliceLo || s > sliceHi) return 0; }
  bool inSet = inEditSet(p, a);
  scale = faceScale;
  vec3 orient = a == 0 ? colX : (a == 1 ? colY : colZ);
  if (colorMode == 1) {
    int l = int(dot(p, sliceD));
    l = ((l - 1) / 2) % 3; if (l < 0) l += 3;     // ABC stacking along the slicer's diagonal
    base = l == 0 ? colA : (l == 1 ? colB : colC);
  } else if (colorMode == 2) {
    if (now != 0u && before == 0u) base = colBorn;
    else if (now != 0u) base = orient * 0.55;
    else { base = colDied; scale = faceScale * 0.45; }
  } else base = orient;
  bool shown = now != 0u || (colorMode == 2 && before != 0u);
  if (editKind == 0) return shown ? 1 : 0;
  if (inSet) return shown ? 1 : 2;
  return shown ? 3 : 0;
}

uniform vec3 lightDir;
uniform float fogNear, fogFar, border;
vec3 shade(vec3 base, vec3 n, vec3 toEye, float depth, vec2 uv) {
  float lit = 0.62 + 0.30 * abs(dot(n, lightDir)) + 0.12 * abs(dot(n, toEye));
  vec3 c = base * lit;
  float e = max(abs(uv.x), abs(uv.y));
  c *= mix(1.0, 0.72, border * smoothstep(0.80, 0.92, e));
  float f = clamp((depth - fogNear) / max(fogFar - fogNear, 1e-3), 0.0, 1.0);
  return mix(c, bg, 0.55 * f * f);
}
`;

function commonUniforms() {
  return {
    S: { value: new THREE.ExternalTexture(null) }, P: { value: new THREE.ExternalTexture(null) },
    Bk: { value: new THREE.ExternalTexture(null) }, brickOn: { value: false },
    faceScale: { value: 0.6 },
    colX: { value: v3(PALETTE.x) }, colY: { value: v3(PALETTE.y) }, colZ: { value: v3(PALETTE.z) },
    colA: { value: v3(PALETTE.abc[0]) }, colB: { value: v3(PALETTE.abc[1]) }, colC: { value: v3(PALETTE.abc[2]) },
    colBorn: { value: v3(PALETTE.born) }, colDied: { value: v3(PALETTE.died) },
    bg: { value: v3([0x48, 0x43, 0x40]) },
    colorMode: { value: 0 },
    sliceOn: { value: false }, sliceD: { value: new THREE.Vector3(1, 1, 1) }, sliceLo: { value: 0 }, sliceHi: { value: 0 },
    editKind: { value: 0 }, editAxis: { value: 0 }, editCoord: { value: 0 }, editS: { value: 0 }, editD: { value: new THREE.Vector3(1, 1, 1) },
    lightDir: { value: new THREE.Vector3(0.45, 0.8, 0.4).normalize() },
    fogNear: { value: 0 }, fogFar: { value: 1 }, border: { value: 1 },
    dims: { value: new THREE.Vector3(1, 1, 1) },
    hullLo: { value: new THREE.Vector4() }, hullHi: { value: new THREE.Vector4() }, hullOn: { value: 0 },
    isOrtho: { value: false }, camDir: { value: new THREE.Vector3(0, 0, -1) },
    pass: { value: 0 },
  };
}

// pulled = true: no instancing, no attributes; 6 vertices per cell slot from gl_VertexID.
// pass 0: opaque cells; pass 1 (editor only): translucent ghosts.
function quadMaterial(layout, uniforms, pulled, pass) {
  const u = { ...uniforms, pass: { value: pass } };
  return new THREE.RawShaderMaterial({
    glslVersion: THREE.GLSL3,
    uniforms: u,
    side: THREE.DoubleSide,
    transparent: pass === 1, depthWrite: pass === 0,
    vertexShader: `
precision highp float; precision highp int; precision highp usampler2D;
${layoutGLSL(layout)}
${CELL_GLSL}
uniform mat4 modelViewMatrix, projectionMatrix;
uniform vec3 cameraPosition, camDir;
uniform bool isOrtho;
uniform vec3 dims;
uniform int pass;
${pulled ? 'const vec2 CORNERS[6] = vec2[6](vec2(-1,-1), vec2(1,-1), vec2(1,1), vec2(-1,-1), vec2(1,1), vec2(-1,1));' : 'in vec3 position;'}
flat out int vAxis, vCat;
flat out vec3 vBase;
out vec3 vNormal, vToEye;
out vec2 vUV;
out float vDepth;
void main() {
  ${pulled ? 'int id = gl_VertexID / 6; vec2 q = CORNERS[gl_VertexID - id * 6];' : 'int id = gl_InstanceID; vec2 q = position.xy;'}
  int axis = id % 3; id /= 3;
  ivec3 c = ivec3(id % NX, (id / NX) % NY, id / (NX * NY));
  vec3 base; float scale;
  int cat = cellCat(c, axis, base, scale);
  bool draw = pass == 0 ? cat == 1 : (cat == 2 || cat == 3);
  if (!draw) { gl_Position = vec4(2.0, 2.0, 2.0, 1.0); return; }
  vec3 centre = vec3(c) + 0.5; vec3 n;
  vec3 off;
  vec2 uv = q * 0.5 * (cat == 2 ? 0.92 : scale);
  if (axis == 0) { centre.x += 0.5; n = vec3(1, 0, 0); off = vec3(0.0, uv.x, uv.y); }
  else if (axis == 1) { centre.y += 0.5; n = vec3(0, 1, 0); off = vec3(uv.y, 0.0, uv.x); }
  else { centre.z += 0.5; n = vec3(0, 0, 1); off = vec3(uv.x, uv.y, 0.0); }
  vec3 world = centre + off - 0.5 * dims;
  vec4 mv = modelViewMatrix * vec4(world, 1.0);
  gl_Position = projectionMatrix * mv;
  vAxis = axis; vCat = cat; vBase = base; vNormal = n; vUV = q;
  vToEye = isOrtho ? -camDir : normalize(cameraPosition - world);
  vDepth = -mv.z;
}`,
    fragmentShader: `
precision highp float; precision highp int; precision highp usampler2D;
${layoutGLSL(layout)}
${CELL_GLSL}
flat in int vAxis, vCat;
flat in vec3 vBase;
in vec3 vNormal, vToEye;
in vec2 vUV;
in float vDepth;
out vec4 fragColor;
void main() {
  vec3 n = dot(vNormal, vToEye) < 0.0 ? -vNormal : vNormal;
  vec3 c = shade(vBase, n, normalize(vToEye), vDepth, vUV);
  if (vCat == 2) {          // dead slot of the edit set: a faint outline
    float e = max(abs(vUV.x), abs(vUV.y));
    fragColor = vec4(mix(vec3(0.85), vBase, 0.4), e > 0.84 ? 0.32 : 0.035);
  } else if (vCat == 3) fragColor = vec4(c, 0.28);
  else fragColor = vec4(c, 1.0);
}`,
  });
}

function raymarchMaterial(layout, brickLayout, uniforms) {
  return new THREE.RawShaderMaterial({
    glslVersion: THREE.GLSL3,
    uniforms,
    side: THREE.BackSide,
    vertexShader: `
precision highp float;
uniform mat4 modelViewMatrix, projectionMatrix, modelMatrix;
in vec3 position;
out vec3 vWorld;
void main() {
  vWorld = (modelMatrix * vec4(position, 1.0)).xyz;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}`,
    fragmentShader: `
precision highp float; precision highp int; precision highp usampler2D;
${layoutGLSL(layout)}
${brickGLSL(brickLayout)}
${CELL_GLSL}
uniform usampler2D Bk;
uniform bool brickOn;
uniform vec3 cameraPosition, camDir;
uniform bool isOrtho;
uniform mat4 viewMatrix, projectionMatrix;
uniform vec3 dims;
uniform vec4 hullLo, hullHi;   // diagonal hull (doubled coords), used to clip rays when hullOn
uniform float hullOn;
in vec3 vWorld;
out vec4 fragColor;

// clip [tNear, tFar] to lo <= a + b t <= hi
void clipSlab(float a, float b, float lo, float hi, inout float tNear, inout float tFar) {
  if (abs(b) < 1e-7) { if (a < lo || a > hi) tFar = -1.0; return; }
  float u = (lo - a) / b, v = (hi - a) / b;
  tNear = max(tNear, min(u, v)); tFar = min(tFar, max(u, v));
}

void main() {
  vec3 rd = isOrtho ? normalize(camDir) : normalize(vWorld - cameraPosition);
  vec3 ro = (isOrtho ? vWorld - rd * (length(dims) + 1.0) : cameraPosition) + 0.5 * dims;   // cube space
  vec3 inv = 1.0 / rd;
  vec3 t0 = (vec3(0.0) - ro) * inv, t1 = (dims - ro) * inv;
  vec3 tmin = min(t0, t1), tmax = max(t0, t1);
  float tNear = max(max(tmin.x, tmin.y), tmin.z), tFar = min(min(tmax.x, tmax.y), tmax.z);
  // s(t) = d.p along the ray, p = 2x - 1 in doubled coordinates. Face squares reach at most
  // 2*faceScale doubled units across a layer: margin 2.5.
  const mat4 D = mat4(1, 1, 1, 0,  1, 1, -1, 0,  1, -1, 1, 0,  -1, 1, 1, 0);
  if (hullOn > 0.5) {
    // The hull only ever shrinks (T2), so a slightly stale hull still contains every live cell.
    vec4 a = vec4(2.0 * ro - 1.0, 0.0) * D, b = vec4(2.0 * rd, 0.0) * D;
    for (int q = 0; q < 4; q++) clipSlab(a[q], b[q], hullLo[q] - 2.5, hullHi[q] + 2.5, tNear, tFar);
  }
  if (sliceOn) clipSlab(dot(2.0 * ro - 1.0, sliceD), dot(2.0 * rd, sliceD), sliceLo - 2.5, sliceHi + 2.5, tNear, tFar);
  if (tFar < max(tNear, 0.0)) discard;
  float tStart = max(tNear, 0.0) - 1e-4;
  ivec3 c = ivec3(floor(ro + rd * tStart));
  ivec3 stp = ivec3(sign(rd));
  vec3 tDelta = abs(inv);
  vec3 tNext = (vec3(c) + max(vec3(stp), 0.0) - ro) * inv;   // next boundary per axis
  ivec3 N = ivec3(NX, NY, NZ);
  float half_ = 0.5 * faceScale;
  ivec3 lastBrick = ivec3(-99);
  int maxSteps = NX + NY + NZ + 4;
  for (int s = 0; s < 8192; s++) {
    if (s >= maxSteps) break;
    // empty-space skipping: entering an empty brick jumps to its exit. The face on the exit
    // plane is still tested: the walk restarts just before it, in the empty brick's last cube.
    if (brickOn && all(greaterThanEqual(c, ivec3(0))) && all(lessThan(c, N))) {
      ivec3 bk = c / BRICK;
      if (bk != lastBrick) {
        lastBrick = bk;
        if (!brickLive(Bk, bk)) {
          vec3 bmin = vec3(bk * BRICK), bmax = min(bmin + float(BRICK), dims);
          vec3 tb = ((mix(bmin, bmax, step(0.0, rd))) - ro) * inv;
          float tExit = min(min(tb.x, tb.y), tb.z);
          if (tExit > tFar + 1e-4) break;
          vec3 pe = ro + rd * (tExit - 1e-4);
          c = clamp(ivec3(floor(pe)), ivec3(bmin), ivec3(bmax) - 1);
          tNext = (vec3(c) + max(vec3(stp), 0.0) - ro) * inv;
        }
      }
    }
    int a = tNext.x < tNext.y ? (tNext.x < tNext.z ? 0 : 2) : (tNext.y < tNext.z ? 1 : 2);
    if (tNext[a] > tFar + 1e-4) break;
    // the crossing itself from the plane equation (not the accumulated tNext), so that a walk
    // restarted after brick skipping hits exactly the same points as an uninterrupted one
    float t = (float(c[a] + max(stp[a], 0)) - ro[a]) * inv[a];
    // crossing the plane between c and c + stp[a]*e_a: that face is the +a face of the lower cube
    ivec3 f = c; if (stp[a] < 0) f[a] -= 1;
    if (all(greaterThanEqual(f, ivec3(0))) && all(lessThan(f, N))) {
      vec3 h = ro + rd * t;
      vec2 uv = a == 0 ? h.yz : (a == 1 ? h.zx : h.xy);
      vec2 cuv = uv - floor(uv) - 0.5;
      if (abs(cuv.x) <= half_ && abs(cuv.y) <= half_) {
        vec3 base; float scale;
        if (cellCat(f, a, base, scale) == 1 && abs(cuv.x) <= 0.5 * scale && abs(cuv.y) <= 0.5 * scale) {
          vec3 n = vec3(0.0); n[a] = -float(stp[a]);
          vec3 world = h - 0.5 * dims;
          vec4 vp = viewMatrix * vec4(world, 1.0);
          vec4 clip = projectionMatrix * vp;
          gl_FragDepth = 0.5 * (clip.z / clip.w) + 0.5;
          fragColor = vec4(shade(base, n, -rd, -vp.z, cuv / (0.5 * scale)), 1.0);
          return;
        }
      }
    }
    c[a] += stp[a];
    tNext[a] += tDelta[a];
  }
  discard;
}`,
  });
}

export class CellView {
  constructor(scene) {
    this.scene = scene;
    this.group = new THREE.Group();
    scene.add(this.group);
    this.uniforms = commonUniforms();
    this.mode = 'raymarch';
    this.editing = false;
    this.layout = null;
    this.meshes = {};
  }

  // (Re)build for a new layout (dims / packing change).
  setLayout(layout, brickLayout) {
    for (const m of Object.values(this.meshes)) { this.group.remove(m); m.geometry.dispose(); m.material.dispose(); }
    this.layout = layout;
    this.uniforms.dims.value.set(layout.nx, layout.ny, layout.nz);
    const slots = 3 * layout.nx * layout.ny * layout.nz;

    const quad = new THREE.InstancedBufferGeometry();
    quad.setAttribute('position', new THREE.Float32BufferAttribute([-1, -1, 0, 1, -1, 0, 1, 1, 0, -1, 1, 0], 3));
    quad.setIndex([0, 1, 2, 0, 2, 3]);
    quad.instanceCount = slots;
    const inst = new THREE.Mesh(quad, quadMaterial(layout, this.uniforms, false, 0));

    const pulledGeom = new THREE.BufferGeometry();
    pulledGeom.setDrawRange(0, 6 * slots);
    const pulled = new THREE.Mesh(pulledGeom, quadMaterial(layout, this.uniforms, true, 0));
    const ghosts = new THREE.Mesh(pulledGeom, quadMaterial(layout, this.uniforms, true, 1));
    ghosts.renderOrder = 1;

    const box = new THREE.Mesh(new THREE.BoxGeometry(layout.nx + 0.02, layout.ny + 0.02, layout.nz + 0.02), raymarchMaterial(layout, brickLayout, this.uniforms));

    this.meshes = { instanced: inst, quads: pulled, ghosts, raymarch: box };
    for (const m of Object.values(this.meshes)) { m.frustumCulled = false; this.group.add(m); }
    this.setMode(this.mode);
  }

  // The view actually drawn: the editor always uses the quads (it needs the ghost pass).
  setMode(mode) {
    this.mode = mode;
    const m = this.editing ? 'quads' : mode;
    for (const [k, mesh] of Object.entries(this.meshes)) mesh.visible = k === m || (k === 'ghosts' && this.editing);
  }
  get drawn() { return this.editing ? 'quads' : this.mode; }

  setEdit(set) {     // null, { kind: 'plane', axis, coord } or { kind: 'layer', d, s }
    const u = this.uniforms;
    this.editing = !!set;
    u.editKind.value = !set ? 0 : set.kind === 'plane' ? 1 : 2;
    if (set && set.kind === 'plane') { u.editAxis.value = set.axis; u.editCoord.value = set.coord; }
    if (set && set.kind === 'layer') { u.editD.value.fromArray(set.d); u.editS.value = set.s; }
    this.setMode(this.mode);
  }

  setSlice(slice) {  // null or { d: [..], lo, hi } (s values)
    const u = this.uniforms;
    u.sliceOn.value = !!slice;
    if (slice) { u.sliceD.value.fromArray(slice.d); u.sliceLo.value = slice.lo; u.sliceHi.value = slice.hi; }
  }
  setLayerDiag(d) { if (!this.uniforms.sliceOn.value) this.uniforms.sliceD.value.fromArray(d); }
  setColorMode(m) { this.uniforms.colorMode.value = Math.max(0, COLOR_MODES.indexOf(m)); }

  // hull: { loS, hiS } valid for the current state (or older: it only shrinks), or null.
  setHullClip(hull) {
    this.uniforms.hullOn.value = hull ? 1 : 0;
    if (hull) { this.uniforms.hullLo.value.fromArray(hull.loS); this.uniforms.hullHi.value.fromArray(hull.hiS); }
  }

  // Called every frame before rendering.
  // bricksTex must always be a valid texture (an integer sampler left without one makes the draw
  // fail); useBricks says whether the ray-marcher may trust it (it is only rebuilt when drawn).
  update(sim, bricksTex, useBricks, camera, { faceScale, border }) {
    const u = this.uniforms;
    u.S.value.sourceTexture = sim.texture;
    u.P.value.sourceTexture = sim.prevTexture;
    u.Bk.value.sourceTexture = bricksTex;
    u.brickOn.value = !!useBricks;
    u.faceScale.value = faceScale;
    u.border.value = border;
    u.isOrtho.value = !!camera.isOrthographicCamera;
    camera.getWorldDirection(u.camDir.value);
    const d = camera.position.length();
    const r = 0.5 * u.dims.value.length();
    u.fogNear.value = Math.max(0, d - r);
    u.fogFar.value = d + r;
  }
}
