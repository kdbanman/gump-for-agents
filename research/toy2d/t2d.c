/* t2d.c -- bit-sliced replicas of an outer-totalistic rule on an arbitrary finite cell graph.
 *
 * Built for research/toy2d (2D analogues of gump).  Replica r lives in bit (r % 64) of word (r / 64);
 * W words per cell, 64*W replicas.  The graph, the seeding orbits (for symmetric soups), the watched
 * "lines" (e.g. the edge rows of a vessel) and the "events" (sets of lines that must all be empty, e.g. one
 * edge row = a peel, two adjacent interior rows = a firewall) come from a binary file written by geom.py.
 *
 *   t2d life  GRAPH B S p seed Tmax          one soup per replica, run to settle or Tmax; prints per replica:
 *                                            settle_gen (-1 = still running) and first time of every event
 *   t2d qsd   GRAPH B S p seed T0 gens OUT   quasi-stationary sampling with restarts: a replica whose event
 *                                            fires or which settles is recorded and reseeded; states younger
 *                                            than T0 are not measured.  Writes OUT (text, key value...).
 *   t2d trace GRAPH B S p seed gens          replica 0 only: per generation, population and line counts
 *
 * B, S are bit masks over the neighbour count (bit k = count k).  Settled = period 1 or 2 (state(t) ==
 * state(t-2)), checked every generation, or period dividing 840 (checked every 840 generations).
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#ifndef W
#define W 4
#endif
#define NR (64 * W)
typedef uint64_t u64;

static int N, K, R, M, E;
static int32_t *nb, *orb;
static int *lflag, *llen, **lcell, *elen, **eline;
static u64 *x0, *x1, *x2, *snap; /* x0 = current, x1 = t-1, x2 = t-2 */
static int nterm; static int tk[16], tmode[16]; /* tmode: 1 = birth only, 2 = survive only, 3 = both */

static u64 rs[4];
static inline u64 rotl(const u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static u64 rnd(void) { const u64 r = rotl(rs[1] * 5, 7) * 9, t = rs[1] << 17;
  rs[2] ^= rs[0]; rs[3] ^= rs[1]; rs[1] ^= rs[2]; rs[0] ^= rs[3]; rs[2] ^= t; rs[3] = rotl(rs[3], 45); return r; }
static void seedrng(u64 s) { rs[0] = 0x9E3779B97F4A7C15ULL ^ s; rs[1] = 0xD1B54A32D192ED03ULL + s * 7;
  rs[2] = 0x8CB92BA72F3D8DD7ULL; rs[3] = s * 0x2545F4914F6CDD1DULL + 1; for (int i = 0; i < 20; i++) rnd(); }
static int pbits[16]; static int npb;
static void setp(double p) { /* 16-bit binary expansion of p */
  int v = (int)floor(p * 65536.0 + 0.5); if (v > 65535) v = 65535; npb = 16;
  for (int i = 0; i < 16; i++) pbits[i] = (v >> i) & 1; }
static u64 rword(void) { u64 w = 0; for (int i = 0; i < npb; i++) { u64 r = rnd(); w = pbits[i] ? (w | r) : (w & r); } return w; }

static void rdi(FILE *f, int32_t *a, size_t n) { if (fread(a, 4, n, f) != n) { fprintf(stderr, "short graph\n"); exit(2); } }
static void load(const char *fn) {
  FILE *f = fopen(fn, "rb"); if (!f) { perror(fn); exit(2); }
  int32_t h[2]; rdi(f, h, 2); N = h[0]; K = h[1];
  nb = malloc(4 * (size_t)N * K); rdi(f, nb, (size_t)N * K);
  for (size_t i = 0; i < (size_t)N * K; i++) if (nb[i] < 0) nb[i] = N;
  orb = malloc(4 * (size_t)N); rdi(f, orb, N);
  rdi(f, h, 1); R = h[0];
  rdi(f, h, 1); M = h[0];
  lflag = malloc(4 * (M + 1)); llen = malloc(4 * (M + 1)); lcell = malloc(sizeof(int *) * (M + 1));
  for (int l = 0; l < M; l++) { rdi(f, h, 2); lflag[l] = h[0]; llen[l] = h[1]; lcell[l] = malloc(4 * (llen[l] + 1)); rdi(f, lcell[l], llen[l]); }
  rdi(f, h, 1); E = h[0];
  elen = malloc(4 * (E + 1)); eline = malloc(sizeof(int *) * (E + 1));
  for (int e = 0; e < E; e++) { rdi(f, h, 1); elen[e] = h[0]; eline[e] = malloc(4 * (elen[e] + 1)); rdi(f, eline[e], elen[e]); }
  fclose(f);
  x0 = calloc((size_t)(N + 1) * W, 8); x1 = calloc((size_t)(N + 1) * W, 8);
  x2 = calloc((size_t)(N + 1) * W, 8); snap = calloc((size_t)(N + 1) * W, 8);
}
static void setrule(int B, int S) {
  nterm = 0;
  for (int k = 0; k <= 15; k++) { int b = B >> k & 1, s = S >> k & 1; if (b || s) { tk[nterm] = k; tmode[nterm++] = b + 2 * s; } }
}

/* one generation: x2 <- x1 <- x0 <- f(x0) (pointer rotation) */
static void step(void) {
  u64 *nx = x2;
  for (int i = 0; i < N; i++) {
    const int32_t *ni = nb + (size_t)i * K;
    u64 s0[W] = {0}, s1[W] = {0}, s2[W] = {0}, s3[W] = {0};
    for (int k = 0; k < K; k++) {
      const u64 *a = x0 + (size_t)ni[k] * W;
      for (int w = 0; w < W; w++) { u64 c = s0[w] & a[w]; s0[w] ^= a[w]; u64 c2 = s1[w] & c; s1[w] ^= c; u64 c3 = s2[w] & c2; s2[w] ^= c2; s3[w] ^= c3; }
    }
    const u64 *xi = x0 + (size_t)i * W; u64 *o = nx + (size_t)i * W;
    for (int w = 0; w < W; w++) {
      u64 r = 0;
      for (int t = 0; t < nterm; t++) {
        int k = tk[t];
        u64 e = ((k & 1) ? s0[w] : ~s0[w]) & ((k & 2) ? s1[w] : ~s1[w]) & ((k & 4) ? s2[w] : ~s2[w]) & ((k & 8) ? s3[w] : ~s3[w]);
        if (tmode[t] == 1) e &= ~xi[w]; else if (tmode[t] == 2) e &= xi[w];
        r |= e;
      }
      o[w] = r;
    }
  }
  x2 = x1; x1 = x0; x0 = nx;
}

static void reseed(int r, int fresh_all) {
  int w = r / 64; u64 bit = 1ULL << (r % 64);
  static u64 *rb = NULL; static int rbn = 0;
  if (rbn < R) { free(rb); rb = malloc(8 * (size_t)(R + 1)); rbn = R; }
  (void)fresh_all;
  for (int j = 0; j < R; j++) rb[j] = rword() & 1; /* one Bernoulli(p) bit per orbit */
  for (int i = 0; i < N; i++) {
    u64 *c = x0 + (size_t)i * W + w;
    if (orb[i] >= 0 && rb[orb[i]]) *c |= bit; else *c &= ~bit;
    x1[(size_t)i * W + w] |= bit; x2[(size_t)i * W + w] &= ~bit; /* history that cannot look settled */
  }
}
static void seed_all(void) {
  /* fast path: whole words */
  u64 *rb = malloc(8 * (size_t)(R + 1) * W);
  for (int j = 0; j < R * W; j++) rb[j] = rword();
  for (int i = 0; i < N; i++) for (int w = 0; w < W; w++) {
    x0[(size_t)i * W + w] = orb[i] >= 0 ? rb[(size_t)orb[i] * W + w] : 0;
    x1[(size_t)i * W + w] = ~0ULL; x2[(size_t)i * W + w] = 0; }
  free(rb);
}

/* per-line OR (alive mask) */
static void line_alive(u64 *alive /* M*W */) {
  for (int l = 0; l < M; l++) for (int w = 0; w < W; w++) {
    u64 a = 0; for (int j = 0; j < llen[l]; j++) a |= x0[(size_t)lcell[l][j] * W + w]; alive[(size_t)l * W + w] = a; }
}
/* settled masks: period <= 2 */
static void settled2(u64 *s) {
  for (int w = 0; w < W; w++) s[w] = 0;
  for (int i = 0; i < N; i++) for (int w = 0; w < W; w++) s[w] |= x0[(size_t)i * W + w] ^ x2[(size_t)i * W + w];
  for (int w = 0; w < W; w++) s[w] = ~s[w];
}
static void settled840(u64 *s) {
  for (int w = 0; w < W; w++) s[w] = 0;
  for (int i = 0; i < N; i++) for (int w = 0; w < W; w++) s[w] |= x0[(size_t)i * W + w] ^ snap[(size_t)i * W + w];
  for (int w = 0; w < W; w++) s[w] = ~s[w];
}
/* bit-sliced population count of a line, per replica */
static void line_count(int l, int *cnt /* NR */) {
  u64 c[W][12]; memset(c, 0, sizeof c);
  for (int j = 0; j < llen[l]; j++) for (int w = 0; w < W; w++) {
    u64 a = x0[(size_t)lcell[l][j] * W + w];
    for (int b = 0; a && b < 12; b++) { u64 t = c[w][b] & a; c[w][b] ^= a; a = t; }
  }
  for (int w = 0; w < W; w++) for (int r = 0; r < 64; r++) { int v = 0; for (int b = 0; b < 12; b++) v |= (int)((c[w][b] >> r) & 1) << b; cnt[w * 64 + r] = v; }
}
static int popall(int r) { int w = r / 64, b = r % 64, n = 0; for (int i = 0; i < N; i++) n += (x0[(size_t)i * W + w] >> b) & 1; return n; }

int main(int argc, char **argv) {
  if (argc < 7) { fprintf(stderr, "usage: see header\n"); return 2; }
  const char *mode = argv[1];
  load(argv[2]); setrule(atoi(argv[3]), atoi(argv[4])); setp(atof(argv[5])); seedrng(strtoull(argv[6], 0, 10));
  u64 *alive = malloc(8 * (size_t)(M + 1) * W), sm[W], ev[W];
  if (!strcmp(mode, "life")) {
    long Tmax = atol(argv[7]);
    seed_all(); memcpy(snap, x0, 8 * (size_t)(N + 1) * W);
    long *settle = malloc(8 * NR), *evt = malloc(8 * (size_t)NR * (E + 1));
    for (int r = 0; r < NR; r++) settle[r] = -1;
    for (size_t i = 0; i < (size_t)NR * E; i++) evt[i] = -1;
    int left = NR;
    /* events at t = 0 */
    for (long t = 1; t <= Tmax && left > 0; t++) {
      step();
      line_alive(alive);
      for (int e = 0; e < E; e++) {
        for (int w = 0; w < W; w++) { u64 d = ~0ULL; for (int j = 0; j < elen[e]; j++) d &= ~alive[(size_t)eline[e][j] * W + w]; ev[w] = d; }
        for (int r = 0; r < NR; r++) if (evt[(size_t)r * E + e] < 0 && settle[r] < 0 && (ev[r / 64] >> (r % 64) & 1)) evt[(size_t)r * E + e] = t;
      }
      settled2(sm);
      for (int r = 0; r < NR; r++) if (settle[r] < 0 && (sm[r / 64] >> (r % 64) & 1)) { settle[r] = t - 2 < 0 ? 0 : t - 2; left--; }
      if (t % 840 == 0) {
        settled840(sm);
        for (int r = 0; r < NR; r++) if (settle[r] < 0 && (sm[r / 64] >> (r % 64) & 1)) { settle[r] = t - 840; left--; }
        memcpy(snap, x0, 8 * (size_t)(N + 1) * W);
      }
    }
    for (int r = 0; r < NR; r++) {
      printf("%ld %d", settle[r], popall(r));
      for (int e = 0; e < E; e++) printf(" %ld", evt[(size_t)r * E + e]);
      printf("\n");
    }
    return 0;
  }
  if (!strcmp(mode, "trace")) {
    long gens = atol(argv[7]);
    seed_all();
    int *cnt = malloc(4 * NR);
    printf("init"); for (int i = 0; i < N; i++) if (x0[(size_t)i * W] & 1) printf(" %d", i); printf("\n");
    for (long t = 0; t <= gens; t++) {
      if (t) step();
      printf("%ld %d", t, popall(0));
      for (int l = 0; l < M; l++) { line_count(l, cnt); printf(" %d", cnt[0]); }
      printf("\n");
    }
    printf("final"); for (int i = 0; i < N; i++) if (x0[(size_t)i * W] & 1) printf(" %d", i); printf("\n");
    return 0;
  }
  if (!strcmp(mode, "qsd")) {
    long T0 = atol(argv[7]); double gens = atof(argv[8]); const char *out = argv[9];
    seed_all(); memcpy(snap, x0, 8 * (size_t)(N + 1) * W);
    long *age = calloc(NR, 8);
    int nh = 0; for (int l = 0; l < M; l++) if (lflag[l] & 1) nh++;
    int maxlen = 0; for (int l = 0; l < M; l++) if (llen[l] > maxlen) maxlen = llen[l];
    double *hist = calloc((size_t)(maxlen + 1), sizeof(double)); /* pooled over histogram lines */
    int *cnt = malloc(4 * NR), *prevc = calloc((size_t)NR * (M + 1), 4);
    double exposure = 0; long ndeath_e[64] = {0}, early = 0, settles = 0, settles_exp = 0;
    double from[8] = {0}; /* histogram-line count at t-1 for deaths of single-line events: 0..7 (7 = >=7) */
    double aexp[64] = {0}, adeath[64] = {0};
    long ndeaths = 0;
    FILE *dl = NULL; char dfn[4096]; snprintf(dfn, sizeof dfn, "%s.deaths", out); dl = fopen(dfn, "w");
    for (double g = 0; g < gens; g += 1) {
      /* exposure: replicas with age >= T0 before the step */
      u64 expm[W] = {0};
      for (int r = 0; r < NR; r++) if (age[r] >= T0) { expm[r / 64] |= 1ULL << (r % 64); exposure += 1;
        int b = 0; long a = age[r] - T0 + 1; while (a > 1) { a >>= 1; b++; } aexp[b] += 1; }
      step();
      for (int r = 0; r < NR; r++) age[r]++;
      long t = (long)g + 1;
      line_alive(alive);
      int killed[NR]; memset(killed, 0, sizeof killed);
      for (int e = 0; e < E; e++) {
        for (int w = 0; w < W; w++) { u64 d = ~0ULL; for (int j = 0; j < elen[e]; j++) d &= ~alive[(size_t)eline[e][j] * W + w]; ev[w] = d; }
        for (int r = 0; r < NR; r++) if (!killed[r] && (ev[r / 64] >> (r % 64) & 1)) {
          killed[r] = 1;
          if (expm[r / 64] >> (r % 64) & 1) {
            ndeath_e[e < 63 ? e : 63]++; ndeaths++;
            int b = 0; long a = age[r] - 1 - T0 + 1; while (a > 1) { a >>= 1; b++; } adeath[b] += 1;
            if (elen[e] == 1) { int pc = prevc[(size_t)r * M + eline[e][0]]; from[pc < 7 ? pc : 7] += 1; }
            if (dl) fprintf(dl, "%d %ld\n", e, age[r]);
          } else early++;
        }
      }
      settled2(sm);
      if (t % 840 == 0) { u64 s8[W]; settled840(s8); for (int w = 0; w < W; w++) sm[w] |= s8[w]; memcpy(snap, x0, 8 * (size_t)(N + 1) * W); }
      for (int r = 0; r < NR; r++) if (!killed[r] && (sm[r / 64] >> (r % 64) & 1)) { killed[r] = 2; settles++; if (expm[r / 64] >> (r % 64) & 1) settles_exp++; }
      /* histogram of living, measured replicas (state after the step, if they are exposed next step) */
      int anym = 0; for (int r = 0; r < NR; r++) if (!killed[r] && age[r] >= T0) { anym = 1; break; }
      if (anym || 1) {
        for (int l = 0; l < M; l++) {
          if (!(lflag[l] & 1)) continue;
          line_count(l, cnt);
          for (int r = 0; r < NR; r++) { prevc[(size_t)r * M + l] = cnt[r]; if (!killed[r] && age[r] >= T0) hist[cnt[r]] += 1; }
        }
      }
      for (int r = 0; r < NR; r++) if (killed[r]) { reseed(r, 0); age[r] = 0; }
    }
    FILE *f = fopen(out, "w");
    fprintf(f, "replicas %d\nT0 %ld\ngens %.0f\nexposure %.0f\ndeaths %ld\nearly %ld\nsettles %ld\nsettles_exposed %ld\nhistlines %d\n",
            NR, T0, gens, exposure, ndeaths, early, settles, settles_exp, nh);
    fprintf(f, "deaths_by_event"); for (int e = 0; e < E && e < 64; e++) fprintf(f, " %ld", ndeath_e[e]); fprintf(f, "\n");
    fprintf(f, "from"); for (int k = 0; k < 8; k++) fprintf(f, " %.0f", from[k]); fprintf(f, "\n");
    fprintf(f, "age_exposure"); for (int b = 0; b < 64; b++) fprintf(f, " %.0f", aexp[b]); fprintf(f, "\n");
    fprintf(f, "age_deaths"); for (int b = 0; b < 64; b++) fprintf(f, " %.0f", adeath[b]); fprintf(f, "\n");
    fprintf(f, "hist"); for (int k = 0; k <= maxlen; k++) fprintf(f, " %.0f", hist[k]); fprintf(f, "\n");
    fclose(f); if (dl) fclose(dl);
    return 0;
  }
  fprintf(stderr, "unknown mode\n"); return 2;
}
