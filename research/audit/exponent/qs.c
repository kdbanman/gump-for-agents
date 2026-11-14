/* qs.c -- quasi-stationary hazard of face death for B45/S345 on a cell graph written by graphs.py.
 * Audit code for research/audit/REVIEW-exponent.md; shares no code with research/theory/exponent/drv.c.
 *
 *   qs GRAPH T0 SEED MAXSEC MAXDEATHS [P0]
 *
 * 64*W replicas, bit-sliced.  Each replica starts from an i.i.d. soup of density P0 (default 0.35) on the dynamic
 * cells.  Every generation: noise cells are redrawn (Bernoulli(rho), 16-bit binary expansion), dynamic cells step.
 * A transition made by a replica whose age before the step is >= T0 is "exposed".  After the step:
 *   death  = some death event fires (all its lines empty)  -> counted if exposed (each face that died counts once)
 *   censor = otherwise, a censor event fires, or (settle=1) the state equals the state 2 generations back or the
 *            snapshot taken at the last power-of-two age (Brent: catches every period eventually)
 * Dead or censored replicas are replaced by fresh soups (age 0).  Output: exposure, deaths, censored counts,
 * the mean population of the death lines over exposed generations, hazard by age bin, death-age moments.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define W 4
#define NR (64 * W)
typedef uint64_t u64;

static u64 rs;
static inline u64 rnd(void) {              /* wyrand */
  rs += 0xa0761d6478bd642fULL;
  __uint128_t t = (__uint128_t)rs * (rs ^ 0xe7037ed1a0b428dbULL);
  return (u64)(t >> 64) ^ (u64)t;
}
static inline u64 bern(int v16) {          /* each bit 1 with probability v16 / 65536 */
  if (v16 <= 0) return 0; if (v16 >= 65536) return ~0ULL;
  u64 w = 0;
  for (int i = 0; i < 16; i++) { u64 r = rnd(); w = ((v16 >> i) & 1) ? (w | r) : (w & r); }
  return w;
}

static int N, M, NL, ND, NC, SETTLE;
static int32_t *nb, *rho;
static int *ll, **lc, *dl, **de, *cl, **ce;

static int32_t rdi(FILE *f) { int32_t v; if (fread(&v, 4, 1, f) != 1) { fprintf(stderr, "short\n"); exit(2); } return v; }
static void rdgroup(FILE *f, int *n, int **len, int ***arr) {
  *n = rdi(f); *len = malloc(sizeof(int) * (*n + 1)); *arr = malloc(sizeof(int *) * (*n + 1));
  for (int i = 0; i < *n; i++) { (*len)[i] = rdi(f); (*arr)[i] = malloc(sizeof(int) * ((*len)[i] + 1));
    for (int j = 0; j < (*len)[i]; j++) (*arr)[i][j] = rdi(f); }
}

static void stepall(u64 (*x)[W], u64 (*y)[W]) {   /* B45/S345: alive next iff n in {4,5}, or alive and n = 3 */
for (int i = 0; i < N; i++) {
  const int32_t *ni = nb + (size_t)i * 12;
  for (int w = 0; w < W; w++) {
    u64 c0b = 0, c1 = 0, c2 = 0, c3 = 0;
    for (int k = 0; k < 12; k++) { u64 a = x[ni[k]][w];
      u64 t0 = c0b & a; c0b ^= a; u64 t1 = c1 & t0; c1 ^= t0; u64 t2 = c2 & t1; c2 ^= t1; c3 |= t2; }
    u64 s = x[i][w];
    y[i][w] = ~c3 & ((c2 & ~c1) | (s & ~c2 & c1 & c0b));
  }
}
}

int main(int argc, char **argv) {
  if (argc < 6) { fprintf(stderr, "qs GRAPH T0 SEED MAXSEC MAXDEATHS [P0]\n"); return 2; }
  FILE *f = fopen(argv[1], "rb"); if (!f) { perror(argv[1]); return 2; }
  N = rdi(f); M = rdi(f);
  nb = malloc(sizeof(int32_t) * N * 12);
  for (int i = 0; i < N * 12; i++) { int v = rdi(f); nb[i] = v < 0 ? N + M : v; }
  rho = malloc(sizeof(int32_t) * (M + 1)); for (int i = 0; i < M; i++) rho[i] = rdi(f);
  rdgroup(f, &NL, &ll, &lc); rdgroup(f, &ND, &dl, &de); rdgroup(f, &NC, &cl, &ce); SETTLE = rdi(f); fclose(f);
  long T0 = atol(argv[2]); rs = strtoull(argv[3], 0, 10) * 0x9E3779B97F4A7C15ULL + 12345; for (int i = 0; i < 8; i++) rnd();
  double maxsec = atof(argv[4]); long maxd = atol(argv[5]); double p0 = argc > 6 ? atof(argv[6]) : 0.35;
  int v0 = (int)floor(p0 * 65536 + 0.5);
  size_t S = (size_t)(N + M + 1);
  u64 (*x)[W] = calloc(S, sizeof *x), (*y)[W] = calloc(S, sizeof *y), (*xm1)[W] = calloc(S, sizeof *xm1),
      (*xm2)[W] = calloc(S, sizeof *xm2), (*snap)[W] = calloc(S, sizeof *snap);
  long age[NR]; memset(age, 0, sizeof age);
  u64 snapvalid[W] = {0};
  for (int i = 0; i < N; i++) for (int w = 0; w < W; w++) x[i][w] = bern(v0);
  double expo = 0, deaths = 0, censS = 0, censC = 0, early = 0, popsum = 0, sa = 0, sa2 = 0, nd_rep = 0;
  double bexp[40] = {0}, bdth[40] = {0};
  double gens = 0; clock_t c0 = clock();
  u64 la[64][W];                              /* line alive masks (NL <= 64 assumed for death/censor lines) */
  int NLc = NL < 64 ? NL : 64;
  if (maxd < 0) {                             /* trace: dump 4 replicas, run -maxd plain steps, dump again */
    for (int pass = 0; pass < 2; pass++) {
      for (int r = 0; r < 4; r++) { int w = (r * 67) / 64; u64 bit = 1ULL << ((r * 67) % 64);
        for (int i = 0; i < N; i++) putchar((x[i][w] & bit) ? '1' : '0'); putchar('\n'); }
      if (pass) break;
      for (long g = 0; g < -maxd; g++) {
        for (int w = 0; w < W; w++) x[N + M][w] = 0;
        stepall(x, y);
        void *t = x; x = y; y = t;
      }
    }
    return 0;
  }
  for (;;) {
    if (((long)gens & 1023) == 0) {
      double el = (double)(clock() - c0) / CLOCKS_PER_SEC;
      if (el > maxsec || deaths >= maxd) break;
    }
    gens += 1;
    u64 ex[W] = {0};
    for (int r = 0; r < NR; r++) if (age[r] >= T0) ex[r / 64] |= 1ULL << (r % 64);
    /* population of death lines before the step, exposed replicas only */
    for (int d = 0; d < ND; d++) for (int q = 0; q < dl[d]; q++) { int l = de[d][q];
      for (int j = 0; j < ll[l]; j++) for (int w = 0; w < W; w++) popsum += __builtin_popcountll(x[lc[l][j]][w] & ex[w]); }
    for (int j = 0; j < M; j++) for (int w = 0; w < W; w++) x[N + j][w] = bern(rho[j]);
    for (int w = 0; w < W; w++) x[N + M][w] = 0;
    stepall(x, y);
    if (SETTLE) { void *t = xm2; xm2 = xm1; xm1 = x; x = y; y = t; }
    else { void *t = x; x = y; y = t; }
    for (int r = 0; r < NR; r++) age[r]++;
    for (int l = 0; l < NLc; l++) for (int w = 0; w < W; w++) { u64 a = 0;
      for (int j = 0; j < ll[l]; j++) a |= x[lc[l][j]][w]; la[l][w] = a; }
    u64 dead[W] = {0}, cens[W] = {0};
    int ndf[NR]; memset(ndf, 0, sizeof ndf);
    for (int d = 0; d < ND; d++) for (int w = 0; w < W; w++) { u64 e = ~0ULL;
      for (int q = 0; q < dl[d]; q++) e &= ~la[de[d][q]][w];
      dead[w] |= e; for (u64 m = e; m; m &= m - 1) ndf[w * 64 + __builtin_ctzll(m)]++; }
    for (int c = 0; c < NC; c++) for (int w = 0; w < W; w++) { u64 e = ~0ULL;
      for (int q = 0; q < cl[c]; q++) e &= ~la[ce[c][q]][w]; cens[w] |= e & ~dead[w]; }
    for (int w = 0; w < W; w++) { u64 m = cens[w] & ex[w]; censC += __builtin_popcountll(m); }
    if (SETTLE) {
      u64 d2[W] = {0}, ds[W] = {0};
      for (int i = 0; i < N; i++) for (int w = 0; w < W; w++) { d2[w] |= x[i][w] ^ xm2[i][w]; ds[w] |= x[i][w] ^ snap[i][w]; }
      for (int w = 0; w < W; w++) { u64 st = (~d2[w] | (~ds[w] & snapvalid[w])) & ~dead[w] & ~cens[w];
        censS += __builtin_popcountll(st & ex[w]); cens[w] |= st; }
    }
    for (int r = 0; r < NR; r++) {
      int w = r / 64; u64 bit = 1ULL << (r % 64);
      int exposed = (ex[w] & bit) != 0;
      if (exposed) { expo += 1; int b = 0; long a = (age[r] - 1) / (T0 > 0 ? T0 : 1); while (a > 0 && b < 39) { a >>= 1; b++; } bexp[b] += 1;
        if (dead[w] & bit) { deaths += ndf[r]; nd_rep += 1; bdth[b] += 1; double t = age[r]; sa += t; sa2 += t * t; } }
      else if (dead[w] & bit) early += 1;
      if ((dead[w] | cens[w]) & bit) {
        for (int i = 0; i < N; i++) { u64 v = bern(v0) & bit; x[i][w] = (x[i][w] & ~bit) | v; }
        for (size_t i = 0; i < S; i++) { xm1[i][w] |= bit; xm2[i][w] &= ~bit; }
        snapvalid[w] &= ~bit; age[r] = 0;
      } else if (SETTLE && age[r] >= 2 && (age[r] & (age[r] - 1)) == 0) {
        for (int i = 0; i < N; i++) snap[i][w] = (snap[i][w] & ~bit) | (x[i][w] & bit);
        snapvalid[w] |= bit;
      }
    }
  }
  double nlines = 0; for (int d = 0; d < ND; d++) nlines += 1;
  double h = deaths / (nlines * expo);
  printf("{\"gens\": %.0f, \"exposure\": %.0f, \"deaths\": %.0f, \"death_replicas\": %.0f, \"faces\": %.0f, "
         "\"censored_settled\": %.0f, \"censored_cut\": %.0f, \"early\": %.0f, \"lntau\": %.5f, \"err\": %.5f, "
         "\"mean_face_pop\": %.4f, \"death_age_mean\": %.2f, \"death_age_sd\": %.2f, \"T0\": %ld, ",
         gens, expo, deaths, nd_rep, nlines, censS, censC, early, -log(h), 1 / sqrt(deaths), popsum / (nlines * expo),
         sa / nd_rep, sqrt(sa2 / nd_rep - (sa / nd_rep) * (sa / nd_rep)), T0);
  printf("\"age_bins_T0_units\": [");
  int first = 1;
  for (int b = 0; b < 40; b++) if (bexp[b] > 0) { printf("%s[%d, %.0f, %.0f]", first ? "" : ", ", b, bexp[b], bdth[b]); first = 0; }
  printf("]}\n");
  return 0;
}
