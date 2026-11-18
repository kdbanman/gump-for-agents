// holes.c -- blast/holes: empty patches in living faces of gump (B45/S345 on the faces of the cubic honeycomb).
// Own bit-sliced graph stepper, 256 lanes (independent replicas), written from reference/oracle.py and
// docs/AUTOMATON.md. Vessels: "slab n L" = L {111} layers, periodic in the plane with period lattice (n,0),(0,n)
// (3 n^2 cells per face, two faces); "hull R" = the octahedron |x|+|y|+|z| <= R in doubled coordinates (8 faces
// of 3k(k+1)/2 cells, k = (R+1)/2).
//
//   holes val slab n L SEED GENS NEG OUT        dump three lanes every generation for validate.py
//   holes val hull R 0 SEED GENS NEG OUT        (NEG=1: one swapped neighbour, the negative control)
//   holes run slab n L SEED GENS BURN OUT [TRACK]
//   holes run hull R 0 SEED GENS BURN OUT [TRACK]
//
// A unit cell is the three faces of one cube that lie in the face layer and point out of the vessel (a kagome
// triangle); on the hull face with outward diagonal (1,1,1) these are the cells with floor(x/2), floor(z/2),
// floor(y/2) = (i, j, m), i + j + m = k - 1, and i, j, m are the unit cell's distances from the three rims. A
// rhombus a x b at (I0, J0) is the unit cells I0 <= I < I0 + a, J0 <= J < J0 + b. Counted every generation: the
// number of lanes in which every cell of the rhombus is dead, for all a, b <= 8, by group of 32 lanes (8 groups
// = 8 independent sets of replicas, from which the errors are taken).
//   slab: four grids, 0 = top face class P (outward-pointing triangles, the hull's kind), 1 = top face class Q
//         (the inward-pointing triangles), 2 = bottom face class P, 3 = bottom face class Q; summed over the
//         n^2 translates.
//   hull: one table resolved by position (I0, J0), summed over the 8 faces and the 3 rotations of each face
//         (I, J) = (i, j), (j, m), (m, i).
// Shapes of a*b <= 4 unit cells are counted every 8th generation only (the stride is the 7th field of a T line).
// TRACK=1 also records how patches of 2x2, 3x3, 4x4 empty (class P only): at each generation at which a patch is
// empty and was not empty in any of the 4 generations before, the patch's population and the population of the
// cells of the second layer adjacent to it over the last 10 generations (2x2: every 64th generation only).
// Output: "T grid a b I0 J0 stride c0..c7" (counts by lane group) and "P grid a b I0 J0 n .. old .. re .. bust ..
// full .. nben .. face <10 lags> ben <10 lags> fall <21 bins>".
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <immintrin.h>

typedef uint64_t v4 __attribute__((vector_size(32)));
#define MAXC 24000
#define GMAX 18
#define AM 8
#define BM 8
#define NGRP 8
#define NLAG 10
#define RINGMAX 12
#define NTR 3
#define PL 16
#define SUBS 8   // shapes of a*b <= 4 unit cells are counted every SUBS-th generation only
static const int TA[NTR] = {2, 3, 4}, TB[NTR] = {2, 3, 4};

static int N, isSlab, SN, SL, HR;
static int cx[MAXC], cy[MAXC], cz[MAXC], lay[MAXC], nb[MAXC][12];
static v4 *S[RINGMAX];
static int ring = 2;

typedef struct {
  uint64_t n, nold, nre, nbust, nfull, fallhist[21];
  double sface[NLAG], sben[NLAG], nbensum;
} Pre;
typedef struct {
  int G, wrap, npos, track;
  int cell[GMAX][GMAX][3], ben[GMAX][GMAX][6];
  uint64_t *tab;      // [(a-1)][(b-1)][pos][grp]
  v4 *vc;             // bit-sliced counters over time, [(a-1)][(b-1)][pos][PL planes], flushed into tab
  unsigned char *touched;
  Pre *pre;           // [NTR][npos]
} Grid;
static Grid *grids; static int ngrid;
static int *facecells[8], nface[8], nfaces;
static uint64_t facedeaths, facepop, facepopn;

static uint64_t rs[4];
static inline uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static inline uint64_t rnd(void) {
  uint64_t r = rotl(rs[0] + rs[3], 23) + rs[0], t = rs[1] << 17;
  rs[2] ^= rs[0]; rs[3] ^= rs[1]; rs[1] ^= rs[2]; rs[0] ^= rs[3]; rs[2] ^= t; rs[3] = rotl(rs[3], 45);
  return r;
}
static void seedrng(uint64_t s) {
  for (int i = 0; i < 4; i++) {
    s += 0x9E3779B97F4A7C15ULL; uint64_t z = s;
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL; z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL; rs[i] = z ^ (z >> 31);
  }
}

// the 12 neighbour offsets of a face with normal axis a, as in reference/oracle.py offsets()
static void offsets(int a, int o[12][3]) {
  int b = (a == 0) ? 1 : 0, c = (a == 2) ? 1 : 2, k = 0;
  for (int sb = 2; sb >= -2; sb -= 4) for (int sc = 2; sc >= -2; sc -= 4) {
    o[k][0] = o[k][1] = o[k][2] = 0; o[k][b] = sb; o[k][c] = sc; k++;
  }
  for (int sa = 1; sa >= -1; sa -= 2) for (int ti = 0; ti < 2; ti++) for (int st = 1; st >= -1; st -= 2) {
    int t = ti ? c : b;
    o[k][0] = o[k][1] = o[k][2] = 0; o[k][a] = sa; o[k][t] = st; k++;
  }
}
static inline int fdiv2(int v) { return (v >= 0) ? v / 2 : -((-v + 1) / 2); }
static inline int pmod(int v, int n) { v %= n; return v < 0 ? v + n : v; }

// ---- slab: cell (l, x, y, a) is the +a face of cube (i, j, k) = (x, -x-y, y+l); index ((l n + x) n + y) 3 + a
static inline int sidx(int l, int x, int y, int a) { return ((l * SN + pmod(x, SN)) * SN + pmod(y, SN)) * 3 + a; }
static void build_slab(int n, int L) {
  isSlab = 1; SN = n; SL = L; N = 3 * n * n * L;
  for (int l = 0; l < L; l++) for (int x = 0; x < n; x++) for (int y = 0; y < n; y++) for (int a = 0; a < 3; a++) {
    int c = sidx(l, x, y, a), cu[3] = {x, -x - y, y + l}, p[3], o[12][3];
    for (int d = 0; d < 3; d++) p[d] = 2 * cu[d] + (d == a);
    cx[c] = p[0]; cy[c] = p[1]; cz[c] = p[2]; lay[c] = l;
    offsets(a, o);
    for (int q = 0; q < 12; q++) {
      int r[3] = {p[0] + o[q][0], p[1] + o[q][1], p[2] + o[q][2]};
      int a2 = (r[0] & 1) ? 0 : (r[1] & 1) ? 1 : 2;
      int c2[3]; for (int d = 0; d < 3; d++) c2[d] = fdiv2(r[d] - (d == a2));
      int l2 = c2[0] + c2[1] + c2[2];
      nb[c][q] = (l2 < 0 || l2 >= L) ? N : sidx(l2, c2[0], c2[2] - l2, a2);
    }
  }
}
// ---- hull
static int *hidx; static int HW;
static inline int hget(int x, int y, int z) {
  if (abs(x) + abs(y) + abs(z) > HR) return -1;
  return hidx[((x + HR) * HW + (y + HR)) * HW + (z + HR)];
}
static void build_hull(int R) {
  isSlab = 0; HR = R; HW = 2 * R + 1; hidx = malloc(sizeof(int) * HW * HW * HW); N = 0;
  for (int x = -R; x <= R; x++) for (int y = -R; y <= R; y++) for (int z = -R; z <= R; z++) {
    int *h = &hidx[((x + R) * HW + (y + R)) * HW + (z + R)]; *h = -1;
    if (abs(x) + abs(y) + abs(z) > R) continue;
    if ((abs(x) & 1) + (abs(y) & 1) + (abs(z) & 1) != 1) continue;
    if (N >= MAXC) { fprintf(stderr, "MAXC\n"); exit(1); }
    *h = N; cx[N] = x; cy[N] = y; cz[N] = z; lay[N] = 0; N++;
  }
  for (int c = 0; c < N; c++) {
    int p[3] = {cx[c], cy[c], cz[c]}, a = (abs(p[0]) & 1) ? 0 : (abs(p[1]) & 1) ? 1 : 2, o[12][3];
    offsets(a, o);
    for (int q = 0; q < 12; q++) { int h = hget(p[0] + o[q][0], p[1] + o[q][1], p[2] + o[q][2]); nb[c][q] = h < 0 ? N : h; }
  }
}

// ---- the stepper: B45/S345 on 256 lanes
#define FA(a, b, c, s, k) { v4 _x = (a) ^ (b); s = _x ^ (c); k = ((a) & (b)) | ((c) & _x); }
#define HA(a, b, s, k) { s = (a) ^ (b); k = (a) & (b); }
static void step(const v4 *restrict s, v4 *restrict t) {
  for (int c = 0; c < N; c++) {
    const int *b = nb[c];
    v4 s1, s2, s3, s4, c1, c2, c3, c4, u, c5, b0, c6, v1, v2, d1, d2, b1, d3, b2, b3;
    FA(s[b[0]], s[b[1]], s[b[2]], s1, c1); FA(s[b[3]], s[b[4]], s[b[5]], s2, c2);
    FA(s[b[6]], s[b[7]], s[b[8]], s3, c3); FA(s[b[9]], s[b[10]], s[b[11]], s4, c4);
    FA(s1, s2, s3, u, c5); HA(u, s4, b0, c6);
    FA(c1, c2, c3, v1, d1); FA(c4, c5, c6, v2, d2); HA(v1, v2, b1, d3);
    FA(d1, d2, d3, b2, b3);
    t[c] = ~b3 & ((b2 & ~b1) | (s[c] & ~b2 & b1 & b0));
  }
  t[N] = (v4){0, 0, 0, 0};
}
static inline int nz(v4 v) { return !_mm256_testz_si256((__m256i)v, (__m256i)v); }

// ---- grids
static void *zalloc(size_t n) { n = (n + 63) & ~(size_t)63; void *p = aligned_alloc(64, n); memset(p, 0, n); return p; }
static Grid *newgrid(int G, int wrap, int npos, Grid *share, int track) {
  Grid *g = &grids[ngrid++]; memset(g, 0, sizeof *g);
  g->G = G; g->wrap = wrap; g->npos = npos; g->track = track;
  size_t nc = (size_t)AM * BM * npos;
  g->tab = share ? share->tab : zalloc(nc * NGRP * 8);
  g->vc = share ? share->vc : zalloc(nc * PL * sizeof(v4));
  g->touched = share ? share->touched : zalloc(nc);
  g->pre = share ? share->pre : zalloc((size_t)NTR * npos * sizeof(Pre));
  for (int I = 0; I < GMAX; I++) for (int J = 0; J < GMAX; J++) {
    for (int q = 0; q < 3; q++) g->cell[I][J][q] = -1;
    for (int q = 0; q < 6; q++) g->ben[I][J][q] = -1;
  }
  return g;
}
static void addben(Grid *g, int I, int J, int c) {
  for (int q = 0; q < 6; q++) { if (g->ben[I][J][q] == c) return; if (g->ben[I][J][q] < 0) { g->ben[I][J][q] = c; return; } }
}
static void grids_slab(void) {
  int n = SN, L = SL; grids = zalloc(4 * sizeof(Grid)); nfaces = 2;
  for (int f = 0; f < 2; f++) {
    int l = f ? 0 : L - 1, lb = f ? 1 : L - 2;
    facecells[f] = malloc(sizeof(int) * 3 * n * n); nface[f] = 0;
    for (int x = 0; x < n; x++) for (int y = 0; y < n; y++) for (int a = 0; a < 3; a++) facecells[f][nface[f]++] = sidx(l, x, y, a);
    for (int cls = 0; cls < 2; cls++) {       // cls 0 = P (hull-like), 1 = Q
      // top face: P = the three +faces of a cube (site (x,y)); bottom face: P = the three -faces of a cube
      int minus = (f == 0) ? cls : !cls;
      Grid *g = newgrid(n, 1, 1, NULL, cls == 0);
      for (int X = 0; X < n; X++) for (int Y = 0; Y < n; Y++) {
        if (!minus) for (int a = 0; a < 3; a++) g->cell[X][Y][a] = sidx(l, X, Y, a);
        else { g->cell[X][Y][0] = sidx(l, X - 1, Y + 1, 0); g->cell[X][Y][1] = sidx(l, X, Y + 1, 1); g->cell[X][Y][2] = sidx(l, X, Y, 2); }
        for (int q = 0; q < 3; q++) { int c = g->cell[X][Y][q]; for (int e = 0; e < 12; e++) { int d = nb[c][e]; if (d < N && lay[d] == lb) addben(g, X, Y, d); } }
      }
    }
  }
}
static void grids_hull(void) {
  int R = HR, k = (R + 1) / 2; grids = zalloc(24 * sizeof(Grid)); nfaces = 8;
  for (int f = 0; f < 8; f++) {
    int sg[3] = {(f & 1) ? -1 : 1, (f & 2) ? -1 : 1, (f & 4) ? -1 : 1};
    facecells[f] = malloc(sizeof(int) * 3 * k * (k + 1) / 2); nface[f] = 0;
    Grid *g[3]; for (int pm = 0; pm < 3; pm++) g[pm] = newgrid(k, 0, k * k, ngrid ? &grids[0] : NULL, 1);
    for (int c = 0; c < N; c++) {
      int q[3] = {sg[0] * cx[c], sg[1] * cy[c], sg[2] * cz[c]};
      if (q[0] + q[1] + q[2] != R) continue;
      facecells[f][nface[f]++] = c;
      int i = q[0] / 2, m = q[1] / 2, j = q[2] / 2, slot = (q[0] & 1) ? 0 : (q[1] & 1) ? 1 : 2;
      int IJ[3][2] = {{i, j}, {j, m}, {m, i}};
      for (int pm = 0; pm < 3; pm++) {
        g[pm]->cell[IJ[pm][0]][IJ[pm][1]][slot] = c;
        for (int e = 0; e < 12; e++) { int d = nb[c][e]; if (d < N && sg[0] * cx[d] + sg[1] * cy[d] + sg[2] * cz[d] == R - 2) addben(g[pm], IJ[pm][0], IJ[pm][1], d); }
      }
    }
    if (nface[f] != 3 * k * (k + 1) / 2) { fprintf(stderr, "face count\n"); exit(1); }
  }
}

static long tnow;
static void record(Grid *g, int s, int I0, int J0, int lane) {
  static int stamp[MAXC + 1], sid;
  int a = TA[s], b = TB[s], G = g->G, fc[3 * 64], nf = 0, bc[6 * 64], nbn = 0;
  sid++;
  for (int i = 0; i < a; i++) for (int j = 0; j < b; j++) {
    int I = I0 + i, J = J0 + j; if (g->wrap) { I %= G; J %= G; }
    for (int q = 0; q < 3; q++) fc[nf++] = g->cell[I][J][q];
    for (int q = 0; q < 6; q++) { int c = g->ben[I][J][q]; if (c >= 0 && stamp[c] != sid) { stamp[c] = sid; bc[nbn++] = c; } }
  }
  int w = lane >> 6, bit = lane & 63, pf[NLAG], pb[NLAG];
  for (int lag = 0; lag < NLAG; lag++) {
    const v4 *st = S[(tnow - lag + 4 * ring) % ring]; int x = 0, y = 0;
    for (int q = 0; q < nf; q++) x += (st[fc[q]][w] >> bit) & 1;
    for (int q = 0; q < nbn; q++) y += (st[bc[q]][w] >> bit) & 1;
    pf[lag] = x; pb[lag] = y;
  }
  Pre *p = &g->pre[s * g->npos + (g->npos > 1 ? I0 * G + J0 : 0)];
  if (pf[1] == 0) { p->nold++; return; }      // already empty one generation ago: not a new emptying
  for (int lag = 2; lag <= 4; lag++) if (pf[lag] == 0) { p->nre++; return; }   // a flicker of an emptied patch
  p->n++; p->nbensum += nbn;
  int maxfall = 0, maxpop = 0;
  for (int lag = 0; lag < NLAG; lag++) {
    p->sface[lag] += (double)pf[lag] / nf; p->sben[lag] += (double)pb[lag] / nbn;
    if (pf[lag] > maxpop) maxpop = pf[lag];
    if (lag + 1 < NLAG && pf[lag + 1] - pf[lag] > maxfall) maxfall = pf[lag + 1] - pf[lag];
  }
  if (2 * maxfall >= nf) p->nbust++;
  if (10 * maxpop >= 7 * nf) p->nfull++;
  p->fallhist[(20 * maxfall) / nf]++;
}

static v4 E[GMAX][GMAX], Ra[GMAX][GMAX], Rb[GMAX][GMAX];
static inline void vadd(v4 *pl, v4 v) {
  for (int k = 0; k < PL; k++) { v4 t = pl[k]; pl[k] = t ^ v; v &= t; if (!nz(v)) return; }
  fprintf(stderr, "counter overflow\n"); exit(1);
}
static void flush(Grid *g) {
  size_t nc = (size_t)AM * BM * g->npos;
  for (size_t q = 0; q < nc; q++) if (g->touched[q]) {
    v4 *pl = g->vc + q * PL; uint64_t *t8 = g->tab + q * NGRP;
    for (int k = 0; k < PL; k++) {
      v4 v = pl[k];
      if (nz(v)) for (int w = 0; w < 4; w++) {
        t8[2 * w] += (uint64_t)__builtin_popcountll(v[w] & 0xffffffffULL) << k; t8[2 * w + 1] += (uint64_t)__builtin_popcountll(v[w] >> 32) << k;
      }
      pl[k] = (v4){0, 0, 0, 0};
    }
    g->touched[q] = 0;
  }
}
static void count_grid(const v4 *st, Grid *g, int dotrack, int sub, int sub64) {
  const int G = g->G, wrap = g->wrap, npos = g->npos;
  const v4 zero = {0, 0, 0, 0};
  int rowA[GMAX], rowB[GMAX];
  for (int I = 0; I < G; I++) {
    int any = 0;
    for (int J = 0; J < G; J++) {
      const int *c = g->cell[I][J];
      v4 e = (c[0] < 0) ? zero : ~(st[c[0]] | st[c[1]] | st[c[2]]);
      E[I][J] = e; Ra[I][J] = e; any |= nz(e);
    }
    rowA[I] = any;
  }
  for (int a = 1; a <= AM; a++) {
    if (a > 1) {
      int anyall = 0;
      for (int I = 0; I < G; I++) {
        if (!rowA[I]) continue;
        int I2 = I + a - 1;
        if (I2 >= G) { if (!wrap) { rowA[I] = 0; continue; } I2 -= G; }
        int any = 0;
        for (int J = 0; J < G; J++) { v4 v = Ra[I][J] & E[I2][J]; Ra[I][J] = v; any |= nz(v); }
        rowA[I] = any; anyall |= any;
      }
      if (!anyall) break;
    }
    for (int I = 0; I < G; I++) { rowB[I] = rowA[I]; if (rowA[I]) for (int J = 0; J < G; J++) Rb[I][J] = Ra[I][J]; }
    for (int b = 1; b <= BM; b++) {
      if (b > 1) {
        int anyall = 0;
        for (int I = 0; I < G; I++) {
          if (!rowB[I]) continue;
          int any = 0;
          for (int J = 0; J < G; J++) {
            int J2 = J + b - 1;
            if (J2 >= G) { if (!wrap) { Rb[I][J] = zero; continue; } J2 -= G; }
            v4 v = Rb[I][J] & Ra[I][J2]; Rb[I][J] = v; any |= nz(v);
          }
          rowB[I] = any; anyall |= any;
        }
        if (!anyall) break;
      }
      const size_t q0 = (size_t)((a - 1) * BM + (b - 1)) * npos;
      const int docount = (a * b > 4) || sub;
      int s = -1;
      if (dotrack && g->track && a == b) for (int q = 0; q < NTR; q++) if (TA[q] == a) s = q;
      if (s == 0 && !sub64) s = -1;          // 2x2 is frequent: its histories are sampled every 64th generation
      if (!docount && s < 0) continue;
      for (int I = 0; I < G; I++) {
        if (!rowB[I]) continue;
        for (int J = 0; J < G; J++) {
          v4 v = Rb[I][J];
          if (!nz(v)) continue;
          if (docount) { size_t q = q0 + (npos > 1 ? I * G + J : 0); vadd(g->vc + q * PL, v); g->touched[q] = 1; }
          if (s >= 0) for (int w = 0; w < 4; w++) { uint64_t x = v[w]; while (x) { int bit = __builtin_ctzll(x); x &= x - 1; record(g, s, I, J, 64 * w + bit); } }
        }
      }
    }
  }
}

static void facecheck(const v4 *st) {
  for (int f = 0; f < nfaces; f++) {
    v4 o = {0, 0, 0, 0};
    for (int q = 0; q < nface[f]; q++) { v4 v = st[facecells[f][q]]; o |= v; for (int w = 0; w < 4; w++) facepop += __builtin_popcountll(v[w]); }
    facepopn += 256ULL * nface[f];
    for (int w = 0; w < 4; w++) facedeaths += __builtin_popcountll(~o[w]);
  }
}

static void dump(const char *out, int argc, char **argv, long ngen, double secs, uint64_t seed) {
  char tmp[600]; snprintf(tmp, sizeof tmp, "%s.tmp", out);
  FILE *F = fopen(tmp, "w"); if (!F) { perror(tmp); exit(1); }
  fprintf(F, "# holes"); for (int i = 1; i < argc; i++) fprintf(F, " %s", argv[i]); fprintf(F, "\n");
  fprintf(F, "H vessel %s n %d L %d R %d N %d seed %llu gens %ld secs %.1f lanes 256 groups %d facecells %d faces %d\n",
          isSlab ? "slab" : "hull", SN, SL, HR, N, (unsigned long long)seed, ngen, secs, NGRP, nface[0], nfaces);
  fprintf(F, "H facedensity %.6f emptyfacechecks %llu\n", facepopn ? (double)facepop / facepopn : 0.0, (unsigned long long)facedeaths);
  int ntab = isSlab ? 4 : 1;
  for (int gi = 0; gi < ntab; gi++) {
    Grid *g = &grids[gi]; flush(g);
    for (int a = 1; a <= AM; a++) for (int b = 1; b <= BM; b++) for (int pos = 0; pos < g->npos; pos++) {
      uint64_t *t8 = g->tab + ((size_t)((a - 1) * BM + (b - 1)) * g->npos + pos) * NGRP, tot = 0;
      for (int q = 0; q < NGRP; q++) tot += t8[q];
      if (!tot) continue;
      fprintf(F, "T %d %d %d %d %d %d", gi, a, b, g->npos > 1 ? pos / g->G : 0, g->npos > 1 ? pos % g->G : 0, a * b > 4 ? 1 : SUBS);
      for (int q = 0; q < NGRP; q++) fprintf(F, " %llu", (unsigned long long)t8[q]);
      fprintf(F, "\n");
    }
    if (isSlab && gi % 2 == 1) continue;
    for (int s = 0; s < NTR; s++) for (int pos = 0; pos < g->npos; pos++) {
      Pre *p = &g->pre[s * g->npos + pos]; if (!p->n && !p->nre && !p->nold) continue;
      fprintf(F, "P %d %d %d %d %d n %llu old %llu re %llu bust %llu full %llu nben %.2f face", gi, TA[s], TB[s], g->npos > 1 ? pos / g->G : 0,
              g->npos > 1 ? pos % g->G : 0, (unsigned long long)p->n, (unsigned long long)p->nold, (unsigned long long)p->nre, (unsigned long long)p->nbust,
              (unsigned long long)p->nfull, p->n ? p->nbensum / p->n : 0.0);
      for (int l = 0; l < NLAG; l++) fprintf(F, " %.4f", p->n ? p->sface[l] / p->n : 0.0);
      fprintf(F, " ben"); for (int l = 0; l < NLAG; l++) fprintf(F, " %.4f", p->n ? p->sben[l] / p->n : 0.0);
      fprintf(F, " fall"); for (int l = 0; l < 21; l++) fprintf(F, " %llu", (unsigned long long)p->fallhist[l]);
      fprintf(F, "\n");
    }
  }
  fclose(F); rename(tmp, out);
}

int main(int argc, char **argv) {
  if (argc < 9) { fprintf(stderr, "usage: see header\n"); return 1; }
  int isval = !strcmp(argv[1], "val"), slab = !strcmp(argv[2], "slab");
  int p1 = atoi(argv[3]), p2 = atoi(argv[4]); uint64_t seed = strtoull(argv[5], 0, 10); long gens = atol(argv[6]);
  if (slab) build_slab(p1, p2); else build_hull(p1);
  if (isval) {
    int neg = atoi(argv[7]); const char *out = argv[8];
    if (neg) { int c = N / 2; nb[c][0] = nb[(c + 7) % N][3]; }
    for (int r = 0; r < 2; r++) S[r] = aligned_alloc(32, sizeof(v4) * (N + 1));
    seedrng(seed);
    for (int c = 0; c < N; c++) for (int w = 0; w < 4; w++) S[0][c][w] = rnd();
    S[0][N] = (v4){0, 0, 0, 0};
    FILE *F = fopen(out, "w");
    int off = slab ? 0 : HR + 3, H = slab ? 2 * SN : 2 * (HR + 3);
    fprintf(F, "%d %d %ld\n", N, H, gens);
    for (int c = 0; c < N; c++) fprintf(F, "%d %d %d\n", slab ? pmod(cx[c], H) : cx[c] + off, slab ? pmod(cy[c], H) : cy[c] + off, slab ? pmod(cz[c], H) : cz[c] + off);
    static const int lanes[3] = {0, 77, 255};
    char *buf = malloc(N + 2);
    for (long t = 0; t <= gens; t++) {
      const v4 *st = S[t & 1];
      for (int q = 0; q < 3; q++) { for (int c = 0; c < N; c++) buf[c] = '0' + ((st[c][lanes[q] >> 6] >> (lanes[q] & 63)) & 1); buf[N] = '\n'; fwrite(buf, 1, N + 1, F); }
      step(S[t & 1], S[(t + 1) & 1]);
    }
    fclose(F); return 0;
  }
  long burn = atol(argv[7]); const char *out = argv[8]; int track = argc > 9 ? atoi(argv[9]) : 0;
  ring = track ? RINGMAX : 2;
  if (slab) grids_slab(); else grids_hull();
  for (int r = 0; r < ring; r++) S[r] = aligned_alloc(32, sizeof(v4) * (N + 1));
  seedrng(seed);
  for (int c = 0; c < N; c++) for (int w = 0; w < 4; w++) S[0][c][w] = rnd();
  S[0][N] = (v4){0, 0, 0, 0};
  struct timespec t0, t1; clock_gettime(CLOCK_MONOTONIC, &t0);
  long ngen = 0, nextdump = 20000;
  const long flushper = isSlab ? 60000 / (SN * SN) : 60000 / 24;   // adds into one counter between flushes < 2^16
  for (long t = 0; t < burn + gens; t++) {
    step(S[t % ring], S[(t + 1) % ring]);
    tnow = t + 1;
    if (t + 1 > burn) {
      const v4 *st = S[(t + 1) % ring];
      int dotrack = track && (t + 1 > burn + NLAG + 1);
      ngen++;
      for (int gi = 0; gi < ngrid; gi++) count_grid(st, &grids[gi], dotrack, (ngen % SUBS) == 0, (ngen % 64) == 0);
      if (ngen % flushper == 0) for (int gi = 0; gi < (isSlab ? 4 : 1); gi++) flush(&grids[gi]);
      if ((ngen & 63) == 0) facecheck(st);
      if (ngen == nextdump || t + 1 == burn + gens) {
        clock_gettime(CLOCK_MONOTONIC, &t1);
        dump(out, argc, argv, ngen, (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec), seed);
        nextdump = ngen * 2 < ngen + 400000 ? ngen * 2 : ngen + 400000;
      }
    }
  }
  clock_gettime(CLOCK_MONOTONIC, &t1);
  fprintf(stderr, "done %ld gens %.1f s\n", ngen, (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec));
  return 0;
}
