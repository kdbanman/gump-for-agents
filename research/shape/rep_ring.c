/* rep_ring (research/shape): rep.c plus "-r L0 L1": keeps the last 64 states of layers L0, L1 (the two faces) and,
 * at the first generation where either is entirely dead in a replica, prints that face's history:
 *   D r f gen  s_{gen-63} ... s_gen     (s = one 0/1 character per cell of the layer, in the layer's cell order)
 * Stepping code identical to rep.c.  Original header:
 * rep: many independent replicas of gump (B45/S345) on one finite cell graph, bit-sliced:
 * replica r lives in bit (r % 64) of word (r / 64); W words per cell (64*W replicas).
 *
 * Input file (int32 little endian, written by geom.py):
 *   n, nbr[n*12] (-1 = dead forever), orbit[n] (-1 = never live initially; cells sharing an orbit id
 *   get the same random bit: symmetric soups), nL, then per layer: size, cell indices.
 * Usage: rep FILE W p seed cap K [-i cells.txt] [-t]
 *   p      soup density (each orbit live with probability p, independently per replica)
 *   cap    max generations;  K  resolution (gens) of layer last-alive times
 *   -i F   replica 0 starts from the cell indices listed in F (one per line), the rest are soups
 *   -t     print "T gen pop" of replica 0 every generation (validation)
 * Output: one line per replica:  r settle pop lc2 la_0 ... la_{nL-1}
 *   lc2    = last generation (resolution K, rounded up) at which the state differed from the state two
 *            generations earlier (for a replica ending in a still life or period 2: its settle time to K)
 *   settle = generation by which the replica was certainly periodic with period dividing 840
 *            (compared at multiples of 840), or -1 if not by cap; pop = final population;
 *   la_L   = last generation (resolution K, rounded up) at which layer L had a live cell, -1 never.
 * Runs until every replica settled or cap.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef uint64_t u64;
static uint64_t s[4];
static inline u64 rotl(const u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static u64 nxt(void) { const u64 r = rotl(s[1] * 5, 7) * 9, t = s[1] << 17;
  s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2]; s[0] ^= s[3]; s[2] ^= t; s[3] = rotl(s[3], 45); return r; }

#define FA(a, b, c, sum, car) { u64 _x = (a) ^ (b); sum = _x ^ (c); car = ((a) & (b)) | (_x & (c)); }

int main(int argc, char **argv) {
  if (argc < 7) { fprintf(stderr, "usage: rep FILE W p seed cap K [-i F] [-t]\n"); return 1; }
  int W = atoi(argv[2]); double p = atof(argv[3]); u64 seed = strtoull(argv[4], 0, 10);
  long cap = atol(argv[5]); int K = atoi(argv[6]); const char *initf = 0; int trace = 0; int RL[2] = {-1, -1};
  for (int i = 7; i < argc; i++) { if (!strcmp(argv[i], "-i")) initf = argv[++i]; else if (!strcmp(argv[i], "-t")) trace = 1; else if (!strcmp(argv[i], "-r")) { RL[0] = atoi(argv[++i]); RL[1] = atoi(argv[++i]); } }
  FILE *f = fopen(argv[1], "rb"); int n; if (!f || fread(&n, 4, 1, f) != 1) return 1;
  int32_t *nb = malloc(4 * 12 * (size_t)n), *orb = malloc(4 * (size_t)n);
  if (fread(nb, 4, 12 * (size_t)n, f) != 12 * (size_t)n || fread(orb, 4, n, f) != (size_t)n) return 1;
  for (size_t i = 0; i < 12 * (size_t)n; i++) if (nb[i] < 0) nb[i] = n;   /* row n = always zero */
  int nL; if (fread(&nL, 4, 1, f) != 1) return 1;
  int *lsz = malloc(4 * nL); int32_t **lc = malloc(sizeof(void *) * nL);
  for (int L = 0; L < nL; L++) { if (fread(&lsz[L], 4, 1, f) != 1) return 1; lc[L] = malloc(4 * (size_t)lsz[L]);
    if (fread(lc[L], 4, lsz[L], f) != (size_t)lsz[L]) return 1; }
  fclose(f);
  int R = 64 * W;
  u64 *a = calloc((size_t)(n + 1) * W, 8), *b = calloc((size_t)(n + 1) * W, 8), *snap = calloc((size_t)n * W, 8);
  u64 *acc = calloc((size_t)nL * W, 8), *settled = calloc(W, 8);
  u64 *pp = calloc((size_t)(n + 1) * W, 8), *accc = calloc(W, 8); long *lc2 = malloc(sizeof(long) * 64 * W);
  for (int r = 0; r < 64 * W; r++) lc2[r] = 0;
  long *la = malloc(sizeof(long) * (size_t)nL * R), *st = malloc(sizeof(long) * R);
  for (size_t i = 0; i < (size_t)nL * R; i++) la[i] = -1;
  for (int r = 0; r < R; r++) st[r] = -1;
  /* seed */
  s[0] = 0x9E3779B97F4A7C15ULL ^ seed; s[1] = 0xD1B54A32D192ED03ULL + seed * 7; s[2] = 0x8CB92BA72F3D8DD7ULL; s[3] = seed * 0x2545F4914F6CDD1DULL + 1;
  for (int i = 0; i < 20; i++) nxt();
  int maxo = -1; for (int i = 0; i < n; i++) if (orb[i] > maxo) maxo = orb[i];
  u64 *ob = calloc((size_t)(maxo + 1) * W, 8);
  u64 thr = (u64)(p * 18446744073709551616.0); if (p >= 1) thr = ~0ULL;
  for (int o = 0; o <= maxo; o++) for (int w = 0; w < W; w++) { u64 x = 0;
    for (int k = 0; k < 64; k++) if (nxt() < thr) x |= 1ULL << k; ob[(size_t)o * W + w] = x; }
  for (int i = 0; i < n; i++) if (orb[i] >= 0) memcpy(a + (size_t)i * W, ob + (size_t)orb[i] * W, 8 * W);
  if (initf) { for (int i = 0; i < n; i++) a[(size_t)i * W] &= ~1ULL;
    FILE *g = fopen(initf, "r"); int c; while (fscanf(g, "%d", &c) == 1) a[(size_t)c * W] |= 1ULL; fclose(g); }
  memcpy(snap, a, 8 * (size_t)n * W);
  long gen = 0;
  enum { H = 64 };
  u64 *ring[2] = {0, 0}, *alivep = 0, *recd = 0;
  if (RL[0] >= 0) { for (int f = 0; f < 2; f++) ring[f] = calloc((size_t)H * lsz[RL[f]] * W, 8);
    alivep = calloc(2 * (size_t)W, 8); recd = calloc(W, 8); }
  for (; gen < cap;) {
    /* layer accumulation for the current state */
    for (int L = 0; L < nL; L++) for (int k = 0; k < lsz[L]; k++) { const u64 *x = a + (size_t)lc[L][k] * W;
      for (int w = 0; w < W; w++) acc[(size_t)L * W + w] |= x[w]; }
    if (gen % K == 0) {
      for (int L = 0; L < nL; L++) for (int w = 0; w < W; w++) { u64 x = acc[(size_t)L * W + w];
        while (x) { int k = __builtin_ctzll(x); x &= x - 1; la[(size_t)L * R + 64 * w + k] = gen; } acc[(size_t)L * W + w] = 0; }
      for (int w = 0; w < W; w++) { u64 x = accc[w]; while (x) { int k = __builtin_ctzll(x); x &= x - 1; lc2[64 * w + k] = gen; } accc[w] = 0; }
    }
    if (RL[0] >= 0) {
      int slot = gen % H;
      for (int f = 0; f < 2; f++) { int L = RL[f];
        for (int c = 0; c < lsz[L]; c++) memcpy(ring[f] + ((size_t)slot * lsz[L] + c) * W, a + (size_t)lc[L][c] * W, 8 * W);
        for (int w = 0; w < W; w++) { u64 al = 0; for (int c = 0; c < lsz[L]; c++) al |= a[(size_t)lc[L][c] * W + w];
          u64 died = (gen > 0 ? alivep[f * W + w] : 0) & ~al & ~recd[w];
          while (died) { int k = __builtin_ctzll(died); died &= died - 1; recd[w] |= 1ULL << k;
            printf("D %d %d %ld", 64 * w + k, f, gen);
            for (long g = gen - H + 1; g <= gen; g++) { if (g < 0) continue; int sl = g % H; putchar(' ');
              for (int c = 0; c < lsz[L]; c++) putchar('0' + (int)((ring[f][((size_t)sl * lsz[L] + c) * W + w] >> k) & 1)); }
            putchar('\n'); }
          alivep[f * W + w] = al; } }
    }
    if (trace) { long pop = 0; for (int i = 0; i < n; i++) pop += a[(size_t)i * W] & 1; printf("T %ld %ld\n", gen, pop); }
    /* step */
    for (int i = 0; i < n; i++) {
      const int32_t *q = nb + 12 * (size_t)i; u64 *o = b + (size_t)i * W; const u64 *me = a + (size_t)i * W;
      const u64 *x0 = a + (size_t)q[0] * W, *x1 = a + (size_t)q[1] * W, *x2 = a + (size_t)q[2] * W, *x3 = a + (size_t)q[3] * W,
                *x4 = a + (size_t)q[4] * W, *x5 = a + (size_t)q[5] * W, *x6 = a + (size_t)q[6] * W, *x7 = a + (size_t)q[7] * W,
                *x8 = a + (size_t)q[8] * W, *x9 = a + (size_t)q[9] * W, *x10 = a + (size_t)q[10] * W, *x11 = a + (size_t)q[11] * W;
      for (int w = 0; w < W; w++) {
        u64 s0, c0, s1, c1, s2, c2, s3, c3, o1, t4, b0, t5, u0, f0, u1, f1, b1, f2, b2, b3;
        FA(x0[w], x1[w], x2[w], s0, c0); FA(x3[w], x4[w], x5[w], s1, c1);
        FA(x6[w], x7[w], x8[w], s2, c2); FA(x9[w], x10[w], x11[w], s3, c3);
        FA(s0, s1, s2, o1, t4); b0 = o1 ^ s3; t5 = o1 & s3;
        FA(c0, c1, c2, u0, f0); FA(c3, t4, t5, u1, f1); b1 = u0 ^ u1; f2 = u0 & u1;
        FA(f0, f1, f2, b2, b3);
        o[w] = ~b3 & ((b2 & ~b1) | (me[w] & ~b2 & b1 & b0));
      }
    }
    /* compare gen+1 (b) with gen-1 (pp), then rotate: pp <- gen, a <- gen+1 */
    if (gen >= 1) for (int i = 0; i < n; i++) for (int w = 0; w < W; w++) accc[w] |= b[(size_t)i * W + w] ^ pp[(size_t)i * W + w];
    { u64 *t = pp; pp = a; a = b; b = t; } gen++;
    if (gen % 840 == 0) {
      int all = 1;
      for (int w = 0; w < W; w++) { u64 eq = ~0ULL;
        for (int i = 0; i < n; i++) eq &= ~(a[(size_t)i * W + w] ^ snap[(size_t)i * W + w]);
        u64 nw = eq & ~settled[w]; while (nw) { int k = __builtin_ctzll(nw); nw &= nw - 1; st[64 * w + k] = gen - 840; }
        settled[w] |= eq; if (settled[w] != ~0ULL) all = 0; }
      memcpy(snap, a, 8 * (size_t)n * W);
      if (all) break;
    }
  }
  /* final flush of layer accumulators (state at gen) */
  for (int L = 0; L < nL; L++) for (int k = 0; k < lsz[L]; k++) { const u64 *x = a + (size_t)lc[L][k] * W;
    for (int w = 0; w < W; w++) acc[(size_t)L * W + w] |= x[w]; }
  for (int L = 0; L < nL; L++) for (int w = 0; w < W; w++) { u64 x = acc[(size_t)L * W + w];
    while (x) { int k = __builtin_ctzll(x); x &= x - 1; la[(size_t)L * R + 64 * w + k] = gen; } }
  for (int r = 0; r < R; r++) {
    long pop = 0; for (int i = 0; i < n; i++) pop += (a[(size_t)i * W + r / 64] >> (r % 64)) & 1;
    printf("%d %ld %ld %ld", r, st[r], pop, lc2[r]);
    for (int L = 0; L < nL; L++) printf(" %ld", la[(size_t)L * R + r]);
    printf("\n");
  }
  fprintf(stderr, "gens %ld\n", gen);
  return 0;
}
