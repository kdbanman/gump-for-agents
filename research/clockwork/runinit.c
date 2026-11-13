/* Run given initial states on a finite cell graph (vessel.py format) to their final cycle.
 * usage: runinit VESSEL MAXGEN < inits     (one initial state per line: live cell indices)
 * output per line: mu period pop : live cells at generation mu   (period 0 = not periodic by MAXGEN)
 * Brent cycle detection with exact state comparison, then exact transient by replay (as vessel.c).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int n; static int32_t *nb;

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
    if (argc < 3) { fprintf(stderr, "usage: runinit VESSEL MAXGEN < inits\n"); return 1; }
    FILE *f = fopen(argv[1], "rb");
    if (!f || fread(&n, 4, 1, f) != 1) return 1;
    nb = malloc(sizeof(int32_t) * 12 * (size_t)n);
    if (fread(nb, 4, 12 * (size_t)n, f) != 12 * (size_t)n) return 1;
    fclose(f);
    long maxgen = atol(argv[2]);
    unsigned char *init = malloc(n), *a = malloc(n), *b = malloc(n), *saved = malloc(n), *y = malloc(n);
    static char line[1 << 20];
    while (fgets(line, sizeof line, stdin)) {
        memset(init, 0, n);
        char *p = line, *e;
        for (;;) { long v = strtol(p, &e, 10); if (e == p) break; if (v >= 0 && v < n) init[v] = 1; p = e; }
        memcpy(a, init, n); memcpy(saved, a, n);
        long g = 0, power = 1, lam = 0, period = 0;
        while (g < maxgen) {
            stepf(a, b); { unsigned char *t = a; a = b; b = t; } g++; lam++;
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
        int pop = 0; for (int i = 0; i < n; i++) pop += a[i];
        printf("%ld %ld %d :", mu, period, pop);
        for (int i = 0; i < n; i++) if (a[i]) printf(" %d", i);
        printf("\n");
    }
    return 0;
}
