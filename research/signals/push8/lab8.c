// lab8: B45/S345 (gump) on a box of the face lattice in sheared coordinates (x, y, w = x + z), push 8.
// A site is a cell iff exactly one of x, y, z = w - x is odd.  The array has a halo of 2 sites on every side.
// Interior sizes NX, NY, NW (all even), origin (x0, y0, w0) all even, so index parity = coordinate parity.
// Outside the box: dead (the caller checks that nothing reaches the outermost interior layers: `touch`).
// ring != 0: the box is periodic in x with period NX at fixed w (the move (NX, 0, -NX) in x, y, z: a ring of NX/2
// units of a wire along (1,0,-1)).
#include <stdint.h>
#include <string.h>

static int off[3][12][3];   // per axis: (dx, dy, dw)

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

// x: (NX+4) * (NY+4) * (NW+4) bytes, index ((i * (NY+4)) + j) * (NW+4) + k, i = x - x0 + 2 etc.
// returns the number of generations run; *touch is set to 1 if a live cell ever lies in the outermost interior
// layer in y or w (or x when not a ring).
int run(uint8_t* x, uint8_t* y, int NX, int NY, int NW, int n, int ring, int* touch) {
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
            uint8_t* row = x + ((size_t)i * SY + j) * SW;
            uint8_t* out = y + ((size_t)i * SY + j) * SW;
            for (int k = 2; k < NW + 2; k++) {
                int pz = (k - i) & 1;
                if (px + py + pz != 1) continue;
                int a = px ? 0 : (py ? 1 : 2);
                const long* dd = d[a];
                const uint8_t* p = row + k;
                int c = p[dd[0]] + p[dd[1]] + p[dd[2]] + p[dd[3]] + p[dd[4]] + p[dd[5]] + p[dd[6]] + p[dd[7]] + p[dd[8]] + p[dd[9]] + p[dd[10]] + p[dd[11]];
                int v = (c == 4 || c == 5 || (*p && c == 3));
                out[k] = v;
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
