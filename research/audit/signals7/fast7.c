// fast7: B45/S345 on a RING of L units of the 5 x 5 tube (-1 <= x+y+z, x-y+z <= 7) along v = (1,0,-1).
// Written for REVIEW-signals-7 from the rule; the same object as orc7.Tor.helix (the oracle on a helix torus), against
// which fastcheck.py compares it bit for bit.  State: x[u * NC + i], u = 0..L-1, i = index into orc7.BASE.
// Neighbours outside the tube are dead for ever (T2/T3; see orc7.py).
#include <stdint.h>
#include <string.h>
#define NC 38
static int nn[NC], ndu[NC][12], nj[NC][12];
void setup(const int* cnt, const int* du, const int* j) {
    for (int i = 0; i < NC; i++) { nn[i] = cnt[i]; for (int k = 0; k < cnt[i]; k++) { ndu[i][k] = du[i * 12 + k]; nj[i][k] = j[i * 12 + k]; } }
}
void run(uint8_t* x, uint8_t* y, int L, int n) {
    for (int g = 0; g < n; g++) {
        for (int u = 0; u < L; u++) {
            const uint8_t* row[3];
            row[0] = x + (size_t)((u + L - 1) % L) * NC; row[1] = x + (size_t)u * NC; row[2] = x + (size_t)((u + 1) % L) * NC;
            for (int i = 0; i < NC; i++) {
                int c = 0;
                for (int k = 0; k < nn[i]; k++) c += row[ndu[i][k] + 1][nj[i][k]];
                int s = row[1][i];
                y[(size_t)u * NC + i] = (c == 4 || c == 5 || (s && c == 3));
            }
        }
        memcpy(x, y, (size_t)L * NC);
    }
}
