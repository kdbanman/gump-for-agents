/* pc: PR 18 review -- independent bit-sliced gump stepper on the slab + empty-patch counter (own code; program file
 * from geom18.py). 64*W replicas from p-soups; burn B generations; then G generations in NB time batches; at every
 * generation, per measured group (face, kind, shape: a list of OR-nodes, one per translate), count
 *   samples = live replicas x translates, hits = empty translates, hits2 = empty now and at the previous generation.
 * A replica whose face dies (a face layer all dead) or that settles (state(t) == state(t-2) at a check every 1024
 * generations) is masked out from then on and reported.
 * Usage: pc PROG W p seed B G NB OUT [-i cells.txt -t T]   (-i: replica 0 starts from the listed cell indices; -t:
 *   after T generations print replica 0's live cell indices and exit -- the engine check)
 * OUT: one line per (batch, group): batch name samples hits hits2
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint64_t u64;
static u64 sm;
static inline u64 rnd(void) { u64 z = (sm += 0x9e3779b97f4a7c15ULL); z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
  z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; return z ^ (z >> 31); }
static int rdi(FILE *f) { int32_t x; if (fread(&x, 4, 1, f) != 1) { fprintf(stderr, "short read\n"); exit(1); } return x; }

int main(int argc, char **argv) {
  if (argc < 9) { fprintf(stderr, "usage\n"); return 1; }
  int W = atoi(argv[2]); double p = atof(argv[3]); sm = strtoull(argv[4], 0, 10) * 0x2545F4914F6CDD1DULL + 777;
  long B = atol(argv[5]), G = atol(argv[6]); int NB = atoi(argv[7]); const char *outf = argv[8];
  const char *initf = 0; long T = -1;
  for (int i = 9; i < argc; i++) { if (!strcmp(argv[i], "-i")) initf = argv[++i]; else if (!strcmp(argv[i], "-t")) T = atol(argv[++i]); }
  FILE *f = fopen(argv[1], "rb"); int n = rdi(f);
  int *nb = malloc(4 * 12 * (size_t)n); for (int i = 0; i < 12 * n; i++) nb[i] = rdi(f);
  int nf[2]; int *fc[2];
  for (int k = 0; k < 2; k++) { nf[k] = rdi(f); fc[k] = malloc(4 * nf[k]); for (int i = 0; i < nf[k]; i++) fc[k][i] = rdi(f); }
  int nn = rdi(f); int *noff = malloc(4 * (nn + 1)); int cap = 1 << 20, *ops = malloc(4 * cap), no = 0;
  for (int k = 0; k < nn; k++) { int c = rdi(f); noff[k] = no; if (no + c > cap) { cap *= 2; ops = realloc(ops, 4 * cap); }
    for (int i = 0; i < c; i++) ops[no++] = rdi(f); }
  noff[nn] = no;
  int ng = rdi(f); char **gname = malloc(sizeof(char *) * ng); int *gn = malloc(4 * ng); int **gid = malloc(sizeof(int *) * ng);
  for (int g = 0; g < ng; g++) { int L = rdi(f); gname[g] = calloc(L + 1, 1); if (fread(gname[g], 1, L, f) != (size_t)L) return 2;
    gn[g] = rdi(f); gid[g] = malloc(4 * gn[g]); for (int i = 0; i < gn[g]; i++) gid[g][i] = rdi(f); }
  fclose(f);
  int tot = n + 1 + nn;                                   /* value slots: cells, sentinel n, nodes */
  u64 *a = calloc((size_t)tot * W, 8), *b = calloc((size_t)tot * W, 8), *old = calloc((size_t)n * W, 8);
  u64 thr = (u64)(p * 18446744073709551616.0);
  for (int i = 0; i < n; i++) for (int w = 0; w < W; w++) { u64 x = 0; for (int k = 0; k < 64; k++) if (rnd() < thr) x |= 1ULL << k; a[(size_t)i * W + w] = x; }
  if (initf) { for (int i = 0; i < n; i++) a[(size_t)i * W] &= ~1ULL; FILE *g = fopen(initf, "r"); int c;
    while (fscanf(g, "%d", &c) == 1) a[(size_t)c * W] |= 1ULL; fclose(g); }
  /* empty-mask memory for hits2: per measured item */
  long nit = 0; for (int g = 0; g < ng; g++) nit += gn[g];
  u64 *prev = calloc((size_t)nit * W, 8);
  u64 *mask = malloc(8 * W); for (int w = 0; w < W; w++) mask[w] = ~0ULL;
  long *S = calloc(ng, sizeof(long)), *H = calloc(ng, sizeof(long)), *H2 = calloc(ng, sizeof(long));
  FILE *out = fopen(outf, "w");
  long nface = 0, nsettle = 0;
  long total = B + G, per = G / NB;
  for (long gen = 0; gen < total; gen++) {
    for (int i = 0; i < n; i++) {
      const int *q = nb + 12 * (size_t)i; u64 *o = b + (size_t)i * W; const u64 *me = a + (size_t)i * W;
      for (int w = 0; w < W; w++) {
        u64 c0 = 0, c1 = 0, c2 = 0, c3 = 0;
        for (int t = 0; t < 12; t++) { u64 x = a[(size_t)q[t] * W + w];
          u64 k0 = c0 & x; c0 ^= x; u64 k1 = c1 & k0; c1 ^= k0; u64 k2 = c2 & k1; c2 ^= k1; c3 |= k2; }
        u64 is4 = ~c3 & c2 & ~c1 & ~c0, is5 = ~c3 & c2 & ~c1 & c0, is3 = ~c3 & ~c2 & c1 & c0;
        o[w] = is4 | is5 | (me[w] & is3);
      }
    }
    { u64 *t = a; a = b; b = t; }                         /* sentinel slot n stays 0 in both */
    long g1 = gen + 1;
    if (T >= 0 && g1 == T) { for (int i = 0; i < n; i++) if (a[(size_t)i * W] & 1) printf("%d\n", i); return 0; }
    /* face death */
    for (int w = 0; w < W; w++) { u64 x0 = 0, x1 = 0;
      for (int k = 0; k < nf[0]; k++) x0 |= a[(size_t)fc[0][k] * W + w];
      for (int k = 0; k < nf[1]; k++) x1 |= a[(size_t)fc[1][k] * W + w];
      u64 d = (~x0 | ~x1) & mask[w]; nface += __builtin_popcountll(d); mask[w] &= ~d; }
    if ((g1 + 2) % 1024 == 0) memcpy(old, a, 8 * (size_t)n * W);
    if (g1 % 1024 == 0) for (int w = 0; w < W; w++) { u64 df = 0; for (int i = 0; i < n; i++) df |= a[(size_t)i * W + w] ^ old[(size_t)i * W + w];
      u64 d = ~df & mask[w]; nsettle += __builtin_popcountll(d); mask[w] &= ~d; }
    if (g1 <= B) continue;
    /* OR nodes */
    for (int k = 0; k < nn; k++) { u64 *v = a + (size_t)(n + 1 + k) * W;
      for (int w = 0; w < W; w++) { u64 x = 0; for (int c = noff[k]; c < noff[k + 1]; c++) x |= a[(size_t)ops[c] * W + w]; v[w] = x; } }
    long it = 0; int first = (g1 == B + 1);
    for (int g = 0; g < ng; g++) {
      long h = 0, h2 = 0;
      for (int i = 0; i < gn[g]; i++, it++) { const u64 *v = a + (size_t)gid[g][i] * W; u64 *pv = prev + (size_t)it * W;
        for (int w = 0; w < W; w++) { u64 e = ~v[w] & mask[w]; h += __builtin_popcountll(e); if (!first) h2 += __builtin_popcountll(e & pv[w]); pv[w] = e; } }
      long ms = 0; for (int w = 0; w < W; w++) ms += __builtin_popcountll(mask[w]);
      H[g] += h; H2[g] += h2; S[g] += ms * gn[g];
    }
    if ((g1 - B) % per == 0) {
      long bt = (g1 - B) / per - 1;
      for (int g = 0; g < ng; g++) { fprintf(out, "%ld\t%s\t%ld\t%ld\t%ld\n", bt, gname[g], S[g], H[g], H2[g]); S[g] = H[g] = H2[g] = 0; }
      fflush(out);
      fprintf(stderr, "batch %ld done (gen %ld); masked: face %ld settle %ld\n", bt, g1, nface, nsettle);
    }
  }
  fprintf(out, "#masked\tface %ld\tsettle %ld\n", nface, nsettle);
  fclose(out);
  return 0;
}
