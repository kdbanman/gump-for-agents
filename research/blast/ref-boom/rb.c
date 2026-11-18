// rb.c -- referee's stepper for the 8-layer {111} slab of gump, periodic in the plane with period lattice
// (H,K),(0,D) in the hexagonal basis e1 = (2,-2,0), e2 = (2,0,-2) (doubled coordinates; e1.e2 = |e1|^2/2).
// Written from docs/AUTOMATON.md and reference/oracle.py alone. 64 replicas, bit-sliced.
//   rb dump H K D seed gens [neg]      geometry + trajectory of replica 3 (for val.py)
//   rb run  H K D seed Mfacegens out   statistics of launches (see REVIEW.md)
//   rb island H K D seed Mfacegens out   the same, plus the island experiment (binary rbi; see below)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <assert.h>
typedef uint64_t u64;
#define MAXN 1024
#define R 64
#define BURN 300
static int H, K, D, A, N;
static int nb[MAXN][12], cx[MAXN], cy[MAXN], cz[MAXN];
static u64 ring[R][MAXN + 1];
static u64 rs;
static u64 rnd(void) { u64 z = (rs += 0x9E3779B97F4A7C15ULL); z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
  z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL; return z ^ (z >> 31); }
static int fdiv(int a, int b) { int q = a / b; if ((a % b != 0) && ((a < 0) != (b < 0))) q--; return q; }
static int cls(int x, int y, int z) {            // class of a cell modulo the period lattice; -1 outside the slab
  int s = x + y + z; if (s < 1 || s > 15) return -1;
  int yp = y & 1, zp = z & 1;
  if (yp && zp) return -2;
  int type = yp ? 1 : (zp ? 2 : 0);
  if (type == 0 && !(x & 1)) return -2;
  int a = (yp - y) / 2, b = (zp - z) / 2;        // cell = q + a e1 + b e2, q = (s-yp-zp, yp, zp)
  int m = fdiv(a, H); int a0 = a - m * H; b -= m * K; int b0 = ((b % D) + D) % D;
  int layer = (s - 1) / 2;
  return ((layer * 3 + type) * H + a0) * D + b0;
}
static void build(int neg) {
  A = 3 * H * D; N = 8 * A; assert(N <= MAXN);
  for (int idx = 0; idx < N; idx++) {
    int b0 = idx % D, a0 = (idx / D) % H, type = (idx / (D * H)) % 3, layer = idx / (D * H * 3);
    int s = 2 * layer + 1, yp = (type == 1), zp = (type == 2);
    int p[3] = { s - yp - zp + 2 * a0 + 2 * b0, yp - 2 * a0, zp - 2 * b0 };
    assert(cls(p[0], p[1], p[2]) == idx);
    cx[idx] = p[0]; cy[idx] = p[1]; cz[idx] = p[2];
    int a = type, b = (a + 1) % 3, c = (a + 2) % 3, k = 0;
    for (int sb = 2; sb >= -2; sb -= 4) for (int sc = 2; sc >= -2; sc -= 4) {
      int q[3] = { p[0], p[1], p[2] }; q[b] += sb; q[c] += sc;
      int n = cls(q[0], q[1], q[2]); assert(n != -2); nb[idx][k++] = n < 0 ? N : n; }
    for (int sa = 1; sa >= -1; sa -= 2) for (int ti = 0; ti < 2; ti++) for (int st = 1; st >= -1; st -= 2) {
      int t = ti ? c : b; int q[3] = { p[0], p[1], p[2] }; q[a] += sa; q[t] += st;
      int n = cls(q[0], q[1], q[2]); assert(n != -2); nb[idx][k++] = n < 0 ? N : n; }
    assert(k == 12);
  }
  if (neg) { int c0 = N / 2 + 5; nb[c0][7] = (nb[c0][7] + 1) % N; }   // negative control: one swapped neighbour
}
#define CSA(h, l, a, b, c) do { u64 _u = (a) ^ (b); (h) = ((a) & (b)) | (_u & (c)); (l) = _u ^ (c); } while (0)
static void step(const u64 *restrict s, u64 *restrict o) {
  for (int c = 0; c < N; c++) {
    const int *n = nb[c];
    u64 c1, s1, c2, s2, c3, s3, c4, s4, c5, s5, d1, t1, d2, t2, b3, b2;
    CSA(c1, s1, s[n[0]], s[n[1]], s[n[2]]); CSA(c2, s2, s[n[3]], s[n[4]], s[n[5]]);
    CSA(c3, s3, s[n[6]], s[n[7]], s[n[8]]); CSA(c4, s4, s[n[9]], s[n[10]], s[n[11]]);
    CSA(c5, s5, s1, s2, s3);
    u64 b0 = s5 ^ s4, c6 = s5 & s4;
    CSA(d1, t1, c1, c2, c3); CSA(d2, t2, c4, c5, c6);
    u64 b1 = t1 ^ t2, d3 = t1 & t2;
    CSA(b3, b2, d1, d2, d3);
    u64 x = s[c];
    o[c] = ~b3 & ((b2 & ~b1) | (x & ~b2 & b1 & b0));   // B45 / S345
  }
  o[N] = 0;
}
static void cnt(const u64 *s, int base, u64 *pl) {
  for (int b = 0; b < 7; b++) pl[b] = 0;
  for (int i = 0; i < A; i++) { u64 in = s[base + i]; for (int b = 0; b < 7 && in; b++) { u64 cr = pl[b] & in; pl[b] ^= in; in = cr; } }
}
static inline int ext(const u64 *pl, int r) { int p = 0; for (int b = 0; b < 7; b++) p |= (int)((pl[b] >> r) & 1) << b; return p; }
static int lpop(long tt, int l, int r) { const u64 *s = ring[tt & (R - 1)] + l * A; int p = 0; for (int i = 0; i < A; i++) p += (int)((s[i] >> r) & 1); return p; }
static void reinit(u64 *s, int r) { for (int c = 0; c < N; c++) { s[c] &= ~(1ULL << r); if (rnd() % 5 < 2) s[c] |= 1ULL << r; } }

// ---- island mode: after an over-full generation (face population q at t-1), the state at t is taken; the live
// face cells are grouped into clusters (connected through in-layer neighbours); variant j < 63 keeps cluster j only
// (all other cells of that face killed, everything beneath untouched), variant 63 is the untouched state.  A variant
// "fails" if its face is empty before it holds Lhalf cells again.
static int isl = 0, Lhalf; static long isN[3][128], isF[3][128], isU[3][128], isC[3][2], isPar[3], isOver, ISCAP = 15000;
static void island(const u64 *s, int r, int f, int q) {
  static u64 wa[MAXN + 1], wb[MAXN + 1];
  int bin = q < 0.70 * A ? 0 : (q < 0.78 * A ? 1 : 2);
  if (isPar[bin] >= ISCAP) return;
  int base = (f ? 7 : 0) * A, comp[128], size[64], stack[128], ncomp = 0;
  for (int i = 0; i < A; i++) comp[i] = -1;
  for (int i = 0; i < A; i++) if (((s[base + i] >> r) & 1) && comp[i] < 0) {
    if (ncomp == 63) { isOver++; return; }
    int sp = 0, sz = 0; stack[sp++] = i; comp[i] = ncomp;
    while (sp) { int c = stack[--sp]; sz++;
      for (int k = 0; k < 12; k++) { int n = nb[base + c][k];
        if (n >= base && n < base + A && ((s[n] >> r) & 1) && comp[n - base] < 0) { comp[n - base] = ncomp; stack[sp++] = n - base; } } }
    size[ncomp++] = sz; }
  if (!ncomp) return;
  for (int c = 0; c < N; c++) wa[c] = ((s[c] >> r) & 1) ? ~0ULL : 0;
  wa[N] = 0;
  for (int i = 0; i < A; i++) if (comp[i] >= 0) wa[base + i] = (1ULL << comp[i]) | (1ULL << 63);
  u64 und = ((1ULL << ncomp) - 1) | (1ULL << 63), failm = 0, pl[7]; u64 *a = wa, *b = wb;
  for (int g = 0; g < 400 && und; g++) {
    step(a, b); u64 *tmp = a; a = b; b = tmp; cnt(a, base, pl);
    for (int j = 0; j < 64; j++) if ((und >> j) & 1) { int p = ext(pl, j);
      if (p == 0) { failm |= 1ULL << j; und &= ~(1ULL << j); } else if (p >= Lhalf) und &= ~(1ULL << j); } }
  for (int j = 0; j < ncomp; j++) { isN[bin][size[j]]++; isF[bin][size[j]] += (failm >> j) & 1; isU[bin][size[j]] += (und >> j) & 1; }
  isC[bin][0]++; isC[bin][1] += (failm >> 63) & 1; isPar[bin]++;
}

static long Np[128], Lp[128], dur[R + 2], profDn[128][5], profCn[128];
static double profD[128][5][4], profC[128][4][4], normS[4], normS2[4];
static long normN;
int main(int argc, char **argv) {
  if (argc < 7) { fprintf(stderr, "usage\n"); return 2; }
  H = atoi(argv[2]); K = atoi(argv[3]); D = atoi(argv[4]); rs = strtoull(argv[5], 0, 10) * 0x2545F4914F6CDD1DULL + 12345;
  int dump = !strcmp(argv[1], "dump"); isl = !strcmp(argv[1], "island");
  build(dump && argc > 7 && !strcmp(argv[7], "neg"));
  memset(ring, 0, sizeof ring);
  for (int r = 0; r < 64; r++) reinit(ring[0], r);
  if (dump) {
    int gens = atoi(argv[6]); long t = 0;
    for (; t < 200; t++) step(ring[t & 63], ring[(t + 1) & 63]);
    printf("%d %d %d %d %d\n", H, K, D, A, N);
    for (int c = 0; c < N; c++) printf("%d %d %d %d\n", c, cx[c], cy[c], cz[c]);
    for (int g = 0; g <= gens; g++, t++) {
      const u64 *s = ring[t & 63];
      for (int c = 0; c < N; c++) putchar('0' + (int)((s[c] >> 3) & 1));
      putchar('\n');
      step(ring[t & 63], ring[(t + 1) & 63]);
    }
    return 0;
  }
  double target = atof(argv[6]) * 1e6; const char *out = argv[7];
  int L = (A + 1) / 2, Cmin = (int)(0.62 * A); Lhalf = L;
  int burn[64], lastP[64][2], prevP[64][2]; long lastT[64][2], born[64];
  for (int r = 0; r < 64; r++) { burn[r] = BURN; born[r] = 0; for (int f = 0; f < 2; f++) { lastP[r][f] = 0; prevP[r][f] = 0; lastT[r][f] = 0; } }
  static u64 snap[MAXN + 1]; memcpy(snap, ring[0], sizeof snap);
  long t = 0, E = 0, deaths = 0, old = 0, nper = 0, burnfail = 0;
  u64 pl0[7], pl1[7];
  while (E < target) {
    u64 *nxt = ring[(t + 1) & 63];
    step(ring[t & 63], nxt); t++;
    cnt(nxt, 0, pl0); cnt(nxt, 7 * A, pl1);
    u64 kill = 0, live = 0;
    for (int r = 0; r < 64; r++) {
      int p[2] = { ext(pl0, r), ext(pl1, r) };
      if (burn[r] > 0) {
        for (int f = 0; f < 2; f++) if (p[f] >= L) { lastT[r][f] = t; lastP[r][f] = p[f]; }
        if (p[0] == 0 || p[1] == 0) { kill |= 1ULL << r; burnfail++; }
        else if (--burn[r] == 0) born[r] = t;
        prevP[r][0] = p[0]; prevP[r][1] = p[1];
        continue;
      }
      live |= 1ULL << r;
      for (int f = 0; f < 2; f++) {
        Np[p[f]]++;
        if (p[f] > 0) E++;
        if (p[f] >= L) { lastT[r][f] = t; lastP[r][f] = p[f]; }
        else if (p[f] == 0) {
          deaths++; int lp = lastP[r][f]; long tl = lastT[r][f], d = t - tl;
          Lp[lp]++; dur[d < R ? d : R]++;
          if (d <= R - 5) {
            for (int lag = -2; lag <= 2; lag++) { long tt = tl + lag; if (tt > t) continue;
              for (int k = 0; k < 4; k++) profD[lp][lag + 2][k] += lpop(tt, f ? 7 - k : k, r);
              profDn[lp][lag + 2]++; }
          } else old++;
          kill |= 1ULL << r;
        }
      }
      if (!((kill >> r) & 1) && ((t + r) & 7) == 0 && t - born[r] >= 4)
        for (int f = 0; f < 2; f++) { int q = prevP[r][f]; if (q < Cmin) continue;
          for (int lag = -2; lag <= 1; lag++) for (int k = 0; k < 4; k++) profC[q][lag + 2][k] += lpop(t - 1 + lag, f ? 7 - k : k, r);
          profCn[q]++; }
      if (isl && !((kill >> r) & 1) && t - born[r] >= 4)
        for (int f = 0; f < 2; f++) if (prevP[r][f] >= Cmin && p[f] > 0) island(nxt, r, f, prevP[r][f]);
      prevP[r][0] = p[0]; prevP[r][1] = p[1];
    }
    if (isl && isPar[0] >= ISCAP && isPar[1] >= ISCAP && isPar[2] >= ISCAP) break;
    if ((t & 31) == 0) {
      live &= ~kill;
      for (int k = 0; k < 4; k++) { long sm = 0;
        for (int i = 0; i < A; i++) sm += __builtin_popcountll(nxt[k * A + i] & live) + __builtin_popcountll(nxt[(7 - k) * A + i] & live);
        normS[k] += sm; }
      normN += 2 * __builtin_popcountll(live);
    }
    if (t % 840 == 0) {
      u64 diff = 0; for (int c = 0; c < N; c++) diff |= nxt[c] ^ snap[c];
      for (int r = 0; r < 64; r++) if (!((diff >> r) & 1) && burn[r] == 0 && !((kill >> r) & 1)) { kill |= 1ULL << r; nper++; }
    }
    for (int r = 0; r < 64; r++) if ((kill >> r) & 1) { reinit(nxt, r); burn[r] = BURN; for (int f = 0; f < 2; f++) { lastP[r][f] = 0; lastT[r][f] = t; prevP[r][f] = 0; } }
    if (t % 840 == 0) memcpy(snap, nxt, sizeof snap);
  }
  FILE *fo = fopen(out, "w");
  fprintf(fo, "A %d %d %d %d seed %s\n", A, H, K, D, argv[5]);
  fprintf(fo, "E %ld deaths %ld old %ld nper %ld burnfail %ld gens %ld\n", E, deaths, old, nper, burnfail, t);
  for (int p = 0; p <= A; p++) fprintf(fo, "N %d %ld\n", p, Np[p]);
  for (int p = 0; p <= A; p++) if (Lp[p]) fprintf(fo, "L %d %ld\n", p, Lp[p]);
  for (int d = 0; d <= R; d++) if (dur[d]) fprintf(fo, "U %d %ld\n", d, dur[d]);
  for (int p = 0; p <= A; p++) for (int lg = 0; lg < 5; lg++) if (profDn[p][lg])
    fprintf(fo, "D %d %d %ld %.0f %.0f %.0f %.0f\n", p, lg - 2, profDn[p][lg], profD[p][lg][0], profD[p][lg][1], profD[p][lg][2], profD[p][lg][3]);
  for (int p = 0; p <= A; p++) if (profCn[p]) for (int lg = 0; lg < 4; lg++)
    fprintf(fo, "C %d %d %ld %.0f %.0f %.0f %.0f\n", p, lg - 2, profCn[p], profC[p][lg][0], profC[p][lg][1], profC[p][lg][2], profC[p][lg][3]);
  if (isl) for (int b = 0; b < 3; b++) { fprintf(fo, "IC %d %ld %ld %ld over %ld\n", b, isPar[b], isC[b][0], isC[b][1], isOver);
    for (int z = 1; z <= A; z++) if (isN[b][z]) fprintf(fo, "I %d %d %ld %ld %ld\n", b, z, isN[b][z], isF[b][z], isU[b][z]); }
  fprintf(fo, "M %ld %.0f %.0f %.0f %.0f\n", normN, normS[0], normS[1], normS[2], normS[3]);
  fclose(fo);
  return 0;
}
