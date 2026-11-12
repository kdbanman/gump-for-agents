// Two three.js views of the live faces, both reading the simulation texture directly
// (THREE.ExternalTexture around the sim's WebGLTexture; no CPU readback):
//
//  - "instanced": one instanced quad per cell (3 per cube); the vertex shader fetches the
//    cell's bit and collapses dead cells. Cost ~ volume, independent of the screen.
//  - "raymarch": a box whose fragment shader walks the cube grid with a 3D DDA. Each step of a
//    DDA in a cubic grid crosses exactly one face, i.e. one cell, so a step = one bit test.
//    Cost ~ pixels x path length, independent of population.
//
// World space = cube space shifted so the volume is centred on the origin; cube (i,j,k)
// spans [i,i+1]x[j,j+1]x[k,k+1] before the shift. Face X[i,j,k] sits on the plane x = i+1.
import * as THREE from 'three';
import { layoutGLSL } from './gl/layout.js';

export const PALETTE = {
  x: [117, 149, 172], y: [107, 126, 81], z: [245, 153, 78], background: '#484340',
};
const vec3c = (c) => new THREE.Vector3(c[0] / 255, c[1] / 255, c[2] / 255);

const SHADE_GLSL = `
uniform vec3 colX, colY, colZ, bg;
uniform vec3 lightDir;
uniform float fogNear, fogFar;
uniform float border;
// axis 0/1/2, normal facing the viewer, view-space depth, in-face coords in [-1,1]
vec3 shade(int axis, vec3 n, vec3 toEye, float depth, vec2 uv) {
  vec3 base = axis == 0 ? colX : (axis == 1 ? colY : colZ);
  float lit = 0.62 + 0.30 * abs(dot(n, lightDir)) + 0.12 * abs(dot(n, toEye));
  vec3 c = base * lit;
  float e = max(abs(uv.x), abs(uv.y));
  c *= mix(1.0, 0.72, border * smoothstep(0.80, 0.92, e));
  float f = clamp((depth - fogNear) / max(fogFar - fogNear, 1e-3), 0.0, 1.0);
  return mix(c, bg, 0.55 * f * f);
}
`;

function commonUniforms(stateTex) {
  return {
    S: { value: stateTex },
    faceScale: { value: 0.5 },
    colX: { value: vec3c(PALETTE.x) }, colY: { value: vec3c(PALETTE.y) }, colZ: { value: vec3c(PALETTE.z) },
    bg: { value: vec3c([0x48, 0x43, 0x40]) },
    lightDir: { value: new THREE.Vector3(0.45, 0.8, 0.4).normalize() },
    fogNear: { value: 0 }, fogFar: { value: 1 },
    border: { value: 1 },
    dims: { value: new THREE.Vector3(1, 1, 1) },
    hullLo: { value: new THREE.Vector4() }, hullHi: { value: new THREE.Vector4() }, hullOn: { value: 0 },
  };
}

// pulled = true: no instancing, no attributes; 6 vertices per cell from gl_VertexID.
function quadMaterial(layout, uniforms, pulled) {
  return new THREE.RawShaderMaterial({
    glslVersion: THREE.GLSL3,
    uniforms,
    side: THREE.DoubleSide,
    vertexShader: `
precision highp float; precision highp int; precision highp usampler2D;
${layoutGLSL(layout)}
uniform usampler2D S;
uniform mat4 modelViewMatrix, projectionMatrix, modelMatrix;
uniform vec3 cameraPosition;
uniform float faceScale;
uniform vec3 dims;
${pulled ? 'const vec2 CORNERS[6] = vec2[6](vec2(-1,-1), vec2(1,-1), vec2(1,1), vec2(-1,-1), vec2(1,1), vec2(-1,1));'
          : 'in vec3 position;          // quad corner in (u, v) = position.xy, each +-1'}
flat out int vAxis;
out vec3 vNormal, vToEye;
out vec2 vUV;
out float vDepth;
void main() {
${pulled ? 'int id = gl_VertexID / 6; vec2 q = CORNERS[gl_VertexID - id * 6];' : 'int id = gl_InstanceID; vec2 q = position.xy;'}
  int axis = id % 3; id /= 3;
  ivec3 c = ivec3(id % NX, (id / NX) % NY, id / (NX * NY));
  uvec3 bits = cellBits(S, c);
  uint alive = axis == 0 ? bits.x : (axis == 1 ? bits.y : bits.z);
  if (alive == 0u) { gl_Position = vec4(2.0, 2.0, 2.0, 1.0); return; }
  vec3 centre = vec3(c) + 0.5; vec3 n = vec3(0.0);
  vec3 off;
  vec2 uv = q * 0.5 * faceScale;
  if (axis == 0) { centre.x += 0.5; n = vec3(1, 0, 0); off = vec3(0.0, uv.x, uv.y); }
  else if (axis == 1) { centre.y += 0.5; n = vec3(0, 1, 0); off = vec3(uv.y, 0.0, uv.x); }
  else { centre.z += 0.5; n = vec3(0, 0, 1); off = vec3(uv.x, uv.y, 0.0); }
  vec3 world = centre + off - 0.5 * dims;
  vec4 mv = modelViewMatrix * vec4(world, 1.0);
  gl_Position = projectionMatrix * mv;
  vAxis = axis; vNormal = n; vUV = q;
  vToEye = normalize(cameraPosition - world);
  vDepth = -mv.z;
}`,
    fragmentShader: `
precision highp float; precision highp int;
${SHADE_GLSL}
flat in int vAxis;
in vec3 vNormal, vToEye;
in vec2 vUV;
in float vDepth;
out vec4 fragColor;
void main() {
  vec3 n = dot(vNormal, vToEye) < 0.0 ? -vNormal : vNormal;
  fragColor = vec4(shade(vAxis, n, normalize(vToEye), vDepth, vUV), 1.0);
}`,
  });
}

function raymarchMaterial(layout, uniforms) {
  return new THREE.RawShaderMaterial({
    glslVersion: THREE.GLSL3,
    uniforms: { ...uniforms, invView: { value: new THREE.Matrix4() } },
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
${SHADE_GLSL}
uniform usampler2D S;
uniform vec3 cameraPosition;
uniform mat4 viewMatrix, projectionMatrix;
uniform float faceScale;
uniform vec3 dims;
uniform vec4 hullLo, hullHi;   // diagonal hull (doubled coords), used to clip rays when hullOn
uniform float hullOn;
in vec3 vWorld;
out vec4 fragColor;
void main() {
  vec3 ro = cameraPosition + 0.5 * dims;              // cube space
  vec3 rd = normalize(vWorld - cameraPosition);
  vec3 inv = 1.0 / rd;
  vec3 t0 = (vec3(0.0) - ro) * inv, t1 = (dims - ro) * inv;
  vec3 tmin = min(t0, t1), tmax = max(t0, t1);
  float tNear = max(max(tmin.x, tmin.y), tmin.z), tFar = min(min(tmax.x, tmax.y), tmax.z);
  if (hullOn > 0.5) {
    // The hull only ever shrinks (T2), so a slightly stale hull still contains every live cell.
    // Face squares reach at most 2*faceScale doubled units across a layer: margin 2.5.
    const mat4 D = mat4(1, 1, 1, 0,  1, 1, -1, 0,  1, -1, 1, 0,  -1, 1, 1, 0);
    vec4 a = vec4(2.0 * ro - 1.0, 0.0) * D, b = vec4(2.0 * rd, 0.0) * D;   // s(t) = a + b t, per diagonal
    for (int q = 0; q < 4; q++) {
      float lo = hullLo[q] - 2.5, hi = hullHi[q] + 2.5;
      if (abs(b[q]) < 1e-6) { if (a[q] < lo || a[q] > hi) discard; continue; }
      float u = (lo - a[q]) / b[q], v = (hi - a[q]) / b[q];
      tNear = max(tNear, min(u, v)); tFar = min(tFar, max(u, v));
    }
  }
  if (tFar < max(tNear, 0.0)) discard;
  float tStart = max(tNear, 0.0) - 1e-4;
  vec3 p = ro + rd * tStart;
  ivec3 c = ivec3(floor(p));
  ivec3 stp = ivec3(sign(rd));
  vec3 tDelta = abs(inv);
  vec3 tNext = (vec3(c) + max(vec3(stp), 0.0) - ro) * inv;   // next boundary per axis
  ivec3 N = ivec3(NX, NY, NZ);
  float half_ = 0.5 * faceScale;
  int maxSteps = NX + NY + NZ + 4;
  for (int s = 0; s < 4096; s++) {
    if (s >= maxSteps) break;
    int a = tNext.x < tNext.y ? (tNext.x < tNext.z ? 0 : 2) : (tNext.y < tNext.z ? 1 : 2);
    float t = tNext[a];
    if (t > tFar + 1e-4) break;
    // crossing the plane between c and c + stp[a]*e_a: that face is the +a face of the lower cube
    ivec3 f = c; if (stp[a] < 0) f[a] -= 1;
    if (all(greaterThanEqual(f, ivec3(0))) && all(lessThan(f, N))) {
      vec3 h = ro + rd * t;
      vec2 uv = a == 0 ? h.yz : (a == 1 ? h.zx : h.xy);
      vec2 cuv = uv - floor(uv) - 0.5;
      if (abs(cuv.x) <= half_ && abs(cuv.y) <= half_) {
        uvec3 bits = cellBits(S, f);
        uint alive = a == 0 ? bits.x : (a == 1 ? bits.y : bits.z);
        if (alive != 0u) {
          vec3 n = vec3(0.0); n[a] = -float(stp[a]);
          vec3 world = h - 0.5 * dims;
          vec4 vp = viewMatrix * vec4(world, 1.0);
          vec4 clip = projectionMatrix * vp;
          gl_FragDepth = 0.5 * (clip.z / clip.w) + 0.5;
          fragColor = vec4(shade(a, n, -rd, -vp.z, cuv / half_), 1.0);
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
    this.stateTex = new THREE.ExternalTexture(null);
    this.uniforms = commonUniforms(this.stateTex);
    this.mode = 'raymarch';
    this.layout = null;
    this.meshes = {};
  }

  // (Re)build for a new layout (dims / packing change).
  setLayout(layout) {
    for (const m of Object.values(this.meshes)) { this.group.remove(m); m.geometry.dispose(); m.material.dispose(); }
    this.layout = layout;
    this.uniforms.dims.value.set(layout.nx, layout.ny, layout.nz);

    const quad = new THREE.InstancedBufferGeometry();
    quad.setAttribute('position', new THREE.Float32BufferAttribute([-1, -1, 0, 1, -1, 0, 1, 1, 0, -1, 1, 0], 3));
    quad.setIndex([0, 1, 2, 0, 2, 3]);
    quad.instanceCount = 3 * layout.nx * layout.ny * layout.nz;
    const inst = new THREE.Mesh(quad, quadMaterial(layout, this.uniforms, false));
    inst.frustumCulled = false;

    const pulledGeom = new THREE.BufferGeometry();
    pulledGeom.setDrawRange(0, 18 * layout.nx * layout.ny * layout.nz);
    const pulled = new THREE.Mesh(pulledGeom, quadMaterial(layout, this.uniforms, true));
    pulled.frustumCulled = false;

    const box = new THREE.Mesh(new THREE.BoxGeometry(layout.nx + 0.02, layout.ny + 0.02, layout.nz + 0.02), raymarchMaterial(layout, this.uniforms));
    box.frustumCulled = false;

    this.meshes = { instanced: inst, quads: pulled, raymarch: box };
    for (const m of Object.values(this.meshes)) this.group.add(m);
    this.setMode(this.mode);
  }

  setMode(mode) {
    this.mode = mode;
    for (const [k, m] of Object.entries(this.meshes)) m.visible = k === mode;
  }

  // Called every frame before rendering.
  // hull: { loS, hiS } valid for the current state (or older: it only shrinks), or null.
  setHullClip(hull) {
    this.uniforms.hullOn.value = hull ? 1 : 0;
    if (hull) { this.uniforms.hullLo.value.fromArray(hull.loS); this.uniforms.hullHi.value.fromArray(hull.hiS); }
  }

  update(simTexture, camera, { faceScale, border }) {
    this.stateTex.sourceTexture = simTexture;
    this.uniforms.faceScale.value = faceScale;
    this.uniforms.border.value = border;
    const d = camera.position.length();
    const r = 0.5 * this.uniforms.dims.value.length();
    this.uniforms.fogNear.value = Math.max(0, d - r);
    this.uniforms.fogFar.value = d + r;
  }
}
