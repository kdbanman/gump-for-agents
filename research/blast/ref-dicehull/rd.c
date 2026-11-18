/* rd.c: referee's own stepper for the hull dice chain (research/blast/ref-dicehull). 256 lanes, bit-sliced.
   Graph from geom.py. Rule cells (index < NRULE): gump B45/S345 on 12 neighbours (index n = dead outside).
   Dice cells (index >= NRULE): replaced after every generation by independent coins of density DPM/64 (32 = fair).

   rd G.bin val INIT.bin GENS OUT.bin SEED DPM   validation: lanes 0..3 start from INIT (n bytes each), every generation's
                                                state of those lanes (dice included) is written to OUT (n bytes per lane).
   rd G.bin run SEED GENS BURN DPM              brute force: every lane starts as a soup (density 1/2 on all cells); after
        BURN generations its exposure counts; when the watched face (cells 0..A-1) is empty the death is booked (if
        the lane was counting) and the lane is reseeded. tau = counted generations with the face alive / deaths.
        Every 4 generations: population (HIST = its histogram) of the watched face (mean, variance) and per-cell occupancy, counting lanes only.
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
typedef uint64_t u64;
typedef u64 vec __attribute__((vector_size(32)));
#define NL 256
static u64 s[4];
static inline u64 rotl(u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static inline u64 rnd(void) { u64 r = rotl(s[1] * 5, 7) * 9, t = s[1] << 17; s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2]; s[0] ^= s[3]; s[2] ^= t; s[3] = rotl(s[3], 45); return r; }
static void seedrng(u64 x) { for (int i = 0; i < 4; i++) { x += 0x9E3779B97F4A7C15ULL; u64 z = x; z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL; z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL; s[i] = z ^ (z >> 31); } }
static inline vec rvec(void) { vec v = {rnd(), rnd(), rnd(), rnd()}; return v; }
/* a word whose bits are 1 with probability dpm/64: bitwise comparison of a 6-bit uniform number with dpm */
static inline vec coin(int dpm) {
  if (dpm == 32) return rvec();
  vec lt = {0, 0, 0, 0}, eq = ~lt;
  for (int k = 5; k >= 0; k--) { vec r = rvec(); if ((dpm >> k) & 1) { lt |= eq & ~r; eq &= r; } else eq &= ~r; }
  return lt;   /* uniform < dpm */
}
static int n, A, NRULE; static int32_t *nb, *xyz; static vec *a, *b;
static void step(int dpm) {
  for (int i = 0; i < NRULE; i++) {
    const int32_t *q = nb + 12 * i; vec c0 = {0, 0, 0, 0}, c1 = c0, c2 = c0, c3 = c0;
    for (int u = 0; u < 12; u++) { vec x = a[q[u]], t; t = c0 & x; c0 ^= x; x = t; t = c1 & x; c1 ^= x; x = t; t = c2 & x; c2 ^= x; c3 ^= t; }
    vec n45 = ~c3 & c2 & ~c1, n3 = ~c3 & ~c2 & c1 & c0;
    b[i] = n45 | (a[i] & n3);
  }
  for (int i = NRULE; i < n; i++) b[i] = coin(dpm);
  b[n] = (vec){0, 0, 0, 0};
  vec *t = a; a = b; b = t;
}
static inline int getbit(const vec *v, int lane) { return (int)(((*v)[lane >> 6] >> (lane & 63)) & 1); }
int main(int argc, char **argv) {
  FILE *f = fopen(argv[1], "rb"); int32_t hd[3]; if (!f || fread(hd, 4, 3, f) != 3) return 1; n = hd[0]; A = hd[1]; NRULE = hd[2];
  nb = malloc(4 * 12 * (size_t)NRULE); xyz = malloc(12 * (size_t)n);
  if (fread(nb, 4, 12 * (size_t)NRULE, f) != 12 * (size_t)NRULE || fread(xyz, 4, 3 * (size_t)n, f) != 3 * (size_t)n) return 1; fclose(f);
  a = aligned_alloc(32, 32 * (size_t)(n + 1)); b = aligned_alloc(32, 32 * (size_t)(n + 1)); memset(a, 0, 32 * (size_t)(n + 1)); memset(b, 0, 32 * (size_t)(n + 1));
  if (!strcmp(argv[2], "val")) {
    FILE *fi = fopen(argv[3], "rb"); long gens = atol(argv[4]); FILE *fo = fopen(argv[5], "wb"); seedrng(strtoull(argv[6], 0, 10)); int dpm = atoi(argv[7]);
    unsigned char *buf = malloc(n);
    for (int l = 0; l < 4; l++) { if (fread(buf, 1, n, fi) != (size_t)n) return 1; int lane = l * 85; for (int i = 0; i < n; i++) if (buf[i]) a[i][lane >> 6] |= 1ULL << (lane & 63); }
    for (long g = 0; g < gens; g++) { step(dpm); for (int l = 0; l < 4; l++) { int lane = l * 85; for (int i = 0; i < n; i++) buf[i] = getbit(&a[i], lane); fwrite(buf, 1, n, fo); } }
    fclose(fo); return 0;
  }
  seedrng(strtoull(argv[3], 0, 10)); long gens = atol(argv[4]); int burn = atoi(argv[5]); int dpm = atoi(argv[6]);
  int all8 = !strcmp(argv[2], "run8");   /* run8 (full hull only): a lane is retired at the first death of ANY of the 8 faces; tau_face = 8 * exposure / deaths */
  int R = 0; for (int i = 0; i < A; i++) { int q = xyz[3 * i] + xyz[3 * i + 1] + xyz[3 * i + 2]; if (q > R) R = q; }
  int *fl[8], fnum[8]; for (int f = 0; f < 8; f++) { fl[f] = malloc(4 * (size_t)n); fnum[f] = 0; int sx = f & 1 ? -1 : 1, sy = f & 2 ? -1 : 1, sz = f & 4 ? -1 : 1;
    for (int i = 0; i < n; i++) if (sx * xyz[3 * i] + sy * xyz[3 * i + 1] + sz * xyz[3 * i + 2] == R) fl[f][fnum[f]++] = i; }
  if (all8) for (int f = 0; f < 8; f++) if (fnum[f] != A) { fprintf(stderr, "run8 needs the full hull\n"); return 1; }
  int win = !strcmp(argv[2], "win");     /* win: also the histogram WHIST of the minimum of the face population over consecutive 24-generation
                                            blocks of counting lanes (the sampler's score: min over 24 generations after a generation with the face alive) */
  static int bc[NL], bmin[NL]; long *whist = calloc(A + 1, sizeof(long)); long nblk = 0; for (int l = 0; l < NL; l++) bmin[l] = 1 << 20;
  static int age[NL]; for (int i = 0; i < n; i++) a[i] = rvec();
  double expo = 0, deaths = 0, ps = 0, ps2 = 0, pn = 0; double *occ = calloc(A, 8); long burndeaths = 0; long *hist = calloc(A + 1, sizeof(long));
  for (long g = 1; g <= gens; g++) {
    step(dpm);
    vec alive = {0, 0, 0, 0}; for (int i = 0; i < A; i++) alive |= a[i];
    if (all8) for (int f = 1; f < 8; f++) { vec al = {0, 0, 0, 0}; for (int k = 0; k < A; k++) al |= a[fl[f][k]]; alive &= al; }
    vec cnt = {0, 0, 0, 0}; for (int l = 0; l < NL; l++) { age[l]++; if (age[l] > burn) cnt[l >> 6] |= 1ULL << (l & 63); }
    if (win) { static int wp[NL]; memset(wp, 0, sizeof wp);
      for (int i = 0; i < A; i++) for (int w = 0; w < 4; w++) { u64 x = a[i][w]; while (x) { wp[w * 64 + __builtin_ctzll(x)]++; x &= x - 1; } }
      for (int l = 0; l < NL; l++) if (age[l] > burn + 1) { if (wp[l] < bmin[l]) bmin[l] = wp[l]; bc[l]++;
          if (bc[l] == 24 || wp[l] == 0) { whist[bmin[l]]++; nblk++; bc[l] = 0; bmin[l] = 1 << 20; } } }
    for (int w = 0; w < 4; w++) { expo += __builtin_popcountll(alive[w] & cnt[w]); u64 d = ~alive[w];
      deaths += __builtin_popcountll(d & cnt[w]); burndeaths += __builtin_popcountll(d & ~cnt[w]);
      while (d) { int k = __builtin_ctzll(d); d &= d - 1; int lane = w * 64 + k; age[lane] = 0; u64 m = 1ULL << k;
        for (int i = 0; i < n; i++) a[i][w] = (a[i][w] & ~m) | (rnd() & m); } }
    if ((g & 3) == 0) {
      static int pop[NL]; memset(pop, 0, sizeof pop);
      for (int i = 0; i < A; i++) { for (int w = 0; w < 4; w++) { u64 x = a[i][w] & cnt[w]; occ[i] += __builtin_popcountll(x); while (x) { pop[w * 64 + __builtin_ctzll(x)]++; x &= x - 1; } } }
      for (int l = 0; l < NL; l++) if (age[l] > burn && age[l] > 0) { ps += pop[l]; ps2 += (double)pop[l] * pop[l]; pn += 1; hist[pop[l]]++; }
    }
  }
  double m = ps / pn, v = ps2 / pn - m * m;
  printf("RUN n %d A %d NRULE %d dpm %d burn %d gens %ld exposure %.0f deaths %.0f lntau %.4f +- %.4f burn_deaths %ld Pbar %.3f sigma %.3f samples %.0f\n",
         n, A, NRULE, dpm, burn, gens, expo, deaths, deaths > 0 ? log((all8 ? 8 : 1) * expo / deaths) : 99.0, deaths > 0 ? 1 / sqrt(deaths) : 0.0, burndeaths, m, sqrt(v), pn);
  for (int i = 0; i < A; i++) printf("OCC %d %d %d %.5f\n", xyz[3 * i], xyz[3 * i + 1], xyz[3 * i + 2], occ[i] / pn);
  if (win) { printf("WHIST %ld", nblk); for (int p = 0; p <= A; p++) printf(" %ld", whist[p]); printf("\n"); }
  printf("HIST"); for (int p = 0; p <= A; p++) printf(" %ld", hist[p]); printf("\n");
  return 0;
}
