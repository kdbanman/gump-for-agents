// st4.c (review of dying round 4): an independent bit-sliced gump stepper on the octahedral vessel of geom.py, with
// renewal lives, excursions of each hull face's population and three ways of catching a depleted face.
// Shares no code with research/dying/ex4.c or research/audit/dying/r3_ex.c (written from docs/AUTOMATON.md and the
// round-4 definitions in research/dying/PREDICTIONS.md).
//
//   st4 GRAPH trace SEED GENS                 lane 0's live cell indices at every generation (no restarts)
//   st4 GRAPH run SEED GENS PBAR LEVELS KEEP ATLVL SAMPK OUTPREFIX
//     LEVELS  4 integer thresholds, decreasing (catch at P <= L)
//     KEEP    4 keep probabilities (one draw per excursion, nested as in the study)
//     ATLVL   4 probabilities: at every generation of a lane at age > T0 with P == L_j exactly, write the face state
//             with this probability ("a random moment at the level"; time-weighted)
//     SAMPK   stationary samples: every SAMPK generations, every lane at age > T0, all 8 faces
// Protocol (the study's, re-implemented): 256 lanes, soup Bernoulli(0.4) per cell, T0 = 512; a life ends at the first
// face death (any face empty), or when the state repeats a snapshot taken at a power-of-two age; the lane then
// restarts from a fresh soup. An excursion of face f starts at a generation with P < PBAR whose previous generation
// had P >= PBAR, both at age > T0; it ends recovered (P >= PBAR), dead (P = 0) or censored (life ends otherwise).
// Output files: OUT.cat  per excursion with a kept catch: int32 {lane, face, end, minP, keptmask, P[4]} then u64
//                        states[4][2] (catch at each level, 0 if not kept) then u64 bottom[2] (first generation at the
//                        minimum): 36 + 64 + 16 = 116 bytes
//               OUT.lvl  int32 {lane, face, j, P} u64 state[2]
//               OUT.smp  int32 {lane, face, age, P} u64 state[2]
//               OUT.tab  text: exposure, face deaths, excursion minima by end type
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define W 4
#define NL (W * 64)
typedef uint64_t u64;
static u64 rs;
static u64 rnd(void) { u64 z = (rs += 0x9e3779b97f4a7c15ULL); z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL; z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; return z ^ (z >> 31); }
static double unif(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static int N, A, *nb, fc[8][128];
static u64 *x, *y;

static void soup(int lane) {
    int w = lane / 64; u64 m = 1ULL << (lane % 64);
    for (int i = 0; i < N; i++) { if (unif() < 0.4) x[i * W + w] |= m; else x[i * W + w] &= ~m; }
}
static void state(int f, int lane, u64 st[2]) {
    int w = lane / 64, b = lane % 64; st[0] = st[1] = 0;
    for (int k = 0; k < A; k++) if ((x[fc[f][k] * W + w] >> b) & 1) st[k >> 6] |= 1ULL << (k & 63);
}

int main(int argc, char **argv) {
    FILE *g = fopen(argv[1], "r");
    if (fscanf(g, "%d %d", &N, &A) != 2) return 1;
    nb = malloc(sizeof(int) * N * 12);
    for (int i = 0; i < N * 12; i++) if (fscanf(g, "%d", &nb[i]) != 1) return 1;
    for (int f = 0; f < 8; f++) for (int k = 0; k < A; k++) if (fscanf(g, "%d", &fc[f][k]) != 1) return 1;
    fclose(g);
    int trace = !strcmp(argv[2], "trace");
    rs = strtoull(argv[3], 0, 10) * 0x2545F4914F6CDD1DULL + 12345;
    long long GENS = atoll(argv[4]);
    x = calloc((size_t)(N + 1) * W, 8); y = calloc((size_t)(N + 1) * W, 8);
    u64 *snap = calloc((size_t)N * W, 8);
    for (int l = 0; l < NL; l++) soup(l);
    double PBAR = 0; int LV[4] = {0}; double KP[4] = {0}, AT[4] = {0}; long SAMPK = 1 << 30;
    FILE *fcat = 0, *flvl = 0, *fsmp = 0, *ftab = 0;
    if (!trace) {
        PBAR = atof(argv[5]);
        if (sscanf(argv[6], "%d,%d,%d,%d", &LV[0], &LV[1], &LV[2], &LV[3]) != 4) return 3;
        if (sscanf(argv[7], "%lf,%lf,%lf,%lf", &KP[0], &KP[1], &KP[2], &KP[3]) != 4) return 3;
        if (sscanf(argv[8], "%lf,%lf,%lf,%lf", &AT[0], &AT[1], &AT[2], &AT[3]) != 4) return 3;
        SAMPK = atol(argv[9]);
        char fn[512];
        sprintf(fn, "%s.cat", argv[10]); fcat = fopen(fn, "wb");
        sprintf(fn, "%s.lvl", argv[10]); flvl = fopen(fn, "wb");
        sprintf(fn, "%s.smp", argv[10]); fsmp = fopen(fn, "wb");
        sprintf(fn, "%s.tab", argv[10]); ftab = fopen(fn, "w");
    }
    const long T0 = 512;
    static long age[NL], snapage[NL];
    static int inx[NL][8], prevhi[NL][8], minp[NL][8], kept[NL][8], caught[NL][8], cP[NL][8][4];
    static double ku[NL][8];
    static u64 cst[NL][8][4][2], bst[NL][8][2];
    static long long expo = 0, fdeath = 0, xmin[3][128];   // xmin[end-1][minP]
    static long long nlives[4];
    for (long long gen = 0; gen < GENS; gen++) {
        if (trace) { printf("%lld", gen); for (int i = 0; i < N; i++) if (x[i * W] & 1) printf(" %d", i); printf("\n"); }
        for (int i = 0; i < N; i++) {
            const int *q = nb + i * 12;
            for (int w = 0; w < W; w++) {
                u64 c0 = 0, c1 = 0, c2 = 0, c3 = 0;   // saturating 4-bit counter (c3 = "8 or more")
                for (int k = 0; k < 12; k++) {
                    u64 a = x[q[k] * W + w];
                    u64 t0 = c0 & a; c0 ^= a; u64 t1 = c1 & t0; c1 ^= t0; u64 t2 = c2 & t1; c2 ^= t1; c3 |= t2;
                }
                u64 xi = x[i * W + w];
                u64 n3 = ~c3 & ~c2 & c1 & c0, n45 = ~c3 & c2 & ~c1;   // n == 3; n in {4, 5}
                y[i * W + w] = n45 | (xi & n3);
            }
        }
        { u64 *t = x; x = y; y = t; }
        if (trace) continue;
        for (int l = 0; l < NL; l++) age[l]++;
        long long gabs = gen + 1;
        int sampnow = (gabs % SAMPK) == 0;
        static int P[8][NL];
        for (int f = 0; f < 8; f++) {
            for (int w = 0; w < W; w++) {
                u64 c[7] = {0};
                for (int k = 0; k < A; k++) { u64 car = x[fc[f][k] * W + w]; for (int b = 0; b < 7 && car; b++) { u64 t = c[b] & car; c[b] ^= car; car = t; } }
                for (int b = 0; b < 64; b++) { int p = 0; for (int k = 0; k < 7; k++) p |= (int)((c[k] >> b) & 1) << k; P[f][w * 64 + b] = p; }
            }
        }
        for (int l = 0; l < NL; l++) {
            int ok = age[l] > T0, anydead = 0;
            for (int f = 0; f < 8; f++) {
                int p = P[f][l];
                if (p == 0) anydead = 1;
                if (ok) { expo++; if (p == 0) fdeath++; }
                if (ok && sampnow) { u64 st[2]; state(f, l, st); int32_t h[4] = {l, f, (int32_t)age[l], p}; fwrite(h, 4, 4, fsmp); fwrite(st, 8, 2, fsmp); }
                if (ok) for (int j = 0; j < 4; j++) if (p == LV[j] && AT[j] > 0 && unif() < AT[j]) {
                    u64 st[2]; state(f, l, st); int32_t h[4] = {l, f, j, p}; fwrite(h, 4, 4, flvl); fwrite(st, 8, 2, flvl); }
                int start = 0;
                if (!inx[l][f] && ok && prevhi[l][f] && p < PBAR) {
                    if (p == 0) xmin[1][0]++;
                    else { inx[l][f] = 1; start = 1; minp[l][f] = 999; kept[l][f] = 0; caught[l][f] = 0; ku[l][f] = unif();
                        memset(cst[l][f], 0, sizeof cst[l][f]); memset(bst[l][f], 0, sizeof bst[l][f]); for (int j = 0; j < 4; j++) cP[l][f][j] = -1; }
                }
                if (inx[l][f]) {
                    for (int j = 0; j < 4; j++) if (!((caught[l][f] >> j) & 1) && p <= LV[j]) {
                        caught[l][f] |= 1 << j; cP[l][f][j] = p;
                        if (ku[l][f] < KP[j]) { kept[l][f] |= 1 << j; state(f, l, cst[l][f][j]); }
                    }
                    if (p < minp[l][f]) { minp[l][f] = p; if (kept[l][f]) state(f, l, bst[l][f]); }
                    int en = 0;
                    if (!start) { if (p == 0) en = 2; else if (p >= PBAR) en = 1; }
                    if (start && p == 0) en = 2;
                    if (en) {
                        xmin[en - 1][minp[l][f]]++;
                        if (kept[l][f]) { int32_t h[9] = {l, f, en, minp[l][f], kept[l][f], cP[l][f][0], cP[l][f][1], cP[l][f][2], cP[l][f][3]};
                            fwrite(h, 4, 9, fcat); fwrite(cst[l][f], 8, 8, fcat); fwrite(bst[l][f], 8, 2, fcat); }
                        inx[l][f] = 0;
                    }
                }
                prevhi[l][f] = ok && p >= PBAR;
            }
            // settled: equality with the snapshot (taken at power-of-two ages)
            int w = l / 64, b = l % 64; u64 m = 1ULL << b;
            int settled = 0;
            if (snapage[l]) { settled = 1; for (int i = 0; i < N; i++) if ((x[i * W + w] ^ snap[i * W + w]) & m) { settled = 0; break; } }
            if (anydead || settled) {
                nlives[anydead ? 1 : 2]++;
                for (int f = 0; f < 8; f++) {
                    if (inx[l][f]) { if (P[f][l] != 0) { xmin[2][minp[l][f]]++;
                            if (kept[l][f]) { int32_t h[9] = {l, f, 3, minp[l][f], kept[l][f], cP[l][f][0], cP[l][f][1], cP[l][f][2], cP[l][f][3]};
                                fwrite(h, 4, 9, fcat); fwrite(cst[l][f], 8, 8, fcat); fwrite(bst[l][f], 8, 2, fcat); } }
                        inx[l][f] = 0; }
                    prevhi[l][f] = 0;
                }
                soup(l); age[l] = 0; snapage[l] = 0;
            } else if ((age[l] & (age[l] - 1)) == 0) {
                for (int i = 0; i < N; i++) snap[i * W + w] = (snap[i * W + w] & ~m) | (x[i * W + w] & m);
                snapage[l] = age[l];
            }
        }
    }
    if (!trace) {
        fprintf(ftab, "gens %lld expo %lld fdeath %lld lives_dead %lld lives_settled %lld\n", GENS, expo, fdeath, nlives[1], nlives[2]);
        for (int e = 0; e < 3; e++) for (int p = 0; p < 128; p++) if (xmin[e][p]) fprintf(ftab, "X %d %d %lld\n", e + 1, p, xmin[e][p]);
        fclose(fcat); fclose(flvl); fclose(fsmp); fclose(ftab);
    }
    return 0;
}
