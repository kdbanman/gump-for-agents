// st.c (push 8b): gump (B45/S345 on the 12-neighbour face lattice, docs/AUTOMATON.md) on the infinite lattice,
// sparse.  A cell (x, y, z), doubled coordinates with exactly one odd, is the key
//     ((x + OFF) << 42) | ((y + OFF) << 21) | (z + OFF),   OFF = 2^20 (even, so the low bit of a field is the parity).
// Ring (L > 0): cells are taken modulo the translation (2L, 0, -2L), representatives 0 <= x < 2L.
// Checked cell for cell against reference/oracle.py by check_st.py.
// Build: gcc -O2 -shared -fPIC -o st.so st.c
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
typedef uint64_t u64;
typedef int64_t i64;
#define OFF ((i64)1 << 20)

static i64 delta[3][12];
static int ready = 0;

static void init(void) {
    for (int a = 0; a < 3; a++) {
        int b = (a + 1) % 3, c = (a + 2) % 3, k = 0;
        for (int sb = -2; sb <= 2; sb += 4) for (int sc = -2; sc <= 2; sc += 4) {
            i64 o[3] = {0, 0, 0}; o[b] = sb; o[c] = sc;
            delta[a][k++] = o[0] * ((i64)1 << 42) + o[1] * ((i64)1 << 21) + o[2];
        }
        for (int sa = -1; sa <= 1; sa += 2) for (int ti = 0; ti < 2; ti++) for (int st = -1; st <= 1; st += 2) {
            int t = ti ? c : b; i64 o[3] = {0, 0, 0}; o[a] = sa; o[t] = st;
            delta[a][k++] = o[0] * ((i64)1 << 42) + o[1] * ((i64)1 << 21) + o[2];
        }
    }
    ready = 1;
}

static u64 *tk = 0; static uint8_t *tv = 0; static u64 tsize = 0; static uint32_t *used = 0; static u64 ucap = 0;

static inline u64 hsh(u64 k) { k ^= k >> 29; k *= 0x9E3779B97F4A7C15ULL; k ^= k >> 32; return k; }

static inline u64 wrapk(u64 k, i64 L) {
    if (!L) return k;
    i64 x = (i64)(k >> 42) - OFF;
    if (x < 0) k += (((u64)(2 * L)) << 42) - (u64)(2 * L);
    else if (x >= 2 * L) k -= (((u64)(2 * L)) << 42) - (u64)(2 * L);
    return k;
}

static inline uint32_t slot(u64 k, u64 mask, u64 *nused) {
    u64 h = hsh(k) & mask;
    while (tk[h] && tk[h] != k) h = (h + 1) & mask;
    if (!tk[h]) { tk[h] = k; tv[h] = 0; used[(*nused)++] = (uint32_t)h; }
    return (uint32_t)h;
}

static int cmp(const void *a, const void *b) { u64 x = *(const u64 *)a, y = *(const u64 *)b; return x < y ? -1 : x > y; }

// one generation: in[0..n) -> out (capacity cap); returns the new count, or -1 if cap is too small
static int step1(const u64 *in, int n, u64 *out, int cap, i64 L) {
    u64 need = 1024; while (need < (u64)n * 40) need <<= 1;
    if (need > tsize) {
        free(tk); free(tv); tsize = need;
        tk = (u64 *)calloc(tsize, sizeof(u64)); tv = (uint8_t *)malloc(tsize);
    }
    if ((u64)n * 13 + 16 > ucap) { free(used); ucap = (u64)n * 13 + 16; used = (uint32_t *)malloc(ucap * sizeof(uint32_t)); }
    u64 mask = tsize - 1, nused = 0;
    for (int i = 0; i < n; i++) {
        u64 k = in[i];
        int a = ((k >> 42) & 1) ? 0 : (((k >> 21) & 1) ? 1 : 2);
        tv[slot(k, mask, &nused)] |= 0x80;
        for (int j = 0; j < 12; j++) tv[slot(wrapk(k + (u64)delta[a][j], L), mask, &nused)]++;
    }
    int m = 0;
    for (u64 i = 0; i < nused; i++) {
        uint32_t h = used[i]; uint8_t v = tv[h]; int c = v & 0x7f;
        if (c == 4 || c == 5 || (c == 3 && (v & 0x80))) { if (m < cap) out[m] = tk[h]; m++; }
        tk[h] = 0;
    }
    return m <= cap ? m : -1;
}

// gens generations; buf (capacity cap) holds the cells on entry (n of them) and on exit, sorted; tmp is scratch of
// the same capacity.  Returns the final count, or -1 on overflow.
int run(u64 *buf, int n, u64 *tmp, int cap, int gens, int L) {
    if (!ready) init();
    u64 *a = buf, *b = tmp;
    for (int g = 0; g < gens; g++) {
        n = step1(a, n, b, cap, L);
        if (n < 0) return -1;
        u64 *t = a; a = b; b = t;
    }
    if (a != buf) memcpy(buf, a, (size_t)n * sizeof(u64));
    qsort(buf, n, sizeof(u64), cmp);
    return n;
}
