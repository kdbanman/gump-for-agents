/* fr.c: CPU face-torus runner (research/gpu-local/cpu). A second code, independent of the GPU kernel, for
 * ln tau_face on the slabs of research/shape/tslab.py (8 or m layers on the in-plane lattice (a,kk),(0,b)).
 *
 * Bit-sliced: 64 * W replicas (W = 4: 256 lanes, faster than 8 or 16 on this Ryzen) per thread, state[node][W] u64, AVX2 vectors of 4 words.
 * Each lane runs successive lives (renewal): a life starts from a fresh density-p soup (all nodes) and ends at its
 * first event, tested EVERY generation on the state after the step:
 *   kind 4  transverse firewall: some ring (transverse diagonal with >= 3 layers) has three cyclically consecutive
 *           dead layers (permanent by AUTOMATON.md T3). Also when a face died in the same generation (ties -> 4).
 *   kind 1  face death: layer t = 0 or t = m-1 has no live cell (and no firewall).
 *   kind 2  settled, period 1 or 2: state(g) == state(g-2) (after a reseed state(g-1) := soup, as the GPU does).
 *   kind 3  settled, longer cycle: state(g) == a snapshot of the same life. Three snapshots per lane, taken at
 *           global generations that are multiples of 2^10, 2^14, 2^18 (and set to the soup at each reseed), compared
 *           every generation: any period P <= 2^k (k = 10, 14, 18) is caught within 2^(k+1) + P generations of
 *           entering the cycle. Longer periods are not caught (the life stays open).
 * The lane is reseeded in the same generation; so every lane-generation is exposure of exactly one life:
 * exposure = lanes x generations. ln tau_face = ln(2 E / F).
 *
 * Usage:
 *   fr run VESSEL SEED0 THREADS HOURS CHUNK_MIN CSV CODE CMD
 *        thread t uses seed SEED0 + t; appends one csv row per thread per chunk (counts within the chunk).
 *   fr trace VESSEL INIT OUT GENS        no events, no reseeds: INIT = n*W u64 (node-major); OUT gets GENS states
 *   fr events VESSEL SEED GENS LIVES SOUPS   one thread: LIVES gets "lane birth age kind" per ended life
 *        (kind 0 = open at the end); SOUPS gets each soup (int64 gen, int32 lane, n bytes 0/1), gen 0 first.
 *   fr bench VESSEL SEED GENS            single-thread speed.
 * Vessel file (int32 LE, written by fr.py): magic 0x46524631, n, m, A, a, kk, b, nb[n*12] (-1 = outside),
 *   t[n] (d0 layer), nr, per ring: L, layer[n].
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
typedef u64 v4 __attribute__((vector_size(32), aligned(8)));   /* aligned(8): mingw-w64 does not realign the stack for 32-byte spills */

/* ---------------- vessel ---------------- */
static int n, m, A, la, lk, lb, nr, RL[3];
static int32_t *nb;              /* n*12, outside -> n (sentinel row, always 0) */
static int32_t *tl;              /* d0 layer per node */
static int32_t *slot;            /* n*4: accumulator slots (face slot, ring slots), unused -> dummy */
static int nslot, dummy, fs0, fs1, rs0[3];
static int32_t *sstart, *snode;   /* CSR: nodes of each real slot (faces, ring layers) */

static int rdi(FILE *f) { int32_t x; if (fread(&x, 4, 1, f) != 1) { fprintf(stderr, "short vessel file\n"); exit(1); } return x; }

static void load(const char *path) {
  FILE *f = fopen(path, "rb"); if (!f) { fprintf(stderr, "cannot open %s\n", path); exit(1); }
  if (rdi(f) != 0x46524631) { fprintf(stderr, "bad magic\n"); exit(1); }
  n = rdi(f); m = rdi(f); A = rdi(f); la = rdi(f); lk = rdi(f); lb = rdi(f);
  nb = malloc(4 * 12 * (size_t)n); tl = malloc(4 * (size_t)n);
  for (int i = 0; i < 12 * n; i++) { int x = rdi(f); nb[i] = x < 0 ? n : x; }
  for (int i = 0; i < n; i++) tl[i] = rdi(f);
  nr = rdi(f); if (nr > 3) exit(1);
  int32_t *rl[3];
  for (int r = 0; r < nr; r++) { RL[r] = rdi(f); rl[r] = malloc(4 * (size_t)n); for (int i = 0; i < n; i++) rl[r][i] = rdi(f); }
  fclose(f);
  /* slots: 0 = face t=0, 1 = face t=m-1, then rings, then dummy */
  fs0 = 0; fs1 = 1; nslot = 2;
  for (int r = 0; r < nr; r++) { rs0[r] = nslot; nslot += RL[r]; }
  dummy = nslot++;
  slot = malloc(4 * 4 * (size_t)n);
  int cnt0 = 0, cnt1 = 0;
  for (int i = 0; i < n; i++) {
    slot[4 * i] = tl[i] == 0 ? fs0 : tl[i] == m - 1 ? fs1 : dummy;
    cnt0 += tl[i] == 0; cnt1 += tl[i] == m - 1;
    for (int r = 0; r < 3; r++) slot[4 * i + 1 + r] = r < nr ? rs0[r] + rl[r][i] : dummy;
  }
  if (cnt0 != A || cnt1 != A) { fprintf(stderr, "face sizes %d %d != A %d\n", cnt0, cnt1, A); exit(1); }
  sstart = calloc(dummy + 1, 4); snode = malloc(4 * 4 * (size_t)n); int k = 0;
  for (int sl = 0; sl < dummy; sl++) { sstart[sl] = k;
    for (int i = 0; i < n; i++) for (int j = 0; j < 4; j++) if (slot[4 * i + j] == sl) snode[k++] = i; }
  sstart[dummy] = k;
}

/* ---------------- rng: xoshiro256** seeded by splitmix64 ---------------- */
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
static const u64 THR = (u64)(0.4 * 18446744073709551616.0);

/* ---------------- one replica block ---------------- */
typedef struct {
  u64 *cur, *prv, *sn[3];        /* (n+1)*W each; row n = 0 */
  u64 *acc;                      /* nslot*W */
  u64 dif[W], sd[3][W];
  long long *birth;              /* 64W */
  long long g;                   /* global generation of cur */
  rng_t rng;
  long long cnt[5];              /* lives ended by kind 1..4 (index = kind) */
  long long agesum;              /* sum of ages of ended lives */
  FILE *lives, *soups;
} blk_t;

static u64 *al(size_t words) { u64 *p = NULL; p = _aligned_malloc(8 * words, 64); if (!p) exit(1); memset(p, 0, 8 * words); return p; }

static void soup_lane(blk_t *B, int lane) {
  int w = lane >> 6; u64 bit = 1ULL << (lane & 63);
  unsigned char *row = B->soups ? malloc(n) : NULL;
  for (int i = 0; i < n; i++) {
    int on = rnext(&B->rng) < THR;
    size_t k = (size_t)i * W + w;
    if (on) { B->cur[k] |= bit; B->prv[k] |= bit; } else { B->cur[k] &= ~bit; B->prv[k] &= ~bit; }
    for (int s = 0; s < 3; s++) B->sn[s][k] = (B->sn[s][k] & ~bit) | (B->cur[k] & bit);
    if (row) row[i] = (unsigned char)on;
  }
  if (row) { int64_t gg = B->g; int32_t ln = lane; fwrite(&gg, 8, 1, B->soups); fwrite(&ln, 4, 1, B->soups); fwrite(row, 1, n, B->soups); free(row); }
  B->birth[lane] = B->g;
}

static void blk_init(blk_t *B, u64 seed, FILE *lives, FILE *soups) {
  memset(B, 0, sizeof *B);
  size_t N = (size_t)(n + 1) * W;
  B->cur = al(N); B->prv = al(N); for (int s = 0; s < 3; s++) B->sn[s] = al(N);
  B->acc = al((size_t)nslot * W);
  B->birth = calloc(64 * W, sizeof(long long));
  rseed(&B->rng, seed); B->lives = lives; B->soups = soups; B->g = 0;
  for (int l = 0; l < 64 * W; l++) soup_lane(B, l);
}

#define FA(s, c, x, y, z) do { v4 t_ = (x) ^ (y); s = t_ ^ (z); c = ((x) & (y)) | (t_ & (z)); } while (0)

/* one generation: cur -> new state (written into prv, then swapped); accumulators for the new state */
static inline void step(blk_t *B, int with_events) {
  const v4 *c = (const v4 *)B->cur; v4 *p = (v4 *)B->prv;
  const v4 *s0 = (const v4 *)B->sn[0], *s1 = (const v4 *)B->sn[1], *s2 = (const v4 *)B->sn[2];
  v4 *acc = (v4 *)B->acc;
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
      /* count = b0 + 2 b1 + 4 b2 + 8 b3; born on 4, 5; survives on 3, 4, 5 */
      v4 r = ~b3 & ((b2 & ~b1) | (me & ~b2 & b1 & b0));
      if (with_events) {
        dif[v] |= r ^ p[i * NV + v];
        d0[v] |= r ^ s0[i * NV + v]; d1[v] |= r ^ s1[i * NV + v]; d2[v] |= r ^ s2[i * NV + v];
      }
      p[i * NV + v] = r;
    }
  }
  if (with_events) for (int sl = 0; sl < dummy; sl++) {     /* layer ORs of the new state (in p) */
    v4 o[NV]; for (int v = 0; v < NV; v++) o[v] = (v4){0};
    for (int k = sstart[sl]; k < sstart[sl + 1]; k++) { const v4 *x = p + (size_t)snode[k] * NV; for (int v = 0; v < NV; v++) o[v] |= x[v]; }
    for (int v = 0; v < NV; v++) acc[sl * NV + v] = o[v];
  }
  { u64 *t = B->cur; B->cur = B->prv; B->prv = t; }
  B->g++;
  if (with_events) for (int v = 0; v < NV; v++) for (int k = 0; k < 4; k++) {
    B->dif[4 * v + k] = dif[v][k]; B->sd[0][4 * v + k] = d0[v][k]; B->sd[1][4 * v + k] = d1[v][k]; B->sd[2][4 * v + k] = d2[v][k];
  }
}

static void events(blk_t *B) {
  const u64 *acc = B->acc;
  for (int w = 0; w < W; w++) {
    u64 deadF = ~acc[fs0 * W + w] | ~acc[fs1 * W + w];
    u64 fw = 0;
    for (int r = 0; r < nr; r++) {
      int L = RL[r]; const u64 *a = acc + (size_t)rs0[r] * W + w;
      for (int l = 0; l < L; l++) fw |= ~a[(size_t)l * W] & ~a[(size_t)((l + 1) % L) * W] & ~a[(size_t)((l + 2) % L) * W];
    }
    u64 still = ~B->dif[w];
    u64 per = ~B->sd[0][w] | ~B->sd[1][w] | ~B->sd[2][w];
    u64 end = deadF | fw | still | per;
    while (end) {
      int k = __builtin_ctzll(end); u64 bit = 1ULL << k; end &= end - 1;
      int lane = 64 * w + k;
      int kind = (fw & bit) ? 4 : (deadF & bit) ? 1 : (still & bit) ? 2 : 3;
      long long age = B->g - B->birth[lane];
      B->cnt[kind]++; B->agesum += age;
      if (B->lives) fprintf(B->lives, "%d %lld %lld %d\n", lane, B->birth[lane], age, kind);
      soup_lane(B, lane);
    }
  }
  /* snapshots of the state at g (after reseeds, which already set the reseeded lanes) */
  for (int s = 0; s < 3; s++) {
    int sh = s == 0 ? 10 : s == 1 ? 14 : 18;
    if ((B->g & ((1LL << sh) - 1)) == 0) memcpy(B->sn[s], B->cur, 8 * (size_t)n * W);
  }
}

static double now(void) { struct timespec ts; clock_gettime(CLOCK_REALTIME, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }
static void utc(char *buf, size_t sz) { time_t t = time(NULL); struct tm tmv; gmtime_s(&tmv, &t); strftime(buf, sz, "%Y-%m-%dT%H:%M:%SZ", &tmv); }

/* ---------------- run ---------------- */
static const char *g_csv, *g_code, *g_cmd; static double g_hours, g_chunk; static int g_threads;
static pthread_mutex_t g_mu = PTHREAD_MUTEX_INITIALIZER;

static void csv_row(u64 seed, int chunk, const char *start, double wall, long long gens, const long long *dk,
                    long long dage, int lanes) {
  pthread_mutex_lock(&g_mu);
  FILE *f = fopen(g_csv, "a+");
  if (!f) { fprintf(stderr, "cannot open csv %s\n", g_csv); pthread_mutex_unlock(&g_mu); return; }
  fseek(f, 0, SEEK_END);
  if (ftell(f) == 0)
    fprintf(f, "torus,m,A,seed,chunk,start_utc,wall_s,gens,exposure,face,fw,settled,settled12,settled_cyc,open,threads,lanes,agesum_ended,code,cmd\n");
  fprintf(f, "\"%d,%d,%d\",%d,%d,%llu,%d,%s,%.1f,%lld,%lld,%lld,%lld,%lld,%lld,%lld,%d,%d,%d,%lld,%s,\"%s\"\n",
          la, lk, lb, m, A, (unsigned long long)seed, chunk, start, wall, gens, gens * lanes, dk[1], dk[4], dk[2] + dk[3], dk[2],
          dk[3], lanes, g_threads, lanes, dage, g_code, g_cmd);
  fclose(f);
  pthread_mutex_unlock(&g_mu);
}

static void *worker(void *arg) {
  u64 seed = (u64)(uintptr_t)arg;
  blk_t *B = malloc(sizeof(blk_t)); blk_init(B, seed, NULL, NULL);
  double t_end = now() + g_hours * 3600.0;
  int chunk = 0;
  for (;;) {
    char start[32]; utc(start, sizeof start);
    double t0 = now(); long long g0 = B->g, c0[5], a0 = B->agesum; memcpy(c0, B->cnt, sizeof c0);
    double t_stop = t0 + g_chunk * 60.0; if (t_stop > t_end) t_stop = t_end;
    int last = 0;
    for (;;) {
      for (int k = 0; k < 4096; k++) { step(B, 1); events(B); }
      double t = now();
      if (t >= t_stop) { last = t >= t_end - 1e-9 || t_stop >= t_end; break; }
    }
    long long dk[5]; for (int k = 0; k < 5; k++) dk[k] = B->cnt[k] - c0[k];
    csv_row(seed, chunk, start, now() - t0, B->g - g0, dk, B->agesum - a0, 64 * W);
    chunk++;
    if (last) break;
  }
  return NULL;
}

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: see fr.c\n"); return 1; }
  const char *mode = argv[1]; load(argv[2]);
#ifdef _WIN32
  SetPriorityClass(GetCurrentProcess(), BELOW_NORMAL_PRIORITY_CLASS);
#endif
  if (!strcmp(mode, "run")) {
    if (argc < 10) { fprintf(stderr, "usage: fr run VESSEL SEED0 THREADS HOURS CHUNK_MIN CSV CODE CMD\n"); return 1; }
    u64 seed0 = strtoull(argv[3], 0, 10); g_threads = atoi(argv[4]); g_hours = atof(argv[5]); g_chunk = atof(argv[6]);
    g_csv = argv[7]; g_code = argv[8]; g_cmd = argv[9];
    if (g_threads < 1 || g_threads > 12) { fprintf(stderr, "threads must be 1..12\n"); return 1; }
    pthread_t th[12];
    for (int t = 0; t < g_threads; t++) pthread_create(&th[t], NULL, worker, (void *)(uintptr_t)(seed0 + t));
    for (int t = 0; t < g_threads; t++) pthread_join(th[t], NULL);
    return 0;
  }
  if (!strcmp(mode, "trace")) {
    blk_t *B = malloc(sizeof(blk_t)); blk_init(B, 1, NULL, NULL);
    FILE *f = fopen(argv[3], "rb"); if (fread(B->cur, 8, (size_t)n * W, f) != (size_t)n * W) return 1; fclose(f);
    memcpy(B->prv, B->cur, 8 * (size_t)n * W);
    FILE *o = fopen(argv[4], "wb"); long long G = atoll(argv[5]);
    for (long long g = 0; g < G; g++) { step(B, 1); fwrite(B->cur, 8, (size_t)n * W, o); }
    fclose(o); return 0;
  }
  if (!strcmp(mode, "events")) {
    FILE *lv = fopen(argv[5], "w"), *sp = fopen(argv[6], "wb");
    blk_t *B = malloc(sizeof(blk_t)); blk_init(B, strtoull(argv[3], 0, 10), lv, sp);
    long long G = atoll(argv[4]);
    for (long long g = 0; g < G; g++) { step(B, 1); events(B); }
    for (int l = 0; l < 64 * W; l++) fprintf(lv, "%d %lld %lld 0\n", l, B->birth[l], B->g - B->birth[l]);
    fclose(lv); fclose(sp);
    printf("events: gens %lld face %lld fw %lld s12 %lld scyc %lld\n", B->g, B->cnt[1], B->cnt[4], B->cnt[2], B->cnt[3]);
    return 0;
  }
  if (!strcmp(mode, "bench")) {
    blk_t *B = malloc(sizeof(blk_t)); blk_init(B, strtoull(argv[3], 0, 10), NULL, NULL);
    long long G = atoll(argv[4]); double t0 = now();
    for (long long g = 0; g < G; g++) { step(B, 1); events(B); }
    double dt = now() - t0;
    printf("bench n=%d: %lld gens x %d lanes in %.3f s: %.4g replica-gens/s; face %lld fw %lld settled %lld\n",
           n, G, 64 * W, dt, G * 64.0 * W / dt, B->cnt[1], B->cnt[4], B->cnt[2] + B->cnt[3]);
    return 0;
  }
  fprintf(stderr, "unknown mode\n"); return 1;
}
