/* ss.c (research/blast/split-slab): bit-sliced gump on a slab graph, 512 lanes, with
 *   (1) a plain renewal run that books excursion minima of each face ("flux stage": brute force + nu(p)),
 *   (2) forward-flux / fixed-effort multilevel splitting on the face population, clones separated by flips,
 *   (3) a dump mode for validation against reference/oracle.py.
 * Written from docs/AUTOMATON.md; shares no code with other steppers of this repository.
 *
 * Geometry file (geom.py): int32 n, A, nbr[n*12] (n = outside = always dead). Layer l = cells [l A, (l+1) A).
 *
 *   ss GEOM dump INIT.bin LANE GENS OUT.bin SEED
 *        lane LANE starts from INIT (n bytes 0/1), all other lanes from a 0.4 soup; writes n bytes per generation
 *        (generations 0..GENS) of lane LANE.
 *   ss GEOM ffs SEED NREP PA LAM0 DELTA M N0TGT NFLIP FDEP0 FDEP1 NPATH [PATHFILE] [BRUTEGENS]
 *        NREP independent replications of the whole estimator. See README.md for the exact algorithm.
 *   ss GEOM plain SEED GENS PA LAM0
 *        plain renewal run only (512 lanes, GENS generations): deaths, exposure, excursion-minimum histogram.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
typedef uint64_t u64;
#define W 8
#define NL (64 * W)
#define NB 10
typedef u64 vec __attribute__((vector_size(64), aligned(8)));

static int n, A, nw;
static int *nb;
static u64 *a, *b;
static u64 sm;
static inline u64 rnd(void) { u64 z = (sm += 0x9e3779b97f4a7c15ULL); z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
  z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; return z ^ (z >> 31); }
static inline u64 mix(u64 *s) { u64 z = (*s += 0x9e3779b97f4a7c15ULL); z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
  z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; return z ^ (z >> 31); }

#define FA(s, c, p, q, r) do { vec t_ = (p) ^ (q); s = t_ ^ (r); c = ((p) & (q)) | (t_ & (r)); } while (0)
static inline vec rule(const vec *x, vec me) {
  vec s0, c0, s1, c1, s2, c2, s3, c3, u, cu, b0, cv, p, cp, q, cq, b1, cw, b2, b3;
  FA(s0, c0, x[0], x[1], x[2]); FA(s1, c1, x[3], x[4], x[5]); FA(s2, c2, x[6], x[7], x[8]); FA(s3, c3, x[9], x[10], x[11]);
  FA(u, cu, s0, s1, s2); b0 = u ^ s3; cv = u & s3;            /* ones */
  FA(p, cp, c0, c1, c2); FA(q, cq, c3, cu, cv); b1 = p ^ q; cw = p & q;   /* twos */
  FA(b2, b3, cp, cq, cw);                                       /* fours, eights */
  return ~b3 & ((b2 & ~b1) | (me & ~b2 & b1 & b0));            /* count 4,5 -> alive; count 3 -> keeps state */
}
/* WD = 0: gump on the 8-layer slab. WD = w > 0 ("dice chain"): layers 0..w-1 follow the rule, layers w and w+1 are
   replaced after every generation by fresh fair coin flips (independent per cell, lane and generation), deeper
   layers are never read; the vessel then has ONE face (layer 0) and is a true Markov chain. */
static int WD = 0;
static void step(void) {
  int nstep = WD ? WD * A : n;
  for (int i = 0; i < nstep; i++) {
    const int *q = nb + 12 * (size_t)i; vec x[12], me, o;
    for (int t = 0; t < 12; t++) memcpy(&x[t], a + (size_t)q[t] * W, 64);
    memcpy(&me, a + (size_t)i * W, 64); o = rule(x, me); memcpy(b + (size_t)i * W, &o, 64);
  }
  if (WD) for (int i = WD * A; i < (WD + 2) * A; i++) for (int w = 0; w < W; w++) b[(size_t)i * W + w] = rnd();
  u64 *t = a; a = b; b = t;
}
/* bit-sliced population of layer starting at cell `base` : c[bit][word] */
static void laypop(int base, u64 c[NB][W]) {
  vec cc[NB]; for (int k = 0; k < NB; k++) cc[k] = (vec){0};
  for (int i = base; i < base + A; i++) { vec x; memcpy(&x, a + (size_t)i * W, 64);
    for (int k = 0; k < NB; k++) { vec t = cc[k] & x; cc[k] ^= x; x = t; } }
  for (int k = 0; k < NB; k++) memcpy(c[k], &cc[k], 64);
}
static inline u64 lt_mask(u64 c[NB][W], int w, int K) {   /* lanes with count < K */
  if (K <= 0) return 0; if (K >= (1 << NB)) return ~0ULL;
  u64 lt = 0, eq = ~0ULL;
  for (int k = NB - 1; k >= 0; k--) { u64 x = c[k][w]; if ((K >> k) & 1) { lt |= eq & ~x; eq &= x; } else eq &= ~x; }
  return lt;
}
static inline int lane_count(u64 c[NB][W], int lane) { int w = lane >> 6, k = lane & 63, p = 0;
  for (int t = 0; t < NB; t++) p |= (int)((c[t][w] >> k) & 1) << t; return p; }
static void lane_get(int lane, u64 *cfg) { int w = lane >> 6, k = lane & 63; memset(cfg, 0, 8 * nw);
  for (int i = 0; i < n; i++) cfg[i >> 6] |= ((a[(size_t)i * W + w] >> k) & 1) << (i & 63); }
static void lane_put(int lane, const u64 *cfg) { int w = lane >> 6, k = lane & 63; u64 bit = 1ULL << k;
  for (int i = 0; i < n; i++) { u64 *x = a + (size_t)i * W + w; *x = (*x & ~bit) | (((cfg[i >> 6] >> (i & 63)) & 1) << k); } }
static void lane_soup(int lane) { int w = lane >> 6, k = lane & 63; u64 bit = 1ULL << k; u64 thr = (u64)(0.4 * 18446744073709551616.0);
  for (int i = 0; i < n; i++) { u64 *x = a + (size_t)i * W + w; if (rnd() < thr) *x |= bit; else *x &= ~bit; } }
/* the flips of a clone: NFLIP cells, each uniform in the layers at depth FDEP0..FDEP1 beneath the active face */
static int NFLIP, FDEP0, FDEP1;
static void apply_flips(u64 *cfg, int face, u64 seed) {
  int nlay = FDEP1 - FDEP0 + 1;
  for (int f = 0; f < NFLIP; f++) { u64 z = mix(&seed); int r = (int)((z >> 11) % (u64)(nlay * A));
    int dep = FDEP0 + r / A, c = r % A; int lay = face ? 7 - dep : dep; int cell = lay * A + c;
    cfg[cell >> 6] ^= 1ULL << (cell & 63); }
}

/* ---------- flux stage (plain renewal run) ---------- */
#define BURN 1000
#define LCAP 50000
#define TMAX 1000   /* a trial not ended after TMAX generations is a failure (settled lane) */
static int PA, LAM0;
static int st[NL][2], curmin[NL][2]; static long burn[NL], age[NL];
static double g_E; static long g_N0, g_deaths, g_hist[1 << NB], g_cross[1 << NB], g_capped; static double g_sp, g_spp, g_ns;
/* store of level-0 crossings */
static u64 *s0; static int *s0face, *s0pop; static long s0cap, s0n;
static void flux_reset(void) { for (int l = 0; l < NL; l++) { lane_soup(l); burn[l] = BURN; age[l] = 0; st[l][0] = st[l][1] = 0; } }
static void flux_gen(int store) {
  step();
  u64 c[2][NB][W]; laypop(0, c[0]); laypop(7 * A, c[1]);
  for (int l = 0; l < NL; l++) {
    if (burn[l] > 0) { if (--burn[l] == 0) { for (int f = 0; f < 2; f++) st[l][f] = 0; age[l] = 0; } continue; }
    age[l]++;
    int dead = 0;
    for (int f = 0; f < (WD ? 1 : 2); f++) {
      int p = lane_count(c[f], l);
      if (st[l][f] == 0) { if (p >= PA) st[l][f] = 1; else { if (p == 0) dead = 1; continue; } }
      g_E += 1; g_sp += p; g_spp += (double)p * p; g_ns += 1;
      if (st[l][f] == 1) {
        if (p <= LAM0) { g_N0++; g_cross[p]++; st[l][f] = 2; curmin[l][f] = p;
          if (store && s0n < s0cap) { lane_get(l, s0 + (size_t)s0n * nw); s0face[s0n] = f; s0pop[s0n] = p; s0n++; }
          if (p == 0) { g_deaths++; g_hist[0]++; dead = 1; } }
      } else {
        if (p < curmin[l][f]) curmin[l][f] = p;
        if (p == 0) { g_deaths++; g_hist[0]++; dead = 1; }
        else if (p >= PA) { g_hist[curmin[l][f]]++; st[l][f] = 1; }
      }
    }
    if (!dead && age[l] >= LCAP) { g_capped++; dead = 1; }
    if (dead) { lane_soup(l); burn[l] = BURN; st[l][0] = st[l][1] = 0; }
  }
}

/* ---------- splitting stages ---------- */
typedef struct { long cap, cnt; u64 *state; int *face, *pop, *parent, *t, *anc; u64 *seed; } store_t;
static void st_alloc(store_t *s, long cap, int withstate) { s->cap = cap; s->cnt = 0;
  s->state = withstate ? malloc((size_t)cap * nw * 8) : 0; s->face = malloc(4 * cap); s->pop = malloc(4 * cap);
  s->parent = malloc(4 * cap); s->t = malloc(4 * cap); s->anc = malloc(4 * cap); s->seed = malloc(8 * cap); }

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage\n"); return 1; }
  FILE *f = fopen(argv[1], "rb"); int32_t hd[2]; if (fread(hd, 4, 2, f) != 2) return 1; n = hd[0]; A = hd[1]; nw = (n + 63) / 64;
  nb = malloc(4 * 12 * (size_t)n); if (fread(nb, 4, 12 * (size_t)n, f) != 12 * (size_t)n) return 1; fclose(f);
  a = aligned_alloc(64, (size_t)(n + 1) * W * 8); b = aligned_alloc(64, (size_t)(n + 1) * W * 8);
  memset(a, 0, (size_t)(n + 1) * W * 8); memset(b, 0, (size_t)(n + 1) * W * 8);
  const char *mode = argv[2];
  if (getenv("WD")) WD = atoi(getenv("WD"));
  if (!strcmp(mode, "dump")) {
    const char *initf = argv[3]; int lane = atoi(argv[4]); long gens = atol(argv[5]); const char *outf = argv[6];
    sm = strtoull(argv[7], 0, 10) * 0x2545F4914F6CDD1DULL + 99;
    for (int l = 0; l < NL; l++) lane_soup(l);
    unsigned char *buf = malloc(n); FILE *g = fopen(initf, "rb"); if (fread(buf, 1, n, g) != (size_t)n) return 1; fclose(g);
    u64 *cfg = calloc(nw, 8); for (int i = 0; i < n; i++) if (buf[i]) cfg[i >> 6] |= 1ULL << (i & 63);
    lane_put(lane, cfg); FILE *o = fopen(outf, "wb");
    for (long gen = 0; gen <= gens; gen++) { lane_get(lane, cfg); for (int i = 0; i < n; i++) buf[i] = (cfg[i >> 6] >> (i & 63)) & 1;
      fwrite(buf, 1, n, o); if (gen < gens) step(); }
    fclose(o); return 0;
  }
  if (!strcmp(mode, "plain")) {
    sm = strtoull(argv[3], 0, 10) * 0x2545F4914F6CDD1DULL + 7; long gens = atol(argv[4]); PA = atoi(argv[5]); LAM0 = atoi(argv[6]);
    flux_reset(); for (long g = 0; g < gens; g++) flux_gen(0);
    printf("PLAIN A %d PA %d LAM0 %d E %.6e N0 %ld deaths %ld capped %ld meanpop %.4f varpop %.4f lntau_brute %.4f +- %.4f\n", A, PA, LAM0, g_E, g_N0,
           g_deaths, g_capped, g_sp / g_ns, g_spp / g_ns - (g_sp / g_ns) * (g_sp / g_ns), g_deaths ? log(g_E / g_deaths) : 0.0, g_deaths ? 1 / sqrt(g_deaths) : 0.0);
    long cum = 0; for (int p = 0; p <= LAM0; p++) { cum += g_hist[p]; if (g_hist[p] || g_cross[p]) printf("HIST %d min %ld cum %ld cross %ld\n", p, g_hist[p], cum, g_cross[p]); }
    return 0;
  }
  if (!strcmp(mode, "lag")) {   /* ss GEOM lag SEED GENS [PATHFILE]: natural deaths of plain gump (no flips). Mean population of the layer at depth d
       beneath a dying face by lag before its death, and per death the face cells' last-alive generations. */
    sm = strtoull(argv[3], 0, 10) * 0x2545F4914F6CDD1DULL + 7; long gens = atol(argv[4]);
    #define RB 64
    static u64 rc[RB][8][NB][W]; static long born[NL]; static u64 fring[RB][2][512][W]; FILE *pp = argc > 5 ? fopen(argv[5], "w") : 0;
    double sum[RB][8] = {{0}}, sq[RB][8] = {{0}}, m1[8] = {0}, m2[8] = {0}; long nd = 0, ns = 0; double E = 0;
    if (A > 512) return 1;
    if (pp) fprintf(pp, "# A %d; one line per natural face death: P face age pop(-1) pop(-2) ... pop(-24) | last[c] for c = 0..A-1 (cell c of the dying face: last generation alive relative to the death generation, -1..-63; -64 = not alive in the last 63 generations)\n", A);
    for (int l = 0; l < NL; l++) { lane_soup(l); born[l] = 0; }
    for (long g = 1; g <= gens; g++) { step(); int slot = g % RB; for (int y = 0; y < 8; y++) laypop(y * A, rc[slot][y]);
      for (int c2 = 0; c2 < A; c2++) { memcpy(fring[slot][0][c2], a + (size_t)c2 * W, 64); memcpy(fring[slot][1][c2], a + (size_t)(7 * A + c2) * W, 64); }
      if ((g & 15) == 0) for (int l = 0; l < NL; l++) if (g - born[l] > 1000) { for (int y = 0; y < 8; y++) { int r = lane_count(rc[slot][y], l); m1[y] += r; m2[y] += (double)r * r; } ns++; }
      for (int w = 0; w < W; w++) { u64 z0 = ~0ULL, z1 = ~0ULL; for (int k = 0; k < NB; k++) { z0 &= ~rc[slot][0][k][w]; z1 &= ~rc[slot][7][k][w]; }
        u64 z = z0 | z1;
        while (z) { int k = __builtin_ctzll(z); z &= z - 1; int l = 64 * w + k; int f = (z0 >> k) & 1 ? 0 : 1; long age = g - born[l];
          if (age > 1000 + RB) { nd++; E += 2.0 * (age - 1000 - RB);
            for (int lag = 0; lag < RB; lag++) { int sl = (int)(((g - lag) % RB + RB) % RB);
              for (int d = 0; d < 8; d++) { int y = f ? 7 - d : d; int q = lane_count(rc[sl][y], l); sum[lag][d] += q; sq[lag][d] += (double)q * q; } }
            if (pp) { fprintf(pp, "P %d %ld", f, age); for (int lag = 1; lag <= 24; lag++) fprintf(pp, " %d", lane_count(rc[((g - lag) % RB + RB) % RB][f ? 7 : 0], l)); fprintf(pp, " |");
              for (int c2 = 0; c2 < A; c2++) { int last = -RB; for (int lag = 1; lag < RB; lag++) if ((fring[((g - lag) % RB + RB) % RB][f][c2][w] >> k) & 1) { last = -lag; break; } fprintf(pp, " %d", last); } fprintf(pp, "\n"); } }
          lane_soup(l); born[l] = g; } } }
    for (int l = 0; l < NL; l++) if (gens - born[l] > 1000 + RB) E += 2.0 * (gens - born[l] - 1000 - RB);
    printf("LAG A %d deaths %ld (lives older than %d generations) exposure %.4e lntau_brute %.4f +- %.4f\n", A, nd, 1000 + RB, E, nd ? log(E / nd) : 0.0, nd ? 1 / sqrt(nd) : 0.0);
    printf("stationary mean (sd) by layer:"); for (int y = 0; y < 8; y++) printf(" %.2f (%.2f)", m1[y] / ns, sqrt(m2[y] / ns - (m1[y] / ns) * (m1[y] / ns))); printf("\n");
    printf("lag: mean pop at depth 0..7 beneath the dying face; then sd of the face pop; then z = (mean - stationary)/sd for depth 0..7\n");
    for (int lag = 0; lag < RB; lag += (lag < 24 ? 1 : 4)) { printf("%2d:", lag); for (int d = 0; d < 8; d++) printf(" %6.2f", sum[lag][d] / nd);
      printf("  | %5.2f |", sqrt(sq[lag][0] / nd - (sum[lag][0] / nd) * (sum[lag][0] / nd))); for (int d = 0; d < 8; d++) { int y = d; double mu = (m1[y] + m1[7 - y]) / 2 / ns, sd = sqrt((m2[y] + m2[7 - y]) / 2 / ns - mu * mu); printf(" %6.2f", (sum[lag][d] / nd - mu) / sd); } printf("\n"); }
    return 0;
  }
  if (!strcmp(mode, "sub")) {
    /* Subset simulation on the dice chain (WD = w > 0), exact for that Markov chain.
       ss G sub SEED NREP LAM1 DELTA NBATCH NSWEEP KFLIP TPRE TWIN [PATHFILE]
       A chain = (stationary initial state, T = TPRE + TWIN generations of dice for layers w, w+1). Score = minimum face population over
       generations TPRE+1..T, defined only if the face is alive at generation TPRE. Event {score = 0} = {death time in (TPRE, T]}, probability
       TWIN / tau. Levels LAM1 > LAM1 - DELTA > ... > 0. P_1 from NBATCH*512 independent chains; at each level the chains at or below it are
       copied round-robin to refill the ensemble and moved by NSWEEP Metropolis sweeps (proposal: flip KFLIP dice bits uniform in space-time;
       accept iff the score stays at or below the level), then the share at or below the next level is P_{i+1}. */
    if (!WD) { fprintf(stderr, "sub needs WD\n"); return 1; }
    u64 seed0 = strtoull(argv[3], 0, 10); int nrep = atoi(argv[4]); int LAM1 = atoi(argv[5]), DELTA = atoi(argv[6]), NBATCH = atoi(argv[7]), NSWEEP = atoi(argv[8]), KFLIP = atoi(argv[9]);
    int TPRE = atoi(argv[10]), TWIN = atoi(argv[11]); int T = TPRE + TWIN; FILE *pp = (argc > 12 && strcmp(argv[12], "-")) ? fopen(argv[12], "w") : 0; if (T > 127) return 1;
    int WBACK = argc > 13 ? atoi(argv[13]) : 0;   /* > 0: every second sweep proposes flips only in the WBACK generations of dice before the chain's minimum */
    size_t ssz = (size_t)(n + 1) * W, dsz = (size_t)T * 2 * A * W; long NC = (long)NBATCH * NL;
    u64 *init = malloc(NBATCH * ssz * 8), *init2 = malloc(NBATCH * ssz * 8), *D = malloc(NBATCH * dsz * 8), *D2 = malloc(NBATCH * dsz * 8), *Dp = malloc(dsz * 8), *pl = malloc(ssz * 8);
    int *score = malloc(4 * NC), *score2 = malloc(4 * NC), *seeds = malloc(4 * NC), *gmin = malloc(4 * NC), *gmin2 = malloc(4 * NC); static int am[NL]; static short popser[NL][128]; static int sc[NL]; static long page[NL];
    double *rate = malloc(8 * nrep); double sumlnP[64] = {0}; long nlevP[64] = {0}; double accs = 0, accn = 0; int lamlist[64], nlam = 0;
    #define EVAL(initb, diceb) do { memcpy(a, (initb), ssz * 8); for (int t_ = 0; t_ < T; t_++) { \
        for (int i_ = 0; i_ < WD * A; i_++) { const int *q_ = nb + 12 * (size_t)i_; vec x_[12], me_, o_; for (int u_ = 0; u_ < 12; u_++) memcpy(&x_[u_], a + (size_t)q_[u_] * W, 64); \
          memcpy(&me_, a + (size_t)i_ * W, 64); o_ = rule(x_, me_); memcpy(b + (size_t)i_ * W, &o_, 64); } \
        memcpy(b + (size_t)WD * A * W, (diceb) + (size_t)t_ * 2 * A * W, (size_t)2 * A * W * 8); { u64 *sw_ = a; a = b; b = sw_; } \
        u64 c_[NB][W]; laypop(0, c_); for (int l_ = 0; l_ < NL; l_++) popser[l_][t_ + 1] = lane_count(c_, l_); } \
      for (int l_ = 0; l_ < NL; l_++) { int m_ = 1 << 20, a_ = T; if (popser[l_][TPRE] > 0) for (int g_ = TPRE + 1; g_ <= T; g_++) if (popser[l_][g_] < m_) { m_ = popser[l_][g_]; a_ = g_; } sc[l_] = m_; am[l_] = a_; } } while (0)
    printf("# sub A %d WD %d LAM1 %d DELTA %d chains %ld NSWEEP %d KFLIP %d TPRE %d TWIN %d\n", A, WD, LAM1, DELTA, NC, NSWEEP, KFLIP, TPRE, TWIN);
    sm = seed0 * 0x2545F4914F6CDD1DULL + 4242; for (int l = 0; l < NL; l++) { lane_soup(l); page[l] = 0; }
    for (int g = 0; g < 1000; g++) step(); for (int l = 0; l < NL; l++) page[l] = 1000;
    for (int rep = 0; rep < nrep; rep++) {
      long nvalid = 0;
      for (int bt = 0; bt < NBATCH; bt++) {
        for (int g = 0; g < 64; g++) step();
        u64 c[NB][W]; laypop(0, c); int valid[NL];
        for (int l = 0; l < NL; l++) { page[l] += 64; int p0 = lane_count(c, l); valid[l] = (p0 > 0 && page[l] >= 1000); if (p0 == 0) { lane_soup(l); page[l] = 0; } }
        memcpy(pl, a, ssz * 8); memcpy(init + bt * ssz, a, ssz * 8); u64 *d = D + bt * dsz; for (size_t x = 0; x < dsz; x++) d[x] = rnd();
        EVAL(init + bt * ssz, d); for (int l = 0; l < NL; l++) { score[bt * NL + l] = valid[l] ? sc[l] : (1 << 20); gmin[bt * NL + l] = am[l]; nvalid += valid[l]; }
        memcpy(a, pl, ssz * 8);
      }
      memcpy(pl, a, ssz * 8);
      int lam = LAM1, lev = 0; double prod = 1; long denom = nvalid; printf("REP %d valid %ld :", rep, nvalid);
      for (;;) {
        long ns = 0; for (long j = 0; j < NC; j++) if (score[j] <= lam) seeds[ns++] = (int)j;
        double P = (double)ns / denom; prod *= P; printf(" %d:%ld", lam, ns); lamlist[lev] = lam; if (ns) { sumlnP[lev] += log(P); nlevP[lev]++; } lev++; if (lev > nlam) nlam = lev;
        if (ns == 0 || lam == 0) break;
        u64 r0 = rnd() % (u64)ns;
        memset(init2, 0, NBATCH * ssz * 8); memset(D2, 0, NBATCH * dsz * 8);
        for (long j = 0; j < NC; j++) { int src = seeds[(r0 + (u64)j) % (u64)ns]; int sb = src / NL, sl = src % NL, db = (int)(j / NL), dl = (int)(j % NL);
          const u64 *si = init + sb * ssz + (sl >> 6); u64 *di = init2 + db * ssz + (dl >> 6); int sk = sl & 63, dk = dl & 63;
          for (int i = 0; i < n; i++) di[(size_t)i * W] |= ((si[(size_t)i * W] >> sk) & 1) << dk;
          const u64 *sd = D + sb * dsz + (sl >> 6); u64 *dd = D2 + db * dsz + (dl >> 6); size_t nd2 = (size_t)T * 2 * A;
          for (size_t i = 0; i < nd2; i++) dd[i * W] |= ((sd[i * W] >> sk) & 1) << dk;
          score2[j] = score[src]; gmin2[j] = gmin[src]; }
        { u64 *t1 = init; init = init2; init2 = t1; t1 = D; D = D2; D2 = t1; int *t2 = score; score = score2; score2 = t2; t2 = gmin; gmin = gmin2; gmin2 = t2; }
        for (int sw = 0; sw < NSWEEP; sw++) for (int bt = 0; bt < NBATCH; bt++) { u64 *d = D + bt * dsz; memcpy(Dp, d, dsz * 8);
          int foc = (WBACK > 0 && (sw & 1)); static int tlo[NL], thi[NL];
          for (int l = 0; l < NL; l++) { tlo[l] = T; thi[l] = -1; for (int k = 0; k < KFLIP; k++) { u64 z = rnd(); size_t pos;
              if (foc) { int g0 = gmin[bt * NL + l]; int t = g0 - WBACK + (int)((z >> 40) % (u64)WBACK); if (t < 0) t = 0; if (t < tlo[l]) tlo[l] = t; if (t > thi[l]) thi[l] = t;
                pos = (size_t)t * 2 * A + (size_t)((z >> 8) % (u64)(2 * A)); }
              else pos = (size_t)((z >> 8) % (u64)((size_t)T * 2 * A));
              Dp[pos * W + (l >> 6)] ^= 1ULL << (l & 63); } }
          EVAL(init + bt * ssz, Dp); u64 acc[W] = {0};
          for (int l = 0; l < NL; l++) { accn++; int ok = sc[l] <= lam; if (ok && foc) ok = (tlo[l] >= am[l] - WBACK && thi[l] < am[l]);   /* the reverse move must be proposable */
            if (ok) { acc[l >> 6] |= 1ULL << (l & 63); score[bt * NL + l] = sc[l]; gmin[bt * NL + l] = am[l]; accs++; } }
          for (size_t x = 0; x < dsz; x++) { int w = (int)(x % W); d[x] = (d[x] & ~acc[w]) | (Dp[x] & acc[w]); } }
        denom = NC; lam = lam - DELTA > 0 ? lam - DELTA : 0;
      }
      rate[rep] = prod / TWIN; printf(" rate %.5e lntau %.4f\n", rate[rep], rate[rep] > 0 ? -log(rate[rep]) : 99.0); fflush(stdout);
      if (pp && rate[rep] > 0) for (int bt = 0; bt < NBATCH; bt++) { EVAL(init + bt * ssz, D + bt * dsz);   /* dying paths of the dice chain: face population by generation */
          for (int l = 0; l < NL; l++) if (sc[l] == 0) { int gd = TPRE + 1; while (popser[l][gd] > 0) gd++; fprintf(pp, "S %d %d %d |", rep, bt * NL + l, gd);
            for (int g = gd - 1; g >= 1 && g >= gd - 24; g--) fprintf(pp, " %d", popser[l][g]); fprintf(pp, "\n"); } }
      memcpy(a, pl, ssz * 8);
    }
    double m = 0, v = 0; for (int i = 0; i < nrep; i++) m += rate[i]; m /= nrep; for (int i = 0; i < nrep; i++) v += (rate[i] - m) * (rate[i] - m);
    printf("SUMMARY sub A %d WD %d reps %d lntau %.4f +- %.4f (rel sd of one replication %.3f) acceptance %.3f\n", A, WD, nrep, -log(m), nrep > 1 ? sqrt(v / (nrep - 1) / nrep) / m : 0,
           nrep > 1 ? sqrt(v / (nrep - 1)) / m : 0, accs / (accn > 0 ? accn : 1));
    for (int i = 0; i < nlam; i++) if (nlevP[i]) printf("LEVEL %d lam %d mean lnP %.4f (%ld reps)\n", i, lamlist[i], sumlnP[i] / nlevP[i], nlevP[i]);
    if (pp) fclose(pp);
    return 0;
  }
  /* ffs */
  u64 seed0 = strtoull(argv[3], 0, 10); int nrep = atoi(argv[4]); PA = atoi(argv[5]); LAM0 = atoi(argv[6]); int DELTA = atoi(argv[7]);
  long M = atol(argv[8]); long N0TGT = atol(argv[9]); NFLIP = atoi(argv[10]); FDEP0 = atoi(argv[11]); FDEP1 = atoi(argv[12]);
  int npath = atoi(argv[13]); const char *pathf = argc > 14 ? argv[14] : 0;
  int lam[256], nlev = 0; for (int x = LAM0; x > 0; x -= DELTA) lam[nlev++] = x; lam[nlev++] = 0;   /* lam[0] = LAM0, ..., lam[nlev-1] = 0 */
  s0cap = M; s0 = malloc((size_t)s0cap * nw * 8); s0face = malloc(4 * s0cap); s0pop = malloc(4 * s0cap);
  store_t *S = malloc(sizeof(store_t) * nlev); for (int i = 1; i < nlev; i++) st_alloc(&S[i], M, 0);
  u64 *bufA = malloc((size_t)M * nw * 8), *bufB = malloc((size_t)M * nw * 8); u64 *cfg = malloc(8 * nw);
  FILE *pf = pathf ? fopen(pathf, "w") : 0;
  u64 *bak = aligned_alloc(64, (size_t)(n + 1) * W * 8);
  if (pf) { fprintf(pf, "# n %d A %d PA %d levels", n, A, PA); for (int i = 0; i < nlev; i++) fprintf(pf, " %d", lam[i]);
    fprintf(pf, " NFLIP %d FDEP %d %d\n", NFLIP, FDEP0, FDEP1); }
  double *rate = malloc(8 * nrep); double sumP[256] = {0}, sumReach[256] = {0}; double sumPhi = 0;
  long totS[256] = {0}, totM[256] = {0}, timeouts = 0, lanegens = 0;
  printf("# A %d n %d PA %d levels", A, n, PA); for (int i = 0; i < nlev; i++) printf(" %d", lam[i]);
  printf(" M %ld N0TGT %ld NFLIP %d FDEP %d %d\n", M, N0TGT, NFLIP, FDEP0, FDEP1);
  for (int rep = 0; rep < nrep; rep++) {
    sm = (seed0 * 1000003ULL + rep) * 0x2545F4914F6CDD1DULL + 12345;
    /* stage 0: flux */
    double E0 = g_E; long N00 = g_N0; s0n = 0; if (rep == 0) flux_reset();   /* one persistent plain ensemble; its windows feed the replications */
    do { for (int g = 0; g < 64; g++) flux_gen(1); lanegens += 64L * NL; } while (g_N0 - N00 < N0TGT);
    double E = g_E - E0; long N0 = g_N0 - N00; double phi = N0 / E; sumPhi += phi;
    memcpy(bak, a, (size_t)(n + 1) * W * 8);
    double r = phi; int ok = 1; long Sprev = s0n; u64 *prev = s0, *cur = bufA;
    int *pface = s0face, *ppop = s0pop; int *pt = 0;
    printf("REP %d N0 %ld E %.4e", rep, N0, E);
    for (int i = 1; i < nlev && ok; i++) {
      store_t *T = &S[i]; T->cnt = 0; int L = lam[i];
      long launched = 0, done = 0, succ = 0; u64 r0 = rnd() % (u64)Sprev;
      int lpar[NL]; u64 lseed[NL]; long lstart[NL]; int lface[NL]; u64 busy[W] = {0}, act1[W] = {0}; long gen = 0;
      #define LAUNCH(lane) do { int l_ = (lane); int w_ = l_ >> 6; u64 bit_ = 1ULL << (l_ & 63); busy[w_] &= ~bit_; \
        while (launched < M) { long j_ = launched++; int par_ = (int)((r0 + (u64)j_) % (u64)Sprev); u64 sd_ = rnd(); \
          memcpy(cfg, prev + (size_t)par_ * nw, 8 * nw); apply_flips(cfg, pface[par_], sd_); \
          if (ppop[par_] <= L) { long k_ = T->cnt++; memcpy(cur + (size_t)k_ * nw, cfg, 8 * nw); T->face[k_] = pface[par_]; T->pop[k_] = ppop[par_]; \
            T->parent[k_] = par_; T->seed[k_] = sd_; T->t[k_] = pt ? pt[par_] : 0; done++; succ++; continue; } \
          lane_put(l_, cfg); lpar[l_] = par_; lseed[l_] = sd_; lstart[l_] = gen; lface[l_] = pface[par_]; busy[w_] |= bit_; \
          if (pface[par_]) act1[w_] |= bit_; else act1[w_] &= ~bit_; break; } } while (0)
      for (int l = 0; l < NL; l++) LAUNCH(l);
      for (;;) {
        u64 any = 0; for (int w = 0; w < W; w++) any |= busy[w]; if (!any) break;
        step(); gen++; lanegens += NL;
        u64 c[2][NB][W]; laypop(0, c[0]); laypop(7 * A, c[1]);
        for (int w = 0; w < W; w++) {
          u64 le0 = lt_mask(c[0], w, L + 1), le1 = lt_mask(c[1], w, L + 1), ge0 = ~lt_mask(c[0], w, PA), ge1 = ~lt_mask(c[1], w, PA);
          u64 sc = busy[w] & ((~act1[w] & le0) | (act1[w] & le1)); u64 fl = busy[w] & ~sc & ((~act1[w] & ge0) | (act1[w] & ge1));
          if ((gen & 255) == 0) { for (int k = 0; k < 64; k++) if (((busy[w] & ~sc & ~fl) >> k) & 1 && gen - lstart[64 * w + k] > TMAX) { fl |= 1ULL << k; timeouts++; } }
          while (sc) { int k = __builtin_ctzll(sc); sc &= sc - 1; int l = 64 * w + k; long kk = T->cnt++;
            lane_get(l, cur + (size_t)kk * nw); T->face[kk] = lface[l]; T->pop[kk] = lane_count(c[lface[l]], l);
            T->parent[kk] = lpar[l]; T->seed[kk] = lseed[l]; T->t[kk] = (pt ? pt[lpar[l]] : 0) + (int)(gen - lstart[l]); done++; succ++; LAUNCH(l); }
          while (fl) { int k = __builtin_ctzll(fl); fl &= fl - 1; int l = 64 * w + k; done++; LAUNCH(l); }
        }
      }
      double P = (double)succ / (double)M; r *= P; totS[i] += succ; totM[i] += M; sumP[i] += P; sumReach[i] += r;
      printf(" %ld", succ);
      if (succ == 0) { ok = 0; break; }
      Sprev = succ; prev = cur; cur = (cur == bufA) ? bufB : bufA; pface = T->face; ppop = T->pop; pt = T->t;
    }
    memcpy(a, bak, (size_t)(n + 1) * W * 8);
    rate[rep] = ok ? r : 0; printf(" rate %.6e lntau %.4f\n", rate[rep], rate[rep] > 0 ? -log(rate[rep]) : 99.0); fflush(stdout);
    /* reactive paths: lineages of a sample of deaths (stage-0 state + the flip seeds of every stage) */
    if (pf && ok) { store_t *T = &S[nlev - 1]; long nd = T->cnt; for (int q = 0; q < npath && q < nd; q++) {
        long idx = (long)(rnd() % (u64)nd); u64 seeds[256]; long id = idx; int tt = T->t[idx], face = T->face[idx];
        for (int i = nlev - 1; i >= 1; i--) { seeds[i] = S[i].seed[id]; id = S[i].parent[id]; }
        fprintf(pf, "PATH rep %d face %d t %d s0pop %d seeds", rep, face, tt, s0pop[id]);
        for (int i = 1; i < nlev; i++) fprintf(pf, " %llu", (unsigned long long)seeds[i]);
        fprintf(pf, " state "); for (int x = 0; x < nw; x++) fprintf(pf, "%016llx", (unsigned long long)s0[(size_t)id * nw + x]); fprintf(pf, "\n"); }
      fflush(pf); }
  }
  /* summary: mean of the replications' rates, error from their scatter */
  double m = 0, v = 0; for (int i = 0; i < nrep; i++) m += rate[i]; m /= nrep; for (int i = 0; i < nrep; i++) v += (rate[i] - m) * (rate[i] - m);
  double se = nrep > 1 ? sqrt(v / (nrep - 1) / nrep) : 0;
  printf("SUMMARY A %d reps %d lntau %.4f +- %.4f (rel sd of one replication %.3f) phi %.5e timeouts %ld lanegens %.3e\n", A, nrep, -log(m), se / m,
         nrep > 1 ? sqrt(v / (nrep - 1)) / m : 0, sumPhi / nrep, timeouts, (double)lanegens);
  printf("FLUXSTAGE E %.6e N0 %ld deaths %ld capped %ld meanpop %.4f varpop %.4f", g_E, g_N0, g_deaths, g_capped, g_sp / g_ns, g_spp / g_ns - (g_sp / g_ns) * (g_sp / g_ns));
  if (g_deaths) printf(" lntau_brute %.4f +- %.4f", log(g_E / g_deaths), 1 / sqrt(g_deaths)); printf("\n");
  /* per level: pooled P, the split estimate of nu(level) = phi * prod P, and the plain-run nu(level) from excursion minima */
  { long cum[1 << NB]; long cc = 0; for (int p = 0; p < (1 << NB); p++) { cc += g_hist[p]; cum[p] = cc; }
    for (int i = 1; i < nlev; i++) { double nus = sumReach[i] / nrep; long nat = cum[lam[i]];
      printf("LEVEL %d lam %d P %.5f lnnu_split %.4f natural_count %ld lnnu_plain %.4f diff %.4f +- %.4f\n", i, lam[i], (double)totS[i] / totM[i], log(nus), nat,
             nat ? log(nat / g_E) : 0.0, nat ? log(nus) - log(nat / g_E) : 0.0, nat ? 1 / sqrt(nat) : 0.0); } }
  for (int i = 0; i < nrep; i++) printf("RATE %d %.8e\n", i, rate[i]);
  if (pf) fclose(pf);
  return 0;
}
