/* st: stepper for the review of research/shape3 (written from docs/AUTOMATON.md; shares no code with ts.c / ts3.c).
 * Bit-sliced: WW words of 64 lanes = 64*WW independent replicas, each running successive lives (renewal) on the
 * slab described by the geometry file of geom.py.  Events are resolved EVERY generation:
 *   F  a face layer entirely dead        W  three cyclically consecutive transverse layers dead (diagonals with >= 3
 *   X  both at the same generation          layers)
 *   S  settled: the whole lane state equals a snapshot taken earlier in the same life (Brent's scheme: snapshot at
 *      ages 0, 1, 2, 4, 8, ...), so the life is exactly periodic from the snapshot on; no limit on the period.
 *      Logged as "S censor_age period detect_age"; censor_age = snapshot age (a time inside the cycle).
 *   C  age reached the cap (-c; default none)    E  still running at the end (censored)
 * Neighbour count: a tree of half adders (12 x 1 bit -> 6 x 2 bit -> 3 x 3 bit -> 4 bit); rule B45/S345.
 * RNG: xoshiro256** seeded by splitmix64(seed).
 *
 *   st GEOM SEED GENS EVOUT [-c CAP] [-z ZFILE]       renewal run, p = 0.4
 *   st GEOM SEED GENS EVOUT -i INIT -t G1,G2,...      lane 0 starts from the listed cells (no renewal, no events);
 *                                                     prints "T g cell cell ..." for lane 0 at the listed generations
 * ZFILE: for every settled life whose period does not divide 840, a line "Z period censor_age detect_age cells..."
 * (the lane state at detection; at most 50 lines).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#ifndef WW
#define WW 8
#endif
typedef uint64_t u64;

static u64 S4[4];
static inline u64 rotl(u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static u64 nxt(void) { u64 r = rotl(S4[1] * 5, 7) * 9, t = S4[1] << 17; S4[2] ^= S4[0]; S4[3] ^= S4[1];
  S4[1] ^= S4[2]; S4[0] ^= S4[3]; S4[2] ^= t; S4[3] = rotl(S4[3], 45); return r; }
static void seedrng(u64 s) { for (int i = 0; i < 4; i++) { u64 z = (s += 0x9e3779b97f4a7c15ULL);
  z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL; z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; S4[i] = z ^ (z >> 31); } }

static int32_t *buf; static size_t bp;
static int gi(void) { return buf[bp++]; }

static int n, *nb, nf0, *f0, nf1, *f1, nd, dL[3], *dlay[3];
static int *lcells[3], lstart[3][64];

static void step(const u64 *restrict a, u64 *restrict o) {
  for (int i = 0; i < n; i++) {
    const int *q = nb + 12 * i;
    const u64 *p[12]; for (int t = 0; t < 12; t++) p[t] = a + (size_t)q[t] * WW;
    const u64 *me = a + (size_t)i * WW; u64 *out = o + (size_t)i * WW;
    for (int w = 0; w < WW; w++) {
      u64 x[12]; for (int t = 0; t < 12; t++) x[t] = p[t][w];
      u64 l[6], h[6];
      for (int j = 0; j < 6; j++) { l[j] = x[2 * j] ^ x[2 * j + 1]; h[j] = x[2 * j] & x[2 * j + 1]; }
      u64 r0[3], r1[3], r2[3];
      for (int j = 0; j < 3; j++) { u64 A0 = l[2 * j], A1 = h[2 * j], B0 = l[2 * j + 1], B1 = h[2 * j + 1];
        u64 k0 = A0 & B0; r0[j] = A0 ^ B0; u64 hx = A1 ^ B1; r1[j] = hx ^ k0; r2[j] = (A1 & B1) | (k0 & hx); }
      /* u = r[0] + r[1]  (4 bits) */
      u64 k = r0[0] & r0[1]; u64 u0 = r0[0] ^ r0[1];
      u64 t1 = r1[0] ^ r1[1]; u64 u1 = t1 ^ k; k = (r1[0] & r1[1]) | (k & t1);
      u64 t2 = r2[0] ^ r2[1]; u64 u2 = t2 ^ k; u64 u3 = (r2[0] & r2[1]) | (k & t2);
      /* v = u + r[2] */
      k = u0 & r0[2]; u64 v0 = u0 ^ r0[2];
      t1 = u1 ^ r1[2]; u64 v1 = t1 ^ k; k = (u1 & r1[2]) | (k & t1);
      t2 = u2 ^ r2[2]; u64 v2 = t2 ^ k; k = (u2 & r2[2]) | (k & t2);
      u64 v3 = u3 ^ k;   /* sum <= 12 < 16: no carry out of bit 3 */
      u64 four_five = ~v3 & v2 & ~v1;                 /* 4 = 0100, 5 = 0101 */
      u64 three = ~v3 & ~v2 & v1 & v0;                /* 3 = 0011 */
      out[w] = four_five | (me[w] & three);
    }
  }
}

int main(int argc, char **argv) {
  if (argc < 5) { fprintf(stderr, "usage: st GEOM SEED GENS EVOUT [opts]\n"); return 1; }
  long seed = atol(argv[2]); long gens = atol(argv[3]); const char *evf = argv[4];
  long cap = -1; const char *zf = 0, *initf = 0, *tlist = 0;
  for (int i = 5; i < argc; i++) {
    if (!strcmp(argv[i], "-c")) cap = atol(argv[++i]); else if (!strcmp(argv[i], "-z")) zf = argv[++i];
    else if (!strcmp(argv[i], "-i")) initf = argv[++i]; else if (!strcmp(argv[i], "-t")) tlist = argv[++i];
  }
  FILE *g = fopen(argv[1], "rb"); fseek(g, 0, SEEK_END); long sz = ftell(g); fseek(g, 0, SEEK_SET);
  buf = malloc(sz); if (fread(buf, 1, sz, g) != (size_t)sz) return 2; fclose(g);
  n = gi(); nb = malloc(sizeof(int) * 12 * n); for (int i = 0; i < 12 * n; i++) nb[i] = gi();
  nf0 = gi(); f0 = malloc(4 * nf0); for (int i = 0; i < nf0; i++) f0[i] = gi();
  nf1 = gi(); f1 = malloc(4 * nf1); for (int i = 0; i < nf1; i++) f1[i] = gi();
  nd = gi();
  for (int d = 0; d < nd; d++) { dL[d] = gi(); dlay[d] = malloc(4 * n); for (int i = 0; i < n; i++) dlay[d][i] = gi();
    /* cells grouped by layer */
    lcells[d] = malloc(4 * n); int c = 0;
    for (int l = 0; l < dL[d]; l++) { lstart[d][l] = c; for (int i = 0; i < n; i++) if (dlay[d][i] == l) lcells[d][c++] = i; }
    lstart[d][dL[d]] = c; }
  seedrng((u64)seed * 0x9E3779B97F4A7C15ULL + 0x1234567ULL);
  const int R = 64 * WW; const u64 thr = (u64)(0.4 * 18446744073709551616.0);
  u64 *a = aligned_alloc(64, 8 * (size_t)(n + 1) * WW), *b = aligned_alloc(64, 8 * (size_t)(n + 1) * WW);
  u64 *snap = aligned_alloc(64, 8 * (size_t)n * WW);
  memset(a, 0, 8 * (size_t)(n + 1) * WW); memset(b, 0, 8 * (size_t)(n + 1) * WW);   /* cell n: always dead */
  for (int i = 0; i < n; i++) for (int w = 0; w < WW; w++) { u64 x = 0; for (int k = 0; k < 64; k++) x |= (u64)(nxt() < thr) << k; a[(size_t)i * WW + w] = x; }
  long *born = calloc(R, sizeof(long)), *sa = calloc(R, sizeof(long)), *nsave = malloc(R * sizeof(long));
  for (int r = 0; r < R; r++) nsave[r] = 1;
  if (initf) { FILE *h = fopen(initf, "r"); for (int i = 0; i < n; i++) a[(size_t)i * WW] &= ~1ULL; int c;
    while (fscanf(h, "%d", &c) == 1) a[(size_t)c * WW] |= 1ULL; fclose(h); }
  memcpy(snap, a, 8 * (size_t)n * WW);
  long tall = tlist && !strcmp(tlist, "all"), *tg = malloc(8 * 4096); int nt = 0;
  if (tlist && !tall) { char *s = strdup(tlist), *tok = strtok(s, ","); while (tok && nt < 4096) { tg[nt++] = atol(tok); tok = strtok(0, ","); } }
  FILE *ev = fopen(evf, "w"); FILE *zo = zf ? fopen(zf, "w") : 0; int nz = 0;
  long cnt[6] = {0}; double E = 0;
  for (long gen = 0; gen < gens; gen++) {
    if (initf) { int hit = tall; for (int t = 0; t < nt; t++) hit |= tg[t] == gen;
      if (hit) { printf("T %ld", gen); for (int i = 0; i < n; i++) if (a[(size_t)i * WW] & 1) printf(" %d", i); printf("\n"); } }
    step(a, b); { u64 *t = a; a = b; b = t; }
    long g1 = gen + 1;
    if (initf) continue;
    for (int w = 0; w < WW; w++) {
      u64 o0 = 0, o1 = 0; for (int i = 0; i < nf0; i++) o0 |= a[(size_t)f0[i] * WW + w];
      for (int i = 0; i < nf1; i++) o1 |= a[(size_t)f1[i] * WW + w];
      u64 eF = ~o0 | ~o1, eW = 0;
      for (int d = 0; d < nd; d++) { int L = dL[d]; if (L < 3) continue; u64 dead[64];
        for (int l = 0; l < L; l++) { u64 x = 0; for (int c = lstart[d][l]; c < lstart[d][l + 1]; c++) x |= a[(size_t)lcells[d][c] * WW + w]; dead[l] = ~x; }
        for (int l = 0; l < L; l++) eW |= dead[l] & dead[(l + 1) % L] & dead[(l + 2) % L]; }
      u64 df = 0; for (int i = 0; i < n; i++) df |= a[(size_t)i * WW + w] ^ snap[(size_t)i * WW + w];
      u64 eS = ~df;
      u64 any = eF | eW | eS, save = 0, reseed = 0;
      for (int k = 0; k < 64; k++) {
        int r = 64 * w + k; long age = g1 - born[r]; u64 bit = 1ULL << k;
        if (any & bit) {
          if ((eF & bit) && (eW & bit)) { cnt[2]++; fprintf(ev, "X %ld\n", age); E += age; }
          else if (eF & bit) { cnt[0]++; fprintf(ev, "F %ld\n", age); E += age; }
          else if (eW & bit) { cnt[1]++; fprintf(ev, "W %ld\n", age); E += age; }
          else { long p = age - sa[r]; cnt[3]++; fprintf(ev, "S %ld %ld %ld\n", sa[r], p, age); E += sa[r];
            if (zo && 840 % p != 0 && nz < 50) { nz++; fprintf(zo, "Z %ld %ld %ld", p, sa[r], age);
              for (int i = 0; i < n; i++) if ((a[(size_t)i * WW + w] >> k) & 1) fprintf(zo, " %d", i); fprintf(zo, "\n"); fflush(zo); } }
          reseed |= bit;
        } else if (cap > 0 && age >= cap) { cnt[4]++; fprintf(ev, "C %ld\n", age); E += age; reseed |= bit; }
        else if (age == nsave[r]) { save |= bit; sa[r] = age; nsave[r] *= 2; }
      }
      if (reseed) {
        for (int i = 0; i < n; i++) { u64 x = a[(size_t)i * WW + w] & ~reseed, rb = 0;
          for (int k = 0; k < 64; k++) if ((reseed >> k) & 1) rb |= (u64)(nxt() < thr) << k;
          a[(size_t)i * WW + w] = x | rb; }
        for (int k = 0; k < 64; k++) if ((reseed >> k) & 1) { int r = 64 * w + k; born[r] = g1; sa[r] = 0; nsave[r] = 1; }
        save |= reseed;
      }
      if (save) for (int i = 0; i < n; i++) { size_t j = (size_t)i * WW + w; snap[j] = (snap[j] & ~save) | (a[j] & save); }
    }
  }
  if (!initf) for (int r = 0; r < R; r++) { long age = gens - born[r]; fprintf(ev, "E %ld\n", age); E += age; cnt[5]++; }
  fclose(ev); if (zo) fclose(zo);
  printf("SUMMARY gens %ld R %d exposure %.6e F %ld W %ld X %ld S %ld C %ld E %ld\n", gens, R, E, cnt[0], cnt[1], cnt[2], cnt[3], cnt[4], cnt[5]);
  return 0;
}
