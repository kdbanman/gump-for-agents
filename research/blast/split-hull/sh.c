// sh.c: forward-flux sampler for the death of a face of gump's octahedral hull (research/blast/split-hull).
//
// Vessel: all cells p (doubled coordinates, exactly one odd) with |x|+|y|+|z| <= R, R odd, centred on a cube centre;
// everything outside is dead for ever (T2), so this is the infinite lattice's dynamics for a seed inside the hull.
// Face f (f = 0..7, sign pattern d): the cells with d.p = R. Face 0 is d = (+,+,+): the watched face.
// Stepper: B45/S345 on the 12-neighbour graph, bit-sliced, 64 lanes per word, WMAX words.
// The exact statement of the algorithm is in README.md ("The sampler, exactly"); this file is its implementation.
//
//   gcc -O3 -march=native -o sh sh.c -lm
//   ./sh R SEED M [LAG=1] [NFLIP=1] [STEP=2] [H=0.125] [PATHFILE or -] [CAP=200000]   one replication of the estimator
//        [MODE=0]: 1 = donor swap instead of flips (see perturb())
//        (NFLIP = -f means one flip per f perturbation sites, rounded up; the frozen setting is  M=300000 2 -6 3 0.5 FILE 100000)
//   ./sh R SEED 0 GENS                                    brute force: base run only for GENS generations
//   gcc -O3 -march=native -shared -fPIC -DLIB -o libsh.so sh.c -lm     (validation against reference/oracle.py)
#define _GNU_SOURCE
#include <immintrin.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef uint64_t u64;
#define WMAX 32
#define NL (WMAX * 64)
#define T0 200          // ageing-in of a fresh soup before its exposure counts (the anchors' protocol)
#define TFLAG 100       // age from which the "has been at or above P-bar" flag is tracked
#define SOUP 0.35
#define THR 12          // a word is refreshed when this many of its lanes have finished
#define TMAX 20000      // a trial longer than this is booked as a timeout (and a failure)
#define AGEMAX 100000   // base run: a hull older than this is reseeded and counted (guards settled lives)
#define PMAX 500        // dying paths kept per run (reservoir)

static int R, n, A, NC, NCW, DEPTH;
static int *co, *nb, nf[8], *fcell[8], nS, *S;
static u64 *Xr[8], *X, Fz[WMAX], faceor[8][WMAX], *fmask[8];
static int NS = 2, cs = 0, LAG = 1, NFLIP = 1;   // ring of NS = LAG+1 state arrays; X = Xr[cs] is the present
static uint8_t pop[NL];

// ---------------------------------------------------------------- geometry
int geom_init(int R_, int D_) {
    R = R_; DEPTH = D_;
    int L = 2 * R + 1;
    int *idx = malloc(sizeof(int) * L * L * L);
    for (int i = 0; i < L * L * L; i++) idx[i] = -1;
    co = malloc(sizeof(int) * 3 * L * L * L);
    n = 0;
    for (int pass = 0; pass < 2; pass++) {
        for (int x = -R; x <= R; x++) for (int y = -R; y <= R; y++) for (int z = -R; z <= R; z++) {
            if ((x & 1) + (y & 1) + (z & 1) != 1) continue;
            if (abs(x) + abs(y) + abs(z) > R) continue;
            if ((pass == 0) != (x + y + z == R)) continue;
            idx[((x + R) * L + (y + R)) * L + (z + R)] = n;
            co[3 * n] = x; co[3 * n + 1] = y; co[3 * n + 2] = z; n++;
        }
        if (pass == 0) A = n;
    }
    NC = n + 8 * A; NCW = (NC + 63) / 64;
    nb = malloc(sizeof(int) * 12 * n);
    for (int i = 0; i < n; i++) {
        int *p = co + 3 * i, a = (p[0] & 1) ? 0 : (p[1] & 1) ? 1 : 2, b = (a + 1) % 3, c = (a + 2) % 3, k = 0;
        int off[12][3];
        memset(off, 0, sizeof off);
        for (int sb = 2; sb >= -2; sb -= 4) for (int sc = 2; sc >= -2; sc -= 4) { off[k][b] = sb; off[k][c] = sc; k++; }
        for (int sa = 1; sa >= -1; sa -= 2) for (int t = 0; t < 2; t++) for (int st = 1; st >= -1; st -= 2) {
            off[k][a] = sa; off[k][t ? c : b] = st; k++;
        }
        for (int j = 0; j < 12; j++) {
            int x = p[0] + off[j][0], y = p[1] + off[j][1], z = p[2] + off[j][2], v = -1;
            if (abs(x) <= R && abs(y) <= R && abs(z) <= R) v = idx[((x + R) * L + (y + R)) * L + (z + R)];
            nb[12 * i + j] = v < 0 ? NC : v;
        }
    }
    for (int f = 0; f < 8; f++) {
        int sx = (f & 1) ? -1 : 1, sy = (f & 2) ? -1 : 1, sz = (f & 4) ? -1 : 1;
        fcell[f] = malloc(sizeof(int) * n); nf[f] = 0;
        fmask[f] = calloc(NCW, 8);
        for (int i = 0; i < n; i++)
            if (sx * co[3 * i] + sy * co[3 * i + 1] + sz * co[3 * i + 2] == R) {
                fcell[f][nf[f]++] = i; fmask[f][i >> 6] |= 1ULL << (i & 63);
            }
    }
    S = malloc(sizeof(int) * n); nS = 0;
    int r2 = R - 2 * DEPTH;   // perturbation sites: layer DEPTH beneath face 0, at least two layers beneath every other face
    for (int i = 0; i < n; i++) {
        int *p = co + 3 * i, okk = (p[0] + p[1] + p[2] == r2);
        for (int f = 1; f < 8 && okk; f++) {
            int sx = (f & 1) ? -1 : 1, sy = (f & 2) ? -1 : 1, sz = (f & 4) ? -1 : 1;
            if (sx * p[0] + sy * p[1] + sz * p[2] > R - 4) okk = 0;
        }
        if (okk) S[nS++] = i;
    }
    for (int k = 0; k < NS; k++) {
        Xr[k] = aligned_alloc(64, sizeof(u64) * (size_t)(NC + 1) * WMAX);
        memset(Xr[k], 0, sizeof(u64) * (size_t)(NC + 1) * WMAX);
    }
    cs = 0; X = Xr[0];
    memset(Fz, 0, sizeof Fz);
    free(idx);
    return n;
}

// ---------------------------------------------------------------- stepper
// One generation for words 0..W-1, written into the next array of the ring. Lanes whose bit is set in Fz are frozen:
// nothing of theirs is overwritten in any array of the ring.
// Columns 0..n-1: cells. Columns n+8c..n+8c+7: bit planes of the age of face-0 cell c (generations since it was
// last alive, 0 if alive, saturating at 255).
static void step(int W) {
    u64 *Y = Xr[(cs + 1) % NS];
    u64 c0[WMAX] __attribute__((aligned(64))), c1[WMAX] __attribute__((aligned(64)));
    u64 c2[WMAX] __attribute__((aligned(64))), c3[WMAX] __attribute__((aligned(64)));
    for (int i = 0; i < n; i++) {
        const int *q = nb + 12 * i;
        for (int w = 0; w < W; w++) c0[w] = c1[w] = c2[w] = c3[w] = 0;
        for (int j = 0; j < 12; j++) {
            const u64 *v = X + (size_t)q[j] * WMAX;
            for (int w = 0; w < W; w++) {
                u64 a = v[w], t = c0[w] & a; c0[w] ^= a; a = t;
                t = c1[w] & a; c1[w] ^= a; a = t;
                t = c2[w] & a; c2[w] ^= a; c3[w] |= t;
            }
        }
        const u64 *x = X + (size_t)i * WMAX; u64 *y = Y + (size_t)i * WMAX;
        for (int w = 0; w < W; w++) {
            u64 n45 = ~c3[w] & c2[w] & ~c1[w], n3 = ~c3[w] & ~c2[w] & c1[w] & c0[w];
            u64 nw = n45 | (x[w] & n3);
            y[w] = (nw & ~Fz[w]) | (y[w] & Fz[w]);
        }
    }
    for (int c = 0; c < A; c++) {
        const u64 *al = Y + (size_t)c * WMAX;
        const u64 *p = X + (size_t)(n + 8 * c) * WMAX; u64 *o = Y + (size_t)(n + 8 * c) * WMAX;
        for (int w = 0; w < W; w++) {
            u64 sat = p[w];
            for (int k = 1; k < 8; k++) sat &= p[k * WMAX + w];
            u64 carry = ~sat;
            for (int k = 0; k < 8; k++) {
                u64 v = p[k * WMAX + w], nv = (v ^ carry) & ~al[w];
                carry &= v;
                o[k * WMAX + w] = (nv & ~Fz[w]) | (o[k * WMAX + w] & Fz[w]);
            }
        }
    }
    cs = (cs + 1) % NS; X = Xr[cs];
}

// pop[lane] = population of face 0; faceor[f][w] = OR of face f's cells (bit clear: that lane's face f is empty).
static void observe(int W) {
    u64 s[8][WMAX] __attribute__((aligned(64))), cy[WMAX] __attribute__((aligned(64)));
    memset(s, 0, sizeof s);
    for (int c = 0; c < A; c++) {
        const u64 *v = X + (size_t)c * WMAX;
        for (int w = 0; w < W; w++) cy[w] = v[w];
        for (int k = 0; k < 8; k++)
            for (int w = 0; w < W; w++) { u64 t = s[k][w] & cy[w]; s[k][w] ^= cy[w]; cy[w] = t; }
    }
    for (int w = 0; w < W; w++)
        for (int g = 0; g < 8; g++) {
            u64 acc = 0;
            for (int k = 0; k < 8; k++) acc |= _pdep_u64(s[k][w] >> (8 * g), 0x0101010101010101ULL) << k;
            memcpy(pop + w * 64 + 8 * g, &acc, 8);
        }
    for (int f = 1; f < 8; f++) {
        for (int w = 0; w < W; w++) cy[w] = 0;
        for (int k = 0; k < nf[f]; k++) {
            const u64 *v = X + (size_t)fcell[f][k] * WMAX;
            for (int w = 0; w < W; w++) cy[w] |= v[w];
        }
        for (int w = 0; w < W; w++) faceor[f][w] = cy[w];
    }
}

// ---------------------------------------------------------------- lanes and packed configurations
static void transpose64(u64 a[64]) {   // out[c] bit b = in[b] bit c
    u64 m = 0x00000000FFFFFFFFULL;
    for (int j = 32; j != 0; j >>= 1, m ^= (m << j))
        for (int k = 0; k < 64; k = (k + j + 1) & ~j) {
            u64 t = ((a[k] >> j) ^ a[k + j]) & m;
            a[k + j] ^= t; a[k] ^= t << j;
        }
}
static void word_out_s(int w, u64 *T, int sl) {   // T[b*NCW + blk]: packed configuration of lane w*64+b in ring array sl
    u64 a[64]; const u64 *X = Xr[sl];
    for (int blk = 0; blk < NCW; blk++) {
        for (int c = 0; c < 64; c++) { int col = blk * 64 + c; a[c] = col < NC ? X[(size_t)col * WMAX + w] : 0; }
        transpose64(a);
        for (int b = 0; b < 64; b++) T[(size_t)b * NCW + blk] = a[b];
    }
}
static void word_out(int w, u64 *T) { word_out_s(w, T, cs); }
static void word_in_s(int w, const u64 *T, int sl) {
    u64 a[64]; u64 *X = Xr[sl];
    for (int blk = 0; blk < NCW; blk++) {
        for (int b = 0; b < 64; b++) a[b] = T[(size_t)b * NCW + blk];
        transpose64(a);
        for (int c = 0; c < 64; c++) { int col = blk * 64 + c; if (col < NC) X[(size_t)col * WMAX + w] = a[c]; }
    }
}
static void word_in(int w, const u64 *T) { word_in_s(w, T, cs); }
static void lane_load(int lane, const u64 *cfg) {
    int w = lane >> 6, b = lane & 63; u64 m = 1ULL << b;
    for (int col = 0; col < NC; col++) {
        u64 *p = X + (size_t)col * WMAX + w;
        *p = (*p & ~m) | (((cfg[col >> 6] >> (col & 63)) & 1) << b);
    }
}
static void lane_extract_s(int lane, u64 *cfg, int sl) {
    int w = lane >> 6, b = lane & 63; const u64 *X = Xr[sl];
    memset(cfg, 0, 8 * NCW);
    for (int col = 0; col < NC; col++) cfg[col >> 6] |= ((X[(size_t)col * WMAX + w] >> b) & 1) << (col & 63);
}

__attribute__((unused)) static void lane_extract(int lane, u64 *cfg) { lane_extract_s(lane, cfg, cs); }
static u64 rs[4];
static inline u64 rotl(u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static inline u64 rnd(void) {
    u64 r = rotl(rs[1] * 5, 7) * 9, t = rs[1] << 17;
    rs[2] ^= rs[0]; rs[3] ^= rs[1]; rs[1] ^= rs[2]; rs[0] ^= rs[3]; rs[2] ^= t; rs[3] = rotl(rs[3], 45);
    return r;
}
static void seed_rng(u64 s) {
    for (int i = 0; i < 4; i++) {
        s += 0x9E3779B97F4A7C15ULL; u64 z = s;
        z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL; z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL; rs[i] = z ^ (z >> 31);
    }
}
static inline double rndu(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static inline u64 rndn(u64 m) { return (u64)(((__uint128_t)rnd() * m) >> 64); }

static inline int cbit(const u64 *c, int i) { return (c[i >> 6] >> (i & 63)) & 1; }
static void cfg_soup(u64 *c) {
    memset(c, 0, 8 * NCW);
    for (int i = 0; i < n; i++) if (rndu() < SOUP) c[i >> 6] |= 1ULL << (i & 63);
    for (int i = 0; i < A; i++) if (!cbit(c, i)) for (int k = 0; k < 8; k++) { int col = n + 8 * i + k; c[col >> 6] |= 1ULL << (col & 63); }
}
__attribute__((unused)) static int cfg_pop0(const u64 *c) {
    int p = 0;
    for (int i = 0; i < A; i += 64) { u64 v = c[i >> 6]; if (A - i < 64) v &= (1ULL << (A - i)) - 1; p += __builtin_popcountll(v); }
    return p;
}
__attribute__((unused)) static int cfg_ndead(const u64 *c) {
    int k = 0;
    for (int f = 0; f < 8; f++) { u64 o = 0; for (int j = 0; j < NCW; j++) o |= c[j] & fmask[f][j]; k += (o == 0); }
    return k;
}
static int cfg_age(const u64 *c, int i) { int a = 0; for (int k = 0; k < 8; k++) a |= cbit(c, n + 8 * i + k) << k; return a; }
// The perturbation: with probability 1/2 kill one live cell of S chosen uniformly, otherwise revive one dead cell of
// S chosen uniformly (the other kind if there is none of the kind drawn).
static void cfg_flip(u64 *c) {
    int live[4096], dead[4096], nl = 0, nd = 0;
    for (int k = 0; k < nS; k++) { if (cbit(c, S[k])) live[nl++] = S[k]; else dead[nd++] = S[k]; }
    int kill = rnd() >> 63, i;
    if (kill && nl == 0) kill = 0;
    if (!kill && nd == 0) kill = 1;
    i = kill ? live[rndn(nl)] : dead[rndn(nd)];
    c[i >> 6] ^= 1ULL << (i & 63);
}
static void cfg_flips(u64 *c) { for (int k = 0; k < NFLIP; k++) cfg_flip(c); }

#ifdef LIB
// ---------------------------------------------------------------- validation interface (ctypes)
void v_coords(int *out) { memcpy(out, co, sizeof(int) * 3 * n); }
int v_A(void) { return A; }
int v_nS(void) { return nS; }
void v_sites(int *out) { memcpy(out, S, sizeof(int) * nS); }
void v_clear(void) { for (int k = 0; k < NS; k++) memset(Xr[k], 0, sizeof(u64) * (size_t)(NC + 1) * WMAX); memset(Fz, 0, sizeof Fz); }
void v_setlag(int m) { LAG = m; NS = m + 1; }
void v_set(int lane, const uint8_t *cells) {
    for (int i = 0; i < n; i++) { u64 *p = X + (size_t)i * WMAX + (lane >> 6); *p = (*p & ~(1ULL << (lane & 63))) | ((u64)(cells[i] & 1) << (lane & 63)); }
}
void v_get(int lane, uint8_t *cells) { for (int i = 0; i < n; i++) cells[i] = (X[(size_t)i * WMAX + (lane >> 6)] >> (lane & 63)) & 1; }
void v_step(void) { step(WMAX); observe(WMAX); }
int v_cs(void) { return cs; }
int v_ns(void) { return NS; }
void v_get_s(int lane, uint8_t *cells, int sl) { for (int i = 0; i < n; i++) cells[i] = (Xr[sl][(size_t)i * WMAX + (lane >> 6)] >> (lane & 63)) & 1; }
int v_pop(int lane) { return pop[lane]; }
int v_faceor(int lane, int f) { return (faceor[f][lane >> 6] >> (lane & 63)) & 1; }
int v_age(int lane, int c) { int a = 0; for (int k = 0; k < 8; k++) a |= ((X[(size_t)(n + 8 * c + k) * WMAX + (lane >> 6)] >> (lane & 63)) & 1) << k; return a; }
void v_swap(int i, int j, int newnb) { nb[12 * i + j] = newnb; }
int v_nb(int i, int j) { return nb[12 * i + j]; }
void v_freeze(int lane) { Fz[lane >> 6] |= 1ULL << (lane & 63); }
// round trip of the packed-configuration machinery: out through word_out, in through word_in / lane_load
int v_roundtrip(void) {
    u64 *T = malloc(8 * (size_t)64 * NCW), *c = malloc(8 * NCW); int bad = 0;
    for (int w = 0; w < WMAX; w++) {
        word_out(w, T);
        for (int b = 0; b < 64; b++) { lane_extract(w * 64 + b, c); bad += memcmp(c, T + (size_t)b * NCW, 8 * NCW) != 0; }
        for (int b = 0; b < 64; b++) lane_load(w * 64 + b, T + (size_t)((b + 1) % 64) * NCW);   // rotate lanes by one
        u64 *T2 = malloc(8 * (size_t)64 * NCW); word_out(w, T2);
        for (int b = 0; b < 64; b++) bad += memcmp(T2 + (size_t)b * NCW, T + (size_t)((b + 1) % 64) * NCW, 8 * NCW) != 0;
        word_in(w, T); word_out(w, T2); bad += memcmp(T, T2, 8 * (size_t)64 * NCW) != 0; free(T2);
    }
    free(T); free(c); return bad;
}
#else
// ---------------------------------------------------------------- the sampler
enum { IDLE, RUN, SUCC };
static int Wact, LA, L0, Lnext, final_stage;
static int lage[NL], linA[NL], lstate[NL], lanc[NL], lt0[NL], llen[NL], lk[NL], lfs[NL];
static u64 *cur, *nxt, *T, *TS[8]; static int *canc, *ct, *nanc, *nt, Ncur, Nnxt, M;
static long launched, done, ntimeout, nrun; static double succw, lensum; static int *order;
static uint8_t *pages, *phist; static int *panc, *pT, *pk, npath; static long pseen, nbust, nreplaybad;
#define HL 16            // generations of face-0 population kept with every lane and stored configuration (newest last)
static uint8_t lhist[NL][HL], bh[NL][HL], *chist, *nhist;
static void path_add(const u64 *c, int anc, int Tl, int k, const uint8_t *h) {   // c: the state at the death generation
    long slot; pseen++;
    for (int i = 1; i < HL; i++) if (2 * (h[i - 1] - h[i]) >= A) { nbust++; break; }   // a one-generation fall of half the face
    if (npath < PMAX) slot = npath++; else { slot = (long)rndn(pseen); if (slot >= PMAX) return; }
    panc[slot] = anc; pT[slot] = Tl; pk[slot] = k; memcpy(phist + slot * HL, h, HL);
    for (int i = 0; i < A; i++) pages[slot * A + i] = cfg_age(c, i);
}
static int CAPN; static long nseen;
// MODE 1 ("donor swap"): instead of flips, everything at depth >= DEPTH beneath the watched face (x+y+z <= R - 2 DEPTH)
// is replaced by the same cells of an independent hull taken from the base run at an unrelated time (the pool).
#define POOLN 4096
static int MODE = 0, npool = 0; static u64 *pool, *deepmask;
static void perturb(u64 *c) {
    if (!MODE) { cfg_flips(c); return; }
    const u64 *d = pool + (size_t)rndn(npool) * NCW;
    for (int j = 0; j < NCW; j++) c[j] = (c[j] & ~deepmask[j]) | (d[j] & deepmask[j]);
}
// lag: the state LAG generations before the success (what the next stage's clones start from)
static void store_success(const u64 *lag, int anc, int Tl, const uint8_t *h) {   // reservoir of CAPN: a uniform subset of the successes
    long slot; nseen++;
    if (Nnxt < CAPN) slot = Nnxt++; else { slot = (long)rndn(nseen); if (slot >= CAPN) return; }
    memcpy(nxt + (size_t)slot * NCW, lag, 8 * NCW); nanc[slot] = anc; nt[slot] = Tl; memcpy(nhist + slot * HL, h, HL);
}
static void flush_succ(int w) {   // store the successes sitting frozen in word w
    int need = 0;
    for (int b = 0; b < 64; b++) { int lane = w * 64 + b; if (lstate[lane] == SUCC) { need |= 1 << ((lfs[lane] + 1) % NS); if (final_stage) need |= 1 << lfs[lane]; } }
    if (!need) return;
    for (int sl = 0; sl < NS; sl++) if (need >> sl & 1) word_out_s(w, TS[sl], sl);
    for (int b = 0; b < 64; b++) {
        int lane = w * 64 + b;
        if (lstate[lane] != SUCC) continue;
        int Tl = lt0[lane] + llen[lane] - LAG;
        store_success(TS[(lfs[lane] + 1) % NS] + (size_t)b * NCW, lanc[lane], Tl, lhist[lane]);
        if (final_stage) path_add(TS[lfs[lane]] + (size_t)b * NCW, lanc[lane], Tl, lk[lane], lhist[lane]);
        lstate[lane] = IDLE;
    }
}
static void refresh(int w) {
    flush_succ(w);
    word_out(w, T);
    u64 fz = Fz[w];
    while (fz && launched < M) {
        int b = __builtin_ctzll(fz), lane = w * 64 + b; fz &= fz - 1;
        u64 *c = T + (size_t)b * NCW;
        int j = order[launched % Ncur]; launched++;
        memcpy(c, cur + (size_t)j * NCW, 8 * NCW); perturb(c);
        lstate[lane] = RUN; lanc[lane] = canc[j]; lt0[lane] = ct[j]; llen[lane] = 0; nrun++; memcpy(lhist[lane], chist + (size_t)j * HL, HL);
        Fz[w] &= ~(1ULL << b);
    }
    word_in(w, T);
}
static void compact(void) {
    static u64 *buf; static int ma[NL], mt[NL], ml[NL]; static uint8_t mh[NL][HL];
    if (!buf) buf = malloc(8 * (size_t)NL * NCW);
    int na = 0, Wold = Wact;
    for (int w = 0; w < Wold; w++) flush_succ(w);
    for (int lane = 0; lane < Wold * 64; lane++) if (lstate[lane] == RUN) { memcpy(mh[na], lhist[lane], HL); ma[na] = lanc[lane]; mt[na] = lt0[lane]; ml[na] = llen[lane]; na++; }
    int Wnew = na ? (na + 63) / 64 : 1;
    for (int sl = 0; sl < NS; sl++) {
        int k = 0;
        for (int w = 0; w < Wold; w++) {
            int any = 0;
            for (int b = 0; b < 64; b++) any |= lstate[w * 64 + b] == RUN;
            if (!any) continue;
            word_out_s(w, T, sl);
            for (int b = 0; b < 64; b++) if (lstate[w * 64 + b] == RUN) { memcpy(buf + (size_t)k * NCW, T + (size_t)b * NCW, 8 * NCW); k++; }
        }
        for (int w = 0; w < Wnew; w++) {
            memset(T, 0, 8 * (size_t)64 * NCW);
            for (int b = 0; b < 64; b++) if (w * 64 + b < na) memcpy(T + (size_t)b * NCW, buf + (size_t)(w * 64 + b) * NCW, 8 * NCW);
            word_in_s(w, T, sl);
        }
    }
    for (int lane = 0; lane < NL; lane++) lstate[lane] = IDLE;
    for (int w = 0; w < WMAX; w++) Fz[w] = ~0ULL;
    for (int lane = 0; lane < na; lane++) { memcpy(lhist[lane], mh[lane], HL); lstate[lane] = RUN; lanc[lane] = ma[lane]; lt0[lane] = mt[lane]; llen[lane] = ml[lane]; Fz[lane >> 6] &= ~(1ULL << (lane & 63)); }
    Wact = Wnew;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: sh R SEED M [LAG NFLIP STEP H PATHFILE|- CAP] | sh R SEED 0 GENS\n"); return 2; }
    int Rr = atoi(argv[1]); u64 seed = strtoull(argv[2], 0, 10); M = atoi(argv[3]);
    long bfgens = (M == 0 && argc > 4) ? atol(argv[4]) : 0;
    LAG = (M && argc > 4) ? atoi(argv[4]) : 1; NFLIP = (M && argc > 5) ? atoi(argv[5]) : 1;
    int STEP = (M && argc > 6) ? atoi(argv[6]) : 2;
    double H = (M && argc > 7) ? atof(argv[7]) : 0.125;
    const char *pathfile = (M && argc > 8 && strcmp(argv[8], "-")) ? argv[8] : 0;
    CAPN = (M && argc > 9) ? atoi(argv[9]) : 200000;
    if (CAPN > M && M) CAPN = M;
    MODE = (M && argc > 10) ? atoi(argv[10]) : 0;
    if (LAG < 1 || LAG > 7) { fprintf(stderr, "LAG must be 1..7\n"); return 2; }
    NS = LAG + 1;
    int D = 2 * LAG + 1;     // a flip there cannot reach the face layer within LAG generations
    geom_init(Rr, D); seed_rng(seed);
    if (NFLIP <= 0) NFLIP = (nS + (-NFLIP ? -NFLIP : 6) - 1) / (-NFLIP ? -NFLIP : 6);   // NFLIP = -f: one flip per f sites, rounded up
    pool = malloc(8 * (size_t)POOLN * NCW); deepmask = calloc(NCW, 8);
    for (int i = 0; i < n; i++) if (co[3 * i] + co[3 * i + 1] + co[3 * i + 2] <= R - 2 * D) deepmask[i >> 6] |= 1ULL << (i & 63);
    if (nS < 2 && !MODE) { fprintf(stderr, "no perturbation sites at depth %d in R = %d\n", D, Rr); return 2; }
    {   // self-test of the transpose
        u64 a[64], b[64]; for (int i = 0; i < 64; i++) a[i] = b[i] = rnd();
        transpose64(b);
        for (int i = 0; i < 64; i++) for (int j = 0; j < 64; j++) if (((b[i] >> j) & 1) != ((a[j] >> i) & 1)) { fprintf(stderr, "transpose broken\n"); return 1; }
    }
    T = malloc(8 * (size_t)64 * NCW);
    for (int k = 0; k < NS; k++) TS[k] = malloc(8 * (size_t)64 * NCW);
    u64 *tmp = malloc(8 * NCW);
    // ---- base run: NL independent hulls from fresh soups
    for (int w = 0; w < WMAX; w++) { for (int b = 0; b < 64; b++) cfg_soup(T + (size_t)b * NCW); word_in(w, T); }
    memset(lage, 0, sizeof lage); memset(linA, 0, sizeof linA);
    double psum = 0, psum2 = 0, pcnt = 0, exposure = 0, d0w = 0; long ncross = 0, deaths = 0, nold = 0, nstore = 0;
    static uint8_t exmin[NL]; static double exh[256]; memset(exmin, 255, sizeof exmin);   // brute-force table of excursion minima
    int phase = 0;        // 0 burn-in, 1 pilot (P-bar), 2 flags settle, 3 counting
    long g = 0, gphase = 0; double PBAR = 0, SIG = 0;
    int cap = M ? CAPN : 1;
    cur = malloc(8 * (size_t)cap * NCW); nxt = malloc(8 * (size_t)cap * NCW);
    chist = malloc((size_t)cap * HL); nhist = malloc((size_t)cap * HL); memset(bh, 0, sizeof bh);
    canc = malloc(sizeof(int) * cap); ct = malloc(sizeof(int) * cap); nanc = malloc(sizeof(int) * cap); nt = malloc(sizeof(int) * cap);
    LA = 1000; L0 = -1;
    for (;; g++, gphase++) {
        if (phase == 0 && gphase == T0) { phase = 1; gphase = 0; }
        if (phase == 1 && gphase == 300) {
            PBAR = psum / pcnt; SIG = sqrt(psum2 / pcnt - PBAR * PBAR);
            LA = (int)ceil(PBAR); L0 = (int)floor(0.9 * PBAR);
            phase = 2; gphase = 0; memset(linA, 0, sizeof linA);
        }
        if (phase == 2 && gphase == 100) { phase = 3; gphase = 0; }
        if (phase == 3 && ((M && nstore >= CAPN) || (!M && gphase >= bfgens))) break;
        if (MODE && phase == 3 && gphase % 100 == 0 && npool < POOLN)   // donors: 512 hulls every 100 generations
            for (int k = 0; k < 512 && npool < POOLN; k++) { int lane = (int)((gphase / 100 * 512 + k) % NL); if (lage[lane] > T0) lane_extract(lane, pool + (size_t)npool++ * NCW); }
        step(WMAX); observe(WMAX);
        for (int lane = 0; lane < NL; lane++) {
            int w = lane >> 6, b = lane & 63, p = pop[lane], nd = (p == 0);
            for (int f = 1; f < 8; f++) nd += !((faceor[f][w] >> b) & 1);
            lage[lane]++;
            memmove(bh[lane], bh[lane] + 1, HL - 1); bh[lane][HL - 1] = p;
            int counted = (phase == 3 && lage[lane] > T0);
            if (counted) exposure += 1;
            int reseed = 0, cross = 0;
            // excursion below lambda_A: booked at its end with its minimum (brute force; the sampler does not use it)
            if (nd || p >= LA) { int mn = (nd && p == 0) ? 0 : exmin[lane]; if (nd && p > 0 && p < mn) mn = p; if (counted && mn < LA) exh[mn] += 1; exmin[lane] = 255; }
            else if (p < exmin[lane]) exmin[lane] = p;
            if (nd) {
                if (counted) {
                    deaths++;
                    if (p == 0) { d0w += 1.0 / nd; if (linA[lane]) cross = 1; }   // straight from above P-bar to nothing
                }
                reseed = 1;
            } else {
                if (phase == 1 && lage[lane] > T0) { psum += p; psum2 += (double)p * p; pcnt += 1; }
                if (lage[lane] >= TFLAG) {
                    if (p >= LA) linA[lane] = 1;
                    else if (p <= L0 && linA[lane]) { linA[lane] = 0; cross = counted; }
                }
                if (lage[lane] > AGEMAX) { nold++; reseed = 1; }
            }
            if (cross) {
                ncross++;
                if (M && nstore < CAPN && rndu() < H) {   // keep the state LAG generations before the crossing
                    lane_extract_s(lane, cur + (size_t)nstore * NCW, (cs + 1) % NS); memcpy(chist + (size_t)nstore * HL, bh[lane], HL); canc[nstore] = nstore; ct[nstore] = 0; nstore++;
                }
            }
            if (reseed) { cfg_soup(tmp); lane_load(lane, tmp); lage[lane] = 0; linA[lane] = 0; }
        }
    }
    double lnphi = log(ncross / exposure);
    printf("# R %d n %d A %d nS %d LAG %d D %d NFLIP %d STEP %d H %g CAP %d seed %llu M %d MODE %d npool %d\n", R, n, A, nS, LAG, D, NFLIP, STEP, H, CAPN, (unsigned long long)seed, M, MODE, npool);
    printf("# PBAR %.4f SIG %.4f LA %d L0 %d exposure %.0f ncross %ld lnPhi0 %.5f deaths_any %ld d0w %.3f old %ld direct_lntau %.4f direct_err %.4f\n",
           PBAR, SIG, LA, L0, exposure, ncross, lnphi, deaths, d0w, nold,
           deaths ? log(8 * exposure / deaths) : NAN, deaths ? 1 / sqrt((double)deaths) : NAN);
    if (!M) {
        double cum = 0;
        for (int L = 0; L <= L0; L++) { cum += exh[L]; if (cum > 0) printf("E R %d level %d count %.0f lnnu %.5f err %.5f\n", R, L, cum, log(cum / exposure), 1 / sqrt(cum)); }
        return 0;
    }
    // ---- stages
    Ncur = (int)nstore;
    order = malloc(sizeof(int) * CAPN);
    pages = malloc((size_t)PMAX * A); phist = malloc((size_t)PMAX * HL); panc = malloc(sizeof(int) * PMAX); pT = malloc(sizeof(int) * PMAX); pk = malloc(sizeof(int) * PMAX);
    int *acnt = malloc(sizeof(int) * CAPN);
    double lnq = 0; int lev = L0, zero = 0, stage = 0;
    while (lev > 0) {
        Lnext = lev - STEP > 0 ? lev - STEP : 0; final_stage = (Lnext == 0);
        if (Ncur == 0) { zero = 1; break; }
        for (int i = 0; i < Ncur; i++) order[i] = i;
        for (int i = Ncur - 1; i > 0; i--) { int j = (int)rndn(i + 1), t = order[i]; order[i] = order[j]; order[j] = t; }
        for (int lane = 0; lane < NL; lane++) lstate[lane] = IDLE;
        for (int w = 0; w < WMAX; w++) Fz[w] = ~0ULL;
        Wact = WMAX; launched = done = 0; succw = 0; lensum = 0; Nnxt = 0; nrun = 0; nseen = 0; long gens = 0;
        while (done < M) {
            if (launched < M) { for (int w = 0; w < Wact; w++) if (__builtin_popcountll(Fz[w]) >= THR) refresh(w); }
            else if (nrun * 2 <= (long)Wact * 64 && Wact > 1) compact();
            step(Wact); observe(Wact); gens++;
            for (int w = 0; w < Wact; w++) {
                u64 run = ~Fz[w];
                while (run) {
                    int b = __builtin_ctzll(run), lane = w * 64 + b; run &= run - 1;
                    if (++llen[lane] < LAG) continue;   // catching up with the parent: the face is the parent's own
                    int p = pop[lane], od = 0, fin = 0;
                    if (llen[lane] == LAG) nreplaybad += (p != lhist[lane][HL - 1]);   // the replay must end on the parent's face
                    else { memmove(lhist[lane], lhist[lane] + 1, HL - 1); lhist[lane][HL - 1] = p; }
                    for (int f = 1; f < 8; f++) od += !((faceor[f][w] >> b) & 1);
                    if (p == 0) { fin = SUCC; lk[lane] = 1 + od; succw += final_stage ? 1.0 / (1 + od) : 1.0; }
                    else if (od) fin = IDLE;
                    else if (p <= Lnext) { fin = SUCC; lk[lane] = 1; succw += 1.0; }
                    else if (p >= LA) fin = IDLE;
                    else if (llen[lane] > TMAX) { fin = IDLE; ntimeout++; }
                    else continue;
                    lstate[lane] = fin; lfs[lane] = cs; Fz[w] |= 1ULL << b; done++; nrun--; lensum += llen[lane] - LAG;
                }
            }
        }
        for (int w = 0; w < Wact; w++) flush_succ(w);
        double p = succw / M; lnq += log(p);
        memset(acnt, 0, sizeof(int) * CAPN); int dist = 0; double tsum = 0, s2 = 0;
        for (int i = 0; i < Nnxt; i++) { if (!acnt[nanc[i]]++) dist++; tsum += nt[i]; }
        for (int i = 0; i < CAPN; i++) s2 += (double)acnt[i] * acnt[i];
        double neff = s2 > 0 ? (double)Nnxt * Nnxt / s2 : 0;
        printf("L %d from %d to %d trials %d succw %.3f p %.6f stored %d ancestors %d neff %.1f meanlen %.2f meanT %.2f gens %ld lnnu_next %.5f\n",
               stage, lev, Lnext, M, succw, p, Nnxt, dist, neff, lensum / (M > 0 ? M : 1), Nnxt ? tsum / Nnxt : 0.0, gens, lnphi + lnq);
        fflush(stdout);
        { u64 *t = cur; cur = nxt; nxt = t; uint8_t *hh = chist; chist = nhist; nhist = hh; int *q = canc; canc = nanc; nanc = q; q = ct; ct = nt; nt = q; Ncur = Nnxt; }
        lev = Lnext; stage++;
        if (succw == 0) { zero = 1; break; }
    }
    printf("RESULT R %d seed %llu M %d lnPhi0 %.5f lnq %.5f lntau %.5f zero %d timeouts %ld paths_seen %ld busts %ld replaybad %ld\n", R, (unsigned long long)seed, M,
           lnphi, lnq, zero ? INFINITY : -(lnphi + lnq), zero, ntimeout, pseen, nbust, nreplaybad);
    if (pathfile && npath) {
        FILE *fp = fopen(pathfile, "w");
        fprintf(fp, "# R %d seed %llu M %d A %d LAG %d NFLIP %d STEP %d ; line C: doubled coordinates of the face-0 cells; then one line per dying path:\n", R, (unsigned long long)seed, M, A, LAG, NFLIP, STEP);
        fprintf(fp, "# ancestor T k age[0..A-1]   (ancestor: index of the 0.9 P-bar crossing the path descends from; T: generations from that crossing to the death; k: faces empty at the death;\n# age: generations before the death generation at which the cell was last alive, 255 = 255 or more;\n# after the token P: the face population at the last 16 generations, the death generation (0) last)\n");
        fprintf(fp, "C");
        for (int i = 0; i < A; i++) fprintf(fp, " %d,%d,%d", co[3 * i], co[3 * i + 1], co[3 * i + 2]);
        fprintf(fp, "\n");
        for (int s = 0; s < npath; s++) {
            fprintf(fp, "%d %d %d", panc[s], pT[s], pk[s]);
            for (int i = 0; i < A; i++) fprintf(fp, " %d", pages[(size_t)s * A + i]);
            fprintf(fp, " P");
            for (int i = 0; i < HL; i++) fprintf(fp, " %d", phist[(size_t)s * HL + i]);
            fprintf(fp, "\n");
        }
        fclose(fp);
    }
    return 0;
}
#endif
