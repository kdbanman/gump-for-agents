/* exg.c -- ex1d.c generalised to any one-row capped-threshold dice surrogate: a row of L cells, in-row neighbours
 * within range R (2R of them), nc private coins of density rho beneath each cell, n = k + coins,
 * alive next iff (n + eta >= T) and (n <= C).   cross2 B34/S234: R 2, nc 2, T 3, C 4.
 * "gump's count on a line": R 3 (6 in-row neighbours, as a face cell has 6 in its plane), nc 3 (3 beneath),
 * T 5, C 5 (B45/S345), rho 0.4155.
 *   exg L ring(1|0) R nc T C rho [Kmax=0]        output as ex1d.c
 * Kernel applied site by site in place on 2^(L+2R) (ring) or 2^(L+R) (segment) numbers. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
typedef uint64_t u64;
static int L, ring, R; static u64 S, SF; static double q[2][16], *A;
static void apply(const double *vin, double *vout) {
  memset(A, 0, SF * 8);
  for (u64 s = 1; s < S; s++) { double a = vin[s]; if (a == 0) continue; u64 w = s;
    if (ring) for (int j = 1; j <= R; j++) { w |= ((s >> (L - j)) & 1) << (L + j - 1); w |= ((s >> (j - 1)) & 1) << (L + R + j - 1); }
    A[w] = a; }
  int G = 1 << (R - 1);
  for (int x = 0; x < L; x++) {
    int idx[8]; for (int j = 1; j <= R; j++) idx[j] = x + j < L ? x + j : (ring ? L + R + (x + j - L) : -1);
    u64 bx = 1ULL << x, nlo = 1ULL << x, nmid = 1ULL << (L - 1 - x), ntop = SF >> (L + R);
    for (u64 top = 0; top < ntop; top++) for (u64 mid = 0; mid < nmid; mid++) { u64 base = (mid << (x + 1)) | (top << (L + R));
      int nn = 0; for (int j = 1; j <= R; j++) if (idx[j] >= 0) nn += (base >> idx[j]) & 1;
      for (u64 lo = 0; lo < nlo; lo++) { u64 w = base | lo; double o[2][16];
        for (int e = 0; e < 2; e++) for (int D = 0; D < 2 * G; D++) o[e][D] = A[w | (e ? bx : 0) | ((u64)D << L)];
        for (int e = 0; e < 2; e++) for (int dl = 0; dl < G; dl++) { int k0 = nn + __builtin_popcount(dl);
          double a0 = o[e][dl], a1 = o[e][dl | G], on = a0 * q[e][k0] + a1 * q[e][k0 + 1], off = (a0 + a1) - on;
          u64 t = w | ((u64)(e | (dl << 1)) << L); A[t] = off; A[t | bx] = on; } } }
  }
  u64 F = SF >> L;
  for (u64 s = 0; s < S; s++) { double a = 0; for (u64 f = 0; f < F; f++) a += A[s | f << L]; vout[s] = a; }
}
static int nbk(u64 s, int x) { int k = 0; for (int d = -R; d <= R; d++) { if (!d) continue; int y = x + d; if (ring) y = (y + L) % L; else if (y < 0 || y >= L) continue; k += (s >> y) & 1; } return k; }
int main(int argc, char **argv) {
  if (argc < 8) { fprintf(stderr, "usage: exg L ring R nc T C rho [Kmax]\n"); return 2; }
  L = atoi(argv[1]); ring = atoi(argv[2]); R = atoi(argv[3]); int nc = atoi(argv[4]), T = atoi(argv[5]), C = atoi(argv[6]); double r = atof(argv[7]); int Kmax = argc > 8 ? atoi(argv[8]) : 0;
  double pb[8]; for (int b = 0; b <= nc; b++) { double c = 1; for (int i = 0; i < b; i++) c = c * (nc - i) / (i + 1); pb[b] = c * pow(r, b) * pow(1 - r, nc - b); }
  for (int e = 0; e < 2; e++) for (int k = 0; k <= 2 * R; k++) { q[e][k] = 0; for (int b = 0; b <= nc; b++) { int n = k + b; if (n + e >= T && n <= C) q[e][k] += pb[b]; } }
  S = 1ULL << L; SF = S << (ring ? 2 * R : R);
  A = malloc(SF * 8); double *v = malloc(S * 8), *u = malloc(S * 8); if (!A || !v || !u) { fprintf(stderr, "memory\n"); return 3; }
  for (u64 s = 0; s < S; s++) v[s] = 1.0 / (double)(S - 1); v[0] = 0;
  double h = 0, hold = -1; int it;
  for (it = 0; it < 5000; it++) { apply(v, u); h = u[0]; double tot = 0; for (u64 s = 1; s < S; s++) tot += u[s];
    for (u64 s = 1; s < S; s++) v[s] = u[s] / tot; v[0] = 0;
    if (it > 20 && fabs(h - hold) < 1e-11 * h) break; hold = h; }
  double lam = 1 - h;
  printf("L %d ring %d R %d nc %d T %d C %d rho %g iterations %d\nh %.12e\nlntau %.10f\n", L, ring, R, nc, T, C, r, it, h, -log(h));
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
      double tu = 0; for (u64 s = 1; s < S; s++) tu += u[s];
      printf("bust K %d share %.8f living_window_Km1_transitions %.8f\n", K, 1 - N / (lk * h), 1 - tu / lk); fflush(stdout);
      if (K == Kmax) break;
      apply(u, rr);
      for (int n = F; n <= L; n++) { for (u64 s = 0; s < S; s++) tmp[s] = __builtin_popcountll(s) == n ? u[s] : 0;
        apply(tmp, out); for (u64 s = 1; s < S; s++) if (__builtin_popcountll(s) <= n - F) rr[s] -= out[s]; }
      for (u64 s = 1; s < S; s++) u[s] = rr[s] > 0 ? rr[s] : 0; u[0] = 0; lk *= lam; } }
  return 0;
}
