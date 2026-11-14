/* ts3 (research/shape3): ts.c with a carry-save AVX-512 step kernel; otherwise unchanged.
 * ts: independent bit-sliced gump stepper for the review of research/shape/ (shares no code with it).
 * 64*W replicas; each replica runs successive lives ("renewal"): a life starts from a fresh p-soup and ends at its
 * first event (face death, transverse firewall), or is censored (settled with period | 840, or age >= cap); the
 * replica is then reseeded. Events are detected every K generations (age rounded up to K).
 *
 * Input (int32 LE, written by ts.py): n; nbr[n*12] (-1 = outside the slab, always dead);
 *   face0 size, cells; face1 size, cells; ndiag; per diag: nlayers, per layer: size, cells (in ring order);
 *   nint (interior d0 layers, in order), per layer: size, cells.
 * Usage: ts FILE W p seed cap K gens EVENTS_OUT [-i init.txt]   (-i: W=1, replica 0 from listed cells, trace pops)
 * Output: summary line on stdout; EVENTS_OUT gets one line per ended life: type age
 *   type F = face death, X = face death and firewall at the same check, W = firewall, S = settled, C = cap,
 *   E = still running at the end of the run (censored).
 * Diagnostics on stdout: number of checks at which some replica had 2 adjacent dead transverse layers,
 * and the number of interior d0 firewalls (three adjacent dead interior layers) first seen within a life.
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
typedef struct { int n; int *c; } lay;
static lay rdl(FILE *f) { lay L; L.n = rdi(f); L.c = malloc(4 * L.n); for (int i = 0; i < L.n; i++) L.c[i] = rdi(f); return L; }


/* shape3: carry-save count of the 12 neighbours (replaces ts.c's ripple counter; same rule, same everything else).
   n = b0 + 2 b1 + 4 b2 + 8 b3; born on n = 4, 5; survive on n = 3, 4, 5. */
#define FA(s, c, x, y, z) do { __typeof__(x) t_ = (x) ^ (y); s = t_ ^ (z); c = ((x) & (y)) | (t_ & (z)); } while (0)
#define RULE_BODY(T) \
  T s1, c1, s2, c2, s3, c3, s4, c4, S, C, b0, H, t1, d1, t2, d2, b1, e, b2, b3; \
  FA(s1, c1, x[0], x[1], x[2]); FA(s2, c2, x[3], x[4], x[5]); FA(s3, c3, x[6], x[7], x[8]); FA(s4, c4, x[9], x[10], x[11]); \
  FA(S, C, s1, s2, s3); b0 = S ^ s4; H = S & s4; \
  FA(t1, d1, c1, c2, c3); FA(t2, d2, c4, C, H); b1 = t1 ^ t2; e = t1 & t2; \
  FA(b2, b3, d1, d2, e); \
  return ~b3 & ((b2 & ~b1) | (me & ~b2 & b1 & b0));
static inline u64 rule(const u64 *x, u64 me) { RULE_BODY(u64) }
typedef u64 v8 __attribute__((vector_size(64), aligned(8)));
static inline v8 rule8(const v8 *x, v8 me) { RULE_BODY(v8) }
static void step8(const u64 *a, u64 *b, const int *nb, int n, int W) {
  for (int i = 0; i < n; i++) {
    const int *q = nb + 12 * (size_t)i;
    for (int w = 0; w < W; w += 8) {
      v8 x[12]; for (int t = 0; t < 12; t++) memcpy(&x[t], a + (size_t)q[t] * W + w, 64);
      v8 me; memcpy(&me, a + (size_t)i * W + w, 64);
      v8 o = rule8(x, me); memcpy(b + (size_t)i * W + w, &o, 64);
    }
  }
}

int main(int argc, char **argv) {
  if (argc < 9) { fprintf(stderr, "usage\n"); return 1; }
  int W = atoi(argv[2]); double p = atof(argv[3]); sm = strtoull(argv[4], 0, 10) * 0x2545F4914F6CDD1DULL + 12345;
  long cap = atol(argv[5]); int K = atoi(argv[6]); long gens = atol(argv[7]); const char *evf = argv[8];
  const char *initf = 0, *proff = 0;
  for (int i = 9; i < argc; i++) { if (!strcmp(argv[i], "-i")) initf = argv[++i]; else if (!strcmp(argv[i], "-p")) proff = argv[++i]; }
  FILE *f = fopen(argv[1], "rb"); int n = rdi(f);
  int *nb = malloc(4 * 12 * (size_t)n); for (int i = 0; i < 12 * n; i++) { int x = rdi(f); nb[i] = x < 0 ? n : x; }
  lay F0 = rdl(f), F1 = rdl(f); int nd = rdi(f); int *nl = malloc(4 * nd); lay **D = malloc(sizeof(lay *) * nd);
  for (int d = 0; d < nd; d++) { nl[d] = rdi(f); D[d] = malloc(sizeof(lay) * nl[d]); for (int l = 0; l < nl[d]; l++) D[d][l] = rdl(f); }
  int ni = rdi(f); lay *I = malloc(sizeof(lay) * ni); for (int l = 0; l < ni; l++) I[l] = rdl(f);
  fclose(f);
  int R = 64 * W; u64 thr = (u64)(p * 18446744073709551616.0);
  u64 *a = calloc((size_t)(n + 1) * W, 8), *b = calloc((size_t)(n + 1) * W, 8), *snap = calloc((size_t)n * W, 8);
  long *born = calloc(R, sizeof(long)); u64 *intfw = calloc(W, 8);
  for (int i = 0; i < n; i++) for (int w = 0; w < W; w++) { u64 x = 0; for (int k = 0; k < 64; k++) if (rnd() < thr) x |= 1ULL << k; a[(size_t)i * W + w] = x; }
  if (initf) { for (int i = 0; i < n; i++) a[(size_t)i * W] &= ~1ULL; FILE *g = fopen(initf, "r"); int c;
    while (fscanf(g, "%d", &c) == 1) a[(size_t)c * W] |= 1ULL; fclose(g); cap = gens + 1; }
  memcpy(snap, a, 8 * (size_t)n * W);
  FILE *ev = fopen(evf, "w");
  long nF = 0, nX = 0, nW = 0, nS = 0, nC = 0, near2 = 0, nI = 0; double E = 0;
  u64 *dead = malloc(8 * 64);
  /* -p: ring buffer of the two face layers over the last 32 generations; at each face death, the dying face's
     population in the 24 generations before its death generation (first all-dead generation) */
  int RB = 32, nf = F0.n + F1.n; u64 *ring = proff ? calloc((size_t)RB * nf * W, 8) : 0; FILE *pf = proff ? fopen(proff, "w") : 0;
  for (long gen = 0; gen < gens; gen++) {
    if (initf) { long pop = 0; for (int i = 0; i < n; i++) pop += a[(size_t)i * W] & 1; printf("T %ld %ld\n", gen, pop); }
    if (W % 8 == 0) step8(a, b, nb, n, W); else
    for (int i = 0; i < n; i++) {
      const int *q = nb + 12 * (size_t)i; u64 *o = b + (size_t)i * W; const u64 *me = a + (size_t)i * W;
      for (int w = 0; w < W; w++) {
        u64 x[12]; for (int t = 0; t < 12; t++) x[t] = a[(size_t)q[t] * W + w];
        o[w] = rule(x, me[w]);
      }
    }
    { u64 *t = a; a = b; b = t; }
    long g1 = gen + 1;
    if (ring) { u64 *sl = ring + (size_t)(g1 % RB) * nf * W;
      for (int k = 0; k < F0.n; k++) memcpy(sl + (size_t)k * W, a + (size_t)F0.c[k] * W, 8 * W);
      for (int k = 0; k < F1.n; k++) memcpy(sl + (size_t)(F0.n + k) * W, a + (size_t)F1.c[k] * W, 8 * W); }
    int chk = (g1 % K == 0), set = (g1 % 840 == 0);
    if (!chk && !set) continue;
    for (int w = 0; w < W; w++) {
      u64 endF = 0, endW = 0, endS = 0;
      if (chk) {
        u64 x0 = 0, x1 = 0; for (int k = 0; k < F0.n; k++) x0 |= a[(size_t)F0.c[k] * W + w];
        for (int k = 0; k < F1.n; k++) x1 |= a[(size_t)F1.c[k] * W + w];
        endF = ~x0 | ~x1;
        u64 n2 = 0;
        for (int d = 0; d < nd; d++) { int L = nl[d]; if (L < 3) continue;
          for (int l = 0; l < L; l++) { u64 x = 0; for (int k = 0; k < D[d][l].n; k++) x |= a[(size_t)D[d][l].c[k] * W + w]; dead[l] = ~x; }
          for (int l = 0; l < L; l++) { endW |= dead[l] & dead[(l + 1) % L] & dead[(l + 2) % L]; n2 |= dead[l] & dead[(l + 1) % L]; } }
        near2 += __builtin_popcountll(n2);
        { u64 di[16]; for (int l = 0; l < ni; l++) { u64 x = 0; for (int k = 0; k < I[l].n; k++) x |= a[(size_t)I[l].c[k] * W + w]; di[l] = ~x; }
          u64 fi = 0; for (int l = 0; l + 2 < ni; l++) fi |= di[l] & di[l + 1] & di[l + 2];
          u64 nw = fi & ~intfw[w]; nI += __builtin_popcountll(nw); intfw[w] |= fi; }
      }
      if (set) { u64 eq = ~0ULL; for (int i = 0; i < n; i++) eq &= ~(a[(size_t)i * W + w] ^ snap[(size_t)i * W + w]);
        for (int i = 0; i < n; i++) snap[(size_t)i * W + w] = a[(size_t)i * W + w];
        endS = eq; }
      u64 endAny = endF | endW | endS;
      for (int k = 0; k < 64; k++) { int r = 64 * w + k; long age = g1 - born[r];
        u64 bit = 1ULL << k; int cens = 0;
        if (endAny & bit) {
          if ((endF & bit) && (endW & bit)) { nX++; fprintf(ev, "X %ld\n", age); E += age; }
          else if (endF & bit) { nF++; fprintf(ev, "F %ld\n", age); E += age;
            if (pf && age > RB) for (int fc = 0; fc < 2; fc++) {
              int off = fc ? F0.n : 0, cnt = fc ? F1.n : F0.n;
              #define POP(g) ({ const u64 *sl_ = ring + (size_t)((g) % RB) * nf * W; int c_ = 0; \
                for (int j_ = 0; j_ < cnt; j_++) c_ += (sl_[(size_t)(off + j_) * W + w] >> k) & 1; c_; })
              if (POP(g1) != 0) continue;
              long gl = g1; while (gl > g1 - RB + 1 && POP(gl) == 0) gl--;
              long gd = gl + 1; if (gd - 24 <= g1 - RB) continue;
              fprintf(pf, "P %d", fc); for (long g = gd - 24; g < gd; g++) fprintf(pf, " %d", POP(g)); fprintf(pf, "\n");
            } }
          else if (endW & bit) { nW++; fprintf(ev, "W %ld\n", age); E += age; }
          else { if (age < 840) continue;   /* snapshot predates this life */
                 nS++; fprintf(ev, "S %ld\n", age - 840); E += age - 840; }
        } else if (age >= cap && !initf) { nC++; fprintf(ev, "C %ld\n", age); E += age; cens = 1; }
        else continue;
        (void)cens;
        if (initf) continue;
        /* reseed replica r */
        for (int i = 0; i < n; i++) { u64 *x = a + (size_t)i * W + w; if (rnd() < thr) *x |= bit; else *x &= ~bit; }
        intfw[w] &= ~bit; born[r] = g1;
      }
    }
  }
  long nE = 0; if (!initf) for (int r = 0; r < R; r++) { long age = gens - born[r]; fprintf(ev, "E %ld\n", age); E += age; nE++; }
  fclose(ev); if (pf) fclose(pf);
  printf("SUMMARY gens %ld R %d exposure %.6e F %ld X %ld W %ld S %ld C %ld E %ld near2 %ld intfw %ld\n",
         gens, R, E, nF, nX, nW, nS, nC, nE, near2, nI);
  return 0;
}
