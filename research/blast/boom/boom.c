/* boom.c (research/blast/boom): boom and bust of a face, measured in two factors.
 * Bit-sliced gump (B45/S345), 512 replicas, on a cell graph written by geom.py. The kernel (rule8, step,
 * readgraph, trace) is the one of ../anatomy/an.c; it is validated here again by validate.py on every vessel.
 *
 *   boom GRAPH trace INIT T OUT                      (validation; see validate.py)
 *   boom GRAPH run SEED DENS GENS T0 P0 MRES OUT
 *       renewal lives from soups of density DENS; a life ends when a face is empty; statistics at age > T0 >= 34.
 *       OUT.sum   text summary;  OUT.M  doubles [(na+1)^2]: counts of face-generations P(t-1) -> P(t)
 *       OUT.G2    doubles [(na+1)^2][3]: by (P(t-2), P(t-1)): count, sum P(t), sum P(t)^2
 *       OUT.GU    doubles [(na+1)(nu+1)][6]: by (P, U)(t-1): count, sum P', sum U', sum P'^2, sum U'^2, sum P'U'
 *       OUT.M3    doubles [(na+1)^3]: counts P(t-2), P(t-1) -> P(t);  OUT.M4 (na <= 64) uint32 [(na+1)(nu+1)]^2:
 *                 counts (P, U)(t-1) -> (P, U)(t), U = population of the layer beneath the face
 *                 (M3 and M4 were added at 04:08 UTC; the runs of run_a.sh and run_b.sh used the binary without them)
 *       OUT.deaths text: one line per death: face age then P(t-1..t-32) then U(t-1..t-32)
 *       OUT.par   parents: for each population p >= P0 a uniform reservoir of MRES states with P = p:
 *                 header int32 {nrec, recsize, n, HL}; record = packed state, face, P, P(t-1..t-32), U(t-1..t-32)
 *   boom GRAPH clone PAR DEEP K H SEED OUT
 *       every parent K times: clone 0 untouched, clones 1..K-1 with one flipped cell each (distinct cells of DEEP);
 *       H generations. OUT.txt: 'p idx face P ndead' per parent, 'd idx clone k P(1..k)' per clone whose face is empty
 *       at generation k <= H; 'b P k type n sum sumsq' moments of P(t+k), type 0 = untouched, 1 = flipped.
 *       OUT.Mc doubles [12][(na+1)^2]: transitions P(t+k) -> P(t+k+1) of all clones, k = 0..11.
 *
 *   gcc -O3 -march=native -o boom boom.c -lm
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
#define HL 32
static u64 sm;
static inline u64 rnd(void) { u64 z = (sm += 0x9e3779b97f4a7c15ULL); z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
  z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; return z ^ (z >> 31); }
static int rdi(FILE *f) { int32_t x; if (fread(&x, 4, 1, f) != 1) { fprintf(stderr, "short read\n"); exit(1); } return x; }

#define FA(s, c, x, y, z) do { v8 t_ = (x) ^ (y); s = t_ ^ (z); c = ((x) & (y)) | (t_ & (z)); } while (0)
static inline v8 rule8(const v8 *x, v8 me) {
  v8 s1, c1, s2, c2, s3, c3, s4, c4, S, C, b0, Hh, t1, d1, t2, d2, b1, e, b2, b3;
  FA(s1, c1, x[0], x[1], x[2]); FA(s2, c2, x[3], x[4], x[5]); FA(s3, c3, x[6], x[7], x[8]); FA(s4, c4, x[9], x[10], x[11]);
  FA(S, C, s1, s2, s3); b0 = S ^ s4; Hh = S & s4;
  FA(t1, d1, c1, c2, c3); FA(t2, d2, c4, C, Hh); b1 = t1 ^ t2; e = t1 & t2;
  FA(b2, b3, d1, d2, e);
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
static void readgraph(const char *path) {
  FILE *f = fopen(path, "rb"); if (!f) { perror(path); exit(1); }
  n = rdi(f); nb = malloc(4 * 12 * (size_t)n);
  for (int i = 0; i < 12 * n; i++) { int x = rdi(f); nb[i] = x < 0 ? n : x; }
  nf = rdi(f); F = malloc(sizeof(face) * nf);
  for (int k = 0; k < nf; k++) { int na = rdi(f); int *c = malloc(4 * 4096); for (int j = 0; j < na; j++) c[j] = rdi(f);
    int nu = rdi(f); for (int j = 0; j < nu; j++) c[na + j] = rdi(f); F[k].na = na; F[k].nu = nu; F[k].c = c; }
  fclose(f);
}
static u64 thr;
static void seed_rep(u64 *a, int r) { u64 bit = 1ULL << (r & 63); int w = r >> 6;
  for (int i = 0; i < n; i++) { if (rnd() < thr) a[(size_t)i * W + w] |= bit; else a[(size_t)i * W + w] &= ~bit; } }
/* population of the m cells c[] in every replica */
static void popc(const u64 *a, const int *c, int m, unsigned char *out) {
  for (int w = 0; w < W; w++) {
    u64 k[8] = {0, 0, 0, 0, 0, 0, 0, 0};
    for (int j = 0; j < m; j++) { u64 v = a[(size_t)c[j] * W + w]; for (int q = 0; q < 8 && v; q++) { u64 t = k[q] & v; k[q] ^= v; v = t; } }
    for (int bit = 0; bit < 64; bit++) { int P = 0; for (int q = 0; q < 8; q++) P |= (int)(k[q] >> bit & 1) << q; out[w * 64 + bit] = (unsigned char)P; }
  }
}

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: see header\n"); return 1; }
  readgraph(argv[1]);
  size_t SZ = (size_t)(n + 1) * W * 8, ST = (size_t)n * W;
  u64 *a = aligned_alloc(64, SZ), *b = aligned_alloc(64, SZ); memset(a, 0, SZ); memset(b, 0, SZ);
  int na = F[0].na, nu = F[0].nu, nbt = (n + 7) / 8;
  char path[4096];
  if (!strcmp(argv[2], "trace")) {
    int T = atoi(argv[4]); sm = 777; thr = (u64)(0.4 * 18446744073709551616.0);
    for (int r = 0; r < R; r++) seed_rep(a, r);
    for (int i = 0; i < n; i++) a[(size_t)i * W] &= ~1ULL;
    FILE *g = fopen(argv[3], "r"); int c; while (fscanf(g, "%d", &c) == 1) a[(size_t)c * W] |= 1ULL; fclose(g);
    FILE *o = fopen(argv[5], "wb"); unsigned char *buf = malloc(nbt);
    for (int t = 0; t <= T; t++) {
      memset(buf, 0, nbt); for (int i = 0; i < n; i++) if (a[(size_t)i * W] & 1ULL) buf[i >> 3] |= 1 << (i & 7);
      fwrite(buf, 1, nbt, o);
      step(a, b); u64 *x = a; a = b; b = x; }
    fclose(o); return 0;
  }
  int recsize = nbt + 2 + 2 * HL;
  if (!strcmp(argv[2], "run")) {
    sm = strtoull(argv[3], 0, 10) * 0x2545F4914F6CDD1DULL + 12345; double dens = atof(argv[4]); thr = (u64)(dens * 18446744073709551616.0);
    long GENS = atol(argv[5]), T0 = atol(argv[6]); int P0 = atoi(argv[7]), MRES = atoi(argv[8]);
    if (T0 < HL + 2) { fprintf(stderr, "T0 >= 34\n"); return 1; }
    for (int f = 0; f < nf; f++) if (F[f].na != na || F[f].nu != nu) { fprintf(stderr, "faces differ\n"); return 1; }
    int NA = na + 1, NU = nu + 1;
    double *M = calloc((size_t)NA * NA, 8), *G2 = calloc((size_t)NA * NA * 3, 8), *GU = calloc((size_t)NA * NU * 6, 8);
    double *M3 = calloc((size_t)NA * NA * NA, 8);                                   /* [P(t-2)][P(t-1)][P(t)] */
    uint32_t *M4 = na <= 64 ? calloc((size_t)NA * NU * NA * NU, 4) : NULL;          /* [P(t-1)][U(t-1)][P(t)][U(t)] */
    unsigned char *hp = calloc((size_t)nf * R * HL, 1), *hu = calloc((size_t)nf * R * HL, 1), *Pn = malloc((size_t)nf * R), *Un = malloc((size_t)nf * R);
    long *age = calloc(R, sizeof(long)); long deaths = 0, nS = 0; double expoF = 0;
    int NP = na - P0 + 1; double *rc = calloc(NP, 8); unsigned char *res = calloc((size_t)NP * MRES, recsize);
    u64 *snap = calloc(ST, 8);
    snprintf(path, sizeof path, "%s.deaths", argv[9]); FILE *fd = fopen(path, "w");
    for (int r = 0; r < R; r++) seed_rep(a, r);
    for (long g = 1; g <= GENS; g++) {
      step(a, b); { u64 *x = a; a = b; b = x; }
      for (int f = 0; f < nf; f++) { popc(a, F[f].c, na, Pn + (size_t)f * R); popc(a, F[f].c + na, nu, Un + (size_t)f * R); }
      int i1 = (int)((g - 1) % HL), i2 = (int)((g - 2 + HL) % HL), i0 = (int)(g % HL);
      for (int r = 0; r < R; r++) {
        age[r]++; int dead = 0;
        for (int f = 0; f < nf; f++) {
          size_t ix = ((size_t)f * R + r) * HL; int P = Pn[(size_t)f * R + r], U = Un[(size_t)f * R + r];
          if (age[r] > T0) {
            int p1 = hp[ix + i1], p2 = hp[ix + i2], u1 = hu[ix + i1];
            expoF += 1; M[(size_t)p1 * NA + P] += 1;
            M3[((size_t)p2 * NA + p1) * NA + P] += 1; if (M4) M4[(((size_t)p1 * NU + u1) * NA + P) * NU + U]++;
            double *q = G2 + ((size_t)p2 * NA + p1) * 3; q[0] += 1; q[1] += P; q[2] += (double)P * P;
            q = GU + ((size_t)p1 * NU + u1) * 6; q[0] += 1; q[1] += P; q[2] += U; q[3] += (double)P * P; q[4] += (double)U * U; q[5] += (double)P * U;
            if (P == 0) { deaths++; fprintf(fd, "%d %ld", f, age[r]);
              for (int j = 1; j <= HL; j++) fprintf(fd, " %d", hp[ix + (g - j) % HL]);
              for (int j = 1; j <= HL; j++) fprintf(fd, " %d", hu[ix + (g - j) % HL]);
              fprintf(fd, "\n"); }
            else if (P >= P0) {
              int k = P - P0; rc[k] += 1; long slot = -1;
              if (rc[k] <= MRES) slot = (long)rc[k] - 1; else { u64 x = rnd() % (u64)rc[k]; if (x < (u64)MRES) slot = (long)x; }
              if (slot >= 0) { unsigned char *rec = res + ((size_t)k * MRES + slot) * recsize; memset(rec, 0, recsize);
                int w = r >> 6, bit = r & 63;
                for (int i = 0; i < n; i++) if (a[(size_t)i * W + w] >> bit & 1) rec[i >> 3] |= 1 << (i & 7);
                rec[nbt] = (unsigned char)f; rec[nbt + 1] = (unsigned char)P;
                for (int j = 1; j <= HL; j++) { rec[nbt + 1 + j] = hp[ix + (g - j) % HL]; rec[nbt + 1 + HL + j] = hu[ix + (g - j) % HL]; } }
            }
          }
          hp[ix + i0] = (unsigned char)P; hu[ix + i0] = (unsigned char)U; if (P == 0) dead = 1;
        }
        if (dead) { seed_rep(a, r); age[r] = 0; }
      }
      if (g % 840 == 0) {   /* a replica whose state repeats after 840 generations is not chaos any more: restart it */
        u64 d[W]; memset(d, 0, sizeof d); for (size_t i = 0; i < ST; i++) d[i % W] |= a[i] ^ snap[i];
        for (int r = 0; r < R; r++) if (age[r] >= 840 && !(d[r >> 6] >> (r & 63) & 1)) { nS++; seed_rep(a, r); age[r] = 0; }
        memcpy(snap, a, 8 * ST); }
    }
    fclose(fd);
    snprintf(path, sizeof path, "%s.M", argv[9]); FILE *o = fopen(path, "wb"); fwrite(M, 8, (size_t)NA * NA, o); fclose(o);
    snprintf(path, sizeof path, "%s.M3", argv[9]); o = fopen(path, "wb"); fwrite(M3, 8, (size_t)NA * NA * NA, o); fclose(o);
    if (M4) { snprintf(path, sizeof path, "%s.M4", argv[9]); o = fopen(path, "wb"); fwrite(M4, 4, (size_t)NA * NU * NA * NU, o); fclose(o); }
    snprintf(path, sizeof path, "%s.G2", argv[9]); o = fopen(path, "wb"); fwrite(G2, 8, (size_t)NA * NA * 3, o); fclose(o);
    snprintf(path, sizeof path, "%s.GU", argv[9]); o = fopen(path, "wb"); fwrite(GU, 8, (size_t)NA * NU * 6, o); fclose(o);
    snprintf(path, sizeof path, "%s.par", argv[9]); o = fopen(path, "wb"); int32_t nrec = 0;
    for (int k = 0; k < NP; k++) nrec += (int32_t)(rc[k] < MRES ? rc[k] : MRES);
    int32_t hd[4] = {nrec, recsize, n, HL}; fwrite(hd, 4, 4, o);
    for (int k = 0; k < NP; k++) { long m = (long)(rc[k] < MRES ? rc[k] : MRES); fwrite(res + (size_t)k * MRES * recsize, recsize, m, o); }
    fclose(o);
    snprintf(path, sizeof path, "%s.sum", argv[9]); o = fopen(path, "w");
    fprintf(o, "n %d nf %d na %d nu %d gens %ld T0 %ld P0 %d MRES %d seed %s dens %s\n", n, nf, na, nu, GENS, T0, P0, MRES, argv[3], argv[4]);
    fprintf(o, "expoF %.0f deaths %ld settled %ld parents %d\n", expoF, deaths, nS, nrec);
    fprintf(o, "lntau %.4f err %.4f\n", log(expoF / (deaths ? deaths : 1)), 1 / sqrt(deaths ? deaths : 1));
    fclose(o);
    printf("lntau %.4f +- %.4f deaths %ld expoF %.3e settled %ld parents %d\n", log(expoF / (deaths ? deaths : 1)), 1 / sqrt(deaths ? deaths : 1), deaths, expoF, nS, nrec);
    return 0;
  }
  if (!strcmp(argv[2], "clone")) {
    FILE *fp = fopen(argv[3], "rb"); int32_t hd[4]; if (fread(hd, 4, 4, fp) != 4) return 1;
    int nrec = hd[0]; if (hd[1] != recsize || hd[2] != n) { fprintf(stderr, "parents do not fit the graph\n"); return 1; }
    unsigned char *par = malloc((size_t)nrec * recsize); if (fread(par, recsize, nrec, fp) != (size_t)nrec) return 1; fclose(fp);
    int *deep = malloc(4 * (size_t)n), nd = 0; FILE *g = fopen(argv[4], "r"); int c; while (fscanf(g, "%d", &c) == 1) deep[nd++] = c; fclose(g);
    int K = atoi(argv[5]), H = atoi(argv[6]); sm = strtoull(argv[7], 0, 10) * 0x2545F4914F6CDD1DULL + 999;
    if (K - 1 > nd || R % K || H > 64) { fprintf(stderr, "K - 1 <= deep cells, K | 512, H <= 64\n"); return 1; }
    int NA = na + 1, PB = R / K;
    double *Mc = calloc((size_t)12 * NA * NA, 8), *bm = calloc((size_t)NA * 13 * 2 * 3, 8);
    unsigned char *Pn = malloc((size_t)nf * R), *traj = malloc((size_t)R * (H + 1)); int *dk = malloc(4 * R);
    snprintf(path, sizeof path, "%s.txt", argv[8]); FILE *o = fopen(path, "w");
    for (int base = 0; base < nrec; base += PB) {
      int np = nrec - base < PB ? nrec - base : PB;
      memset(a, 0, SZ);
      for (int j = 0; j < np; j++) { const unsigned char *rec = par + (size_t)(base + j) * recsize;
        for (int i = 0; i < n; i++) if (rec[i >> 3] >> (i & 7) & 1) for (int q = 0; q < K; q++) { int r = j * K + q; a[(size_t)i * W + (r >> 6)] |= 1ULL << (r & 63); }
        for (int q = 1; q < K; q++) { int t = q - 1 + (int)(rnd() % (u64)(nd - (q - 1))); int x = deep[t]; deep[t] = deep[q - 1]; deep[q - 1] = x;
          int r = j * K + q; a[(size_t)x * W + (r >> 6)] ^= 1ULL << (r & 63); }
        for (int q = 0; q < K; q++) { traj[(size_t)(j * K + q) * (H + 1)] = rec[nbt + 1]; dk[j * K + q] = 0; } }
      for (int k = 1; k <= H; k++) {
        step(a, b); { u64 *x = a; a = b; b = x; }
        for (int f = 0; f < nf; f++) popc(a, F[f].c, na, Pn + (size_t)f * R);
        for (int j = 0; j < np; j++) { const unsigned char *rec = par + (size_t)(base + j) * recsize; int f = rec[nbt], P0p = rec[nbt + 1];
          for (int q = 0; q < K; q++) { int r = j * K + q; if (dk[r]) continue; int P = Pn[(size_t)f * R + r]; unsigned char *tr = traj + (size_t)r * (H + 1);
            tr[k] = (unsigned char)P; if (k <= 12) { Mc[((size_t)(k - 1) * NA + tr[k - 1]) * NA + P] += 1;
              double *x = bm + (((size_t)P0p * 13 + k) * 2 + (q > 0)) * 3; x[0] += 1; x[1] += P; x[2] += (double)P * P; }
            if (P == 0) dk[r] = k; } }
      }
      for (int j = 0; j < np; j++) { const unsigned char *rec = par + (size_t)(base + j) * recsize; int nd_ = 0;
        for (int q = 0; q < K; q++) if (dk[j * K + q]) nd_++;
        fprintf(o, "p %d %d %d %d\n", base + j, rec[nbt], rec[nbt + 1], nd_);
        for (int q = 0; q < K; q++) { int r = j * K + q; if (!dk[r]) continue; fprintf(o, "d %d %d %d", base + j, q, dk[r]);
          for (int k = 1; k <= dk[r]; k++) fprintf(o, " %d", traj[(size_t)r * (H + 1) + k]); fprintf(o, "\n"); } }
    }
    for (int P = 0; P < NA; P++) for (int k = 1; k <= 12; k++) for (int ty = 0; ty < 2; ty++) { double *x = bm + (((size_t)P * 13 + k) * 2 + ty) * 3;
      if (x[0] > 0) fprintf(o, "b %d %d %d %.0f %.0f %.0f\n", P, k, ty, x[0], x[1], x[2]); }
    fclose(o);
    snprintf(path, sizeof path, "%s.Mc", argv[8]); o = fopen(path, "wb"); fwrite(Mc, 8, (size_t)12 * NA * NA, o); fclose(o);
    return 0;
  }
  if (!strcmp(argv[2], "island")) {
    /* boom GRAPH island PAR H SEED PMIN PMAX OUT: every parent with PMIN <= P <= PMAX is stepped once (the bust). The live
     * cells of its face then fall into clusters (connected through the 6 in-layer neighbours). Replicas: the bust state
     * untouched, and one per cluster with every other cell of that face killed (the layers beneath untouched).
     * Each is run until its face is empty (outcome 0) or has >= L = ceil(A/2) cells (1), at most H generations (2).
     * OUT: 'i idx P q U ncl out0 t0  size:out:t ...' (q, U: face and layer beneath after the bust). */
    FILE *fp = fopen(argv[3], "rb"); int32_t hd[4]; if (fread(hd, 4, 4, fp) != 4) return 1;
    int nrec = hd[0]; if (hd[1] != recsize || hd[2] != n) { fprintf(stderr, "parents do not fit the graph\n"); return 1; }
    unsigned char *par = malloc((size_t)nrec * recsize); if (fread(par, recsize, nrec, fp) != (size_t)nrec) return 1; fclose(fp);
    int H = atoi(argv[4]), PMIN = atoi(argv[6]), PMAX = atoi(argv[7]), L = (na + 1) / 2; (void)argv[5];
    int *sel = malloc(4 * (size_t)nrec), nsel = 0; for (int i = 0; i < nrec; i++) { int P = par[(size_t)i * recsize + nbt + 1]; if (P >= PMIN && P <= PMAX) sel[nsel++] = i; }
    unsigned char *B = malloc((size_t)R * n), *Pn = malloc((size_t)nf * R), *Un = malloc((size_t)nf * R);
    int *cl = malloc(4 * (size_t)R * na), *ncl = malloc(4 * R), *csz = malloc(4 * (size_t)R * na), *fid = malloc(4 * (size_t)(n + 1)), *stk = malloc(4 * (size_t)na);
    int *qp = malloc(4 * R), *qc = malloc(4 * R), *oc = malloc(4 * R), *ot = malloc(4 * R);
    FILE *o = fopen(argv[8], "w");
    for (int base = 0; base < nsel; base += R) {
      int np = nsel - base < R ? nsel - base : R;
      memset(a, 0, SZ);
      for (int j = 0; j < np; j++) { const unsigned char *rec = par + (size_t)sel[base + j] * recsize;
        for (int i = 0; i < n; i++) if (rec[i >> 3] >> (i & 7) & 1) a[(size_t)i * W + (j >> 6)] |= 1ULL << (j & 63); }
      step(a, b); { u64 *x = a; a = b; b = x; }
      for (int f = 0; f < nf; f++) { popc(a, F[f].c, na, Pn + (size_t)f * R); popc(a, F[f].c + na, nu, Un + (size_t)f * R); }
      for (int j = 0; j < np; j++) for (int i = 0; i < n; i++) B[(size_t)j * n + i] = (unsigned char)(a[(size_t)i * W + (j >> 6)] >> (j & 63) & 1);
      unsigned char *qq = malloc(np), *uu = malloc(np);
      for (int j = 0; j < np; j++) { const unsigned char *rec = par + (size_t)sel[base + j] * recsize; int f = rec[nbt];
        qq[j] = Pn[(size_t)f * R + j]; uu[j] = Un[(size_t)f * R + j];
        for (int i = 0; i <= n; i++) fid[i] = -1; for (int q = 0; q < na; q++) fid[F[f].c[q]] = q;
        int *c = cl + (size_t)j * na; for (int q = 0; q < na; q++) c[q] = -1; int nc = 0;
        for (int q = 0; q < na; q++) { if (c[q] >= 0 || !B[(size_t)j * n + F[f].c[q]]) continue; int sp = 0, sz = 0; stk[sp++] = q; c[q] = nc;
          while (sp) { int x = stk[--sp]; sz++; const int *nn = nb + 12 * (size_t)F[f].c[x];
            for (int t = 0; t < 12; t++) { int y = fid[nn[t]]; if (y >= 0 && c[y] < 0 && B[(size_t)j * n + F[f].c[y]]) { c[y] = nc; stk[sp++] = y; } } }
          csz[(size_t)j * na + nc] = sz; nc++; }
        ncl[j] = nc; }
      int j0 = 0;
      while (j0 < np) {
        int nq = 0, j1 = j0; while (j1 < np && nq + 1 + ncl[j1] <= R) { qp[nq] = j1; qc[nq++] = -1; for (int c = 0; c < ncl[j1]; c++) { qp[nq] = j1; qc[nq++] = c; } j1++; }
        if (j1 == j0) { fprintf(stderr, "too many clusters\n"); return 1; }
        memset(a, 0, SZ);
        for (int r = 0; r < nq; r++) { int j = qp[r]; const unsigned char *rec = par + (size_t)sel[base + j] * recsize; int f = rec[nbt];
          for (int i = 0; i <= n; i++) fid[i] = -1; for (int q = 0; q < na; q++) fid[F[f].c[q]] = q;
          for (int i = 0; i < n; i++) { if (!B[(size_t)j * n + i]) continue; if (qc[r] >= 0 && fid[i] >= 0 && cl[(size_t)j * na + fid[i]] != qc[r]) continue;
            a[(size_t)i * W + (r >> 6)] |= 1ULL << (r & 63); }
          oc[r] = 2; ot[r] = H; if (qc[r] < 0 && qq[j] >= L) { oc[r] = 1; ot[r] = 0; } if (qc[r] < 0 && qq[j] == 0) { oc[r] = 0; ot[r] = 0; } }
        for (int k = 1; k <= H; k++) {
          step(a, b); { u64 *x = a; a = b; b = x; }
          for (int f = 0; f < nf; f++) popc(a, F[f].c, na, Pn + (size_t)f * R);
          for (int r = 0; r < nq; r++) { if (oc[r] != 2) continue; int f = par[(size_t)sel[base + qp[r]] * recsize + nbt]; int P = Pn[(size_t)f * R + r];
            if (P == 0) { oc[r] = 0; ot[r] = k; } else if (P >= L) { oc[r] = 1; ot[r] = k; } } }
        for (int r = 0; r < nq; ) { int j = qp[r]; const unsigned char *rec = par + (size_t)sel[base + j] * recsize;
          fprintf(o, "i %d %d %d %d %d %d %d ", sel[base + j], rec[nbt + 1], qq[j], uu[j], ncl[j], oc[r], ot[r]); r++;
          for (int c = 0; c < ncl[j]; c++, r++) fprintf(o, " %d:%d:%d", csz[(size_t)j * na + c], oc[r], ot[r]);
          fprintf(o, "\n"); }
        j0 = j1; }
      free(qq); free(uu);
    }
    fclose(o); return 0;
  }
  fprintf(stderr, "unknown mode\n"); return 1;
}
