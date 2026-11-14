/* parity.c -- exam S-E1: the 2D rule's edge row over a parity bulk (source's S-E1), bit-sliced, 64*W replicas.
 *
 * Cells (x, j), x in Z_L, 0 <= j <= H.  Row 0: B34/S234 on the cross (in-row x+-1, x+-2; (x,1), (x,2) beneath;
 * nothing above).  Rows 1..H: alive next iff the number of live cross neighbours is odd (in-row x+-1, x+-2;
 * rows j+-1, j+-2 at column x; row 0 counts; rows < 0 and > H are dead).  Start: every cell Bernoulli(1/2).
 * A replica dies when row 0 is empty; every replica is censored at generation T = H/2.
 *
 *   parity run   L H nbatch seed T0      -> totals: exposure deaths, hazard by age bins, one-cell statistics
 *   parity trace L H gens seed           -> replica 0's full grid at generations 0..gens (no light-cone pruning)
 *
 * Light cone (run mode): row 0 at generation T depends on row r at generation t only if r <= 2(T - t), so at
 * generation t only rows 0..min(H, 2(T - t)) are updated; the others are never read again.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifndef W
#define W 4
#endif
typedef uint64_t u64;
static u64 s[4];
static inline u64 rotl(u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static inline u64 rnd(void) { u64 r = rotl(s[1] * 5, 7) * 9, t = s[1] << 17; s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2];
  s[0] ^= s[3]; s[2] ^= t; s[3] = rotl(s[3], 45); return r; }
static void seedrng(u64 x) { for (int i = 0; i < 4; i++) { x += 0x9E3779B97F4A7C15ULL; u64 z = x;
  z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL; z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL; s[i] = z ^ (z >> 31); } }

static int L, H;
static u64 *A, *B;   /* [(j * L + x) * W + w] */
#define AT(a, j, x) ((a) + ((size_t)(j) * L + (size_t)(((x) % L + L) % L)) * W)

static void step(int rows) {  /* B <- f(A) for rows 0..rows-1 (rows <= H+1); then swap */
  for (int j = 0; j < rows; j++) for (int x = 0; x < L; x++) {
    u64 *o = AT(B, j, x);
    const u64 *c = AT(A, j, x), *l1 = AT(A, j, x - 1), *r1 = AT(A, j, x + 1), *l2 = AT(A, j, x - 2), *r2 = AT(A, j, x + 2);
    if (j == 0) {
      const u64 *d1 = AT(A, 1, x), *d2 = AT(A, 2, x);
      for (int w = 0; w < W; w++) {
        u64 in[6] = {l1[w], r1[w], l2[w], r2[w], H >= 1 ? d1[w] : 0, H >= 2 ? d2[w] : 0};
        u64 b0 = 0, b1 = 0, b2 = 0;  /* 3-bit counter */
        for (int k = 0; k < 6; k++) { u64 a = in[k], c0 = b0 & a; b0 ^= a; u64 c1 = b1 & c0; b1 ^= c0; b2 |= c1; }
        u64 n2 = ~b2 & b1 & ~b0, n3 = ~b2 & b1 & b0, n4 = b2 & ~b1 & ~b0;
        o[w] = (~c[w] & (n3 | n4)) | (c[w] & (n2 | n3 | n4));
      }
    } else {
      for (int w = 0; w < W; w++) {
        u64 v = l1[w] ^ r1[w] ^ l2[w] ^ r2[w] ^ AT(A, j - 1, x)[w];
        if (j - 2 >= 0) v ^= AT(A, j - 2, x)[w];
        if (j + 1 <= H) v ^= AT(A, j + 1, x)[w];
        if (j + 2 <= H) v ^= AT(A, j + 2, x)[w];
        o[w] = v;
      }
    }
  }
  u64 *t = A; A = B; B = t;
}

int main(int argc, char **argv) {
  if (argc < 6) { fprintf(stderr, "usage: see header\n"); return 2; }
  L = atoi(argv[2]); H = atoi(argv[3]);
  size_t sz = (size_t)(H + 1) * L * W;
  A = calloc(sz, 8); B = calloc(sz, 8);
  if (!strcmp(argv[1], "trace")) {
    int gens = atoi(argv[4]); seedrng(strtoull(argv[5], 0, 10));
    for (size_t i = 0; i < sz; i++) A[i] = rnd();
    for (int t = 0; t <= gens; t++) {
      if (t) step(H + 1);
      printf("gen %d\n", t);
      for (int j = 0; j <= H; j++) { for (int x = 0; x < L; x++) putchar('0' + (int)(AT(A, j, x)[0] & 1)); putchar('\n'); }
    }
    return 0;
  }
  long nbatch = atol(argv[4]); u64 seed = strtoull(argv[5], 0, 10); int T0 = atoi(argv[6]);
  int T = H / 2; int noprune = getenv("NOPRUNE") != NULL;
  double expo = 0, deaths = 0, one = 0, onedie = 0, bexp[16] = {0}, bdth[16] = {0};
  for (long b = 0; b < nbatch; b++) {
    seedrng(seed * 1000003ULL + (u64)b);
    for (size_t i = 0; i < sz; i++) A[i] = rnd();
    u64 alive[W]; for (int w = 0; w < W; w++) alive[w] = ~0ULL;
    /* a soup whose row 0 is already empty is dead at age 0 (never exposed) */
    for (int w = 0; w < W; w++) { u64 a = 0; for (int x = 0; x < L; x++) a |= AT(A, 0, x)[w]; alive[w] &= a; }
    for (int t = 1; t <= T; t++) {
      int age = t - 1; u64 ex[W], on[W];
      for (int w = 0; w < W; w++) {
        ex[w] = age >= T0 ? alive[w] : 0;
        u64 c0 = 0, c1 = 0; for (int x = 0; x < L; x++) { u64 a = AT(A, 0, x)[w]; c1 |= c0 & a; c0 |= a; }
        on[w] = c0 & ~c1 & ex[w];
      }
      int rows = 2 * (T - t) + 1; if (rows > H + 1 || noprune) rows = H + 1;
      step(rows);
      int bin = age < 30 ? 0 : (age - 30) / 10 + 1; if (bin > 15) bin = 15;  /* ages 30-39, 40-49, ... */
      for (int w = 0; w < W; w++) {
        u64 a = 0; for (int x = 0; x < L; x++) a |= AT(A, 0, x)[w];
        u64 dead = ~a;
        int ne = __builtin_popcountll(ex[w]), nd = __builtin_popcountll(ex[w] & dead);
        expo += ne; deaths += nd; bexp[bin] += ne; bdth[bin] += nd;
        one += __builtin_popcountll(on[w]); onedie += __builtin_popcountll(on[w] & dead);
        alive[w] &= a;
      }
    }
  }
  printf("L %d H %d T0 %d replicas %ld\nexposure %.0f\ndeaths %.0f\none %.0f\nonedie %.0f\n", L, H, T0, nbatch * 64 * W, expo, deaths, one, onedie);
  printf("bexp"); for (int i = 0; i < 16; i++) printf(" %.0f", bexp[i]); printf("\nbdth"); for (int i = 0; i < 16; i++) printf(" %.0f", bdth[i]); printf("\n");
  return 0;
}
