/* fl.c: bit-sliced replicas of gump (B45/S345) on a finite cell graph, as a shared library for fl.py.
 *
 * Replica r lives in bit (r % 64) of word (r / 64) of every cell; W words per cell, 64*W replicas.
 * The cell graph is arbitrary (neighbour index n = a cell that is dead forever), so the same code runs
 * open-space octahedra (exact by T2) and the O_h orbit-reduced graph of a symmetric state (one cell per
 * orbit; a neighbour is the orbit of the neighbouring cell, so multiplicities come out right).
 * The kernel is research/peeling/rep.c's carry-save adder tree.
 *
 * Observables: G groups of (cell, weight); after every step the weighted live count of every group is
 * available per replica (bit-sliced counters, then a nibble-spread transpose). Some groups are "faces";
 * m(r) = min over face groups of the count is the order parameter.
 *
 *   fl_init       graph + groups
 *   fl_state      pointer to the current state, (n+1)*W words, row n always zero (python views it)
 *   fl_counts     counts of the current state
 *   fl_run        step `gens` generations, write counts after every step; optional reseed of replicas whose
 *                 m hits 0 (stationary sampling with restarts); per-replica age (gens since seed) is kept
 *   fl_run_until  step until, per replica, m <= lo[r] or m >= hi[r] (checked on the initial state too);
 *                 stopped replicas are frozen; returns the stop generation per replica (-1 = not stopped)
 */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

typedef uint64_t u64;
static int n, W, G, B, NF;
static int32_t *nb;           /* n*12 */
static int *gsz, *goff; static int32_t *gcell, *gwt; static int *face;
static u64 *bufA, *bufB, *cur, *nxt_;
static u64 spread16[16];
static u64 *seedmask;         /* n: cells that are seeded (bit 0 of word) */
static uint32_t *age;
static u64 rs[4];

static inline u64 rotl(const u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static u64 rnd(void) { const u64 r = rotl(rs[1] * 5, 7) * 9, t = rs[1] << 17;
  rs[2] ^= rs[0]; rs[3] ^= rs[1]; rs[1] ^= rs[2]; rs[0] ^= rs[3]; rs[2] ^= t; rs[3] = rotl(rs[3], 45); return r; }

void fl_seed(u64 seed) { rs[0] = 0x9E3779B97F4A7C15ULL ^ seed; rs[1] = 0xD1B54A32D192ED03ULL + seed * 7;
  rs[2] = 0x8CB92BA72F3D8DD7ULL; rs[3] = seed * 0x2545F4914F6CDD1DULL + 1; for (int i = 0; i < 20; i++) rnd(); }

int fl_init(int n_, int W_, const int32_t *nb_, int G_, const int32_t *gsz_, const int32_t *gcell_, const int32_t *gwt_,
            int nf, const int32_t *face_, const int32_t *seedable) {
  n = n_; W = W_; G = G_; NF = nf;
  free(nb); nb = malloc(4 * 12 * (size_t)n);
  for (size_t i = 0; i < 12 * (size_t)n; i++) nb[i] = nb_[i] < 0 ? n : nb_[i];
  free(gsz); free(goff); gsz = malloc(4 * G); goff = malloc(4 * (G + 1)); goff[0] = 0;
  int maxw = 0;
  for (int g = 0; g < G; g++) { gsz[g] = gsz_[g]; goff[g + 1] = goff[g] + gsz[g]; }
  free(gcell); free(gwt); gcell = malloc(4 * (size_t)goff[G] + 4); gwt = malloc(4 * (size_t)goff[G] + 4);
  memcpy(gcell, gcell_, 4 * (size_t)goff[G]); memcpy(gwt, gwt_, 4 * (size_t)goff[G]);
  for (int g = 0; g < G; g++) { int s = 0; for (int k = goff[g]; k < goff[g + 1]; k++) s += gwt[k]; if (s > maxw) maxw = s; }
  B = 1; while ((1 << B) <= maxw) B++;
  if (B > 16) return -1;
  free(face); face = malloc(4 * (nf + 1)); memcpy(face, face_, 4 * nf);
  free(bufA); free(bufB); bufA = calloc((size_t)(n + 1) * W, 8); bufB = calloc((size_t)(n + 1) * W, 8);
  cur = bufA; nxt_ = bufB;
  for (int v = 0; v < 16; v++) { u64 x = 0; for (int i = 0; i < 4; i++) if (v >> i & 1) x |= 1ULL << (16 * i); spread16[v] = x; }
  free(seedmask); seedmask = calloc(n, 8); for (int i = 0; i < n; i++) seedmask[i] = seedable[i] ? 1 : 0;
  free(age); age = calloc(64 * (size_t)W, 4);
  fl_seed(12345);
  return B;
}

u64 *fl_state(void) { return bufA; }
uint32_t *fl_age(void) { return age; }

#define FA(a, b, c, sum, car) { u64 _x = (a) ^ (b); sum = _x ^ (c); car = ((a) & (b)) | (_x & (c)); }

/* one generation cur -> nxt_; frozen replicas (bits set in frz[w]) keep their state */
static void step(const u64 *frz, u64 *diff) {
  for (int i = 0; i < n; i++) {
    const int32_t *q = nb + 12 * (size_t)i; u64 *o = nxt_ + (size_t)i * W; const u64 *me = cur + (size_t)i * W;
    const u64 *x0 = cur + (size_t)q[0] * W, *x1 = cur + (size_t)q[1] * W, *x2 = cur + (size_t)q[2] * W, *x3 = cur + (size_t)q[3] * W,
              *x4 = cur + (size_t)q[4] * W, *x5 = cur + (size_t)q[5] * W, *x6 = cur + (size_t)q[6] * W, *x7 = cur + (size_t)q[7] * W,
              *x8 = cur + (size_t)q[8] * W, *x9 = cur + (size_t)q[9] * W, *x10 = cur + (size_t)q[10] * W, *x11 = cur + (size_t)q[11] * W;
    for (int w = 0; w < W; w++) {
      u64 s0, c0, s1, c1, s2, c2, s3, c3, o1, t4, b0, t5, u0, f0, u1, f1, b1, f2, b2, b3;
      FA(x0[w], x1[w], x2[w], s0, c0); FA(x3[w], x4[w], x5[w], s1, c1);
      FA(x6[w], x7[w], x8[w], s2, c2); FA(x9[w], x10[w], x11[w], s3, c3);
      FA(s0, s1, s2, o1, t4); b0 = o1 ^ s3; t5 = o1 & s3;
      FA(c0, c1, c2, u0, f0); FA(c3, t4, t5, u1, f1); b1 = u0 ^ u1; f2 = u0 & u1;
      FA(f0, f1, f2, b2, b3);
      u64 r = ~b3 & ((b2 & ~b1) | (me[w] & ~b2 & b1 & b0));
      if (frz) r = (r & ~frz[w]) | (me[w] & frz[w]);
      if (diff) diff[w] |= r ^ o[w];          /* o held the state two generations back (double buffer) */
      o[w] = r;
    }
  }
  u64 *t = cur; cur = nxt_; nxt_ = t;
}

static void settle_buf(void) { if (cur != bufA) { memcpy(bufA, cur, 8 * (size_t)(n + 1) * W); nxt_ = bufB; cur = bufA; } }

/* counts of group g for word w into out[0..63] */
static void count_group(int g, int w, uint16_t *out) {
  u64 c[16]; for (int b = 0; b < B; b++) c[b] = 0;
  for (int k = goff[g]; k < goff[g + 1]; k++) {
    u64 x = cur[(size_t)gcell[k] * W + w]; if (!x) continue;
    int wt = gwt[k];
    for (int j = 0; wt; j++, wt >>= 1) if (wt & 1) { u64 carry = x; for (int b = j; carry && b < B; b++) { u64 t = c[b] & carry; c[b] ^= carry; carry = t; } }
  }
  u64 o[16]; memset(o, 0, sizeof o);
  for (int b = 0; b < B; b++) { u64 x = c[b]; if (!x) continue;
    for (int nib = 0; nib < 16; nib++) o[nib] |= spread16[(x >> (4 * nib)) & 15] << b; }
  memcpy(out, o, 128);
}

/* out[g*R + r] */
void fl_counts(uint16_t *out) {
  int R = 64 * W;
  for (int g = 0; g < G; g++) for (int w = 0; w < W; w++) count_group(g, w, out + (size_t)g * R + 64 * w);
}

static void reseed(int r, double p) {
  int w = r / 64; u64 bit = 1ULL << (r % 64);
  u64 thr = (u64)(p * 18446744073709551616.0);
  for (int i = 0; i < n; i++) { u64 *x = cur + (size_t)i * W + w; *x &= ~bit; if (seedmask[i] && rnd() < thr) *x |= bit; }
  age[r] = 0;
}

/* step gens generations; counts[t][g][r] (uint16) after step t (may be NULL), ages[t][r] age after step t (may be NULL).
 * reseed_p > 0: a replica with a face count 0 after a step is recorded (its counts row shows the 0) and then reseeded.
 * Returns number of reseeds. */
static long gclock = 0, nsettle = 0; static u64 *snap840 = NULL;
long fl_settles(void) { return nsettle; }
long fl_run(long gens, uint16_t *counts, uint32_t *ages, double reseed_p) {
  int R = 64 * W; long nres = 0;
  uint16_t *tmp = malloc(2 * (size_t)G * R);
  u64 *diff = calloc(W, 8);
  if (!snap840) snap840 = calloc((size_t)(n + 1) * W, 8);
  for (long t = 0; t < gens; t++) {
    for (int w = 0; w < W; w++) diff[w] = 0;
    step(NULL, diff);
    for (int r = 0; r < R; r++) age[r]++;
    gclock++;
    if (reseed_p > 0) {
      /* settled replicas (period 1 or 2 now; any period dividing 840 at multiples of 840) are reseeded; their age
         restarts, so python's age >= T0 cut drops them. Checked only for age > 2 (the buffer holds that replica's
         own state two generations back). */
      if (gclock % 840 == 0) {
        for (int w = 0; w < W; w++) { u64 eq = ~0ULL;
          for (int i = 0; i < n; i++) eq &= ~(cur[(size_t)i * W + w] ^ snap840[(size_t)i * W + w]);
          for (int k = 0; k < 64; k++) if ((eq >> k & 1) && age[64 * w + k] > 840) diff[w] &= ~(1ULL << k); else if (eq >> k & 1) diff[w] |= 1ULL << k; }
        memcpy(snap840, cur, 8 * (size_t)(n + 1) * W);
      }
      for (int r = 0; r < R; r++) if (!(diff[r / 64] >> (r % 64) & 1) && age[r] > 2) { reseed(r, reseed_p); nsettle++; age[r] = 0; }
    }
    uint16_t *row = counts ? counts + (size_t)t * G * R : tmp;
    if (counts || reseed_p > 0) fl_counts(row);
    if (ages) memcpy(ages + (size_t)t * R, age, 4 * (size_t)R);
    if (reseed_p > 0) for (int r = 0; r < R; r++) {
      int dead = 0; for (int f = 0; f < NF; f++) if (row[(size_t)face[f] * R + r] == 0) dead = 1;
      if (dead) { reseed(r, reseed_p); nres++; }
    }
  }
  settle_buf(); free(tmp); free(diff);
  return nres;
}

/* stop per replica when m <= lo[r] or m >= hi[r]; stop_gen[r] = generations stepped (-1: not stopped by maxgens);
 * stop_m[r] = m at stop (or at the end). minm[r] = smallest m seen (incl. start). Returns gens stepped. */
long fl_run_until(long maxgens, const int32_t *lo, const int32_t *hi, int32_t *stop_gen, int32_t *stop_m, int32_t *minm) {
  int R = 64 * W; u64 *frz = calloc(W, 8); int left = 0;
  uint16_t *row = malloc(2 * (size_t)G * R);
  int32_t *m = malloc(4 * (size_t)R);
  long t = 0;
  for (;;) {
    for (int r = 0; r < R; r++) m[r] = 1 << 30;
    for (int f = 0; f < NF; f++) for (int w = 0; w < W; w++) {
      uint16_t c[64]; count_group(face[f], w, c);
      for (int k = 0; k < 64; k++) if (c[k] < m[64 * w + k]) m[64 * w + k] = c[k];
    }
    left = 0;
    for (int r = 0; r < R; r++) {
      if (frz[r / 64] >> (r % 64) & 1) continue;
      if (t == 0 || m[r] < minm[r]) minm[r] = m[r];
      if (m[r] <= lo[r] || m[r] >= hi[r]) { frz[r / 64] |= 1ULL << (r % 64); stop_gen[r] = (int32_t)t; stop_m[r] = m[r]; }
      else { left++; stop_m[r] = m[r]; stop_gen[r] = -1; }
    }
    if (!left || t >= maxgens) break;
    step(frz, NULL); t++;
  }
  settle_buf(); free(frz); free(row); free(m);
  return t;
}
