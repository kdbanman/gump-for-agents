/* hd.c: hull-face death recorder (research/dying2/hull). The stepper is research/gpu-local/cpu/fr.c's (bit-sliced,
 * W = 4: 256 lanes per thread, AVX2), copied; the vessel is the exact hull of the soup region |p|_1 <= R (8 faces),
 * the events and the protocol those of research/gpu/facelaw.py (soup p = 0.35 on the seedable nodes, everything
 * else dead; a life ends at the first generation some face layer is empty = kind 1, or when it settles: kind 2
 * period 1-2, kind 3 a cycle caught by snapshots at multiples of 2^10, 2^14, 2^18 as in fr.c). Events every generation.
 *
 * Recording, per thread (256 lanes):
 *   ring of the 8 face populations per lane, last HMAX generations; ring of the face-layer state (all face cells,
 *   the union of the 8 faces), last SMAX generations.
 *   type 1 dump at a face death at age > T0: the last HD populations and SD states of that lane.
 *   type 2 dump at the end of a recovered excursion whose minimum is in 1..KDUMP (at most CAPREC per minimum value
 *     per thread): the last HR populations and SR states.
 *   type 3 dump (null): every NULLEV generations, every lane at age > 2000: its 8 populations and face state now
 *     (at most NULLCAP per thread).
 *   excursions (research/dying/PREDICTIONS.md round 2 definition, per face, at ages > T0 with the previous generation
 *   also at age > T0): starts at the first P < U after a generation with P >= U; ends recovered at P >= U, dead at
 *   P = 0, censored when the life ends otherwise. Histograms of the minimum by end type; every excursion with
 *   minimum <= KDUMP is also written as a line (thread lane face start mingen end min type).
 *   lives: one line per ended life: lane birth age kind facemask (faces empty at the end); open lives at the end, kind 0.
 *   P histogram over face-generations at age > T0.
 *
 * Usage:
 *   hd run VESSEL SEED0 THREADS HOURS PREFIX U KDUMP CAPREC MAXDEATHS NULLEV NULLCAP HD SD HR SR
 *        thread t: seed SEED0 + t; files PREFIX_t{t}.{lives,exc,dump,hist}; runs HOURS; dumps the first MAXDEATHS deaths.
 *   hd trace VESSEL SEED GENS OUT      no events: OUT = initial state then GENS states (n*W u64 each, node-major),
 *        then for each generation the 8 x 256 face counts (uint8) computed by the production counter.
 * Dump record: int32 magic 0x48445031, type, thread, lane; int64 gen (of the last state), birth; int32 a, b, c, d
 *   (type 1: facemask, 0, 0, 0; type 2: face, min, start gen offset g - start, g - mingen); int32 nH, nS;
 *   nH x 8 uint8 populations (oldest first), nS x NFB bytes face-layer states (bit i of the fn list, oldest first).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <pthread.h>
#ifdef _WIN32
#include <windows.h>
#endif

typedef uint64_t u64;
#define W 4
#define NV (W / 4)
#define LANES (64 * W)
#define NF 8
#define NB 7
#define T0 200
#define HMAX 4096
#define SMAX 1024
typedef u64 v4 __attribute__((vector_size(32), aligned(8)));

static int n, nfn, NFB;
static int32_t *nb, *seedm, *fn, *fA, *fpos[NF];

static int rdi(FILE *f) { int32_t x; if (fread(&x, 4, 1, f) != 1) { fprintf(stderr, "short vessel file\n"); exit(1); } return x; }

static void load(const char *path) {
  FILE *f = fopen(path, "rb"); if (!f) { fprintf(stderr, "cannot open %s\n", path); exit(1); }
  if (rdi(f) != 0x48563031) { fprintf(stderr, "bad magic\n"); exit(1); }
  n = rdi(f); if (rdi(f) != NF) exit(1); nfn = rdi(f); NFB = (nfn + 7) / 8;
  nb = malloc(4 * 12 * (size_t)n); seedm = malloc(4 * (size_t)n); fn = malloc(4 * (size_t)nfn); fA = malloc(4 * NF);
  for (int i = 0; i < 12 * n; i++) { int x = rdi(f); nb[i] = x < 0 ? n : x; }
  for (int i = 0; i < n; i++) seedm[i] = rdi(f);
  for (int i = 0; i < nfn; i++) fn[i] = rdi(f);
  for (int k = 0; k < NF; k++) { fA[k] = rdi(f); fpos[k] = malloc(4 * (size_t)fA[k]); for (int i = 0; i < fA[k]; i++) fpos[k][i] = rdi(f); }
  fclose(f);
}

typedef struct { u64 s[4]; } rng_t;
static inline u64 rotl(u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static inline u64 rnext(rng_t *g) {
  u64 *s = g->s; const u64 r = rotl(s[1] * 5, 7) * 9, t = s[1] << 17;
  s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2]; s[0] ^= s[3]; s[2] ^= t; s[3] = rotl(s[3], 45); return r;
}
static void rseed(rng_t *g, u64 seed) {
  u64 z = seed ^ 0x6a09e667f3bcc909ULL;
  for (int i = 0; i < 4; i++) { z += 0x9e3779b97f4a7c15ULL; u64 x = z; x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
    x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL; g->s[i] = x ^ (x >> 31); }
  for (int i = 0; i < 16; i++) rnext(g);
}
static const u64 THR = (u64)(0.35 * 18446744073709551616.0);

/* run parameters */
static int U = 32, KDUMP = 12, CAPREC = 500, NULLEV = 997, NULLCAP = 50000, HD = 4096, SD = 1024, HR = 1024, SR = 256;
static long long MAXDEATHS = 1000000;

typedef struct {
  u64 *cur, *prv, *sn[3];
  u64 dif[W], sd[3][W];
  long long birth[LANES];
  long long g;
  rng_t rng;
  uint8_t cnt[NF][LANES];
  uint8_t *rcnt;                 /* HMAX x NF x LANES */
  u64 *rst;                      /* SMAX x nfn x W */
  /* excursions */
  uint8_t inx[NF][LANES], above[NF][LANES], xmin[NF][LANES];
  long long xstart[NF][LANES], xming[NF][LANES];
  long long hrec[128], hdead[128], hcens[128], hP[128], Ef;
  long long nrec[128];
  long long cntk[4], deaths_dumped, nnull;
  int tid;
  FILE *lives, *exc, *dump;
} blk_t;

static u64 *al(size_t words) { u64 *p = _aligned_malloc(8 * words, 64); if (!p) exit(1); memset(p, 0, 8 * words); return p; }

static void soup_lane(blk_t *B, int lane) {
  int w = lane >> 6; u64 bit = 1ULL << (lane & 63);
  for (int i = 0; i < n; i++) {
    int on = seedm[i] && rnext(&B->rng) < THR;
    size_t k = (size_t)i * W + w;
    if (on) { B->cur[k] |= bit; B->prv[k] |= bit; } else { B->cur[k] &= ~bit; B->prv[k] &= ~bit; }
    for (int s = 0; s < 3; s++) B->sn[s][k] = (B->sn[s][k] & ~bit) | (B->cur[k] & bit);
  }
  B->birth[lane] = B->g;
  for (int f = 0; f < NF; f++) { B->inx[f][lane] = 0; B->above[f][lane] = 0; }
}

static void blk_init(blk_t *B, u64 seed, int tid) {
  memset(B, 0, sizeof *B);
  size_t N = (size_t)(n + 1) * W;
  B->cur = al(N); B->prv = al(N); for (int s = 0; s < 3; s++) B->sn[s] = al(N);
  B->rcnt = calloc((size_t)HMAX * NF * LANES, 1);
  B->rst = al((size_t)SMAX * nfn * W);
  B->tid = tid;
  rseed(&B->rng, seed); B->g = 0;
  for (int l = 0; l < LANES; l++) soup_lane(B, l);
}

#define FA(s, c, x, y, z) do { v4 t_ = (x) ^ (y); s = t_ ^ (z); c = ((x) & (y)) | (t_ & (z)); } while (0)

/* one generation (fr.c's step): cur -> new state; dif / snapshot differences; then face counts and the rings */
static inline void step(blk_t *B) {
  const v4 *c = (const v4 *)B->cur; v4 *p = (v4 *)B->prv;
  const v4 *s0 = (const v4 *)B->sn[0], *s1 = (const v4 *)B->sn[1], *s2 = (const v4 *)B->sn[2];
  v4 dif[NV], d0[NV], d1[NV], d2[NV];
  for (int v = 0; v < NV; v++) { dif[v] = (v4){0}; d0[v] = (v4){0}; d1[v] = (v4){0}; d2[v] = (v4){0}; }
  for (int i = 0; i < n; i++) {
    const int32_t *q = nb + 12 * (size_t)i;
    for (int v = 0; v < NV; v++) {
      v4 x0 = c[q[0] * NV + v], x1 = c[q[1] * NV + v], x2 = c[q[2] * NV + v], x3 = c[q[3] * NV + v],
         x4 = c[q[4] * NV + v], x5 = c[q[5] * NV + v], x6 = c[q[6] * NV + v], x7 = c[q[7] * NV + v],
         x8 = c[q[8] * NV + v], x9 = c[q[9] * NV + v], x10 = c[q[10] * NV + v], x11 = c[q[11] * NV + v];
      v4 me = c[i * NV + v];
      v4 a1, c1, a2, c2, a3, c3, a4, c4, S, C, b0, H, t1, e1, t2, e2, b1, e, b2, b3;
      FA(a1, c1, x0, x1, x2); FA(a2, c2, x3, x4, x5); FA(a3, c3, x6, x7, x8); FA(a4, c4, x9, x10, x11);
      FA(S, C, a1, a2, a3); b0 = S ^ a4; H = S & a4;
      FA(t1, e1, c1, c2, c3); FA(t2, e2, c4, C, H); b1 = t1 ^ t2; e = t1 & t2;
      FA(b2, b3, e1, e2, e);
      v4 r = ~b3 & ((b2 & ~b1) | (me & ~b2 & b1 & b0));
      dif[v] |= r ^ p[i * NV + v];
      d0[v] |= r ^ s0[i * NV + v]; d1[v] |= r ^ s1[i * NV + v]; d2[v] |= r ^ s2[i * NV + v];
      p[i * NV + v] = r;
    }
  }
  { u64 *t = B->cur; B->cur = B->prv; B->prv = t; }
  B->g++;
  for (int v = 0; v < NV; v++) for (int k = 0; k < 4; k++) {
    B->dif[4 * v + k] = dif[v][k]; B->sd[0][4 * v + k] = d0[v][k]; B->sd[1][4 * v + k] = d1[v][k]; B->sd[2][4 * v + k] = d2[v][k];
  }
  /* face-layer state into the ring */
  u64 *rs = B->rst + (size_t)(B->g & (SMAX - 1)) * nfn * W;
  for (int i = 0; i < nfn; i++) memcpy(rs + (size_t)i * W, B->cur + (size_t)fn[i] * W, 8 * W);
  /* face counts: bit-sliced ripple counters over each face's cells */
  for (int f = 0; f < NF; f++) {
    u64 pl[NB][W]; memset(pl, 0, sizeof pl);
    for (int j = 0; j < fA[f]; j++) {
      const u64 *x = rs + (size_t)fpos[f][j] * W;
      for (int w = 0; w < W; w++) { u64 cy = x[w]; for (int b = 0; b < NB && cy; b++) { u64 t = pl[b][w] & cy; pl[b][w] ^= cy; cy = t; } }
    }
    for (int w = 0; w < W; w++) for (int k = 0; k < 64; k++) {
      int v = 0; for (int b = 0; b < NB; b++) v |= (int)((pl[b][w] >> k) & 1) << b;
      B->cnt[f][64 * w + k] = (uint8_t)v;
    }
  }
  memcpy(B->rcnt + (size_t)(B->g & (HMAX - 1)) * NF * LANES, B->cnt, NF * LANES);
}

static void dump(blk_t *B, int type, int lane, int a, int b, int c, int d, int nH, int nS) {
  int32_t h[4] = {0x48445031, type, B->tid, lane}; fwrite(h, 4, 4, B->dump);
  int64_t gg[2] = {B->g, B->birth[lane]}; fwrite(gg, 8, 2, B->dump);
  int32_t x[6] = {a, b, c, d, nH, nS}; fwrite(x, 4, 6, B->dump);
  uint8_t pop[NF];
  for (long long t = B->g - nH + 1; t <= B->g; t++) {
    const uint8_t *r = B->rcnt + (size_t)(t & (HMAX - 1)) * NF * LANES;
    for (int f = 0; f < NF; f++) pop[f] = r[f * LANES + lane];
    fwrite(pop, 1, NF, B->dump);
  }
  int w = lane >> 6, k = lane & 63;
  uint8_t *row = calloc(NFB, 1);
  for (long long t = B->g - nS + 1; t <= B->g; t++) {
    const u64 *rs = B->rst + (size_t)(t & (SMAX - 1)) * nfn * W;
    memset(row, 0, NFB);
    for (int i = 0; i < nfn; i++) if ((rs[(size_t)i * W + w] >> k) & 1) row[i >> 3] |= (uint8_t)(1 << (i & 7));
    fwrite(row, 1, NFB, B->dump);
  }
  free(row);
}

static void xline(blk_t *B, int lane, int f, int type) {
  if (B->exc && B->xmin[f][lane] <= KDUMP)
    fprintf(B->exc, "%d %d %d %lld %lld %lld %d %d\n", B->tid, lane, f, B->xstart[f][lane], B->xming[f][lane], B->g,
            B->xmin[f][lane], type);
}

static void events(blk_t *B) {
  for (int w = 0; w < W; w++) {
    u64 still = ~B->dif[w];
    u64 per = ~B->sd[0][w] | ~B->sd[1][w] | ~B->sd[2][w];
    for (int k = 0; k < 64; k++) {
      int lane = 64 * w + k; u64 bit = 1ULL << k;
      long long age = B->g - B->birth[lane];
      int fm = 0;
      for (int f = 0; f < NF; f++) if (B->cnt[f][lane] == 0) fm |= 1 << f;
      int kind = fm ? 1 : (still & bit) ? 2 : (per & bit) ? 3 : 0;
      if (age > T0) {                        /* excursions: this generation and the previous at age > T0 */
        for (int f = 0; f < NF; f++) {
          int P = B->cnt[f][lane];
          B->hP[P]++; B->Ef++;
          if (B->inx[f][lane]) {
            if (P < B->xmin[f][lane]) { B->xmin[f][lane] = (uint8_t)P; B->xming[f][lane] = B->g; }
            if (P == 0) { B->hdead[0]++; xline(B, lane, f, 1); B->inx[f][lane] = 0; }
            else if (P >= U) {
              int m = B->xmin[f][lane];
              B->hrec[m]++; xline(B, lane, f, 2); B->inx[f][lane] = 0;
              if (B->dump && m >= 1 && m <= KDUMP && B->nrec[m] < CAPREC) {
                B->nrec[m]++;
                dump(B, 2, lane, f, m, (int)(B->g - B->xstart[f][lane]), (int)(B->g - B->xming[f][lane]), HR, SR);
              }
            }
          } else if (B->above[f][lane] && P < U) {
            B->inx[f][lane] = 1; B->xmin[f][lane] = (uint8_t)P; B->xstart[f][lane] = B->g; B->xming[f][lane] = B->g;
            if (P == 0) { B->hdead[0]++; xline(B, lane, f, 1); B->inx[f][lane] = 0; }
          }
          B->above[f][lane] = P >= U;
        }
      }
      if (kind) {
        for (int f = 0; f < NF; f++) if (B->inx[f][lane]) { B->hcens[B->xmin[f][lane]]++; xline(B, lane, f, 3); B->inx[f][lane] = 0; }
        B->cntk[kind]++;
        if (B->lives) fprintf(B->lives, "%d %lld %lld %d %d\n", lane, B->birth[lane], age, kind, fm);
        if (kind == 1 && age > T0 && B->dump && B->deaths_dumped < MAXDEATHS) { dump(B, 1, lane, fm, 0, 0, 0, HD, SD); B->deaths_dumped++; }
        soup_lane(B, lane);
      }
    }
  }
  if (NULLEV > 0 && B->g % NULLEV == 0 && B->nnull < NULLCAP && B->dump)
    for (int lane = 0; lane < LANES; lane++)
      if (B->g - B->birth[lane] > 2000 && B->nnull < NULLCAP) { dump(B, 3, lane, 0, 0, 0, 0, 1, 1); B->nnull++; }
  for (int s = 0; s < 3; s++) {
    int sh = s == 0 ? 10 : s == 1 ? 14 : 18;
    if ((B->g & ((1LL << sh) - 1)) == 0) memcpy(B->sn[s], B->cur, 8 * (size_t)n * W);
  }
}

static double now(void) { struct timespec ts; clock_gettime(CLOCK_REALTIME, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }

static const char *g_prefix; static double g_hours; static u64 g_seed0;

static void write_hist(blk_t *B, double wall) {
  char p[1024]; snprintf(p, sizeof p, "%s_t%d.hist", g_prefix, B->tid);
  FILE *f = fopen(p, "w"); if (!f) return;
  fprintf(f, "seed %llu gens %lld lanes %d wall_s %.1f U %d KDUMP %d Ef %lld kind1 %lld kind2 %lld kind3 %lld dumped1 %lld null %lld\n",
          (unsigned long long)(g_seed0 + B->tid), B->g, LANES, wall, U, KDUMP, B->Ef, B->cntk[1], B->cntk[2], B->cntk[3], B->deaths_dumped, B->nnull);
  fprintf(f, "P hP rec dead cens nrecdumped\n");
  for (int i = 0; i < 128; i++) fprintf(f, "%d %lld %lld %lld %lld %lld\n", i, B->hP[i], B->hrec[i], B->hdead[i], B->hcens[i], B->nrec[i]);
  fclose(f);
}

static void *worker(void *arg) {
  int tid = (int)(uintptr_t)arg;
  blk_t *B = malloc(sizeof(blk_t)); blk_init(B, g_seed0 + tid, tid);
  char p[1024];
  snprintf(p, sizeof p, "%s_t%d.lives", g_prefix, tid); B->lives = fopen(p, "w");
  snprintf(p, sizeof p, "%s_t%d.exc", g_prefix, tid); B->exc = fopen(p, "w");
  snprintf(p, sizeof p, "%s_t%d.dump", g_prefix, tid); B->dump = fopen(p, "wb");
  if (!B->lives || !B->exc || !B->dump) { fprintf(stderr, "cannot open outputs\n"); exit(1); }
  double t0 = now(), t_end = t0 + g_hours * 3600.0, last = t0;
  for (;;) {
    for (int k = 0; k < 4096; k++) { step(B); events(B); }
    double t = now();
    if (t - last > 300) { write_hist(B, t - t0); fflush(B->lives); fflush(B->exc); fflush(B->dump); last = t; }
    if (t >= t_end) break;
  }
  for (int l = 0; l < LANES; l++) fprintf(B->lives, "%d %lld %lld 0 0\n", l, B->birth[l], B->g - B->birth[l]);
  write_hist(B, now() - t0);
  fclose(B->lives); fclose(B->exc); fclose(B->dump);
  return NULL;
}

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: see hd.c\n"); return 1; }
  const char *mode = argv[1]; load(argv[2]);
#ifdef _WIN32
  SetPriorityClass(GetCurrentProcess(), BELOW_NORMAL_PRIORITY_CLASS);
#endif
  if (!strcmp(mode, "run")) {
    if (argc < 17) { fprintf(stderr, "usage: hd run VESSEL SEED0 THREADS HOURS PREFIX U KDUMP CAPREC MAXDEATHS NULLEV NULLCAP HD SD HR SR\n"); return 1; }
    g_seed0 = strtoull(argv[3], 0, 10); int th = atoi(argv[4]); g_hours = atof(argv[5]); g_prefix = argv[6];
    U = atoi(argv[7]); KDUMP = atoi(argv[8]); CAPREC = atoi(argv[9]); MAXDEATHS = atoll(argv[10]); NULLEV = atoi(argv[11]);
    NULLCAP = atoi(argv[12]); HD = atoi(argv[13]); SD = atoi(argv[14]); HR = atoi(argv[15]); SR = atoi(argv[16]);
    if (th < 1 || th > 8 || HD > HMAX || HR > HMAX || SD > SMAX || SR > SMAX || KDUMP > 126) { fprintf(stderr, "bad arguments\n"); return 1; }
    pthread_t t[8];
    for (int i = 0; i < th; i++) pthread_create(&t[i], NULL, worker, (void *)(uintptr_t)i);
    for (int i = 0; i < th; i++) pthread_join(t[i], NULL);
    return 0;
  }
  if (!strcmp(mode, "trace")) {
    blk_t *B = malloc(sizeof(blk_t)); blk_init(B, strtoull(argv[3], 0, 10), 0);
    long long G = atoll(argv[5]);
    FILE *o = fopen(argv[4], "wb");
    fwrite(B->cur, 8, (size_t)n * W, o);
    uint8_t *cs = malloc((size_t)G * NF * LANES);
    for (long long g = 0; g < G; g++) { step(B); fwrite(B->cur, 8, (size_t)n * W, o); memcpy(cs + (size_t)g * NF * LANES, B->cnt, NF * LANES); }
    fwrite(cs, 1, (size_t)G * NF * LANES, o);
    fclose(o); return 0;
  }
  if (!strcmp(mode, "bench")) {
    blk_t *B = malloc(sizeof(blk_t)); blk_init(B, 1, 0);
    long long G = atoll(argv[3]); double t0 = now();
    for (long long g = 0; g < G; g++) { step(B); events(B); }
    double dt = now() - t0;
    printf("bench n=%d nfn=%d: %lld gens x %d lanes in %.3f s: %.4g replica-gens/s; kinds %lld %lld %lld\n",
           n, nfn, G, LANES, dt, G * (double)LANES / dt, B->cntk[1], B->cntk[2], B->cntk[3]);
    return 0;
  }
  fprintf(stderr, "unknown mode\n"); return 1;
}
