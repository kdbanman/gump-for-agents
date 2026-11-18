// q.c (audit of signals push 8b): gump, B45/S345 on the faces of the cubic honeycomb (docs/AUTOMATON.md section 2),
// on the infinite lattice, sparse.  Written for the audit; shares nothing with the push's st.c.
// A cell is (x, y, z) in doubled coordinates, exactly one odd.  Key: 20 bits per coordinate, biased by 2^19.
// The neighbour table is taken from the cube-index form of AUTOMATON.md (three volumes X, Y, Z), not from the
// doubled offsets, and is checked against reference/oracle.py by check_q.py.
// Build: gcc -O2 -shared -fPIC -o q.so q.c
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define BIAS (1 << 19)
#define M20 ((1 << 20) - 1)
typedef int64_t i64;

static inline i64 pack(int x, int y, int z) { return ((i64)(x + BIAS) << 40) | ((i64)(y + BIAS) << 20) | (i64)(z + BIAS); }
static inline void unpack(i64 k, int *x, int *y, int *z) {
    *x = (int)((k >> 40) & M20) - BIAS; *y = (int)((k >> 20) & M20) - BIAS; *z = (int)(k & M20) - BIAS;
}

// neighbours of a cell of volume a at cube (i, j, k): 4 in the same volume, 4 in each of the other two
// (AUTOMATON.md, cyclic in X->Y->Z, i->j->k).  out: 12 doubled coordinates.
static void neigh(int x, int y, int z, int out[12][3]) {
    int c[3] = {x, y, z};
    int a = (x & 1) ? 0 : ((y & 1) ? 1 : 2);
    int b = (a + 1) % 3, d = (a + 2) % 3;
    int cube[3];            // cube index of the cell: (c - e_a) / 2
    for (int q = 0; q < 3; q++) cube[q] = (c[q] - (q == a)) >> 1;
    int n = 0;
    // A[i, j+-1, k+-1]
    for (int s = -1; s <= 1; s += 2) for (int t = -1; t <= 1; t += 2) {
        int e[3]; e[a] = cube[a]; e[b] = cube[b] + s; e[d] = cube[d] + t;
        for (int q = 0; q < 3; q++) out[n][q] = 2 * e[q] + (q == a);
        n++;
    }
    // B[i,j,k] B[i,j-1,k] B[i+1,j,k] B[i+1,j-1,k]   (B = next volume; its own index runs along b)
    for (int da = 0; da <= 1; da++) for (int db = -1; db <= 0; db++) {
        int e[3]; e[a] = cube[a] + da; e[b] = cube[b] + db; e[d] = cube[d];
        for (int q = 0; q < 3; q++) out[n][q] = 2 * e[q] + (q == b);
        n++;
    }
    // D[i,j,k] D[i,j,k-1] D[i+1,j,k] D[i+1,j,k-1]
    for (int da = 0; da <= 1; da++) for (int dd = -1; dd <= 0; dd++) {
        int e[3]; e[a] = cube[a] + da; e[b] = cube[b]; e[d] = cube[d] + dd;
        for (int q = 0; q < 3; q++) out[n][q] = 2 * e[q] + (q == d);
        n++;
    }
}

typedef struct { i64 key; uint32_t stamp; uint8_t cnt, live; } slot_t;
static slot_t *tab = 0; static size_t tsz = 0; static uint32_t stamp = 0;
static uint32_t *touched = 0; static size_t tcap = 0;

static inline size_t hfn(i64 k) { uint64_t h = (uint64_t)k * 0xD6E8FEB86659FD93ULL; h ^= h >> 31; h *= 0xA24BAED4963EE407ULL; return (size_t)(h >> 20); }

static slot_t *find(i64 k, size_t *nt) {
    size_t m = tsz - 1, h = hfn(k) & m;
    for (;;) {
        slot_t *s = &tab[h];
        if (s->stamp != stamp) { s->stamp = stamp; s->key = k; s->cnt = 0; s->live = 0; touched[(*nt)++] = (uint32_t)h; return s; }
        if (s->key == k) return s;
        h = (h + 1) & m;
    }
}

static int cmp64(const void *a, const void *b) { i64 x = *(const i64 *)a, y = *(const i64 *)b; return (x > y) - (x < y); }

// one generation; returns the number of live cells (out must hold 13 * n), unsorted
static int step1(const i64 *in, int n, i64 *out) {
    size_t need = 256; while (need < (size_t)n * 32) need <<= 1;
    if (need > tsz) { free(tab); tsz = need; tab = (slot_t *)calloc(tsz, sizeof(slot_t)); stamp = 0; }
    if ((size_t)n * 13 + 8 > tcap) { free(touched); tcap = (size_t)n * 13 + 8; touched = (uint32_t *)malloc(tcap * sizeof(uint32_t)); }
    if (++stamp == 0) { memset(tab, 0, tsz * sizeof(slot_t)); stamp = 1; }
    size_t nt = 0;
    for (int i = 0; i < n; i++) {
        int x, y, z, nb[12][3]; unpack(in[i], &x, &y, &z);
        find(in[i], &nt)->live = 1;
        neigh(x, y, z, nb);
        for (int j = 0; j < 12; j++) find(pack(nb[j][0], nb[j][1], nb[j][2]), &nt)->cnt++;
    }
    int m = 0;
    for (size_t i = 0; i < nt; i++) {
        slot_t *s = &tab[touched[i]];
        int alive = s->live ? (s->cnt >= 3 && s->cnt <= 5) : (s->cnt == 4 || s->cnt == 5);
        if (alive) out[m++] = s->key;
    }
    return m;
}

// gens generations.  a (n cells) and b are buffers of capacity cap.  Returns the count, with the result sorted in a;
// -1 if the pattern outgrew cap / 13.
int q_run(i64 *a, int n, i64 *b, int cap, int gens) {
    i64 *p = a, *q = b;
    for (int g = 0; g < gens; g++) {
        if ((i64)n * 13 > cap) return -1;
        n = step1(p, n, q);
        i64 *t = p; p = q; q = t;
    }
    if (p != a) memcpy(a, p, (size_t)n * sizeof(i64));
    qsort(a, (size_t)n, sizeof(i64), cmp64);
    return n;
}
