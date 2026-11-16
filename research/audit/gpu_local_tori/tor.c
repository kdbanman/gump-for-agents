/* tor.c: gump (B45/S345) on an 8-layer face torus (graph from geo.py), bit-sliced, lives renewed, every event
 * tested every generation. Written for research/audit/REVIEW-gpu-local-tori.md; nothing taken from research/.
 *
 *   tor run   GEO W SEED GENS OUT     64*W lanes, GENS generations; one binary record per life to OUT
 *   tor trace GEO SEED GENS OUT       64 lanes (word 0) of first-life soups, no events, no renewal; the whole
 *                                     state (n words) after every generation 0..GENS to OUT (validation)
 *
 * A life starts from a soup (every cell live with probability 0.4, from a counter hash of (seed, lane, life, cell))
 * at age 0. After every generation, in this order:
 *   firewall (kind 4): on a transverse diagonal with >= 3 layers, three cyclically consecutive layers all dead;
 *   face death (kind 1): layer t = 0 or t = M-1 empty (a firewall in the same generation wins, as on the GPU);
 *   cycle (kind 2): the state equals the lane's snapshot, taken at ages 1, 2, 4, 8, ... (any period).
 * A life that ends is recorded (lane, kind, birth generation, age, snapshot age, life number) and the lane reseeds
 * at once. At the end every open life is recorded with kind 0. Exposure of a life = its age at its end.
 * Build with -DMUTANT=1 for a wrong rule (survival also at n = 6): the validation must then fail.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef uint64_t u64;

static inline u64 mix(u64 z) { z += 0x9E3779B97F4A7C15ULL; z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
  z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL; return z ^ (z >> 31); }
static inline int soupbit(u64 seed, u64 lane, u64 life, u64 cell) {
  u64 h = mix(mix(mix(mix(seed) ^ lane) ^ life) ^ cell);
  return (h >> 11) < (u64)(0.4 * 9007199254740992.0);   /* 0.4 * 2^53 */
}

typedef struct { int32_t lane, kind; int64_t birth, age, snap, life; } rec_t;

int n, M, W, nlay[3]; int32_t *nb, *tl, *sd[3];
u64 *A, *B, *S;          /* state now, next, snapshot: [(n+1)*W], row n = 0 */

static void step(void) {
  for (int i = 0; i < n; i++) {
    const int32_t *q = nb + 12 * i; const u64 *me = A + (size_t)i * W; u64 *o = B + (size_t)i * W;
    for (int w = 0; w < W; w++) {
      u64 x[12];
      for (int k = 0; k < 12; k++) x[k] = A[(size_t)q[k] * W + w];
      /* count to 4 bits c0..c3 by four 3-input adders, then sum */
      u64 s[4], c[4];
      for (int g = 0; g < 4; g++) { u64 a = x[3 * g], b = x[3 * g + 1], d = x[3 * g + 2];
        s[g] = a ^ b ^ d; c[g] = (a & b) | (a & d) | (b & d); }
      u64 o1 = s[0] ^ s[1] ^ s[2], k1 = (s[0] & s[1]) | (s[0] & s[2]) | (s[1] & s[2]);
      u64 c0 = o1 ^ s[3], k2 = o1 & s[3];                    /* weight 1 */
      /* weight-2 inputs: c[0..3], k1, k2 (six bits) */
      u64 u0 = c[0] ^ c[1] ^ c[2], f0 = (c[0] & c[1]) | (c[0] & c[2]) | (c[1] & c[2]);
      u64 u1 = c[3] ^ k1 ^ k2, f1 = (c[3] & k1) | (c[3] & k2) | (k1 & k2);
      u64 c1 = u0 ^ u1, f2 = u0 & u1;
      u64 c2 = f0 ^ f1 ^ f2, c3 = (f0 & f1) | (f0 & f2) | (f1 & f2);
      u64 n3 = ~c3 & ~c2 & c1 & c0, n4 = ~c3 & c2 & ~c1 & ~c0, n5 = ~c3 & c2 & ~c1 & c0;
      u64 nx = n4 | n5 | (me[w] & n3);
#if MUTANT
      u64 n6 = ~c3 & c2 & c1 & ~c0; nx |= me[w] & n6;
#endif
      o[w] = nx;
    }
  }
  u64 *t = A; A = B; B = t;
}

static void seedlane(u64 seed, int lane, u64 life) {
  int w = lane / 64; u64 bit = 1ULL << (lane % 64);
  for (int i = 0; i < n; i++) { u64 *x = A + (size_t)i * W + w;
    if (soupbit(seed, lane, life, i)) *x |= bit; else *x &= ~bit; }
}

int main(int argc, char **argv) {
  if (argc < 6) { fprintf(stderr, "usage: tor run GEO W SEED GENS OUT | tor trace GEO SEED GENS OUT\n"); return 1; }
  int trace = !strcmp(argv[1], "trace");
  FILE *f = fopen(argv[2], "rb"); if (!f) return 1;
  if (fread(&n, 4, 1, f) != 1 || fread(&M, 4, 1, f) != 1) return 1;
  nb = malloc(4 * 12 * (size_t)n); tl = malloc(4 * (size_t)n);
  if (fread(nb, 4, 12 * (size_t)n, f) != 12 * (size_t)n || fread(tl, 4, n, f) != (size_t)n) return 1;
  for (int d = 0; d < 3; d++) { sd[d] = malloc(4 * (size_t)n); if (fread(sd[d], 4, n, f) != (size_t)n) return 1; }
  if (fread(nlay, 4, 3, f) != 3) return 1;
  fclose(f);
  for (int i = 0; i < 12 * n; i++) if (nb[i] < 0) nb[i] = n;
  W = trace ? 1 : atoi(argv[3]);
  int ai = trace ? 3 : 4;
  u64 seed = strtoull(argv[ai], 0, 10); long long gens = atoll(argv[ai + 1]); const char *outp = argv[ai + 2];
  int R = 64 * W;
  A = calloc((size_t)(n + 1) * W, 8); B = calloc((size_t)(n + 1) * W, 8); S = calloc((size_t)(n + 1) * W, 8);
  long long *age = calloc(R, 8), *birth = calloc(R, 8), *snapage = calloc(R, 8), *life = calloc(R, 8);
  for (int r = 0; r < R; r++) seedlane(seed, r, 0);
  FILE *out = fopen(outp, "wb"); if (!out) return 1;
  if (trace) {
    fwrite(A, 8, n, out);
    for (long long g = 1; g <= gens; g++) { step(); fwrite(A, 8, n, out); }
    fclose(out); return 0;
  }
  /* face cells, transverse layer cell lists */
  int nf0 = 0, nf1 = 0; int32_t *f0 = malloc(4 * n), *f1 = malloc(4 * n);
  for (int i = 0; i < n; i++) { if (tl[i] == 0) f0[nf0++] = i; if (tl[i] == M - 1) f1[nf1++] = i; }
  int usefw[3]; for (int d = 0; d < 3; d++) usefw[d] = nlay[d] >= 3;
  u64 *hasnap = calloc(W, 8), *al = calloc(64 * (size_t)W, 8);
  long long nrec = 0, cnt[5] = {0};
  for (long long G = 1; G <= gens; G++) {
    step();
    for (int w = 0; w < W; w++) {
      u64 a0 = 0, a1 = 0;
      for (int k = 0; k < nf0; k++) a0 |= A[(size_t)f0[k] * W + w];
      for (int k = 0; k < nf1; k++) a1 |= A[(size_t)f1[k] * W + w];
      u64 face = ~(a0 & a1), fw = 0;
      for (int d = 0; d < 3; d++) if (usefw[d]) {
        int L = nlay[d]; u64 lay[64] = {0};
        for (int i = 0; i < n; i++) lay[sd[d][i]] |= A[(size_t)i * W + w];
        for (int l = 0; l < L; l++) fw |= ~(lay[l] | lay[(l + 1) % L] | lay[(l + 2) % L]);
      }
      u64 diff = 0;
      for (int i = 0; i < n; i++) diff |= A[(size_t)i * W + w] ^ S[(size_t)i * W + w];
      u64 cyc = ~diff & hasnap[w];
      u64 end = fw | face | cyc;
      u64 snapm = 0;
      for (int k = 0; k < 64; k++) { int r = 64 * w + k; long long a = ++age[r];
        if (!((end >> k) & 1) && (a & (a - 1)) == 0) snapm |= 1ULL << k; }
      if (end) {
        u64 x = end;
        while (x) { int k = __builtin_ctzll(x); x &= x - 1; int r = 64 * w + k;
          rec_t q = { r, ((fw >> k) & 1) ? 4 : ((face >> k) & 1) ? 1 : 2, birth[r], age[r],
                      ((hasnap[w] >> k) & 1) ? snapage[r] : -1, life[r] };
          fwrite(&q, sizeof q, 1, out); nrec++; cnt[q.kind]++;
          life[r]++; birth[r] = G; age[r] = 0; snapage[r] = 0; seedlane(seed, r, life[r]); }
        hasnap[w] &= ~end;
      }
      if (snapm) {
        for (int i = 0; i < n; i++) { u64 *s = S + (size_t)i * W + w; *s = (*s & ~snapm) | (A[(size_t)i * W + w] & snapm); }
        hasnap[w] |= snapm;
        u64 x = snapm; while (x) { int k = __builtin_ctzll(x); x &= x - 1; snapage[64 * w + k] = age[64 * w + k]; }
      }
    }
  }
  for (int r = 0; r < R; r++) { rec_t q = { r, 0, birth[r], age[r], -1, life[r] }; fwrite(&q, sizeof q, 1, out); }
  fclose(out);
  fprintf(stderr, "gens %lld lanes %d records %lld face %lld fw %lld cycle %lld\n", gens, R, nrec + R, cnt[1], cnt[4], cnt[2]);
  return 0;
}
