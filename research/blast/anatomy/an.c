/* an.c (research/blast/anatomy): bit-sliced gump (B45/S345), 512 replicas, on a cell graph written by geom.py.
 * Written from docs/AUTOMATON.md for the blast of 2026-11-18; shares no code with the earlier steppers
 * (the carry-save count is the textbook one). Validated against reference/oracle.py by validate.py.
 *
 * Graph file (int32 LE): n; nbr[12 n] (-1 = a cell that is dead for ever); nf; per face: na, face cells, nu,
 *   cells of the layer beneath; ng; per transverse group: nl; per layer (ring order): size, cells.
 *
 *   an GRAPH run SEED P GENS T0 PBAR H MAXREC OUT
 *       renewal lives from fresh soups of density P. A life ends when a face is empty (F), when three consecutive
 *       transverse layers are empty (W, looked for every 64 generations), or when the state equals a snapshot
 *       taken 840 m generations earlier in the same life, m = 1..32 (S). Statistics only at life age > T0.
 *       OUT.sum: exposure, deaths, histogram of the face population P, excursions below PBAR by minimum, occupancy.
 *       OUT.rec: for each of the first MAXREC deaths, int64 {replica, face, age, generation, firewall flag,
 *                generations since P was last >= PBAR (-1: never at age > T0)} then H rows, row j = state j
 *                generations before the death (j = 0..H-1): the face's cells then the layer beneath, bit-packed
 *                (ceil(na/8) + ceil(nu/8) bytes per row).
 *   an GRAPH trace INIT T OUT
 *       replica 0 from the cell list INIT (the other 511 from a soup); OUT gets ceil(n/8) bytes per generation 0..T.
 *   an GRAPH punch SEED P T0 TMAX NTRIALS CLEAR OUT
 *       per trial: fresh soups, T0 generations, then the cells listed in CLEAR are killed in every replica and
 *       face 0 (its cells, then the layer beneath) is written for generations 0..TMAX: 8 uint64 per cell.
 *
 *   gcc -O3 -march=native -o an an.c -lm
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
typedef uint64_t u64;
typedef u64 v8 __attribute__((vector_size(64), aligned(8)));
#define W 8
#define R 512
#define NS 33
static u64 sm;
static inline u64 rnd(void) { u64 z = (sm += 0x9e3779b97f4a7c15ULL); z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
  z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; return z ^ (z >> 31); }
static int rdi(FILE *f) { int32_t x; if (fread(&x, 4, 1, f) != 1) { fprintf(stderr, "short read\n"); exit(1); } return x; }

/* n = number of live neighbours among 12 = b0 + 2 b1 + 4 b2 + 8 b3; alive next iff n in {4,5}, or n = 3 and alive. */
#define FA(s, c, x, y, z) do { v8 t_ = (x) ^ (y); s = t_ ^ (z); c = ((x) & (y)) | (t_ & (z)); } while (0)
static inline v8 rule8(const v8 *x, v8 me) {
  v8 s1, c1, s2, c2, s3, c3, s4, c4, S, C, b0, Hh, t1, d1, t2, d2, b1, e, b2, b3;
  FA(s1, c1, x[0], x[1], x[2]); FA(s2, c2, x[3], x[4], x[5]); FA(s3, c3, x[6], x[7], x[8]); FA(s4, c4, x[9], x[10], x[11]);
  FA(S, C, s1, s2, s3); b0 = S ^ s4; Hh = S & s4;              /* ones: b0, carries C and Hh of weight 2 */
  FA(t1, d1, c1, c2, c3); FA(t2, d2, c4, C, Hh); b1 = t1 ^ t2; e = t1 & t2;   /* twos */
  FA(b2, b3, d1, d2, e);                                        /* fours */
  return ~b3 & ((b2 & ~b1) | (me & ~b2 & b1 & b0));
}
static int n, *nb;
static void step(const u64 *a, u64 *b) {
  for (int i = 0; i < n; i++) {
    const int *q = nb + 12 * (size_t)i; v8 x[12], me, o;
    for (int t = 0; t < 12; t++) memcpy(&x[t], a + (size_t)q[t] * W, 64);
    memcpy(&me, a + (size_t)i * W, 64); o = rule8(x, me); memcpy(b + (size_t)i * W, &o, 64);
  }
}
typedef struct { int na, nu, *c; } face;
static int nf; static face *F;
static int ng, *gl, **gsz, ***gc;
static void readgraph(const char *path) {
  FILE *f = fopen(path, "rb"); if (!f) { perror(path); exit(1); }
  n = rdi(f); nb = malloc(4 * 12 * (size_t)n);
  for (int i = 0; i < 12 * n; i++) { int x = rdi(f); nb[i] = x < 0 ? n : x; }
  nf = rdi(f); F = malloc(sizeof(face) * nf);
  for (int k = 0; k < nf; k++) { int na = rdi(f); int *c = malloc(4 * 4096); for (int j = 0; j < na; j++) c[j] = rdi(f);
    int nu = rdi(f); for (int j = 0; j < nu; j++) c[na + j] = rdi(f); F[k].na = na; F[k].nu = nu; F[k].c = c; }
  ng = rdi(f); gl = malloc(4 * (ng + 1)); gsz = malloc(sizeof(int *) * (ng + 1)); gc = malloc(sizeof(int **) * (ng + 1));
  for (int g = 0; g < ng; g++) { gl[g] = rdi(f); gsz[g] = malloc(4 * gl[g]); gc[g] = malloc(sizeof(int *) * gl[g]);
    for (int l = 0; l < gl[g]; l++) { gsz[g][l] = rdi(f); gc[g][l] = malloc(4 * gsz[g][l]); for (int j = 0; j < gsz[g][l]; j++) gc[g][l][j] = rdi(f); } }
  fclose(f);
}
static u64 thr;
static void seed_rep(u64 *a, int r) { u64 bit = 1ULL << (r & 63); int w = r >> 6;
  for (int i = 0; i < n; i++) { if (rnd() < thr) a[(size_t)i * W + w] |= bit; else a[(size_t)i * W + w] &= ~bit; } }
/* replicas with a transverse firewall: three consecutive (ring) layers of some group empty */
static void firewalls(const u64 *a, u64 *fw) {
  for (int w = 0; w < W; w++) fw[w] = 0;
  for (int g = 0; g < ng; g++) { int L = gl[g]; u64 *e = malloc(8 * W * L);
    for (int l = 0; l < L; l++) for (int w = 0; w < W; w++) { u64 o = 0; for (int j = 0; j < gsz[g][l]; j++) o |= a[(size_t)gc[g][l][j] * W + w]; e[l * W + w] = ~o; }
    for (int l = 0; l < L; l++) for (int w = 0; w < W; w++) fw[w] |= e[l * W + w] & e[((l + 1) % L) * W + w] & e[((l + 2) % L) * W + w];
    free(e); }
}

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: see header\n"); return 1; }
  readgraph(argv[1]);
  size_t SZ = (size_t)(n + 1) * W * 8;
  u64 *a = aligned_alloc(64, SZ), *b = aligned_alloc(64, SZ); memset(a, 0, SZ); memset(b, 0, SZ);
  if (!strcmp(argv[2], "trace")) {
    int T = atoi(argv[4]); sm = 777; thr = (u64)(0.4 * 18446744073709551616.0);
    for (int r = 0; r < R; r++) seed_rep(a, r);
    for (int i = 0; i < n; i++) a[(size_t)i * W] &= ~1ULL;
    FILE *g = fopen(argv[3], "r"); int c; while (fscanf(g, "%d", &c) == 1) a[(size_t)c * W] |= 1ULL; fclose(g);
    FILE *o = fopen(argv[5], "wb"); int nbt = (n + 7) / 8; unsigned char *buf = malloc(nbt);
    for (int t = 0; t <= T; t++) {
      memset(buf, 0, nbt); for (int i = 0; i < n; i++) if (a[(size_t)i * W] & 1ULL) buf[i >> 3] |= 1 << (i & 7);
      fwrite(buf, 1, nbt, o);
      step(a, b); u64 *x = a; a = b; b = x; }
    fclose(o); return 0;
  }
  if (!strcmp(argv[2], "punch")) {
    sm = strtoull(argv[3], 0, 10) * 0x2545F4914F6CDD1DULL + 12345; double p = atof(argv[4]); thr = (u64)(p * 18446744073709551616.0);
    int T0 = atoi(argv[5]), TMAX = atoi(argv[6]), NT = atoi(argv[7]);
    int *cl = malloc(4 * (size_t)n), ncl = 0; FILE *g = fopen(argv[8], "r"); int c; while (fscanf(g, "%d", &c) == 1) cl[ncl++] = c; fclose(g);
    FILE *o = fopen(argv[9], "wb"); int nw = F[0].na + F[0].nu;
    for (int tr = 0; tr < NT; tr++) {
      for (int r = 0; r < R; r++) seed_rep(a, r);
      for (int t = 0; t < T0; t++) { step(a, b); u64 *x = a; a = b; b = x; }
      for (int j = 0; j < ncl; j++) memset(a + (size_t)cl[j] * W, 0, 64);
      for (int t = 0; t <= TMAX; t++) {
        for (int j = 0; j < nw; j++) fwrite(a + (size_t)F[0].c[j] * W, 8, W, o);
        step(a, b); u64 *x = a; a = b; b = x; }
    }
    fclose(o); return 0;
  }
  /* run */
  sm = strtoull(argv[3], 0, 10) * 0x2545F4914F6CDD1DULL + 12345; double p = atof(argv[4]); thr = (u64)(p * 18446744073709551616.0);
  long GENS = atol(argv[5]); long T0 = atol(argv[6]); int PBAR = atoi(argv[7]); int H = atoi(argv[8]); long MAXREC = atol(argv[9]);
  char path[4096]; snprintf(path, sizeof path, "%s.rec", argv[10]); FILE *rec = fopen(path, "wb");
  int na = F[0].na, nu = F[0].nu; for (int f = 0; f < nf; f++) if (F[f].na != na || F[f].nu != nu) { fprintf(stderr, "faces differ\n"); return 1; }
  if (T0 < H + 2 || na > 127) { fprintf(stderr, "need T0 > H + 1 and na < 128\n"); return 1; }
  size_t ST = (size_t)n * W;
  u64 *hist = malloc(8 * ST * H), *snaps = calloc(ST * NS, 8);
  long *age = calloc(R, sizeof(long)); int nlive = 0; u64 agemask[W]; memset(agemask, 0, sizeof agemask);
  unsigned char *armed = calloc((size_t)nf * R, 1), *inx = calloc((size_t)nf * R, 1), *minp = calloc((size_t)nf * R, 1), *endl = calloc(R, 1);
  long *xstart = calloc((size_t)nf * R, sizeof(long));
  double expo = 0; long deaths = 0, unarmed = 0, nWl = 0, nSl = 0, nrec = 0, nFW = 0;
  double *hP = calloc(na + 1, 8), *xrec = calloc(na + 1, 8), *xcen = calloc(na + 1, 8), *occ = calloc((size_t)nf * (na + nu), 8), occden = 0;
  int nba = (na + 7) / 8, nbu = (nu + 7) / 8; unsigned char *row = malloc(nba + nbu + 1);
  for (int r = 0; r < R; r++) seed_rep(a, r);
  for (long g = 1; g <= GENS; g++) {
    step(a, b); { u64 *x = a; a = b; b = x; }
    for (int r = 0; r < R; r++) if (++age[r] == T0 + 1) { nlive++; agemask[r >> 6] |= 1ULL << (r & 63); }
    memcpy(hist + ST * (g % H), a, 8 * ST);
    expo += nlive;
    for (int f = 0; f < nf; f++) {
      const int *fc = F[f].c;
      for (int w = 0; w < W; w++) {
        u64 c[7] = {0, 0, 0, 0, 0, 0, 0}, orr = 0;
        for (int j = 0; j < na; j++) { u64 v = a[(size_t)fc[j] * W + w]; orr |= v;
          for (int k = 0; k < 7 && v; k++) { u64 t = c[k] & v; c[k] ^= v; v = t; } }
        u64 live = agemask[w];
        for (int bit = 0; bit < 64; bit++) {
          int r = w * 64 + bit; if (!(live >> bit & 1)) continue;
          int P = 0; for (int k = 0; k < 7; k++) P |= (int)(c[k] >> bit & 1) << k;
          hP[P] += 1; size_t ix = (size_t)f * R + r;
          if (!inx[ix]) { if (P >= PBAR) armed[ix] = 1; else if (armed[ix]) { inx[ix] = 1; minp[ix] = P; xstart[ix] = g; } }
          else { if (P < minp[ix]) minp[ix] = P; if (P >= PBAR) { xrec[minp[ix]] += 1; inx[ix] = 0; } }
        }
        u64 emp = ~orr;
        while (emp) { int bit = __builtin_ctzll(emp); emp &= emp - 1; int r = w * 64 + bit; endl[r] = 1;
          if (age[r] <= T0) continue;
          deaths++; size_t ix = (size_t)f * R + r; if (!inx[ix]) unarmed++;
          if (nrec < MAXREC) {
            u64 fw[W]; firewalls(a, fw); int64_t hd[6] = {r, f, age[r], g, (int64_t)(fw[w] >> bit & 1), inx[ix] ? g - xstart[ix] : -1};
            if (hd[4]) nFW++;
            fwrite(hd, 8, 6, rec);
            for (int j = 0; j < H; j++) { const u64 *s = hist + ST * ((g - j) % H); memset(row, 0, nba + nbu);
              for (int q = 0; q < na; q++) if (s[(size_t)fc[q] * W + w] >> bit & 1) row[q >> 3] |= 1 << (q & 7);
              for (int q = 0; q < nu; q++) if (s[(size_t)fc[na + q] * W + w] >> bit & 1) row[nba + (q >> 3)] |= 1 << (q & 7);
              fwrite(row, 1, nba + nbu, rec); }
            nrec++; }
        }
      }
    }
    if (g % 16 == 0) { occden += nlive;
      for (int f = 0; f < nf; f++) for (int j = 0; j < na + nu; j++) { const u64 *s = a + (size_t)F[f].c[j] * W; long cnt = 0;
        for (int w = 0; w < W; w++) cnt += __builtin_popcountll(s[w] & agemask[w]); occ[(size_t)f * (na + nu) + j] += cnt; } }
    if (ng && g % 64 == 0) { u64 fw[W]; firewalls(a, fw);
      for (int r = 0; r < R; r++) if (!endl[r] && (fw[r >> 6] >> (r & 63) & 1)) { endl[r] = 2; if (age[r] > T0) nWl++; } }
    if (g % 840 == 0) { long q = g / 840;
      for (int m = 1; m < NS && m <= q; m++) { const u64 *s = snaps + ST * ((q - m) % NS); u64 d[W]; memset(d, 0, sizeof d);
        for (size_t i = 0; i < ST; i++) d[i % W] |= a[i] ^ s[i];
        for (int r = 0; r < R; r++) if (!endl[r] && age[r] >= 840L * m && !(d[r >> 6] >> (r & 63) & 1)) { endl[r] = 3;
          if (age[r] > T0) { nSl++; long back = 840L * m; if (back > age[r] - T0) back = age[r] - T0; expo -= back; } } }
      memcpy(snaps + ST * (q % NS), a, 8 * ST); }
    for (int r = 0; r < R; r++) if (endl[r]) {
      for (int f = 0; f < nf; f++) { size_t ix = (size_t)f * R + r; if (inx[ix] && !(endl[r] == 1 && minp[ix] == 0)) xcen[minp[ix]] += 1; inx[ix] = 0; armed[ix] = 0; }
      if (age[r] > T0) { nlive--; agemask[r >> 6] &= ~(1ULL << (r & 63)); }
      seed_rep(a, r); age[r] = 0; endl[r] = 0; }
  }
  fclose(rec);
  snprintf(path, sizeof path, "%s.sum", argv[10]); FILE *o = fopen(path, "w");
  fprintf(o, "n %d nf %d na %d nu %d gens %ld T0 %ld PBAR %d H %d seed %s p %s\n", n, nf, na, nu, GENS, T0, PBAR, H, argv[3], argv[4]);
  fprintf(o, "exposure %.0f deaths %ld unarmed %ld W %ld S %ld records %ld firewall_at_death %ld\n", expo, deaths, unarmed, nWl, nSl, nrec, nFW);
  fprintf(o, "lntau %.4f err %.4f\n", log(nf * expo / (deaths ? deaths : 1)), 1 / sqrt(deaths ? deaths : 1));
  fprintf(o, "histP"); for (int k = 0; k <= na; k++) fprintf(o, " %.0f", hP[k]); fprintf(o, "\n");
  fprintf(o, "xrec"); for (int k = 0; k <= na; k++) fprintf(o, " %.0f", xrec[k]); fprintf(o, "\n");
  fprintf(o, "xcen"); for (int k = 0; k <= na; k++) fprintf(o, " %.0f", xcen[k]); fprintf(o, "\n");
  fprintf(o, "occden %.0f\n", occden);
  for (int f = 0; f < nf; f++) { fprintf(o, "occ %d", f); for (int j = 0; j < na + nu; j++) fprintf(o, " %.0f", occ[(size_t)f * (na + nu) + j]); fprintf(o, "\n"); }
  fclose(o);
  printf("lntau %.4f +- %.4f  deaths %ld  exposure %.3e  W %ld S %ld unarmed %ld\n", log(nf * expo / (deaths ? deaths : 1)), 1 / sqrt(deaths ? deaths : 1), deaths, expo, nWl, nSl, unarmed);
  return 0;
}
