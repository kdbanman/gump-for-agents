// st8: B45/S345 on a box of the face lattice, for REVIEW-signals-8.  Written from docs/AUTOMATON.md section 2.
// Array index (i, j, k) = (x - x0, y - y0, (x + z) - w0) + 2, with x0, y0, w0 even; a halo of 2 dead sites on every
// side.  The 12 neighbour offsets per normal axis are passed in by the caller as (dx, dy, dw) triples (the Python
// side builds them from the doubled offsets and asserts they equal oracle.offsets), so no rule geometry is coded here
// except "a site is a cell iff exactly one of x, y, z is odd".  Everything outside the box is dead; `touch` reports
// whether a live cell was ever written in the outermost interior layer (then the run is not exact).
#include <stdint.h>
#include <string.h>

int st8_run(uint8_t *a, uint8_t *b, int NX, int NY, int NW, int gens, const int *off, int *touch) {
    const long SY = NY + 4, SW = NW + 4, SX = NX + 4;
    long d[3][12];
    for (int ax = 0; ax < 3; ax++)
        for (int n = 0; n < 12; n++) {
            const int *o = off + (ax * 12 + n) * 3;
            d[ax][n] = ((long)o[0] * SY + o[1]) * SW + o[2];
        }
    int hit = 0;
    for (int g = 0; g < gens; g++) {
        memset(b, 0, (size_t)(SX * SY * SW));
        for (long i = 2; i < NX + 2; i++)
            for (long j = 2; j < NY + 2; j++) {
                const uint8_t *src = a + (i * SY + j) * SW;
                uint8_t *dst = b + (i * SY + j) * SW;
                int px = (int)(i & 1), py = (int)(j & 1);
                for (long k = 2; k < NW + 2; k++) {
                    int pz = (int)((k - i) & 1);
                    if (px + py + pz != 1) continue;
                    const long *dd = d[px ? 0 : (py ? 1 : 2)];
                    int n = 0;
                    for (int q = 0; q < 12; q++) n += src[k + dd[q]];
                    int alive = src[k];
                    int nxt = alive ? (n >= 3 && n <= 5) : (n == 4 || n == 5);
                    if (nxt) {
                        dst[k] = 1;
                        if (i == 2 || i == NX + 1 || j == 2 || j == NY + 1 || k == 2 || k == NW + 1) hit = 1;
                    }
                }
            }
        uint8_t *t = a; a = b; b = t;
    }
    if (gens & 1) { memcpy(b, a, (size_t)(SX * SY * SW)); }   // result always ends in the caller's first array
    *touch = hit;
    return gens;
}
