/* t4: independent bit-sliced renewal stepper for gump (B45/S345) on the 4x4 8-layer slab torus (graph from geom4.py).
 * 64*W lanes; each lane runs one life at a time; a life ends at the first generation (checked after EVERY step) at
 * which
 *   - a transverse firewall exists (three cyclically consecutive dead layers of a transverse diagonal): kind 4
 *     (ties with a face death go to the firewall, as research/shape and eqtorus.py do),
 *   - else a face layer (t = 0 or t = 7) is extinct: kind 1,
 *   - else the state equals the lane's snapshot (taken at ages 1, 2, 4, 8, ...; Brent): kind 5, settled, any period;
 *     the cycle was certainly entered by the snapshot age, which is recorded.
 * The lane is then reseeded at once (density 0.4 on every node, own hash RNG) and a new life starts at age 0.
 *
 * Usage: t4 GRAPH W SEED GENS OUT          run; OUT gets int64 records (age, kind, snap_age, life id), open lives as kind 0
 *        t4 GRAPH W SEED GENS -trace INIT  lane 0 from node list INIT, no events, print "gen node node ..." each gen
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef uint64_t u64;
static int n, W;
static int32_t *nb;
static int fsz[2], *fl[2], tsz[3][8], *tl[3][8];

static u64 mix(u64 z) { z += 0x9E3779B97F4A7C15ULL; z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
  z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL; return z ^ (z >> 31); }
static const u64 THR = (u64)(0.4 * 9007199254740992.0);   /* 0.4 * 2^53 */
static int soup_bit(u64 seed, u64 life, int cell) { return (mix(mix(seed ^ mix(life)) + (u64)cell) >> 11) < THR; }

static void rd(void *p, size_t sz, size_t k, FILE *f) { if (fread(p, sz, k, f) != k) { fprintf(stderr, "short read\n"); exit(1); } }

static void step(const u64 *a, u64 *b) {
  for (int i = 0; i < n; i++) {
    const int32_t *q = nb + 12 * i; const u64 *me = a + (size_t)i * W; u64 *o = b + (size_t)i * W;
    for (int w = 0; w < W; w++) {
      u64 s0 = 0, s1 = 0, s2 = 0, s3 = 0;
      for (int k = 0; k < 12; k++) {             /* ripple counter, saturating in s3 (n >= 8) */
        u64 x = a[(size_t)q[k] * W + w], c0 = s0 & x; s0 ^= x;
        u64 c1 = s1 & c0; s1 ^= c0; u64 c2 = s2 & c1; s2 ^= c1; s3 |= c2;
      }
      o[w] = ~s3 & ((s2 & ~s1) | (me[w] & ~s2 & s1 & s0));   /* 4,5: born/survive; 3: survive */
    }
  }
  memset(b + (size_t)n * W, 0, 8 * (size_t)W);
}

int main(int argc, char **argv) {
  if (argc < 6) { fprintf(stderr, "usage\n"); return 1; }
  FILE *f = fopen(argv[1], "rb"); W = atoi(argv[2]); u64 seed = strtoull(argv[3], 0, 10); long G = atol(argv[4]);
  rd(&n, 4, 1, f); nb = malloc(4 * 12 * (size_t)n); rd(nb, 4, 12 * (size_t)n, f);
  for (int i = 0; i < 12 * n; i++) if (nb[i] < 0) nb[i] = n;
  for (int L = 0; L < 2; L++) { rd(&fsz[L], 4, 1, f); fl[L] = malloc(4 * fsz[L]); rd(fl[L], 4, fsz[L], f); }
  for (int d = 0; d < 3; d++) for (int L = 0; L < 8; L++) { rd(&tsz[d][L], 4, 1, f); tl[d][L] = malloc(4 * tsz[d][L]); rd(tl[d][L], 4, tsz[d][L], f); }
  fclose(f);
  int R = 64 * W, trace = argc > 6 && !strcmp(argv[5], "-trace");
  u64 *a = calloc((size_t)(n + 1) * W, 8), *b = calloc((size_t)(n + 1) * W, 8), *snap = calloc((size_t)n * W, 8);
  long *birth = calloc(R, sizeof(long)), *nexts = malloc(R * sizeof(long)), *sage = malloc(R * sizeof(long));
  u64 *sval = calloc(W, 8), life = 0;
  u64 *lifeid = malloc(R * 8);
  for (int r = 0; r < R; r++) { lifeid[r] = life++; nexts[r] = 1; sage[r] = -1;
    for (int i = 0; i < n; i++) if (soup_bit(seed, lifeid[r], i)) a[(size_t)i * W + r / 64] |= 1ULL << (r % 64); }
  if (trace) {
    for (int i = 0; i < n; i++) a[(size_t)i * W] &= ~1ULL;
    FILE *g = fopen(argv[6], "r"); int c; while (fscanf(g, "%d", &c) == 1) a[(size_t)c * W] |= 1ULL; fclose(g);
  }
  FILE *out = trace ? NULL : fopen(argv[5], "wb");
  u64 *ev = malloc(8 * W), *F0 = malloc(8 * W), *F1 = malloc(8 * W), *fw = malloc(8 * W), *eq = malloc(8 * W);
  u64 Ld[8 * 64];
  for (long gen = 1; gen <= G; gen++) {
    step(a, b); { u64 *t = a; a = b; b = t; }
    if (trace) { printf("%ld", gen); for (int i = 0; i < n; i++) if (a[(size_t)i * W] & 1) printf(" %d", i); printf("\n"); continue; }
    for (int w = 0; w < W; w++) { F0[w] = F1[w] = fw[w] = 0; eq[w] = 0; }
    for (int k = 0; k < fsz[0]; k++) for (int w = 0; w < W; w++) F0[w] |= a[(size_t)fl[0][k] * W + w];
    for (int k = 0; k < fsz[1]; k++) for (int w = 0; w < W; w++) F1[w] |= a[(size_t)fl[1][k] * W + w];
    for (int d = 0; d < 3; d++) {
      for (int L = 0; L < 8; L++) { u64 *l = Ld + (size_t)L * W; for (int w = 0; w < W; w++) l[w] = 0;
        for (int k = 0; k < tsz[d][L]; k++) for (int w = 0; w < W; w++) l[w] |= a[(size_t)tl[d][L][k] * W + w]; }
      for (int L = 0; L < 8; L++) for (int w = 0; w < W; w++)
        fw[w] |= ~Ld[L * W + w] & ~Ld[((L + 1) % 8) * W + w] & ~Ld[((L + 2) % 8) * W + w];
    }
    for (int w = 0; w < W; w++) { u64 x = 0; for (int i = 0; i < n; i++) x |= a[(size_t)i * W + w] ^ snap[(size_t)i * W + w];
      eq[w] = ~x & sval[w]; }
    for (int w = 0; w < W; w++) {
      u64 face = ~F0[w] | ~F1[w];
      u64 e = fw[w] | face | eq[w];
      ev[w] = e;
      while (e) {
        int k = __builtin_ctzll(e); e &= e - 1; int r = 64 * w + k; u64 bit = 1ULL << k;
        int64_t rec[4] = { gen - birth[r], (fw[w] & bit) ? 4 : (face & bit) ? 1 : 5, (fw[w] | face) & bit ? -1 : sage[r], (int64_t)lifeid[r] };
        fwrite(rec, 8, 4, out);
        lifeid[r] = life++; birth[r] = gen; nexts[r] = 1; sage[r] = -1; sval[w] &= ~bit;
        for (int i = 0; i < n; i++) { u64 *x = a + (size_t)i * W + w; *x = soup_bit(seed, lifeid[r], i) ? (*x | bit) : (*x & ~bit); }
      }
    }
    /* snapshots due: lanes (still in the same life) whose age reached nexts */
    for (int w = 0; w < W; w++) {
      u64 due = 0;
      for (int k = 0; k < 64; k++) { int r = 64 * w + k; if (!((ev[w] >> k) & 1) && gen - birth[r] == nexts[r]) due |= 1ULL << k; }
      if (!due) continue;
      for (int i = 0; i < n; i++) { u64 *s = snap + (size_t)i * W + w; *s = (*s & ~due) | (a[(size_t)i * W + w] & due); }
      sval[w] |= due;
      for (int k = 0; k < 64; k++) if ((due >> k) & 1) { int r = 64 * w + k; sage[r] = nexts[r]; nexts[r] *= 2; }
    }
  }
  if (!trace) {
    for (int r = 0; r < R; r++) { int64_t rec[4] = { G - birth[r], 0, sage[r], (int64_t)lifeid[r] }; fwrite(rec, 8, 4, out); }
    fclose(out);
    fprintf(stderr, "done: %llu lives started, %ld gens x %d lanes\n", (unsigned long long)life, G, R);
  }
  return 0;
}
