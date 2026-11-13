/* fg.c -- the EXACT functional graph of the toy (cross2, B34/S234) on a small vessel: every one of the 2^N states.
 *
 *   fg box   H L OUT     H x L box, outside dead forever; 4 edges (top/bottom rows, left/right columns)
 *   fg strip H L OUT     H rows, L columns periodic along the edge (L >= 5); 2 edges (top/bottom rows)
 *
 * N = H*L <= 32 (one byte per state: 4 GB at N = 32).  Two passes over all states, each O(2^N) rule evaluations:
 *  A. death times.  T(x) = 0 if some edge of x is empty, else 1 + T(F(x)); T = infinity iff the orbit never loses an
 *     edge, i.e. x is in the basin of an IMMORTAL cycle (every edge occupied at every phase).  Exact histogram of T
 *     over all 2^N states, the immortal cycles (count by period) and the size of their basin.
 *  B. the whole graph.  All cycles by period (with: immortal? empty? edge-touching at all phases for each edge?),
 *     number of cyclic states, exact histogram of transient lengths (distance to the cycle).
 * Table codes: 0 unknown, 1..252 exact value, 253 = ">= 253" (resolved by walking on), 254 on the current path,
 * 255 = infinity (pass A) / cyclic (pass B).
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef uint64_t u64;
typedef uint32_t u32;

static int H, L, N, periodic;
static u64 FULL, mA[3], mB[3], mC[3], mD[3], edge[4]; static int nedge;

static inline u64 step(u64 s) {
  u64 a, b, c, d, e, f, g, h;
  if (periodic) {
    a = ((s >> 1) & mA[1]) | ((s << (L - 1)) & mB[1]);
    b = ((s << 1) & mC[1]) | ((s >> (L - 1)) & mD[1]);
    c = ((s >> 2) & mA[2]) | ((s << (L - 2)) & mB[2]);
    d = ((s << 2) & mC[2]) | ((s >> (L - 2)) & mD[2]);
  } else {
    a = (s >> 1) & mA[1]; b = (s << 1) & mC[1]; c = (s >> 2) & mA[2]; d = (s << 2) & mC[2];
  }
  e = s >> L; f = (s << L) & FULL; g = s >> (2 * L); h = (s << (2 * L)) & FULL;
  /* 8-input bit-sliced sum */
  u64 s1 = a ^ b ^ c, c1 = (a & b) | (c & (a ^ b));
  u64 s2 = d ^ e ^ f, c2 = (d & e) | (f & (d ^ e));
  u64 s3 = g ^ h, c3 = g & h;
  u64 n0 = s1 ^ s2 ^ s3, c4 = (s1 & s2) | (s3 & (s1 ^ s2));
  u64 t = c1 ^ c2 ^ c3, d1 = (c1 & c2) | (c3 & (c1 ^ c2));
  u64 n1 = t ^ c4, d2 = t & c4;
  u64 n2 = d1 ^ d2, n3 = d1 & d2;
  u64 e3 = ~n3 & ~n2 & n1 & n0, e4 = ~n3 & n2 & ~n1 & ~n0, e2 = ~n3 & ~n2 & n1 & ~n0;
  return (e3 | e4 | (s & e2)) & FULL;
}
static inline int alive0(u64 s) { for (int i = 0; i < nedge; i++) if (!(s & edge[i])) return 0; return 1; }

static uint8_t *tab; static u32 *stk; static size_t stkcap;
static void push(size_t *n, u32 v) { if (*n == stkcap) { stkcap *= 2; stk = realloc(stk, stkcap * 4); if (!stk) { fprintf(stderr, "stack\n"); exit(3); } } stk[(*n)++] = v; }
#define HMAX (1 << 22)
static u64 *hist; static u64 hover;
static inline void count(u64 T) { if (T < HMAX) hist[T]++; else hover++; }
#define PMAX 4096
static u64 cyc_n[PMAX + 1], cyc_big, cyc_big_states, cyc_maxp;

int main(int argc, char **argv) {
  if (argc < 5) { fprintf(stderr, "usage: fg box|strip H L OUT\n"); return 2; }
  periodic = !strcmp(argv[1], "strip"); H = atoi(argv[2]); L = atoi(argv[3]); N = H * L;
  if (N > 32 || (periodic && L < 5)) { fprintf(stderr, "need N <= 32 (and L >= 5 for strips)\n"); return 2; }
  FULL = N == 64 ? ~0ULL : (1ULL << N) - 1;
  for (int k = 1; k <= 2; k++) { mA[k] = mB[k] = mC[k] = mD[k] = 0;
    for (int y = 0; y < H; y++) for (int x = 0; x < L; x++) { u64 bit = 1ULL << (y * L + x);
      if (x < L - k) mA[k] |= bit; else mB[k] |= bit;
      if (x >= k) mC[k] |= bit; else mD[k] |= bit; } }
  nedge = 0; u64 top = 0, bot = 0, lef = 0, rig = 0;
  for (int x = 0; x < L; x++) { top |= 1ULL << x; bot |= 1ULL << ((H - 1) * L + x); }
  for (int y = 0; y < H; y++) { lef |= 1ULL << (y * L); rig |= 1ULL << (y * L + L - 1); }
  edge[nedge++] = top; edge[nedge++] = bot; if (!periodic) { edge[nedge++] = lef; edge[nedge++] = rig; }
  u64 TOT = 1ULL << N;
  tab = calloc(TOT, 1); hist = calloc(HMAX, 8); stkcap = 1 << 20; stk = malloc(stkcap * 4);
  if (!tab || !hist) { fprintf(stderr, "memory\n"); return 3; }
  FILE *fo = fopen(argv[4], "w");
  fprintf(fo, "vessel %s\nH %d\nL %d\nN %d\n", argv[1], H, L, N);

  /* ---------------- pass A: death times ---------------- */
  u64 n_inf = 0, icyc_states = 0, icyc = 0;
  memset(cyc_n, 0, sizeof cyc_n); cyc_big = cyc_big_states = cyc_maxp = 0;
  for (u64 x = 0; x < TOT; x++) {
    if (!alive0(x)) { hist[0]++; continue; }
    if (tab[x]) continue;
    size_t n = 0; push(&n, (u32)x); tab[x] = 254;
    u64 y = step(x); u64 base = 0; int inf = 0;
    for (;;) {
      if (!alive0(y)) { base = 0; break; }
      uint8_t v = tab[y];
      if (v == 0) { push(&n, (u32)y); tab[y] = 254; y = step(y); continue; }
      if (v == 254) { size_t j = n; while (stk[j - 1] != (u32)y) j--; u64 p = n - (j - 1);
        icyc++; icyc_states += p; if (p <= PMAX) cyc_n[p]++; else { cyc_big++; cyc_big_states += p; } if (p > cyc_maxp) cyc_maxp = p;
        inf = 1; break; }
      if (v == 255) { inf = 1; break; }
      if (v <= 252) { base = v; break; }
      { u64 z = y, st = 0; for (;;) { z = step(z); st++; if (!alive0(z)) { base = st; break; } if (tab[z] <= 252) { base = st + tab[z]; break; } } }
      break;
    }
    if (inf) { n_inf += n; while (n) tab[stk[--n]] = 255; }
    else { u64 T = base; while (n) { T++; count(T); tab[stk[--n]] = T > 252 ? 253 : (uint8_t)T; } }
  }
  fprintf(fo, "immortal_basin %llu\nimmortal_cycles %llu\nimmortal_cyclic_states %llu\nimmortal_max_period %llu\n",
          (unsigned long long)n_inf, (unsigned long long)icyc, (unsigned long long)icyc_states, (unsigned long long)cyc_maxp);
  fprintf(fo, "immortal_by_period"); for (int p = 1; p <= PMAX; p++) if (cyc_n[p]) fprintf(fo, " %d:%llu", p, (unsigned long long)cyc_n[p]);
  if (cyc_big) fprintf(fo, " big:%llu:%llu", (unsigned long long)cyc_big, (unsigned long long)cyc_big_states); fprintf(fo, "\n");
  { int last = 0; for (int t = 0; t < HMAX; t++) if (hist[t]) last = t;
    fprintf(fo, "death_hist"); for (int t = 0; t <= last; t++) fprintf(fo, " %llu", (unsigned long long)hist[t]); fprintf(fo, "\ndeath_over %llu\n", (unsigned long long)hover); }
  fflush(fo);

  /* ---------------- pass B: all cycles, transient lengths ---------------- */
  memset(tab, 0, TOT); memset(hist, 0, HMAX * 8); hover = 0;
  /* per-period: cycles, and how many are immortal / have population 0 */
  static u64 pc[PMAX + 1], pim[PMAX + 1]; u64 bigc = 0, bigs = 0, maxp = 0, ncyc = 0, ncs = 0, nim = 0, nims = 0;
  u64 edge_touch_cyc = 0, edge_touch_states = 0;   /* cycles that keep SOME cell in an edge at every phase (not all edges) */
  for (u64 x = 0; x < TOT; x++) {
    if (tab[x]) continue;
    size_t n = 0; push(&n, (u32)x); tab[x] = 254;
    u64 y = step(x); u64 base = 0;
    for (;;) {
      uint8_t v = tab[y];
      if (v == 0) { push(&n, (u32)y); tab[y] = 254; y = step(y); continue; }
      if (v == 254) { size_t j = n; while (stk[j - 1] != (u32)y) j--; u64 p = n - (j - 1);
        int im = 1, anyedge = 1; for (size_t q = j - 1; q < n; q++) { u64 z = stk[q]; if (!alive0(z)) im = 0; u64 all = 0; for (int i = 0; i < nedge; i++) all |= edge[i]; if (!(z & all)) anyedge = 0; }
        ncyc++; ncs += p; if (im) { nim++; nims += p; } if (anyedge) { edge_touch_cyc++; edge_touch_states += p; }
        if (p <= PMAX) { pc[p]++; if (im) pim[p]++; } else { bigc++; bigs += p; } if (p > maxp) maxp = p;
        while (n > j - 1) tab[stk[--n]] = 255;
        base = 0; break; }
      if (v == 255) { base = 0; break; }
      if (v <= 252) { base = v; break; }
      { u64 z = y, st = 0; for (;;) { z = step(z); st++; if (tab[z] == 255) { base = st; break; } if (tab[z] <= 252) { base = st + tab[z]; break; } } }
      break;
    }
    { u64 T = base; while (n) { T++; count(T); tab[stk[--n]] = T > 252 ? 253 : (uint8_t)T; } }
  }
  fprintf(fo, "cycles %llu\ncyclic_states %llu\nmax_period %llu\ncycles_immortal %llu\ncyclic_states_immortal %llu\ncycles_edge_touching %llu\ncyclic_states_edge_touching %llu\n",
          (unsigned long long)ncyc, (unsigned long long)ncs, (unsigned long long)maxp, (unsigned long long)nim, (unsigned long long)nims,
          (unsigned long long)edge_touch_cyc, (unsigned long long)edge_touch_states);
  fprintf(fo, "cycles_by_period"); for (int p = 1; p <= PMAX; p++) if (pc[p]) fprintf(fo, " %d:%llu:%llu", p, (unsigned long long)pc[p], (unsigned long long)pim[p]);
  if (bigc) fprintf(fo, " big:%llu:%llu", (unsigned long long)bigc, (unsigned long long)bigs); fprintf(fo, "\n");
  { int last = 0; for (int t = 0; t < HMAX; t++) if (hist[t]) last = t;
    fprintf(fo, "transient_hist %llu", (unsigned long long)ncs); for (int t = 1; t <= last; t++) fprintf(fo, " %llu", (unsigned long long)hist[t]); fprintf(fo, "\ntransient_over %llu\n", (unsigned long long)hover); }
  fclose(fo);
  return 0;
}
