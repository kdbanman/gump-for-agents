/* ex5.c (blast/model): ex3.c plus, for the boom-and-bust decomposition, (1) DL[lag][P]: for every face death at age > T0,
 * the face's population lag = 1..15 generations before it; (2) J[P'][P]: the joint histogram of the face's population at
 * consecutive generations (both at age > T0). Appended to HIST as lines 'dl LAG c0 .. c127' and 'J Pprev c0 .. c127'.
 * Identity used: for any fixed lag L, deaths/exposure = sum_P pi(P) g_L(P), g_L(P) = DL[L][P]/phist[P].
 * Nothing else is changed (the lives file stays byte-identical to sy's; checked by validate.py's same_lives on ex5).
 *
 * ex3.c: ex.c (round 2) for faces of up to 127 cells, plus dumps of deep excursions (round 3).
 *   ex3 GRAPH run SEED P GENS CHK OUT PBAR T0 HIST M3 DUMP CAP
 *   as ex, and: for every excursion whose P reaches <= M3 (M3 < 0: none; faces of <= 64 nodes only), the face
 *   orbit's node states (bit k = k-th node of its group in the graph file) from the first generation with P <= M3 to
 *   the end of the excursion, at most CAP generations; record int32 {replica, face, end type (1 rec, 2 dead,
 *   3 censored), length, minP, truncated} then length uint64 states.
 *
 * ex.c: research/theory/symmetric/sy.c unchanged in its dynamics and lives file, plus online excursion statistics
 * of each face orbit's population P (cells of one face alive) at every generation.
 *
 *   ex GRAPH run SEED P GENS CHK OUT PBAR T0 HIST
 *     HIST (text): exposure E (face-orbit generations at life age > T0), face deaths at age > T0, the histogram of P
 *     over that exposure, and a table minP x end type of excursions (start: first generation with P < PBAR after one
 *     with P >= PBAR, both at age > T0; end 1 recovered (P >= PBAR), 2 dead (P = 0), 3 censored (life ended otherwise
 *     or job ended)). The face's cells are the nodes of its orbit representative (one node per cell, checked).
 *
 * Original header:
 * sy.c: 512 bit-sliced replicas of gump (B45/S345) on a finite cell graph (usually an orbit graph, see geom.py).
 *
 *   sy GRAPH run SEED P GENS CHK OUT     renewal lives from fresh soups of density P (one draw per node);
 *                                        GENS generations per replica; events looked for every CHK generations;
 *                                        one uint32 per finished life in OUT: (age in checks << 3) | type
 *   sy GRAPH trace INIT T                replica 0 from the node list in INIT; prints "gen population" for
 *                                        gen 0..T (population = sum of node weights) and the final node list
 *
 * Life ends (type): 1 F  a face group is empty (the face is dead for ever, T2)
 *                   2 W  a transverse firewall (three consecutive transverse layers empty, T3)
 *                   3 X  both at the same check
 *                   4 S  settled: the state equals a snapshot of the same life. Snapshots are taken on a ladder of
 *                        ages (in checks) 1, 2, .., each rung max(1, age/8) after the last, so any period is caught
 *                        once a rung's gap exceeds it. For an S life the record holds the age of the matching
 *                        SNAPSHOT (the life was already periodic then), not the age at detection.
 *                   5 O  open at the end of the job
 * The kernel is the carry-save adder tree of research/fluct/fl.c. Node index n is a cell that is dead for ever.
 *
 *   gcc -O3 -march=native -o sy sy.c
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define W 8
#define R (64 * W)
typedef uint64_t u64;
static int n, NG, NF, NT;
static int32_t *nb, *wt;
static int *gsz, *goff, *gcell, *face, *trip;
static u64 *cur, *nxt, *snap;
static u64 rs[4];

static inline u64 rotl(const u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static u64 rnd(void) { const u64 r = rotl(rs[1] * 5, 7) * 9, t = rs[1] << 17;
  rs[2] ^= rs[0]; rs[3] ^= rs[1]; rs[1] ^= rs[2]; rs[0] ^= rs[3]; rs[2] ^= t; rs[3] = rotl(rs[3], 45); return r; }
static void seed_rng(u64 s) { for (int i = 0; i < 4; i++) { s += 0x9E3779B97F4A7C15ULL; u64 z = s;
  z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL; z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL; rs[i] = z ^ (z >> 31); } }

#define FA(a, b, c, sum, car) { u64 _x = (a) ^ (b); sum = _x ^ (c); car = ((a) & (b)) | (_x & (c)); }

static void step(void) {
  for (int i = 0; i < n; i++) {
    const int32_t *q = nb + 12 * (size_t)i; u64 *o = nxt + (size_t)i * W; const u64 *me = cur + (size_t)i * W;
    const u64 *x0 = cur + (size_t)q[0] * W, *x1 = cur + (size_t)q[1] * W, *x2 = cur + (size_t)q[2] * W, *x3 = cur + (size_t)q[3] * W,
              *x4 = cur + (size_t)q[4] * W, *x5 = cur + (size_t)q[5] * W, *x6 = cur + (size_t)q[6] * W, *x7 = cur + (size_t)q[7] * W,
              *x8 = cur + (size_t)q[8] * W, *x9 = cur + (size_t)q[9] * W, *x10 = cur + (size_t)q[10] * W, *x11 = cur + (size_t)q[11] * W;
    for (int w = 0; w < W; w++) {
      u64 s0, c0, s1, c1, s2, c2, s3, c3, o1, t4, b0, t5, u0, f0, u1, f1, b1, f2, b2, b3;
      FA(x0[w], x1[w], x2[w], s0, c0); FA(x3[w], x4[w], x5[w], s1, c1);
      FA(x6[w], x7[w], x8[w], s2, c2); FA(x9[w], x10[w], x11[w], s3, c3);
      FA(s0, s1, s2, o1, t4); b0 = o1 ^ s3; t5 = o1 & s3;
      FA(c0, c1, c2, u0, f0); FA(c3, t4, t5, u1, f1); b1 = u0 ^ u1; f2 = u0 & u1;
      FA(f0, f1, f2, b2, b3);
      /* count = b0 + 2 b1 + 4 b2 + 8 b3; alive next iff count in {4,5}, or me and count == 3 */
      o[w] = ~b3 & ((b2 & ~b1) | (me[w] & ~b2 & b1 & b0));
    }
  }
  u64 *t = cur; cur = nxt; nxt = t;
}

static void reseed(int r, u64 thr) {
  int w = r / 64; u64 bit = 1ULL << (r % 64);
  for (int i = 0; i < n; i++) { u64 *x = cur + (size_t)i * W + w; *x &= ~bit; if (rnd() < thr) *x |= bit; }
}

static void die(const char *m) { fprintf(stderr, "sy: %s\n", m); exit(1); }

static void load(const char *path) {
  FILE *f = fopen(path, "r"); if (!f) die("cannot open graph");
  if (fscanf(f, "%d", &n) != 1) die("bad graph");
  nb = malloc(4 * 12 * (size_t)n); wt = malloc(4 * (size_t)n);
  for (size_t i = 0; i < 12 * (size_t)n; i++) { int v; if (fscanf(f, "%d", &v) != 1) die("bad nb"); nb[i] = v < 0 ? n : v; }
  for (int i = 0; i < n; i++) if (fscanf(f, "%d", &wt[i]) != 1) die("bad wt");
  if (fscanf(f, "%d", &NG) != 1) die("bad ng");
  gsz = malloc(4 * (NG + 1)); goff = malloc(4 * (NG + 2)); goff[0] = 0;
  size_t cap = 1024, used = 0; gcell = malloc(4 * cap);
  for (int g = 0; g < NG; g++) { if (fscanf(f, "%d", &gsz[g]) != 1) die("bad group");
    for (int k = 0; k < gsz[g]; k++) { if (used == cap) { cap *= 2; gcell = realloc(gcell, 4 * cap); }
      if (fscanf(f, "%d", &gcell[used++]) != 1) die("bad group cell"); }
    goff[g + 1] = (int)used; }
  if (fscanf(f, "%d", &NF) != 1) die("bad nf");
  face = malloc(4 * (NF + 1)); for (int k = 0; k < NF; k++) if (fscanf(f, "%d", &face[k]) != 1) die("bad face");
  if (fscanf(f, "%d", &NT) != 1) die("bad nt");
  trip = malloc(12 * (size_t)(NT + 1)); for (int k = 0; k < 3 * NT; k++) if (fscanf(f, "%d", &trip[k]) != 1) die("bad triple");
  fclose(f);
  size_t sz = (size_t)(n + 1) * W * 8;
  cur = aligned_alloc(64, sz); nxt = aligned_alloc(64, sz); snap = aligned_alloc(64, sz);
  memset(cur, 0, sz); memset(nxt, 0, sz); memset(snap, 0, sz);
}

int main(int argc, char **argv) {
  if (argc < 3) die("usage");
  load(argv[1]);
  if (!strcmp(argv[2], "trace")) {
    FILE *f = fopen(argv[3], "r"); if (!f) die("cannot open init"); long T = atol(argv[4]); int v;
    while (fscanf(f, "%d", &v) == 1) cur[(size_t)v * W] |= 1ULL;
    fclose(f);
    for (long t = 0; t <= T; t++) {
      long pop = 0; for (int i = 0; i < n; i++) if (cur[(size_t)i * W] & 1) pop += wt[i];
      printf("%ld %ld\n", t, pop);
      if (t < T) step();
    }
    printf("final");
    for (int i = 0; i < n; i++) if (cur[(size_t)i * W] & 1) printf(" %d", i);
    printf("\n");
    return 0;
  }
  if (strcmp(argv[2], "run")) die("mode");
  double pbar = atof(argv[8]); long t0 = atol(argv[9]); FILE *hf = fopen(argv[10], "w"); if (!hf) die("cannot open hist");
  /* face orbit representatives: group ids in face[]; their node lists in gcell */
  static int agen[R], inexc[R][8], minp[R][8], prevok[R][8], fdead[R][8];
  static long phist[8][128], exc[128][4]; long expo = 0, fdeaths = 0;
  static unsigned char ring[R][8][16]; static long DL[16][128], JJ[128][128];
  if (NF > 8) die("NF > 8");
  for (int f = 0; f < NF; f++) if (gsz[face[f]] > 127) die("face orbit with more than 127 nodes");
  #define FACEPOP(cnt_) { for (int f = 0; f < NF; f++) { u64 c[W][7]; memset(c, 0, sizeof c); \
      for (int k = goff[face[f]]; k < goff[face[f] + 1]; k++) { const u64 *x = cur + (size_t)gcell[k] * W; \
        for (int w = 0; w < W; w++) { u64 car = x[w]; for (int b = 0; b < 7 && car; b++) { u64 t = c[w][b] & car; c[w][b] ^= car; car = t; } } } \
      for (int r = 0; r < R; r++) { int w = r / 64, bb = r % 64, v = 0; for (int b = 0; b < 7; b++) v |= (int)((c[w][b] >> bb) & 1) << b; cnt_[r][f] = v; } } }
  static int pop[R][8];
  int M3 = atoi(argv[11]); FILE *df = fopen(argv[12], "wb"); int CAP = atoi(argv[13]); if (!df) die("cannot open dump");
  for (int f = 0; f < NF; f++) if (gsz[face[f]] > 64) M3 = -1;
  static int rec_on[R][8], rec_len[R][8], rec_trunc[R][8]; u64 *recbuf = calloc((size_t)R * 8 * CAP, 8); long ndumped = 0;
  #define FSTATE(r_, f_) ({ int w_ = (r_) / 64, b_ = (r_) % 64; u64 v_ = 0; int kk_ = 0; \
      for (int k_ = goff[face[f_]]; k_ < goff[face[f_] + 1]; k_++, kk_++) v_ |= ((cur[(size_t)gcell[k_] * W + w_] >> b_) & 1ULL) << kk_; v_; })
  #define RECEND(r_, f_, ty_) { if (rec_on[r_][f_]) { int32_t hd_[6] = {r_, f_, ty_, rec_len[r_][f_], minp[r_][f_], rec_trunc[r_][f_]}; \
      fwrite(hd_, 4, 6, df); fwrite(recbuf + ((size_t)(r_) * 8 + (f_)) * CAP, 8, rec_len[r_][f_], df); ndumped++; rec_on[r_][f_] = 0; } }
  #define RECADD(r_, f_) { if (rec_len[r_][f_] < CAP) recbuf[((size_t)(r_) * 8 + (f_)) * CAP + rec_len[r_][f_]++] = FSTATE(r_, f_); else rec_trunc[r_][f_] = 1; }
  u64 seed = strtoull(argv[3], 0, 10); double p = atof(argv[4]); long gens = atol(argv[5]); int chk = atoi(argv[6]);
  FILE *out = fopen(argv[7], "wb"); if (!out) die("cannot open out");
  seed_rng(seed); u64 thr = (u64)(p * 18446744073709551616.0);
  static uint32_t age[R], snapage[R], nextsnap[R];
  for (int r = 0; r < R; r++) { reseed(r, thr); age[r] = 0; snapage[r] = 0; nextsnap[r] = 1; }
  memcpy(snap, cur, (size_t)(n + 1) * W * 8);
  u64 *z = malloc(8 * (size_t)W * (NG + 1));
  long nlives = 0, cnt[6] = {0, 0, 0, 0, 0, 0};
  for (long g = 0; g < gens; g += chk) {
    for (int k = 0; k < chk; k++) { step();
      FACEPOP(pop);
      for (int r = 0; r < R; r++) { agen[r]++; int ok = agen[r] > t0;
        for (int f = 0; f < NF; f++) { if (fdead[r][f]) continue; int P = pop[r][f];
          if (ok) { expo++; phist[f][P]++; }
          if (ok && agen[r] - 1 > t0) JJ[ring[r][f][(agen[r] - 1) & 15]][P]++;
          if (ok && P == 0) for (int L = 1; L < 16; L++) if (agen[r] - L > t0) DL[L][ring[r][f][(agen[r] - L) & 15]]++;
          ring[r][f][agen[r] & 15] = (unsigned char)P;
          if (inexc[r][f]) { if (P < minp[r][f]) minp[r][f] = P;
            if (!rec_on[r][f] && P <= M3) { rec_on[r][f] = 1; rec_len[r][f] = 0; rec_trunc[r][f] = 0; }
            if (rec_on[r][f]) RECADD(r, f);
            if (P == 0) { exc[minp[r][f]][2]++; inexc[r][f] = 0; RECEND(r, f, 2); }
            else if (P >= pbar) { exc[minp[r][f]][1]++; inexc[r][f] = 0; RECEND(r, f, 1); } }
          else if (ok && prevok[r][f] && P < pbar) { inexc[r][f] = 1; minp[r][f] = P;
            if (P <= M3) { rec_on[r][f] = 1; rec_len[r][f] = 0; rec_trunc[r][f] = 0; RECADD(r, f); }
            if (P == 0) { exc[0][2]++; inexc[r][f] = 0; RECEND(r, f, 2); } }
          if (P == 0) { fdead[r][f] = 1; if (ok) fdeaths++; }
          prevok[r][f] = ok && P >= pbar; } } }
    u64 fd[W], fw[W], eq[W], take[W];
    for (int w = 0; w < W; w++) { fd[w] = 0; fw[w] = 0; eq[w] = 0; take[w] = 0; }
    for (int gI = 0; gI < NG; gI++) { u64 *zz = z + (size_t)gI * W; for (int w = 0; w < W; w++) zz[w] = 0;
      for (int k = goff[gI]; k < goff[gI + 1]; k++) { const u64 *x = cur + (size_t)gcell[k] * W; for (int w = 0; w < W; w++) zz[w] |= x[w]; }
      for (int w = 0; w < W; w++) zz[w] = ~zz[w]; }
    for (int k = 0; k < NF; k++) for (int w = 0; w < W; w++) fd[w] |= z[(size_t)face[k] * W + w];
    for (int k = 0; k < NT; k++) for (int w = 0; w < W; w++)
      fw[w] |= z[(size_t)trip[3 * k] * W + w] & z[(size_t)trip[3 * k + 1] * W + w] & z[(size_t)trip[3 * k + 2] * W + w];
    for (int i = 0; i < n; i++) { const u64 *x = cur + (size_t)i * W, *s = snap + (size_t)i * W; for (int w = 0; w < W; w++) eq[w] |= x[w] ^ s[w]; }
    for (int r = 0; r < R; r++) {
      int w = r / 64; u64 bit = 1ULL << (r % 64);
      age[r]++;
      int f = (fd[w] & bit) != 0, x = (fw[w] & bit) != 0, s = (eq[w] & bit) == 0;
      int type = (f && x) ? 3 : f ? 1 : x ? 2 : s ? 4 : 0;
      if (type) { uint32_t rec = ((type == 4 ? snapage[r] : age[r]) << 3) | (uint32_t)type; fwrite(&rec, 4, 1, out); cnt[type]++; nlives++;
        reseed(r, thr); age[r] = 0; snapage[r] = 0; nextsnap[r] = 1; take[w] |= bit;
        agen[r] = 0; for (int f = 0; f < NF; f++) { if (inexc[r][f]) { exc[minp[r][f]][3]++; RECEND(r, f, 3); } inexc[r][f] = 0; prevok[r][f] = 0; fdead[r][f] = 0; } }
      else if (age[r] == nextsnap[r]) { take[w] |= bit; snapage[r] = age[r]; nextsnap[r] = age[r] + (age[r] / 8 > 1 ? age[r] / 8 : 1); }
      if (age[r] >= (1u << 28)) die("age overflow");
    }
    for (int i = 0; i < n; i++) { const u64 *x = cur + (size_t)i * W; u64 *s = snap + (size_t)i * W;
      for (int w = 0; w < W; w++) s[w] = (s[w] & ~take[w]) | (x[w] & take[w]); }
    if (((g / chk) & 0xFFFF) == 0) fflush(out);
  }
  for (int r = 0; r < R; r++) { uint32_t rec = (age[r] << 3) | 5u; fwrite(&rec, 4, 1, out); cnt[5]++; }
  fclose(out);
  for (int r = 0; r < R; r++) for (int f = 0; f < NF; f++) if (inexc[r][f]) { exc[minp[r][f]][3]++; RECEND(r, f, 3); }
  fclose(df); fprintf(stderr, "dumped %ld deep excursions (M3 %d)\n", ndumped, M3);
  fprintf(hf, "expo %ld\nfdeaths %ld\nnf %d\npbar %g\nt0 %ld\n", expo, fdeaths, NF, pbar, t0);
  fprintf(hf, "phist"); for (int P = 0; P < 128; P++) { long t = 0; for (int f = 0; f < NF; f++) t += phist[f][P]; fprintf(hf, " %ld", t); } fprintf(hf, "\n");
  for (int P = 0; P < 128; P++) fprintf(hf, "exc %d %ld %ld %ld\n", P, exc[P][1], exc[P][2], exc[P][3]);
  for (int L = 1; L < 16; L++) { fprintf(hf, "dl %d", L); for (int P = 0; P < 128; P++) fprintf(hf, " %ld", DL[L][P]); fprintf(hf, "\n"); }
  for (int Q = 0; Q < 128; Q++) { long t = 0; for (int P = 0; P < 128; P++) t += JJ[Q][P]; if (!t) continue;
    fprintf(hf, "J %d", Q); for (int P = 0; P < 128; P++) fprintf(hf, " %ld", JJ[Q][P]); fprintf(hf, "\n"); }
  fclose(hf);
  printf("{\"snap\": \"ladder\", \"n\": %d, \"gens\": %ld, \"chk\": %d, \"p\": %g, \"seed\": %llu, \"F\": %ld, \"W\": %ld, \"X\": %ld, \"S\": %ld, \"open\": %ld}\n",
         n, gens, chk, p, (unsigned long long)seed, cnt[1], cnt[2], cnt[3], cnt[4], cnt[5]);
  return 0;
}
