/* dy.c: how wrapped faces die (research/dying2). A copy of research/gpu-local/cpu/fr.c (the stepper, the events and
 * the reseeding are fr.c's, unchanged) that also, per lane and per face layer:
 *   - counts the face population P every generation (bit-sliced counter, then per lane);
 *   - keeps a ring buffer of the last H generations of layers 0, 1, m-2, m-1 (both faces and the layer beneath each);
 *   - follows excursions (research/dying round 2 definition): only generations at life age > T0 = 512 count; an
 *     excursion starts at the first generation with P < PBAR after a generation (also at age > T0) with P >= PBAR;
 *     it ends recovered at the first later generation with P >= PBAR, dead when the face is empty and the life ends
 *     as a face death (kind 1), censored when the life ends otherwise (other face's death, firewall, settled);
 *     tallied by the excursion's minimum P and end type;
 *   - dumps, as binary records: every face death at age > T0 (the last min(H, age - T0) generations of the dying
 *     face and the layer beneath it, ending at the first empty generation), every recovered excursion with minimum
 *     <= KDUMP (the last min(R, age - T0) generations ending at the recovery generation), and null samples (the state
 *     of one face of every lane at age > T0, at generations that are multiples of 2^NULLSH).
 * Record: int64 hdr[12] = type (1 death, 2 recovered, 3 null), seed, lane, face (0: layer 0, 1: layer m-1), birth,
 *   g (last generation stored), age, a1, a2, a3, a4, L; then L x (face layer bits, beneath layer bits), oldest first;
 *   each layer ceil(A/8) bytes, cell i of the layer (node base + i) at byte i>>3, bit i&7.
 *   death: a1 = excursion start generation (-1 if none), a2 = the other face's P, a3 = 1 if both faces died.
 *   recovered: a1 = start generation, a2 = first generation at the minimum, a3 = minimum.   null: a1 = P.
 * Stats (cumulative, one line per chunk per thread): see stats_line().
 *
 * Usage:
 *   dy run VESSEL SEED0 THREADS HOURS CHUNK_MIN OUTDIR PBAR KDUMP NULLSH H R MAXDEATH MAXREC
 *   dy events VESSEL SEED GENS OUTDIR PBAR KDUMP NULLSH H R NL   one thread; also lives.txt / soups.bin as fr.c;
 *        all tallies and dumps only for lanes < NL (for the numpy check)
 *   dy trace VESSEL INIT OUT GENS        as fr.c
 *   dy bench VESSEL SEED GENS
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
#define LN (64 * W)
#define T0 512
#define MAXA 127
typedef u64 v4 __attribute__((vector_size(32), aligned(8)));

/* ---------------- vessel ---------------- */
static int n, m, A, la, lk, lb, nr, RL[3];
static int32_t *nb, *tl, *slot;
static int nslot, dummy, fs0, fs1, rs0[3];
static int32_t *sstart, *snode;

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
  /* dy: layers must be contiguous blocks of A nodes in layer order (tslab's node order) */
  if (n != m * A || A > MAXA) { fprintf(stderr, "n %d != m*A or A > %d\n", n, MAXA); exit(1); }
  for (int i = 0; i < n; i++) if (tl[i] != i / A) { fprintf(stderr, "layers not contiguous\n"); exit(1); }
  sstart = calloc(dummy + 1, 4); snode = malloc(4 * 4 * (size_t)n); int k = 0;
  for (int sl = 0; sl < dummy; sl++) { sstart[sl] = k;
    for (int i = 0; i < n; i++) for (int j = 0; j < 4; j++) if (slot[4 * i + j] == sl) snode[k++] = i; }
  sstart[dummy] = k;
}

/* ---------------- rng ---------------- */
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

/* ---------------- parameters of the recording ---------------- */
static double g_pbar = 1e9; static int g_kdump = -1, g_nullsh = 62, g_H = 4096, g_R = 1024, g_nl = LN;
static long long g_maxdeath = 1LL << 60, g_maxrec = 1LL << 60;

/* ---------------- one replica block ---------------- */
typedef struct {
  u64 *cur, *prv, *sn[3];
  u64 *acc;
  u64 dif[W], sd[3][W];
  long long *birth;
  long long g;
  rng_t rng;
  long long cnt[5];
  long long agesum;
  FILE *lives, *soups;
  /* dy */
  u64 seed;
  u64 *ring;                       /* H slots x 4A x W */
  unsigned char P[2][LN];
  int prevok[2][LN], prevab[2][LN], inexc[2][LN], minp[2][LN];
  long long gstart[2][LN], gmin[2][LN];
  long long expo, sumP, sumP2, hist[MAXA + 1], exc[MAXA + 1][3], deaths_ok, dead_noexc, ndd, nrd, nnull, rec_skipped;
  FILE *dump;
} blk_t;

static u64 *al(size_t words) { u64 *p = _aligned_malloc(8 * words, 64); if (!p) { fprintf(stderr, "out of memory\n"); exit(1); } memset(p, 0, 8 * words); return p; }

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
  for (int f = 0; f < 2; f++) { B->prevok[f][lane] = 0; B->inexc[f][lane] = 0; }
}

static void blk_init(blk_t *B, u64 seed, FILE *lives, FILE *soups, FILE *dump, int with_ring) {
  memset(B, 0, sizeof *B);
  size_t N = (size_t)(n + 1) * W;
  B->cur = al(N); B->prv = al(N); for (int s = 0; s < 3; s++) B->sn[s] = al(N);
  B->acc = al((size_t)nslot * W);
  B->birth = calloc(LN, sizeof(long long));
  B->seed = seed; B->dump = dump;
  if (with_ring) B->ring = al((size_t)g_H * 4 * A * W);
  rseed(&B->rng, seed); B->lives = lives; B->soups = soups; B->g = 0;
  for (int l = 0; l < LN; l++) soup_lane(B, l);
}

#define FA(s, c, x, y, z) do { v4 t_ = (x) ^ (y); s = t_ ^ (z); c = ((x) & (y)) | (t_ & (z)); } while (0)

/* fr.c's step, unchanged */
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
      v4 r = ~b3 & ((b2 & ~b1) | (me & ~b2 & b1 & b0));
      if (with_events) {
        dif[v] |= r ^ p[i * NV + v];
        d0[v] |= r ^ s0[i * NV + v]; d1[v] |= r ^ s1[i * NV + v]; d2[v] |= r ^ s2[i * NV + v];
      }
      p[i * NV + v] = r;
    }
  }
  if (with_events) for (int sl = 0; sl < dummy; sl++) {
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

/* ---------------- dy: counting, ring, excursions, dumps ---------------- */
static inline u64 *ring_slot(blk_t *B, long long g) { return B->ring + (size_t)(g % g_H) * 4 * A * W; }

/* layer offsets inside a ring slot: [layer 0][layer 1][layer m-2][layer m-1] */
static void write_rec(blk_t *B, long long type, int lane, int face, long long gend, long long L,
                      long long a1, long long a2, long long a3, long long a4) {
  int64_t h[12] = {type, (int64_t)B->seed, lane, face, B->birth[lane], gend, gend - B->birth[lane], a1, a2, a3, a4, L};
  fwrite(h, 8, 12, B->dump);
  int nb8 = (A + 7) / 8, w = lane >> 6, k = lane & 63;
  int offF = face == 0 ? 0 : 3 * A, offB = face == 0 ? A : 2 * A;
  unsigned char buf[2 * ((MAXA + 8) / 8)];
  for (long long gg = gend - L + 1; gg <= gend; gg++) {
    const u64 *s = ring_slot(B, gg);
    memset(buf, 0, 2 * nb8);
    for (int i = 0; i < A; i++) {
      if ((s[(size_t)(offF + i) * W + w] >> k) & 1) buf[i >> 3] |= (unsigned char)(1 << (i & 7));
      if ((s[(size_t)(offB + i) * W + w] >> k) & 1) buf[nb8 + (i >> 3)] |= (unsigned char)(1 << (i & 7));
    }
    fwrite(buf, 1, 2 * nb8, B->dump);
  }
}

static void count_ring_tally(blk_t *B) {
  const u64 *c = B->cur;
  /* ring */
  u64 *s = ring_slot(B, B->g);
  memcpy(s, c, 8 * (size_t)2 * A * W);
  memcpy(s + (size_t)2 * A * W, c + (size_t)(m - 2) * A * W, 8 * (size_t)2 * A * W);
  /* per-lane counts of the two faces */
  for (int f = 0; f < 2; f++) {
    const v4 *x = (const v4 *)(c + (size_t)(f ? (m - 1) * A : 0) * W);
    v4 pl[7]; for (int k = 0; k < 7; k++) pl[k] = (v4){0};
    for (int i = 0; i < A; i++) { v4 cc = x[i]; for (int k = 0; k < 7; k++) { v4 t = pl[k] & cc; pl[k] ^= cc; cc = t; } }
    for (int w = 0; w < W; w++) {
      u64 q[7]; for (int k = 0; k < 7; k++) q[k] = pl[k][w];
      for (int b = 0; b < 64; b++) {
        int v = 0; for (int k = 0; k < 7; k++) v |= (int)((q[k] >> b) & 1) << k;
        B->P[f][64 * w + b] = (unsigned char)v;
      }
    }
  }
  /* excursions and stationary tallies */
  const long long g = B->g;
  int nulls = (g & ((1LL << g_nullsh) - 1)) == 0, nf = (int)((g >> g_nullsh) & 1);
  for (int lane = 0; lane < g_nl; lane++) {
    long long age = g - B->birth[lane];
    int ok = age > T0;
    for (int f = 0; f < 2; f++) {
      int P = B->P[f][lane], ab = P >= g_pbar;
      if (B->inexc[f][lane]) {
        if (P < B->minp[f][lane]) { B->minp[f][lane] = P; B->gmin[f][lane] = g; }
        if (ab) {
          int mp = B->minp[f][lane];
          B->exc[mp][0]++;
          if (mp <= g_kdump) {
            if (B->nrd < g_maxrec) {
              long long L = age - T0; if (L > g_R) L = g_R;
              write_rec(B, 2, lane, f, g, L, B->gstart[f][lane], B->gmin[f][lane], mp, 0); B->nrd++;
            } else B->rec_skipped++;
          }
          B->inexc[f][lane] = 0;
        }
      } else if (ok && B->prevok[f][lane] && B->prevab[f][lane] && !ab) {
        B->inexc[f][lane] = 1; B->minp[f][lane] = P; B->gmin[f][lane] = g; B->gstart[f][lane] = g;
      }
      B->prevab[f][lane] = ab; B->prevok[f][lane] = ok;
      if (ok) { B->expo++; B->sumP += P; B->sumP2 += (long long)P * P; B->hist[P]++; }
    }
    if (nulls && ok && B->dump) { write_rec(B, 3, lane, nf, g, 1, B->P[nf][lane], 0, 0, 0); B->nnull++; }
  }
}

static void events(blk_t *B) {
  const u64 *acc = B->acc;
  for (int w = 0; w < W; w++) {
    u64 dead0 = ~acc[fs0 * W + w], dead1 = ~acc[fs1 * W + w];
    u64 deadF = dead0 | dead1;
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
      if (lane < g_nl) {
        int dd[2] = {(dead0 & bit) != 0, (dead1 & bit) != 0};
        for (int f = 0; f < 2; f++) {
          if (kind == 1 && dd[f]) {
            if (age > T0) {
              B->deaths_ok++;
              if (B->inexc[f][lane]) B->exc[B->minp[f][lane]][1]++; else B->dead_noexc++;
              if (B->ring && B->dump && B->ndd < g_maxdeath) {
                long long L = age - T0; if (L > g_H) L = g_H;
                write_rec(B, 1, lane, f, B->g, L, B->inexc[f][lane] ? B->gstart[f][lane] : -1, B->P[1 - f][lane], dd[0] && dd[1], 0);
                B->ndd++;
              }
            }
          } else if (B->inexc[f][lane]) B->exc[B->minp[f][lane]][2]++;
        }
      }
      soup_lane(B, lane);
    }
  }
  for (int s = 0; s < 3; s++) {
    int sh = s == 0 ? 10 : s == 1 ? 14 : 18;
    if ((B->g & ((1LL << sh) - 1)) == 0) memcpy(B->sn[s], B->cur, 8 * (size_t)n * W);
  }
}

static double now(void) { struct timespec ts; clock_gettime(CLOCK_REALTIME, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }
static void utc(char *buf, size_t sz) { time_t t = time(NULL); struct tm tmv; gmtime_s(&tmv, &t); strftime(buf, sz, "%Y-%m-%dT%H:%M:%SZ", &tmv); }

/* one line, cumulative over the thread's run:
 * seed chunk utc wall gens lanegens face fw s12 scyc deaths_ok dead_noexc expo sumP sumP2 ndd nrd nnull rec_skipped open
 *   H hist[0..A]  E (rec dead cens) for min = 0..A */
static void stats_line(FILE *f, blk_t *B, int chunk, double wall) {
  char t[32]; utc(t, sizeof t);
  int open = 0; for (int l = 0; l < g_nl; l++) open += B->inexc[0][l] + B->inexc[1][l];
  fprintf(f, "%llu %d %s %.1f %lld %lld %lld %lld %lld %lld %lld %lld %lld %lld %lld %lld %lld %lld %lld %d H",
          (unsigned long long)B->seed, chunk, t, wall, B->g, B->g * (long long)LN, B->cnt[1], B->cnt[4], B->cnt[2], B->cnt[3],
          B->deaths_ok, B->dead_noexc, B->expo, B->sumP, B->sumP2, B->ndd, B->nrd, B->nnull, B->rec_skipped, open);
  for (int p = 0; p <= A; p++) fprintf(f, " %lld", B->hist[p]);
  fprintf(f, " E");
  for (int p = 0; p <= A; p++) fprintf(f, " %lld %lld %lld", B->exc[p][0], B->exc[p][1], B->exc[p][2]);
  fprintf(f, "\n");
}

/* ---------------- run ---------------- */
static const char *g_out; static double g_hours, g_chunk; static int g_threads;

static void *worker(void *arg) {
  u64 seed = (u64)(uintptr_t)arg;
  char path[1024]; snprintf(path, sizeof path, "%s/dump_%llu.bin", g_out, (unsigned long long)seed);
  FILE *dump = fopen(path, "ab"); if (!dump) { fprintf(stderr, "cannot open %s\n", path); return NULL; }
  setvbuf(dump, NULL, _IOFBF, 1 << 22);
  char spath[1024]; snprintf(spath, sizeof spath, "%s/stats_%llu.txt", g_out, (unsigned long long)seed);
  blk_t *B = malloc(sizeof(blk_t)); blk_init(B, seed, NULL, NULL, dump, 1);
  double tstart = now(), t_end = tstart + g_hours * 3600.0;
  int chunk = 0;
  for (;;) {
    double t_stop = now() + g_chunk * 60.0; if (t_stop > t_end) t_stop = t_end;
    int last = 0;
    for (;;) {
      for (int k = 0; k < 4096; k++) { step(B, 1); count_ring_tally(B); events(B); }
      double t = now();
      if (B->ndd >= g_maxdeath) { last = 1; break; }
      if (t >= t_stop) { last = t >= t_end - 1e-9 || t_stop >= t_end; break; }
    }
    fflush(dump);
    FILE *sf = fopen(spath, "a"); if (sf) { stats_line(sf, B, chunk, now() - tstart); fclose(sf); }
    chunk++;
    if (last) break;
  }
  fclose(dump);
  return NULL;
}

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: see dy.c\n"); return 1; }
  const char *mode = argv[1]; load(argv[2]);
#ifdef _WIN32
  SetPriorityClass(GetCurrentProcess(), BELOW_NORMAL_PRIORITY_CLASS);
#endif
  if (!strcmp(mode, "run")) {
    if (argc < 15) { fprintf(stderr, "usage: dy run VESSEL SEED0 THREADS HOURS CHUNK_MIN OUTDIR PBAR KDUMP NULLSH H R MAXDEATH MAXREC\n"); return 1; }
    u64 seed0 = strtoull(argv[3], 0, 10); g_threads = atoi(argv[4]); g_hours = atof(argv[5]); g_chunk = atof(argv[6]);
    g_out = argv[7]; g_pbar = atof(argv[8]); g_kdump = atoi(argv[9]); g_nullsh = atoi(argv[10]); g_H = atoi(argv[11]);
    g_R = atoi(argv[12]); g_maxdeath = atoll(argv[13]); g_maxrec = atoll(argv[14]);
    if (g_R > g_H || g_threads < 1 || g_threads > 12) { fprintf(stderr, "bad R/H or threads\n"); return 1; }
    pthread_t th[12];
    for (int t = 0; t < g_threads; t++) pthread_create(&th[t], NULL, worker, (void *)(uintptr_t)(seed0 + t));
    for (int t = 0; t < g_threads; t++) pthread_join(th[t], NULL);
    return 0;
  }
  if (!strcmp(mode, "trace")) {
    blk_t *B = malloc(sizeof(blk_t)); blk_init(B, 1, NULL, NULL, NULL, 0);
    FILE *f = fopen(argv[3], "rb"); if (fread(B->cur, 8, (size_t)n * W, f) != (size_t)n * W) return 1; fclose(f);
    memcpy(B->prv, B->cur, 8 * (size_t)n * W);
    FILE *o = fopen(argv[4], "wb"); long long G = atoll(argv[5]);
    for (long long g = 0; g < G; g++) { step(B, 1); fwrite(B->cur, 8, (size_t)n * W, o); }
    fclose(o); return 0;
  }
  if (!strcmp(mode, "events")) {
    if (argc < 12) { fprintf(stderr, "usage: dy events VESSEL SEED GENS OUTDIR PBAR KDUMP NULLSH H R NL\n"); return 1; }
    char p1[1024], p2[1024], p3[1024], p4[1024]; const char *od = argv[5];
    g_pbar = atof(argv[6]); g_kdump = atoi(argv[7]); g_nullsh = atoi(argv[8]); g_H = atoi(argv[9]); g_R = atoi(argv[10]); g_nl = atoi(argv[11]);
    snprintf(p1, sizeof p1, "%s/lives.txt", od); snprintf(p2, sizeof p2, "%s/soups.bin", od);
    snprintf(p3, sizeof p3, "%s/dump.bin", od); snprintf(p4, sizeof p4, "%s/stats.txt", od);
    FILE *lv = fopen(p1, "w"), *sp = fopen(p2, "wb"), *dp = fopen(p3, "wb");
    blk_t *B = malloc(sizeof(blk_t)); blk_init(B, strtoull(argv[3], 0, 10), lv, sp, dp, 1);
    long long G = atoll(argv[4]); double t0 = now();
    for (long long g = 0; g < G; g++) { step(B, 1); count_ring_tally(B); events(B); }
    for (int l = 0; l < LN; l++) fprintf(lv, "%d %lld %lld 0\n", l, B->birth[l], B->g - B->birth[l]);
    fclose(lv); fclose(sp); fclose(dp);
    FILE *sf = fopen(p4, "w"); stats_line(sf, B, 0, now() - t0); fclose(sf);
    printf("events: gens %lld face %lld fw %lld s12 %lld scyc %lld; deaths_ok %lld dumps %lld rec %lld null %lld; %.1f s\n",
           B->g, B->cnt[1], B->cnt[4], B->cnt[2], B->cnt[3], B->deaths_ok, B->ndd, B->nrd, B->nnull, now() - t0);
    return 0;
  }
  if (!strcmp(mode, "bench")) {
    g_H = 4096;
    blk_t *B = malloc(sizeof(blk_t)); blk_init(B, strtoull(argv[3], 0, 10), NULL, NULL, NULL, 1);
    long long G = atoll(argv[4]); double t0 = now();
    for (long long g = 0; g < G; g++) { step(B, 1); count_ring_tally(B); events(B); }
    double dt = now() - t0;
    printf("bench n=%d: %lld gens x %d lanes in %.3f s: %.4g replica-gens/s; face %lld fw %lld settled %lld\n",
           n, G, LN, dt, G * (double)LN / dt, B->cnt[1], B->cnt[4], B->cnt[2] + B->cnt[3]);
    return 0;
  }
  fprintf(stderr, "unknown mode\n"); return 1;
}
