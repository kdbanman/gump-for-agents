// step7: B45/S345 on a window of the 5 x 5 tube (-1 <= x+y+z, x-y+z <= 7) along v = (1,0,-1) (push 7).
// State: x[u * NC + i], u = 0 .. nu-1 the window's units (absolute unit ua + u), i the cell of the unit (geom7's E
// cells then O cells, as written by step7.py).  Cells outside the tube are dead for ever (T2: the tube is closed).
// Below the window (absolute units < ua): if `tt` is given, the plain train, read from tt[(t mod 4) * 2 * NC +
// (unit mod 2) * NC + i] at the generation being stepped (exact while the train there is undisturbed, which the
// caller checks); if tt is NULL, dead.  Above the window: dead.  The neighbour table nb[i * 12 + k] = (du, j) pairs
// (du in -1..1), with count nn[i].  ring != 0: the window is a ring (unit nu is unit 0), for checks on the oracle's
// ring torus.
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

#define NC 38
static int nn[NC]; static int ndu[NC][12], nj[NC][12];

void setup(const int* cnt, const int* du, const int* j) {
    for (int i = 0; i < NC; i++) { nn[i] = cnt[i]; for (int k = 0; k < cnt[i]; k++) { ndu[i][k] = du[i * 12 + k]; nj[i][k] = j[i * 12 + k]; } }
}

// step n generations from generation t; x is updated in place; scratch y of the same size
void run(uint8_t* x, uint8_t* y, int nu, int ua, int t, int n, const uint8_t* tt, int ring) {
    for (int g = 0; g < n; g++, t++) {
        const uint8_t* trow = tt ? tt + (size_t)(t & 3) * 2 * NC : 0;
        for (int u = 0; u < nu; u++) {
            for (int i = 0; i < NC; i++) {
                int c = 0;
                for (int k = 0; k < nn[i]; k++) {
                    int w = u + ndu[i][k];
                    if (ring) { w = (w + nu) % nu; c += x[w * NC + nj[i][k]]; continue; }
                    if (w >= nu) continue;
                    if (w < 0) { if (trow) c += trow[(((ua + w) % 2 + 2) % 2) * NC + nj[i][k]]; continue; }
                    c += x[w * NC + nj[i][k]];
                }
                int s = x[u * NC + i];
                y[u * NC + i] = (c == 4 || c == 5 || (s && c == 3));
            }
        }
        memcpy(x, y, (size_t)nu * NC);
    }
}

// many independent windows of equal size at once (batch b: x + b * nu * NC), all from generation t
void run_many(uint8_t* x, uint8_t* y, int B, int nu, int ua, int t, int n, const uint8_t* tt) {
    for (int b = 0; b < B; b++) run(x + (size_t)b * nu * NC, y, nu, ua, t, n, tt, 0);
}
