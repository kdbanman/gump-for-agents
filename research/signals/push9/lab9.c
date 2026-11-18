// lab9 (push 9): lab8's stepper with a static bias: every site's neighbour count is increased by bias[site].
// Same array layout as push 8's lab8.c (sheared coordinates (x, y, w = x + z), a halo of 2 sites, ring in x).
// With bias all zero it is lab8's rule exactly (checked by check9.py against lab8 and so against the oracle).
// A search tool only: a bias stands for the live cells of some object that never changes.
#include <stdint.h>
#include <string.h>

static int off[3][12][3];

static void make_off(void) {
    for (int a = 0; a < 3; a++) {
        int b = (a + 1) % 3, c = (a + 2) % 3, k = 0;
        if (b > c) { int t = b; b = c; c = t; }
        for (int sb = 2; sb >= -2; sb -= 4) for (int sc = 2; sc >= -2; sc -= 4) {
            int o[3] = {0, 0, 0}; o[b] = sb; o[c] = sc;
            off[a][k][0] = o[0]; off[a][k][1] = o[1]; off[a][k][2] = o[0] + o[2]; k++;
        }
        for (int sa = 1; sa >= -1; sa -= 2) for (int ti = 0; ti < 2; ti++) for (int st = 1; st >= -1; st -= 2) {
            int t = ti ? c : b; int o[3] = {0, 0, 0}; o[a] = sa; o[t] = st;
            off[a][k][0] = o[0]; off[a][k][1] = o[1]; off[a][k][2] = o[0] + o[2]; k++;
        }
    }
}

int run_bias(uint8_t* x, uint8_t* y, const uint8_t* bias, int NX, int NY, int NW, int n, int ring, int* touch) {
    static int done = 0;
    if (!done) { make_off(); done = 1; }
    int SY = NY + 4, SW = NW + 4, SX = NX + 4;
    long d[3][12];
    for (int a = 0; a < 3; a++) for (int k = 0; k < 12; k++)
        d[a][k] = ((long)off[a][k][0] * SY + off[a][k][1]) * SW + off[a][k][2];
    size_t tot = (size_t)SX * SY * SW;
    size_t slab = (size_t)SY * SW;
    *touch = 0;
    for (int g = 0; g < n; g++) {
        if (ring) {
            memcpy(x, x + (size_t)NX * slab, 2 * slab);
            memcpy(x + (size_t)(NX + 2) * slab, x + 2 * slab, 2 * slab);
        }
        memset(y, 0, tot);
        for (int i = 2; i < NX + 2; i++) for (int j = 2; j < NY + 2; j++) {
            int px = i & 1, py = j & 1;
            size_t base = ((size_t)i * SY + j) * SW;
            for (int k = 2; k < NW + 2; k++) {
                int pz = (k - i) & 1;
                if (px + py + pz != 1) continue;
                int a = px ? 0 : (py ? 1 : 2);
                const long* dd = d[a];
                const uint8_t* p = x + base + k;
                int c = bias[base + k];
                for (int q = 0; q < 12; q++) c += p[dd[q]];
                int v = (c == 4 || c == 5 || (*p && c == 3));
                y[base + k] = v;
                if (v && (j == 2 || j == NY + 1 || k == 2 || k == NW + 1 || (!ring && (i == 2 || i == NX + 1)))) *touch = 1;
            }
        }
        memcpy(x, y, tot);
    }
    if (ring) {
        memset(x, 0, 2 * slab);
        memset(x + (size_t)(NX + 2) * slab, 0, 2 * slab);
    }
    return n;
}
