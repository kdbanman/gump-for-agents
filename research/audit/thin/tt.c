/* tt: independent bit-sliced gump stepper for the review of research/theory/thin/ (shares no code with it).
 * Graph, faces, walls, coin cells and layer lists come from tt.py (built from research/audit/shape/geom_check.py,
 * i.e. from AUTOMATON.md's cube-index table).  64*W replicas ("lanes"); each lane runs successive lives.
 *
 * A life starts from a soup of density 0.4 on every non-coin cell (wall cells then cleared) and ends at
 *   F  a face is empty (checked every generation; both faces empty at once counts two deaths),
 *   S  the state of the non-coin cells equals the lane's snapshot (snapshots at ages 16, 32, 64, ...; compared
 *      every generation, so any period is found); exposure is cut at the snapshot age (only with -r),
 *   W  three adjacent dead layers among the listed interior layers (checked every 16 generations),
 *   E  end of run (censored).
 * Coins: before every generation each coin cell is redrawn alive with probability q/256 (8 random words per word).
 * Walls: cells held dead (cleared after the soup and after every step).
 * Exposure and deaths are kept for ages >= T0, in power-of-two age bins.
 *
 * Input (int32 LE): n; nbr[n*12] (-1 = dead); nface, per face: size, cells; nwall, cells; ncoin, cells; q256;
 *   nlay, per layer: size, cells; rep (1 = look for repeating states)
 * Usage: tt FILE seed gens T0 OUT [-t TRACE G] [-P PROF maxprof]
 *   -t: lane 0 only, every generation's full state (cells as 0/1 string) written to TRACE for G generations
 *   -P: at each face death at age > T0 + 32, the face's cells over the 32 generations before (hex per gen)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#ifndef W
#define W 16
#endif
typedef uint64_t u64;
static u64 sm;
static inline u64 rnd(void) { u64 z = (sm += 0x9e3779b97f4a7c15ULL); z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
  z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; return z ^ (z >> 31); }
static int rdi(FILE *f) { int32_t x; if (fread(&x, 4, 1, f) != 1) { fprintf(stderr, "short read\n"); exit(1); } return x; }
typedef struct { int n; int *c; } lst;
static lst rdl(FILE *f) { lst L; L.n = rdi(f); L.c = malloc(4 * (L.n + 1)); for (int i = 0; i < L.n; i++) L.c[i] = rdi(f); return L; }
#define NB 48
#define RB 32

int main(int argc, char **argv) {
  if (argc < 6) { fprintf(stderr, "usage\n"); return 1; }
  sm = strtoull(argv[2], 0, 10) * 0x2545F4914F6CDD1DULL + 777;
  long gens = atol(argv[3]), T0 = atol(argv[4]); const char *outf = argv[5];
  const char *tracef = 0, *proff = 0; long tgen = 0, maxprof = 0;
  for (int i = 6; i < argc; i++) {
    if (!strcmp(argv[i], "-t")) { tracef = argv[++i]; tgen = atol(argv[++i]); }
    else if (!strcmp(argv[i], "-P")) { proff = argv[++i]; maxprof = atol(argv[++i]); } }
  FILE *f = fopen(argv[1], "rb"); int n = rdi(f);
  int *nb = malloc(4 * 12 * (size_t)n); for (int i = 0; i < 12 * n; i++) { int x = rdi(f); nb[i] = x < 0 ? n : x; }
  int nf = rdi(f); lst *F = malloc(sizeof(lst) * nf); for (int k = 0; k < nf; k++) F[k] = rdl(f);
  lst WL = rdl(f), CL = rdl(f); int q = rdi(f);
  int nl = rdi(f); lst *L = malloc(sizeof(lst) * (nl + 1)); for (int k = 0; k < nl; k++) L[k] = rdl(f);
  int rep = rdi(f); fclose(f);
  char *iscoin = calloc(n + 1, 1); for (int k = 0; k < CL.n; k++) iscoin[CL.c[k]] = 1;
  int ndyn = 0; int *dyn = malloc(4 * n); for (int i = 0; i < n; i++) if (!iscoin[i]) dyn[ndyn++] = i;
  const int R = 64 * W; const u64 thr = (u64)(0.4 * 18446744073709551616.0);
  u64 (*a)[W] = calloc(n + 1, sizeof *a), (*b)[W] = calloc(n + 1, sizeof *b), (*snap)[W] = calloc(n + 1, sizeof *snap);
  long *born = calloc(R, sizeof(long)), *snapage = calloc(R, sizeof(long));
  double expo[NB] = {0}; long dth[NB] = {0};
  long nF = 0, nF2 = 0, nS = 0, nWf = 0, nE = 0, nprof = 0; double E = 0; long maxage = 0;
  int nfc = 0; for (int k = 0; k < nf; k++) nfc += F[k].n;
  u64 *ring = proff ? calloc((size_t)RB * nfc * W, 8) : 0; FILE *pf = proff ? fopen(proff, "w") : 0;
  FILE *tf = tracef ? fopen(tracef, "w") : 0;
  if (tf) gens = tgen;
  /* soup */
  for (int i = 0; i < n; i++) for (int w = 0; w < W; w++) { u64 x = 0; if (!iscoin[i]) for (int k = 0; k < 64; k++) if (rnd() < thr) x |= 1ULL << k; a[i][w] = x; }
  for (int k = 0; k < WL.n; k++) memset(a[WL.c[k]], 0, sizeof a[0]);
  memset(a[n], 0, sizeof a[0]); memset(b[n], 0, sizeof b[0]);
#define ADDEXP(age) do { long A_ = (age); if (A_ > maxage) maxage = A_; if (A_ > T0) { E += A_ - T0; \
    for (int j_ = 0; j_ < NB; j_++) { long lo_ = 1L << j_, hi_ = 1L << (j_ + 1); if (lo_ < T0) lo_ = T0; \
      if (A_ > lo_ && hi_ > lo_) expo[j_] += (A_ < hi_ ? A_ : hi_) - lo_; } } } while (0)
  for (long gen = 0; gen < gens; gen++) {
    /* coins for this generation */
    for (int k = 0; k < CL.n; k++) for (int w = 0; w < W; w++) { u64 lt = 0;
      for (int i = 0; i < 8; i++) { u64 bi = rnd(); lt = ((q >> i) & 1) ? (~bi | lt) : (~bi & lt); } a[CL.c[k]][w] = lt; }
    if (tf) { fprintf(tf, "G %ld ", gen); for (int i = 0; i < n; i++) fputc('0' + (int)(a[i][0] & 1), tf); fputc('\n', tf); }
    for (int d = 0; d < ndyn; d++) { int i = dyn[d]; const int *qn = nb + 12 * (size_t)i;
      u64 c0[W], c1[W], c2[W], c3[W];
      for (int w = 0; w < W; w++) c0[w] = c1[w] = c2[w] = c3[w] = 0;
      for (int t = 0; t < 12; t++) { const u64 *x = a[qn[t]];
        for (int w = 0; w < W; w++) { u64 k0 = c0[w] & x[w]; c0[w] ^= x[w]; u64 k1 = c1[w] & k0; c1[w] ^= k0; u64 k2 = c2[w] & k1; c2[w] ^= k1; c3[w] |= k2; } }
      for (int w = 0; w < W; w++) { u64 is45 = ~c3[w] & c2[w] & ~c1[w], is3 = ~c3[w] & ~c2[w] & c1[w] & c0[w];
        b[i][w] = is45 | (a[i][w] & is3); } }
    for (int k = 0; k < CL.n; k++) memset(b[CL.c[k]], 0, sizeof b[0]);
    for (int k = 0; k < WL.n; k++) memset(b[WL.c[k]], 0, sizeof b[0]);
    { u64 (*t)[W] = a; a = b; b = t; }
    long g1 = gen + 1;
    if (tf) continue;
    if (ring) { int off = 0; for (int k = 0; k < nf; k++) for (int j = 0; j < F[k].n; j++, off++)
        memcpy(ring + ((size_t)(g1 % RB) * nfc + off) * W, a[F[k].c[j]], 8 * W); }
    int chkW = (g1 % 16 == 0);
    for (int w = 0; w < W; w++) {
      u64 dead[2] = {0, 0}; u64 anyF;
      for (int k = 0; k < nf; k++) { u64 x = 0; for (int j = 0; j < F[k].n; j++) x |= a[F[k].c[j]][w]; dead[k] = ~x; }
      anyF = dead[0] | (nf > 1 ? dead[1] : 0);
      u64 eq = 0;
      if (rep) { eq = ~0ULL; for (int d = 0; d < ndyn && eq; d++) { int i = dyn[d]; eq &= ~(a[i][w] ^ snap[i][w]); } }
      u64 fw = 0;
      if (chkW && nl >= 3) { u64 dl[64]; for (int l = 0; l < nl; l++) { u64 x = 0; for (int j = 0; j < L[l].n; j++) x |= a[L[l].c[j]][w]; dl[l] = ~x; }
        for (int l = 0; l + 2 < nl; l++) fw |= dl[l] & dl[l + 1] & dl[l + 2]; }
      for (int k = 0; k < 64; k++) { u64 bit = 1ULL << k; int r = 64 * w + k; long age = g1 - born[r]; int end = 0;
        if (anyF & bit) { int nd = ((dead[0] & bit) != 0) + (nf > 1 && (dead[1] & bit) != 0); end = 1;
          if (age > T0) { nF += nd; nF2 += nd == 2; int j = 63 - __builtin_clzll((u64)(age - 1)); dth[j] += nd; }
          ADDEXP(age);
          if (pf && nprof < maxprof && age > T0 + RB) for (int fc = 0; fc < nf; fc++) if (dead[fc] & bit) {
            int off = 0; for (int kk = 0; kk < fc; kk++) off += F[kk].n;
            fprintf(pf, "P %d", fc);
            for (int gg = g1 - RB + 1; gg <= g1; gg++) { fputc(' ', pf); int acc = 0, nbits = 0;
              for (int j = 0; j < F[fc].n; j++) { acc |= (int)((ring[((size_t)(gg % RB) * nfc + off + j) * W + w] >> k) & 1) << nbits; nbits++;
                if (nbits == 4 || j == F[fc].n - 1) { fputc("0123456789abcdef"[acc], pf); acc = 0; nbits = 0; } } }
            fputc('\n', pf); nprof++; } }
        else if (rep && (eq & bit) && snapage[r] > 0) { end = 2; nS++; ADDEXP(snapage[r]); }
        else if (fw & bit) { end = 3; nWf++; ADDEXP(age); }
        if (end) { for (int i = 0; i < n; i++) { if (iscoin[i]) continue; if (rnd() < thr) a[i][w] |= bit; else a[i][w] &= ~bit; }
          for (int j = 0; j < WL.n; j++) a[WL.c[j]][w] &= ~bit;
          born[r] = g1; snapage[r] = 0; continue; }
        if (rep && age >= 16 && !(age & (age - 1))) { for (int d = 0; d < ndyn; d++) { int i = dyn[d]; snap[i][w] = (snap[i][w] & ~bit) | (a[i][w] & bit); }
          snapage[r] = age; }
      }
    }
  }
  if (tf) { fclose(tf); return 0; }
  for (int r = 0; r < R; r++) { ADDEXP(gens - born[r]); nE++; }
  if (pf) fclose(pf);
  FILE *o = fopen(outf, "w");
  fprintf(o, "gens %ld R %d T0 %ld faces %d exposure %.6e deaths %ld both %ld settled %ld firewall %ld censored %ld maxage %ld\n",
          gens, R, T0, nf, E, nF, nF2, nS, nWf, nE, maxage);
  fprintf(o, "expo"); for (int j = 0; j < NB; j++) fprintf(o, " %.0f", expo[j]); fprintf(o, "\n");
  fprintf(o, "deaths"); for (int j = 0; j < NB; j++) fprintf(o, " %ld", dth[j]); fprintf(o, "\n");
  fclose(o);
  return 0;
}
