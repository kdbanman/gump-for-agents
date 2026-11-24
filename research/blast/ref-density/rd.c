/* rd.c -- ref-density: an independent stepper and dart process for the noisy octahedral hull.
 *
 * Written from reference/oracle.py (neighbourhood, rule) and from the prose of
 * research/blast/noisy/README.md ("The chain, exactly") and research/blast/density/README.md.
 * No code from nz.c, nzd.c or research/audit/blastnoisy/.
 *
 * Vessel: every doubled-coordinate cell p (exactly one odd coordinate) with |x|+|y|+|z| <= R, R odd;
 * the oracle's 12 neighbours; a neighbour outside the hull is dead; rule B45/S345.
 * Faces: f = sign vector d_f, face cells d_f.p = R; depth of p under f = (R - d_f.p)/2. Face 0 = (+,+,+) is watched.
 * 512 independent hulls ("lanes"), bit-sliced: S[cell*W + w] bit b = lane 64w+b.
 *
 * Noise (law, exactly): region N = cells at depth >= D0 under face 0 and >= 3 under each of the other 7 faces.
 * B = smallest power of two >= 4|N|. After every generation, in every lane independently, M darts are thrown
 * one after another at B squares, i.i.d. uniform; |N| squares are the cells of N, the rest are empty.
 * Implemented in law-equivalent form: K ~ Binomial(M, |N|/B) darts land on N (inversion of the exact pmf),
 * then K i.i.d. uniform cells of N in sequence; each such dart sets its cell to a coin:
 *   f            fair coin, P(alive) = 1/2 exactly (one bit of a fresh 32-bit draw)
 *   p:P          every depth at P(alive) = round(P 2^32)/2^32
 *   b:1:P1,2:P2,...,*:Pdeep   bias by depth under the watched face (depth k, '*' = every depth not listed)
 *   c            copy: the CURRENT state (darts earlier in the same generation included) of a uniformly
 *                chosen cell of N at the same depth under face 0 (the dart's own cell included)
 *   w            copy: the same, from the whole hull layer at that depth under face 0 (all hull cells with
 *                x+y+z = R - 2k, rim and other faces' cells included)
 * M = 0 is gump. eps = M/B. Darts are thrown only in lanes whose life did not end at this generation.
 *
 * Life protocol: lanes start as soups (each cell alive w.p. round(0.35 2^32)/2^32), age 0. Generation: step all
 * lanes; age += 1; a lane-generation is exposure iff age > 200; if any face is empty the life ends (a death of the
 * watched face iff face 0 is empty, alone or tied, counted iff age > 200) and the lane is re-seeded at age 0;
 * otherwise darts. ln tau = ln(exposure/deaths) +- 1/sqrt(deaths). No settled-life guard (max age reported).
 *
 * Diagnostics (all over exposure lane-generations, after the step and before darts):
 *   DENS: mean density of core k (= N cells at depth k for D0 = 1, i.e. depth k under face 0, >= 3 under others)
 *         and of the full layer k (all hull cells at depth k under face 0).
 *   BYF: for lanes with face population F <= 20: counts of samples, sum of core-1 and full-1 live counts by F.
 *   DESC k: descents of the watched face from >= 16 live cells (armed at an exposure generation) to <= k, and how
 *         many of them ended in the watched face's death before it was back at >= 16 (descents cut by another
 *         face's death are counted in neither 'died' nor 'back'; reported separately).
 *   LAG (first LAGGENS generations, all lanes): Pearson correlation over pairs within one life, both times
 *         exposure, of X(t-L) and Y(t) for L = 0..8, for (X,Y) in (full1,F), (F,full1), (core1,F), (F,core1),
 *         (F,F), (full1,full1), (core1,core1).
 *
 * Usage:
 *   rd R validate SEED GENS             no noise, no re-seeding, prints lanes 0..2 (hex, cell order) each gen
 *   rd R cells                          prints the cell table
 *   rd R run SEED GENS M D0 COIN [LAGGENS] [CKPT]
 *   env RD_NEGCTL=1: one neighbour of axis-0 cells replaced by the edge-sharing coplanar face (negative control)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>

typedef uint64_t u64;
#define W 8
#define LANES (64 * W)
#define MAXC 6000

/* ---------- RNG: xoshiro256** seeded with splitmix64 ---------- */
static u64 rs[4];
static inline u64 rotl(u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static inline u64 rnd(void) {
    u64 r = rotl(rs[1] * 5, 7) * 9, t = rs[1] << 17;
    rs[2] ^= rs[0]; rs[3] ^= rs[1]; rs[1] ^= rs[2]; rs[0] ^= rs[3]; rs[2] ^= t; rs[3] = rotl(rs[3], 45);
    return r;
}
static void seedrng(u64 s) {
    for (int i = 0; i < 4; i++) {
        s += 0x9e3779b97f4a7c15ULL; u64 z = s;
        z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL; z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
        rs[i] = z ^ (z >> 31);
    }
}
static inline uint32_t unif(uint32_t n) { /* exact uniform on [0,n) (Lemire) */
    u64 m = (rnd() >> 32) * (u64)n; uint32_t l = (uint32_t)m;
    if (l < n) { uint32_t t = (uint32_t)(-n) % n; while (l < t) { m = (rnd() >> 32) * (u64)n; l = (uint32_t)m; } }
    return (uint32_t)(m >> 32);
}

/* ---------- geometry ---------- */
static int R, NC, OFF, DIM;
static int CX[MAXC], CY[MAXC], CZ[MAXC], AX[MAXC];
static int *lut;
static int nbr[MAXC * 12];
static int sg[8][3];
static int dep[8][MAXC];
static int face[8][200], nface[8];

static int L(int x, int y, int z) {
    if (abs(x) + abs(y) + abs(z) > R) return -1;
    return lut[((x + OFF) * DIM + (y + OFF)) * DIM + (z + OFF)];
}
static void geometry(int negctl) {
    OFF = R + 4; DIM = 2 * R + 9;
    lut = malloc(sizeof(int) * DIM * DIM * DIM);
    for (int i = 0; i < DIM * DIM * DIM; i++) lut[i] = -1;
    NC = 0;
    for (int x = -R; x <= R; x++) for (int y = -R; y <= R; y++) for (int z = -R; z <= R; z++) {
        int odd = (x & 1) + (y & 1) + (z & 1);
        if (odd != 1 || abs(x) + abs(y) + abs(z) > R) continue;
        CX[NC] = x; CY[NC] = y; CZ[NC] = z; AX[NC] = (x & 1) ? 0 : (y & 1) ? 1 : 2;
        lut[((x + OFF) * DIM + (y + OFF)) * DIM + (z + OFF)] = NC; NC++;
    }
    for (int c = 0; c < NC; c++) {
        int a = AX[c], b = (a + 1) % 3, cc = (a + 2) % 3; if (b > cc) { int t = b; b = cc; cc = t; }
        int offs[12][3], k = 0;
        for (int sb = 2; sb >= -2; sb -= 4) for (int sc = 2; sc >= -2; sc -= 4) {
            int o[3] = {0, 0, 0}; o[b] = sb; o[cc] = sc; memcpy(offs[k++], o, sizeof o);
        }
        for (int sa = 1; sa >= -1; sa -= 2) for (int ti = 0; ti < 2; ti++) for (int st = 1; st >= -1; st -= 2) {
            int t = ti ? cc : b; int o[3] = {0, 0, 0}; o[a] = sa; o[t] = st; memcpy(offs[k++], o, sizeof o);
        }
        if (negctl && a == 0) { offs[0][1] = 2; offs[0][2] = 0; } /* corner-touching -> edge-sharing coplanar */
        int p[3] = {CX[c], CY[c], CZ[c]};
        for (int j = 0; j < 12; j++) {
            int q = L(p[0] + offs[j][0], p[1] + offs[j][1], p[2] + offs[j][2]);
            nbr[12 * c + j] = q < 0 ? NC : q;     /* NC = the always-dead cell */
        }
    }
    int f = 0;
    for (int s0 = 1; s0 >= -1; s0 -= 2) for (int s1 = 1; s1 >= -1; s1 -= 2) for (int s2 = 1; s2 >= -1; s2 -= 2) {
        sg[f][0] = s0; sg[f][1] = s1; sg[f][2] = s2; nface[f] = 0;
        for (int c = 0; c < NC; c++) {
            int s = s0 * CX[c] + s1 * CY[c] + s2 * CZ[c];
            dep[f][c] = (R - s) / 2;
            if (dep[f][c] == 0) face[f][nface[f]++] = c;
        }
        f++;
    }
}

/* ---------- state and step ---------- */
static u64 *S, *T;
#define FA(a, b, c, s, cy) do { u64 _t = (a) ^ (b); s = _t ^ (c); cy = ((a) & (b)) | (_t & (c)); } while (0)
static void step(void) {
    for (int c = 0; c < NC; c++) {
        const int *nb = nbr + 12 * c;
        const u64 *p0 = S + W * nb[0], *p1 = S + W * nb[1], *p2 = S + W * nb[2], *p3 = S + W * nb[3];
        const u64 *p4 = S + W * nb[4], *p5 = S + W * nb[5], *p6 = S + W * nb[6], *p7 = S + W * nb[7];
        const u64 *p8 = S + W * nb[8], *p9 = S + W * nb[9], *p10 = S + W * nb[10], *p11 = S + W * nb[11];
        const u64 *xs = S + W * c; u64 *o = T + W * c;
        for (int w = 0; w < W; w++) {
            u64 s1, c1, s2, c2, s3, c3, s4, c4, t1, d1, b0, d2, u1, e1, u2, e2, b1, e3, b2, b3;
            FA(p0[w], p1[w], p2[w], s1, c1); FA(p3[w], p4[w], p5[w], s2, c2);
            FA(p6[w], p7[w], p8[w], s3, c3); FA(p9[w], p10[w], p11[w], s4, c4);
            FA(s1, s2, s3, t1, d1); b0 = t1 ^ s4; d2 = t1 & s4;                 /* weight 1 */
            FA(c1, c2, c3, u1, e1); FA(c4, d1, d2, u2, e2); b1 = u1 ^ u2; e3 = u1 & u2; /* weight 2 */
            FA(e1, e2, e3, b2, b3);                                            /* weight 4, 8 */
            u64 x = xs[w];
            o[w] = ~b3 & ((b2 & ~b1) | (x & ~b2 & b1 & b0));  /* n in {4,5}, or alive and n == 3 */
        }
    }
    u64 *t = S; S = T; T = t;
}
static inline int getb(int c, int l) { return (S[W * c + (l >> 6)] >> (l & 63)) & 1; }
static inline void setb(int c, int l, int v) {
    u64 bit = 1ULL << (l & 63);
    if (v) S[W * c + (l >> 6)] |= bit; else S[W * c + (l >> 6)] &= ~bit;
}
static void lanecount(const int *cells, int n, int *out) {
    for (int w = 0; w < W; w++) {
        u64 b[8] = {0};
        for (int i = 0; i < n; i++) {
            u64 cy = S[W * cells[i] + w];
            for (int j = 0; j < 8 && cy; j++) { u64 t = b[j] & cy; b[j] ^= cy; cy = t; }
        }
        for (int l = 0; l < 64; l++) {
            int v = 0; for (int j = 0; j < 8; j++) v |= (int)((b[j] >> l) & 1) << j;
            out[w * 64 + l] = v;
        }
    }
}
static const uint64_t SOUP = 1503238554ULL; /* round(0.35 * 2^32) */
static void soup(int l) { for (int c = 0; c < NC; c++) setb(c, l, (rnd() >> 32) < SOUP); }

/* ---------- groups ---------- */
static int NN, Ncell[MAXC], inN[MAXC];
static int core[40][MAXC], ncore[40], full[40][MAXC], nfull[40];
static int core1[64], ncore1, full1[200], nfull1;

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "see header\n"); return 1; }
    R = atoi(argv[1]); const char *mode = argv[2];
    geometry(getenv("RD_NEGCTL") != NULL);
    S = calloc((size_t)W * (NC + 1), 8); T = calloc((size_t)W * (NC + 1), 8);
    if (!strcmp(mode, "cells")) {
        printf("NC %d\n", NC);
        for (int c = 0; c < NC; c++) printf("%d %d %d\n", CX[c], CY[c], CZ[c]);
        return 0;
    }
    if (!strcmp(mode, "validate")) {
        seedrng(strtoull(argv[3], 0, 10)); int gens = atoi(argv[4]);
        for (int l = 0; l < LANES; l++) soup(l);
        printf("NC %d\n", NC);
        for (int c = 0; c < NC; c++) printf("C %d %d %d\n", CX[c], CY[c], CZ[c]);
        int F[LANES];
        for (int g = 0; g <= gens; g++) {
            if (g) step();
            lanecount(face[0], nface[0], F);
            for (int l = 0; l < 3; l++) {
                printf("G %d %d %d ", g, l, F[l]);
                for (int f = 0; f < 8; f++) { int e = 1; for (int i = 0; i < nface[f]; i++) if (getb(face[f][i], l)) { e = 0; break; } putchar('0' + e); }
                putchar(' ');
                for (int c = 0; c < NC; c += 4) { int v = 0; for (int j = 0; j < 4 && c + j < NC; j++) v |= getb(c + j, l) << j; putchar("0123456789abcdef"[v]); }
                putchar('\n');
            }
        }
        return 0;
    }
    if (strcmp(mode, "run")) { fprintf(stderr, "unknown mode\n"); return 1; }
    u64 seed = strtoull(argv[3], 0, 10); long gens = atol(argv[4]); int M = atoi(argv[5]); int D0 = atoi(argv[6]);
    const char *coin = argv[7]; long laggens = argc > 8 ? atol(argv[8]) : 0; long ckpt = argc > 9 ? atol(argv[9]) : 500000;
    seedrng(seed);
    /* groups */
    NN = 0;
    for (int c = 0; c < NC; c++) {
        int ok = dep[0][c] >= D0; for (int f = 1; f < 8; f++) if (dep[f][c] < 3) ok = 0;
        inN[c] = ok; if (ok) Ncell[NN++] = c;
        int k = dep[0][c];
        int corek = 1; for (int f = 1; f < 8; f++) if (dep[f][c] < 3) corek = 0;
        if (corek) core[k][ncore[k]++] = c;
        full[k][nfull[k]++] = c;
    }
    ncore1 = ncore[1]; memcpy(core1, core[1], sizeof(int) * ncore1); nfull1 = nfull[1]; memcpy(full1, full[1], sizeof(int) * nfull1);
    int B = 1; while (B < 4 * NN) B *= 2;
    /* coin */
    int cmode = 0; /* 0 bias, 1 copy core, 2 copy whole layer */
    double pk[40]; for (int k = 0; k < 40; k++) pk[k] = 0.5;
    if (!strcmp(coin, "f")) {}
    else if (!strncmp(coin, "p:", 2)) { double p = atof(coin + 2); for (int k = 0; k < 40; k++) pk[k] = p; }
    else if (!strncmp(coin, "b:", 2)) {
        char buf[512]; strncpy(buf, coin + 2, 511); buf[511] = 0; double deep = -1; int set[40] = {0};
        for (char *tok = strtok(buf, ","); tok; tok = strtok(0, ",")) {
            char *colon = strchr(tok, ':'); *colon = 0; double p = atof(colon + 1);
            if (tok[0] == '*') deep = p; else { int k = atoi(tok); pk[k] = p; set[k] = 1; }
        }
        for (int k = 0; k < 40; k++) if (!set[k] && deep >= 0) pk[k] = deep;
    }
    else if (!strcmp(coin, "c")) cmode = 1;
    else if (!strcmp(coin, "w")) cmode = 2;
    else { fprintf(stderr, "bad coin\n"); return 1; }
    u64 thr[MAXC];
    for (int c = 0; c < NC; c++) { double p = pk[dep[0][c]]; thr[c] = (u64)llround(p * 4294967296.0); }
    /* binomial(M, NN/B) cdf */
    double *cdf = malloc(sizeof(double) * (M + 1)); { double p = (double)NN / B, acc = 0;
        for (int k = 0; k <= M; k++) { double lp = lgamma(M + 1.0) - lgamma(k + 1.0) - lgamma(M - k + 1.0) + k * log(p) + (M - k) * log1p(-p); acc += exp(lp); cdf[k] = acc; }
        cdf[M] = 2.0; }
    double q = 1 - pow(1 - 1.0 / B, M);
    printf("SETUP R %d NC %d face %d NN %d B %d M %d eps %.6f q_hit %.6f D0 %d coin %s seed %llu gens %ld\n", R, NC, nface[0], NN, B, M, (double)M / B, q, D0, coin, (unsigned long long)seed, gens);
    printf("GROUPS core:"); for (int k = 0; k <= R; k++) printf(" %d", ncore[k]); printf("  full:"); for (int k = 0; k <= R; k++) printf(" %d", nfull[k]); printf("\n");
    if (cmode == 0) { printf("BIAS"); for (int k = 0; k <= 10; k++) printf(" %d:%.6f", k, thr[full[k][0]] / 4294967296.0); printf("\n"); }
    fflush(stdout);
    /* state */
    static int age[LANES], F[LANES], C1[LANES], L1[LANES], armed[LANES], minlev[LANES];
    for (int l = 0; l < LANES; l++) { soup(l); age[l] = 0; armed[l] = 0; }
    double expo = 0, deaths = 0, deaths_any = 0, deaths_other = 0;
    double dens_core[40] = {0}, dens_full[40] = {0};
    double byf_n[64] = {0}, byf_c1[64] = {0}, byf_l1[64] = {0}, byf_c1sq[64] = {0};
    double fhist[200] = {0};
    double desc[17] = {0}, died[17] = {0}, cut[17] = {0};
    /* lag accumulators: 7 pairs x 9 lags: n, sx, sy, sxx, syy, sxy */
    double lag[7][9][6]; memset(lag, 0, sizeof lag);
    static int hF[LANES][9], hL[LANES][9], hC[LANES][9];
    long maxage = 0;
    for (long g = 1; g <= gens; g++) {
        step();
        u64 cnt[W], emp[W], wdead[W];
        for (int w = 0; w < W; w++) { cnt[w] = 0; emp[w] = 0; }
        for (int l = 0; l < LANES; l++) { age[l]++; if (age[l] > 200) cnt[l >> 6] |= 1ULL << (l & 63); if (age[l] > maxage) maxage = age[l]; }
        for (int f = 0; f < 8; f++) for (int w = 0; w < W; w++) {
            u64 o = 0; for (int i = 0; i < nface[f]; i++) o |= S[W * face[f][i] + w];
            if (f == 0) wdead[w] = ~o;
            emp[w] |= ~o;
        }
        for (int w = 0; w < W; w++) {
            expo += __builtin_popcountll(cnt[w]);
            deaths += __builtin_popcountll(wdead[w] & cnt[w]);
            deaths_any += __builtin_popcountll(emp[w] & cnt[w]);
        }
        /* densities over exposure */
        for (int k = 1; k <= 8 && k <= R; k++) {
            for (int i = 0; i < ncore[k]; i++) for (int w = 0; w < W; w++) dens_core[k] += __builtin_popcountll(S[W * core[k][i] + w] & cnt[w]);
            if (k <= 3) for (int i = 0; i < nfull[k]; i++) for (int w = 0; w < W; w++) dens_full[k] += __builtin_popcountll(S[W * full[k][i] + w] & cnt[w]);
        }
        lanecount(face[0], nface[0], F);
        int dolag = g <= laggens;
        if (dolag) { lanecount(core1, ncore1, C1); lanecount(full1, nfull1, L1); }
        for (int l = 0; l < LANES; l++) {
            int counted = age[l] > 200, f = F[l];
            if (counted) fhist[f] += 1;
            if (counted && f <= 20) {
                int c1v, l1v;
                if (dolag) { c1v = C1[l]; l1v = L1[l]; }
                else { c1v = 0; for (int i = 0; i < ncore1; i++) c1v += getb(core1[i], l); l1v = 0; for (int i = 0; i < nfull1; i++) l1v += getb(full1[i], l); }
                byf_n[f] += 1; byf_c1[f] += c1v; byf_l1[f] += l1v; byf_c1sq[f] += (double)c1v * c1v;
            }
            /* descents */
            int ended = (emp[l >> 6] >> (l & 63)) & 1;
            if (f >= 16) { armed[l] = counted; minlev[l] = 99; }
            else if (armed[l] && f < minlev[l]) {
                for (int k = f; k < minlev[l] && k <= 15; k++) desc[k] += 1;
                minlev[l] = f;
            }
            if (ended && armed[l] && minlev[l] <= 15) {
                int wd = (wdead[l >> 6] >> (l & 63)) & 1;
                for (int k = minlev[l]; k <= 15; k++) { if (wd) died[k] += 1; else cut[k] += 1; }
            }
            if (dolag) {
                int a = age[l];
                for (int j = 8; j > 0; j--) { hF[l][j] = hF[l][j - 1]; hL[l][j] = hL[l][j - 1]; hC[l][j] = hC[l][j - 1]; }
                hF[l][0] = f; hL[l][0] = L1[l]; hC[l][0] = C1[l];
                for (int Lg = 0; Lg <= 8; Lg++) {
                    if (a - Lg <= 200) break;
                    double xs[7] = {hL[l][Lg], hF[l][Lg], hC[l][Lg], hF[l][Lg], hF[l][Lg], hL[l][Lg], hC[l][Lg]};
                    double ys[7] = {f, L1[l], f, C1[l], f, L1[l], C1[l]};
                    for (int p = 0; p < 7; p++) { double *A = lag[p][Lg]; A[0] += 1; A[1] += xs[p]; A[2] += ys[p]; A[3] += xs[p] * xs[p]; A[4] += ys[p] * ys[p]; A[5] += xs[p] * ys[p]; }
                }
            }
            if (ended) { soup(l); age[l] = 0; armed[l] = 0; minlev[l] = 99; }
        }
        /* darts */
        if (M > 0) for (int l = 0; l < LANES; l++) {
            if (age[l] == 0) continue;
            double u = (rnd() >> 11) * 0x1.0p-53; int K = 0; while (cdf[K] <= u) K++;
            for (int j = 0; j < K; j++) {
                int c = Ncell[unif(NN)], v;
                if (cmode == 0) v = (rnd() >> 32) < thr[c];
                else { int k = dep[0][c]; v = cmode == 1 ? getb(core[k][unif(ncore[k])], l) : getb(full[k][unif(nfull[k])], l); }
                setb(c, l, v);
            }
        }
        if (g % ckpt == 0 || g == gens) {
            printf("CKPT %ld expo %.0f deaths %.0f lntau %.4f err %.4f any %.0f\n", g, expo, deaths, log(expo / deaths), 1 / sqrt(deaths), deaths_any);
            fflush(stdout);
        }
    }
    printf("RESULT R %d M %d B %d D0 %d coin %s seed %llu gens %ld expo %.0f deaths %.0f lntau %.4f err %.4f deaths_any8 %.0f maxage %ld\n",
           R, M, B, D0, coin, (unsigned long long)seed, gens, expo, deaths, log(expo / deaths), 1 / sqrt(deaths), deaths_any, maxage);
    { double s = 0, s2 = 0, n = 0; for (int f = 0; f < 200; f++) { n += fhist[f]; s += f * fhist[f]; s2 += (double)f * f * fhist[f]; }
      printf("FACE mean %.4f sd %.4f\n", s / n, sqrt(s2 / n - (s / n) * (s / n))); }
    for (int k = 1; k <= 8 && k <= R; k++) printf("DENS core %d n %d %.5f\n", k, ncore[k], ncore[k] ? dens_core[k] / (expo * ncore[k]) : 0);
    for (int k = 1; k <= 3; k++) printf("DENS full %d n %d %.5f\n", k, nfull[k], dens_full[k] / (expo * nfull[k]));
    for (int f = 0; f <= 20; f++) if (byf_n[f] > 0) printf("BYF %d n %.0f core1 %.5f full1 %.5f core1var %.5f\n", f, byf_n[f], byf_c1[f] / (byf_n[f] * ncore1), byf_l1[f] / (byf_n[f] * nfull1), byf_c1sq[f] / byf_n[f] - pow(byf_c1[f] / byf_n[f], 2));
    for (int k = 0; k <= 15; k++) printf("DESC %d desc %.0f died %.0f cut %.0f\n", k, desc[k], died[k], cut[k]);
    if (laggens) {
        const char *nm[7] = {"full1->F", "F->full1", "core1->F", "F->core1", "F->F", "full1->full1", "core1->core1"};
        for (int p = 0; p < 7; p++) { printf("LAG %s", nm[p]);
            for (int Lg = 0; Lg <= 8; Lg++) { double *A = lag[p][Lg], n = A[0];
                double cov = A[5] / n - A[1] / n * A[2] / n, vx = A[3] / n - pow(A[1] / n, 2), vy = A[4] / n - pow(A[2] / n, 2);
                printf(" %+.4f", cov / sqrt(vx * vy)); }
            printf("\n"); }
    }
    return 0;
}
