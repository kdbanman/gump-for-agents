/* exact1d.c -- the w = 1 driven-edge model solved exactly on a ring of L cells (L <= 24).
 *
 * Model: one row eta in {0,1}^L (periodic).  Each generation every cell x draws an independent b in {0,1,2}
 * (two Bernoulli(rho) cells "below", classes rho1 and rho2) and applies the toy's rule with n = k + b, k = number
 * of live cells among x-2, x-1, x+1, x+2:   alive next iff (n + eta >= 3 and n <= 4)   [cross2, B34/S234].
 * Given eta the cells update independently: P(eta'_x = 1) = q[eta_x][k_x].  The all-dead row is absorbing.
 *
 * Computes by power iteration on the killed kernel (distribution on the 2^L - 1 living rows) the quasi-stationary
 * distribution mu and the survival eigenvalue lambda; h = 1 - lambda is the exact death rate per generation,
 * tau = 1/h.  The kernel is applied site by site in O(L 2^(L+4)) (two delay bits and two wrap bits).
 *
 *   exact1d L rho1 rho2 [tol] [maxit]      prints lambda, h, ln tau, the distribution of n under mu, the death
 *                                          flux by n, and the emptiness formation probabilities under mu.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
typedef uint64_t u64;

static int L; static double q[2][5];

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: exact1d L rho1 rho2 [tol] [maxit]\n"); return 2; }
  L = atoi(argv[1]); double r1 = atof(argv[2]), r2 = atof(argv[3]);
  double tol = argc > 4 ? atof(argv[4]) : 1e-12; int maxit = argc > 5 ? atoi(argv[5]) : 5000;
  double pb[3] = {(1 - r1) * (1 - r2), r1 * (1 - r2) + r2 * (1 - r1), r1 * r2};
  for (int e = 0; e < 2; e++) for (int k = 0; k < 5; k++) { q[e][k] = 0;
    for (int b = 0; b < 3; b++) { int n = k + b; if (n + e >= 3 && n <= 4) q[e][k] += pb[b]; } }
  u64 S = 1ULL << L, S4 = S << 4;
  double *v = malloc(S * 8), *A = malloc(S4 * 8), *B = malloc(S4 * 8);
  if (!v || !A || !B) { fprintf(stderr, "memory\n"); return 3; }
  for (u64 s = 0; s < S; s++) v[s] = 1.0 / (double)(S - 1); v[0] = 0;
  double lam = 0, lamold = -1; int it;
  /* word layout: bits 0..L-1 main, bit L = d1 (old x-1), L+1 = d2 (old x-2), L+2 = s0 (old 0), L+3 = s1 (old 1) */
  for (it = 0; it < maxit; it++) {
    memset(A, 0, S4 * 8);
    for (u64 s = 1; s < S; s++) { u64 w = s | ((s >> (L - 1)) & 1) << L | ((s >> (L - 2)) & 1) << (L + 1) | (s & 1) << (L + 2) | ((s >> 1) & 1) << (L + 3); A[w] = v[s]; }
    for (int x = 0; x < L; x++) {
      memset(B, 0, S4 * 8);
      int i1 = x + 1 < L ? x + 1 : L + 2 + (x + 1 - L), i2 = x + 2 < L ? x + 2 : L + 2 + (x + 2 - L);
      for (u64 w = 0; w < S4; w++) { double a = A[w]; if (a == 0) continue;
        int e = (w >> x) & 1, d1 = (w >> L) & 1, d2 = (w >> (L + 1)) & 1;
        int k = d1 + d2 + (int)((w >> i1) & 1) + (int)((w >> i2) & 1);
        u64 t = (w & ~((1ULL << x) | (3ULL << L))) | ((u64)e << L) | ((u64)d1 << (L + 1));
        double p = q[e][k];
        B[t] += a * (1 - p); B[t | (1ULL << x)] += a * p; }
      double *T = A; A = B; B = T;
    }
    double tot = 0;
    for (u64 s = 0; s < S; s++) { double a = 0; for (int e = 0; e < 16; e++) a += A[s | ((u64)e << L)]; v[s] = a; }
    for (u64 s = 1; s < S; s++) tot += v[s];
    lam = tot; v[0] = 0; for (u64 s = 1; s < S; s++) v[s] /= tot;
    if (fabs(lam - lamold) < tol * (1 - lam) && it > 20) break;
    lamold = lam;
  }
  double h = 1 - lam;
  printf("L %d\nrho %g %g\niterations %d\nlambda %.15g\nh %.12e\nlntau %.10f\n", L, r1, r2, it, lam, h, -log(h));
  printf("q0"); for (int k = 0; k < 5; k++) printf(" %.6f", q[0][k]); printf("\nq1"); for (int k = 0; k < 5; k++) printf(" %.6f", q[1][k]); printf("\n");
  double *pn = calloc(L + 1, 8), *fl = calloc(L + 1, 8), *gap = calloc(L + 1, 8);
  for (u64 s = 1; s < S; s++) { double a = v[s]; int n = __builtin_popcountll(s); pn[n] += a;
    double d = 1; for (int x = 0; x < L && d > 0; x++) { int e = (s >> x) & 1;
      int k = (int)((s >> ((x + 1) % L)) & 1) + (int)((s >> ((x + 2) % L)) & 1) + (int)((s >> ((x + L - 1) % L)) & 1) + (int)((s >> ((x + L - 2) % L)) & 1);
      d *= 1 - q[e][k]; }
    fl[n] += a * d;
    /* longest run of zeros starting at cell 0: window [0, m) empty for all m <= z */
    int z = 0; while (z < L && !((s >> z) & 1)) z++; for (int m = 1; m <= z; m++) gap[m] += a; }
  printf("pn"); for (int n = 0; n <= L; n++) printf(" %.10e", pn[n]); printf("\n");
  printf("deathflux"); for (int n = 0; n <= L; n++) printf(" %.10e", fl[n]); printf("\n");
  printf("emptywindow"); for (int m = 0; m <= L; m++) printf(" %.10e", m ? gap[m] : 1.0); printf("\n");
  return 0;
}
