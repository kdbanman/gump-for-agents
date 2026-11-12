// GLSL shared by every view: which cells are drawn and how (slice, colour modes, editor
// categories), the renderer's own neighbour count (fate / neighbourhood modes), and shading.
// Kept free of three.js so the tests can compile it into their own passes.
export const CELL_GLSL = `
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

uniform vec3 colDies, colNear, colDs0, colDs1, colDs2, colDs3, colDs4, colFocus;
uniform ivec3 focusP;
uniform int focusA;
uint comp(uvec3 v, int a) { return a == 0 ? v.x : (a == 1 ? v.y : v.z); }
// State of the cell at doubled coordinates q (exactly one odd component); outside: torus or dead.
int cellAtD(ivec3 q) {
  int b = (q.x & 1) != 0 ? 0 : ((q.y & 1) != 0 ? 1 : 2);
  ivec3 e = ivec3(b == 0 ? 1 : 0, b == 1 ? 1 : 0, b == 2 ? 1 : 0);
  ivec3 c = (q - e) / 2;                       // exact: q - e is even
  ivec3 N = ivec3(NX, NY, NZ);
#if TORUS
  c = (c % N + N) % N;
#else
  if (any(lessThan(c, ivec3(0))) || any(greaterThanEqual(c, N))) return 0;
#endif
  return int(comp(cellBits(S, c), b));
}
// Live neighbours of cell (cube c, axis a): the 12 offsets of docs/AUTOMATON.md §2.
int nbrCount(ivec3 c, int a) {
  ivec3 p = 2 * c; p[a] += 1;
  int b = (a + 1) % 3, d = (a + 2) % 3, n = 0;
  for (int i = 0; i < 4; i++) {              // coplanar, corner-sharing: +-2 e_b +-2 e_d
    ivec3 o = ivec3(0); o[b] = (i & 1) == 0 ? 2 : -2; o[d] = (i & 2) == 0 ? 2 : -2;
    n += cellAtD(p + o);
  }
  for (int i = 0; i < 8; i++) {              // perpendicular, edge-sharing: +-e_a +-e_t, t in {b, d}
    ivec3 o = ivec3(0); o[a] = (i & 1) == 0 ? 1 : -1; o[(i & 2) == 0 ? b : d] = (i & 4) == 0 ? 1 : -1;
    n += cellAtD(p + o);
  }
  return n;
}
bool isNeighbour(ivec3 q, int a) {          // q = offset from a focus cell with normal a
  int b = (a + 1) % 3, d = (a + 2) % 3;
  ivec3 m = abs(q);
  if (q[a] == 0) return m[b] == 2 && m[d] == 2;
  return m[a] == 1 && ((m[b] == 1 && q[d] == 0) || (m[d] == 1 && q[b] == 0));
}
bool inEditSet(vec3 p, int a) {
  if (editKind == 1) return a == editAxis && p[a] == editCoord;
  if (editKind == 2) return dot(p, editD) == editS;
  return true;
}
// Cell (cube c, axis a): is it drawn, its base colour, its face scale and 'live' flag.
// cat: 0 hidden, 1 opaque, 2 dead slot outline (edit set / one birth away), 3 live but faint
// (outside the edit set / not in the neighbourhood), 4 translucent fill (predicted birth, dead neighbour)
int cellCat(ivec3 c, int a, out vec3 base, out float scale) {
  uint now = comp(cellBits(S, c), a);
  scale = faceScale;
  if (colorMode == 3) {                       // fate: what the rule does to this cell next
    int n = nbrCount(c, a);
    vec3 orient = a == 0 ? colX : (a == 1 ? colY : colZ);
    vec3 pp = vec3(2 * c); pp[a] += 1.0;
    if (sliceOn) { float s = dot(pp, sliceD); if (s < sliceLo || s > sliceHi) return 0; }
    if (now != 0u) { bool stays = n >= 3 && n <= 5; base = stays ? orient * 0.6 : colDies; return 1; }
    if (n == 4 || n == 5) { base = colBorn; return 4; }
    if (n == 3) { base = colNear; return 2; }
    return 0;
  }
  if (colorMode == 4) {                       // neighbourhood of the focus cell
    ivec3 pp = 2 * c; pp[a] += 1;
    ivec3 q = pp - focusP;
    vec3 orient = a == 0 ? colX : (a == 1 ? colY : colZ);
    if (q == ivec3(0)) { base = colFocus; return 1; }
    if (isNeighbour(q, focusA)) {
      int ds = int(dot(vec3(q), sliceD));
      base = ds <= -4 ? colDs0 : ds == -2 ? colDs1 : ds == 0 ? colDs2 : ds == 2 ? colDs3 : colDs4;
      scale = now != 0u ? faceScale : faceScale * 0.8;   // the neighbours are the subject: always drawn; dead ones a bit smaller
      return 1;
    }
    return now != 0u ? 3 : 0;
  }
  uint before = colorMode == 2 ? comp(cellBits(P, c), a) : now;
  vec3 p = vec3(2 * c); p[a] += 1.0;
  if (sliceOn) { float s = dot(p, sliceD); if (s < sliceLo || s > sliceHi) return 0; }
  bool inSet = inEditSet(p, a);
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
export const cellGLSL = () => CELL_GLSL;
