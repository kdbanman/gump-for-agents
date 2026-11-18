/* mc.c: Monte Carlo of the same one-layer dice surrogate as qsd.c (same graph file, same kernel), for faces too
   large for the exact product.  Estimator: after a burn-in of T0 generations from a Bernoulli(1/2) start
   (replicas that die in the burn-in are restarted), tau = (generations lived) / (deaths).
   usage: mc graph rho1 rho2 deaths maxgens seed [T0=200] [rho3]  (rho3: density of the coins coded as tens in the m1, m2 fields; geom.py hull2)     prints: A deaths exposure lntau stderr density, then the shares of deaths with a fall of >= A/2 cells in one of
   the last 6 generations, with a state of >= 0.7A cells among the last 6, and with the death itself such a fall
   build: gcc -O3 -march=native -o mc mc.c -lm */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>
#define MAXA 256
static int A, m1[MAXA], m2[MAXA], deg[MAXA], nb[MAXA][12];
static uint64_t thr[MAXA][2][8];
static uint64_t sx[4];
static inline uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static inline uint64_t rnd(void) { uint64_t r = rotl(sx[1] * 5, 7) * 9, t = sx[1] << 17;
    sx[2] ^= sx[0]; sx[3] ^= sx[1]; sx[1] ^= sx[2]; sx[0] ^= sx[3]; sx[2] ^= t; sx[3] = rotl(sx[3], 45); return r; }
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r"); if (!f || fscanf(f, "%d", &A) != 1) return 1;
    for (int i = 0; i < A; i++) { if (fscanf(f, "%d %d %d", &m1[i], &m2[i], &deg[i]) != 3) return 1;
        for (int j = 0; j < deg[i]; j++) if (fscanf(f, "%d", &nb[i][j]) != 1) return 1; }
    double r1 = atof(argv[2]), r2 = atof(argv[3]); double r3 = argc > 8 ? atof(argv[8]) : 0;  /* density of coins coded as tens in m1, m2 */ long want = atol(argv[4]); double maxg = atof(argv[5]);
    uint64_t seed = strtoull(argv[6], 0, 10); int T0 = argc > 7 ? atoi(argv[7]) : 200;
    for (int i = 0; i < 4; i++) { seed += 0x9E3779B97F4A7C15ULL; uint64_t z = seed; z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
        z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL; sx[i] = z ^ (z >> 31); }
    for (int i = 0; i < A; i++) {
        double pb[4] = {0, 0, 0, 0};
        int n1 = m1[i] % 10, n2 = m2[i] % 10, n3 = m1[i] / 10 + m2[i] / 10, nt = n1 + n2 + n3;   /* n3 coins have density r3 */
        for (int c = 0; c < (1 << nt); c++) { double p = 1; int b = 0;
            for (int t = 0; t < nt; t++) { double r = t < n1 ? r1 : (t < n1 + n2 ? r2 : r3); if (c >> t & 1) { p *= r; b++; } else p *= 1 - r; }
            pb[b] += p; }
        for (int x = 0; x < 2; x++) for (int k = 0; k < 8; k++) { double s = 0;
            for (int b = 0; b < 4; b++) { int n = k + b; if (x ? (n >= 3 && n <= 5) : (n == 4 || n == 5)) s += pb[b]; }
            thr[i][x][k] = s >= 1 ? ~0ULL : (uint64_t)(s * 18446744073709551616.0); }
    }
    unsigned char x[MAXA], y[MAXA]; long deaths = 0, bust6 = 0, over6 = 0, bust1 = 0; double expo = 0, popsum = 0;
    int hist[8], half = (A + 1) / 2, thr7 = (int)ceil(0.7 * A - 1e-9);   /* routes: see qsd.c */
    while (deaths < want && expo < maxg) {
        int pop = 0;
        for (int i = 0; i < A; i++) { x[i] = rnd() >> 63; pop += x[i]; }
        long t = 0; for (int i = 0; i < 8; i++) hist[i] = pop;
        while (pop > 0 && expo < maxg) {
            int np = 0;
            for (int i = 0; i < A; i++) { int k = 0; for (int j = 0; j < deg[i]; j++) k += x[nb[i][j]];
                y[i] = rnd() < thr[i][x[i]][k]; np += y[i]; }
            for (int i = 0; i < A; i++) x[i] = y[i];
            t++;
            for (int i = 6; i > 0; i--) hist[i] = hist[i - 1];
            hist[0] = np;                                   /* hist[0] = new population, hist[1] = before, ... */
            if (t > T0) { expo += 1; popsum += pop; if (np == 0) { deaths++;
                int b = 0, o = 0;                           /* last 6 living states hist[1..6], last 6 transitions */
                for (int i = 1; i <= 6; i++) { if (hist[i] - hist[i - 1] >= half) b = 1; if (hist[i] >= thr7) o = 1; }
                bust6 += b; over6 += o; bust1 += (hist[1] >= half); } }
            pop = np;
        }
    }
    printf("%d %ld %.0f %.5f %.5f %.5f %.4f %.4f %.4f\n", A, deaths, expo, log(expo / deaths), 1 / sqrt((double)deaths), popsum / expo / A,
           (double)bust6 / deaths, (double)over6 / deaths, (double)bust1 / deaths);
    return 0;
}
