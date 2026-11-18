/* qsd.c: exact quasi-stationary law and extinction rate of the one-layer dice surrogate of a gump face.

   Chain.  State x in {0,1}^A.  One generation: every cell i draws b_i = Bin(m1_i, rho1) + Bin(m2_i, rho2),
   independently of everything; with k_i = number of live in-layer neighbours (counted with multiplicity),
   n = k_i + b_i:  a dead cell is born iff n in {4,5}, a live cell survives iff n in {3,4,5}  (B45/S345).
   All cells update at once (synchronously).  The empty face is absorbing.

   Method.  The kernel is P(x,x') = prod_i q_i(x'_i | x_i, k_i(x)).  The product v -> vP is carried out one cell
   at a time on an array indexed by the "old" bits still needed and the "new" bits already produced (a transfer
   product): cell c adds the bit new_c with weight q_c(new_c | old), and an old bit is summed out as soon as every
   cell that reads it has been processed.  No dense matrix.  Memory 2^(peak bits) doubles.
   Power iteration on the chain killed at the empty face: v <- vP restricted to non-empty states, normalised.
   h = (vP)(empty) / |v| converges to 1 - lambda; from the quasi-stationary law the death time is exactly
   geometric with mean tau = 1/h.

   usage: qsd graph rho1 rho2 [maxiter=4000] [tol=1e-13] [verbose 0/1] [tilt]
   graph: A; then per cell "m1 m2 deg n1..ndeg"; then an elimination order (see geom.py).
   build: gcc -O3 -march=native -o qsd qsd.c -lm                                                    */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>

#define MAXA 40
static int A, m1[MAXA], m2[MAXA], deg[MAXA], nb[MAXA][12], order[MAXA];
static double q[MAXA][2][8];           /* q[i][x][k] = P(alive next | state x, k live in-layer neighbours) */
static double rho1, rho2;

static void make_q(void) {
    for (int i = 0; i < A; i++) {
        double pb[4] = {0, 0, 0, 0};
        for (int c1 = 0; c1 <= m1[i]; c1++)
            for (int c2 = 0; c2 <= m2[i]; c2++) {
                double p = 1;
                /* binomial weights */
                double bin1 = 1, bin2 = 1;
                if (m1[i] == 2) bin1 = (c1 == 1) ? 2 : 1;
                if (m1[i] == 1 || m1[i] == 0) bin1 = 1;
                p *= bin1 * pow(rho1, c1) * pow(1 - rho1, m1[i] - c1);
                p *= bin2 * pow(rho2, c2) * pow(1 - rho2, m2[i] - c2);
                pb[c1 + c2] += p;
            }
        for (int x = 0; x < 2; x++)
            for (int k = 0; k < 8; k++) {
                double s = 0;
                for (int b = 0; b < 4; b++) {
                    int n = k + b;
                    int alive = x ? (n >= 3 && n <= 5) : (n == 4 || n == 5);
                    if (alive) s += pb[b];
                }
                q[i][x][k] = s;
            }
    }
}

/* variable bookkeeping */
static int posold[MAXA], posnew[MAXA];     /* bit position of old_i / new_i, -1 if absent */
static int at_kind[64], at_id[64];         /* what sits at each bit: kind 0 old, 1 new */
static int nbits;
static uint64_t depmask[MAXA];             /* cells that read old_i (as a set of cells) */
static double *T;

static void sum_out(int p) {               /* sum out the variable at bit p, move the top variable into p */
    uint64_t N = 1ULL << nbits, bp = 1ULL << p;
    for (uint64_t s = 0; s < N; s++) if (!(s & bp)) T[s] += T[s | bp];
    int top = nbits - 1;
    if (p != top) {
        uint64_t bt = 1ULL << top;
        for (uint64_t s = 0; s < bt; s++) if (s & bp) T[s] = T[(s ^ bp) | bt];
        at_kind[p] = at_kind[top]; at_id[p] = at_id[top];
        if (at_kind[p] == 0) posold[at_id[p]] = p; else posnew[at_id[p]] = p;
    }
    nbits--;
}

/* one product v -> vP.  On entry T holds v with old_i at bit posold[i] (A bits).  On exit T holds vP with
   new_i at bit posnew[i]; then posold := posnew. */
static void matvec(void) {
    uint64_t done = 0;
    for (int i = 0; i < A; i++) posnew[i] = -1;
    for (int t = 0; t < A; t++) {
        int c = order[t];
        uint64_t M[4] = {0, 0, 0, 0};          /* M[w]: bits of neighbours of multiplicity w */
        int mult[MAXA]; memset(mult, 0, sizeof mult);
        for (int j = 0; j < deg[c]; j++) mult[nb[c][j]]++;
        for (int i = 0; i < A; i++) if (mult[i]) {
            if (mult[i] > 3 || posold[i] < 0) { fprintf(stderr, "plan error\n"); exit(1); }
            M[mult[i]] |= 1ULL << posold[i];
        }
        uint64_t self = 1ULL << posold[c];
        const double *q0 = q[c][0], *q1 = q[c][1];
        done |= 1ULL << c;
        int freed[MAXA], nf = 0;
        for (int i = 0; i < A; i++) if (posold[i] >= 0 && (depmask[i] & ~done) == 0) freed[nf++] = i;
        uint64_t N = 1ULL << nbits;
#define KOF(s) (__builtin_popcountll((s) & M[1]) + 2 * __builtin_popcountll((s) & M[2]) + 3 * __builtin_popcountll((s) & M[3]))
        if (nf > 0) {                          /* new_c takes the place of the first freed old variable */
            int p = posold[freed[0]]; uint64_t bp = 1ULL << p;
            for (uint64_t s = 0; s < N; s++) if (!(s & bp)) {
                uint64_t s1 = s | bp;
                double a0 = ((s & self) ? q1 : q0)[KOF(s)], a1 = ((s1 & self) ? q1 : q0)[KOF(s1)];
                double t0 = T[s], t1 = T[s1];
                T[s] = t0 * (1 - a0) + t1 * (1 - a1);
                T[s1] = t0 * a0 + t1 * a1;
            }
            posold[freed[0]] = -1; posnew[c] = p; at_kind[p] = 1; at_id[p] = c;
            for (int f = 1; f < nf; f++) { int pf = posold[freed[f]]; posold[freed[f]] = -1; sum_out(pf); }
        } else {                               /* new_c becomes a new top bit */
            for (uint64_t s = 0; s < N; s++) {
                double a = ((s & self) ? q1 : q0)[KOF(s)];
                double t0 = T[s];
                T[s | N] = t0 * a; T[s] = t0 * (1 - a);
            }
            posnew[c] = nbits; at_kind[nbits] = 1; at_id[nbits] = c; nbits++;
        }
    }
    if (nbits != A) { fprintf(stderr, "plan error: %d bits left\n", nbits); exit(1); }
    for (int i = 0; i < A; i++) { posold[i] = posnew[i]; at_kind[posold[i]] = 0; at_id[posold[i]] = i; }
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: qsd graph rho1 rho2 [maxiter] [tol] [quiet]\n"); return 1; }
    FILE *f = fopen(argv[1], "r");
    if (!f || fscanf(f, "%d", &A) != 1 || A > MAXA) { fprintf(stderr, "bad graph\n"); return 1; }
    for (int i = 0; i < A; i++) {
        if (fscanf(f, "%d %d %d", &m1[i], &m2[i], &deg[i]) != 3) return 1;
        for (int j = 0; j < deg[i]; j++) if (fscanf(f, "%d", &nb[i][j]) != 1) return 1;
    }
    for (int i = 0; i < A; i++) if (fscanf(f, "%d", &order[i]) != 1) return 1;
    fclose(f);
    rho1 = atof(argv[2]); rho2 = atof(argv[3]);
    int maxiter = argc > 4 ? atoi(argv[4]) : 4000;
    double tol = argc > 5 ? atof(argv[5]) : 1e-13;
    make_q();
    for (int i = 0; i < A; i++) depmask[i] = 1ULL << i;
    for (int c = 0; c < A; c++) for (int j = 0; j < deg[c]; j++) depmask[nb[c][j]] |= 1ULL << c;
    /* peak bits for this order */
    int peak = A;
    { uint64_t done = 0, gone = 0; int n = A;
      for (int t = 0; t < A; t++) { done |= 1ULL << order[t]; int nf = 0;
        for (int i = 0; i < A; i++) if (!(gone >> i & 1) && (depmask[i] & ~done) == 0) { gone |= 1ULL << i; nf++; }
        if (nf) n -= nf - 1; else { n++; if (n > peak) peak = n; } } }
    T = malloc(sizeof(double) << peak);
    if (!T) { fprintf(stderr, "no memory for %d bits\n", peak); return 1; }
    uint64_t NA = 1ULL << A;
    for (int i = 0; i < A; i++) { posold[i] = i; at_kind[i] = 0; at_id[i] = i; }
    nbits = A;
    for (uint64_t s = 0; s < NA; s++) T[s] = 1.0;
    T[0] = 0;
    { double z = (double)(NA - 1); for (uint64_t s = 1; s < NA; s++) T[s] /= z; }
    double h = 0, hprev = -1; int good = 0, it;
    for (it = 1; it <= maxiter; it++) {
        matvec();
        h = T[0]; T[0] = 0;
        double z = 0;
        for (uint64_t s = 1; s < NA; s++) z += T[s];
        for (uint64_t s = 1; s < NA; s++) T[s] /= z;
        /* mass is conserved by the product: h + z = 1 up to rounding */
        if (fabs(h + z - 1) > 1e-9) { fprintf(stderr, "mass not conserved: %g\n", h + z - 1); return 1; }
        if (hprev > 0 && fabs(h - hprev) <= tol * h) good++; else good = 0;
        if (argc > 6 && atoi(argv[6]) && it % 20 == 0) fprintf(stderr, "it %d h %.15g\n", it, h);
        hprev = h;
        if (good >= 8) break;
    }
    /* statistics of the quasi-stationary law mu = T */
    double pn[MAXA + 1], hn[MAXA + 1], occ[MAXA], docc[MAXA], mean = 0, var = 0, hsum = 0;
    memset(pn, 0, sizeof pn); memset(hn, 0, sizeof hn); memset(occ, 0, sizeof occ); memset(docc, 0, sizeof docc);
    uint64_t nbm[MAXA][4];
    for (int c = 0; c < A; c++) { int mult[MAXA]; memset(mult, 0, sizeof mult);
        for (int w = 0; w < 4; w++) nbm[c][w] = 0;
        for (int j = 0; j < deg[c]; j++) mult[nb[c][j]]++;
        for (int i = 0; i < A; i++) if (mult[i]) nbm[c][mult[i]] |= 1ULL << posold[i]; }
    for (uint64_t s = 1; s < NA; s++) {
        double v = T[s]; int n = __builtin_popcountll(s);
        pn[n] += v;
        double d = 1;
        for (int c = 0; c < A && d > 0; c++) {
            int k = __builtin_popcountll(s & nbm[c][1]) + 2 * __builtin_popcountll(s & nbm[c][2]) + 3 * __builtin_popcountll(s & nbm[c][3]);
            d *= 1 - q[c][(s >> posold[c]) & 1][k];
        }
        hn[n] += v * d; hsum += v * d;
        for (int c = 0; c < A; c++) if ((s >> posold[c]) & 1) { occ[c] += v; docc[c] += v * d; }
    }
    for (int n = 1; n <= A; n++) { mean += n * pn[n]; }
    for (int n = 1; n <= A; n++) { var += (n - mean) * (n - mean) * pn[n]; }
    printf("A %d peakbits %d iterations %d rho1 %.6f rho2 %.6f\n", A, peak, it, rho1, rho2);
    printf("h %.13e  check_h %.13e  lntau %.12f\n", h, hsum, -log(h));
    printf("density %.12f  var_per_cell %.12f\n", mean / A, var / A);
    printf("pn"); for (int n = 1; n <= A; n++) printf(" %.6e", pn[n]); printf("\n");
    printf("death_from_n"); for (int n = 1; n <= A; n++) printf(" %.6e", hn[n] / hsum); printf("\n");
    printf("occ"); for (int c = 0; c < A; c++) printf(" %.8f", occ[c]); printf("\n");
    printf("predeath_occ"); for (int c = 0; c < A; c++) printf(" %.8f", docc[c] / hsum); printf("\n");
    /* Tilt identity (README, Theorem 2): with eps_i(x) = -ln P(cell i dead next | x) and E = sum_i eps_i,
       h = E_mu[exp(-E)], so ln tau = int_0^1 <E>_s ds = sum_i c_i, c_i = int_0^1 <eps_i>_s ds,
       <.>_s the mean under mu_s ~ mu exp(-sE).  32-point Gauss-Legendre in s.  Also cumulants of E under mu. */
    if (argc > 7) {
        enum { NG = 32 };
        double xs[NG], ws[NG];
        for (int i = 0; i < NG; i++) {            /* Gauss-Legendre nodes on [0,1] by Newton */
            double z = cos(M_PI * (i + 0.75) / (NG + 0.5)), pp = 0;
            for (int itn = 0; itn < 100; itn++) {
                double p1 = 1, p2 = 0;
                for (int j = 1; j <= NG; j++) { double p3 = p2; p2 = p1; p1 = ((2.0 * j - 1) * z * p2 - (j - 1.0) * p3) / j; }
                pp = NG * (z * p1 - p2) / (z * z - 1);
                double dz = p1 / pp; z -= dz; if (fabs(dz) < 1e-15) break;
            }
            xs[i] = 0.5 * (1 - z); ws[i] = 1.0 / ((1 - z * z) * pp * pp);
        }
        static double Z[NG], Ns[NG][MAXA], Ds[NG], Es[NG];
        double k1 = 0, m2c = 0, m3c = 0, m4c = 0;
        double lneps[MAXA][2][8];
        for (int c = 0; c < A; c++) for (int x = 0; x < 2; x++) for (int k = 0; k < 8; k++) lneps[c][x][k] = -log(1 - q[c][x][k]);
        for (uint64_t s = 1; s < NA; s++) k1 += T[s] * 0;   /* placeholder to keep structure simple */
        for (int pass = 0; pass < 2; pass++)
        for (uint64_t s = 1; s < NA; s++) {
            double v = T[s], e[MAXA], E = 0;
            for (int c = 0; c < A; c++) {
                int k = __builtin_popcountll(s & nbm[c][1]) + 2 * __builtin_popcountll(s & nbm[c][2]) + 3 * __builtin_popcountll(s & nbm[c][3]);
                e[c] = lneps[c][(s >> posold[c]) & 1][k]; E += e[c];
            }
            if (pass == 0) { k1 += v * E; continue; }
            double dE = E - k1; m2c += v * dE * dE; m3c += v * dE * dE * dE; m4c += v * dE * dE * dE * dE;
            int n = __builtin_popcountll(s);
            for (int g = 0; g < NG; g++) {
                double w = v * exp(-xs[g] * E);
                Z[g] += w; Ds[g] += w * n; Es[g] += w * E;
                for (int c = 0; c < A; c++) Ns[g][c] += w * e[c];
            }
        }
        double ci[MAXA], tot = 0;
        for (int c = 0; c < A; c++) { ci[c] = 0; for (int g = 0; g < NG; g++) ci[c] += ws[g] * Ns[g][c] / Z[g]; tot += ci[c]; }
        printf("tilt_sum_ci %.12f  (lntau %.12f)\n", tot, -log(h));
        printf("price_map"); for (int c = 0; c < A; c++) printf(" %.8f", ci[c]); printf("\n");
        printf("E_cumulants_per_cell k1 %.10f k2 %.10f k3 %.10f k4 %.10f\n", k1 / A, m2c / A, m3c / A, (m4c - 3 * m2c * m2c) / A);
        printf("cumulant_series_lntau 1: %.6f 2: %.6f 3: %.6f 4: %.6f\n", k1, k1 - m2c / 2, k1 - m2c / 2 + m3c / 6,
               k1 - m2c / 2 + m3c / 6 - (m4c - 3 * m2c * m2c) / 24);
        printf("tilt_path s:<E>_s/A:density_s");
        for (int g = 0; g < NG; g += 3) printf(" %.3f:%.5f:%.5f", xs[g], Es[g] / Z[g] / A, Ds[g] / Z[g] / A);
        printf("\n");
    }
    return 0;
}
