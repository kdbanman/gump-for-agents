/* fd2.c: the joint one-step map (P, B) -> (P', B') of a face and the layer beneath (C = third layer recorded for
   the closure test).  Same stepper as fd.c (validated the same way: validate.py with FD=./fd2).
   gcc -O3 -march=native -o fd2 fd2.c -lm
   fd2 GEOM trace SEED REPLICA GENS OUT
   fd2 GEOM map SEED SECONDS PSTAR BSTAR OUT
   map: soup 0.375, burn-in 1000, restart at the first empty face (as fd.c).  For every face-generation after
   burn-in with previous state (P, B, C): cell (P, B) accumulates n, P', B', P'^2, B'^2, P'B', C, C^2, C P', C B'.
   Also the joint histogram of (P', B') one generation after |P - PSTAR| <= 1, |B - BSTAR| <= 2 ("jump").      */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <math.h>
typedef uint64_t u64;
typedef u64 vec __attribute__((vector_size(32)));
#define NR 256
#define MAXN 1024
#define MAXF 8
#define MAXA 128
#define BURN 1000
#define NP 128
static int N, F, A[3][MAXF], nb[MAXN][12], fc[3][MAXF][MAXA];
static vec *S, *T;
static u64 rs;
static inline u64 rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs * 0x2545F4914F6CDD1DULL; }
#define W(v, w) (((u64 *)&(v))[w])
static void step(void) {
    for (int i = 0; i < N; i++) {
        const int *n = nb[i];
        vec n0 = S[n[0]], n1 = S[n[1]], n2 = S[n[2]], n3 = S[n[3]], n4 = S[n[4]], n5 = S[n[5]];
        vec n6 = S[n[6]], n7 = S[n[7]], n8 = S[n[8]], n9 = S[n[9]], n10 = S[n[10]], n11 = S[n[11]];
        vec s1, c1, s2, c2, s3, c3, s4, c4, sA, cA, b0, cB, t1, d1, t2, d2, b1, d3, b2, b3, t_;
#define FA(s, c, x, y, z) { t_ = (x) ^ (y); s = t_ ^ (z); c = ((x) & (y)) | (t_ & (z)); }
#define HA(s, c, x, y) { s = (x) ^ (y); c = (x) & (y); }
        FA(s1, c1, n0, n1, n2) FA(s2, c2, n3, n4, n5) FA(s3, c3, n6, n7, n8) FA(s4, c4, n9, n10, n11)
        FA(sA, cA, s1, s2, s3) HA(b0, cB, sA, s4)
        FA(t1, d1, c1, c2, c3) FA(t2, d2, c4, cA, cB)
        HA(b1, d3, t1, t2)
        FA(b2, b3, d1, d2, d3)
        vec x = S[i];
        vec n45 = ~b3 & b2 & ~b1;
        vec n3_ = ~b3 & ~b2 & b1 & b0;
        T[i] = n45 | (x & n3_);
    }
    vec *q = S; S = T; T = q;
    memset(&S[N], 0, sizeof(vec));
}
static void soup(int r) {
    int w = r >> 6; u64 m = 1ULL << (r & 63);
    for (int i = 0; i < N; i++) {
        u64 x = rnd() >> 20;
        if (((x | (x >> 1)) & (x >> 2)) & 1) W(S[i], w) |= m; else W(S[i], w) &= ~m;
    }
}
static void count(int l, int f, uint8_t *out) {
    vec c[7]; for (int k = 0; k < 7; k++) c[k] = (vec){0, 0, 0, 0};
    for (int j = 0; j < A[l][f]; j++) { vec carry = S[fc[l][f][j]]; for (int k = 0; k < 7; k++) { vec t = c[k] & carry; c[k] ^= carry; carry = t; } }
    for (int w = 0; w < 4; w++) {
        u64 c0 = W(c[0], w), c1 = W(c[1], w), c2 = W(c[2], w), c3 = W(c[3], w), c4 = W(c[4], w), c5 = W(c[5], w), c6 = W(c[6], w);
        for (int b = 0; b < 64; b++)
            out[w * 64 + b] = ((c0 >> b) & 1) | (((c1 >> b) & 1) << 1) | (((c2 >> b) & 1) << 2) | (((c3 >> b) & 1) << 3) | (((c4 >> b) & 1) << 4) | (((c5 >> b) & 1) << 5) | (((c6 >> b) & 1) << 6);
    }
}
int main(int argc, char **argv) {
    if (argc < 4) return 1;
    FILE *g = fopen(argv[1], "r");
    if (!g || fscanf(g, "%d %d", &N, &F) != 2) return 2;
    for (int i = 0; i < N; i++) for (int j = 0; j < 12; j++) if (fscanf(g, "%d", &nb[i][j]) != 1) return 2;
    for (int l = 0; l < 3; l++) for (int f = 0; f < F; f++) {
        if (fscanf(g, "%d", &A[l][f]) != 1) return 2;
        for (int j = 0; j < A[l][f]; j++) if (fscanf(g, "%d", &fc[l][f][j]) != 1) return 2;
    }
    fclose(g);
    S = aligned_alloc(32, (MAXN + 1) * sizeof(vec)); T = aligned_alloc(32, (MAXN + 1) * sizeof(vec));
    memset(S, 0, (MAXN + 1) * sizeof(vec)); memset(T, 0, (MAXN + 1) * sizeof(vec));
    rs = strtoull(argv[3], 0, 10) * 0x9E3779B97F4A7C15ULL + 0x1234567ULL;
    for (int i = 0; i < 20; i++) rnd();
    for (int r = 0; r < NR; r++) soup(r);
    if (!strcmp(argv[2], "trace")) {
        int R = atoi(argv[4]), G = atoi(argv[5]);
        FILE *o = fopen(argv[6], "wb");
        uint8_t buf[MAXN];
        for (int t = 0; t <= G; t++) {
            for (int i = 0; i < N; i++) buf[i] = (W(S[i], R >> 6) >> (R & 63)) & 1;
            fwrite(buf, 1, N, o);
            step();
        }
        fclose(o);
        return 0;
    }
    double secs = atof(argv[4]); int PS = atoi(argv[5]), BS = atoi(argv[6]);
    static double acc[NP][NP][10]; static u64 jump[NP][NP];
    static uint8_t pP[MAXF][NR], pB[MAXF][NR], pC[MAXF][NR], cur[3][NR], dead[NR];
    static int age[NR];
    u64 exposure = 0, deaths = 0, gen = 0;
    time_t t0 = time(0);
    for (;;) {
        if ((gen & 1023) == 0 && difftime(time(0), t0) >= secs) break;
        for (int r = 0; r < NR; r++) if (age[r] >= BURN) exposure++;
        step(); gen++;
        for (int r = 0; r < NR; r++) age[r]++;
        memset(dead, 0, NR);
        for (int f = 0; f < F; f++) {
            for (int l = 0; l < 3; l++) count(l, f, cur[l]);
            for (int r = 0; r < NR; r++) {
                int P = cur[0][r], B = cur[1][r], C = cur[2][r];
                if (age[r] >= BURN + 2) {
                    int p = pP[f][r], b = pB[f][r], c = pC[f][r];
                    double *a = acc[p][b];
                    a[0] += 1; a[1] += P; a[2] += B; a[3] += P * P; a[4] += B * B; a[5] += P * B;
                    a[6] += c; a[7] += c * c; a[8] += c * P; a[9] += c * B;
                    if (abs(p - PS) <= 1 && abs(b - BS) <= 2) jump[P][B]++;
                    if (P == 0) deaths++;
                }
                if (P == 0) dead[r] = 1;
                pP[f][r] = P; pB[f][r] = B; pC[f][r] = C;
            }
        }
        for (int r = 0; r < NR; r++) if (dead[r]) { soup(r); age[r] = 0; }
    }
    FILE *o = fopen(argv[7], "w");
    fprintf(o, "N %d F %d A %d AB %d AC %d gen %llu exposure %llu deaths %llu PS %d BS %d\n", N, F, A[0][0], A[1][0], A[2][0],
            (unsigned long long)gen, (unsigned long long)exposure, (unsigned long long)deaths, PS, BS);
    for (int p = 0; p < NP; p++) for (int b = 0; b < NP; b++) if (acc[p][b][0] > 0) {
        fprintf(o, "c %d %d", p, b);
        for (int k = 0; k < 10; k++) fprintf(o, " %.0f", acc[p][b][k]);
        fprintf(o, "\n");
    }
    for (int p = 0; p < NP; p++) for (int b = 0; b < NP; b++) if (jump[p][b]) fprintf(o, "j %d %d %llu\n", p, b, (unsigned long long)jump[p][b]);
    fclose(o);
    return 0;
}
