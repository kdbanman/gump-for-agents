/* toygap.c -- empty-window statistics E(l) of the edge of the toy (B34/S234, range-2 cross) in an H x 128 strip
 * periodic along the edge, for research/audit/REVIEW-exponent.md (verdict 2).  Shares no code with
 * research/theory/exponent/.  One strip at a time; rows are 128-bit words (bit x = column x).
 *
 *   toygap run SEED SECONDS BATCHGENS [H]     prints one line per batch: gens N c1 c2 ... c64
 *        c_l = number of (edge, start) pairs whose window of l consecutive edge cells is empty, over exposed
 *        generations (age >= 300 after a restart, state after the step, replica not restarted at that step);
 *        N = 128 * 2 * exposed generations.  Restart (soup 0.4) when: an edge row is empty, three consecutive
 *        interior rows are empty, three consecutive columns are empty, or the state equals the state two
 *        generations back or the snapshot taken at the last power-of-two age.
 *   toygap trace SEED GENS [H]               initial and final state of one soup (for validation)
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef unsigned __int128 u128;
#define HMAX 32
#define LMAX 64
static int H = 16;
static uint64_t s_;
static inline uint64_t rnd(void) { uint64_t z = (s_ += 0x9E3779B97F4A7C15ULL);
  z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL; z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL; return z ^ (z >> 31); }
static inline u128 rot(u128 v, int k) { k &= 127; return k ? (v << k) | (v >> (128 - k)) : v; }

static void soup(u128 *x) {               /* density 0.4 per cell */
  for (int y = 0; y < H; y++) { u128 v = 0;
    for (int b = 0; b < 128; b++) if ((rnd() >> 11) * (1.0 / 9007199254740992.0) < 0.4) v |= (u128)1 << b;
    x[y] = v; }
}
static void step(const u128 *x, u128 *o) {
  for (int y = 0; y < H; y++) {
    u128 nb[8]; int k = 0;
    nb[k++] = rot(x[y], 1); nb[k++] = rot(x[y], -1); nb[k++] = rot(x[y], 2); nb[k++] = rot(x[y], -2);
    nb[k++] = y >= 1 ? x[y - 1] : 0; nb[k++] = y >= 2 ? x[y - 2] : 0;
    nb[k++] = y + 1 < H ? x[y + 1] : 0; nb[k++] = y + 2 < H ? x[y + 2] : 0;
    u128 a0 = 0, a1 = 0, a2 = 0, a3 = 0;      /* 4-bit counter */
    for (int i = 0; i < 8; i++) { u128 c = a0 & nb[i]; a0 ^= nb[i]; u128 c1 = a1 & c; a1 ^= c; u128 c2 = a2 & c1; a2 ^= c1; a3 |= c2; }
    u128 n2 = ~a3 & ~a2 & a1 & ~a0, n3 = ~a3 & ~a2 & a1 & a0, n4 = ~a3 & a2 & ~a1 & ~a0;
    o[y] = n3 | n4 | (x[y] & n2);
  }
}

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage in header\n"); return 2; }
  s_ = strtoull(argv[2], 0, 10) * 2654435761ULL + 99;
  if (!strcmp(argv[1], "trace")) {
    long G = atol(argv[3]); if (argc > 4) H = atoi(argv[4]);
    u128 x[HMAX], o[HMAX]; soup(x);
    for (int pass = 0; pass < 2; pass++) {
      for (int y = 0; y < H; y++) { for (int b = 0; b < 128; b++) putchar((int)((x[y] >> b) & 1) + '0'); putchar('\n'); }
      if (pass) break;
      for (long g = 0; g < G; g++) { step(x, o); memcpy(x, o, sizeof(u128) * H); }
    }
    return 0;
  }
  double sec = atof(argv[3]); long B = atol(argv[4]); if (argc > 5) H = atoi(argv[5]);
  const long T0 = 300;
  u128 x[HMAX], o[HMAX], m1[HMAX], m2[HMAX], snap[HMAX]; int sv = 0;
  soup(x); memset(m1, 0xff, sizeof m1); memset(m2, 0, sizeof m2);
  long age = 0; double c[LMAX + 1]; double N = 0; long gb = 0;
  long restarts[5] = {0};
  memset(c, 0, sizeof c);
  clock_t t0 = clock();
  for (;;) {
    step(x, o);
    memcpy(m2, m1, sizeof(u128) * H); memcpy(m1, x, sizeof(u128) * H); memcpy(x, o, sizeof(u128) * H);
    age++; gb++;
    int ev = 0;
    if (x[0] == 0 || x[H - 1] == 0) ev = 1;
    for (int y = 1; !ev && y + 2 <= H - 2; y++) if ((x[y] | x[y + 1] | x[y + 2]) == 0) ev = 2;
    if (!ev) { u128 col = 0; for (int y = 0; y < H; y++) col |= x[y];
      u128 z = ~col; if (z & rot(z, 1) & rot(z, 2)) ev = 3; }
    if (!ev) { int eq2 = 1, eqs = sv; for (int y = 0; y < H; y++) { if (x[y] != m2[y]) eq2 = 0; if (x[y] != snap[y]) eqs = 0; }
      if (eq2 || eqs) ev = 4; }
    if (ev) { restarts[ev] += (age > T0); soup(x); memset(m1, 0xff, sizeof m1); memset(m2, 0, sizeof m2); sv = 0; age = 0; }
    else {
      if ((age & (age - 1)) == 0 && age >= 2) { memcpy(snap, x, sizeof(u128) * H); sv = 1; }
      if (age > T0) {
        for (int e = 0; e < 2; e++) { u128 z = ~x[e ? H - 1 : 0], w = z;
          N += 128;
          for (int l = 1; l <= LMAX && w; l++) { if (l > 1) w &= rot(z, -(l - 1));
            c[l] += (double)(__builtin_popcountll((uint64_t)w) + __builtin_popcountll((uint64_t)(w >> 64))); } }
      }
    }
    if (gb >= B) {
      printf("%ld %.0f", gb, N); for (int l = 1; l <= LMAX; l++) printf(" %.0f", c[l]);
      printf(" | %ld %ld %ld %ld\n", restarts[1], restarts[2], restarts[3], restarts[4]); fflush(stdout);
      memset(c, 0, sizeof c); N = 0; gb = 0; memset(restarts, 0, sizeof restarts);
      if ((double)(clock() - t0) / CLOCKS_PER_SEC > sec) break;
    }
  }
  return 0;
}
