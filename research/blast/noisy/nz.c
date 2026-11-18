/* nz.c (research/blast/noisy): epsilon-noisy gump on the whole octahedral hull.
 *
 * Vessel: every cell p (doubled coordinates, exactly one odd) with |x|+|y|+|z| <= R, R odd; neighbours the oracle's
 * twelve, a neighbour outside the hull dead. All eight faces are real (face f: the cells with d_f . p = R; face 0 is
 * d = (+,+,+), the watched face, and its cells come first). Rule: gump, B45/S345, on every cell.
 * Noise: after every generation, M "darts" are thrown at a board of B = 2^CB squares, of which the first |N| are the
 * cells of the noise region N (in the order of the cell table) and the rest are empty; a dart on a cell replaces that
 * cell by the dart's own fair coin (darts in order, a later one overrides). B is the smallest power of two >= 4 |N|.
 * So each cell of N is replaced with probability about eps = M / B per generation, nearly independently; M = 0 is gump.
 * N = cells at depth >= DW under the watched face and >= DO under every other face (depth of p under face f:
 * (R - d_f . p) / 2).  Default DW = 6, DO = 3.
 *
 * Life protocol (the anchors'): a hull starts as a soup (each cell alive with probability 0.35), age 0; a life ends at
 * the first generation at which any of the eight faces is empty.
 *
 *   nz R brute SEED GENS M [DW DO]
 *        512 hulls, plain running for GENS generations after 200 of ageing-in; a hull-generation counts (exposure) when
 *        the hull's age after the step exceeds 200. Prints the exposure, the first deaths of any face, and the lives
 *        ended by the watched face (alone or tied).
 *   nz R sub SEED NREP LAM1 DELTA NBATCH NSWEEP KFLIP TPRE TWIN WBACK M [DW DO [PATHFILE]]
 *        subset simulation over the darts (split-slab's sampler, see README.md for the exact statement).
 *   -DLIB: the stepper for validation against reference/oracle.py (validate.py).
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
#define BURN 1000
#define SOUP 0.35
typedef u64 vec __attribute__((vector_size(64), aligned(8)));
typedef uint16_t dart_t;            /* bits 0..CB-1: square of the board; bit 15: the coin */

static int R, n, A, *co, *nb, nf[8], *fcell[8], nN, *Ncell, CB, B, DW = 6, DO = 3;
static u64 *a, *b;
static u64 sm;
static inline u64 rnd(void) { u64 z = (sm += 0x9e3779b97f4a7c15ULL); z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
  z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; return z ^ (z >> 31); }

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
  Ncell = malloc(sizeof(int) * n); nN = 0;
  for (int f = 0; f < 8; f++) { fcell[f] = malloc(sizeof(int) * n); nf[f] = 0; }
  for (int i = 0; i < n; i++) {
    int *p = co + 3 * i, in = 1;
    for (int f = 0; f < 8; f++) {
      int sx = (f & 1) ? -1 : 1, sy = (f & 2) ? -1 : 1, sz = (f & 4) ? -1 : 1, s = sx * p[0] + sy * p[1] + sz * p[2];
      if (s == R) fcell[f][nf[f]++] = i;
      if ((R - s) / 2 < (f ? DO : DW)) in = 0;
    }
    if (in) Ncell[nN++] = i;
  }
  CB = 2; while ((1 << CB) < 4 * nN) CB++;
  B = 1 << CB;
  a = aligned_alloc(64, (size_t)(n + 1) * W * 8); b = aligned_alloc(64, (size_t)(n + 1) * W * 8);
  memset(a, 0, (size_t)(n + 1) * W * 8); memset(b, 0, (size_t)(n + 1) * W * 8);
  free(idx);
  return n;
}

#define FA(s, c, p, q, r) do { vec t_ = (p) ^ (q); s = t_ ^ (r); c = ((p) & (q)) | (t_ & (r)); } while (0)
static inline vec rule(const vec *x, vec me) {
  vec s0, c0, s1, c1, s2, c2, s3, c3, u, cu, b0, cv, p, cp, q, cq, b1, cw, b2, b3;
  FA(s0, c0, x[0], x[1], x[2]); FA(s1, c1, x[3], x[4], x[5]); FA(s2, c2, x[6], x[7], x[8]); FA(s3, c3, x[9], x[10], x[11]);
  FA(u, cu, s0, s1, s2); b0 = u ^ s3; cv = u & s3;
  FA(p, cp, c0, c1, c2); FA(q, cq, c3, cu, cv); b1 = p ^ q; cw = p & q;
  FA(b2, b3, cp, cq, cw);
  return ~b3 & ((b2 & ~b1) | (me & ~b2 & b1 & b0));     /* count 4, 5: alive; count 3: keeps its state */
}
static void step(void) {       /* one generation of gump on the hull */
  for (int i = 0; i < n; i++) {
    const int *q = nb + 12 * (size_t)i; vec x[12], me, o;
    for (int t = 0; t < 12; t++) memcpy(&x[t], a + (size_t)q[t] * W, 64);
    memcpy(&me, a + (size_t)i * W, 64); o = rule(x, me); memcpy(b + (size_t)i * W, &o, 64);
  }
  u64 *t = a; a = b; b = t;
}
static inline void dart(int lane, dart_t v) {      /* one dart on lane `lane` */
  int sq = v & (B - 1);
  if (sq < nN) { u64 *x = a + (size_t)Ncell[sq] * W + (lane >> 6), bit = 1ULL << (lane & 63); *x = (v >> 15) ? (*x | bit) : (*x & ~bit); }
}
static void noise_slow(int M) {                    /* M fresh darts on every lane, thrown one by one */
  for (int l = 0; l < NL; l++) for (int d = 0; d < M; d += 4) { u64 r = rnd(); for (int k = 0; k < 4 && d + k < M; k++) dart(l, (dart_t)(r >> (16 * k))); }
}
/* The same law, faster: of M darts at a board of B squares, the number that land on N is Binomial(M, |N|/B), and
   those land on uniformly random cells of N, in random order, each with its own coin. */
static int slow_noise = 0;
static void noise_random(int M) {
  static uint32_t cdf[4096]; static int cdfM = -1;
  if (slow_noise || M > 4000) { noise_slow(M); return; }
  if (cdfM != M) { double q = (double)nN / B, pk = pow(1 - q, M), c = 0;
    for (int k = 0; k <= M; k++) { c += pk; cdf[k] = c >= 1 ? 0xFFFFFFFFu : (uint32_t)(c * 4294967296.0); pk = pk * (M - k) / (k + 1) * q / (1 - q); }
    cdf[M] = 0xFFFFFFFFu; cdfM = M; }
  for (int l = 0; l < NL; l++) {
    u64 r = rnd(); uint32_t u = (uint32_t)r; int k = 0; while (cdf[k] <= u && k < M) k++;
    u64 *base = a + (l >> 6), bit = 1ULL << (l & 63); r >>= 32; int have = 1;
    for (int h = 0; h < k; h++) {
      if (!have) { r = rnd(); have = 2; }
      uint32_t v = (uint32_t)r; r >>= 32; have--;
      u64 *x = base + (size_t)Ncell[((u64)(v >> 1) * (u64)nN) >> 31] * W;
      *x = (v & 1) ? (*x | bit) : (*x & ~bit);
    }
  }
}
/* pop[l]: population of the watched face; od[w]: lanes in which another face is empty; nd: number of empty faces */
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
/* Settled lives: a hull whose watched face's population has repeated with period 2 or with period dividing 12 for
   SETTLE generations in a row has stopped being chaos (a still life or oscillator with all faces alive; seen at R = 9,
   about once in 10^9 hull-generations). It is counted and replaced; its last generations stay in the exposure. */
#define SETTLE 4096
static short ring[NL][12]; static int run2[NL], run12[NL], rpos;
static inline int settled(int l) {      /* call once per generation and lane, after observe() */
  short p = (short)pop[l]; int i2 = (rpos + 10) % 12;
  run2[l] = (ring[l][i2] == p) ? run2[l] + 1 : 0; run12[l] = (ring[l][rpos] == p) ? run12[l] + 1 : 0;
  ring[l][rpos] = p;
  if (run2[l] >= SETTLE || run12[l] >= SETTLE) { run2[l] = run12[l] = 0; return 1; }
  return 0;
}
static void lane_soup(int lane) { int w = lane >> 6, k = lane & 63; u64 bit = 1ULL << k; u64 thr = (u64)(SOUP * 18446744073709551616.0);
  for (int i = 0; i < n; i++) { u64 *x = a + (size_t)i * W + w; if (rnd() < thr) *x |= bit; else *x &= ~bit; } }

#ifdef LIB
int v_A(void) { return A; }
int v_nN(void) { return nN; }
int v_B(void) { return B; }
void v_coords(int *out) { memcpy(out, co, sizeof(int) * 3 * n); }
void v_ncells(int *out) { memcpy(out, Ncell, sizeof(int) * nN); }
void v_clear(void) { memset(a, 0, (size_t)(n + 1) * W * 8); memset(b, 0, (size_t)(n + 1) * W * 8); }
void v_set(int lane, const uint8_t *cells) { for (int i = 0; i < n; i++) { u64 *p = a + (size_t)i * W + (lane >> 6); *p = (*p & ~(1ULL << (lane & 63))) | ((u64)(cells[i] & 1) << (lane & 63)); } }
void v_get(int lane, uint8_t *cells) { for (int i = 0; i < n; i++) cells[i] = (a[(size_t)i * W + (lane >> 6)] >> (lane & 63)) & 1; }
void v_step(void) { step(); observe(); }
void v_dart(int lane, int v) { dart(lane, (dart_t)v); }
int v_pop(int lane) { return pop[lane]; }
int v_od(int lane) { return (od[lane >> 6] >> (lane & 63)) & 1; }
int v_ndead(int lane) { return ndead(lane); }
void v_swap(int i, int j, int newnb) { nb[12 * i + j] = newnb; }
int v_nb(int i, int j) { return nb[12 * i + j]; }
#else
int main(int argc, char **argv) {
  if (argc < 6) { fprintf(stderr, "usage: nz R brute SEED GENS M [DW DO] | nz R sub SEED NREP LAM1 DELTA NBATCH NSWEEP KFLIP TPRE TWIN WBACK M [DW DO [PATHFILE]]\n"); return 2; }
  const char *mode = argv[2]; u64 seed0 = strtoull(argv[3], 0, 10);
  if (getenv("NZSLOW")) slow_noise = atoi(getenv("NZSLOW"));   /* 1: throw the M darts one by one (cross-check of the fast form) */
  if (!strcmp(mode, "brute")) {
    long gens = atol(argv[4]); int M = atoi(argv[5]);
    geom_init(atoi(argv[1]), argc > 6 ? atoi(argv[6]) : 6, argc > 7 ? atoi(argv[7]) : 3);
    sm = seed0 * 0x2545F4914F6CDD1DULL + 7;
    static long age[NL]; double E = 0, dw = 0, sp = 0, spp = 0; long Dany = 0, n0 = 0, n0alone = 0, nsettled = 0, maxage = 0;
    for (int l = 0; l < NL; l++) { lane_soup(l); age[l] = 0; }
    for (long g = 0; g < gens + T0; g++) {
      step(); if (M) noise_random(M); observe();
      for (int l = 0; l < NL; l++) {
        age[l]++;
        int counted = (g >= T0 && age[l] > T0), dead0 = (pop[l] == 0), odl = (int)((od[l >> 6] >> (l & 63)) & 1);
        if (counted) { E += 1; if (!dead0 && !odl) { sp += pop[l]; spp += (double)pop[l] * pop[l]; } }
        if (dead0 || odl) {
          if (counted) { Dany++; if (dead0) { n0++; dw += 1.0 / ndead(l); if (!odl) n0alone++; } }
          if (age[l] > maxage) maxage = age[l];
          lane_soup(l); age[l] = 0;
        } else if (settled(l)) { nsettled++; lane_soup(l); age[l] = 0; }
      }
      rpos = (rpos + 1) % 12;
    }
    double ns = E - Dany, pb = sp / ns;
    printf("BRUTE R %d A %d n %d DW %d DO %d nN %d B %d M %d eps %.6f seed %llu exposure %.6e deaths_any %ld watched %ld watched_alone %ld watched_weighted %.3f Pbar %.4f sigP %.4f",
           R, A, n, DW, DO, nN, B, M, (double)M / B, (unsigned long long)seed0, E, Dany, n0, n0alone, dw, pb, sqrt(spp / ns - pb * pb));
    if (Dany) printf(" lntau_any8 %.4f +- %.4f", log(8 * E / Dany), 1 / sqrt((double)Dany));
    if (n0) printf(" lntau_watched %.4f +- %.4f", log(E / n0), 1 / sqrt((double)n0));
    printf(" settled %ld longest_life %ld\n", nsettled, maxage);
    return 0;
  }
  if (strcmp(mode, "sub") || argc < 14) return 2;
  int nrep = atoi(argv[4]), LAM1 = atoi(argv[5]), DELTA = atoi(argv[6]), NBATCH = atoi(argv[7]), NSWEEP = atoi(argv[8]), KFLIP = atoi(argv[9]);
  int TPRE = atoi(argv[10]), TWIN = atoi(argv[11]), WBACK = atoi(argv[12]), M = atoi(argv[13]), T = TPRE + TWIN;
  geom_init(atoi(argv[1]), argc > 14 ? atoi(argv[14]) : 6, argc > 15 ? atoi(argv[15]) : 3);
  FILE *pp = (argc > 16 && strcmp(argv[16], "-")) ? fopen(argv[16], "w") : 0;
  if (M < 1 || T > 127 || nN < 1) { fprintf(stderr, "sub needs M >= 1, T <= 127, a noise region\n"); return 1; }
  sm = seed0 * 0x2545F4914F6CDD1DULL + 4242;
  size_t ssz = (size_t)(n + 1) * W, csz = (size_t)T * M; long NC = (long)NBATCH * NL;
  u64 *init = malloc(NBATCH * ssz * 8), *init2 = malloc(NBATCH * ssz * 8), *pl = malloc(ssz * 8);
  dart_t *DA = malloc(NC * csz * sizeof(dart_t)), *DA2 = malloc(NC * csz * sizeof(dart_t)), *Dp = malloc(NL * csz * sizeof(dart_t));
  int *score = malloc(4 * NC), *score2 = malloc(4 * NC), *seeds = malloc(4 * NC), *gmin = malloc(4 * NC), *gmin2 = malloc(4 * NC);
  static int am[NL], sc[NL]; static short popser[NL][128]; static long page[NL];
  double *rate = malloc(8 * nrep); double sumlnP[128] = {0}, accs = 0, accn = 0; long nlevP[128] = {0}; int lamlist[128], nlam = 0;
  int cbits = CB + 1;                    /* bits of a dart that a proposal may flip: CB of the square, one coin */
  /* EVAL: trajectories of the 512 chains of one batch from their initial states under their darts.
     Score = minimum population of the watched face over generations TPRE+1 .. T, as long as the life lasts: the life
     ends at the first generation go at which another face is empty (that generation still counts, so a tie is a death
     of the watched face). A chain with any face empty at generation TPRE has no score (1 << 20). */
  #define EVAL(initb, darts) do { static int go_[NL], bad_[NL]; memcpy(a, (initb), ssz * 8); \
      for (int l_ = 0; l_ < NL; l_++) { go_[l_] = T + 1; bad_[l_] = 0; } \
      for (int t_ = 0; t_ < T; t_++) { step(); \
        for (int l_ = 0; l_ < NL; l_++) { const dart_t *dd_ = (darts) + ((size_t)l_ * T + t_) * M; for (int d_ = 0; d_ < M; d_++) dart(l_, dd_[d_]); } \
        observe(); \
        for (int l_ = 0; l_ < NL; l_++) { popser[l_][t_ + 1] = (short)pop[l_]; \
          if (go_[l_] > T && ((od[l_ >> 6] >> (l_ & 63)) & 1)) go_[l_] = t_ + 1; \
          if (t_ + 1 == TPRE && (pop[l_] == 0 || go_[l_] <= T)) bad_[l_] = 1; } } \
      for (int l_ = 0; l_ < NL; l_++) { int m_ = 1 << 20, a_ = T; \
        if (!bad_[l_]) for (int g_ = TPRE + 1; g_ <= T && g_ <= go_[l_]; g_++) if (popser[l_][g_] < m_) { m_ = popser[l_][g_]; a_ = g_; } \
        sc[l_] = m_; am[l_] = a_; } } while (0)
  printf("# sub R %d A %d n %d DW %d DO %d nN %d B %d M %d eps %.6f LAM1 %d DELTA %d chains %ld NSWEEP %d KFLIP %d TPRE %d TWIN %d WBACK %d seed %llu\n",
         R, A, n, DW, DO, nN, B, M, (double)M / B, LAM1, DELTA, NC, NSWEEP, KFLIP, TPRE, TWIN, WBACK, (unsigned long long)seed0);
  for (int l = 0; l < NL; l++) { lane_soup(l); page[l] = 0; }
  #define ADVANCE(G) do { for (int g_ = 0; g_ < (G); g_++) { step(); noise_random(M); observe(); \
      for (int l_ = 0; l_ < NL; l_++) { page[l_]++; if (pop[l_] == 0 || ((od[l_ >> 6] >> (l_ & 63)) & 1) || settled(l_)) { lane_soup(l_); page[l_] = 0; } } \
      rpos = (rpos + 1) % 12; } } while (0)
  ADVANCE(BURN);
  for (int rep = 0; rep < nrep; rep++) {
    long nvalid = 0;
    for (int bt = 0; bt < NBATCH; bt++) {
      ADVANCE(64);
      int valid[NL]; for (int l = 0; l < NL; l++) valid[l] = (page[l] >= BURN);
      memcpy(pl, a, ssz * 8); memcpy(init + bt * ssz, a, ssz * 8);
      dart_t *d = DA + (size_t)bt * NL * csz;
      for (size_t x = 0; x < NL * csz; x += 3) { u64 r = rnd(); for (int k = 0; k < 3 && x + k < NL * csz; k++) { u64 v = r >> (21 * k); d[x + k] = (dart_t)((v & (B - 1)) | (((v >> 20) & 1) << 15)); } }
      EVAL(init + bt * ssz, d);
      for (int l = 0; l < NL; l++) { int ok = valid[l] && sc[l] < (1 << 20); score[bt * NL + l] = ok ? sc[l] : (1 << 20); gmin[bt * NL + l] = am[l]; nvalid += ok; }
      memcpy(a, pl, ssz * 8);
    }
    memcpy(pl, a, ssz * 8);
    int lam = LAM1, lev = 0; double prod = 1; long denom = nvalid; printf("REP %d valid %ld :", rep, nvalid);
    for (;;) {
      long ns = 0; for (long j = 0; j < NC; j++) if (score[j] <= lam) seeds[ns++] = (int)j;
      double P = (double)ns / denom; prod *= P; printf(" %d:%ld", lam, ns); lamlist[lev] = lam; if (ns) { sumlnP[lev] += log(P); nlevP[lev]++; } lev++; if (lev > nlam) nlam = lev;
      if (ns == 0 || lam == 0) break;
      u64 r0 = rnd() % (u64)ns;
      memset(init2, 0, NBATCH * ssz * 8);
      for (long j = 0; j < NC; j++) { int src = seeds[(r0 + (u64)j) % (u64)ns]; int sb = src / NL, sl = src % NL, db = (int)(j / NL), dl = (int)(j % NL);
        const u64 *si = init + sb * ssz + (sl >> 6); u64 *di = init2 + db * ssz + (dl >> 6); int sk = sl & 63, dk = dl & 63;
        for (int i = 0; i < n; i++) di[(size_t)i * W] |= ((si[(size_t)i * W] >> sk) & 1) << dk;
        memcpy(DA2 + (size_t)j * csz, DA + (size_t)src * csz, csz * sizeof(dart_t));
        score2[j] = score[src]; gmin2[j] = gmin[src]; }
      { u64 *t1 = init; init = init2; init2 = t1; dart_t *t3 = DA; DA = DA2; DA2 = t3; int *t2 = score; score = score2; score2 = t2; t2 = gmin; gmin = gmin2; gmin2 = t2; }
      for (int sw = 0; sw < NSWEEP; sw++) for (int bt = 0; bt < NBATCH; bt++) { dart_t *d = DA + (size_t)bt * NL * csz; memcpy(Dp, d, NL * csz * sizeof(dart_t));
        int foc = (WBACK > 0 && (sw & 1)); static int tlo[NL], thi[NL];
        for (int l = 0; l < NL; l++) { tlo[l] = T; thi[l] = -1; for (int k = 0; k < KFLIP; k++) { u64 z = rnd(); int t;
            if (foc) { int g0 = gmin[bt * NL + l]; t = g0 - WBACK + (int)((z >> 40) % (u64)WBACK); if (t < 0) t = 0; if (t < tlo[l]) tlo[l] = t; if (t > thi[l]) thi[l] = t; }
            else t = (int)((z >> 40) % (u64)T);
            int dd = (int)((z >> 8) % (u64)M), bitn = (int)((z >> 24) % (u64)cbits);
            Dp[((size_t)l * T + t) * M + dd] ^= (dart_t)(bitn == CB ? 0x8000 : (1 << bitn)); } }
        EVAL(init + bt * ssz, Dp);
        for (int l = 0; l < NL; l++) { accn++; int ok = sc[l] <= lam; if (ok && foc) ok = (tlo[l] >= am[l] - WBACK && thi[l] < am[l]);   /* the reverse move must be proposable */
          if (ok) { memcpy(d + (size_t)l * csz, Dp + (size_t)l * csz, csz * sizeof(dart_t)); score[bt * NL + l] = sc[l]; gmin[bt * NL + l] = am[l]; accs++; } } }
      denom = NC; lam = lam - DELTA > 0 ? lam - DELTA : 0;
    }
    rate[rep] = prod / TWIN; printf(" rate %.5e lntau %.4f\n", rate[rep], rate[rep] > 0 ? -log(rate[rep]) : 99.0); fflush(stdout);
    if (pp && rate[rep] > 0) for (int bt = 0; bt < NBATCH; bt++) { EVAL(init + bt * ssz, DA + (size_t)bt * NL * csz);   /* dying chains: population of the watched face by generation, backwards */
        for (int l = 0; l < NL; l++) if (sc[l] == 0) { int gd = am[l]; fprintf(pp, "S %d %d %d |", rep, bt * NL + l, gd);
          for (int g = gd - 1; g >= 1 && g >= gd - 24; g--) { fprintf(pp, " %d", popser[l][g]); } fprintf(pp, "\n"); } }
    memcpy(a, pl, ssz * 8);
  }
  double m = 0, v = 0; for (int i = 0; i < nrep; i++) m += rate[i]; m /= nrep; for (int i = 0; i < nrep; i++) v += (rate[i] - m) * (rate[i] - m);
  printf("SUMMARY sub R %d A %d M %d eps %.6f reps %d lntau %.4f +- %.4f (rel sd of one replication %.3f) acceptance %.3f\n", R, A, M, (double)M / B, nrep, -log(m),
         nrep > 1 ? sqrt(v / (nrep - 1) / nrep) / m : 0, nrep > 1 ? sqrt(v / (nrep - 1)) / m : 0, accs / (accn > 0 ? accn : 1));
  for (int i = 0; i < nlam; i++) if (nlevP[i]) printf("LEVEL %d lam %d mean lnP %.4f (%ld reps)\n", i, lamlist[i], sumlnP[i] / nlevP[i], nlevP[i]);
  if (pp) fclose(pp);
  return 0;
}
#endif
