/* nb (research/audit/blastnoisy): brute force of the noisy hull chain of research/blast/noisy, written from the
 * specification in that directory's README ("The chain, exactly"), not from its nz.c.  The vessel is a graph file
 * written by research/audit/blast/geom.py (hull R; face 0 is d = (+,+,+), the watched face); the rule and the
 * bit-sliced step are those of research/audit/blast/fd.c (512 hulls, one AVX-512 word per cell).
 *
 * Noise region N: cells in none of layers 0..5 of face 0 and in none of layers 0..2 of faces 1..7, in the order of
 * the vessel file (x, then y, then z ascending).  Board B: the smallest power of two >= 4|N|.  After every
 * generation each hull receives M darts; a dart on square s < |N| sets cell N[s] to the dart's coin.
 *   MODE L (literal): every dart is 16 bits of the generator's stream (low 16 bits of a word first): the square is
 *                     the low log2(B) bits, the coin is bit 15.
 *   MODE F (fast, the same law): per hull K ~ Binomial(M, |N|/B) by inversion of one 64-bit word, then K darts on N,
 *                     two to a word (low 32 bits first; a hull's odd half is dropped), each a uniform cell index by
 *                     the multiply-and-reject method (index = high word of x * |N|; exact); then, after all hulls,
 *                     8 words of coins per cell of N in order: a cell that was hit takes its bit of them (the coin
 *                     of the last dart on a cell is a fair coin independent of everything else).
 *
 *   nb VESSEL info                                   |N|, B
 *   nb VESSEL cdf M                                  the thresholds of MODE F's binomial (u64, one a line)
 *   nb VESSEL trace INIT GENS OUT M SEED MODE        INIT: lines "replica cell" (replicas 0..3 are written);
 *                                                    OUT: generations 0..GENS, 4 rows of n bits each
 *   nb VESSEL dstat M MODE NGEN SEED                 statistics of one generation's darts (hits and coins)
 *   nb VESSEL run SEED GENS M MODE [BURN=200] [REPORT=2000000] [MAXAGE=0]
 *       life protocol of the README: soup 0.35, a life ends at the first generation with any face empty, a
 *       hull-generation counts when the age after the step exceeds BURN.  A line of totals every REPORT generations
 *       (the last line is the result):
 *       RES n A nN B M mode seed gens exposure d0..d7 ties young settled
 *       (d_f: lives older than BURN at whose end face f was empty; ties: those of d0 with another face empty too)
 *       With MAXAGE > 0 a hull that reaches that age is replaced by a new soup (not a death): every counted
 *       hull-generation then has BURN < age <= MAXAGE (the hazard of young hulls).
 *       and, after each RES line, the same by the age of the hull (lower edges 0, 1e3, 3e3, 1e4, ... generations):
 *       AGE lower_edge exposure d0 d0+...+d7
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
typedef uint64_t u64;
typedef u64 v8 __attribute__((vector_size(64), aligned(64)));
#define NREP 512
#define NTR 4

static u64 sm;
static inline u64 rnd(void) { u64 z = (sm += 0x9e3779b97f4a7c15ULL); z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
  z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; return z ^ (z >> 31); }
static u64 dbuf; static int dleft;
static inline unsigned bits(int nbit) {
  if (dleft < nbit) { dbuf = rnd(); dleft = 64; }
  unsigned v = (unsigned)(dbuf & ((1ULL << nbit) - 1)); dbuf >>= nbit; dleft -= nbit; return v;
}

static int n, nf, nlay;
static int *nb;
static int **lsz, ***lc;
static int nN, B, logB, M, *Nl;
static u64 *bcdf; static int guide[4097];

static inline v8 rule(const v8 *x, v8 me) {
#define FA(s, c, p, q, r) do { v8 t_ = (p) ^ (q); s = t_ ^ (r); c = ((p) & (q)) | (t_ & (r)); } while (0)
  v8 s1, c1, s2, c2, s3, c3, s4, c4, S, C5, b0, C6, t1, d1, t2, d2, b1, e, b2, b3;
  FA(s1, c1, x[0], x[1], x[2]); FA(s2, c2, x[3], x[4], x[5]); FA(s3, c3, x[6], x[7], x[8]); FA(s4, c4, x[9], x[10], x[11]);
  FA(S, C5, s1, s2, s3); b0 = S ^ s4; C6 = S & s4;
  FA(t1, d1, c1, c2, c3); FA(t2, d2, c4, C5, C6); b1 = t1 ^ t2; e = t1 & t2;
  FA(b2, b3, d1, d2, e);
  return ~b3 & ((b2 & ~b1) | (me & ~b2 & b1 & b0));
}
static void step(const v8 *a, v8 *b) {
  for (int i = 0; i < n; i++) {
    const int *q = nb + 12 * i;
    v8 x[12];
    for (int t = 0; t < 12; t++) x[t] = a[q[t]];
    b[i] = rule(x, a[i]);
  }
  b[n] = (v8){0};
}
static inline int bitof(const v8 *s, int cell, int r) { return (int)((s[cell][r >> 6] >> (r & 63)) & 1); }
static inline void setbit(v8 *s, int cell, int r, int v) {
  u64 m = 1ULL << (r & 63);
  s[cell][r >> 6] = (s[cell][r >> 6] & ~m) | (v ? m : 0);
}
static void reseed(v8 *s, int r) { for (int i = 0; i < n; i++) setbit(s, i, r, rnd() < (u64)(0.35 * 18446744073709551616.0)); }

static void setup_binom(void) {
  bcdf = malloc(sizeof(u64) * (M + 1));
  long double p = (long double)nN / B, acc = 0;
  for (int k = 0; k <= M; k++) {
    long double lp = lgammal(M + 1.0L) - lgammal(k + 1.0L) - lgammal(M - k + 1.0L) + k * logl(p) + (M - k) * log1pl(-p);
    acc += expl(lp);
    long double t = acc * 18446744073709551616.0L;
    bcdf[k] = (k == M || t >= 18446744073709551615.0L) ? UINT64_MAX : (u64)t;
  }
  int k = 0;
  for (int j = 0; j <= 4096; j++) {
    u64 lo = j < 4096 ? (u64)j << 52 : UINT64_MAX;
    while (k < M && lo >= bcdf[k]) k++;
    guide[j] = k;
  }
}
static inline int binom(u64 u) { int k = guide[u >> 52]; k += (k < M) & (u >= bcdf[k]); while (k < M && u >= bcdf[k]) k++; return k; }

static u64 *hm;
static inline unsigned cellidx(uint32_t x) {
  u64 p = (u64)x * (uint32_t)nN;
  if ((uint32_t)p < (uint32_t)nN) {
    uint32_t t = (uint32_t)(-(uint32_t)nN) % (uint32_t)nN;
    while ((uint32_t)p < t) { x = (uint32_t)rnd(); p = (u64)x * (uint32_t)nN; }
  }
  return (unsigned)(p >> 32);
}
static void darts(v8 *s, int mode) {
  if (!M) return;
  if (mode == 'L') {
    for (int r = 0; r < NREP; r++)
      for (int j = 0; j < M; j++) {
        unsigned v = bits(16), sq = v & (unsigned)(B - 1);
        if (sq < (unsigned)nN) setbit(s, Nl[sq], r, (int)(v >> 15));
      }
  } else {
    memset(hm, 0, sizeof(u64) * 8 * nN);
    for (int r = 0; r < NREP; r++) {
      int K = binom(rnd());
      u64 *col = hm + (r >> 6), m = 1ULL << (r & 63);
      for (int j = 0; j < K; j += 2) {
        u64 w = rnd();
        col[8 * cellidx((uint32_t)w)] |= m;
        col[8 * cellidx((uint32_t)(w >> 32))] |= (j + 1 < K) ? m : 0;
      }
    }
    for (int k = 0; k < nN; k++) {
      v8 c, mk;
      for (int w = 0; w < 8; w++) { c[w] = rnd(); mk[w] = hm[8 * k + w]; }
      s[Nl[k]] = (s[Nl[k]] & ~mk) | (c & mk);
    }
  }
}

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: see the head of nb.c\n"); return 1; }
  FILE *fp = fopen(argv[1], "rb"); if (!fp) { perror(argv[1]); return 1; }
  int32_t v;
#define RD() (fread(&v, 4, 1, fp) == 1 ? v : (fprintf(stderr, "short read\n"), exit(1), 0))
  n = RD(); nb = malloc(sizeof(int) * 12 * n);
  for (int i = 0; i < 12 * n; i++) nb[i] = RD();
  nf = RD(); nlay = RD();
  lsz = malloc(sizeof(int *) * nf); lc = malloc(sizeof(int **) * nf);
  for (int f = 0; f < nf; f++) {
    lsz[f] = malloc(sizeof(int) * nlay); lc[f] = malloc(sizeof(int *) * nlay);
    for (int l = 0; l < nlay; l++) {
      lsz[f][l] = RD(); lc[f][l] = malloc(sizeof(int) * lsz[f][l]);
      for (int k = 0; k < lsz[f][l]; k++) lc[f][l][k] = RD();
    }
  }
  fclose(fp);
  if (nf != 8 || nlay < 6) { fprintf(stderr, "not a hull file with 6 layers a face\n"); return 1; }
  char *out = calloc(n, 1);
  for (int f = 0; f < nf; f++) for (int l = 0; l < (f == 0 ? 6 : 3); l++) for (int k = 0; k < lsz[f][l]; k++) out[lc[f][l][k]] = 1;
  Nl = malloc(sizeof(int) * n); nN = 0;
  for (int i = 0; i < n; i++) if (!out[i]) Nl[nN++] = i;
  for (B = 1, logB = 0; B < 4 * nN; B <<= 1) logB++;
  hm = malloc(sizeof(u64) * 8 * (nN + 1));
  int A = lsz[0][0];
  if (!strcmp(argv[2], "info")) { printf("n %d A %d nN %d B %d\n", n, A, nN, B); return 0; }
  v8 *a = aligned_alloc(64, sizeof(v8) * (n + 1)), *b = aligned_alloc(64, sizeof(v8) * (n + 1));
  memset(a, 0, sizeof(v8) * (n + 1)); memset(b, 0, sizeof(v8) * (n + 1));

  if (!strcmp(argv[2], "cdf")) {
    M = atoi(argv[3]); setup_binom();
    for (int k = 0; k <= M; k++) printf("%llu\n", (unsigned long long)bcdf[k]);
    return 0;
  }
  if (!strcmp(argv[2], "trace")) {
    FILE *in = fopen(argv[3], "r"); int r, c; while (fscanf(in, "%d %d", &r, &c) == 2) setbit(a, c, r, 1); fclose(in);
    long gens = atol(argv[4]); FILE *o = fopen(argv[5], "wb");
    M = atoi(argv[6]); sm = strtoull(argv[7], 0, 10) * 0x9e3779b97f4a7c15ULL + 12345; int mode = argv[8][0];
    if (M) setup_binom();
    uint8_t *row = malloc((n + 7) / 8);
    for (long g = 0; g <= gens; g++) {
      if (g) { step(a, b); v8 *t = a; a = b; b = t; darts(a, mode); }
      for (int rr = 0; rr < NTR; rr++) {
        memset(row, 0, (n + 7) / 8);
        for (int i = 0; i < n; i++) if (bitof(a, i, rr)) row[i >> 3] |= (uint8_t)(1 << (i & 7));
        fwrite(row, 1, (n + 7) / 8, o);
      }
    }
    fclose(o); return 0;
  }
  if (!strcmp(argv[2], "dstat")) {
    M = atoi(argv[3]); int mode = argv[4][0]; long ng = atol(argv[5]);
    sm = strtoull(argv[6], 0, 10) * 0x9e3779b97f4a7c15ULL + 12345; setup_binom();
    double sd = 0, sd2 = 0, ones = 0, hits = 0; long bad = 0;
    double *ch = calloc(nN, sizeof(double)); int *D = malloc(sizeof(int) * NREP);
    for (long g = 0; g < ng; g++) {
      for (int i = 0; i <= n; i++) { a[i] = (v8){0}; b[i] = ~(v8){0}; }
      u64 s0 = sm, b0 = dbuf; int l0 = dleft;
      darts(a, mode);
      sm = s0; dbuf = b0; dleft = l0;
      darts(b, mode);
      memset(D, 0, sizeof(int) * NREP);
      memset(out, 0, n);
      for (int k = 0; k < nN; k++) {
        int c = Nl[k]; out[c] = 1;
        for (int r = 0; r < NREP; r++) {
          int x0 = bitof(a, c, r), x1 = bitof(b, c, r);
          if (x0 == x1) { D[r]++; ch[k]++; hits++; ones += x0; }
        }
      }
      for (int i = 0; i < n; i++) if (!out[i]) for (int w = 0; w < 8; w++) bad += (a[i][w] != 0) + (b[i][w] != ~0ULL);
      for (int r = 0; r < NREP; r++) { sd += D[r]; sd2 += (double)D[r] * D[r]; }
    }
    double tot = (double)ng * NREP, mean = sd / tot, var = sd2 / tot - mean * mean, mn = 1e9, mx = 0;
    for (int k = 0; k < nN; k++) { double f = ch[k] / tot; if (f < mn) mn = f; if (f > mx) mx = f; }
    printf("DSTAT nN %d B %d M %d mode %c trials %.0f mean_distinct %.6f var_distinct %.6f coin_ones %.6f cell_freq_min %.6f cell_freq_max %.6f outside_touched %ld\n",
           nN, B, M, mode, tot, mean, var, ones / hits, mn, mx, bad);
    return 0;
  }

  /* run */
  u64 seed = strtoull(argv[3], 0, 10); sm = seed * 0x9e3779b97f4a7c15ULL + 12345;
  u64 gens = strtoull(argv[4], 0, 10);
  M = atoi(argv[5]); int mode = argv[6][0];
  uint32_t burn = argc > 7 ? (uint32_t)atoi(argv[7]) : 200;
  u64 report = argc > 8 ? strtoull(argv[8], 0, 10) : 2000000;
  uint32_t maxage = argc > 9 ? (uint32_t)atol(argv[9]) : 0;
  if (M) setup_binom();
  static uint32_t age[NREP];
  for (int r = 0; r < NREP; r++) reseed(a, r);
  v8 *snap = aligned_alloc(64, sizeof(v8) * (n + 1)); memcpy(snap, a, sizeof(v8) * (n + 1));
  u64 exposure = 0, d[8] = {0}, ties = 0, young = 0, settled = 0;
#define NAB 12
  static const uint32_t aedge[NAB] = {0, 1000, 3000, 10000, 30000, 100000, 300000, 1000000, 3000000, 10000000, 30000000, 100000000};
  static u64 aE[NAB], aD0[NAB], aD[NAB]; static uint8_t abin[NREP];
  for (u64 g = 1; g <= gens; g++) {
    step(a, b); { v8 *t = a; a = b; b = t; }
    darts(a, mode);
    v8 dead = (v8){0}, fdv[8];
    for (int f = 0; f < 8; f++) {
      v8 any = (v8){0};
      for (int k = 0; k < A; k++) any |= a[lc[f][0][k]];
      fdv[f] = ~any; dead |= ~any;
    }
    for (int r = 0; r < NREP; r++) {
      age[r]++;
      if (abin[r] + 1 < NAB && age[r] >= aedge[abin[r] + 1]) abin[r]++;
      if (age[r] > burn) { exposure++; aE[abin[r]]++; }
    }
    for (int w = 0; w < 8; w++) while (dead[w]) {
      int s = __builtin_ctzll(dead[w]); dead[w] &= dead[w] - 1; int r = w * 64 + s;
      if (age[r] > burn) {
        int nd = 0;
        for (int f = 0; f < 8; f++) if ((fdv[f][w] >> s) & 1) { d[f]++; nd++; }
        if (((fdv[0][w] >> s) & 1) && nd > 1) ties++;
        aD[abin[r]] += (u64)nd; aD0[abin[r]] += (fdv[0][w] >> s) & 1;
      } else young++;
      reseed(a, r); age[r] = 0; abin[r] = 0;
      for (int i = 0; i < n; i++) setbit(snap, i, r, !bitof(a, i, r));
    }
    if (maxage) for (int r = 0; r < NREP; r++) if (age[r] >= maxage) { reseed(a, r); age[r] = 0; abin[r] = 0; }
    if (!M && g % 840 == 0) {
      v8 df = (v8){0};
      for (int i = 0; i < n; i++) df |= a[i] ^ snap[i];
      for (int r = 0; r < NREP; r++) if (!((df[r >> 6] >> (r & 63)) & 1)) { settled++; reseed(a, r); age[r] = 0; abin[r] = 0; }
      memcpy(snap, a, sizeof(v8) * (n + 1));
    }
    if (g % report == 0 || g == gens) {
      printf("RES n %d A %d nN %d B %d M %d mode %c seed %llu gens %llu exposure %llu d", n, A, nN, B, M, mode,
             (unsigned long long)seed, (unsigned long long)g, (unsigned long long)exposure);
      for (int f = 0; f < 8; f++) printf(" %llu", (unsigned long long)d[f]);
      printf(" ties %llu young %llu settled %llu\n", (unsigned long long)ties, (unsigned long long)young, (unsigned long long)settled);
      for (int k = 0; k < NAB; k++) if (aE[k]) printf("AGE %u %llu %llu %llu\n", aedge[k], (unsigned long long)aE[k], (unsigned long long)aD0[k], (unsigned long long)aD[k]);
      fflush(stdout);
    }
  }
  return 0;
}
