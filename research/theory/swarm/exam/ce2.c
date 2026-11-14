/* ce2.c -- exam C-E2: probability that the 2D rule's edge row is empty at generations 1, 2, 3 from a fair soup.
 * Strip periodic in x (L columns), rows 0..6 (row 0 an edge, nothing above; deeper rows cannot reach row 0 by
 * generation 3).  Rule B34/S234 on the cross (x+-1, x+-2 in the row; rows r+-1, r+-2 in the column; rows < 0 dead).
 * Light cone: generation 1 computes rows 0..4, generation 2 rows 0..2, generation 3 row 0.
 *
 *   ce2 sample L nbatch seed     64*W soups per batch; prints soups and counts of row 0 empty at k = 1, 2, 3
 *   ce2 enum   L                 every soup of 7L bits (L <= 4): exact counts
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifndef W
#define W 8
#endif
typedef uint64_t u64;
static u64 s[4];
static inline u64 rotl(u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static inline u64 rnd(void) { u64 r = rotl(s[1] * 5, 7) * 9, t = s[1] << 17; s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2];
  s[0] ^= s[3]; s[2] ^= t; s[3] = rotl(s[3], 45); return r; }
static void seedrng(u64 x) { for (int i = 0; i < 4; i++) { x += 0x9E3779B97F4A7C15ULL; u64 z = x;
  z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL; z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL; s[i] = z ^ (z >> 31); } }

#define RMAX 7
static int L;
static u64 g0[RMAX][64][W], g1[RMAX][64][W];

static void step(u64 (*a)[64][W], u64 (*b)[64][W], int rows, int have) {
  for (int r = 0; r < rows; r++) for (int x = 0; x < L; x++) for (int w = 0; w < W; w++) {
    u64 in[8]; int n = 0;
    in[n++] = a[r][(x + 1) % L][w]; in[n++] = a[r][(x + L - 1) % L][w];
    in[n++] = a[r][(x + 2) % L][w]; in[n++] = a[r][(x + 2 * L - 2) % L][w];
    if (r - 1 >= 0) in[n++] = a[r - 1][x][w];
    if (r - 2 >= 0) in[n++] = a[r - 2][x][w];
    if (r + 1 < have) in[n++] = a[r + 1][x][w];
    if (r + 2 < have) in[n++] = a[r + 2][x][w];
    u64 b0 = 0, b1 = 0, b2 = 0, b3 = 0;
    for (int k = 0; k < n; k++) { u64 c0 = b0 & in[k]; b0 ^= in[k]; u64 c1 = b1 & c0; b1 ^= c0; u64 c2 = b2 & c1; b2 ^= c1; b3 |= c2; }
    u64 n2 = ~b3 & ~b2 & b1 & ~b0, n3 = ~b3 & ~b2 & b1 & b0, n4 = ~b3 & b2 & ~b1 & ~b0;
    u64 xc = a[r][x][w];
    b[r][x][w] = n3 | n4 | (xc & n2);
  }
}
static void run(double *cnt) {  /* g0 holds generation 0 (rows 0..6); adds the number of soups with row 0 empty */
  step(g0, g1, 5, 7);
  for (int w = 0; w < W; w++) { u64 a = 0; for (int x = 0; x < L; x++) a |= g1[0][x][w]; cnt[0] += __builtin_popcountll(~a); }
  step(g1, g0, 3, 5);
  for (int w = 0; w < W; w++) { u64 a = 0; for (int x = 0; x < L; x++) a |= g0[0][x][w]; cnt[1] += __builtin_popcountll(~a); }
  step(g0, g1, 1, 3);
  for (int w = 0; w < W; w++) { u64 a = 0; for (int x = 0; x < L; x++) a |= g1[0][x][w]; cnt[2] += __builtin_popcountll(~a); }
}
int main(int argc, char **argv) {
  L = atoi(argv[2]); double cnt[3] = {0}, soups = 0;
  if (!strcmp(argv[1], "sample")) {
    long nb = atol(argv[3]); seedrng(strtoull(argv[4], 0, 10));
    for (long b = 0; b < nb; b++) {
      for (int r = 0; r < 7; r++) for (int x = 0; x < L; x++) for (int w = 0; w < W; w++) g0[r][x][w] = rnd();
      run(cnt); soups += 64.0 * W;
    }
  } else {  /* enumerate: soup index i, bit (r * L + x) of i = cell (r, x); lanes = low 6 bits of the index */
    int nbits = 7 * L; static const u64 pat[6] = {0xAAAAAAAAAAAAAAAAULL, 0xCCCCCCCCCCCCCCCCULL, 0xF0F0F0F0F0F0F0F0ULL,
                                                  0xFF00FF00FF00FF00ULL, 0xFFFF0000FFFF0000ULL, 0xFFFFFFFF00000000ULL};
    long nb = 1L << (nbits - 6);
    for (long b = 0; b < nb; b += W) {
      for (int w = 0; w < W; w++) { long hi = b + w;
        for (int c = 0; c < nbits; c++) { int r = c / L, x = c % L;
          g0[r][x][w] = c < 6 ? pat[c] : (((hi >> (c - 6)) & 1) ? ~0ULL : 0); } }
      run(cnt); soups += 64.0 * W;
    }
  }
  printf("L %d soups %.0f empty_k1 %.0f empty_k2 %.0f empty_k3 %.0f\n", L, soups, cnt[0], cnt[1], cnt[2]);
  return 0;
}
