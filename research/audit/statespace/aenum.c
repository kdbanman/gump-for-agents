/* Independent exhaustive enumerator for the statespace audit (written without reusing research/statespace/enum.c).
 *
 *   cc -O3 -march=native -fopenmp -o aenum aenum.c
 *   [INDEG=1] ./aenum FILE CHAMPFILE SAMPLEFILE [NSAMPLE]   (INDEG: also the second moment of in-degrees)
 *
 * FILE: int32 n, n*12 int32 neighbours (-1 = dead forever), from geom.py. Multi-edges counted with multiplicity.
 * The map is tabulated with a bit-sliced step: 64 states at a time (the low 6 bits of the state index are the lane),
 * neighbour counts in a 4-bit ripple counter per cell, then a 64 x n bit transpose.
 * Analysis (different from the study's): heights by a path walk with an 8-bit height table, cycles labelled
 * first and labels pushed outwards one height level per pass (nx overwritten by cycle id), image iteration on
 * bitmaps as an internal check that #(height 0) = |f^T(S)|.
 * SAMPLEFILE gets NSAMPLE pseudo-random (s, f(s)) pairs for checking the table against geom.py's python step.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static int n, deg[32], nbl[32][12];

static void block(uint64_t hi, uint32_t *out) {
    uint64_t w[32], o[32];
    for (int j = 0; j < n; j++) {
        if (j < 6) { uint64_t m = 0; for (int l = 0; l < 64; l++) if ((l >> j) & 1) m |= 1ull << l; w[j] = m; }
        else w[j] = ((hi >> (j - 6)) & 1) ? ~0ull : 0ull;
    }
    for (int i = 0; i < n; i++) {
        uint64_t b0 = 0, b1 = 0, b2 = 0, b3 = 0;
        for (int k = 0; k < deg[i]; k++) {
            uint64_t x = w[nbl[i][k]], c1 = b0 & x; b0 ^= x;
            uint64_t c2 = b1 & c1; b1 ^= c1;
            uint64_t c3 = b2 & c2; b2 ^= c2; b3 ^= c3;
        }
        uint64_t x = w[i];
        o[i] = ~b3 & ((b2 & ~b1) | (x & ~b2 & b1 & b0));   /* 4,5 any; 3 if alive */
    }
    for (int l = 0; l < 64; l++) {
        uint32_t t = 0;
        for (int i = 0; i < n; i++) t |= (uint32_t)((o[i] >> l) & 1) << i;
        out[l] = t;
    }
}

int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "rb");
    if (!f || fread(&n, 4, 1, f) != 1 || n < 6 || n > 31) { fprintf(stderr, "bad\n"); return 1; }
    int32_t raw[32 * 12];
    if (fread(raw, 4, 12 * n, f) != (size_t)(12 * n)) return 1;
    fclose(f);
    for (int i = 0; i < n; i++) { deg[i] = 0; for (int k = 0; k < 12; k++) if (raw[12 * i + k] >= 0) nbl[i][deg[i]++] = raw[12 * i + k]; }
    uint64_t S = 1ull << n, NB = S >> 6, W = S >> 6;
    uint32_t *nx = malloc(4 * S); uint8_t *h = malloc(S);
    uint64_t *A = calloc(W, 8), *B = calloc(W, 8);
    if (!nx || !h || !A || !B) { fprintf(stderr, "oom\n"); return 1; }
    #pragma omp parallel for schedule(dynamic, 4096)
    for (int64_t b = 0; b < (int64_t)NB; b++) block((uint64_t)b, nx + 64 * b);
    /* samples */
    FILE *fs = fopen(argv[3], "w"); int ns = argc > 4 ? atoi(argv[4]) : 2000;
    uint64_t r = 0x9E3779B97F4A7C15ull;
    for (int k = 0; k < ns; k++) { r ^= r << 13; r ^= r >> 7; r ^= r << 17; uint64_t s = r & (S - 1); fprintf(fs, "%llx %x\n", (unsigned long long)s, nx[s]); }
    fprintf(fs, "%llx %x\n%llx %x\n", 0ull, nx[0], (unsigned long long)(S - 1), nx[S - 1]); fclose(fs);
    if (getenv("INDEG")) {   /* in-degree second moment: birthday yardstick sqrt(pi M^2 / (2 sum d^2)) */
        uint32_t *cnt = calloc(S, 4); if (!cnt) { fprintf(stderr, "oom indeg\n"); return 1; }
        for (uint64_t s = 0; s < S; s++) cnt[nx[s]]++;
        double sq = 0, sq_ne = 0; uint32_t dmax = 0;
        for (uint64_t s = 0; s < S; s++) { double d = cnt[s]; sq += d * d; if (s) sq_ne += d * d; if (cnt[s] > dmax) dmax = cnt[s]; }
        printf("indeg sum_d2 %.6e max %u indeg0 %u sum_d2_without_empty %.6e\n", sq, dmax, cnt[0], sq_ne);
        free(cnt);
    }
    /* preimage bitmap and image iteration */
    for (uint64_t s = 0; s < S; s++) B[nx[s] >> 6] |= 1ull << (nx[s] & 63);
    uint64_t prev = S, cur = 0; for (uint64_t k = 0; k < W; k++) cur += __builtin_popcountll(B[k]);
    printf("N %d\nno_pred %llu\nimage %llu %llu", n, (unsigned long long)(S - cur), (unsigned long long)S, (unsigned long long)cur);
    int Tst = 1;
    while (cur != prev) {
        uint64_t *t = A; A = B; B = t; memset(B, 0, 8 * W);
        for (uint64_t k = 0; k < W; k++) { uint64_t m = A[k]; while (m) { int l = __builtin_ctzll(m); m &= m - 1; uint32_t y = nx[64 * k + l]; B[y >> 6] |= 1ull << (y & 63); } }
        prev = cur; cur = 0; for (uint64_t k = 0; k < W; k++) cur += __builtin_popcountll(B[k]);
        if (cur != prev) { printf(" %llu", (unsigned long long)cur); Tst++; }
    }
    printf("\nimage_stable_after %d\n", Tst);
    uint64_t imgfinal = cur;
    free(A);
    /* heights */
    memset(h, 255, S);
    static uint32_t path[1 << 16];
    for (uint64_t s0 = 0; s0 < S; s0++) {
        if (h[s0] != 255) continue;
        int L = 0; uint32_t s = (uint32_t)s0;
        while (h[s] == 255) { h[s] = 254; path[L++] = s; s = nx[s]; if (L >= (1 << 16)) { fprintf(stderr, "long path\n"); return 1; } }
        int base;
        if (h[s] == 254) { int q = L - 1; while (path[q] != s) q--; for (int k = q; k < L; k++) h[path[k]] = 0; L = q; base = 0; }
        else base = h[s];
        for (int k = L - 1; k >= 0; k--) { base++; if (base > 250) { fprintf(stderr, "tall\n"); return 1; } h[path[k]] = (uint8_t)base; }
    }
    int maxh = 0; uint64_t hh[256] = {0};
    for (uint64_t s = 0; s < S; s++) { hh[h[s]]++; if (h[s] > maxh) maxh = h[s]; }
    printf("on_cycles %llu (image check %s)\n", (unsigned long long)hh[0], hh[0] == imgfinal ? "agrees" : "DISAGREES");
    /* label cycles; B reused as 'labelled' bitmap */
    memset(B, 0, 8 * W);
    uint32_t cap = 1 << 16, nc = 0; uint32_t *per = malloc(4 * cap), *rep = malloc(4 * cap);
    uint32_t *cyc = malloc(4 * 70000);
    for (uint64_t s = 0; s < S; s++) {
        if (h[s] || ((B[s >> 6] >> (s & 63)) & 1)) continue;
        int p = 0; uint32_t u = (uint32_t)s, mn = u;
        do { cyc[p++] = u; B[u >> 6] |= 1ull << (u & 63); if (u < mn) mn = u; u = nx[u]; } while (u != (uint32_t)s && p < 70000);
        if (nc == cap) { cap *= 2; per = realloc(per, 4 * cap); rep = realloc(rep, 4 * cap); }
        per[nc] = p; rep[nc] = mn;
        for (int k = 0; k < p; k++) nx[cyc[k]] = nc;
        nc++;
    }
    for (int lev = 1; lev <= maxh; lev++)
        for (uint64_t s = 0; s < S; s++) if (h[s] == lev) nx[s] = nx[nx[s]];
    uint64_t *bas = calloc(nc, 8); static uint64_t vh[1 << 16];
    uint64_t pc[4096] = {0}, pst[4096] = {0}; uint32_t maxp = 0;
    for (uint64_t s = 0; s < S; s++) { uint32_t c = nx[s]; bas[c]++; { uint32_t v = h[s] + per[c]; vh[v < 65535 ? v : 65535]++; } }
    for (uint32_t c = 0; c < nc; c++) { uint32_t p = per[c] < 4095 ? per[c] : 4095; pc[p]++; pst[p] += per[c]; if (per[c] > maxp) maxp = per[c]; }
    printf("cycles %u\nperiods(p:cycles:states)", nc);
    for (int p = 1; p < 4096; p++) if (pc[p]) printf(" %d:%llu:%llu", p, (unsigned long long)pc[p], (unsigned long long)pst[p]);
    uint32_t big = 0; for (uint32_t c = 1; c < nc; c++) if (bas[c] > bas[big]) big = c;
    uint32_t e = nx[0];
    printf("\nlargest_basin %llu period %u rep %x\nempty_basin %llu\n", (unsigned long long)bas[big], per[big], rep[big], (unsigned long long)bas[e]);
    double mt = 0, mv = 0; for (int k = 0; k <= maxh; k++) mt += (double)k * hh[k];
    for (int k = 0; k < 65536; k++) mv += (double)k * vh[k];
    uint64_t acc = 0; int medt = 0; for (int k = 0; k <= maxh; k++) { acc += hh[k]; if (acc * 2 >= S) { medt = k; break; } }
    acc = 0; int medv = 0, maxv = 0; for (int k = 0; k < 65536; k++) if (vh[k]) maxv = k;
    for (int k = 0; k < 65536; k++) { acc += vh[k]; if (acc * 2 >= S) { medv = k; break; } }
    printf("transient mean %.6f median %d max %d\nvisited mean %.6f median %d max %d\n", mt / S, medt, maxh, mv / S, medv, maxv);
    printf("transient_hist"); for (int k = 0; k <= maxh; k++) printf(" %llu", (unsigned long long)hh[k]); printf("\n");
    FILE *fc = fopen(argv[2], "w"); uint64_t nch = 0;
    for (uint64_t s = 0; s < S; s++) if (h[s] == maxh) { fprintf(fc, "%llx %u\n", (unsigned long long)s, per[nx[s]]); nch++; }
    fclose(fc);
    printf("champions %llu\n", (unsigned long long)nch);
    return 0;
}
