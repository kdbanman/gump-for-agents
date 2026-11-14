/* aud.c -- the audit's own stepper: 64 bit-sliced replicas of an outer-totalistic rule on an arbitrary cell graph.
 * Shares no code with research/theory/class/gstep.c.  Built as a shared library and driven from aud.py (ctypes):
 *     cc -O3 -march=native -shared -fPIC -o ../../scratch/audit-class/libaud.so aud.c
 * Graph: N cells, K neighbour slots per cell (int32, row-major); slot value N = "no neighbour" (always dead).
 * State arrays have N + 1 words; word N is kept at 0.  Bit r of word i = cell i in replica r.
 * Rule: bit n of Bm = birth at n live neighbours, bit n of Sm = survival at n.  K <= 31.
 */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
typedef uint64_t u64;

static u64 RS[4];
static inline u64 rotl(u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static inline u64 rnd(void) {
    u64 r = rotl(RS[1] * 5, 7) * 9, t = RS[1] << 17;
    RS[2] ^= RS[0]; RS[3] ^= RS[1]; RS[1] ^= RS[2]; RS[0] ^= RS[3]; RS[2] ^= t; RS[3] = rotl(RS[3], 45);
    return r;
}
void aud_seed(u64 s) {
    for (int i = 0; i < 4; i++) {
        s += 0x9E3779B97F4A7C15ULL;
        u64 z = s; z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL; z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
        RS[i] = z ^ (z >> 31);
    }
}

void aud_step(int N, int K, const int32_t *nbr, const u64 *x, u64 *out, uint32_t Bm, uint32_t Sm) {
    for (int i = 0; i < N; i++) {
        u64 s0 = 0, s1 = 0, s2 = 0, s3 = 0, s4 = 0;
        const int32_t *nb = nbr + (size_t)i * K;
        for (int j = 0; j < K; j++) {
            u64 v = x[nb[j]], c;
            c = s0 & v; s0 ^= v; v = c;
            c = s1 & v; s1 ^= v; v = c;
            c = s2 & v; s2 ^= v; v = c;
            c = s3 & v; s3 ^= v; s4 ^= c;
        }
        u64 a = x[i], born = 0, stay = 0;
        for (int n = 0; n <= K; n++) {
            int b = (Bm >> n) & 1, s = (Sm >> n) & 1;
            if (!(b | s)) continue;
            u64 e = ((n & 1) ? s0 : ~s0) & ((n & 2) ? s1 : ~s1) & ((n & 4) ? s2 : ~s2) & ((n & 8) ? s3 : ~s3) &
                    ((n & 16) ? s4 : ~s4);
            if (b) born |= e;
            if (s) stay |= e;
        }
        out[i] = (born & ~a) | (stay & a);
    }
    out[N] = 0;
}

static void reseed(int N, u64 *x, u64 *x1, u64 *snap, int r, uint32_t p16) {
    u64 bit = 1ULL << r;
    for (int i = 0; i < N; i++) {
        if ((rnd() & 0xFFFF) < p16) x[i] |= bit; else x[i] &= ~bit;
        x1[i] &= ~bit;
        snap[i] = (snap[i] & ~bit) | (~x[i] & bit);
    }
}

static int bin_of(long a) { int k = 0; while (a > 1) { a >>= 1; k++; } return k; }   /* floor(log2(a)), a >= 1 */

/* Slab / face run.  nf watched groups (cells fidx[fstart[g] .. fstart[g+1])); a replica "dies" at the first
 * generation at which some group is entirely dead.  It is then reseeded at density p.  Replicas that become
 * periodic (period <= 2, or equal to a Brent snapshot) are censored and reseeded.  Events before age T0 are
 * discarded.  Exposure = replica-generations at age > T0.
 * res[0] exposure, [1] deaths, [2] early deaths, [3] settled (censored), [4] early settled, [5] generations run,
 * res[6 + l] = summed population of label-l cells over sampled old replicas, res[10 + l] = number of such cell
 * samples (l = 0..3).   binexp/bindeath: exposure and deaths by floor(log2(age - T0)) (age - T0 >= 1).
 * waits: age - T0 at each counted death (first maxw of them); wgroup: which group died.
 * res[14 + g] = deaths by group (g < 8). */
long aud_face(int N, int K, const int32_t *nbr, uint32_t Bm, uint32_t Sm, int nf, const int32_t *fidx,
              const int32_t *fstart, const int32_t *lab, double p, int T0, long gens, u64 seed, double *res,
              double *binexp, double *bindeath, int nbins, int32_t *waits, int32_t *wgroup, int maxw) {
    aud_seed(seed);
    uint32_t p16 = (uint32_t)(p * 65536.0 + 0.5);
    u64 *x = calloc(N + 1, 8), *y = calloc(N + 1, 8), *x1 = calloc(N + 1, 8), *snap = calloc(N + 1, 8);
    long age[64];
    long nw = 0;
    for (int i = 0; i < 22; i++) res[i] = 0;
    for (int r = 0; r < 64; r++) { reseed(N, x, x1, snap, r, p16); age[r] = 0; }
    for (long t = 0; t < gens; t++) {
        aud_step(N, K, nbr, x, y, Bm, Sm);
        u64 d2 = 0, ds = 0;
        for (int i = 0; i < N; i++) { d2 |= y[i] ^ x1[i]; ds |= y[i] ^ snap[i]; }
        u64 dead = 0, gdead[8];
        for (int g = 0; g < nf; g++) {
            u64 o = 0;
            for (int k = fstart[g]; k < fstart[g + 1]; k++) o |= y[fidx[k]];
            gdead[g & 7] = ~o;
            dead |= ~o;
        }
        u64 *tmp = x1; x1 = x; x = y; y = tmp;
        u64 periodic = ~d2 | ~ds;
        u64 old = 0;
        for (int r = 0; r < 64; r++) {
            u64 bit = 1ULL << r;
            age[r]++;
            long a = age[r] - T0;
            if (dead & bit) {
                if (a >= 1) {
                    res[1] += 1; res[0] += 1;
                    int k = bin_of(a); if (k < nbins) { bindeath[k] += 1; binexp[k] += 1; }
                    int g = 0; while (g < nf && !(gdead[g & 7] & bit)) g++;
                    if (g < 8) res[14 + g] += 1;
                    if (nw < maxw) { waits[nw] = (int32_t)(a > 2000000000L ? 2000000000L : a); wgroup[nw] = g; nw++; }
                } else res[2] += 1;
                reseed(N, x, x1, snap, r, p16); age[r] = 0;
            } else if (periodic & bit) {
                if (a >= 1) res[3] += 1; else res[4] += 1;
                reseed(N, x, x1, snap, r, p16); age[r] = 0;
            } else {
                if (a >= 1) { res[0] += 1; int k = bin_of(a); if (k < nbins) binexp[k] += 1; old |= bit; }
                if ((age[r] & (age[r] - 1)) == 0 && age[r] >= 4)
                    for (int i = 0; i < N; i++) snap[i] = (snap[i] & ~bit) | (x[i] & bit);
            }
        }
        if ((t & 31) == 0 && old) {
            int no = __builtin_popcountll(old);
            for (int i = 0; i < N; i++) {
                int l = lab[i] & 3;
                res[6 + l] += __builtin_popcountll(x[i] & old);
                res[10 + l] += no;
            }
        }
    }
    res[5] = (double)gens;
    free(x); free(y); free(x1); free(snap);
    return nw;
}

/* Lifetimes of 64 soups in a vessel.  life[r] = first t with x(t) = x(t+2) (kind 1), or the generation at which
 * the state equalled a Brent snapshot (kind 2: an upper bound for the entry into a longer cycle), or -1 if still
 * running at the cap (kind 0).  pop[r] = population when detected (or at the cap).  x0 (optional, N words): seeds. */
void aud_life(int N, int K, const int32_t *nbr, uint32_t Bm, uint32_t Sm, double p, long cap, u64 seed,
              const u64 *x0, int64_t *life, int32_t *pop, int32_t *kind) {
    aud_seed(seed);
    uint32_t p16 = (uint32_t)(p * 65536.0 + 0.5);
    u64 *x = calloc(N + 1, 8), *y = calloc(N + 1, 8), *x1 = calloc(N + 1, 8), *snap = calloc(N + 1, 8);
    if (x0) { memcpy(x, x0, (size_t)N * 8); for (int i = 0; i < N; i++) snap[i] = ~x[i]; }
    else for (int r = 0; r < 64; r++) reseed(N, x, x1, snap, r, p16);
    /* x1 = "state at t = -1": use the complement of x so that no replica is flagged at t = 1 by accident */
    for (int i = 0; i < N; i++) x1[i] = ~x[i];
    u64 run = ~0ULL;
    for (int r = 0; r < 64; r++) { life[r] = -1; kind[r] = 0; pop[r] = 0; }
    long t;
    for (t = 1; t <= cap && run; t++) {
        aud_step(N, K, nbr, x, y, Bm, Sm);
        u64 d2 = 0, ds = 0;
        for (int i = 0; i < N; i++) { d2 |= y[i] ^ x1[i]; ds |= y[i] ^ snap[i]; }
        u64 *tmp = x1; x1 = x; x = y; y = tmp;          /* now x = state at t, x1 = state at t - 1, y = t - 2 */
        u64 done = (~d2 | ~ds) & run;
        if (done) {
            for (int r = 0; r < 64; r++) if (done & (1ULL << r)) {
                int c = 0;
                for (int i = 0; i < N; i++) c += (x[i] >> r) & 1;
                pop[r] = c;
                if (!((d2 >> r) & 1)) { life[r] = t - 2 < 0 ? 0 : t - 2; kind[r] = 1; }
                else { life[r] = t; kind[r] = 2; }
            }
            run &= ~done;
        }
        if ((t & (t - 1)) == 0 && t >= 4) memcpy(snap, x, (size_t)N * 8);
    }
    for (int r = 0; r < 64; r++) if (run & (1ULL << r)) {
        int c = 0;
        for (int i = 0; i < N; i++) c += (x[i] >> r) & 1;
        pop[r] = c;
    }
    free(x); free(y); free(x1); free(snap);
}

/* Torus (or any vessel) bulk statistics: at each of nchk checkpoints (generations chk[k], increasing) record
 * out[4k] = number of replicas not yet periodic, out[4k+1] = mean density over those, out[4k+2] = mean activity
 * (fraction of cells with x(t) != x(t-2)) over those, out[4k+3] = mean density over all 64. */
void aud_bulk(int N, int K, const int32_t *nbr, uint32_t Bm, uint32_t Sm, double p, u64 seed, int nchk,
              const int64_t *chk, double *out) {
    aud_seed(seed);
    uint32_t p16 = (uint32_t)(p * 65536.0 + 0.5);
    u64 *x = calloc(N + 1, 8), *y = calloc(N + 1, 8), *x1 = calloc(N + 1, 8), *snap = calloc(N + 1, 8);
    for (int r = 0; r < 64; r++) reseed(N, x, x1, snap, r, p16);
    for (int i = 0; i < N; i++) x1[i] = ~x[i];
    u64 run = ~0ULL;
    int k = 0;
    for (long t = 1; k < nchk; t++) {
        aud_step(N, K, nbr, x, y, Bm, Sm);
        u64 d2 = 0, ds = 0;
        for (int i = 0; i < N; i++) { d2 |= y[i] ^ x1[i]; ds |= y[i] ^ snap[i]; }
        run &= d2 & ds;
        if (t == chk[k]) {
            double dr = 0, ar = 0, da = 0;
            for (int i = 0; i < N; i++) {
                dr += __builtin_popcountll(y[i] & run);
                ar += __builtin_popcountll((y[i] ^ x1[i]) & run);
                da += __builtin_popcountll(y[i]);
            }
            int nr = __builtin_popcountll(run);
            out[4 * k] = nr; out[4 * k + 1] = nr ? dr / ((double)N * nr) : 0; out[4 * k + 2] = nr ? ar / ((double)N * nr) : 0;
            out[4 * k + 3] = da / ((double)N * 64);
            k++;
        }
        u64 *tmp = x1; x1 = x; x = y; y = tmp;
        if ((t & (t - 1)) == 0 && t >= 4) memcpy(snap, x, (size_t)N * 8);
    }
    free(x); free(y); free(x1); free(snap);
}
