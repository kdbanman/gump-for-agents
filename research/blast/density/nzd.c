/* nzd.c (research/blast/density): the brute-force path of research/blast/noisy/nz.c, with coins whose bias may depend
 * on the depth of the cell they hit, a "shuffled" coin (the state of a random cell of the same layer), frozen coins,
 * and diagnostics of the watched face's excursions and of the layers under it.
 *
 * Vessel, rule, noise region, darts, life protocol: exactly nz.c's (see research/blast/noisy/README.md, "The chain,
 * exactly"). The only change is the coin a dart writes:
 *   - fair (bias exactly 1/2, the default): bit 0 of the dart's own 32-bit word, as in nz.c, so that with every bias
 *     1/2 the run is nz.c's bit for bit (same random stream, same BRUTE line);
 *   - bias p != 1/2: a comparison of a word of a SECOND random stream (sm2) with p 2^64; the main stream, hence the
 *     number, squares and order of the darts, is untouched;
 *   - "s" (shuffle): the current state of a uniformly random cell of the source set of that depth (sm2 picks it);
 *     source set = the whole layer at that depth under the watched face (all its cells in the hull), or, with
 *     NZD_SRC=core, only its cells at depth >= DO under every other face (= the replaced cells when DW <= depth).
 * Depth of a cell = (R - (x+y+z)) / 2, its depth under the watched face (0 = the face).
 *
 *   nzd R brute SEED GENS M [DW DO [BIAS]]
 *     BIAS: "f" (all fair) | a number p (all depths) | a list "k:v,k:v,...,*:v" (v = number, "f" or "s"; "*" = every
 *     depth not listed; default f). A biased coin has bias round(p 2^16) / 2^16, compared with 16 bits of sm2. Env NZD_GENERAL=1: bias 1/2 goes through the comparison path (a control: a
 *     different line, the same law). Env NZD_LAYERS=1: also the layer diagnostics (LAYER / LAG lines; slower).
 *     Env NZD_FROZEN=1: frozen coins: each cell of N is set ONCE per life (at the soup) to a coin of its bias and is
 *     then held at that value for the whole life (not stepped, no darts; M is ignored for the noise but kept in eps).
 *   -DLIB: the stepper and the noise for validation (validate.py).
 *
 * Output: the BRUTE line of nz.c (same fields), then
 *   BIAS ...                      the coin of each depth
 *   REC H h k N_k D_k C_k ...     excursions of the watched face: N_k = counted descents from >= H to <= k,
 *                                 D_k = those ending in the watched face's death (alone or tied) before the face is
 *                                 back at >= H, C_k = those ended by another face's death first (censored);
 *                                 the rest recovered. H = round(A/4) unless NZD_H is set.
 *   LAYER / LAG lines             (NZD_LAYERS=1) see layer_report().
 */
#define _GNU_SOURCE
#include <immintrin.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef uint64_t u64;
#define W 8
#define NL (64 * W)
#define NB 9
#define T0 200
#define SOUP 0.35
#define MAXD 64
typedef u64 vec __attribute__((vector_size(64), aligned(8)));
typedef uint16_t dart_t;

static int R, n, A, *co, *nb, nf[8], *fcell[8], nN, *Ncell, CB, B, DW = 6, DO = 3, *dep0, *dmo;
static u64 *a, *b;
static u64 sm, sm2;
static inline u64 rnd(void) { u64 z = (sm += 0x9e3779b97f4a7c15ULL); z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
  z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; return z ^ (z >> 31); }
static inline u64 rnd2(void) { u64 z = (sm2 += 0x9e3779b97f4a7c15ULL); z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
  z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; return z ^ (z >> 31); }

/* the coin of each depth: kind 0 fair (v & 1), 1 comparison with thr, 2 shuffle, 3 always 1 */
/* kind 4 (conditioned): the bias depends on m = the number of live face neighbours (depth 0) of the cell in the current
   state: cctab[d][m]; fnb = those neighbours */
static u64 cctab[MAXD][4]; static double ccb[MAXD][4]; static int *fnb, *nfnb;
static int ckind[MAXD]; static u64 cthr[MAXD]; static double cbias[MAXD]; static int *srcs[MAXD], nsrc[MAXD];
static int general = 0, frozen = 0, srccore = 0;
static int allfair = -1, allthr = -1;     /* caches of the noise loop's form; reset whenever a coin changes */

int geom_init(int R_, int dw, int dov) {
  R = R_; DW = dw; DO = dov;
  int L = 2 * R + 1; int *idx = malloc(sizeof(int) * L * L * L);
  for (int i = 0; i < L * L * L; i++) idx[i] = -1;
  co = malloc(sizeof(int) * 3 * L * L * L); n = 0;
  for (int pass = 0; pass < 2; pass++) {
    for (int x = -R; x <= R; x++) for (int y = -R; y <= R; y++) for (int z = -R; z <= R; z++) {
      if ((x & 1) + (y & 1) + (z & 1) != 1) continue;
      if (abs(x) + abs(y) + abs(z) > R) continue;
      if ((pass == 0) != (x + y + z == R)) continue;
      idx[((x + R) * L + (y + R)) * L + (z + R)] = n; co[3 * n] = x; co[3 * n + 1] = y; co[3 * n + 2] = z; n++;
    }
    if (pass == 0) A = n;
  }
  nb = malloc(sizeof(int) * 12 * n);
  for (int i = 0; i < n; i++) {
    int *p = co + 3 * i, ax = (p[0] & 1) ? 0 : (p[1] & 1) ? 1 : 2, bx = (ax + 1) % 3, cx = (ax + 2) % 3, k = 0, off[12][3];
    memset(off, 0, sizeof off);
    for (int sb = 2; sb >= -2; sb -= 4) for (int sc = 2; sc >= -2; sc -= 4) { off[k][bx] = sb; off[k][cx] = sc; k++; }
    for (int sa = 1; sa >= -1; sa -= 2) for (int t = 0; t < 2; t++) for (int st = 1; st >= -1; st -= 2) { off[k][ax] = sa; off[k][t ? cx : bx] = st; k++; }
    for (int j = 0; j < 12; j++) {
      int x = p[0] + off[j][0], y = p[1] + off[j][1], z = p[2] + off[j][2], v = -1;
      if (abs(x) <= R && abs(y) <= R && abs(z) <= R) v = idx[((x + R) * L + (y + R)) * L + (z + R)];
      nb[12 * i + j] = v < 0 ? n : v;
    }
  }
  Ncell = malloc(sizeof(int) * n); nN = 0; dep0 = malloc(sizeof(int) * n); dmo = malloc(sizeof(int) * n);
  for (int f = 0; f < 8; f++) { fcell[f] = malloc(sizeof(int) * n); nf[f] = 0; }
  for (int i = 0; i < n; i++) {
    int *p = co + 3 * i, in = 1; dmo[i] = 1 << 20;
    for (int f = 0; f < 8; f++) {
      int sx = (f & 1) ? -1 : 1, sy = (f & 2) ? -1 : 1, sz = (f & 4) ? -1 : 1, s = sx * p[0] + sy * p[1] + sz * p[2];
      if (s == R) fcell[f][nf[f]++] = i;
      if ((R - s) / 2 < (f ? DO : DW)) in = 0;
      if (f == 0) dep0[i] = (R - s) / 2; else if ((R - s) / 2 < dmo[i]) dmo[i] = (R - s) / 2;
    }
    if (in) Ncell[nN++] = i;
  }
  fnb = malloc(sizeof(int) * 3 * n); nfnb = malloc(sizeof(int) * n);
  for (int i = 0; i < n; i++) { nfnb[i] = 0; for (int j = 0; j < 12; j++) { int c = nb[12 * i + j]; if (c < n && dep0[c] == 0 && nfnb[i] < 3) fnb[3 * i + nfnb[i]++] = c; } }
  CB = 2; while ((1 << CB) < 4 * nN) CB++;
  B = 1 << CB;
  a = aligned_alloc(64, (size_t)(n + 1) * W * 8); b = aligned_alloc(64, (size_t)(n + 1) * W * 8);
  memset(a, 0, (size_t)(n + 1) * W * 8); memset(b, 0, (size_t)(n + 1) * W * 8);
  allfair = allthr = -1;
  for (int d = 0; d < MAXD; d++) { ckind[d] = 0; cbias[d] = 0.5; cthr[d] = 0; nsrc[d] = 0; srcs[d] = malloc(sizeof(int) * n); }
  for (int i = 0; i < n; i++) if (dep0[i] < MAXD && (!srccore || dmo[i] >= DO)) srcs[dep0[i]][nsrc[dep0[i]]++] = i;
  free(idx);
  return n;
}
/* set the coin of depth d: p in [0,1] (kind 0 if p == 1/2 and not general), or p < 0: shuffle. A biased coin is a
   comparison of 16 bits of sm2 with round(p 2^16): its exact bias is that integer / 2^16 (printed in the BIAS line). */
void set_coin(int d, double p) {
  allfair = allthr = -1;
  if (p < 0) { ckind[d] = 2; cbias[d] = -1; return; }
  if (p > 1) p = 1;
  if (p == 0.5 && !general) { ckind[d] = 0; cbias[d] = 0.5; return; }
  ckind[d] = 1; cthr[d] = (u64)floor(p * 65536.0 + 0.5); cbias[d] = cthr[d] / 65536.0;
}
void set_srccore(int c) {   /* rebuild the shuffle sources (validation) */
  srccore = c; for (int d = 0; d < MAXD; d++) nsrc[d] = 0;
  for (int i = 0; i < n; i++) if (dep0[i] < MAXD && (!srccore || dmo[i] >= DO)) srcs[dep0[i]][nsrc[dep0[i]]++] = i;
}
void set_general(int g) { general = g; }
void set_ccoin(int d, double p0, double p1, double p2) {   /* conditioned coin: bias p_m, m = live face neighbours */
  allfair = allthr = -1; ckind[d] = 4; cbias[d] = -2; double p[3] = {p0, p1, p2};
  for (int m = 0; m < 3; m++) { cctab[d][m] = (u64)floor((p[m] > 1 ? 1 : p[m]) * 65536.0 + 0.5); ccb[d][m] = cctab[d][m] / 65536.0; } }

#define FA(s, c, p, q, r) do { vec t_ = (p) ^ (q); s = t_ ^ (r); c = ((p) & (q)) | (t_ & (r)); } while (0)
static inline vec rule(const vec *x, vec me) {
  vec s0, c0, s1, c1, s2, c2, s3, c3, u, cu, b0, cv, p, cp, q, cq, b1, cw, b2, b3;
  FA(s0, c0, x[0], x[1], x[2]); FA(s1, c1, x[3], x[4], x[5]); FA(s2, c2, x[6], x[7], x[8]); FA(s3, c3, x[9], x[10], x[11]);
  FA(u, cu, s0, s1, s2); b0 = u ^ s3; cv = u & s3;
  FA(p, cp, c0, c1, c2); FA(q, cq, c3, cu, cv); b1 = p ^ q; cw = p & q;
  FA(b2, b3, cp, cq, cw);
  return ~b3 & ((b2 & ~b1) | (me & ~b2 & b1 & b0));     /* count 4, 5: alive; count 3: keeps its state */
}
static u64 *frz;     /* frozen values of the cells of N (frozen mode), nN x W */
static void step(void) {       /* one generation of gump on the hull */
  for (int i = 0; i < n; i++) {
    const int *q = nb + 12 * (size_t)i; vec x[12], me, o;
    for (int t = 0; t < 12; t++) memcpy(&x[t], a + (size_t)q[t] * W, 64);
    memcpy(&me, a + (size_t)i * W, 64); o = rule(x, me); memcpy(b + (size_t)i * W, &o, 64);
  }
  u64 *t = a; a = b; b = t;
  if (frozen) for (int j = 0; j < nN; j++) memcpy(a + (size_t)Ncell[j] * W, frz + (size_t)j * W, 64);
}
/* 16-bit words of sm2, made in blocks (the loop vectorizes): word i of a block is splitmix(sm2 + (i+1) golden) */
#define CBN 2048
static uint16_t cb16[4 * CBN]; static int cbpos = 4 * CBN;
static void cb_refill(void) {
  u64 base = sm2; u64 *o = (u64 *)cb16;
  for (int i = 0; i < CBN; i++) { u64 z = base + (u64)(i + 1) * 0x9e3779b97f4a7c15ULL; z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
    z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; o[i] = z ^ (z >> 31); }
  sm2 = base + (u64)CBN * 0x9e3779b97f4a7c15ULL; cbpos = 0;
}
static inline uint32_t bits16(void) { if (cbpos == 4 * CBN) cb_refill(); return cb16[cbpos++]; }
static inline u64 coin(int lane, int cell, uint32_t v) {
  int d = dep0[cell];
  switch (ckind[d]) {
    case 0: return v & 1;
    case 1: return bits16() < cthr[d];
    case 4: { int m = 0; for (int j = 0; j < nfnb[cell]; j++) m += (int)((a[(size_t)fnb[3 * cell + j] * W + (lane >> 6)] >> (lane & 63)) & 1);
      return bits16() < cctab[d][m]; }
    default: { uint32_t z = (bits16() << 16) | bits16(); int s = srcs[d][((u64)z * (u64)nsrc[d]) >> 32];
      return (a[(size_t)s * W + (lane >> 6)] >> (lane & 63)) & 1; }
  }
}
/* nz.c's noise_random, the coin replaced by coin(): of M darts at a board of B squares, the number that land on N is
   Binomial(M, |N|/B), and those land on uniformly random cells of N, in random order, each with its own coin. */
static void noise_random(int M) {
  static uint32_t cdf[4096]; static int cdfM = -1;
  if (M > 4000) { fprintf(stderr, "M > 4000 not supported\n"); exit(1); }
  if (cdfM != M) { double q = (double)nN / B, pk = pow(1 - q, M), c = 0;
    for (int k = 0; k <= M; k++) { c += pk; cdf[k] = c >= 1 ? 0xFFFFFFFFu : (uint32_t)(c * 4294967296.0); pk = pk * (M - k) / (k + 1) * q / (1 - q); }
    cdf[M] = 0xFFFFFFFFu; cdfM = M; }
  if (allfair < 0) { allfair = 1; for (int d = 0; d < MAXD; d++) if (ckind[d]) allfair = 0; }
  if (allfair) {      /* nz.c's loop verbatim */
    for (int l = 0; l < NL; l++) {
      u64 r = rnd(); uint32_t u = (uint32_t)r; int k = 0; while (cdf[k] <= u && k < M) k++;
      u64 *base = a + (l >> 6), bit = 1ULL << (l & 63); r >>= 32; int have = 1;
      for (int h = 0; h < k; h++) {
        if (!have) { r = rnd(); have = 2; }
        uint32_t v = (uint32_t)r; r >>= 32; have--;
        u64 *x = base + (size_t)Ncell[((u64)(v >> 1) * (u64)nN) >> 31] * W;
        *x = (*x & ~bit) | (-(u64)(v & 1) & bit);
      }
    }
    return;
  }
  static uint32_t *jthr;
  if (allthr < 0) { allthr = 1; free(jthr); jthr = malloc(sizeof(uint32_t) * nN);
    for (int j = 0; j < nN; j++) { int d = dep0[Ncell[j]]; if (ckind[d] == 2 || ckind[d] == 4) allthr = 0; jthr[j] = ckind[d] == 1 ? (uint32_t)cthr[d] : 32768u; } }
  if (allthr) {       /* every depth a comparison (a fair depth among biased ones: threshold 2^15, same law) */
    for (int l = 0; l < NL; l++) {
      u64 r = rnd(); uint32_t u = (uint32_t)r; int k = 0; while (cdf[k] <= u && k < M) k++;
      u64 *base = a + (l >> 6), bit = 1ULL << (l & 63); r >>= 32; int have = 1;
      if (cbpos + k > 4 * CBN) cb_refill();
      for (int h = 0; h < k; h++) {
        if (!have) { r = rnd(); have = 2; }
        uint32_t v = (uint32_t)r; r >>= 32; have--;
        int j = (int)(((u64)(v >> 1) * (u64)nN) >> 31);
        u64 *x = base + (size_t)Ncell[j] * W;
        *x = (*x & ~bit) | (-(u64)(cb16[cbpos++] < jthr[j]) & bit);
      }
    }
    return;
  }
  for (int l = 0; l < NL; l++) {
    u64 r = rnd(); uint32_t u = (uint32_t)r; int k = 0; while (cdf[k] <= u && k < M) k++;
    u64 *base = a + (l >> 6), bit = 1ULL << (l & 63); r >>= 32; int have = 1;
    for (int h = 0; h < k; h++) {
      if (!have) { r = rnd(); have = 2; }
      uint32_t v = (uint32_t)r; r >>= 32; have--;
      int cell = Ncell[((u64)(v >> 1) * (u64)nN) >> 31];
      u64 *x = base + (size_t)cell * W;
      *x = (*x & ~bit) | (-coin(l, cell, v) & bit);
    }
  }
}
static int pop[NL]; static u64 od[W], forb[8][W];
static void observe(void) {
  vec cc[NB]; for (int k = 0; k < NB; k++) cc[k] = (vec){0};
  for (int i = 0; i < A; i++) { vec x; memcpy(&x, a + (size_t)i * W, 64); for (int k = 0; k < NB; k++) { vec t = cc[k] & x; cc[k] ^= x; x = t; } }
  u64 c[NB][W]; for (int k = 0; k < NB; k++) memcpy(c[k], &cc[k], 64);
  for (int l = 0; l < NL; l++) { int p = 0; for (int k = 0; k < NB; k++) p |= (int)((c[k][l >> 6] >> (l & 63)) & 1) << k; pop[l] = p; }
  for (int w = 0; w < W; w++) od[w] = 0;
  for (int f = 1; f < 8; f++) {
    vec o = (vec){0};
    for (int k = 0; k < nf[f]; k++) { vec x; memcpy(&x, a + (size_t)fcell[f][k] * W, 64); o |= x; }
    memcpy(forb[f], &o, 64); for (int w = 0; w < W; w++) od[w] |= ~forb[f][w];
  }
}
static inline int ndead(int l) { int k = (pop[l] == 0); for (int f = 1; f < 8; f++) k += !((forb[f][l >> 6] >> (l & 63)) & 1); return k; }
#define SETTLE 4096
static short ring[NL][12]; static int run2[NL], run12[NL], rpos;
static inline int settled(int l) {
  short p = (short)pop[l]; int i2 = (rpos + 10) % 12;
  run2[l] = (ring[l][i2] == p) ? run2[l] + 1 : 0; run12[l] = (ring[l][rpos] == p) ? run12[l] + 1 : 0;
  ring[l][rpos] = p;
  if (run2[l] >= SETTLE || run12[l] >= SETTLE) { run2[l] = run12[l] = 0; return 1; }
  return 0;
}
static void lane_soup(int lane) { int w = lane >> 6, k = lane & 63; u64 bit = 1ULL << k; u64 thr = (u64)(SOUP * 18446744073709551616.0);
  for (int i = 0; i < n; i++) { u64 *x = a + (size_t)i * W + w; if (rnd() < thr) *x |= bit; else *x &= ~bit; }
  if (frozen) for (int j = 0; j < nN; j++) {      /* frozen coins: drawn once per life from sm2, held */
    int c = Ncell[j], d = dep0[c]; u64 v = ckind[d] == 1 ? (bits16() < cthr[d]) : (bits16() & 1);
    u64 *x = a + (size_t)c * W + w; if (v) *x |= bit; else *x &= ~bit;
    u64 *y = frz + (size_t)j * W + w; if (v) *y |= bit; else *y &= ~bit; }
}

/* ---- layer diagnostics (NZD_LAYERS=1) ---- */
#define NG 14
#define NLAG 12
static const int lagv[NLAG] = {0, 1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48};
static int ng, *gcell[NG], gn[NG]; static char gname[NG][16];
static int gpop[NG][NL];
/* face births and deaths per generation, keyed by the face's population the generation before; a birth is split by
   how many of the newborn's three neighbours below (two in layer 1, one in layer 2) were alive the generation before */
static int fbl[NL][7], ppop[NL], *below, nbelow[1024];
static double BBp[7][1024], DNp[1024];
static void face_births(void) {   /* after step (b = the previous state, its darts included), before the lanes loop */
  vec cnt[7][7]; for (int c = 0; c < 7; c++) for (int k = 0; k < 7; k++) cnt[c][k] = (vec){0};
  for (int i = 0; i < A; i++) {
    vec now, prev, s0 = (vec){0}, s1 = (vec){0}; memcpy(&now, a + (size_t)i * W, 64); memcpy(&prev, b + (size_t)i * W, 64);
    for (int j = 0; j < nbelow[i]; j++) { vec x; memcpy(&x, b + (size_t)below[3 * i + j] * W, 64); vec t = s0 & x; s0 ^= x; s1 ^= t; }
    vec born = now & ~prev, died = prev & ~now, e[7];
    e[0] = born & ~s0 & ~s1; e[1] = born & s0 & ~s1; e[2] = born & ~s0 & s1; e[3] = born & s0 & s1; e[4] = died;
    e[5] = ~prev & ~s0 & s1; e[6] = ~prev & s0 & s1;      /* dead face cells with 2 (3) live below: the supply */
    for (int c = 0; c < 7; c++) { vec x = e[c]; for (int k = 0; k < 7; k++) { vec t = cnt[c][k] & x; cnt[c][k] ^= x; x = t; } }
  }
  for (int c = 0; c < 7; c++) { u64 w[7][W]; for (int k = 0; k < 7; k++) memcpy(w[k], &cnt[c][k], 64);
    for (int l = 0; l < NL; l++) { int p = 0; for (int k = 0; k < 7; k++) p |= (int)((w[k][l >> 6] >> (l & 63)) & 1) << k; fbl[l][c] = p; } }
}
static double *Sg[NG], *Cg[NG], *Ng;          /* by face population p: sum of the group's population, of its square; count */
static double Lfw[NG][NLAG], Lbw[NG][NLAG], Lsx[NLAG], Lsy[NG][NLAG], Lsxx[NLAG], Lsyy[NG][NLAG], Lsx2[NG][NLAG], Lsy2[NG][NLAG], Ln[NLAG];
static short hx[NL][64], hy[NG][NL][64]; static int hpos, hval[NL];
static void count_group(int g) {
  vec cc[10]; for (int k = 0; k < 10; k++) cc[k] = (vec){0};
  for (int j = 0; j < gn[g]; j++) { vec x; memcpy(&x, a + (size_t)gcell[g][j] * W, 64); for (int k = 0; k < 10; k++) { vec t = cc[k] & x; cc[k] ^= x; x = t; } }
  u64 c[10][W]; for (int k = 0; k < 10; k++) memcpy(c[k], &cc[k], 64);
  for (int l = 0; l < NL; l++) { int p = 0; for (int k = 0; k < 10; k++) p |= (int)((c[k][l >> 6] >> (l & 63)) & 1) << k; gpop[g][l] = p; }
}
static void layer_init(void) {
  ng = 0;
  for (int k = 1; k <= 5; k++) {       /* full layer k; its core (depth >= DO under every other face) */
    for (int core = 0; core < 2; core++) { int g = ng++; gcell[g] = malloc(sizeof(int) * n); gn[g] = 0;
      for (int i = 0; i < n; i++) if (dep0[i] == k && (!core || dmo[i] >= DO)) gcell[g][gn[g]++] = i;
      sprintf(gname[g], core ? "core%d" : "full%d", k); }
  }
  { int g = ng++; gcell[g] = malloc(sizeof(int) * n); gn[g] = 0;
    for (int i = 0; i < n; i++) { if (dep0[i] >= 6 && dmo[i] >= DO) gcell[g][gn[g]++] = i; } sprintf(gname[g], "core6+"); }
  { int g = ng++; gcell[g] = malloc(sizeof(int) * n); gn[g] = 0;       /* the face's outer neighbours: layer 0 itself */
    for (int i = 0; i < n; i++) { if (dep0[i] == 0) gcell[g][gn[g]++] = i; } sprintf(gname[g], "face"); }
  for (int g = 0; g < ng; g++) { Sg[g] = calloc(A + 1, 8); Cg[g] = calloc(A + 1, 8); }
  below = malloc(sizeof(int) * 3 * A);
  for (int i = 0; i < A; i++) { nbelow[i] = 0; for (int j = 0; j < 12; j++) { int c = nb[12 * i + j]; if (c < n && (dep0[c] == 1 || dep0[c] == 2)) below[3 * i + nbelow[i]++] = c; } }
  for (int l = 0; l < NL; l++) ppop[l] = -1;
  Ng = calloc(A + 1, 8);
}
static void layer_accum(int l, int counted) {   /* after observe(); every group counted */
  int x = pop[l];
  if (counted && ppop[l] >= 0) { DNp[ppop[l]] += 1; for (int c = 0; c < 7; c++) BBp[c][ppop[l]] += fbl[l][c]; }
  ppop[l] = x;
  if (counted) { Ng[x] += 1; for (int g = 0; g < ng; g++) { Sg[g][x] += gpop[g][l]; Cg[g][x] += (double)gpop[g][l] * gpop[g][l]; } }
  hx[l][hpos] = (short)x; for (int g = 0; g < ng; g++) hy[g][l][hpos] = (short)gpop[g][l];
  hval[l]++;
  if (!counted) return;
  for (int j = 0; j < NLAG; j++) { int lg = lagv[j]; if (hval[l] <= lg) continue; int q = (hpos - lg) & 63;
    double xp = hx[l][q]; Ln[j] += 1; Lsx[j] += x; Lsxx[j] += (double)x * x;
    for (int g = 0; g < ng; g++) { double y = gpop[g][l], yp = hy[g][l][q];
      Lfw[g][j] += xp * y; Lbw[g][j] += yp * x; Lsy[g][j] += y; Lsyy[g][j] += y * y; Lsx2[g][j] += xp; Lsy2[g][j] += yp; } }
}
static double CMn[3][2][3], CMa[3][2][3], CMf[3][2][3];   /* [set: core1, core2, full1][all, pop <= 10][m]; CMf: changed since the last generation */
static void cond_measure(const u64 *cm) {   /* cm: counted lanes; after observe() */
  u64 low[W]; for (int w = 0; w < W; w++) low[w] = 0;
  for (int l = 0; l < NL; l++) if (pop[l] <= 10) low[l >> 6] |= 1ULL << (l & 63);
  for (int i = 0; i < n; i++) {
    int st = (dep0[i] == 1 && dmo[i] >= DO) ? 0 : (dep0[i] == 2 && dmo[i] >= DO) ? 1 : -1;
    for (int pass = 0; pass < 2; pass++) { int set = pass == 0 ? st : (dep0[i] == 1 ? 2 : -1); if (set < 0) continue;
      for (int w = 0; w < W; w++) { u64 s0 = 0, s1 = 0;
        for (int j = 0; j < nfnb[i]; j++) { u64 x = a[(size_t)fnb[3 * i + j] * W + w], t = s0 & x; s0 ^= x; s1 ^= t; }
        u64 me = a[(size_t)i * W + w], ch = me ^ b[(size_t)i * W + w], mm[3] = {~s0 & ~s1, s0 & ~s1, ~s0 & s1};
        for (int m = 0; m < 3; m++) { u64 q = mm[m] & cm[w];
          CMn[set][0][m] += __builtin_popcountll(q); CMa[set][0][m] += __builtin_popcountll(q & me);
          CMn[set][1][m] += __builtin_popcountll(q & low[w]); CMa[set][1][m] += __builtin_popcountll(q & me & low[w]);
          CMf[set][0][m] += __builtin_popcountll(q & ch); CMf[set][1][m] += __builtin_popcountll(q & ch & low[w]); } } } }
}
static void layer_report(void) {
  { const char *nm[3] = {"core1", "core2", "full1"};
    for (int s_ = 0; s_ < 3; s_++) { printf("CONDM %s : P(alive | m live face neighbours), all / face pop <= 10 :", nm[s_]);
      for (int m = 0; m < 3; m++) if (CMn[s_][0][m] > 0) printf(" m%d %.5f (%.3e) / %.5f (%.3e)", m, CMa[s_][0][m] / CMn[s_][0][m], CMn[s_][0][m],
          CMn[s_][1][m] ? CMa[s_][1][m] / CMn[s_][1][m] : -1.0, CMn[s_][1][m]);
      printf("\n");
      printf("CONDF %s : P(changed since the last generation | m), all / face pop <= 10 :", nm[s_]);
      for (int m = 0; m < 3; m++) if (CMn[s_][0][m] > 0) printf(" m%d %.5f / %.5f", m, CMf[s_][0][m] / CMn[s_][0][m], CMn[s_][1][m] ? CMf[s_][1][m] / CMn[s_][1][m] : -1.0);
      printf("\n"); } }
  /* LAYER g name ncells : overall density ; density given face population <= t for t = 3, 6, 10, 15 ; and a table by p */
  double tot = 0; for (int p = 0; p <= A; p++) tot += Ng[p];
  int thr[6] = {2, 4, 6, 10, 15, 20};
  for (int g = 0; g < ng; g++) {
    double s = 0, c = 0; for (int p = 0; p <= A; p++) { s += Sg[g][p]; c += Ng[p]; }
    printf("LAYER %s n %d density %.5f", gname[g], gn[g], s / c / gn[g]);
    for (int t = 0; t < 6; t++) { double st = 0, ct = 0; for (int p = 0; p <= thr[t] && p <= A; p++) { st += Sg[g][p]; ct += Ng[p]; }
      printf(" | pop<=%d %.5f (share %.2e)", thr[t], ct ? st / ct / gn[g] : -1.0, ct / tot); }
    printf("\n");
  }
  printf("DRIFT p : count births(0 below) births(1) births(2) births(3) deaths dead-with-2-below dead-with-3-below, per generation, keyed by the population before\n");
  for (int p = 0; p <= A; p++) if (DNp[p] > 0) printf("DRIFT %d : %.0f %.5f %.5f %.5f %.5f %.5f %.5f %.5f\n", p, DNp[p], BBp[0][p] / DNp[p], BBp[1][p] / DNp[p], BBp[2][p] / DNp[p], BBp[3][p] / DNp[p], BBp[4][p] / DNp[p], BBp[5][p] / DNp[p], BBp[6][p] / DNp[p]);
  for (int g = 0; g < ng; g++) { printf("BYPOP %s :", gname[g]); for (int p = 0; p <= A; p++) printf(" %d:%.4f:%.0f", p, Ng[p] ? Sg[g][p] / Ng[p] / gn[g] : -1.0, Ng[p]); printf("\n"); }
  /* LAG g : corr(face(t - lag), group(t)) [face leads] and corr(group(t - lag), face(t)) [group leads] */
  for (int g = 0; g < ng; g++) { printf("LAG %s :", gname[g]);
    for (int j = 0; j < NLAG; j++) { double N_ = Ln[j]; if (!N_) continue;
      double mx = Lsx[j] / N_, my = Lsy[g][j] / N_, mxp = Lsx2[g][j] / N_, myp = Lsy2[g][j] / N_;
      double vx = Lsxx[j] / N_ - mx * mx, vy = Lsyy[g][j] / N_ - my * my;
      double cf = (Lfw[g][j] / N_ - mxp * my) / sqrt(vx * vy), cb = (Lbw[g][j] / N_ - myp * mx) / sqrt(vx * vy);
      printf(" %d:%+.4f/%+.4f", lagv[j], cf, cb); }
    printf("\n"); }
}

#ifdef LIB
int v_A(void) { return A; }
int v_nN(void) { return nN; }
int v_B(void) { return B; }
void v_coords(int *out) { memcpy(out, co, sizeof(int) * 3 * n); }
void v_ncells(int *out) { memcpy(out, Ncell, sizeof(int) * nN); }
void v_dep0(int *out) { memcpy(out, dep0, sizeof(int) * n); }
int v_nsrc(int d) { return nsrc[d]; }
void v_srcs(int d, int *out) { memcpy(out, srcs[d], sizeof(int) * nsrc[d]); }
void v_clear(void) { memset(a, 0, (size_t)(n + 1) * W * 8); memset(b, 0, (size_t)(n + 1) * W * 8); }
void v_set(int lane, const uint8_t *cells) { for (int i = 0; i < n; i++) { u64 *p = a + (size_t)i * W + (lane >> 6); *p = (*p & ~(1ULL << (lane & 63))) | ((u64)(cells[i] & 1) << (lane & 63)); } }
void v_get(int lane, uint8_t *cells) { for (int i = 0; i < n; i++) cells[i] = (a[(size_t)i * W + (lane >> 6)] >> (lane & 63)) & 1; }
void v_step(void) { step(); observe(); }
void v_noise(int M) { noise_random(M); }
void v_seed(unsigned long long s) { sm = s * 0x2545F4914F6CDD1DULL + 7; sm2 = s * 0x9E3779B97F4A7C15ULL + 99991; }
int v_pop(int lane) { return pop[lane]; }
int v_od(int lane) { return (od[lane >> 6] >> (lane & 63)) & 1; }
int v_ndead(int lane) { return ndead(lane); }
void v_swap(int i, int j, int newnb) { nb[12 * i + j] = newnb; }
int v_nb(int i, int j) { return nb[12 * i + j]; }
#else
static void parse_bias(const char *s) {
  /* "f" | number | list k:v,...,*:v */
  for (int d = 1; d < MAXD; d++) set_coin(d, 0.5);      /* fair (the comparison path when NZD_GENERAL=1) */
  if (!s || !strcmp(s, "f")) return;
  if (!strchr(s, ':')) { double p = strcmp(s, "s") ? atof(s) : -1; for (int d = 1; d < MAXD; d++) set_coin(d, p); return; }
  char buf[1024]; strncpy(buf, s, 1023); buf[1023] = 0;
  double star = 0.5, cq[MAXD][3]; int have[MAXD] = {0}; double val[MAXD];
  for (char *tok = strtok(buf, ","); tok; tok = strtok(0, ",")) {
    char *c = strchr(tok, ':'); if (!c) { fprintf(stderr, "bad bias %s\n", tok); exit(2); } *c = 0;
    if (c[1] == 'c') { int d = atoi(tok); double q[3] = {0.5, 0.5, 0.5}; sscanf(c + 2, "%lf/%lf/%lf", q, q + 1, q + 2);
      if (d < 1 || d >= MAXD) exit(2);
      have[d] = 2; cq[d][0] = q[0]; cq[d][1] = q[1]; cq[d][2] = q[2]; continue; }
    double v = !strcmp(c + 1, "f") ? 0.5 : !strcmp(c + 1, "s") ? -1 : atof(c + 1);
    if (!strcmp(tok, "*")) star = v; else { int d = atoi(tok); if (d < 1 || d >= MAXD) exit(2); have[d] = 1; val[d] = v; }
  }
  for (int d = 1; d < MAXD; d++) { if (have[d] == 2) set_ccoin(d, cq[d][0], cq[d][1], cq[d][2]); else set_coin(d, have[d] ? val[d] : star); }
}
int main(int argc, char **argv) {
  if (argc < 6 || strcmp(argv[2], "brute")) { fprintf(stderr, "usage: nzd R brute SEED GENS M [DW DO [BIAS]]\n"); return 2; }
  u64 seed0 = strtoull(argv[3], 0, 10);
  if (getenv("NZD_GENERAL")) general = atoi(getenv("NZD_GENERAL"));
  if (getenv("NZD_SRC") && !strcmp(getenv("NZD_SRC"), "core")) srccore = 1;
  if (getenv("NZD_FROZEN")) frozen = atoi(getenv("NZD_FROZEN"));
  int layers = getenv("NZD_LAYERS") ? atoi(getenv("NZD_LAYERS")) : 0;
  long gens = atol(argv[4]); int M = atoi(argv[5]);
  geom_init(atoi(argv[1]), argc > 6 ? atoi(argv[6]) : 6, argc > 7 ? atoi(argv[7]) : 3);
  parse_bias(argc > 8 ? argv[8] : 0);
  if (frozen) { frz = aligned_alloc(64, (size_t)nN * W * 8 + 64); memset(frz, 0, (size_t)nN * W * 8); }
  int H = getenv("NZD_H") ? atoi(getenv("NZD_H")) : (int)floor(A / 4.0 + 0.5);
  if (layers) layer_init();
  sm = seed0 * 0x2545F4914F6CDD1DULL + 7; sm2 = seed0 * 0x9E3779B97F4A7C15ULL + 99991;
  static long age[NL]; double E = 0, dw = 0, sp = 0, spp = 0; long Dany = 0, n0 = 0, n0alone = 0, nsettled = 0, maxage = 0;
  /* excursions: arm[l] bit k = the face has been >= H since its last counted descent to <= k; pend[l] bit k = a
     counted descent to <= k is open (not yet recovered, dead or censored) */
  #define KR 16
  static uint32_t arm[NL], pend[NL]; long NK[KR] = {0}, DK[KR] = {0}, CK[KR] = {0}, RK[KR] = {0};
  for (int l = 0; l < NL; l++) { lane_soup(l); age[l] = 0; arm[l] = pend[l] = 0; }
  FILE *dump = getenv("NZD_DUMP") ? fopen(getenv("NZD_DUMP"), "wb") : 0;   /* validation: per generation 512 pops, 512 bytes odl */
  for (long g = 0; g < gens + T0; g++) {
    step(); if (M && !frozen) noise_random(M); observe();
    if (layers) { for (int q = 0; q < ng; q++) count_group(q); face_births();
      u64 cm[W]; for (int w = 0; w < W; w++) cm[w] = 0; for (int l = 0; l < NL; l++) if (g >= T0 && age[l] + 1 > T0) cm[l >> 6] |= 1ULL << (l & 63);
      cond_measure(cm); }
    if (dump) { static uint8_t buf[2 * NL]; for (int l = 0; l < NL; l++) { buf[l] = (uint8_t)pop[l]; buf[NL + l] = (uint8_t)((od[l >> 6] >> (l & 63)) & 1); } fwrite(buf, 1, 2 * NL, dump); }
    for (int l = 0; l < NL; l++) {
      age[l]++;
      int counted = (g >= T0 && age[l] > T0), dead0 = (pop[l] == 0), odl = (int)((od[l >> 6] >> (l & 63)) & 1);
      if (layers) layer_accum(l, counted);
      if (counted) { E += 1; if (!dead0 && !odl) { sp += pop[l]; spp += (double)pop[l] * pop[l]; } }
      /* excursions */
      { int p = pop[l];
        if (p >= H) { uint32_t m = pend[l]; while (m) { int k = __builtin_ctz(m); RK[k]++; m &= m - 1; } pend[l] = 0; arm[l] = (1u << KR) - 1; }
        else { uint32_t m = arm[l] & ((p < KR) ? ~((1u << p) - 1) : 0) & ((1u << KR) - 1);   /* armed k >= p */
          if (m) { arm[l] &= ~m; if (counted) { pend[l] |= m; uint32_t mm = m; while (mm) { NK[__builtin_ctz(mm)]++; mm &= mm - 1; } } } }
        if (dead0 || odl) { uint32_t m = pend[l]; while (m) { int k = __builtin_ctz(m); if (dead0) DK[k]++; else CK[k]++; m &= m - 1; } pend[l] = 0; arm[l] = 0; } }
      if (dead0 || odl) {
        if (counted) { Dany++; if (dead0) { n0++; dw += 1.0 / ndead(l); if (!odl) n0alone++; } }
        if (age[l] > maxage) maxage = age[l];
        lane_soup(l); age[l] = 0; if (layers) { hval[l] = 0; ppop[l] = -1; }
      } else if (settled(l)) { nsettled++; lane_soup(l); age[l] = 0; if (layers) { hval[l] = 0; ppop[l] = -1; } uint32_t m = pend[l]; while (m) { CK[__builtin_ctz(m)]++; m &= m - 1; } pend[l] = arm[l] = 0; }
    }
    rpos = (rpos + 1) % 12; if (layers) hpos = (hpos + 1) & 63;
  }
  double ns = E - Dany, pb = sp / ns;
  printf("BRUTE R %d A %d n %d DW %d DO %d nN %d B %d M %d eps %.6f seed %llu exposure %.6e deaths_any %ld watched %ld watched_alone %ld watched_weighted %.3f Pbar %.4f sigP %.4f",
         R, A, n, DW, DO, nN, B, M, (double)M / B, (unsigned long long)seed0, E, Dany, n0, n0alone, dw, pb, sqrt(spp / ns - pb * pb));
  if (Dany) printf(" lntau_any8 %.4f +- %.4f", log(8 * E / Dany), 1 / sqrt((double)Dany));
  if (n0) printf(" lntau_watched %.4f +- %.4f", log(E / n0), 1 / sqrt((double)n0));
  printf(" settled %ld longest_life %ld\n", nsettled, maxage);
  printf("BIAS seed %llu general %d frozen %d src %s :", (unsigned long long)seed0, general, frozen, srccore ? "core" : "layer");
  for (int d = DW; d <= R; d++) { int any = 0; for (int j = 0; j < nN; j++) if (dep0[Ncell[j]] == d) any++; if (!any) continue;
    if (ckind[d] == 2) printf(" %d(%d):s", d, any); else if (ckind[d] == 4) printf(" %d(%d):c%.4f/%.4f/%.4f", d, any, ccb[d][0], ccb[d][1], ccb[d][2]); else printf(" %d(%d):%.5f", d, any, cbias[d]); }
  printf("\n");
  printf("REC H %d :", H); for (int k = 0; k < KR; k++) printf(" %d:%ld/%ld/%ld", k, NK[k], DK[k], CK[k]); printf("\n");
  if (layers) layer_report();
  if (dump) fclose(dump);
  return 0;
}
#endif
