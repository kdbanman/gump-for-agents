/* Exhaustive phase portrait of gump (or the uncapped threshold rule) on a small closed vessel.
 * Input: neighbour file from kagtorus.py (int32 n, n*12 int32, -1 = outside / dead forever); n <= 30.
 * Multi-edges are counted with multiplicity (symmetric weighted network).
 * Output: number of cycles and cycle states by period, max transient (steps to reach the cycle) with an
 * example state, number of Garden-of-Eden states, and, per period >= 3, one example cycle state (bitmask).
 *   cc -O2 -o exhaust exhaust.c ; ./exhaust FILE [-u]     (-u: uncapped rule "alive iff n + x >= 4")
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "rb"); int n;
    if (!f || fread(&n, 4, 1, f) != 1 || n > 30) return 1;
    int32_t *nb = malloc(48 * n); if (fread(nb, 4, 12 * n, f) != (size_t)(12 * n)) return 1; fclose(f);
    int uncapped = argc > 2 && !strcmp(argv[2], "-u");
    /* multiplicity masks: level[i][k] = cells appearing > k times in i's list */
    uint32_t lev[30][12]; int nl[30];
    for (int i = 0; i < n; i++) {
        int mult[30] = {0}; nl[i] = 0; memset(lev[i], 0, sizeof lev[i]);
        for (int k = 0; k < 12; k++) if (nb[12 * i + k] >= 0) { int j = nb[12 * i + k]; lev[i][mult[j]] |= 1u << j; mult[j]++; if (mult[j] > nl[i]) nl[i] = mult[j]; }
    }
    uint64_t S = 1ull << n;
    uint32_t *nx = malloc(4 * S); uint16_t *dist = malloc(2 * S); uint8_t *pre = calloc(S / 8 + 1, 1);
    if (!nx || !dist || !pre) { fprintf(stderr, "oom\n"); return 1; }
    for (uint64_t s = 0; s < S; s++) {
        uint32_t t = 0;
        for (int i = 0; i < n; i++) {
            int c = 0; for (int k = 0; k < nl[i]; k++) c += __builtin_popcount((uint32_t)s & lev[i][k]);
            int x = (s >> i) & 1, h = c + x;
            int alive = uncapped ? (h >= 4) : (h >= 4 && c <= 5);
            t |= (uint32_t)alive << i;
        }
        nx[s] = t; pre[t >> 3] |= 1 << (t & 7); dist[s] = 0xFFFF;
    }
    /* cycles: walk with a temporary mark (dist = 0xFFFE while on the current path) */
    uint64_t ncyc[200] = {0}, ncycst[200] = {0}; uint32_t ex[200]; int maxper = 0;
    uint32_t *path = malloc(4 * 70000);
    int maxd = 0; uint32_t maxs = 0;
    for (uint64_t s0 = 0; s0 < S; s0++) {
        if (dist[s0] != 0xFFFF) continue;
        int L = 0; uint32_t s = s0;
        while (dist[s] == 0xFFFF) { dist[s] = 0xFFFE; path[L++] = s; s = nx[s]; if (L >= 70000) { fprintf(stderr, "path too long\n"); return 1; } }
        int base;
        if (dist[s] == 0xFFFE) {          /* new cycle through s */
            int p = 1; uint32_t u = nx[s]; while (u != s) { u = nx[u]; p++; }
            u = s; for (int k = 0; k < p; k++) { dist[u] = 0; u = nx[u]; }
            int pi = p < 199 ? p : 199; if (!ncyc[pi]) ex[pi] = s; ncyc[pi]++; ncycst[pi] += p; if (p > maxper) maxper = p;
        }
        base = dist[s];
        for (int k = L - 1; k >= 0; k--) {
            if (dist[path[k]] == 0) continue;       /* on the cycle */
            base += 1; dist[path[k]] = base;
            if (base > maxd) { maxd = base; maxs = path[k]; }
        }
    }
    uint64_t goe = 0; for (uint64_t s = 0; s < S; s++) if (!((pre[s >> 3] >> (s & 7)) & 1)) goe++;
    double meand = 0; for (uint64_t s = 0; s < S; s++) meand += dist[s]; meand /= S;
    printf("cells %d states %llu rule %s\n", n, (unsigned long long)S, uncapped ? "uncapped" : "gump");
    printf("max transient %d (example state 0x%x), mean transient %.3f, garden-of-eden %llu\n", maxd, maxs, meand, (unsigned long long)goe);
    for (int p = 1; p < 200; p++) if (ncyc[p]) printf("period %d: %llu cycles, %llu states, example 0x%x\n", p,
        (unsigned long long)ncyc[p], (unsigned long long)ncycst[p], ex[p]);
    return 0;
}
