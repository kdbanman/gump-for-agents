/* sweep.c -- exact quasi-stationary death rate of the one-layer model (face on coins), by power iteration with
 * the kernel applied triple by triple (no sampling, no stored matrix).
 *
 * The kernel is a product over triples: p'(y) = sum_x p(x) prod_c P_c(y_c | x). A working tensor over binary
 * variables (old cell values still needed, new cell values already made) is swept through the triples in order.
 * The plan (which bits are what at each step) is made by sweep.py and read from a file:
 *
 *   n0 nsteps
 *   per step: nin keepmask nkept m  sX mX sY mY sZ mZ      (s* = bit position of the cell's old value or -1,
 *                                                           m* = mask of its in-face neighbours' old values)
 *             followed by 2744 * 2^m doubles: outcome probabilities for (sX,kX,sY,kY,sZ,kZ)
 * The output variables of a step are the kept input variables in their order, then the m new values on top.
 *
 * usage: sweep PLAN TOL MAXIT [OUTVEC]      prints h and ln tau per iteration; final line "RESULT h lntau its"
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <immintrin.h>
typedef uint64_t u64;
typedef struct { int nin, nkept, m, s[3]; u64 keep, mk[3]; double *T; } step_t;

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: sweep PLAN TOL MAXIT [OUTVEC]\n"); return 1; }
  FILE *f = fopen(argv[1], "rb"); double tol = atof(argv[2]); int maxit = atoi(argv[3]);
  int n0, ns; if (fscanf(f, "%d %d", &n0, &ns) != 2) return 1;
  step_t *st = calloc(ns, sizeof(step_t)); int nmax = n0;
  for (int i = 0; i < ns; i++) { step_t *q = st + i; long long keep, a, b, c;
    if (fscanf(f, "%d %lld %d %d %d %lld %d %lld %d %lld", &q->nin, &keep, &q->nkept, &q->m, &q->s[0], &a, &q->s[1], &b, &q->s[2], &c) != 10) return 1;
    q->keep = keep; q->mk[0] = a; q->mk[1] = b; q->mk[2] = c;
    int no = 1 << q->m; q->T = malloc(sizeof(double) * 2744 * no);
    for (int k = 0; k < 2744 * no; k++) if (fscanf(f, "%lf", q->T + k) != 1) return 1;
    if (q->nin > nmax) nmax = q->nin; if (q->nkept + q->m > nmax) nmax = q->nkept + q->m; }
  fclose(f);
  u64 N0 = 1ULL << n0, NM = 1ULL << nmax;
  double *A = malloc(sizeof(double) * NM), *B = malloc(sizeof(double) * NM), *p = malloc(sizeof(double) * N0);
  if (!A || !B || !p) { fprintf(stderr, "out of memory (2^%d doubles x 2)\n", nmax); return 1; }
  for (u64 i = 0; i < N0; i++) p[i] = 1.0 / (double)(N0 - 1); p[0] = 0;
  double h = 0, hold = -1; int it;
  for (it = 0; it < maxit; it++) {
    memcpy(A, p, sizeof(double) * N0);
    for (int i = 0; i < ns; i++) { step_t *q = st + i; u64 nin = 1ULL << q->nin; int no = 1 << q->m;
      memset(B, 0, sizeof(double) * (1ULL << (q->nkept + q->m)));
      for (u64 x = 0; x < nin; x++) { double w = A[x]; if (w == 0) continue;
        int idx = 0;
        for (int j = 0; j < 3; j++) { int s = q->s[j] < 0 ? 0 : (int)((x >> q->s[j]) & 1); int k = __builtin_popcountll(x & q->mk[j]);
          idx = idx * 14 + s * 7 + k; }
        const double *t = q->T + (size_t)idx * no; u64 base = _pext_u64(x, q->keep);
        for (int o = 0; o < no; o++) B[base | ((u64)o << q->nkept)] += w * t[o];
      }
      double *tmp = A; A = B; B = tmp; }
    h = A[0]; double sum = 0; for (u64 i = 1; i < N0; i++) sum += A[i];
    p[0] = 0; for (u64 i = 1; i < N0; i++) p[i] = A[i] / sum;
    printf("it %d h %.12g lntau %.8f mass %.12f\n", it, h, -log(h), sum + h); fflush(stdout);
    if (fabs(h - hold) < tol * h) break;
    hold = h;
  }
  printf("RESULT %.12g %.8f %d\n", h, -log(h), it);
  if (argc > 4) { FILE *o = fopen(argv[4], "wb"); fwrite(p, sizeof(double), N0, o); fclose(o); }
  return 0;
}
