/* fu.c -- follow-up stepper and drivers: 64 bit-sliced replicas of an outer-totalistic rule on a cell graph,
 * with the largest dead sealed set computed by bit-sliced peeling.
 *
 * Graph: N cells, K slots per cell (int32 row-major); slot value N = outside the vessel (dead forever).
 * State words: N + 1, word N kept 0.  Bit r = replica r.  Bm / Sm: bit n set = birth / survival at n neighbours.
 * The step is checked cell for cell against a numpy gather stepper and against research/audit/class/aud.c
 * (fu.py validate).
 *
 * Sealed set (Theorem C): W is sealed if every cell of W has at most b - 1 neighbours in the vessel outside W.
 * The largest dead sealed set D(t) is the result of peeling the dead set; it only grows, and once a cell is in it
 * the cell is dead forever.
 */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
typedef uint64_t u64;

static u64 S_[4];
static inline u64 rl(u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static inline u64 rnd(void) {                     /* xoshiro256** */
    u64 r = rl(S_[1] * 5, 7) * 9, t = S_[1] << 17;
    S_[2] ^= S_[0]; S_[3] ^= S_[1]; S_[1] ^= S_[2]; S_[0] ^= S_[3]; S_[2] ^= t; S_[3] = rl(S_[3], 45);
    return r;
}
static void sd(u64 s) {
    for (int i = 0; i < 4; i++) {
        s += 0x9E3779B97F4A7C15ULL;
        u64 z = s; z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL; z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
        S_[i] = z ^ (z >> 31);
    }
}

/* count the K words v[nb[j]] into 5 bit planes c[0..4] */
static inline void count5(const int32_t *nb, int K, const u64 *v, u64 *c) {
    u64 a = 0, b = 0, d = 0, e = 0, f = 0;
    for (int j = 0; j < K; j++) {
        u64 w = v[nb[j]];
        u64 k1 = a & w; a ^= w;
        u64 k2 = b & k1; b ^= k1;
        u64 k3 = d & k2; d ^= k2;
        u64 k4 = e & k3; e ^= k3;
        f |= k4;                                   /* K <= 31 */
    }
    c[0] = a; c[1] = b; c[2] = d; c[3] = e; c[4] = f;
}
static inline u64 eqn(const u64 *c, int n) {
    u64 m = ~0ULL;
    for (int k = 0; k < 5; k++) m &= ((n >> k) & 1) ? c[k] : ~c[k];
    return m;
}
static inline u64 ruleword(const u64 *c, u64 a, uint32_t Bm, uint32_t Sm, int K) {
    u64 born = 0, stay = 0;
    for (int n = 0; n <= K; n++) {
        int bb = (Bm >> n) & 1, ss = (Sm >> n) & 1;
        if (!(bb | ss)) continue;
        u64 e = eqn(c, n);
        if (bb) born |= e;
        if (ss) stay |= e;
    }
    return (born & ~a) | (stay & a);
}

void fu_step(int N, int K, const int32_t *nbr, const u64 *x, u64 *out, uint32_t Bm, uint32_t Sm) {
    u64 c[5];
    for (int i = 0; i < N; i++) {
        count5(nbr + (size_t)i * K, K, x, c);
        out[i] = ruleword(c, x[i], Bm, Sm, K);
    }
    out[N] = 0;
}

/* Largest sealed subset of W (in place).  W has N + 1 words; the routine sets W[N] = ~0 so that outside slots are
 * never counted as "outside W in the vessel".  A cell leaves W when it has >= b neighbours in the vessel not in W. */
void fu_peel(int N, int K, const int32_t *nbr, u64 *W, int b) {
    u64 c[5];
    W[N] = ~0ULL;
    int changed = 1;
    while (changed) {
        changed = 0;
        for (int i = 0; i < N; i++) {
            if (!W[i]) continue;
            const int32_t *nb = nbr + (size_t)i * K;
            /* count neighbours NOT in W */
            u64 a = 0, bb = 0, d = 0, e = 0, f = 0;
            for (int j = 0; j < K; j++) {
                u64 w = ~W[nb[j]];
                u64 k1 = a & w; a ^= w;
                u64 k2 = bb & k1; bb ^= k1;
                u64 k3 = d & k2; d ^= k2;
                u64 k4 = e & k3; e ^= k3;
                f |= k4;
            }
            c[0] = a; c[1] = bb; c[2] = d; c[3] = e; c[4] = f;
            u64 ge = 0;
            for (int n = b; n <= K; n++) ge |= eqn(c, n);
            if (W[i] & ge) { W[i] &= ~ge; changed = 1; }
        }
    }
    W[N] = 0;
}

static void reseed(int N, u64 *x, u64 *x1, u64 *snap, int r, uint32_t p16) {
    u64 bit = 1ULL << r;
    for (int i = 0; i < N; i++) {
        if ((rnd() & 0xFFFF) < p16) x[i] |= bit; else x[i] &= ~bit;
        x1[i] = (x1[i] & ~bit) | (~x[i] & bit);         /* t = -1: complement, never equal by accident */
        snap[i] = (snap[i] & ~bit) | (~x[i] & bit);
    }
}

static int lg2(long a) { int k = 0; while (a > 1) { a >>= 1; k++; } return k; }

/* Slab run with competing endings.  Two boundary groups (g = 0, 1: the cells of the two boundary layers, i.e. the
 * first layer inside each sealed wall).  Every P generations the largest dead sealed set D is computed:
 *   WALL  : D contains every cell of group 0 or of group 1                         -> counted death, reseed
 *   CUT   : D nonempty, not a wall, meets both groups (spans the slab)               -> censored, reseed
 *   PIT   : D nonempty, otherwise                                                    -> censored, reseed
 * PERIODIC: x(t+1) = x(t-1) or x(t+1) = the snapshot taken at the last power-of-two age -> censored, reseed
 * Exposure = replica-generations at age > T0.  Events at age <= T0 are counted separately and not used.
 * res: [0] exposure [1] wall deaths [2] cuts [3] pits [4] periodic [5..8] same four before T0
 *      [9] max age of a replica alive at the end  [10] replicas alive at the end with age > T0
 *      [11..14] summed population of label-l cells over samples of old replicas, [15..18] cell samples of label l
 *      [19] max age ever reached by any replica.
 * binexp/binwall: exposure and wall deaths by floor(log2(age - T0)).  waits: age - T0 of each counted wall death. */
long fu_slab(int N, int K, const int32_t *nbr, uint32_t Bm, uint32_t Sm, int b, const int32_t *gidx,
             const int32_t *gstart, const int32_t *lab, double p, int T0, long gens, int P, u64 seed, double *res,
             double *binexp, double *binwall, int nbins, int32_t *waits, int maxw) {
    sd(seed);
    uint32_t p16 = (uint32_t)(p * 65536.0 + 0.5);
    u64 *x = calloc(N + 1, 8), *y = calloc(N + 1, 8), *x1 = calloc(N + 1, 8), *snap = calloc(N + 1, 8),
        *W = calloc(N + 1, 8);
    long age[64], nw = 0;
    for (int i = 0; i < 20; i++) res[i] = 0;
    for (int r = 0; r < 64; r++) { reseed(N, x, x1, snap, r, p16); age[r] = 0; }
    for (long t = 1; t <= gens; t++) {
        fu_step(N, K, nbr, x, y, Bm, Sm);
        u64 d2 = 0, ds = 0;
        for (int i = 0; i < N; i++) { d2 |= y[i] ^ x1[i]; ds |= y[i] ^ snap[i]; }
        u64 *tmp = x1; x1 = x; x = y; y = tmp;          /* x = new state, x1 = previous */
        u64 periodic = ~d2 | ~ds;
        u64 wall = 0, cut = 0, pit = 0;
        if (t % P == 0) {
            for (int i = 0; i < N; i++) W[i] = ~x[i];
            fu_peel(N, K, nbr, W, b);
            u64 any = 0;
            for (int i = 0; i < N; i++) any |= W[i];
            if (any) {
                u64 full[2], meet[2];
                for (int g = 0; g < 2; g++) {
                    u64 f = ~0ULL, m = 0;
                    for (int k = gstart[g]; k < gstart[g + 1]; k++) { f &= W[gidx[k]]; m |= W[gidx[k]]; }
                    full[g] = f; meet[g] = m;
                }
                wall = any & (full[0] | full[1]);
                cut = any & ~wall & meet[0] & meet[1];
                pit = any & ~wall & ~cut;
            }
        }
        u64 old = 0;
        for (int r = 0; r < 64; r++) {
            u64 bit = 1ULL << r;
            age[r]++;
            if ((double)age[r] > res[19]) res[19] = (double)age[r];
            long a = age[r] - T0;
            int ev = (wall & bit) ? 1 : (cut & bit) ? 2 : (pit & bit) ? 3 : (periodic & bit) ? 4 : 0;
            if (ev) {
                if (a >= 1) {
                    res[ev] += 1;
                    if (ev == 1) {
                        res[0] += 1;
                        int k = lg2(a); if (k < nbins) { binwall[k] += 1; binexp[k] += 1; }
                        if (nw < maxw) waits[nw++] = (int32_t)(a > 2000000000L ? 2000000000L : a);
                    } else { res[0] += 1; int k = lg2(a); if (k < nbins) binexp[k] += 1; }
                } else res[4 + ev] += 1;
                reseed(N, x, x1, snap, r, p16); age[r] = 0;
            } else {
                if (a >= 1) { res[0] += 1; int k = lg2(a); if (k < nbins) binexp[k] += 1; old |= bit; }
                if ((age[r] & (age[r] - 1)) == 0 && age[r] >= 4)
                    for (int i = 0; i < N; i++) snap[i] = (snap[i] & ~bit) | (x[i] & bit);
            }
        }
        if ((t & 63) == 0 && old) {
            int no = __builtin_popcountll(old);
            for (int i = 0; i < N; i++) {
                int l = lab[i] & 3;
                res[11 + l] += __builtin_popcountll(x[i] & old);
                res[15 + l] += no;
            }
        }
    }
    for (int r = 0; r < 64; r++) {
        if ((double)age[r] > res[9]) res[9] = (double)age[r];
        if (age[r] > T0) res[10] += 1;
    }
    free(x); free(y); free(x1); free(snap); free(W);
    return nw;
}

/* Vessel lifetimes of 64 replicas with permanent-death tracking.
 * life[r]: first t with x(t) = x(t+2) (kind 1), or t at which x(t) equalled a power-of-two snapshot (kind 2, an
 * upper bound for the entry into a longer cycle), -1 if running at the cap (kind 0).
 * Every P generations the largest dead sealed set D is computed: tD[r] = first check with D nonempty,
 * tG[r] = first check with D containing all cells of some watched group (ng groups), gfirst[r] = that group,
 * dsize[r] = |D| at the end.  x0: optional N seeds (packed), else soups of density p. */
void fu_life(int N, int K, const int32_t *nbr, uint32_t Bm, uint32_t Sm, int b, int ng, const int32_t *gidx,
             const int32_t *gstart, double p, long cap, int P, u64 seed, const u64 *x0, int64_t *life, int32_t *kind,
             int32_t *pop, int64_t *tD, int64_t *tG, int32_t *gfirst, int32_t *dsize) {
    sd(seed);
    uint32_t p16 = (uint32_t)(p * 65536.0 + 0.5);
    u64 *x = calloc(N + 1, 8), *y = calloc(N + 1, 8), *x1 = calloc(N + 1, 8), *snap = calloc(N + 1, 8),
        *W = calloc(N + 1, 8);
    if (x0) memcpy(x, x0, (size_t)N * 8);
    else for (int r = 0; r < 64; r++) reseed(N, x, x1, snap, r, p16);
    for (int i = 0; i < N; i++) { x1[i] = ~x[i]; snap[i] = ~x[i]; }
    u64 run = ~0ULL, seenD = 0, seenG = 0;
    for (int r = 0; r < 64; r++) { life[r] = -1; kind[r] = 0; pop[r] = 0; tD[r] = -1; tG[r] = -1; gfirst[r] = -1; dsize[r] = 0; }
    for (long t = 1; t <= cap && run; t++) {
        fu_step(N, K, nbr, x, y, Bm, Sm);
        u64 d2 = 0, ds = 0;
        for (int i = 0; i < N; i++) { d2 |= y[i] ^ x1[i]; ds |= y[i] ^ snap[i]; }
        u64 *tmp = x1; x1 = x; x = y; y = tmp;          /* x = state t, x1 = t - 1 */
        if (P > 0 && t % P == 0 && (run & ~(seenD & seenG))) {
            for (int i = 0; i < N; i++) W[i] = ~x[i];
            fu_peel(N, K, nbr, W, b);
            u64 any = 0;
            for (int i = 0; i < N; i++) any |= W[i];
            u64 newD = any & ~seenD & run;
            for (int r = 0; r < 64; r++) if (newD >> r & 1) tD[r] = t;
            seenD |= any;
            for (int g = 0; g < ng; g++) {
                u64 f = ~0ULL;
                for (int k = gstart[g]; k < gstart[g + 1]; k++) f &= W[gidx[k]];
                u64 nG = f & ~seenG & run;
                for (int r = 0; r < 64; r++) if (nG >> r & 1) { tG[r] = t; gfirst[r] = g; }
                seenG |= f & run;
            }
        }
        u64 done = (~d2 | ~ds) & run;
        if (done) {
            for (int i = 0; i < N; i++) W[i] = ~x[i];
            if (P > 0) fu_peel(N, K, nbr, W, b);
            for (int r = 0; r < 64; r++) if (done >> r & 1) {
                int c = 0, dz = 0;
                for (int i = 0; i < N; i++) { c += (x[i] >> r) & 1; dz += (W[i] >> r) & 1; }
                pop[r] = c; dsize[r] = dz;
                if (!((d2 >> r) & 1)) { life[r] = t - 2 < 0 ? 0 : t - 2; kind[r] = 1; }
                else { life[r] = t; kind[r] = 2; }
            }
            run &= ~done;
        }
        if ((t & (t - 1)) == 0 && t >= 4) memcpy(snap, x, (size_t)N * 8);
    }
    if (run) {
        for (int i = 0; i < N; i++) W[i] = ~x[i];
        if (P > 0) fu_peel(N, K, nbr, W, b);
        for (int r = 0; r < 64; r++) if (run >> r & 1) {
            int c = 0, dz = 0;
            for (int i = 0; i < N; i++) { c += (x[i] >> r) & 1; dz += (W[i] >> r) & 1; }
            pop[r] = c; dsize[r] = dz;
        }
    }
    free(x); free(y); free(x1); free(snap); free(W);
}
