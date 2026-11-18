// sl.c -- ref-hull: stepper for the 8-layer {111} slab torus with period lattice (H,K),(0,D), and plain-running dip rates.
// Geometry: cells p (doubled coords, one odd) with s = x+y+z in {-7,...,7}; in-plane basis e1 = (2,-2,0), e2 = (2,0,-2);
// periods H e1 + K e2 and D e2; outside the slab dead (T2 from both sides). Faces: layers s = +7 and s = -7.
//   sl val H K D SEED GENS NEG ; sl nu H K D SEED GENS LAMA
// Written from reference/oracle.py and docs/AUTOMATON.md alone (referee code; see README.md).
//   rh val R SEED GENS NEG            dump states of three lanes for validate.py (NEG=1: one swapped neighbour)
//   rh run R SEED M NS LAG STEP       one replication of the sampler; prints one RESULT line
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define W 4
#define NL (64*W)
#define MAXC 5400
#define KH 8
typedef uint64_t v4 __attribute__((vector_size(32)));

static int R, N, A, LAG = 2, nw;
static int cx[MAXC], cy[MAXC], cz[MAXC], nb[MAXC][12];
static int fc[8][256], nf[8];
static unsigned char deep[MAXC];
static uint64_t S[KH][MAXC + 1][W] __attribute__((aligned(32)));
static int TH, TK, TD;
static int sidx[8][2 * 64][2 * 64];

static uint64_t rs[4];
static inline uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static inline uint64_t rnd(void) {
  uint64_t r = rotl(rs[0] + rs[3], 23) + rs[0], t = rs[1] << 17;
  rs[2] ^= rs[0]; rs[3] ^= rs[1]; rs[1] ^= rs[2]; rs[0] ^= rs[3]; rs[2] ^= t; rs[3] = rotl(rs[3], 45);
  return r;
}
static void seedrng(uint64_t s) {
  for (int i = 0; i < 4; i++) {
    s += 0x9E3779B97F4A7C15ULL; uint64_t z = s;
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL; z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL; rs[i] = z ^ (z >> 31);
  }
}
static inline double urand(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static inline long rint_(long n) { return (long)(urand() * n); }


static int cellof(int x, int y, int z) {   // index of the cell at doubled coordinates, or N (dead) outside the slab
  int s = x + y + z;
  if (s < -7 || s > 7) return N;
  int u = y, w = z;
  int m = (u >= 0) ? u / (2 * TH) : -((-u + 2 * TH - 1) / (2 * TH));
  u -= 2 * TH * m; w -= 2 * TK * m;
  w %= 2 * TD; if (w < 0) w += 2 * TD;
  return sidx[(s + 7) / 2][u][w];
}
static void build(int neg) {
  N = 0;
  for (int si = 0; si < 8; si++) for (int u = 0; u < 2 * TH; u++) for (int w = 0; w < 2 * TD; w++) {
    int s = 2 * si - 7, x = s - u - w;
    sidx[si][u][w] = -1;
    if ((abs(x) & 1) + (u & 1) + (w & 1) != 1) continue;
    sidx[si][u][w] = N; cx[N] = x; cy[N] = u; cz[N] = w; N++;
  }
  nf[0] = nf[1] = 0;
  for (int c = 0; c < N; c++) {
    int p[3] = {cx[c], cy[c], cz[c]};
    int a = (abs(p[0]) & 1) ? 0 : (abs(p[1]) & 1) ? 1 : 2;
    int b = (a == 0) ? 1 : 0, cc = (a == 2) ? 1 : 2;
    int k = 0, offs[12][3];
    for (int sb = 2; sb >= -2; sb -= 4) for (int sc = 2; sc >= -2; sc -= 4) {
      offs[k][0] = offs[k][1] = offs[k][2] = 0; offs[k][b] = sb; offs[k][cc] = sc; k++;
    }
    for (int sa = 1; sa >= -1; sa -= 2) for (int ti = 0; ti < 2; ti++) for (int st = 1; st >= -1; st -= 2) {
      int t = ti ? cc : b;
      offs[k][0] = offs[k][1] = offs[k][2] = 0; offs[k][a] = sa; offs[k][t] = st; k++;
    }
    for (k = 0; k < 12; k++) nb[c][k] = cellof(p[0] + offs[k][0], p[1] + offs[k][1], p[2] + offs[k][2]);
    int s = p[0] + p[1] + p[2];
    if (s == 7) fc[0][nf[0]++] = c;
    if (s == -7) fc[1][nf[1]++] = c;
  }
  for (int c = 0; c < N; c++) for (int k = 0; k < 12; k++) if (nb[c][k] < 0) { fprintf(stderr, "bad neighbour\n"); exit(2); }
  A = nf[0]; nw = (N + 63) / 64;
  if (neg) { int c = N / 2, o = (nb[c][0] + 7) % N; fprintf(stderr, "NEG: cell %d nb[0] %d -> %d\n", c, nb[c][0], o); nb[c][0] = o; }
}
static inline v4 ld(const uint64_t *p) { v4 v; memcpy(&v, p, 32); return v; }
#define FA(x, y, z, sum, car) { v4 t_ = (x) ^ (y); sum = t_ ^ (z); car = ((x) & (y)) | ((z) & t_); }
static void step(int from, int to) {
  uint64_t (*s)[W] = S[from], (*d)[W] = S[to];
  for (int c = 0; c < N; c++) {
    const int *n = nb[c];
    v4 a0 = ld(s[n[0]]), a1 = ld(s[n[1]]), a2 = ld(s[n[2]]), a3 = ld(s[n[3]]), a4 = ld(s[n[4]]), a5 = ld(s[n[5]]);
    v4 a6 = ld(s[n[6]]), a7 = ld(s[n[7]]), a8 = ld(s[n[8]]), a9 = ld(s[n[9]]), a10 = ld(s[n[10]]), a11 = ld(s[n[11]]);
    v4 s1, c1, s2, c2, s3, c3, s4, c4, t1, d1, u1, e1, u2, e2, b2, b3;
    FA(a0, a1, a2, s1, c1) FA(a3, a4, a5, s2, c2) FA(a6, a7, a8, s3, c3) FA(a9, a10, a11, s4, c4)
    FA(s1, s2, s3, t1, d1)
    v4 b0 = t1 ^ s4, d2 = t1 & s4;
    FA(c1, c2, c3, u1, e1) FA(c4, d1, d2, u2, e2)
    v4 b1 = u1 ^ u2, e3 = u1 & u2;
    FA(e1, e2, e3, b2, b3)
    v4 x = ld(s[c]);
    v4 nx = ~b3 & ((b2 & ~b1) | (x & ~b2 & b1 & b0));   // n in {4,5}, or alive and n == 3
    memcpy(d[c], &nx, 32);
  }
}

static inline void setbit(int h, int c, int l, int b) {
  uint64_t m = 1ULL << (l & 63);
  if (b) S[h][c][l >> 6] |= m; else S[h][c][l >> 6] &= ~m;
}
static void soup(int h, int l) { for (int c = 0; c < N; c++) setbit(h, c, l, urand() < 0.35); }
static void extract(int h, int l, uint64_t *cfg) {
  memset(cfg, 0, nw * 8);
  for (int c = 0; c < N; c++) if ((S[h][c][l >> 6] >> (l & 63)) & 1) cfg[c >> 6] |= 1ULL << (c & 63);
}

int main(int argc, char **argv) {
  if (argc < 7) { fprintf(stderr, "usage\n"); return 1; }
  TH = atoi(argv[2]); TK = atoi(argv[3]); TD = atoi(argv[4]); long seed = atol(argv[5]);
  if (TH > 64 || TD > 64) return 1;
  if (!strcmp(argv[1], "val")) {
    int gens = atoi(argv[6]), neg = argc > 7 ? atoi(argv[7]) : 0;
    build(neg); seedrng(seed);
    printf("%d %d %d %d\n", N, TH, TK, TD);
    for (int c = 0; c < N; c++) printf("%d %d %d\n", cx[c], cy[c], cz[c]);
    for (int l = 0; l < NL; l++) soup(0, l);
    int lanes[3] = {0, 97, 255}, cur = 0; uint64_t cfg[(MAXC + 63) / 64];
    for (int g = 0; g <= gens; g++) {
      for (int i = 0; i < 3; i++) {
        extract(cur, lanes[i], cfg);
        printf("%d %d ", g, lanes[i]); for (int k = 0; k < nw; k++) printf("%016llx", (unsigned long long)cfg[k]); printf("\n");
      }
      int nx = (cur + 1) % KH; step(cur, nx); cur = nx;
    }
    return 0;
  }
  // nu: plain running, both faces; first passages of every level from above lamA; split by a preceding over-full generation
  long G = atol(argv[6]); int lamA = atoi(argv[7]);
  build(0); seedrng(seed * 104729 + 31 * TH + 7 * TK + TD);
  static int age[NL], fl[NL][2], cm[NL][2], P2[NL][2], since[NL][2];
  static long Dn[400], Db[400]; long expo = 0, deaths = 0, nP = 0, fdead = 0, nover = 0; double sP = 0, sP2 = 0;
  for (int l = 0; l < NL; l++) { soup(0, l); age[l] = 0; for (int f = 0; f < 2; f++) { fl[l][f] = 0; cm[l][f] = lamA; since[l][f] = 99; } }
  int cur = 0; clock_t t0 = clock();
  for (long g = 1; g <= G; g++) {
    int nx = (cur + 1) % KH; step(cur, nx); cur = nx;
    for (int f = 0; f < 2; f++) {
      v4 cnt[8]; for (int b = 0; b < 8; b++) cnt[b] = (v4){0, 0, 0, 0};
      for (int i = 0; i < nf[f]; i++) { v4 x = ld(S[cur][fc[f][i]]); for (int b = 0; b < 8; b++) { v4 t = cnt[b] & x; cnt[b] ^= x; x = t; } }
      uint64_t pl[8][W]; for (int b = 0; b < 8; b++) memcpy(pl[b], &cnt[b], 32);
      for (int l = 0; l < NL; l++) { int p = 0; for (int b = 0; b < 8; b++) p |= (int)((pl[b][l >> 6] >> (l & 63)) & 1) << b; P2[l][f] = p; }
    }
    for (int l = 0; l < NL; l++) {
      age[l]++;
      int counted = age[l] > 200, anye = (P2[l][0] == 0 || P2[l][1] == 0);
      if (counted) { expo++; for (int f = 0; f < 2; f++) { int p = P2[l][f]; sP += p; sP2 += (double)p * p; nP++; if (10 * p >= 7 * A) nover++; } }
      if (anye) {
        if (counted) { deaths++; for (int f = 0; f < 2; f++) if (P2[l][f] == 0) { fdead++; if (fl[l][f]) { Dn[0]++; Dn[cm[l][f]]--; if (since[l][f] <= 3) { Db[0]++; Db[cm[l][f]]--; } } } }
        soup(cur, l); age[l] = 0; for (int f = 0; f < 2; f++) { fl[l][f] = 0; cm[l][f] = lamA; since[l][f] = 99; }
      } else {
        for (int f = 0; f < 2; f++) {
          int p = P2[l][f];
          if (age[l] >= 100) {
            if (p >= lamA) { fl[l][f] = 1; cm[l][f] = lamA; }
            else if (fl[l][f] && p < cm[l][f]) { if (counted) { Dn[p]++; Dn[cm[l][f]]--; if (since[l][f] <= 3) { Db[p]++; Db[cm[l][f]]--; } } cm[l][f] = p; }
          }
          if (10 * p >= 7 * A) since[l][f] = 0; else if (since[l][f] < 99) since[l][f]++;
        }
      }
    }
  }
  printf("NU T %d,%d,%d seed %ld A %d lamA %d gens %ld expo %ld deaths %ld fdead %ld nover %ld sumP %.1f sumP2 %.1f nP %ld sec %.1f cross", TH, TK, TD, seed, A, lamA, G, expo, deaths, fdead, nover, sP, sP2, nP,
         (double)(clock() - t0) / CLOCKS_PER_SEC);
  long c = 0; for (int L = 0; L < lamA; L++) { c += Dn[L]; printf(" %ld", c); }
  printf(" bust"); c = 0; for (int L = 0; L < lamA; L++) { c += Db[L]; printf(" %ld", c); }
  printf("\n");
  return 0;
}
