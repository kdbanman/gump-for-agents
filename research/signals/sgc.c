/* signals: C kernels for gump (B45/S345, 12 neighbours) on an arbitrary cell graph.
 * Graph: n cells, nb[12*i+k] = index of the k-th neighbour of cell i, or n for "outside, dead forever"
 * (state arrays have n+1 entries, entry n is always 0).  Checked against reference/oracle.py by check_stepper.py.
 * Build: gcc -O2 -shared -fPIC -o sgc.so sgc.c
 */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

/* dense step: a -> b, returns population */
int dstep(int n, const int32_t *nb, const uint8_t *a, uint8_t *b) {
    int pop = 0;
    for (int i = 0; i < n; i++) {
        const int32_t *q = nb + 12 * (size_t)i; int c = 0;
        for (int k = 0; k < 12; k++) c += a[q[k]];
        uint8_t v = a[i] ? (c >= 3 && c <= 5) : (c == 4 || c == 5);
        b[i] = v; pop += v;
    }
    b[n] = 0;
    return pop;
}

/* dense run of g generations in place (st has n+1 entries) */
void drun(int n, const int32_t *nb, uint8_t *st, long g) {
    uint8_t *t = malloc(n + 1);
    for (long i = 0; i < g; i++) { dstep(n, nb, st, t); memcpy(st, t, n + 1); }
    free(t);
}

/* dense run to a cycle (Brent).  st: initial state, overwritten by a state on the cycle (the one at generation
 * *gen_out).  Returns period, 0 if none within maxgen.  *gen_out = generation at which the cycle was detected. */
long dcycle(int n, const int32_t *nb, uint8_t *st, long maxgen, long *gen_out) {
    uint8_t *a = malloc(n + 1), *b = malloc(n + 1), *saved = malloc(n + 1);
    memcpy(a, st, n + 1); memcpy(saved, a, n + 1);
    long g = 0, power = 1, lam = 0, period = 0;
    while (g < maxgen) {
        dstep(n, nb, a, b); { uint8_t *t = a; a = b; b = t; } g++; lam++;
        if (memcmp(a, saved, n) == 0) { period = lam; break; }
        if (lam == power) { memcpy(saved, a, n); power *= 2; lam = 0; }
    }
    memcpy(st, a, n + 1); *gen_out = g;
    free(a); free(b); free(saved);
    return period;
}

/* ---------------------------------------------------------------- sparse stepping */
typedef struct { int n; const int32_t *nb; uint8_t *cnt; int32_t *touched; } W;

/* live list (nl entries) with marks al[] -> out list; al updated in place.  returns new count. */
static int sstep(W *w, int32_t *live, int nl, uint8_t *al, int32_t *out) {
    int nt = 0, n = w->n; const int32_t *nb = w->nb; uint8_t *cnt = w->cnt; int32_t *touched = w->touched;
    for (int a = 0; a < nl; a++) {
        const int32_t *q = nb + 12 * (size_t)live[a];
        for (int k = 0; k < 12; k++) { int j = q[k]; if (j < n) { if (!cnt[j]) touched[nt++] = j; cnt[j]++; } }
    }
    int no = 0;
    for (int a = 0; a < nt; a++) {
        int j = touched[a], c = cnt[j]; cnt[j] = 0;
        if (c == 4 || c == 5 || (c == 3 && al[j])) out[no++] = j;
    }
    for (int a = 0; a < nl; a++) al[live[a]] = 0;
    for (int a = 0; a < no; a++) al[out[a]] = 1;
    return no;
}

/* sparse run of g generations; al (n+1 bytes) in place */
void srun(int n, const int32_t *nb, uint8_t *al, long g) {
    W w = { n, nb, calloc(n + 1, 1), malloc(4 * (size_t)(n + 1)) };
    int32_t *l1 = malloc(4 * (size_t)(n + 1)), *l2 = malloc(4 * (size_t)(n + 1)); int nl = 0;
    for (int i = 0; i < n; i++) if (al[i]) l1[nl++] = i;
    for (long t = 0; t < g; t++) { nl = sstep(&w, l1, nl, al, l2); int32_t *x = l1; l1 = l2; l2 = x; }
    free(w.cnt); free(w.touched); free(l1); free(l2);
}

/* Perturbation tracker.  bg, x: two states (n+1 bytes each), both overwritten by their states at the stop time.
 * unit[i] in [0, N): position of cell i along the ring; u0: origin unit.  Each generation t = 1.. records
 *   lo[t], hi[t] = extreme signed unit offsets (in [-N/2, N/2)) of cells where the states differ, cnt[t] = how many.
 * (lo[0], hi[0], cnt[0] describe the initial difference.)
 * Stops when: the difference vanishes (return 0); x returns to a state it had before (Brent, exact; return 1,
 * *per = period of x); the difference spans >= span units (return 2); maxgen reached (return 3).
 * *gens = number of generations run. */
int track(int n, const int32_t *nb, uint8_t *bg, uint8_t *x, const int32_t *unit, int N, int u0, int span,
          long maxgen, int32_t *lo, int32_t *hi, int32_t *cntv, long *gens, long *per) {
    W w = { n, nb, calloc(n + 1, 1), malloc(4 * (size_t)(n + 1)) };
    size_t sz = 4 * (size_t)(n + 1);
    int32_t *b1 = malloc(sz), *b2 = malloc(sz), *x1 = malloc(sz), *x2 = malloc(sz);
    uint8_t *saved = malloc(n + 1);
    int nbg = 0, nx = 0;
    for (int i = 0; i < n; i++) { if (bg[i]) b1[nbg++] = i; if (x[i]) x1[nx++] = i; }
    memcpy(saved, x, n + 1); int saved_pop = nx;
    long g = 0, power = 1, lam = 0; int ret = 3; *per = 0;
    for (;;) {
        int l = N, h = -N, c = 0;
        for (int a = 0; a < nx; a++) { int j = x1[a]; if (!bg[j]) { int r = ((unit[j] - u0 + N / 2) % N + N) % N - N / 2; if (r < l) l = r; if (r > h) h = r; c++; } }
        for (int a = 0; a < nbg; a++) { int j = b1[a]; if (!x[j]) { int r = ((unit[j] - u0 + N / 2) % N + N) % N - N / 2; if (r < l) l = r; if (r > h) h = r; c++; } }
        lo[g] = l; hi[g] = h; cntv[g] = c;
        if (c == 0) { ret = 0; break; }
        if (h - l + 1 >= span) { ret = 2; break; }
        if (g > 0) {
            if (nx == saved_pop) {
                int same = 1;
                for (int a = 0; a < nx; a++) if (!saved[x1[a]]) { same = 0; break; }
                if (same) { ret = 1; *per = lam; break; }
            }
            if (lam == power) { memcpy(saved, x, n + 1); saved_pop = nx; power *= 2; lam = 0; }
        }
        if (g >= maxgen) { ret = 3; break; }
        nbg = sstep(&w, b1, nbg, bg, b2); { int32_t *t = b1; b1 = b2; b2 = t; }
        nx = sstep(&w, x1, nx, x, x2); { int32_t *t = x1; x1 = x2; x2 = t; }
        g++; lam++;
    }
    *gens = g;
    free(w.cnt); free(w.touched); free(b1); free(b2); free(x1); free(x2); free(saved);
    return ret;
}

/* Soup runner on a ring: for each of nsoup soups (density rho, xorshift seed), run to a cycle; outputs period[s]
 * (0 = none by maxgen), gen[s], and the cycle state into states[s*(n+1) ...] if states != NULL. */
static uint64_t rs;
static inline uint64_t rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
void soups(int n, const int32_t *nb, const uint8_t *mask, int nsoup, double rho, uint64_t seed, long maxgen,
           long *period, long *gen, uint8_t *states) {
    rs = seed * 2654435761ULL + 88172645463325252ULL;
    for (int i = 0; i < 20; i++) rnd();
    uint8_t *st = malloc(n + 1);
    for (int s = 0; s < nsoup; s++) {
        for (int i = 0; i < n; i++) st[i] = mask[i] && ((rnd() >> 11) * (1.0 / 9007199254740992.0) < rho);
        st[n] = 0;
        period[s] = dcycle(n, nb, st, maxgen, &gen[s]);
        if (states) memcpy(states + (size_t)s * (n + 1), st, n + 1);
    }
    free(st);
}
