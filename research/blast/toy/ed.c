/* ed.c -- cross2 B34/S234 ("alive next iff n + x >= 3 except n >= 5 dies"), one replica, one machine word per row.
 * Vessel: W rows of L <= 64 cells, dead outside; per = 1: periodic along the row (a strip, whose two edge rows are
 * RINGS of L cells); per = 0: open (W = L: a box, four edges with ends at corners).
 *   ed trace W L per seed gens [initfile]     print every generation (hex rows) for validation
 *   ed run W L per seed deaths maxgens recfile [T0=300] [samp=997]
 * run: soup p = 0.4, states younger than T0 not measured, events end a residence and reseed: an edge row empty
 * (a death; recorded with the last H = 16 generations of that row), strips only: 3 dead interior rows, 3 dead
 * columns right across; a settled state (equal to a snapshot taken every 64 or every 4096 generations: any period <= 4096).
 * tau_edge = nE * exposure / deaths.  Living windows of edge 0 are sampled every samp generations ("V" records). */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
typedef uint64_t u64;
#define H 16
static int W, L, per; static u64 M, rs;
static inline u64 rnd(void){ u64 z = (rs += 0x9E3779B97F4A7C15ULL); z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL; z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL; return z ^ (z >> 31); }
static void step(const u64 *a, u64 *b) {
  for (int y = 0; y < W; y++) {
    u64 r = a[y], in[8];
    if (per) { in[0] = ((r << 1) | (r >> (L - 1))) & M; in[1] = ((r << 2) | (r >> (L - 2))) & M; in[2] = ((r >> 1) | (r << (L - 1))) & M; in[3] = ((r >> 2) | (r << (L - 2))) & M; }
    else { in[0] = (r << 1) & M; in[1] = (r << 2) & M; in[2] = r >> 1; in[3] = r >> 2; }
    in[4] = y >= 1 ? a[y - 1] : 0; in[5] = y >= 2 ? a[y - 2] : 0; in[6] = y + 1 < W ? a[y + 1] : 0; in[7] = y + 2 < W ? a[y + 2] : 0;
    u64 c0 = 0, c1 = 0, c2 = 0, c3 = 0;
    for (int k = 0; k < 8; k++) { u64 x = in[k], t0 = c0 & x; c0 ^= x; u64 t1 = c1 & t0; c1 ^= t0; u64 t2 = c2 & t1; c2 ^= t1; c3 |= t2; }
    u64 n2 = ~c3 & ~c2 & c1 & ~c0, n3 = ~c3 & ~c2 & c1 & c0, n4 = ~c3 & c2 & ~c1 & ~c0;
    b[y] = (n3 | n4 | (r & n2)) & M;
  }
}
static void soup(u64 *a) { for (int y = 0; y < W; y++) { u64 r = 0; for (int x = 0; x < L; x++) if ((rnd() >> 11) * (1.0 / 9007199254740992.0) < 0.4) r |= 1ULL << x; a[y] = r; } }
static int nE;
static void edges(const u64 *a, u64 *e) { e[0] = a[0]; e[1] = a[W - 1];
  if (!per) { u64 c0 = 0, c1 = 0; for (int y = 0; y < W; y++) { c0 |= (a[y] & 1) << y; c1 |= ((a[y] >> (L - 1)) & 1) << y; } e[2] = c0; e[3] = c1; } }
int main(int argc, char **argv) {
  if (argc < 7) { fprintf(stderr, "usage\n"); return 2; }
  W = atoi(argv[2]); L = atoi(argv[3]); per = atoi(argv[4]); rs = strtoull(argv[5], 0, 10) * 0x2545F4914F6CDD1DULL + 12345;
  M = L == 64 ? ~0ULL : (1ULL << L) - 1; nE = per ? 2 : 4;
  u64 buf[3][64]; u64 *a = buf[0], *b = buf[1], *c = buf[2];
  if (!strcmp(argv[1], "trace")) { int gens = atoi(argv[6]); soup(a);
    if (argc > 7) { FILE *f = fopen(argv[7], "r"); for (int y = 0; y < W; y++) if (fscanf(f, "%llx", (unsigned long long *)&a[y]) != 1) return 3; fclose(f); }
    for (int t = 0; t <= gens; t++) { for (int y = 0; y < W; y++) printf("%llx%c", (unsigned long long)a[y], y == W - 1 ? '\n' : ' '); step(a, b); u64 *T = a; a = b; b = T; }
    return 0; }
  long want = atol(argv[6]); double maxg = atof(argv[7]); FILE *rec = fopen(argv[8], "w");
  int T0 = argc > 9 ? atoi(argv[9]) : 300; long samp = argc > 10 ? atol(argv[10]) : 997;
  double expo = 0, gens = 0; long deaths = 0, dedges = 0, nfw = 0, ncut = 0, nset = 0, nyoung = 0, nV = 0;
  double *hist = calloc(L + 1, 8), *tr = calloc((L + 1) * (L + 1), 8);
  u64 hb[4][H], e[4], ep[4], s1[64], s2[64]; long age = 0; memset(s1, 0, sizeof s1); memset(s2, 0, sizeof s2); soup(a); edges(a, ep); memset(hb, 0, sizeof hb);
  while (deaths < want && gens < maxg) {
    step(a, b); { u64 *T = c; c = a; a = b; b = T; }   /* a = now, c = one generation ago, b = two ago */
    age++; gens++; edges(a, e);
    int ev = 0, dead = 0;
    for (int k = 0; k < nE; k++) if (!e[k]) dead |= 1 << k;
    if (dead) { ev = 1;
      if (age > T0) { deaths++; for (int k = 0; k < nE; k++) if (dead >> k & 1) { dedges++; fprintf(rec, "D %d", k);
            for (int j = H; j >= 1; j--) fprintf(rec, " %llx", (unsigned long long)hb[k][(age - j) % H]); fprintf(rec, "\n"); } }
      else nyoung++; }
    else if (per) { u64 co = 0; for (int y = 0; y < W; y++) co |= a[y];
      u64 z = ~co & M, z1 = ((z << 1) | (z >> (L - 1))) & M, z2 = ((z << 2) | (z >> (L - 2))) & M;
      if (z & z1 & z2) { ev = 1; ncut++; }
      else for (int y = 1; y + 3 <= W - 1; y++) if (!(a[y] | a[y + 1] | a[y + 2])) { ev = 1; nfw++; break; } }
    if (!ev) { /* settled: equal to a snapshot taken every 64 / every 4096 generations (any period <= 4096) */
      if (age > 1 && !memcmp(a, s1, W * 8)) { ev = 1; nset++; } else if (age > 1 && !memcmp(a, s2, W * 8)) { ev = 1; nset++; }
      if ((age & 63) == 0) memcpy(s1, a, W * 8); if ((age & 4095) == 0) memcpy(s2, a, W * 8); }
    if (ev) { soup(a); edges(a, ep); age = 0; memset(s1, 0, sizeof s1); memset(s2, 0, sizeof s2); continue; }
    if (age > T0) { expo++;
      for (int k = 0; k < nE; k++) { int p = __builtin_popcountll(e[k]), q = __builtin_popcountll(ep[k]); hist[p]++; tr[q * (L + 1) + p]++; }
      if (age > T0 + H && ((long)gens % samp) == 0) { nV++; fprintf(rec, "V 0"); for (int j = H - 1; j >= 1; j--) fprintf(rec, " %llx", (unsigned long long)hb[0][(age - j) % H]); fprintf(rec, " %llx\n", (unsigned long long)e[0]); } }
    for (int k = 0; k < nE; k++) { hb[k][age % H] = e[k]; ep[k] = e[k]; }
  }
  fclose(rec);
  double tau = nE * expo / (deaths ? deaths : 1);
  printf("W %d L %d per %d nE %d T0 %d\ngens %.0f exposure %.0f deaths %ld dead_edges %ld firewalls %ld cuts %ld settles %ld young %ld living_windows %ld\n", W, L, per, nE, T0, gens, expo, deaths, dedges, nfw, ncut, nset, nyoung, nV);
  printf("tau_edge %.6g lntau %.4f err %.4f\n", tau, log(tau), 1 / sqrt(deaths ? deaths : 1));
  printf("hist"); for (int p = 0; p <= L; p++) printf(" %.0f", hist[p]); printf("\n");
  for (int q = 0; q <= L; q++) { printf("tr %d", q); for (int p = 0; p <= L; p++) printf(" %.0f", tr[q * (L + 1) + p]); printf("\n"); }
  return 0;
}
