/* Exhaustive state-space map of gump (B45/S345) on a small closed vessel (research/statespace/README.md).
 *
 *   cc -O2 -march=native -o enum enum.c -lm
 *   ./enum FILE [--counts]        full report (key = value lines) on all 2^N states; --counts adds the exact
 *                                 Shannon entropy of f^t(uniform seed) (needs 2 extra 4-byte tables; N <= 29)
 *   ./enum FILE --iterate T       read states (hex, one per line) on stdin, print each followed by its T successors
 *
 * FILE: int32 n, then n*12 int32 neighbour indices, -1 = dead forever (vessels.py write). n <= 32.
 * Multi-edges (small tori) are counted with multiplicity. Bit i of a state = cell i.
 * Memory: next-state table 4*2^N bytes, transient table 2*2^N, two bitmaps 2^N/8 each (+ 8*2^N with --counts).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>

static int n; static uint32_t lev[32][12]; static int nl[32];

static inline uint32_t step(uint32_t s) {
    uint32_t t = 0;
    for (int i = 0; i < n; i++) {
        int c = 0; for (int k = 0; k < nl[i]; k++) c += __builtin_popcount(s & lev[i][k]);
        int x = (s >> i) & 1;
        int alive = x ? (c >= 3 && c <= 5) : (c == 4 || c == 5);
        t |= (uint32_t)alive << i;
    }
    return t;
}

#define BIT(b, s) (((b)[(s) >> 6] >> ((s) & 63)) & 1)
#define SET(b, s) ((b)[(s) >> 6] |= 1ull << ((s) & 63))

int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "rb");
    if (!f || fread(&n, 4, 1, f) != 1 || n > 32) { fprintf(stderr, "bad file\n"); return 1; }
    int32_t *nb = malloc(48 * n); if (fread(nb, 4, 12 * n, f) != (size_t)(12 * n)) return 1; fclose(f);
    for (int i = 0; i < n; i++) {
        int mult[32] = {0}; nl[i] = 0; memset(lev[i], 0, sizeof lev[i]);
        for (int k = 0; k < 12; k++) if (nb[12 * i + k] >= 0) {
            int j = nb[12 * i + k]; lev[i][mult[j]] |= 1u << j; mult[j]++; if (mult[j] > nl[i]) nl[i] = mult[j];
        }
    }
    if (argc > 3 && !strcmp(argv[2], "--iterate")) {
        int T = atoi(argv[3]); char line[64];
        while (fgets(line, sizeof line, stdin)) {
            uint32_t s = (uint32_t)strtoul(line, 0, 16); printf("%x", s);
            for (int t = 0; t < T; t++) { s = step(s); printf(" %x", s); }
            printf("\n");
        }
        return 0;
    }
    int counts = argc > 2 && !strcmp(argv[2], "--counts");
    uint64_t S = 1ull << n, W = (S + 63) / 64;
    uint32_t *nx = malloc(4 * S);
    uint64_t *A = calloc(W, 8), *B = calloc(W, 8);
    if (!nx || !A || !B) { fprintf(stderr, "oom\n"); return 1; }
    printf("cells = %d\nstates = %llu\n", n, (unsigned long long)S);
    for (uint64_t s = 0; s < S; s++) { uint32_t t = step((uint32_t)s); nx[s] = t; SET(B, t); }
    /* image iteration: A = f^t(all); B = f(A) */
    uint64_t sz = 0; for (uint64_t w = 0; w < W; w++) sz += __builtin_popcountll(B[w]);
    printf("image_t = %llu", (unsigned long long)S); printf(" %llu", (unsigned long long)sz);
    uint64_t goe = S - sz;
    int T = 1;
    for (;;) {
        uint64_t *tmp = A; A = B; B = tmp; memset(B, 0, 8 * W);
        for (uint64_t s = 0; s < S; s++) if (BIT(A, s)) SET(B, nx[s]);
        uint64_t sz2 = 0; for (uint64_t w = 0; w < W; w++) sz2 += __builtin_popcountll(B[w]);
        if (sz2 == sz) break;
        printf(" %llu", (unsigned long long)sz2); fflush(stdout); sz = sz2; T++;
    }
    printf("\nimage_stable_from_t = %d\ngoe = %llu\n", T, (unsigned long long)goe);
    /* B now = set of cyclic states (f^T(all) with f(B) = B) */
    uint64_t ncyc_states = sz;
    if (counts) {   /* exact Shannon entropy of f^t(U), all seeds and the seeds not yet settled */
        uint32_t *c0 = malloc(4 * S), *c1 = malloc(4 * S);
        if (!c0 || !c1) { fprintf(stderr, "oom counts\n"); return 1; }
        for (uint64_t s = 0; s < S; s++) c0[s] = 1;
        printf("entropy_t(bits; all | unsettled; unsettled_seeds) =");
        for (int t = 0; t <= T + 1; t++) {
            double H = 0, Hl = 0, L = 0;
            for (uint64_t s = 0; s < S; s++) if (c0[s] && !BIT(B, s)) L += c0[s];
            for (uint64_t s = 0; s < S; s++) if (c0[s]) {
                double p = c0[s] / (double)S; H -= p * log2(p);
                if (!BIT(B, s)) { double q = c0[s] / L; Hl -= q * log2(q); }
            }
            printf(" %d:%.6f|%.6f;%.0f", t, H, Hl, L);
            memset(c1, 0, 4 * S);
            for (uint64_t s = 0; s < S; s++) if (c0[s]) c1[nx[s]] += c0[s];
            uint32_t *tmp = c0; c0 = c1; c1 = tmp;
        }
        printf("\n"); free(c0); free(c1);
    }
    free(A);
    /* walk: transient length dist[s] (0 on a cycle), cycle label overwriting nx[s] once s is finished */
    uint16_t *dist = malloc(2 * S); if (!dist) { fprintf(stderr, "oom dist\n"); return 1; }
    for (uint64_t s = 0; s < S; s++) dist[s] = 0xFFFF;
    uint32_t cap = 1u << 22, ncyc = 0; uint32_t *cper = malloc(4 * cap), *crep = malloc(4 * cap);
    uint32_t *path = malloc(4 * 70000);
    for (uint64_t s0 = 0; s0 < S; s0++) {
        if (dist[s0] != 0xFFFF) continue;
        int L = 0; uint32_t s = (uint32_t)s0;
        while (dist[s] == 0xFFFF) { dist[s] = 0xFFFE; path[L++] = s; s = nx[s]; if (L >= 70000) { fprintf(stderr, "path\n"); return 1; } }
        uint32_t lab;
        if (dist[s] == 0xFFFE) {          /* a new cycle through s */
            if (ncyc == cap) { cap *= 2; cper = realloc(cper, 4 * cap); crep = realloc(crep, 4 * cap); }
            uint32_t p = 1, u = nx[s], mn = s; while (u != s) { if (u < mn) mn = u; u = nx[u]; p++; }
            lab = ncyc++; cper[lab] = p; crep[lab] = mn;
            u = s; for (uint32_t k = 0; k < p; k++) { uint32_t v = nx[u]; dist[u] = 0; nx[u] = lab; u = v; }
        } else lab = nx[s];               /* s finished earlier: nx[s] holds its label */
        int base = dist[s];
        for (int k = L - 1; k >= 0; k--) {
            uint32_t v = path[k]; if (dist[v] == 0) continue;
            base++; if (base >= 0xFFFE) { fprintf(stderr, "transient too long\n"); return 1; }
            dist[v] = base; nx[v] = lab;
        }
    }
    uint64_t *basin = calloc(ncyc, 8);
    uint32_t maxd = 0; uint64_t hist[65536] = {0};
    for (uint64_t s = 0; s < S; s++) { basin[nx[s]]++; hist[dist[s]]++; if (dist[s] > maxd) maxd = dist[s]; }
    printf("cycles = %u\ncyclic_states = %llu\n", ncyc, (unsigned long long)ncyc_states);
    /* by period */
    uint64_t pc[1024] = {0}, ps[1024] = {0}, pb[1024] = {0}; uint32_t maxp = 0;
    for (uint32_t c = 0; c < ncyc; c++) { uint32_t p = cper[c] < 1023 ? cper[c] : 1023; pc[p]++; ps[p] += cper[c]; pb[p] += basin[c]; if (cper[c] > maxp) maxp = cper[c]; }
    printf("by_period(period:cycles:states:basin) =");
    for (int p = 1; p < 1024; p++) if (pc[p]) printf(" %d:%llu:%llu:%llu", p, (unsigned long long)pc[p], (unsigned long long)ps[p], (unsigned long long)pb[p]);
    printf("\n");
    uint32_t big = 0; for (uint32_t c = 1; c < ncyc; c++) if (basin[c] > basin[big]) big = c;
    printf("largest_basin = %llu cycle_period %u rep %x pop %d\n", (unsigned long long)basin[big], cper[big], crep[big], __builtin_popcount(crep[big]));
    printf("empty_basin = %llu\n", (unsigned long long)basin[nx[0]]);
    /* sorted top basins */
    printf("top_basins(size:period:rep) =");
    for (int r = 0; r < 8 && r < (int)ncyc; r++) {
        uint32_t b2 = UINT32_MAX; for (uint32_t c = 0; c < ncyc; c++) if (basin[c] != UINT64_MAX && (b2 == UINT32_MAX || basin[c] > basin[b2])) b2 = c;
        printf(" %llu:%u:%x", (unsigned long long)basin[b2], cper[b2], crep[b2]); basin[b2] = UINT64_MAX;
    }
    printf("\n");
    printf("transient_hist =");
    for (uint32_t d = 0; d <= maxd; d++) printf(" %llu", (unsigned long long)hist[d]);
    printf("\n");
    /* visited = dist + period */
    static uint64_t vh[70000]; uint32_t maxv = 0;
    for (uint64_t s = 0; s < S; s++) { uint32_t v = dist[s] + cper[nx[s]]; if (v < 70000) { vh[v]++; if (v > maxv) maxv = v; } }
    printf("visited_hist(from 1) =");
    for (uint32_t v = 1; v <= maxv; v++) printf(" %llu", (unsigned long long)vh[v]);
    printf("\n");
    printf("champions(transient %u) =", maxd);
    int nch = 0; for (uint64_t s = 0; s < S; s++) if (dist[s] == maxd) { if (nch < 256) printf(" %llx", (unsigned long long)s); nch++; }
    printf("\nn_champions = %d\n", nch);
    uint64_t champ = 0; for (uint64_t s = 0; s < S; s++) if (dist[s] == maxd) { champ = s; break; }
    printf("champion_cycle_period = %u\n", cper[nx[champ]]);
    return 0;
}
