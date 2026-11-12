/* Fast soup runner for gump on an arbitrary finite cell graph (B45/S345).
 *
 * Input (binary, written by vessel.py): int32 n, then n*12 int32 neighbour indices (-1 = a cell
 * outside the vessel that is dead forever, e.g. by T2), then n int32 flags (1 = may be live in the
 * initial soup).  Each soup: flagged cells live independently with probability rho; run until the
 * orbit is periodic (Brent's algorithm with exact state comparison), then replay to get the exact
 * transient mu (first generation of the final cycle) and the period.
 * Output, one line per soup:   id mu period final_pop [: live cell indices of the state at gen mu]
 * period 0 means not periodic by maxgen (mu then = maxgen).
 *
 * usage: vessel FILE nsoups rho seed maxgen [-c] [-p STRIDE]
 *   -c  print the live cells of the first cycle state;  -p  print "T id gen pop" every STRIDE gens
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int n; static int32_t *nb; static int32_t *flag;
static uint64_t rng_s;
static inline uint64_t rnd(void) { rng_s ^= rng_s << 13; rng_s ^= rng_s >> 7; rng_s ^= rng_s << 17; return rng_s; }

static int stepf(const unsigned char *a, unsigned char *b) {
    int pop = 0;
    for (int i = 0; i < n; i++) {
        int c = 0; const int32_t *q = nb + 12 * (size_t)i;
        for (int k = 0; k < 12; k++) { int j = q[k]; if (j >= 0) c += a[j]; }
        unsigned char v = a[i] ? (c >= 3 && c <= 5) : (c == 4 || c == 5);
        b[i] = v; pop += v;
    }
    return pop;
}

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage: vessel FILE nsoups rho seed maxgen [-c] [-p STRIDE]\n"); return 1; }
    FILE *f = fopen(argv[1], "rb");
    if (!f || fread(&n, 4, 1, f) != 1) return 1;
    nb = malloc(sizeof(int32_t) * 12 * (size_t)n); flag = malloc(sizeof(int32_t) * n);
    if (fread(nb, 4, 12 * (size_t)n, f) != 12 * (size_t)n) return 1;
    if (fread(flag, 4, n, f) != (size_t)n) return 1;
    fclose(f);
    int nsoups = atoi(argv[2]); double rho = atof(argv[3]);
    rng_s = strtoull(argv[4], 0, 10) * 2654435761ULL + 88172645463325252ULL;
    long maxgen = atol(argv[5]);
    int printcells = 0, stride = 0;
    for (int i = 6; i < argc; i++) { if (!strcmp(argv[i], "-c")) printcells = 1; if (!strcmp(argv[i], "-p")) stride = atoi(argv[++i]); }
    unsigned char *init = malloc(n), *a = malloc(n), *b = malloc(n), *saved = malloc(n), *y = malloc(n);
    for (int s = 0; s < nsoups; s++) {
        for (int i = 0; i < n; i++) init[i] = flag[i] && ((rnd() >> 11) * (1.0 / 9007199254740992.0) < rho);
        memcpy(a, init, n); memcpy(saved, a, n);
        long g = 0, power = 1, lam = 0, period = 0; int pop = 0;
        while (g < maxgen) {
            pop = stepf(a, b); { unsigned char *t = a; a = b; b = t; } g++; lam++;
            if (stride && g % stride == 0) printf("T %d %ld %d\n", s, g, pop);
            if (memcmp(a, saved, n) == 0) { period = lam; break; }
            if (lam == power) { memcpy(saved, a, n); power *= 2; lam = 0; }
        }
        long mu = maxgen;
        if (period) {
            memcpy(a, init, n); memcpy(y, init, n);
            for (long t = 0; t < period; t++) { stepf(y, b); memcpy(y, b, n); }
            mu = 0;
            while (memcmp(a, y, n) != 0) { stepf(a, b); memcpy(a, b, n); stepf(y, b); memcpy(y, b, n); mu++; }
        }
        pop = 0; for (int i = 0; i < n; i++) pop += a[i];
        printf("%d %ld %ld %d", s, mu, period, pop);
        if (printcells) { printf(" :"); for (int i = 0; i < n; i++) if (a[i]) printf(" %d", i); }
        printf("\n");
        fflush(stdout);
    }
    return 0;
}
