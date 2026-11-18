/* ex1d.c -- the one-row dice surrogate of cross2 B34/S234, solved exactly on a RING or an OPEN SEGMENT of L cells.
 * Model (the swarm's D2, research/theory/exponent/exact1d.c): a row eta in {0,1}^L; every generation each cell
 * draws two private coins (density rho each: the two cells beneath it) and applies the rule with
 * n = k + coins, k = live cells among x-2, x-1, x+1, x+2 (ring: cyclic; segment: cells outside are dead):
 * alive next iff n + eta >= 3 and n <= 4.  The empty row is absorbing.
 * Power iteration on the killed kernel, applied site by site IN PLACE on 2^(L+4) (ring) or 2^(L+2) (segment)
 * numbers.  h = flux into the empty row under the quasi-stationary law mu (computed as a flux, so its relative
 * precision is the iteration's), tau = 1/h.
 *   ex1d L ring(1|0) rho [Kmax=0]
 * prints ln tau, pn (law of the population under mu), the death flux by the population of the last living
 * generation, and for K = 1..Kmax the exact share B_K of the death flux whose last K steps (the fatal step
 * included) contain a one-generation fall of the population of at least L/2, and the share of living windows of
 * K - 1 transitions (under mu, conditioned to survive) that contain one. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
typedef uint64_t u64;
static int L, ring; static u64 S, SF; static double q[2][5], *A;
static void apply(const double *vin, double *vout) {
  memset(A, 0, SF * 8);
  for (u64 s = 1; s < S; s++) { double a = vin[s]; if (a == 0) continue; u64 w = s;
    if (ring) w |= ((s >> (L - 1)) & 1) << L | ((s >> (L - 2)) & 1) << (L + 1) | (s & 1) << (L + 2) | ((s >> 1) & 1) << (L + 3);
    A[w] = a; }
  for (int x = 0; x < L; x++) {
    int i1 = x + 1 < L ? x + 1 : (ring ? L + 2 + (x + 1 - L) : -1), i2 = x + 2 < L ? x + 2 : (ring ? L + 2 + (x + 2 - L) : -1);
    u64 bx = 1ULL << x, b1 = 1ULL << L, b2 = 1ULL << (L + 1), nlo = 1ULL << x, nmid = 1ULL << (L - 1 - x), ntop = SF >> (L + 2);
    for (u64 top = 0; top < ntop; top++) for (u64 mid = 0; mid < nmid; mid++) { u64 base = (mid << (x + 1)) | (top << (L + 2));
      int nn = (i1 >= 0 ? (int)((base >> i1) & 1) : 0) + (i2 >= 0 ? (int)((base >> i2) & 1) : 0);
      for (u64 lo = 0; lo < nlo; lo++) { u64 w = base | lo; double o[8];
        o[0] = A[w]; o[1] = A[w | bx]; o[2] = A[w | b1]; o[3] = A[w | bx | b1]; o[4] = A[w | b2]; o[5] = A[w | bx | b2]; o[6] = A[w | b1 | b2]; o[7] = A[w | bx | b1 | b2];
        for (int e = 0; e < 2; e++) for (int d1 = 0; d1 < 2; d1++) { double a0 = o[e + 2 * d1], a1 = o[e + 2 * d1 + 4];
          double on = a0 * q[e][nn + d1] + a1 * q[e][nn + d1 + 1], off = (a0 + a1) - on;
          u64 t = w | (e ? b1 : 0) | (d1 ? b2 : 0); A[t] = off; A[t | bx] = on; } } }
  }
  u64 F = SF >> L;
  for (u64 s = 0; s < S; s++) { double a = 0; for (u64 f = 0; f < F; f++) a += A[s | f << L]; vout[s] = a; }
}
static int nbk(u64 s, int x) { int k = 0; for (int d = -2; d <= 2; d++) { if (!d) continue; int y = x + d; if (ring) y = (y + L) % L; else if (y < 0 || y >= L) continue; k += (s >> y) & 1; } return k; }
int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: ex1d L ring rho [Kmax]\n"); return 2; }
  L = atoi(argv[1]); ring = atoi(argv[2]); double r = atof(argv[3]); int Kmax = argc > 4 ? atoi(argv[4]) : 0;
  double pb[3] = {(1 - r) * (1 - r), 2 * r * (1 - r), r * r};
  for (int e = 0; e < 2; e++) for (int k = 0; k < 5; k++) { q[e][k] = 0; for (int b = 0; b < 3; b++) { int n = k + b; if (n + e >= 3 && n <= 4) q[e][k] += pb[b]; } }
  S = 1ULL << L; SF = S << (ring ? 4 : 2);
  A = malloc(SF * 8); double *v = malloc(S * 8), *u = malloc(S * 8); if (!A || !v || !u) { fprintf(stderr, "memory\n"); return 3; }
  for (u64 s = 0; s < S; s++) v[s] = 1.0 / (double)(S - 1); v[0] = 0;
  double h = 0, hold = -1; int it;
  for (it = 0; it < 5000; it++) { apply(v, u); h = u[0]; double tot = 0; for (u64 s = 1; s < S; s++) tot += u[s];
    for (u64 s = 1; s < S; s++) v[s] = u[s] / tot; v[0] = 0;
    if (it > 20 && fabs(h - hold) < 1e-11 * h) break; hold = h; }
  double lam = 1 - h;
  printf("L %d ring %d rho %g iterations %d\nh %.12e\nlntau %.10f\n", L, ring, r, it, h, -log(h));
  double *pn = calloc(L + 1, 8), *fl = calloc(L + 1, 8), *d = malloc(S * 8), *dens = calloc(L, 8);
  for (u64 s = 1; s < S; s++) { double a = v[s]; int n = __builtin_popcountll(s); pn[n] += a;
    double dd = 1; for (int x = 0; x < L; x++) { dd *= 1 - q[(s >> x) & 1][nbk(s, x)]; if ((s >> x) & 1) dens[x] += a; } d[s] = dd; fl[n] += a * dd; }
  d[0] = 0;
  printf("pn"); for (int n = 0; n <= L; n++) printf(" %.10e", pn[n]); printf("\n");
  printf("deathflux"); for (int n = 0; n <= L; n++) printf(" %.10e", fl[n]); printf("\n");
  printf("density"); for (int x = 0; x < L; x++) printf(" %.6f", dens[x]); printf("\n");
  if (Kmax > 0) { int F = (L + 1) / 2; double *rr = malloc(S * 8), *tmp = malloc(S * 8), *out = malloc(S * 8);
    memcpy(u, v, S * 8); double lk = 1;
    for (int K = 1; K <= Kmax; K++) {
      double N = 0; for (u64 s = 1; s < S; s++) if (__builtin_popcountll(s) < F) N += u[s] * d[s];
      double tu = 0; for (u64 s = 1; s < S; s++) tu += u[s];   /* living windows of K - 1 transitions without such a fall */
      printf("bust K %d share %.8f living_window_Km1_transitions %.8f\n", K, 1 - N / (lk * h), 1 - tu / lk); fflush(stdout);
      if (K == Kmax) break;
      apply(u, rr);
      for (int n = F; n <= L; n++) { for (u64 s = 0; s < S; s++) tmp[s] = __builtin_popcountll(s) == n ? u[s] : 0;
        apply(tmp, out); for (u64 s = 1; s < S; s++) if (__builtin_popcountll(s) <= n - F) rr[s] -= out[s]; }
      for (u64 s = 1; s < S; s++) u[s] = rr[s] > 0 ? rr[s] : 0; u[0] = 0; lk *= lam; } }
  return 0;
}
