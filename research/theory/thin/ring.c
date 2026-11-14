/* ring.c -- gump on the thin torus (1,1),(0,b), packed along the ring.
 *
 * A layer is a ring of b <= 64 sites with three cells each (thin.py); one 64-bit word holds one orientation of
 * one layer (bit c = site c), and a vector of NL words holds NL independent rings ("lanes").
 *
 *   det    m {111} layers, B45/S345 on all of them, two faces (layers 0 and m-1)
 *   model  w layers of the rule (layer 0 is the face) over two layers of coins: every cell of layers w and
 *          w+1 is redrawn alive with probability rho16/65536 before every generation
 *
 * Each lane lives successive lives: a life starts from a soup of density p0 and ends when a face is empty
 * (checked every generation), when its dynamic state repeats (snapshot comparison every PER generations),
 * when an interior layer of a det slab is found empty at a snapshot, or at the cap. Then the lane is reseeded.
 * Hazards are for ages >= T0 (age = generations since the soup).
 *
 * usage: ring det|model b m_or_w rho16 p0_16 seed GENS T0 CAP GS OUT [-i init.txt] [-d dump.txt]
 *   GS  sample the face statistics every GS generations (0 = none)
 *   -i  lane 0 starts from the listed cells (index (t*3+o)*b+c)       -d  dump every lane every generation
 * Output OUT (text, key value...): totals, age-binned exposure/deaths, face-population histogram, deaths by
 * the face population one generation before, histogram of maximal empty runs of sites, pre-death populations.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include "nbr.h"
#ifndef NL
#define NL 8
#endif
#define MAXT 12
#define PER 840
#define LAG 32
typedef uint64_t u64;
typedef u64 vec __attribute__((vector_size(8 * NL)));

static int b, nt, ndyn, model;      /* nt = layers stored (m, or w + 2), ndyn = dynamic layers */
static u64 MASK;
static vec S[MAXT][3], Tn[MAXT][3], SNAP[MAXT][3];
static vec rs[4];                    /* xoshiro256++ state, one stream per lane */

static inline vec rotlv(vec x, int k) { return (x << k) | (x >> (64 - k)); }
static inline vec rnd(void) {
  vec r = rotlv(rs[0] + rs[3], 23) + rs[0], t = rs[1] << 17;
  rs[2] ^= rs[0]; rs[3] ^= rs[1]; rs[1] ^= rs[2]; rs[0] ^= rs[3]; rs[2] ^= t; rs[3] = rotlv(rs[3], 45);
  return r;
}
static u64 smx;
static u64 splitmix(void) { u64 z = (smx += 0x9e3779b97f4a7c15ULL); z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
  z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; return z ^ (z >> 31); }
/* word of independent bits, each 1 with probability q16 / 65536 */
static inline vec bern(unsigned q16) {
  vec r = {0};
  if (!q16) return r;
  int i = 0; while (!((q16 >> i) & 1)) i++;
  for (; i < 16; i++) { vec w = rnd(); if ((q16 >> i) & 1) r |= w; else r &= w; }
  return r;
}
/* value at site c of the result = value of x at site c + dc (ring of b sites) */
static inline vec shift(vec x, int dc) {
  if (dc == 0) return x;
  int k = dc > 0 ? dc : b + dc;                 /* rotate right by k within b bits */
  vec m = {0}; m += MASK;
  return ((x >> k) | (x << (b - k))) & m;
}
#define FA(a, bb, c, s, cy) { vec _x = (a) ^ (bb); s = _x ^ (c); cy = ((a) & (bb)) | ((c) & _x); }

static void step(void) {
  static vec R[MAXT][3][5];                     /* R[t][o][dc + 2] */
  vec zero = {0};
  for (int t = 0; t < nt; t++) for (int o = 0; o < 3; o++) for (int d = -2; d <= 2; d++) R[t][o][d + 2] = shift(S[t][o], d);
  for (int t = 0; t < ndyn; t++) for (int o = 0; o < 3; o++) {
    vec a[12];
    for (int k = 0; k < 12; k++) { int t2 = t + NBR[o][k][0];
      a[k] = (t2 < 0 || t2 >= nt) ? zero : R[t2][NBR[o][k][1]][NBR[o][k][2] + 2]; }
    vec s1, c1, s2, c2, s3, c3, s4, c4, s5, c5, t1, d1, t2, d2;
    FA(a[0], a[1], a[2], s1, c1); FA(a[3], a[4], a[5], s2, c2); FA(a[6], a[7], a[8], s3, c3); FA(a[9], a[10], a[11], s4, c4);
    FA(s1, s2, s3, s5, c5); vec b0 = s5 ^ s4, c6 = s5 & s4;
    FA(c1, c2, c3, t1, d1); FA(c4, c5, c6, t2, d2); vec b1 = t1 ^ t2, d3 = t1 & t2;
    vec b2 = d1 ^ d2 ^ d3, b3 = (d1 & d2) | (d3 & (d1 ^ d2));
    Tn[t][o] = ~b3 & ((b2 & ~b1) | (S[t][o] & ~b2 & b1 & b0));   /* n in {4,5}, or alive and n = 3 */
  }
  for (int t = 0; t < ndyn; t++) for (int o = 0; o < 3; o++) S[t][o] = Tn[t][o];
}

static unsigned rho16, p016;
static void noise(void) {
  vec m = {0}; m += MASK;
  for (int t = ndyn; t < nt; t++) for (int o = 0; o < 3; o++) S[t][o] = bern(rho16) & m;
}
static void reseed(int l) {
  for (int t = 0; t < ndyn; t++) for (int o = 0; o < 3; o++) { vec r = bern(p016); S[t][o][l] = r[l] & MASK; }
  for (int t = 0; t < ndyn; t++) for (int o = 0; o < 3; o++) SNAP[t][o][l] = ~0ULL;   /* never equal */
}
static inline int facepop(int t, int l) {
  return __builtin_popcountll(S[t][0][l]) + __builtin_popcountll(S[t][1][l]) + __builtin_popcountll(S[t][2][l]);
}
static void dump(FILE *f, long g, char tag) {
  for (int l = 0; l < NL; l++) { fprintf(f, "%ld %d %c", g, l, tag);
    for (int t = 0; t < nt; t++) for (int o = 0; o < 3; o++) fprintf(f, " %llx", (unsigned long long)S[t][o][l]);
    fprintf(f, "\n"); }
}

#define NB 48
static double expo[NB]; static long deaths[NB];
static inline int bin(long a) { return 63 - __builtin_clzll((u64)a + 1); }
static void add_expo(long L) { for (int k = 0; k < NB; k++) { long lo = (1L << k) - 1, hi = (1L << (k + 1)) - 1;
  if (L <= lo) break; expo[k] += (double)((L < hi ? L : hi) - lo); } }

int main(int argc, char **argv) {
  if (argc < 12) { fprintf(stderr, "usage: ring det|model b m_or_w rho16 p0_16 seed GENS T0 CAP GS OUT [-i f] [-d f]\n"); return 1; }
  model = !strcmp(argv[1], "model"); b = atoi(argv[2]); int mw = atoi(argv[3]);
  rho16 = atoi(argv[4]); p016 = atoi(argv[5]); u64 seed = strtoull(argv[6], 0, 10);
  long GENS = atol(argv[7]), T0 = atol(argv[8]), CAP = atol(argv[9]); int GS = atoi(argv[10]); const char *outf = argv[11];
  const char *initf = 0, *dumpf = 0;
  for (int i = 12; i < argc; i++) { if (!strcmp(argv[i], "-i")) initf = argv[++i]; else if (!strcmp(argv[i], "-d")) dumpf = argv[++i]; }
  if (b < 5 || b > 64) { fprintf(stderr, "need 5 <= b <= 64\n"); return 1; }
  ndyn = mw; nt = model ? mw + 2 : mw; if (nt > MAXT) { fprintf(stderr, "too many layers\n"); return 1; }
  MASK = b == 64 ? ~0ULL : ((1ULL << b) - 1);
  int nface = model ? 1 : 2, ft[2] = {0, ndyn - 1};
  smx = seed * 0x2545F4914F6CDD1DULL + 0x1234567ULL;
  for (int i = 0; i < 4; i++) for (int l = 0; l < NL; l++) rs[i][l] = splitmix();
  for (int i = 0; i < 16; i++) rnd();
  long born[NL]; for (int l = 0; l < NL; l++) { reseed(l); born[l] = 0; }
  if (initf) { for (int t = 0; t < ndyn; t++) for (int o = 0; o < 3; o++) S[t][o][0] = 0;
    FILE *f = fopen(initf, "r"); int c; while (fscanf(f, "%d", &c) == 1) S[c / (3 * b)][(c / b) % 3][0] |= 1ULL << (c % b); fclose(f); }
  FILE *df = dumpf ? fopen(dumpf, "w") : 0;
  /* statistics */
  double E0 = 0; long F0 = 0, nF = 0, nS = 0, nI = 0, nC = 0, nBoth = 0;
  static long hpop[200], dpop[200], hrun[66], hmax[66]; long nsamp = 0;
  static double pre[LAG + 1]; static long npre = 0;
  static unsigned char rb[NL][2][LAG];           /* face populations of the last LAG generations */
  static long dlag[LAG + 1][200];                /* dlag[k][n]: deaths with face population n, k generations before */
  for (long g = 0; g < GENS; g++) {
    if (model) noise();
    if (df) dump(df, g, 'S');
    step();
    long g1 = g + 1;
    vec f[2]; for (int k = 0; k < nface; k++) f[k] = S[ft[k]][0] | S[ft[k]][1] | S[ft[k]][2];
    int chk = (g1 % PER == 0), smp = GS && (g1 % GS == 0);
    for (int l = 0; l < NL; l++) {
      long age = g1 - born[l]; int end = 0;
      int dead0 = f[0][l] == 0, dead1 = nface == 2 && f[1][l] == 0;
      if (dead0 || dead1) {
        end = 1; int nd = dead0 + dead1; nF += nd; nBoth += nd == 2;
        deaths[bin(age - 1)] += nd; if (age - 1 >= T0) F0 += nd;
        if (age > LAG + T0) for (int k = 0; k < nface; k++) if (k ? dead1 : dead0) {
          npre++; for (int j = 1; j <= LAG; j++) { int n = rb[l][k][(g1 - j) % LAG]; pre[j] += n; dlag[j][n]++; } }
        if (age - 1 >= T0) for (int k = 0; k < nface; k++) if (k ? dead1 : dead0) dpop[rb[l][k][(g1 - 1) % LAG]]++;
      } else {
        for (int k = 0; k < nface; k++) rb[l][k][g1 % LAG] = (unsigned char)facepop(ft[k], l);
        if (chk) {
          int eq = 1; for (int t = 0; t < ndyn && eq; t++) for (int o = 0; o < 3; o++) if (S[t][o][l] != SNAP[t][o][l]) { eq = 0; break; }
          for (int t = 0; t < ndyn; t++) for (int o = 0; o < 3; o++) SNAP[t][o][l] = S[t][o][l];
          if (eq) { end = 2; nS++; }
          else if (!model) { for (int t = 1; t < ndyn - 1; t++) if (!(S[t][0][l] | S[t][1][l] | S[t][2][l])) { end = 3; } if (end == 3) nI++; }
        }
        if (!end && CAP && age >= CAP) { end = 4; nC++; }
        if (!end && smp && age >= T0) for (int k = 0; k < nface; k++) {
          int t = ft[k]; hpop[rb[l][k][g1 % LAG]]++; nsamp++;
          /* site s = {Z_s, Y_s, X_{s+1}} (contiguous along the axis); empty runs of sites */
          u64 X = S[t][0][l], occ = S[t][2][l] | S[t][1][l] | (((X >> 1) | (X << (b - 1))) & MASK);
          u64 D = ~occ & MASK; int mx = 0;
          if (D) { int s = __builtin_ctzll(occ); if (s) D = ((D >> s) | (D << (b - s))) & MASK;
            while (D) { int tz = __builtin_ctzll(D); D >>= tz; int len = __builtin_ctzll(~D); hrun[len]++; if (len > mx) mx = len;
              D = len < 64 ? D >> len : 0; } }
          hmax[mx]++;
        }
      }
      if (end) {
        long L = end == 2 ? age - PER : age;       /* a repeating state was already repeating one period ago */
        if (L < 0) L = 0;
        add_expo(L); if (L > T0) E0 += (double)(L - T0);
        if (df) { }
        reseed(l); born[l] = g1;
      }
    }
    if (df) { /* the state after reseeding is dumped at the top of the next iteration */ }
  }
  for (int l = 0; l < NL; l++) { long L = GENS - born[l]; add_expo(L); if (L > T0) E0 += (double)(L - T0); }
  if (df) { dump(df, GENS, 'S'); fclose(df); }
  FILE *o = fopen(outf, "w");
  fprintf(o, "mode %s b %d layers %d rho16 %u p016 %u seed %llu gens %ld T0 %ld cap %ld gs %d lanes %d\n", argv[1], b, mw, rho16, p016,
          (unsigned long long)seed, GENS, T0, CAP, GS, NL);
  fprintf(o, "tot expo %.0f deaths %ld alldeaths %ld both %ld settled %ld interior %ld capped %ld nsamp %ld npre %ld\n", E0, F0, nF, nBoth, nS, nI, nC, nsamp, npre);
  fprintf(o, "expo"); for (int k = 0; k < NB; k++) fprintf(o, " %.0f", expo[k]); fprintf(o, "\n");
  fprintf(o, "deaths"); for (int k = 0; k < NB; k++) fprintf(o, " %ld", deaths[k]); fprintf(o, "\n");
  fprintf(o, "hpop"); for (int k = 0; k <= 3 * b; k++) fprintf(o, " %ld", hpop[k]); fprintf(o, "\n");
  fprintf(o, "dpop"); for (int k = 0; k <= 3 * b; k++) fprintf(o, " %ld", dpop[k]); fprintf(o, "\n");
  fprintf(o, "hrun"); for (int k = 0; k <= b; k++) fprintf(o, " %ld", hrun[k]); fprintf(o, "\n");
  fprintf(o, "hmax"); for (int k = 0; k <= b; k++) fprintf(o, " %ld", hmax[k]); fprintf(o, "\n");
  fprintf(o, "pre"); for (int k = 1; k <= LAG; k++) fprintf(o, " %.0f", pre[k]); fprintf(o, "\n");
  for (int j = 1; j <= 4; j++) { fprintf(o, "dlag%d", j); for (int k = 0; k <= 3 * b; k++) fprintf(o, " %ld", dlag[j][k]); fprintf(o, "\n"); }
  fclose(o);
  return 0;
}
