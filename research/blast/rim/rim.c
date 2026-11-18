/* rim.c (research/blast/rim): bit-sliced gump (B45/S345) on a finite cell graph with any number of faces.
 * 64*W replicas (W a multiple of 8, AVX-512 by gcc vector extensions). Renewal lives: a life starts from a fresh
 * p-soup on every node and ends at the first generation in which some face layer is empty (booked every
 * generation), or when it is found settled (state equal to a snapshot 840 m generations back, m = 1..NSNAP-1,
 * within the same life; censored at the snapshot's age); the replica is then reseeded.
 *
 *   rim GRAPH run W P SEED GENS OUT [-s SAMPLE_EVERY] [-r RINGFILE MAXDEATHS]
 *        OUT (text): one line per ended life: "F age mask" (mask: bit f set = face f empty at that generation),
 *        "S age" (settled; age of the matching snapshot), "E age" (open at the end of the run).
 *        stdout: summary; with -s K: per-node live counts over replicas of life age >= 256, every K generations
 *        (written to OUT.dens: node count; first line: number of replica-samples).
 *        -r: for each face death at life age > 400, the bits of all face cells (faces concatenated in file order)
 *        of the dying replica at lags 0,1,..,13 generations before the death generation (lag 0: the first generation
 *        with the face empty), and, every
 *        4096 generations, the same for replica 0 at lag 0 if its age > 400 (stationary samples; lines "Q").
 *   rim GRAPH trace INIT GENS OUT    INIT (text): lines "replica node node ..."; steps GENS generations with no
 *        renewal; OUT (binary): for each generation 0..GENS and each listed replica, n bytes (0/1).
 * Graph (int32 LE): n; nb[n*12] (-1 = dead for ever); nf; per face: size, cells.
 *   gcc -O3 -march=native -o rim rim.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint64_t u64;
typedef u64 v8 __attribute__((vector_size(64), aligned(8)));
#define NSNAP 5
#define MAXF 16
static u64 sm;
static inline u64 rnd(void) { u64 z = (sm += 0x9e3779b97f4a7c15ULL); z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
  z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; return z ^ (z >> 31); }
static int rdi(FILE *f) { int32_t x; if (fread(&x, 4, 1, f) != 1) { fprintf(stderr, "short read\n"); exit(1); } return x; }
#define FA(s, c, x, y, z) do { v8 t_ = (x) ^ (y); s = t_ ^ (z); c = ((x) & (y)) | (t_ & (z)); } while (0)
static inline v8 rule8(const v8 *x, v8 me) {
  v8 s1, c1, s2, c2, s3, c3, s4, c4, S, C, b0, H, t1, d1, t2, d2, b1, e, b2, b3;
  FA(s1, c1, x[0], x[1], x[2]); FA(s2, c2, x[3], x[4], x[5]); FA(s3, c3, x[6], x[7], x[8]); FA(s4, c4, x[9], x[10], x[11]);
  FA(S, C, s1, s2, s3); b0 = S ^ s4; H = S & s4;
  FA(t1, d1, c1, c2, c3); FA(t2, d2, c4, C, H); b1 = t1 ^ t2; e = t1 & t2;
  FA(b2, b3, d1, d2, e);
  /* count = b0 + 2 b1 + 4 b2 + 8 b3; alive next iff count in {4,5}, or me and count == 3 */
  return ~b3 & ((b2 & ~b1) | (me & ~b2 & b1 & b0));
}
static int n, W, nf, fsz[MAXF], *fc[MAXF], *nb;
static void step(const u64 *a, u64 *b) {
  for (int i = 0; i < n; i++) {
    const int *q = nb + 12 * (size_t)i;
    for (int w = 0; w < W; w += 8) {
      v8 x[12]; for (int t = 0; t < 12; t++) memcpy(&x[t], a + (size_t)q[t] * W + w, 64);
      v8 me; memcpy(&me, a + (size_t)i * W + w, 64);
      v8 o = rule8(x, me); memcpy(b + (size_t)i * W + w, &o, 64);
    }
  }
}
static void load(const char *path) {
  FILE *f = fopen(path, "rb"); if (!f) { fprintf(stderr, "no graph\n"); exit(1); }
  n = rdi(f); nb = malloc(4 * 12 * (size_t)n);
  for (int i = 0; i < 12 * n; i++) { int x = rdi(f); nb[i] = x < 0 ? n : x; }
  nf = rdi(f); if (nf > MAXF) { fprintf(stderr, "too many faces\n"); exit(1); }
  for (int k = 0; k < nf; k++) { fsz[k] = rdi(f); fc[k] = malloc(4 * fsz[k]); for (int j = 0; j < fsz[k]; j++) fc[k][j] = rdi(f); }
  fclose(f);
}
int main(int argc, char **argv) {
  if (argc < 6) { fprintf(stderr, "usage\n"); return 1; }
  load(argv[1]);
  if (!strcmp(argv[2], "trace")) {
    W = 8; long gens = atol(argv[4]);
    u64 *a = calloc((size_t)(n + 1) * W, 8), *b = calloc((size_t)(n + 1) * W, 8);
    int reps[64], nr = 0; FILE *g = fopen(argv[3], "r"); char *line = 0; size_t cap = 0;
    while (getline(&line, &cap, g) > 0) { char *p = line; int r = strtol(p, &p, 10); reps[nr++] = r;
      for (;;) { char *q; long c = strtol(p, &q, 10); if (q == p) break; p = q; a[(size_t)c * W + r / 64] |= 1ULL << (r % 64); } }
    fclose(g); FILE *o = fopen(argv[5], "wb"); unsigned char *buf = malloc(n);
    for (long t = 0; t <= gens; t++) {
      for (int k = 0; k < nr; k++) { int r = reps[k]; for (int i = 0; i < n; i++) buf[i] = (a[(size_t)i * W + r / 64] >> (r % 64)) & 1; fwrite(buf, 1, n, o); }
      if (t < gens) { step(a, b); u64 *tt = a; a = b; b = tt; }
    }
    fclose(o); return 0;
  }
  W = atoi(argv[3]); double p = atof(argv[4]); sm = strtoull(argv[5], 0, 10) * 0x2545F4914F6CDD1DULL + 12345;
  long gens = atol(argv[6]); const char *outf = argv[7]; long severy = 0, maxd = 0; const char *ringf = 0;
  for (int i = 8; i < argc; i++) { if (!strcmp(argv[i], "-s")) severy = atol(argv[++i]);
    else if (!strcmp(argv[i], "-r")) { ringf = argv[++i]; maxd = atol(argv[++i]); } }
  int R = 64 * W; u64 thr = (u64)(p * 18446744073709551616.0);
  u64 *a = calloc((size_t)(n + 1) * W, 8), *b = calloc((size_t)(n + 1) * W, 8), *snap = calloc((size_t)NSNAP * n * W, 8);
  long *born = calloc(R, sizeof(long)); double *dens = calloc(n, sizeof(double)); double nsamp = 0;
  for (int i = 0; i < n; i++) for (int w = 0; w < W; w++) { u64 x = 0; for (int k = 0; k < 64; k++) if (rnd() < thr) x |= 1ULL << k; a[(size_t)i * W + w] = x; }
  memcpy(snap, a, 8 * (size_t)n * W);
  FILE *ev = fopen(outf, "w");
  int ncf = 0; for (int k = 0; k < nf; k++) ncf += fsz[k];
  int *allf = malloc(4 * ncf); { int t = 0; for (int k = 0; k < nf; k++) for (int j = 0; j < fsz[k]; j++) allf[t++] = fc[k][j]; }
  enum { RB = 512, NLAG = 14 }; static const int lags[NLAG] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13};
  u64 *ring = ringf ? calloc((size_t)RB * ncf * W, 8) : 0; FILE *rf = ringf ? fopen(ringf, "w") : 0; long nring = 0;
  long nF = 0, nS = 0, nFd[MAXF] = {0}; double E = 0;
  u64 *mature = calloc(W, 8);
  for (long gen = 0; gen < gens; gen++) {
    step(a, b); { u64 *t = a; a = b; b = t; }
    long g1 = gen + 1;
    if (ring) { u64 *sl = ring + (size_t)(g1 % RB) * ncf * W; for (int k = 0; k < ncf; k++) memcpy(sl + (size_t)k * W, a + (size_t)allf[k] * W, 8 * W); }
    if (severy && g1 % severy == 0) {
      for (int w = 0; w < W; w++) { u64 m = 0; for (int k = 0; k < 64; k++) if (g1 - born[64 * w + k] >= 256) m |= 1ULL << k; mature[w] = m; nsamp += __builtin_popcountll(m); }
      for (int i = 0; i < n; i++) { long c = 0; for (int w = 0; w < W; w++) c += __builtin_popcountll(a[(size_t)i * W + w] & mature[w]); dens[i] += c; }
    }
    if (rf && g1 % 4096 == 0 && g1 - born[0] > 400) { fprintf(rf, "Q");
      for (int k = 0; k < ncf; k++) fputc('0' + (int)(a[(size_t)allf[k] * W] & 1), rf); fputc('\n', rf); }
    int set = (g1 % 840 == 0);
    for (int w = 0; w < W; w++) {
      u64 dead[MAXF], endF = 0, endS = 0; int lagS[64];
      for (int k = 0; k < nf; k++) { u64 x = 0; const int *c = fc[k]; for (int j = 0; j < fsz[k]; j++) x |= a[(size_t)c[j] * W + w]; dead[k] = ~x; endF |= ~x; }
      if (set) { long c = g1 / 840; for (int k = 0; k < 64; k++) lagS[k] = 0;
        for (int m = 1; m < NSNAP && m <= c; m++) { const u64 *sp = snap + (size_t)((c - m) % NSNAP) * n * W;
          u64 eq = ~0ULL; for (int i = 0; i < n && eq; i++) eq &= ~(a[(size_t)i * W + w] ^ sp[(size_t)i * W + w]);
          for (int k = 0; k < 64; k++) if (((eq >> k) & 1) && !lagS[k] && g1 - born[64 * w + k] > 840L * m) { lagS[k] = m; endS |= 1ULL << k; } }
        u64 *sc = snap + (size_t)(c % NSNAP) * n * W; for (int i = 0; i < n; i++) sc[(size_t)i * W + w] = a[(size_t)i * W + w]; }
      u64 endAny = endF | endS; if (!endAny) continue;
      for (int k = 0; k < 64; k++) { u64 bit = 1ULL << k; if (!(endAny & bit)) continue; int r = 64 * w + k; long age = g1 - born[r];
        if (endF & bit) { int mask = 0; for (int f = 0; f < nf; f++) if (dead[f] & bit) { mask |= 1 << f; nFd[f]++; }
          nF++; fprintf(ev, "F %ld %d\n", age, mask); E += age;
          if (rf && age > 400 && nring < maxd) { nring++; fprintf(rf, "D %d %ld", mask, age);
            for (int l = 0; l < NLAG; l++) { const u64 *sl = ring + (size_t)((g1 - lags[l]) % RB) * ncf * W; fputc(' ', rf);
              for (int j = 0; j < ncf; j++) fputc('0' + (int)((sl[(size_t)j * W + w] >> k) & 1), rf); }
            fputc('\n', rf); } }
        else { nS++; fprintf(ev, "S %ld\n", age - 840L * lagS[k]); E += age - 840L * lagS[k]; }
        for (int i = 0; i < n; i++) { u64 *x = a + (size_t)i * W + w; if (rnd() < thr) *x |= bit; else *x &= ~bit; }
        born[r] = g1;
      }
    }
  }
  for (int r = 0; r < R; r++) { long age = gens - born[r]; fprintf(ev, "E %ld\n", age); E += age; }
  fclose(ev); if (rf) fclose(rf);
  if (severy) { char nm[1024]; snprintf(nm, sizeof nm, "%s.dens", outf); FILE *d = fopen(nm, "w"); fprintf(d, "%.0f\n", nsamp);
    for (int i = 0; i < n; i++) fprintf(d, "%.0f\n", dens[i]); fclose(d); }
  printf("SUMMARY n %d nf %d gens %ld R %d exposure %.6e F %ld S %ld perface", n, nf, gens, R, E, nF, nS);
  for (int f = 0; f < nf; f++) printf(" %ld", nFd[f]); printf("\n");
  return 0;
}
