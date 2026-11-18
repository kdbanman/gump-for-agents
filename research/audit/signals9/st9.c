/* st9.c (review of signals push 9): a sparse stepper for gump on the infinite lattice, written for this review.
 *
 * Cells are faces of the cubic honeycomb in doubled coordinates (exactly one odd coordinate).  The 12 neighbours of
 * a face with normal axis a (docs/AUTOMATON.md section 2): the 4 coplanar faces at +-2 e_b +- 2 e_c and the 8
 * perpendicular faces at +-e_a +- e_b, +-e_a +- e_c.  Rule B45/S345.
 * The state is a list of live cells (int32 triples).  One step: every live cell adds one to the count of each of its
 * 12 neighbours in an open-addressing hash table; a cell is live next iff (dead and count in {4,5}) or (live and
 * count in {3,4,5}).
 * ring > 0: the lattice modulo the translation (2 ring, 0, -2 ring) (a wire along (1,0,-1) closed on itself).
 * bias: up to NB cells whose neighbour count is raised by one at every step and which are not themselves cells of
 * the state (a "held" live cell that is not stepped); unused by default.
 */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int64_t key; int32_t x, y, z; uint8_t cnt, alive, used; } slot;

static slot *T = 0;
static uint32_t TN = 0, *used = 0, nused = 0;

static void need(uint32_t n) {
    uint32_t want = 1u << 12;
    while (want < n * 40u) want <<= 1;
    if (want > TN) {
        free(T); free(used);
        TN = want; T = (slot *)calloc(TN, sizeof(slot)); used = (uint32_t *)malloc(TN * sizeof(uint32_t));
    }
}

static inline int64_t pack(int32_t x, int32_t y, int32_t z) {
    return (((int64_t)(x + 100000)) << 42) | (((int64_t)(y + 100000)) << 21) | (int64_t)(z + 100000);
}

static inline slot *find(int32_t x, int32_t y, int32_t z) {
    int64_t k = pack(x, y, z);
    uint64_t h = (uint64_t)k * 0x9E3779B97F4A7C15ull;
    uint32_t i = (uint32_t)(h >> 32) & (TN - 1);
    for (;;) {
        slot *s = &T[i];
        if (!s->used) { s->used = 1; s->key = k; s->x = x; s->y = y; s->z = z; s->cnt = 0; s->alive = 0; used[nused++] = i; return s; }
        if (s->key == k) return s;
        i = (i + 1) & (TN - 1);
    }
}

static inline void canon(int32_t *x, int32_t *z, int ring) {
    if (ring > 0) {
        int32_t L = 2 * ring, q = *x >= 0 ? *x / L : -((-*x + L - 1) / L);
        *x -= q * L; *z += q * L;
    }
}

/* one generation; returns the number of live cells written to out (or -1 if out is too small) */
int st_step(const int32_t *in, int n, int32_t *out, int cap, int ring) {
    need((uint32_t)n + 16);
    nused = 0;
    for (int i = 0; i < n; i++) {
        int32_t c[3] = { in[3 * i], in[3 * i + 1], in[3 * i + 2] };
        canon(&c[0], &c[2], ring);
        slot *s = find(c[0], c[1], c[2]); s->alive = 1;
        int a = (c[0] & 1) ? 0 : (c[1] & 1) ? 1 : 2, b = (a + 1) % 3, d = (a + 2) % 3;
        for (int sb = -2; sb <= 2; sb += 4) for (int sd = -2; sd <= 2; sd += 4) {
            int32_t q[3] = { c[0], c[1], c[2] }; q[b] += sb; q[d] += sd;
            canon(&q[0], &q[2], ring); find(q[0], q[1], q[2])->cnt++;
        }
        for (int sa = -1; sa <= 1; sa += 2) for (int w = 0; w < 2; w++) for (int st = -1; st <= 1; st += 2) {
            int32_t q[3] = { c[0], c[1], c[2] }; q[a] += sa; q[w ? d : b] += st;
            canon(&q[0], &q[2], ring); find(q[0], q[1], q[2])->cnt++;
        }
    }
    int m = 0, over = 0;
    for (uint32_t j = 0; j < nused; j++) {
        slot *s = &T[used[j]];
        int live = s->alive ? (s->cnt >= 3 && s->cnt <= 5) : (s->cnt == 4 || s->cnt == 5);
        if (live) {
            if (m < cap) { out[3 * m] = s->x; out[3 * m + 1] = s->y; out[3 * m + 2] = s->z; }
            else over = 1;
            m++;
        }
        s->used = 0;
    }
    return over ? -1 : m;
}

/* gens generations in place (buf has room for cap cells); returns the live count, or -1 on overflow */
int st_run(int32_t *buf, int n, int cap, int gens, int ring) {
    int32_t *tmp = (int32_t *)malloc(3 * (size_t)cap * sizeof(int32_t));
    for (int g = 0; g < gens && n >= 0; g++) {
        n = st_step(buf, n, tmp, cap, ring);
        if (n >= 0) memcpy(buf, tmp, 3 * (size_t)n * sizeof(int32_t));
    }
    free(tmp);
    return n;
}
