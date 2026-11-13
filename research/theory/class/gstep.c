/* gstep.c -- 64 bit-sliced replicas of an outer-totalistic rule on an arbitrary finite cell graph.
 * Written for research/theory/class (what is the class of "gumps"?).  Independent of research/toy2d/t2d.c.
 *
 * Graph file (written by vessel.py), all int32:
 *   N K ; nb[N*K] (-1 = no cell / dead forever) ; nlab ; lab[N] ; nF ; for each watched face: len, cells[len]
 *
 *   gstep qsd  GRAPH Bmask Smask b p seed T0 maxgens maxsec chk
 *       quasi-stationary sampling with restarts.  A replica is ended, recorded and reseeded when
 *         FACE   a watched face (a whole boundary layer) is empty                      -- checked every generation
 *         SEAL   the largest dead sealed set K (every cell <= b-1 neighbours outside K) is nonempty although
 *                no watched face is empty (a transverse cut, a hole, a pit)            -- checked every chk gens
 *         P2     state(t) == state(t-2)                                                -- every generation
 *         CYC    state equals a snapshot taken at the last multiple of 64 or 4096      -- every generation
 *       Events of replicas younger than T0 are counted separately (early) and add no exposure.
 *   gstep bulk GRAPH Bmask Smask b p seed T chk
 *       no restarts; prints at t = chk, 2chk, 4chk, ... : replicas settled, sealed, density and activity of the rest
 *   gstep life GRAPH Bmask Smask b p seed Tmax
 *       no restarts; per replica the time it settled (P2/CYC; -1 = running) and the time of each face's death
 *
 * Activity = fraction of cells with x(t) != x(t-2) (the "mismatch" of the threshold lemma).
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

typedef uint64_t u64;
#define NR 64
#define NP 5 /* counter bit planes: counts up to 31 */

static int N, K, nlab, nF;
static int32_t *nb, *lab;
static int *flen, **fcell;
static u64 *x0, *x1, *x2, *snapA, *snapB, *kk, *kn;
static unsigned Bm, Sm;
static int bmin;

static u64 rs[4];
static inline u64 rotl(const u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static u64 rnd(void) { const u64 r = rotl(rs[1] * 5, 7) * 9, t = rs[1] << 17;
  rs[2] ^= rs[0]; rs[3] ^= rs[1]; rs[1] ^= rs[2]; rs[0] ^= rs[3]; rs[2] ^= t; rs[3] = rotl(rs[3], 45); return r; }
static void seedrng(u64 s) { rs[0] = 0x9E3779B97F4A7C15ULL ^ s; rs[1] = 0xD1B54A32D192ED03ULL + s * 7;
  rs[2] = 0x8CB92BA72F3D8DD7ULL; rs[3] = s * 0x2545F4914F6CDD1DULL + 1; for (int i = 0; i < 20; i++) rnd(); }
static int pb[16];
static void setp(double p) { int v = (int)floor(p * 65536.0 + 0.5); if (v > 65535) v = 65535; if (v < 1) v = 1;
  for (int i = 0; i < 16; i++) pb[i] = (v >> i) & 1; }
static u64 rword(void) { u64 w = 0; for (int i = 0; i < 16; i++) { u64 r = rnd(); w = pb[i] ? (w | r) : (w & r); } return w; }

static void rdi(FILE *f, int32_t *a, size_t n) { if (fread(a, 4, n, f) != n) { fprintf(stderr, "short graph file\n"); exit(2); } }
static void load(const char *fn) {
  FILE *f = fopen(fn, "rb"); if (!f) { perror(fn); exit(2); }
  int32_t h[2]; rdi(f, h, 2); N = h[0]; K = h[1];
  if (K > 31) { fprintf(stderr, "K > 31\n"); exit(2); }
  nb = malloc(4 * (size_t)N * K); rdi(f, nb, (size_t)N * K);
  for (size_t i = 0; i < (size_t)N * K; i++) if (nb[i] < 0) nb[i] = N;
  rdi(f, h, 1); nlab = h[0]; lab = malloc(4 * (size_t)N); rdi(f, lab, N);
  rdi(f, h, 1); nF = h[0]; flen = malloc(sizeof(int) * (nF + 1)); fcell = malloc(sizeof(int *) * (nF + 1));
  for (int j = 0; j < nF; j++) { rdi(f, h, 1); flen[j] = h[0]; fcell[j] = malloc(4 * (size_t)(flen[j] + 1)); rdi(f, fcell[j], flen[j]); }
  fclose(f);
  size_t sz = sizeof(u64) * (size_t)(N + 1);
  x0 = calloc(1, sz); x1 = calloc(1, sz); x2 = calloc(1, sz); snapA = calloc(1, sz); snapB = calloc(1, sz);
  kk = calloc(1, sz); kn = calloc(1, sz);
}

/* count the words src[nb] of cell i into planes c[] */
static inline void count(const u64 *src, int i, u64 *c) {
  const int32_t *q = nb + (size_t)i * K;
  for (int j = 0; j < NP; j++) c[j] = 0;
  for (int k = 0; k < K; k++) {
    u64 carry = src[q[k]];
    for (int j = 0; j < NP && carry; j++) { u64 t = c[j] & carry; c[j] ^= carry; carry = t; }
  }
}
static inline u64 eqk(const u64 *c, int k) { u64 m = ~0ULL; for (int j = 0; j < NP; j++) m &= ((k >> j) & 1) ? c[j] : ~c[j]; return m; }
static inline u64 gek(const u64 *c, int k) { /* count >= k */
  u64 gt = 0, eq = ~0ULL;
  for (int j = NP - 1; j >= 0; j--) { if ((k >> j) & 1) eq &= c[j]; else { gt |= eq & c[j]; eq &= ~c[j]; } }
  return gt | eq; }

static void step(void) { /* x0 -> new x0; x1 <- old x0; x2 <- old x1 */
  u64 *nw = x2; u64 c[NP];
  for (int i = 0; i < N; i++) {
    count(x0, i, c);
    u64 bo = 0, so = 0;
    for (int k = 0; k <= K; k++) { int inb = (Bm >> k) & 1, ins = (Sm >> k) & 1; if (!inb && !ins) continue;
      u64 e = eqk(c, k); if (inb) bo |= e; if (ins) so |= e; }
    nw[i] = (x0[i] & so) | (~x0[i] & bo);
  }
  nw[N] = 0;
  x2 = x1; x1 = x0; x0 = nw; /* now x2 = state(t-2) relative to new x0 = state(t) */
}

/* largest dead sealed subset; returns mask of replicas where it is nonempty */
static u64 sealed(void) {
  u64 c[NP];
  for (int i = 0; i < N; i++) kk[i] = ~x0[i];
  kk[N] = ~0ULL; kn[N] = 0; /* outside the vessel: dead forever, i.e. inside K: contributes 0 to "outside" counts */
  for (int it = 0; it < 100000; it++) {
    u64 any = 0, changed = 0;
    for (int i = 0; i < N; i++) kn[i] = ~kk[i];
    for (int i = 0; i < N; i++) { if (!kk[i]) continue;
      count(kn, i, c); u64 bad = gek(c, bmin) & kk[i]; changed |= bad; kk[i] &= ~bad; any |= kk[i]; }
    if (!any) return 0;
    if (!changed) return any;
  }
  return 0;
}

static void reseed(u64 mask) { for (int i = 0; i < N; i++) { x0[i] = (x0[i] & ~mask) | (rword() & mask); } x0[N] = 0; }
static u64 facedead(int j) { u64 m = 0; for (int q = 0; q < flen[j]; q++) m |= x0[fcell[j][q]]; return ~m; }
static u64 differs(const u64 *a, const u64 *b) { u64 m = 0; for (int i = 0; i < N; i++) m |= a[i] ^ b[i]; return m; }

int main(int argc, char **argv) {
  if (argc < 8) { fprintf(stderr, "usage: see header\n"); return 2; }
  const char *mode = argv[1]; load(argv[2]);
  Bm = (unsigned)strtoul(argv[3], 0, 0); Sm = (unsigned)strtoul(argv[4], 0, 0); bmin = atoi(argv[5]);
  double p = atof(argv[6]); setp(p); seedrng(strtoull(argv[7], 0, 0));
  if (!strcmp(mode, "qsd")) {
    long T0 = atol(argv[8]), maxg = atol(argv[9]); double maxsec = atof(argv[10]); int chk = atoi(argv[11]);
    long t0[NR]; for (int r = 0; r < NR; r++) t0[r] = 0;
    reseed(~0ULL);
    double expo = 0, sa = 0, sa2 = 0; long nface = 0, nseal = 0, np2 = 0, ncyc = 0, early[4] = {0, 0, 0, 0};
    long tA = -1, tB = -1; long t = 0; clock_t c0 = clock();
    double *dl = calloc(nlab, sizeof(double)), *al = calloc(nlab, sizeof(double)); long *nl = calloc(nlab, sizeof(long));
    for (int i = 0; i < N; i++) nl[lab[i]]++;
    double samples = 0; long maxage = 0; double sface[64]; int nsf = 0; (void)sface; (void)nsf;
    while (t < maxg) {
      if ((t & 63) == 0) { memcpy(snapA, x0, sizeof(u64) * N); tA = t; }
      if ((t & 4095) == 0) { memcpy(snapB, x0, sizeof(u64) * N); tB = t; }
      step(); t++;
      u64 ev[4] = {0, 0, 0, 0};
      for (int j = 0; j < nF; j++) ev[0] |= facedead(j);
      u64 old2 = 0, oldA = 0, oldB = 0, oldT = 0;
      for (int r = 0; r < NR; r++) { if (t - t0[r] >= 2) old2 |= 1ULL << r; if (t0[r] <= tA) oldA |= 1ULL << r;
        if (t0[r] <= tB) oldB |= 1ULL << r; if (t - t0[r] >= T0) oldT |= 1ULL << r; }
      ev[2] = ~differs(x0, x2) & old2 & ~ev[0];
      ev[3] = ((~differs(x0, snapA) & oldA) | (~differs(x0, snapB) & oldB)) & ~ev[0] & ~ev[2];
      if (t % chk == 0) {
        ev[1] = sealed() & ~ev[0] & ~ev[2] & ~ev[3];
        u64 m = oldT & ~(ev[0] | ev[1] | ev[2] | ev[3]);
        if (m) { samples += __builtin_popcountll(m);
          for (int i = 0; i < N; i++) { dl[lab[i]] += __builtin_popcountll(x0[i] & m); al[lab[i]] += __builtin_popcountll((x0[i] ^ x2[i]) & m); } }
      }
      u64 all = ev[0] | ev[1] | ev[2] | ev[3];
      if (all) {
        for (int r = 0; r < NR; r++) if ((all >> r) & 1) {
          long age = t - t0[r]; int e = (ev[0] >> r) & 1 ? 0 : (ev[1] >> r) & 1 ? 1 : (ev[2] >> r) & 1 ? 2 : 3;
          if (age < T0) early[e]++;
          else { double a = (double)(age - T0); expo += a; if (e == 0) { nface++; sa += a; sa2 += a * a; } else if (e == 1) nseal++; else if (e == 2) np2++; else ncyc++; }
          t0[r] = t;
        }
        reseed(all);
        /* a reseeded replica must not look period-2 or equal to a snapshot: handled by the age masks */
      }
      if ((t & 1023) == 0 && (double)(clock() - c0) / CLOCKS_PER_SEC > maxsec) break;
    }
    double running = 0; for (int r = 0; r < NR; r++) { long age = t - t0[r]; if (age > maxage) maxage = age; if (age > T0) running += (double)(age - T0); }
    printf("{\"N\":%d,\"K\":%d,\"gens\":%ld,\"T0\":%ld,\"face\":%ld,\"seal\":%ld,\"p2\":%ld,\"cyc\":%ld,\"early\":[%ld,%ld,%ld,%ld],"
           "\"exposure\":%.0f,\"running\":%.0f,\"sum_age\":%.0f,\"sum_age2\":%.6g,\"maxage\":%ld,\"samples\":%.0f,\"nfaces\":%d,\"dens\":[",
           N, K, t, T0, nface, nseal, np2, ncyc, early[0], early[1], early[2], early[3], expo, running, sa, sa2, maxage, samples, nF);
    for (int l = 0; l < nlab; l++) printf("%s%.5f", l ? "," : "", samples && nl[l] ? dl[l] / (samples * nl[l]) : -1.0);
    printf("],\"act\":[");
    for (int l = 0; l < nlab; l++) printf("%s%.5f", l ? "," : "", samples && nl[l] ? al[l] / (samples * nl[l]) : -1.0);
    printf("],\"sec\":%.1f}\n", (double)(clock() - c0) / CLOCKS_PER_SEC);
  } else if (!strcmp(mode, "bulk")) {
    long T = atol(argv[8]); int chk = atoi(argv[9]);
    reseed(~0ULL); u64 settled = 0, seal = 0; long t = 0, next = chk; long tA = -1, tB = -1;
    while (t < T) {
      if ((t & 63) == 0) { memcpy(snapA, x0, sizeof(u64) * N); tA = t; }
      if ((t & 4095) == 0) { memcpy(snapB, x0, sizeof(u64) * N); tB = t; }
      step(); t++;
      if (t >= 2) settled |= ~differs(x0, x2);
      if (tA >= 0) settled |= ~differs(x0, snapA);
      if (tB >= 0) settled |= ~differs(x0, snapB);
      if (t == next || t == T) {
        seal |= sealed(); u64 m = ~settled; double d = 0, a = 0; int cnt = __builtin_popcountll(m);
        for (int i = 0; i < N; i++) { d += __builtin_popcountll(x0[i] & m); a += __builtin_popcountll((x0[i] ^ x2[i]) & m); }
        double dall = 0; for (int i = 0; i < N; i++) dall += __builtin_popcountll(x0[i]);
        printf("{\"t\":%ld,\"settled\":%d,\"sealed\":%d,\"running\":%d,\"dens\":%.5f,\"act\":%.5f,\"dens_all\":%.5f}\n", t,
               __builtin_popcountll(settled), __builtin_popcountll(seal), cnt, cnt ? d / ((double)cnt * N) : -1.0,
               cnt ? a / ((double)cnt * N) : -1.0, dall / (64.0 * N));
        fflush(stdout); next *= 2;
      }
    }
  } else if (!strcmp(mode, "life")) {
    long T = atol(argv[8]); long st[NR]; long (*fd)[NR] = calloc(nF + 1, sizeof(*fd));
    for (int r = 0; r < NR; r++) st[r] = -1; for (int j = 0; j < nF; j++) for (int r = 0; r < NR; r++) fd[j][r] = -1;
    reseed(~0ULL); u64 settled = 0; long t = 0, tA = -1, tB = -1; double pop = 0;
    while (t < T && ~settled) {
      if ((t & 63) == 0) { memcpy(snapA, x0, sizeof(u64) * N); tA = t; }
      if ((t & 4095) == 0) { memcpy(snapB, x0, sizeof(u64) * N); tB = t; }
      step(); t++;
      u64 s = 0; if (t >= 2) s |= ~differs(x0, x2);
      u64 sa = ~differs(x0, snapA), sb = ~differs(x0, snapB);
      for (int r = 0; r < NR; r++) if (!((settled >> r) & 1)) {
        if ((s >> r) & 1) { st[r] = t - 2; settled |= 1ULL << r; }
        else if ((sa >> r) & 1) { st[r] = tA; settled |= 1ULL << r; }
        else if ((sb >> r) & 1) { st[r] = tB; settled |= 1ULL << r; } }
      for (int j = 0; j < nF; j++) { u64 d = facedead(j); for (int r = 0; r < NR; r++) if (((d >> r) & 1) && fd[j][r] < 0) fd[j][r] = t; }
    }
    for (int i = 0; i < N; i++) pop += __builtin_popcountll(x0[i]);
    printf("{\"N\":%d,\"T\":%ld,\"final_dens\":%.5f,\"settle\":[", N, t, pop / (64.0 * N));
    for (int r = 0; r < NR; r++) printf("%s%ld", r ? "," : "", st[r]);
    printf("],\"facedeath\":[");
    for (int j = 0; j < nF; j++) { printf("%s[", j ? "," : ""); for (int r = 0; r < NR; r++) printf("%s%ld", r ? "," : "", fd[j][r]); printf("]"); }
    printf("]}\n");
  } else if (!strcmp(mode, "trace")) { /* gstep trace GRAPH B S b INITFILE(as argv[6]) dummy T : replica 0 from a byte file */
    long T = atol(argv[8]); FILE *f = fopen(argv[6], "rb"); if (!f) { perror(argv[6]); return 2; }
    for (int i = 0; i < N; i++) { int ch = fgetc(f); x0[i] = (ch == 1) ? ~0ULL : 0; } fclose(f);
    for (long t = 0; t < T; t++) { step(); long pop = 0; for (int i = 0; i < N; i++) pop += x0[i] & 1; printf("%ld ", pop); }
    printf("\n"); for (int i = 0; i < N; i++) putchar('0' + (int)(x0[i] & 1)); printf("\n");
    u64 sm = sealed(); printf("%d\n", (int)(sm & 1)); for (int i = 0; i < N; i++) putchar('0' + (int)(kk[i] & 1)); printf("\n");
  } else { fprintf(stderr, "unknown mode\n"); return 2; }
  return 0;
}
