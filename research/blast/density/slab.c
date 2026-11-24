/* slab.c (research/blast/density, third task, item 4): gump on a slab torus (slabgeom.py), 512 lanes bit-sliced, the
 * watched face = layer 0; optionally every cell of layers >= L a fresh coin of bias p every generation (full
 * replacement, bit-serial as in nzd.c, second stream from a hash of the seed).
 *
 *   slab GEOM brute SEED GENS L P      L = 8: gump (no coins); a life ends when layer 0 or layer 7 is empty. L < 8:
 *                                      layers L..7 are coins; a life ends when layer 0 is empty.
 *      512 lanes, soup 0.35 on every cell (coins replace theirs at once), 200 generations of ageing-in, the hull
 *      protocol of nz.c: a hull-generation counts when the age after the step exceeds 200. Prints exposure, deaths of
 *      the watched face (alone or tied), mean face population, the excursion counts (REC, as nzd.c: H = round(A/4)),
 *      and LAYER1: the density of layer 1 overall and given face population <= 20, 15, 10, 6, 4, 2.
 *   -DLIB: the stepper for validate_slab.py.
 */
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef uint64_t u64;
#define W 8
#define NL (64 * W)
#define NB 10
#define T0 200
typedef u64 vec __attribute__((vector_size(64), aligned(8)));
static int n, A, *nb;
static u64 *a, *b, sm, sm2;
static inline u64 fin64(u64 z) { z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL; z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; return z ^ (z >> 31); }
static inline u64 rnd(void) { return fin64(sm += 0x9e3779b97f4a7c15ULL); }
static inline u64 rnd2(void) { return fin64(sm2 += 0x9e3779b97f4a7c15ULL); }
int geom_load(const char *path) {
  FILE *f = fopen(path, "rb"); if (!f) return -1; int hd[2]; if (fread(hd, 4, 2, f) != 2) return -1; n = hd[0]; A = hd[1];
  nb = malloc(sizeof(int) * 12 * n); if (fread(nb, 4, (size_t)12 * n, f) != (size_t)12 * n) return -1; fclose(f);
  a = aligned_alloc(64, (size_t)(n + 1) * W * 8); b = aligned_alloc(64, (size_t)(n + 1) * W * 8);
  memset(a, 0, (size_t)(n + 1) * W * 8); memset(b, 0, (size_t)(n + 1) * W * 8); return n;
}
#define FA(s, c, p, q, r) do { vec t_ = (p) ^ (q); s = t_ ^ (r); c = ((p) & (q)) | (t_ & (r)); } while (0)
static inline vec rule(const vec *x, vec me) {
  vec s0, c0, s1, c1, s2, c2, s3, c3, u, cu, b0, cv, p, cp, q, cq, b1, cw, b2, b3;
  FA(s0, c0, x[0], x[1], x[2]); FA(s1, c1, x[3], x[4], x[5]); FA(s2, c2, x[6], x[7], x[8]); FA(s3, c3, x[9], x[10], x[11]);
  FA(u, cu, s0, s1, s2); b0 = u ^ s3; cv = u & s3;
  FA(p, cp, c0, c1, c2); FA(q, cq, c3, cu, cv); b1 = p ^ q; cw = p & q;
  FA(b2, b3, cp, cq, cw);
  return ~b3 & ((b2 & ~b1) | (me & ~b2 & b1 & b0));
}
void step(void) {
  for (int i = 0; i < n; i++) { const int *q = nb + 12 * (size_t)i; vec x[12], me, o;
    for (int t = 0; t < 12; t++) memcpy(&x[t], a + (size_t)q[t] * W, 64);
    memcpy(&me, a + (size_t)i * W, 64); o = rule(x, me); memcpy(b + (size_t)i * W, &o, 64); }
  u64 *t = a; a = b; b = t;
}
static int L = 8; static u64 thr = 0, lthr[8];   /* lthr[l]: the bias of layer l's coins (layers >= L) */
static inline u64 bword(u64 th) { if (th >= 65536) return ~0ULL; u64 r = 0;
  for (int i = 0; i < 16; i++) { u64 z = rnd2(); r = ((th >> i) & 1) ? (z | r) : (z & r); } return r; }
void coins(void) { for (int i = L * A; i < n; i++) { u64 th = lthr[i / A]; for (int w = 0; w < W; w++) a[(size_t)i * W + w] = bword(th); } }
static void count(int lo, int hi, int *out) {     /* per-lane population of cells [lo, hi) */
  vec cc[NB]; for (int k = 0; k < NB; k++) cc[k] = (vec){0};
  for (int i = lo; i < hi; i++) { vec x; memcpy(&x, a + (size_t)i * W, 64); for (int k = 0; k < NB; k++) { vec t = cc[k] & x; cc[k] ^= x; x = t; } }
  u64 c[NB][W]; for (int k = 0; k < NB; k++) memcpy(c[k], &cc[k], 64);
  for (int l = 0; l < NL; l++) { int p = 0; for (int k = 0; k < NB; k++) p |= (int)((c[k][l >> 6] >> (l & 63)) & 1) << k; out[l] = p; }
}
static void soup(int lane) { u64 bit = 1ULL << (lane & 63), th = (u64)(0.35 * 18446744073709551616.0);
  for (int i = 0; i < n; i++) { u64 *x = a + (size_t)i * W + (lane >> 6); if (rnd() < th) *x |= bit; else *x &= ~bit; } }
#ifdef LIB
void v_set(int lane, const uint8_t *c) { for (int i = 0; i < n; i++) { u64 *p = a + (size_t)i * W + (lane >> 6); *p = (*p & ~(1ULL << (lane & 63))) | ((u64)(c[i] & 1) << (lane & 63)); } }
void v_get(int lane, uint8_t *c) { for (int i = 0; i < n; i++) c[i] = (a[(size_t)i * W + (lane >> 6)] >> (lane & 63)) & 1; }
void v_clear(void) { memset(a, 0, (size_t)(n + 1) * W * 8); }
void v_swap(int i, int j, int v) { nb[12 * i + j] = v; }
int v_nb(int i, int j) { return nb[12 * i + j]; }
void v_coins(int L_, double p, unsigned long long seed) { L = L_; thr = (u64)floor(p * 65536 + 0.5); for (int l = 0; l < 8; l++) lthr[l] = thr; sm2 = fin64(fin64(seed + 0x632BE59BD9B4E019ULL) ^ 0xD1B54A32D192ED03ULL); coins(); }
#else
int main(int argc, char **argv) {
  if (argc < 7 || strcmp(argv[2], "brute")) { fprintf(stderr, "usage: slab GEOM brute SEED GENS L P\n"); return 2; }
  if (geom_load(argv[1]) < 0) { fprintf(stderr, "bad geometry\n"); return 2; }
  u64 seed = strtoull(argv[3], 0, 10); long gens = atol(argv[4]); L = atoi(argv[5]); double p = atof(argv[6]);
  thr = (u64)floor(p * 65536 + 0.5); for (int l = 0; l < 8; l++) lthr[l] = thr;
  { char buf[512]; strncpy(buf, argv[6], 511); buf[511] = 0; int l = L;      /* P may be a list "pL,pL+1,...": one bias a layer */
    for (char *t = strtok(buf, ","); t && l < 8; t = strtok(0, ","), l++) lthr[l] = (u64)floor(atof(t) * 65536 + 0.5);
    for (; l < 8 && l > L; l++) lthr[l] = lthr[l - 1]; }
  sm = fin64(seed * 0x2545F4914F6CDD1DULL + 7); sm2 = fin64(fin64(seed + 0x632BE59BD9B4E019ULL) ^ 0xD1B54A32D192ED03ULL);
  int H = (int)floor(A / 4.0 + 0.5);
  static int pop[NL], pop7[NL], pop1[NL]; static long age[NL]; static uint32_t arm[NL], pend[NL];
  long NK[16] = {0}, DK[16] = {0}, CK[16] = {0}; double E = 0, sp = 0; long n0 = 0, n7 = 0, both = 0;
  double L1n[7] = {0}, L1s[7] = {0}, LYs[8] = {0}, LYn = 0; const int tv[7] = {1 << 20, 20, 15, 10, 6, 4, 2}; static int popl[NL];
  for (int l = 0; l < NL; l++) { soup(l); age[l] = 0; }
  if (L < 8) coins();
  for (long g = 0; g < gens + T0; g++) {
    step(); if (L < 8) coins();
    count(0, A, pop); count(7 * A, 8 * A, pop7); count(A, 2 * A, pop1);
    if (g >= T0 && (g & 7) == 0) { for (int y = 0; y < 8; y++) { count(y * A, (y + 1) * A, popl); for (int l = 0; l < NL; l++) if (age[l] + 1 > T0) LYs[y] += popl[l]; } for (int l = 0; l < NL; l++) if (age[l] + 1 > T0) LYn += 1; }
    for (int l = 0; l < NL; l++) {
      age[l]++; int counted = (g >= T0 && age[l] > T0), d0 = pop[l] == 0, d7 = (L == 8) && pop7[l] == 0;
      if (counted) { E += 1; sp += pop[l]; for (int t = 0; t < 7; t++) if (pop[l] <= tv[t]) { L1n[t] += 1; L1s[t] += pop1[l]; } }
      { int q = pop[l];
        if (q >= H) { pend[l] = 0; arm[l] = 0xFFFF; }
        else { uint32_t m = arm[l] & ((q < 16) ? ~((1u << q) - 1) : 0) & 0xFFFF;
          if (m) { arm[l] &= ~m; if (counted) { pend[l] |= m; uint32_t mm = m; while (mm) { NK[__builtin_ctz(mm)]++; mm &= mm - 1; } } } }
        if (d0 || d7) { uint32_t m = pend[l]; while (m) { int k = __builtin_ctz(m); if (d0) DK[k]++; else CK[k]++; m &= m - 1; } pend[l] = arm[l] = 0; } }
      if (d0 || d7) { if (counted) { if (d0) n0++; if (d7) n7++; if (d0 && d7) both++; } soup(l); age[l] = 0;
        if (L < 8) { for (int i = L * A; i < n; i++) { u64 *x = a + (size_t)i * W + (l >> 6), bit = 1ULL << (l & 63); if (rnd2() & 1) *x |= bit; else *x &= ~bit; } } }
    }
  }
  printf("SLAB A %d n %d L %d p %.5f seed %llu exposure %.6e watched %ld other %ld both %ld Pbar %.4f", A, n, L, thr / 65536.0, (unsigned long long)seed, E, n0, n7, both, sp / E);
  if (n0) printf(" lntau_watched %.4f +- %.4f", log(E / n0), 1 / sqrt((double)n0));
  if (L == 8 && n0 + n7) printf(" lntau_face %.4f +- %.4f", log(2 * E / (n0 + n7)), 1 / sqrt((double)(n0 + n7)));
  printf("\nREC H %d :", H); for (int k = 0; k < 16; k++) printf(" %d:%ld/%ld/%ld", k, NK[k], DK[k], CK[k]);
  printf("\nLAYERS (mean density of each layer, every 8th counted generation) :"); for (int y = 0; y < 8; y++) printf(" %d:%.5f", y, LYn ? LYs[y] / LYn / A : -1.0);
  printf("\nBIASES :"); for (int y = L; y < 8; y++) printf(" %d:%.5f", y, lthr[y] / 65536.0);
  printf("\nLAYER1 n %d :", A); for (int t = 0; t < 7; t++) printf(" %d:%.5f", tv[t] > 1000 ? -1 : tv[t], L1n[t] ? L1s[t] / L1n[t] / A : -1.0); printf("\n");
  return 0;
}
#endif
