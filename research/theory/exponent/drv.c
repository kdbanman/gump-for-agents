/* drv.c -- bit-sliced replicas of an outer-totalistic rule on a finite DIRECTED cell graph whose cells are
 * dynamic (follow the rule), noise (i.i.d. Bernoulli, redrawn every generation: a "random field" replacing
 * deeper layers) or dead.  Optional death noise eps (every live dynamic cell killed independently with
 * probability eps after each step).  Kernel after research/toy2d/t2d.c; written for research/theory/exponent.
 *
 *   drv qsd   GRAPH B S p seed T0 gens OUT [rho0,rho1,...] [eps]   quasi-stationary sampling with restarts
 *   drv trace GRAPH B S p seed gens                                 replica 0: initial cells, line counts per gen
 *
 * Graph file (int32 LE): N M K | nb[N*K] (0..N-1 dynamic, N..N+M-1 noise, -1 dead) | cls[M] (noise class) |
 *   NL, then per line: flag len cells   (flag 1 = pooled histogram + transitions, 2 = cyclic: gap statistics,
 *                                        4 = count kept for pre-death profiles)
 *   NE, then per event: len lines       (event fires when all its lines are empty; the replica is restarted)
 *   NP, then per profile group: event nl lines   (mean count of these lines at lags 1..64 before that event)
 * A directed graph lets a "slave" copy of some rows read a "donor" simulation without acting back on it.
 *
 * Settling (deterministic runs only, i.e. M = 0 and eps = 0): period <= 2 every generation, or equal to a snapshot
 * taken at the last multiple of 64 / 4096 / 262144.  Settled replicas are restarted and not counted as deaths.
 * Exposure = replica-generations at age >= T0 (age counted from the last restart).
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
#define GMAX 96
#define PL 64
typedef uint64_t u64;

static int N, M, K, NL, NE, NP;
static int32_t *nb, *ncls;
static int *lflag, *llen, **lcell, *elen, **eline, *pev, *pnl, **pline;
static u64 *x0, *x1, *x2, *snap, *snapB, *snapC;
static int nterm; static int tk[16], tmode[16];

static u64 rs[4];
static inline u64 rotl(const u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static inline u64 rnd(void) { const u64 r = rotl(rs[1] * 5, 7) * 9, t = rs[1] << 17;
  rs[2] ^= rs[0]; rs[3] ^= rs[1]; rs[1] ^= rs[2]; rs[0] ^= rs[3]; rs[2] ^= t; rs[3] = rotl(rs[3], 45); return r; }
static void seedrng(u64 s) { rs[0] = 0x9E3779B97F4A7C15ULL ^ s; rs[1] = 0xD1B54A32D192ED03ULL + s * 7;
  rs[2] = 0x8CB92BA72F3D8DD7ULL; rs[3] = s * 0x2545F4914F6CDD1DULL + 1; for (int i = 0; i < 20; i++) rnd(); }
static inline double unif(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
/* Bernoulli(p) word, p given as a PB-bit binary fraction v / 2^PB */
#define PB 12
static inline u64 bword(int v) { if (v <= 0) return 0; if (v >= (1 << PB)) return ~0ULL;
  int i = __builtin_ctz(v); u64 w = rnd(); for (i++; i < PB; i++) { u64 r = rnd(); w = (v >> i & 1) ? (w | r) : (w & r); } return w; }
static double pseed; static int rhov[16]; static int nrho;

static void rdi(FILE *f, int32_t *a, size_t n) { if (n && fread(a, 4, n, f) != n) { fprintf(stderr, "short graph\n"); exit(2); } }
static void load(const char *fn) {
  FILE *f = fopen(fn, "rb"); if (!f) { perror(fn); exit(2); }
  int32_t h[3]; rdi(f, h, 3); N = h[0]; M = h[1]; K = h[2];
  nb = malloc(4 * (size_t)N * K + 4); rdi(f, nb, (size_t)N * K);
  for (size_t i = 0; i < (size_t)N * K; i++) if (nb[i] < 0) nb[i] = N + M;
  ncls = malloc(4 * (size_t)M + 4); rdi(f, ncls, M);
  rdi(f, h, 1); NL = h[0];
  lflag = malloc(4 * (NL + 1)); llen = malloc(4 * (NL + 1)); lcell = malloc(sizeof(int *) * (NL + 1));
  for (int l = 0; l < NL; l++) { rdi(f, h, 2); lflag[l] = h[0]; llen[l] = h[1]; lcell[l] = malloc(4 * (llen[l] + 1)); rdi(f, lcell[l], llen[l]); }
  rdi(f, h, 1); NE = h[0];
  elen = malloc(4 * (NE + 1)); eline = malloc(sizeof(int *) * (NE + 1));
  for (int e = 0; e < NE; e++) { rdi(f, h, 1); elen[e] = h[0]; eline[e] = malloc(4 * (elen[e] + 1)); rdi(f, eline[e], elen[e]); }
  rdi(f, h, 1); NP = h[0];
  pev = malloc(4 * (NP + 1)); pnl = malloc(4 * (NP + 1)); pline = malloc(sizeof(int *) * (NP + 1));
  for (int g = 0; g < NP; g++) { rdi(f, h, 2); pev[g] = h[0]; pnl[g] = h[1]; pline[g] = malloc(4 * (pnl[g] + 1)); rdi(f, pline[g], pnl[g]); }
  fclose(f);
  size_t sz = (size_t)(N + M + 1) * W;
  x0 = calloc(sz, 8); x1 = calloc(sz, 8); x2 = calloc(sz, 8); snap = calloc(sz, 8); snapB = calloc(sz, 8); snapC = calloc(sz, 8);
}
static void setrule(int B, int S) {
  nterm = 0;
  for (int k = 0; k <= 15; k++) { int b = B >> k & 1, s = S >> k & 1; if (b || s) { tk[nterm] = k; tmode[nterm++] = b + 2 * s; } }
}
static void fill_noise(void) {
  for (int j = 0; j < M; j++) { int v = rhov[ncls[j] < nrho ? ncls[j] : nrho - 1]; u64 *c = x0 + (size_t)(N + j) * W;
    for (int w = 0; w < W; w++) c[w] = bword(v); }
}
/* one generation of the dynamic cells: x2 <- x1 <- x0 <- f(x0); noise cells of the new x0 are then redrawn */
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
  if (M) fill_noise();
}
/* death noise: clear each of the N*NR dynamic bits independently with probability eps (geometric skipping) */
static double eps = 0, leps;
static void kill_noise(void) {
  double tot = (double)N * NR, pos = -1;
  for (;;) { double u = unif(); if (u <= 0) u = 1e-300; pos += 1.0 + floor(log(u) / leps); if (pos >= tot) break;
    u64 q = (u64)pos; int i = (int)(q / NR), r = (int)(q % NR); x0[(size_t)i * W + r / 64] &= ~(1ULL << (r % 64)); }
}
static void reseed(int r) {
  int w = r / 64; u64 bit = 1ULL << (r % 64); u64 thr = (u64)(pseed * 16777216.0);
  for (int i = 0; i < N; i++) {
    u64 *c = x0 + (size_t)i * W + w;
    if (((rnd() >> 40)) < thr) *c |= bit; else *c &= ~bit;
    x1[(size_t)i * W + w] |= bit; x2[(size_t)i * W + w] &= ~bit; /* history that cannot look settled */
  }
}
static void seed_all(void) {
  for (int r = 0; r < NR; r++) reseed(r);
  if (M) fill_noise();
}
static void line_alive(u64 *alive) {
  for (int l = 0; l < NL; l++) for (int w = 0; w < W; w++) {
    u64 a = 0; for (int j = 0; j < llen[l]; j++) a |= x0[(size_t)lcell[l][j] * W + w]; alive[(size_t)l * W + w] = a; }
}
static void diffmask(const u64 *a, const u64 *b, u64 *s) {
  for (int w = 0; w < W; w++) s[w] = 0;
  for (int i = 0; i < N; i++) for (int w = 0; w < W; w++) s[w] |= a[(size_t)i * W + w] ^ b[(size_t)i * W + w];
  for (int w = 0; w < W; w++) s[w] = ~s[w];
}
static void line_count(int l, int *cnt) {
  u64 c[W][12]; memset(c, 0, sizeof c);
  for (int j = 0; j < llen[l]; j++) for (int w = 0; w < W; w++) {
    u64 a = x0[(size_t)lcell[l][j] * W + w];
    for (int b = 0; a && b < 12; b++) { u64 t = c[w][b] & a; c[w][b] ^= a; a = t; }
  }
  for (int w = 0; w < W; w++) for (int r = 0; r < 64; r++) { int v = 0; for (int b = 0; b < 12; b++) v |= (int)((c[w][b] >> r) & 1) << b; cnt[w * 64 + r] = v; }
}

int main(int argc, char **argv) {
  if (argc < 7) { fprintf(stderr, "usage: see header\n"); return 2; }
  const char *mode = argv[1];
  load(argv[2]); setrule(atoi(argv[3]), atoi(argv[4])); pseed = atof(argv[5]); seedrng(strtoull(argv[6], 0, 10));
  nrho = 1; rhov[0] = 1 << (PB - 1);
  u64 *alive = malloc(8 * (size_t)(NL + 1) * W), sm[W], ev[W];
  if (!strcmp(mode, "trace")) {
    long gens = atol(argv[7]);
    seed_all();
    int *cnt = malloc(4 * NR);
    printf("init"); for (int i = 0; i < N; i++) if (x0[(size_t)i * W] & 1) printf(" %d", i); printf("\n");
    for (long t = 0; t <= gens; t++) {
      if (t) step();
      printf("%ld", t);
      for (int l = 0; l < NL; l++) { line_count(l, cnt); printf(" %d", cnt[0]); }
      printf("\n");
    }
    printf("final"); for (int i = 0; i < N; i++) if (x0[(size_t)i * W] & 1) printf(" %d", i); printf("\n");
    return 0;
  }
  if (strcmp(mode, "qsd")) { fprintf(stderr, "unknown mode\n"); return 2; }
  long T0 = atol(argv[7]); double gens = atof(argv[8]); const char *out = argv[9];
  if (argc > 10) { nrho = 0; char *s = strdup(argv[10]); for (char *t = strtok(s, ","); t && nrho < 16; t = strtok(NULL, ","))
      rhov[nrho++] = (int)floor(atof(t) * (1 << PB) + 0.5); }
  if (argc > 11) { eps = atof(argv[11]); if (eps > 0) leps = log1p(-eps); }
  int det = (M == 0 && eps <= 0);
  size_t sz = (size_t)(N + M + 1) * W * 8;
  seed_all(); memcpy(snap, x0, sz); memcpy(snapB, x0, sz); memcpy(snapC, x0, sz);
  long *age = calloc(NR, 8);
  int nh = 0, maxlen = 0;
  for (int l = 0; l < NL; l++) { if (lflag[l] & 1) nh++; if (llen[l] > maxlen) maxlen = llen[l]; }
  double *hist = calloc((size_t)(maxlen + 1), sizeof(double));
  double (*tr)[32] = calloc(32, sizeof *tr);          /* transitions a -> b of histogram lines, a, b < 32 (31 = more) */
  int *cnt = malloc(4 * (size_t)NR * (NL + 1)), *prevc = calloc((size_t)NR * (NL + 1), 4);
  short *ring = calloc((size_t)NR * (NL + 1) * PL, sizeof(short));
  double *prof = calloc((size_t)(NP + 1) * 16 * PL, sizeof(double)), *profn = calloc(NP + 1, sizeof(double));
  double gapE[GMAX + 1] = {0}, gapN = 0;
  double exposure = 0; long ndeath_e[256] = {0}, early = 0, settles = 0, settles_exp = 0, ndeaths = 0;
  double aexp[64] = {0}, adeath[64] = {0};
  char dfn[4096]; snprintf(dfn, sizeof dfn, "%s.deaths", out); FILE *dl = fopen(dfn, "w");
  for (double g = 0; g < gens; g += 1) {
    u64 expm[W] = {0};
    for (int r = 0; r < NR; r++) if (age[r] >= T0) { expm[r / 64] |= 1ULL << (r % 64); exposure += 1;
      int b = 0; long a = age[r] - T0 + 1; while (a > 1) { a >>= 1; b++; } aexp[b] += 1; }
    step();
    if (eps > 0) kill_noise();
    for (int r = 0; r < NR; r++) age[r]++;
    long t = (long)g + 1;
    line_alive(alive);
    int killed[NR]; memset(killed, 0, sizeof killed);
    for (int e = 0; e < NE; e++) {
      for (int w = 0; w < W; w++) { u64 d = ~0ULL; for (int j = 0; j < elen[e]; j++) d &= ~alive[(size_t)eline[e][j] * W + w]; ev[w] = d; }
      for (int w = 0; w < W; w++) for (u64 m = ev[w]; m; m &= m - 1) {
        int r = w * 64 + __builtin_ctzll(m);
        if (killed[r]) continue;
        killed[r] = 1;
        if (expm[r / 64] >> (r % 64) & 1) {
          ndeath_e[e < 255 ? e : 255]++; ndeaths++;
          int b = 0; long a = age[r] - 1 - T0 + 1; while (a > 1) { a >>= 1; b++; } adeath[b] += 1;
          if (dl) fprintf(dl, "%d %ld\n", e, age[r]);
          if (age[r] >= T0 + PL + 2) for (int gq = 0; gq < NP; gq++) if (pev[gq] == e) {
            profn[gq] += 1;
            for (int i = 0; i < pnl[gq] && i < 16; i++) for (int j = 1; j <= PL; j++)
              prof[((size_t)gq * 16 + i) * PL + (j - 1)] += ring[((size_t)r * NL + pline[gq][i]) * PL + ((t - j) % PL + PL) % PL];
          }
        } else early++;
      }
    }
    if (det) {
      u64 s8[W]; diffmask(x0, x2, sm);
      diffmask(x0, snap, s8); for (int w = 0; w < W; w++) sm[w] |= s8[w];
      if (t > 4096) { diffmask(x0, snapB, s8); for (int w = 0; w < W; w++) sm[w] |= s8[w]; }
      if (t > 262144) { diffmask(x0, snapC, s8); for (int w = 0; w < W; w++) sm[w] |= s8[w]; }
      if (t % 64 == 0) memcpy(snap, x0, sz);
      if (t % 4096 == 0) memcpy(snapB, x0, sz);
      if (t % 262144 == 0) memcpy(snapC, x0, sz);
      for (int r = 0; r < NR; r++) if (!killed[r] && (sm[r / 64] >> (r % 64) & 1)) { killed[r] = 2; settles++; if (expm[r / 64] >> (r % 64) & 1) settles_exp++; }
    }
    u64 nextm[W] = {0};
    for (int r = 0; r < NR; r++) if (!killed[r] && age[r] >= T0) nextm[r / 64] |= 1ULL << (r % 64);
    for (int l = 0; l < NL; l++) {
      if (!(lflag[l] & 5)) continue;
      int *c = cnt + (size_t)l * NR;
      line_count(l, c);
      if (lflag[l] & 1) for (int r = 0; r < NR; r++) {
        if (!killed[r] && age[r] >= T0) hist[c[r]] += 1;
        if (expm[r / 64] >> (r % 64) & 1) { int a = prevc[(size_t)r * NL + l], b = c[r]; if (a > 31) a = 31; if (b > 31) b = 31;
          if (b == 0 || !killed[r]) tr[a][b] += 1; }
      }
      for (int r = 0; r < NR; r++) { prevc[(size_t)r * NL + l] = c[r]; ring[((size_t)r * NL + l) * PL + t % PL] = (short)c[r]; }
    }
    for (int l = 0; l < NL; l++) if (lflag[l] & 2) {
      int len = llen[l];
      for (int w = 0; w < W; w++) { if (!nextm[w]) continue; gapN += (double)len * __builtin_popcountll(nextm[w]);
        for (int s = 0; s < len; s++) { u64 acc = ~nextm[w];
          for (int q = 1; q <= GMAX && q <= len; q++) { acc |= x0[(size_t)lcell[l][(s + q - 1) % len] * W + w]; if (!~acc) break; gapE[q] += __builtin_popcountll(~acc); } } }
    }
    for (int r = 0; r < NR; r++) if (killed[r]) { reseed(r); age[r] = 0; }
  }
  FILE *f = fopen(out, "w");
  fprintf(f, "replicas %d\nT0 %ld\ngens %.0f\nexposure %.0f\ndeaths %ld\nearly %ld\nsettles %ld\nsettles_exposed %ld\nhistlines %d\ncells %d\nnoise %d\n",
          NR, T0, gens, exposure, ndeaths, early, settles, settles_exp, nh, N, M);
  fprintf(f, "rho"); for (int i = 0; i < nrho; i++) fprintf(f, " %.6f", rhov[i] / (double)(1 << PB)); fprintf(f, "\neps %g\n", eps);
  fprintf(f, "deaths_by_event"); for (int e = 0; e < NE && e < 256; e++) fprintf(f, " %ld", ndeath_e[e]); fprintf(f, "\n");
  fprintf(f, "age_exposure"); for (int b = 0; b < 64; b++) fprintf(f, " %.0f", aexp[b]); fprintf(f, "\n");
  fprintf(f, "age_deaths"); for (int b = 0; b < 64; b++) fprintf(f, " %.0f", adeath[b]); fprintf(f, "\n");
  fprintf(f, "hist"); for (int k = 0; k <= maxlen; k++) fprintf(f, " %.0f", hist[k]); fprintf(f, "\n");
  fprintf(f, "trans"); for (int a = 0; a < 32; a++) for (int b = 0; b < 32; b++) fprintf(f, " %.0f", tr[a][b]); fprintf(f, "\n");
  fprintf(f, "gapN %.0f\ngapE", gapN); for (int q = 0; q <= GMAX; q++) fprintf(f, " %.0f", gapE[q]); fprintf(f, "\n");
  for (int gq = 0; gq < NP; gq++) { fprintf(f, "profn%d %.0f\n", gq, profn[gq]);
    for (int i = 0; i < pnl[gq] && i < 16; i++) { fprintf(f, "prof%d_%d", gq, i);
      for (int j = 0; j < PL; j++) fprintf(f, " %.0f", prof[((size_t)gq * 16 + i) * PL + j]); fprintf(f, "\n"); } }
  fclose(f); if (dl) fclose(dl);
  return 0;
}
