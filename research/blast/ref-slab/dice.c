/* dice.c (research/blast/ref-slab): the referee's own stepper for gump on an 8-layer slab graph and for the
 * "dice chain" of agent split-slab (layers 0..5 on gump's rule, layers 6 and 7 replaced after every generation by
 * fair coins, independent per cell and generation; ONE face = layer 0; a face death = the first generation at
 * which layer 0 is empty).  Written from docs/AUTOMATON.md and split-slab's README definition; no code shared
 * with ss.c (own graph builder rgeom.py, own ripple counter, own generator, own bookkeeping).
 *
 *   dice GRAPH dump INIT.bin GENS OUT.bin        plain gump, lane 0 from INIT (n bytes), writes n bytes x (GENS+1)
 *   dice GRAPH brute WD SEED GENS [PATHFILE]     512 lanes; WD = 6: dice chain (one face); WD = 0: gump (two faces)
 *        every life: 0.4 soup, BURN = 1000 generations not counted, ends at the first face death;
 *        tau_face = face-generations / face deaths.  PATHFILE: one line per death, the dying face's population
 *        1..24 generations before the death generation ("S 0 lane gen | p1 p2 ...").
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
typedef uint64_t u64;
#define NW 8
#define LANES (64 * NW)
typedef u64 V __attribute__((vector_size(64), aligned(8)));
#define BURN 1000
#define RING 32
#define PB 9

static int n, A; static int *nbr; static u64 *cur, *nxt;
static u64 xs[4];
static inline u64 rotl(u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static inline u64 rng(void) { u64 r = rotl(xs[0] + xs[3], 23) + xs[0], t = xs[1] << 17;
  xs[2] ^= xs[0]; xs[3] ^= xs[1]; xs[1] ^= xs[2]; xs[0] ^= xs[3]; xs[2] ^= t; xs[3] = rotl(xs[3], 45); return r; }
static void seed_rng(u64 s) { for (int i = 0; i < 4; i++) { s += 0x9e3779b97f4a7c15ULL; u64 z = s; z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
  z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; xs[i] = z ^ (z >> 31); } }

static inline V ld(const u64 *p, int i) { V v; memcpy(&v, p + (size_t)i * NW, 64); return v; }
static void step_rule(int ncell) {
  for (int i = 0; i < ncell; i++) {
    const int *q = nbr + 12 * i; V c0 = {0}, c1 = {0}, c2 = {0}, c3 = {0};
    for (int t = 0; t < 12; t++) { V x = ld(cur, q[t]), k;
      k = c0 & x; c0 ^= x; x = k; k = c1 & x; c1 ^= x; x = k; k = c2 & x; c2 ^= x; x = k; c3 ^= x; }
    V me = ld(cur, i);
    V o = ~c3 & ((c2 & ~c1) | (me & ~c2 & c1 & c0));      /* 4 or 5 -> alive; 3 -> keeps its state; else dead */
    memcpy(nxt + (size_t)i * NW, &o, 64);
  }
}
static void soup_lane(int lane, int ncell) { int w = lane >> 6; u64 bit = 1ULL << (lane & 63);
  for (int i = 0; i < ncell; i++) { u64 *x = cur + (size_t)i * NW + w; if ((rng() >> 11) * (1.0 / 9007199254740992.0) < 0.4) *x |= bit; else *x &= ~bit; } }
static void facepop(int base, u64 c[PB][NW]) { V cc[PB]; for (int k = 0; k < PB; k++) cc[k] = (V){0};
  for (int i = base; i < base + A; i++) { V x = ld(cur, i); for (int k = 0; k < PB; k++) { V t = cc[k] & x; cc[k] ^= x; x = t; } }
  for (int k = 0; k < PB; k++) memcpy(c[k], &cc[k], 64); }
static inline int popof(u64 c[PB][NW], int lane) { int w = lane >> 6, k = lane & 63, p = 0; for (int t = 0; t < PB; t++) p |= (int)((c[t][w] >> k) & 1) << t; return p; }

int main(int argc, char **argv) {
  if (argc < 4) return 1;
  FILE *f = fopen(argv[1], "rb"); int32_t hd[2]; if (!f || fread(hd, 4, 2, f) != 2) return 1; n = hd[0]; A = hd[1];
  nbr = malloc(4 * 12 * (size_t)n); if (fread(nbr, 4, 12 * (size_t)n, f) != 12 * (size_t)n) return 1; fclose(f);
  cur = aligned_alloc(64, (size_t)(n + 1) * NW * 8); nxt = aligned_alloc(64, (size_t)(n + 1) * NW * 8);
  memset(cur, 0, (size_t)(n + 1) * NW * 8); memset(nxt, 0, (size_t)(n + 1) * NW * 8);
  if (!strcmp(argv[2], "dump")) {
    long gens = atol(argv[4]); unsigned char *buf = malloc(n); FILE *g = fopen(argv[3], "rb"); if (fread(buf, 1, n, g) != (size_t)n) return 1; fclose(g);
    seed_rng(12345); for (int l = 1; l < LANES; l++) soup_lane(l, n);
    for (int i = 0; i < n; i++) { u64 *x = cur + (size_t)i * NW; *x = (*x & ~1ULL) | (buf[i] & 1); }
    FILE *o = fopen(argv[5], "wb");
    for (long t = 0; t <= gens; t++) { for (int i = 0; i < n; i++) buf[i] = cur[(size_t)i * NW] & 1; fwrite(buf, 1, n, o);
      if (t < gens) { step_rule(n); u64 *s = cur; cur = nxt; nxt = s; } }
    fclose(o); return 0;
  }
  if (!strcmp(argv[2], "brute")) {
    int WD = atoi(argv[3]); seed_rng(strtoull(argv[4], 0, 10) * 2654435761ULL + 17); long gens = atol(argv[5]); FILE *pp = argc > 6 ? fopen(argv[6], "w") : 0;
    int nf = WD ? 1 : 2, ncell = WD ? WD * A : n; if (WD && (WD + 2) * A > n) return 1;
    static long born[LANES]; static u64 ring[RING][2][PB][NW]; static double lsum[LANES]; static long lcnt[LANES]; static int sampc[LANES], lowc[LANES]; double expo_st = 0; long deaths_st = 0, lives = 0, lives_st = 0; long CAP = getenv("CAP") ? atol(getenv("CAP")) : 0, capped = 0;
    double expo = 0, sp = 0, spp = 0, ns = 0; long deaths = 0, half16 = 0, half24 = 0, p416 = 0, npath = 0;
    for (int l = 0; l < LANES; l++) { soup_lane(l, n); born[l] = 0; }
    for (long g = 1; g <= gens; g++) {
      step_rule(ncell);
      if (WD) { u64 *d = nxt + (size_t)WD * A * NW; for (size_t x = 0; x < (size_t)2 * A * NW; x++) d[x] = rng(); }
      { u64 *s = cur; cur = nxt; nxt = s; }
      int slot = (int)(g % RING); facepop(0, ring[slot][0]); if (nf == 2) facepop(7 * A, ring[slot][1]);
      if ((g & 63) == 0) for (int l = 0; l < LANES; l++) if (g - born[l] > BURN) { int p = popof(ring[slot][0], l); if (nf == 2) { int p2 = popof(ring[slot][1], l); if (p2 < p) p = p2; }
          sp += p; spp += (double)p * p; ns += 1; lsum[l] += p; lcnt[l]++; sampc[l]++; if (4 * p < A) lowc[l]++; }
      for (int w = 0; w < NW; w++) { u64 z[2] = {~0ULL, 0};
        for (int k = 0; k < PB; k++) z[0] &= ~ring[slot][0][k][w];
        if (nf == 2) { z[1] = ~0ULL; for (int k = 0; k < PB; k++) z[1] &= ~ring[slot][1][k][w]; }
        u64 zz = z[0] | z[1];
        while (zz) { int k = __builtin_ctzll(zz); zz &= zz - 1; int l = 64 * w + k; long age = g - born[l];
          if (age > BURN) { expo += (double)nf * (age - BURN); int stuck = (sampc[l] >= 8 && 2 * lowc[l] > sampc[l]); lives++; if (stuck) { lives_st++; expo_st += (double)nf * (age - BURN); deaths_st += ((z[0] >> k) & 1) + ((z[1] >> k) & 1); }
            for (int fc = 0; fc < nf; fc++) if ((z[fc] >> k) & 1) { deaths++;
              if (age > BURN + 26) { int p[26]; for (int lag = 0; lag <= 25; lag++) p[lag] = popof(ring[((g - lag) % RING + RING) % RING][fc], l);
                int f16 = 0, f24 = 0; for (int lag = 1; lag <= 24; lag++) { int d = p[lag] - p[lag - 1]; if (d > f24) f24 = d; if (lag <= 15 && d > f16) f16 = d; }
                /* f16: falls among p[1..16] as in subpaths.py (pairs (lag+1 -> lag), lag = 1..15); f24 includes the last step to 0 */
                { int m = 0; for (int lag = 2; lag <= 16; lag++) { int d = p[lag] - p[lag - 1]; if (d > m) m = d; } f16 = m; }
                npath++; if (2 * f16 >= A) half16++; if (2 * f24 >= A) half24++; if (f16 >= 0.4 * A) p416++;
                if (pp) { fprintf(pp, "S 0 %d %ld |", l, g); for (int lag = 1; lag <= 24; lag++) fprintf(pp, " %d", p[lag]); fprintf(pp, "\n"); } } } }
          soup_lane(l, n); born[l] = g; sampc[l] = lowc[l] = 0; } }
      if (CAP && (g & 63) == 1) for (int l = 0; l < LANES; l++) if (g - born[l] >= CAP) { long age = g - born[l]; expo += (double)nf * (age - BURN); int stuck = (sampc[l] >= 8 && 2 * lowc[l] > sampc[l]); lives++; capped++;
          if (stuck) { lives_st++; expo_st += (double)nf * (age - BURN); } soup_lane(l, n); born[l] = g; sampc[l] = lowc[l] = 0; }
    }
    for (int l = 0; l < LANES; l++) if (gens - born[l] > BURN) { expo += (double)nf * (gens - born[l] - BURN); int stuck = (sampc[l] >= 8 && 2 * lowc[l] > sampc[l]); lives++; if (stuck) { lives_st++; expo_st += (double)nf * (gens - born[l] - BURN); } }
    printf("BRUTE A %d WD %d faces %d gens %ld exposure %.6e deaths %ld lntau_face %.4f +- %.4f | stationary face pop %.3f sd %.3f | paths %ld fall>=A/2 (last 16 gens, subpaths.py convention) %.4f +- %.4f ; >=0.4A %.4f ; fall>=A/2 (last 24 gens incl. last step) %.4f\n",
           A, WD, nf, gens, expo, deaths, deaths ? log(expo / deaths) : 0.0, deaths ? 1 / sqrt((double)deaths) : 0.0, sp / ns, sqrt(spp / ns - (sp / ns) * (sp / ns)),
           npath, npath ? (double)half16 / npath : 0.0, npath ? sqrt((double)half16 * (npath - half16) / npath) / npath : 0.0, npath ? (double)p416 / npath : 0.0, npath ? (double)half24 / npath : 0.0);
    if (getenv("LANEDBG")) for (int l = 0; l < LANES; l += 7) if (lcnt[l]) fprintf(stderr, "lane %d samples %ld meanpop %.2f born %ld\n", l, lcnt[l], lsum[l] / lcnt[l], born[l]);
    printf("STUCK (lives with more than half of their 64-generation samples below A/4; gump: the lower of the two faces) lives %ld of %ld, exposure share %.5f, deaths %ld; capped at age %ld: %ld; lntau_face without stuck lives %.4f +- %.4f\n", lives_st, lives, expo_st / expo, deaths_st, CAP, capped,
           log((expo - expo_st) / (deaths - deaths_st)), 1 / sqrt((double)(deaths - deaths_st)));
    if (pp) fclose(pp);
    return 0;
  }
  return 1;
}
