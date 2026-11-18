/* tube1d.c -- gump (B45/S345 on the faces of the cubic honeycomb) on a slab of nl {111} layers, periodic in the
 * plane with period lattice (h,k),(0,d) in the hexagonal basis e1 = (1,-1,0), e2 = (0,-1,1) (cube steps;
 * |x e1 + y e2|^2 = 2 (x^2 + xy + y^2)).  Bit-sliced: 64 independent lanes per machine word.
 * Written for research/blast/tube1d from docs/AUTOMATON.md and reference/oracle.py (offsets); shares no code with
 * other samplers.
 *
 * Cell (l, a, x, y): layer l = i+j+k in 0..nl-1 (s = 2l+1), orientation a, cube (i,j,k) = (x, -x-y, y+l).
 * index = ((l*3 + a)*h + x)*d + y after reducing (x,y) mod the lattice.  Top layer l = nl-1 is "the face".
 * Outside the slab everything is dead.  ndice = 0: deterministic slab (two faces: l = 0 and l = nl-1).
 * ndice = 2: surrogate: layers 0,1 are i.i.d. Bernoulli(PV/2^PB) redrawn every generation, layers 2..nl-1
 * (w = nl-2 layers, the top one the face) follow the rule: a Markov chain on the w rule layers.
 *
 *   tube1d trace h k d nl seed gens [bad]            lane 0 of a deterministic slab, one line of N bits per gen
 *   tube1d brute h k d nl ndice seed T0 gens [pathfile]   lifetimes by brute force (restart at death); pathfile gets, per
 *                    face death: age face(0 top, 1 bottom) then per face cell the lag (generations before the death at which
 *                    the cell was last alive; 1 = alive in the last living generation; -1 = not alive in the last 255)
 *   tube1d ffs   h k d nl ndice seed M delta N0 [pathfile [maxpaths]]   forward-flux estimate of the face lifetime
 *   tube1d band  h k d nl ndice seed width T reps [depth]   kill a band of the face (and depth-1 layers beneath)
 *   tube1d clone h k d nl ndice seed lamA lam n0     is a death decided at the crossing of lam? (64 clones each)
 *   tube1d bandp h k d nl ndice seed gens T0 [maxbins]   P(band of width w right round the girth is empty), living tube
 *   tube1d geom  h k d nl                             face-cell geometry (index, a, x, y, xi, eta)
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
typedef uint64_t u64;

static int H_, K_, D_, NL, NDICE, N, A, DYN0;
static int *nb;
static double *XI, *ETA; static double LT, GIRTH; static int VA, VB;
static u64 *xa, *xb, *xc;

/* ---- rng: xoshiro256** ---- */
static u64 rs[4];
static inline u64 rotl(const u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static inline u64 rnd(void) { const u64 r = rotl(rs[1] * 5, 7) * 9, t = rs[1] << 17;
  rs[2] ^= rs[0]; rs[3] ^= rs[1]; rs[1] ^= rs[2]; rs[0] ^= rs[3]; rs[2] ^= t; rs[3] = rotl(rs[3], 45); return r; }
static u64 splitmix(u64 *s) { u64 z = (*s += 0x9E3779B97F4A7C15ULL); z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
  z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL; return z ^ (z >> 31); }
static void seedrng(u64 s) { for (int i = 0; i < 4; i++) rs[i] = splitmix(&s); for (int i = 0; i < 16; i++) rnd(); }
/* Bernoulli(PV / 2^PB) word */
#define PB 7
#define PV 53
static inline u64 bword(void) { u64 w = rnd(); /* bit 0 of PV=53 (binary 0110101) is 1: start with prob 1/2 */
  for (int i = 1; i < PB; i++) { u64 r = rnd(); w = (PV >> i & 1) ? (w | r) : (w & r); } return w; }
static inline int bbit(void) { return (rnd() >> 57) < PV; }

/* ---- geometry ---- */
static inline int fdiv(int a, int b) { int q = a / b; if ((a % b != 0) && ((a < 0) != (b < 0))) q--; return q; }
static inline int idx(int l, int a, int x, int y) { int q = fdiv(x, H_); x -= q * H_; y -= q * K_; y -= fdiv(y, D_) * D_;
  return ((l * 3 + a) * H_ + x) * D_ + y; }
static void build(int bad) {
  A = 3 * H_ * D_; N = NL * A; DYN0 = NDICE * A;
  nb = malloc(sizeof(int) * 12 * (size_t)N);
  XI = malloc(sizeof(double) * N); ETA = malloc(sizeof(double) * N);
  /* shortest lattice vector = girth */
  int best = 1 << 30; VA = VB = 0;
  for (int m = 0; m <= 40; m++) for (int j = -400; j <= 400; j++) { if (m == 0 && j <= 0) continue;
    int x = m * H_, y = m * K_ + j * D_; long q = (long)x * x + (long)x * y + (long)y * y; if (q < best) { best = q; VA = x; VB = y; } }
  double vx = VA + 0.5 * VB, vy = -0.8660254037844386 * VB; GIRTH = sqrt(vx * vx + vy * vy);
  LT = H_ * D_ * 0.8660254037844386 / GIRTH;
  double nx = -vy / GIRTH, ny = vx / GIRTH;
  for (int l = 0; l < NL; l++) for (int a = 0; a < 3; a++) for (int x = 0; x < H_; x++) for (int y = 0; y < D_; y++) {
    int c = idx(l, a, x, y);
    int p[3] = {2 * x, 2 * (-x - y), 2 * (y + l)}; p[a] += 1;
    /* in-plane position, hexagonal units: u = (1,-1,0)/sqrt2, w = (1,1,-2)/sqrt6, divided by 2 sqrt2 */
    double X = (p[0] - p[1]) / 4.0, Y = (p[0] + p[1] - 2 * p[2]) / (4.0 * 1.7320508075688772);
    double t = X * nx + Y * ny; t -= floor(t / LT) * LT; XI[c] = t;
    double e = (X * vx + Y * vy) / GIRTH; e -= floor(e / GIRTH) * GIRTH; ETA[c] = e;
    int b = (a + 1) % 3, cc = (a + 2) % 3, n = 0, o[12][3];
    for (int sb = 2; sb >= -2; sb -= 4) for (int sc = 2; sc >= -2; sc -= 4) { o[n][a] = 0; o[n][b] = sb; o[n][cc] = sc; n++; }
    for (int sa = 1; sa >= -1; sa -= 2) for (int ti = 0; ti < 2; ti++) for (int st = 1; st >= -1; st -= 2) {
      int t2 = ti ? cc : b, t3 = ti ? b : cc; o[n][a] = sa; o[n][t2] = st; o[n][t3] = 0; n++; }
    for (int m = 0; m < 12; m++) {
      int q[3] = {p[0] + o[m][0], p[1] + o[m][1], p[2] + o[m][2]};
      int t2 = (q[0] & 1) ? 0 : (q[1] & 1) ? 1 : 2; q[t2] -= 1;
      int i = q[0] / 2, j = q[1] / 2, k = q[2] / 2;   /* all even: exact */
      int l2 = i + j + k;
      nb[12 * c + m] = (l2 < 0 || l2 >= NL) ? N : idx(l2, t2, i, -i - j);
    }
  }
  if (bad) { int c = N / 2 + 1; nb[12 * c + 3] = (nb[12 * c + 3] + 1) % N; }   /* negative control: one wrong neighbour */
  xa = calloc(N + 1, 8); xb = calloc(N + 1, 8); xc = calloc(N + 1, 8);
}

#define FA(a, b, c, s, cy) { u64 _t = (a) ^ (b); s = _t ^ (c); cy = ((a) & (b)) | (_t & (c)); }
#define HA(a, b, s, cy) { s = (a) ^ (b); cy = (a) & (b); }
/* one generation: reads xa, writes xb, then rotates so that xa = new, xb = old, xc = older */
static void step(void) {
  const u64 *x = xa; u64 *y = xc;   /* overwrite the oldest buffer */
  for (int c = DYN0; c < N; c++) {
    const int *n = nb + 12 * c;
    u64 s0, s1, s2, s3, c0, c1, c2, c3, t0, d0, d1, b0, u0, u1, e0, e1, e2, b1, b2, b3;
    FA(x[n[0]], x[n[1]], x[n[2]], s0, c0); FA(x[n[3]], x[n[4]], x[n[5]], s1, c1);
    FA(x[n[6]], x[n[7]], x[n[8]], s2, c2); FA(x[n[9]], x[n[10]], x[n[11]], s3, c3);
    FA(s0, s1, s2, t0, d0); HA(t0, s3, b0, d1);
    FA(c0, c1, c2, u0, e0); FA(c3, d0, d1, u1, e1); HA(u0, u1, b1, e2);
    FA(e0, e1, e2, b2, b3);
    y[c] = ~b3 & ((b2 & ~b1) | (x[c] & ~b2 & b1 & b0));
  }
  for (int c = 0; c < DYN0; c++) y[c] = bword();
  y[N] = 0;
  u64 *t = xc; xc = xb; xb = xa; xa = t;
}
static void popcounts(const u64 *x, int c0, int c1, int *pop) {
  u64 pl[16]; memset(pl, 0, sizeof pl);
  int c = c0;
  for (; c + 2 < c1; c += 3) { u64 s, cy; FA(x[c], x[c + 1], x[c + 2], s, cy);
    for (int b = 0; s; b++) { u64 t = pl[b] & s; pl[b] ^= s; s = t; }
    for (int b = 1; cy; b++) { u64 t = pl[b] & cy; pl[b] ^= cy; cy = t; } }
  for (; c < c1; c++) { u64 s = x[c]; for (int b = 0; s; b++) { u64 t = pl[b] & s; pl[b] ^= s; s = t; } }
  for (int j = 0; j < 64; j++) { int v = 0; for (int b = 0; b < 12; b++) v |= (int)((pl[b] >> j) & 1) << b; pop[j] = v; }
}
static void init_all(void) { for (int c = 0; c < N; c++) xa[c] = bword(); xa[N] = 0; memcpy(xb, xa, 8 * (N + 1)); memcpy(xc, xa, 8 * (N + 1)); }
static void init_lane(int j) { u64 m = 1ULL << j; for (int c = 0; c < N; c++) { if (bbit()) xa[c] |= m; else xa[c] &= ~m; }
  for (int c = 0; c < N; c++) { xb[c] ^= (xb[c] ^ ~xa[c]) & m; xc[c] ^= (xc[c] ^ ~xa[c]) & m; } /* make history differ: no false settle */ }
static int NW;
/* Look-ahead: dice drawn at generation t first reach the face at t+3 (w = 5, 6) or t+4 (w = 7, 8), so the face
 * population at t+2 is a function of the rule layers at t.  The splitting coordinate is that function,
 * lambda(x_t) = |face(t+2)|: when the observed population crosses a level at generation u, the state stored is the
 * one of generation u-2 (buffer xc), and a trial ignores its first two observations (they replay known faces). */
#define LA 2
static void save_lane(int j, u64 *cfg) { memset(cfg, 0, 8 * NW); for (int c = DYN0; c < N; c++) cfg[c >> 6] |= ((xc[c] >> j) & 1ULL) << (c & 63); }
static void load_lane(int j, const u64 *cfg) { u64 m = 1ULL << j;
  for (int c = DYN0; c < N; c++) xa[c] = (xa[c] & ~m) | (((cfg[c >> 6] >> (c & 63)) & 1ULL) << j); }

/* ---- trace ---- */
static void cmd_trace(int gens) {
  for (int c = 0; c < N; c++) xa[c] = rnd() & 1;
  char *s = malloc(N + 2);
  for (int g = 0; g <= gens; g++) { for (int c = 0; c < N; c++) s[c] = '0' + (int)(xa[c] & 1); s[N] = 0; puts(s); if (g < gens) step(); }
}

/* ---- brute force ---- */
static void cmd_brute(int T0, long gens, FILE *pathf) {
  init_all();
  long age[64]; for (int j = 0; j < 64; j++) age[j] = 0;
  double expo = 0; long deaths = 0, settled = 0; u64 fdiff = 0;
  int f0 = N - A; int z0 = NDICE ? f0 : 0; u64 *snap = calloc(N + 1, 8);   /* snapshot for the period | 840 test */
  enum { RB = 256 }; u64 *ring = pathf ? calloc((size_t)RB * 2 * A, 8) : NULL; long npath = 0;
  for (long g = 1; g <= gens; g++) {
    step();
    u64 top = 0, bot = ~0ULL;
    for (int c = f0; c < N; c++) top |= xa[c];
    if (!NDICE) { bot = 0; for (int c = 0; c < A; c++) bot |= xa[c]; }
    u64 dead = ~top | ~bot, sett = 0;
    if (ring) { u64 *r = ring + (size_t)(g % RB) * 2 * A; memcpy(r, xa + f0, 8 * A); if (!NDICE) memcpy(r + A, xa, 8 * A); }
    if (NDICE) { for (int c = f0; c < N; c++) fdiff |= xa[c] ^ xc[c]; if ((g & 255) == 0) { sett = ~fdiff; fdiff = 0; } }
    else if ((g & 127) == 0) { u64 df = 0; for (int c = 0; c < N; c++) df |= xa[c] ^ xc[c]; sett = ~df; }
    if (g % 840 == 0) { u64 df = 0; for (int c = z0; c < N; c++) { df |= xa[c] ^ snap[c]; snap[c] = xa[c]; } sett |= ~df; }   /* zombies: any period dividing 840 */
    for (int j = 0; j < 64; j++) {
      u64 m = 1ULL << j; age[j]++;
      if (dead & m) { if (age[j] > T0) { deaths += ((~top & m) != 0) + ((~bot & m) != 0); expo += 1;
          if (ring && age[j] > RB) for (int f = 0; f < 2; f++) if ((f ? ~bot : ~top) & m) {   /* lag of each cell's last live generation before the death */
            fprintf(pathf, "%ld %d", age[j], f);
            for (int c = 0; c < A; c++) { int lag = -1; for (int k = 1; k < RB; k++) if (ring[(size_t)((g - k) % RB) * 2 * A + f * A + c] & m) { lag = k; break; } fprintf(pathf, " %d", lag); }
            fputc('\n', pathf); fflush(pathf); npath++; } }
        init_lane(j); age[j] = 0; fdiff |= m; }
      else if (sett & m) { settled++; init_lane(j); age[j] = 0; fdiff |= m; }
      else if (age[j] > T0) expo += 1;
    }
  }
  int nf = NDICE ? 1 : 2;
  double tau = nf * expo / (deaths > 0 ? deaths : 1);
  printf("BRUTE h=%d k=%d d=%d nl=%d ndice=%d A=%d exposure=%.0f deaths=%ld settled=%ld lntau_face=%.4f +- %.4f\n",
         H_, K_, D_, NL, NDICE, A, expo, deaths, settled, log(tau), deaths > 0 ? 1 / sqrt((double)deaths) : 0.0);
}

/* ---- forward flux sampling on the face population ---- */
typedef struct { u64 *cfg; int32_t *last; int *pop; int32_t *clock; int n, cap; } Pool;
static int PATHS = 0;
static void pool_init(Pool *p, int cap) { p->cap = cap; p->n = 0; p->cfg = malloc(8 * (size_t)NW * cap); p->pop = malloc(sizeof(int) * cap);
  p->clock = malloc(4 * (size_t)cap); p->last = PATHS ? malloc(4 * (size_t)A * cap) : NULL; }
static int32_t *lastbuf; static int32_t lclock[64];
static inline int32_t *LAST(int j) { return lastbuf + (size_t)j * A; }
static void pool_add_lane(Pool *p, int j, int pop) { if (p->n >= p->cap) return; save_lane(j, p->cfg + (size_t)NW * p->n); p->pop[p->n] = pop;
  p->clock[p->n] = lclock[j]; if (PATHS) memcpy(p->last + (size_t)A * p->n, LAST(j), 4 * (size_t)A); p->n++; }
static void pool_copy(Pool *dst, const Pool *src, int i) { if (dst->n >= dst->cap) return; memcpy(dst->cfg + (size_t)NW * dst->n, src->cfg + (size_t)NW * i, 8 * NW);
  dst->pop[dst->n] = src->pop[i]; dst->clock[dst->n] = src->clock[i]; if (PATHS) memcpy(dst->last + (size_t)A * dst->n, src->last + (size_t)A * i, 4 * (size_t)A); dst->n++; }
static void track_last(void) { int f0 = N - A; for (int c = 0; c < A; c++) { u64 w = xa[f0 + c]; while (w) { int j = __builtin_ctzll(w); LAST(j)[c] = lclock[j]; w &= w - 1; } } }

static void cmd_ffs(int M, int delta, int N0, const char *pathfile, int maxpaths, int lamA_in, int lam0_in) {
  int f0 = N - A, pop[64];
  const int TB = 1000, TM = 400, TMAX = 20000;
  init_all();
  for (int g = 0; g < TB; g++) { step(); u64 top = 0; for (int c = f0; c < N; c++) top |= xa[c];
    if (~top) for (int j = 0; j < 64; j++) if (~top >> j & 1) init_lane(j); }
  double s1 = 0, s2 = 0; long ns = 0;
  for (int g = 0; g < TM; g++) { step(); popcounts(xa, f0, N, pop); for (int j = 0; j < 64; j++) { s1 += pop[j]; s2 += (double)pop[j] * pop[j]; ns++; } }
  double mu = s1 / ns, sd = sqrt(s2 / ns - mu * mu);
  int lamA = lamA_in > 0 ? lamA_in : (int)floor(mu + 0.5), lam0 = lam0_in > 0 ? lam0_in : lamA - (int)fmax(2, floor(sd + 0.5));
  printf("# A=%d N=%d mean face pop %.3f sd %.3f (density %.4f) lamA=%d lam0=%d girth^2=%d (v=%d,%d) length=%.3f\n", A, N, mu, sd, mu / A, lamA, lam0,
         VA * VA + VA * VB + VB * VB, VA, VB, LT);
  if (PATHS) lastbuf = malloc(4 * (size_t)A * 64);
  Pool P, Q; pool_init(&P, N0 > M ? N0 : M); pool_init(&Q, N0 > M ? N0 : M);
  /* basin stage */
  int inA[64], burn[64], started[64]; for (int j = 0; j < 64; j++) { inA[j] = 0; burn[j] = 0; lclock[j] = 0; started[j] = 0; }
  double time = 0; long ncross = 0, gb = 0, nextsave = 0;
  while (ncross < N0) {
    step(); gb++; popcounts(xa, f0, N, pop);
    for (int j = 0; j < 64; j++) {
      if (burn[j] > 0) { if (pop[j] == 0) { init_lane(j); burn[j] = TB; } else burn[j]--; continue; }
      if (pop[j] == 0) { init_lane(j); burn[j] = TB; inA[j] = 0; started[j] = 0; continue; }
      if (!started[j]) { if (pop[j] >= lamA) { started[j] = 1; inA[j] = 1; } continue; }   /* clock starts at the first visit to A */
      time += 1;
      if (pop[j] >= lamA) inA[j] = 1;
      else if (pop[j] <= lam0 && inA[j]) { inA[j] = 0; ncross++; lclock[j] = 0;
        if (PATHS) { for (int c = 0; c < A; c++) LAST(j)[c] = ((xa[f0 + c] >> j) & 1) ? 0 : -1; }
        pool_add_lane(&P, j, pop[j]); }
    }
    (void)nextsave;
  }
  double flux = ncross / time, lnk = log(flux);
  printf("# basin: %ld crossings of lam0 in %.0f lane-gens: flux %.6g per gen (ln %.4f)\n", ncross, time, flux, lnk);
  /* stages */
  int lam = lam0, stage = 0; double work = time, tdeath = 0; long ndeath = 0; FILE *pf = NULL; long npaths = 0;
  while (lam > 0) {
    int lnext = lam - delta; if (lnext < 0) lnext = 0;
    Q.n = 0; long launched = 0, succ = 0, fail = 0, cens = 0; double dur = 0;
    int act[64], age[64]; int nact = 0;
    for (int j = 0; j < 64; j++) act[j] = 0;
    if (lnext == 0 && pathfile && !pf) { pf = fopen(pathfile, "w"); }
    for (;;) {
      /* (re)load idle lanes */
      for (int j = 0; j < 64; j++) while (!act[j] && launched < M) {
        int i = (int)(rnd() % (u64)P.n); launched++;
        if (P.pop[i] <= lnext && lnext > 0) { succ++; pool_copy(&Q, &P, i); continue; }
        load_lane(j, P.cfg + (size_t)NW * i); act[j] = 1; age[j] = 0; nact++;
        lclock[j] = P.clock[i] - LA; if (PATHS) memcpy(LAST(j), P.last + (size_t)A * i, 4 * (size_t)A);
      }
      if (nact == 0) break;
      step(); for (int j = 0; j < 64; j++) lclock[j]++;
      if (PATHS) track_last();
      popcounts(xa, f0, N, pop);
      for (int j = 0; j < 64; j++) if (act[j]) {
        age[j]++; dur += 1;
        if (age[j] <= LA) continue;
        int done = 0;
        if (pop[j] <= lnext) { succ++; done = 1; if (lnext == 0) { tdeath += lclock[j]; ndeath++; }
          if (lnext > 0) pool_add_lane(&Q, j, pop[j]);
          else if (pf && npaths < maxpaths) { fprintf(pf, "%d", lclock[j]); for (int c = 0; c < A; c++) { int v = LAST(j)[c]; fprintf(pf, " %d", v < 0 ? -1 : lclock[j] - v); } fputc('\n', pf); npaths++; } }
        else if (pop[j] >= lamA) { fail++; done = 1; }
        else if (age[j] > TMAX) { cens++; done = 1; }
        if (done) { act[j] = 0; nact--; }
      }
    }
    double p = (double)succ / M; work += dur;
    printf("stage %d: lam %d -> %d  p = %.5f  (succ %ld fail %ld cens %ld; mean dur %.1f; pool %d)\n", stage, lam, lnext, p, succ, fail, cens, dur / M, Q.n);
    fflush(stdout);
    if (succ == 0) { printf("RESULT FAILED at stage %d\n", stage); return; }
    lnk += log(p);
    Pool t = P; P = Q; Q = t; lam = lnext; stage++;
  }
  if (pf) fclose(pf);
  printf("RESULT h=%d k=%d d=%d nl=%d ndice=%d A=%d M=%d delta=%d lamA=%d lam0=%d lnflux=%.4f lntau_face=%.4f work=%.3g tdip=%.1f\n", H_, K_, D_, NL, NDICE, A, M, delta, lamA, lam0,
         log(flux), -lnk, work, ndeath ? tdeath / ndeath : 0.0);
}

/* ---- clone test: how much of a death is decided when the look-ahead population first crosses lam? ----
 * n0 crossing states (first crossing of lam since the last visit to lamA), each copied into 64 lanes with
 * independent dice and run until the face is empty or back at lamA.  Prints the histogram of deaths out of 64. */
static void cmd_clone(int lamA, int lam, int n0) {
  int f0 = N - A, pop[64]; init_all();
  for (int g = 0; g < 1000; g++) step();
  int inA[64]; for (int j = 0; j < 64; j++) inA[j] = 0;
  u64 *pool = malloc(8 * (size_t)NW * n0); int n = 0; double time = 0;
  while (n < n0) { step(); popcounts(xa, f0, N, pop); time += 64;
    for (int j = 0; j < 64 && n < n0; j++) { if (pop[j] == 0) { init_lane(j); inA[j] = 0; continue; }
      if (pop[j] >= lamA) inA[j] = 1; else if (pop[j] <= lam && inA[j]) { inA[j] = 0; save_lane(j, pool + (size_t)NW * n); n++; } } }
  long hist[65]; memset(hist, 0, sizeof hist); double sq = 0, sq2 = 0;
  for (int i = 0; i < n0; i++) {
    for (int j = 0; j < 64; j++) load_lane(j, pool + (size_t)NW * i);
    u64 open = ~0ULL; int k = 0;
    for (int g = 1; g <= 5000 && open; g++) { step(); if (g <= LA) continue; popcounts(xa, f0, N, pop);
      for (int j = 0; j < 64; j++) if (open >> j & 1) { if (pop[j] == 0) { k++; open &= ~(1ULL << j); } else if (pop[j] >= lamA) open &= ~(1ULL << j); } }
    hist[k]++; sq += k / 64.0; sq2 += (k / 64.0) * (k / 64.0);
  }
  double q = sq / n0, v = sq2 / n0 - q * q;
  printf("CLONE A=%d lamA=%d lam=%d n0=%d flux=%.4g mean q=%.5g  var(q)=%.4g  var/(q(1-q))=%.3f  (1 = decided at the crossing, 0 = nothing decided)\n",
         A, lamA, lam, n0, n0 / time, q, v, v / (q * (1 - q)));
  printf("deaths out of 64 clones: count\n"); for (int k = 0; k <= 64; k++) if (hist[k]) printf("  %d: %ld\n", k, hist[k]);
}

/* ---- stationary probability that a band right round the girth is empty (brute force, living tube) ----
 * bins of 0.5 lattice units along the axis; a window of m bins is empty when no face cell in it is alive.
 * Counts, per window position and generation, P(empty) and the rate at which empty windows appear. */
static void cmd_bandp(long gens, int T0, int wm) {
  const double BW = 0.5; int nbin = (int)ceil(LT / BW - 1e-9); int nf = NDICE ? 1 : 2;
  int *bin = malloc(sizeof(int) * N), *bcnt = calloc(nbin, sizeof(int));
  for (int c = 0; c < N; c++) { int b = (int)(XI[c] / BW); if (b >= nbin) b = nbin - 1; bin[c] = b; if (c >= N - A) bcnt[b]++; }
  if (wm > nbin - 2) wm = nbin - 2;
  double *cnt = calloc(wm + 1, sizeof(double)), *births = calloc(wm + 1, sizeof(double)), samples = 0;
  u64 *prev = calloc((size_t)2 * (wm + 1) * nbin, 8), *any = malloc(8 * nbin), *e = malloc(8 * nbin);
  init_all(); for (int g = 0; g < T0; g++) step();
  long restarts = 0; int cool[64]; for (int j = 0; j < 64; j++) cool[j] = 0;
  for (long g = 0; g < gens; g++) {
    step(); u64 ok = 0; for (int j = 0; j < 64; j++) { if (cool[j] > 0) cool[j]--; else ok |= 1ULL << j; }
    for (int f = 0; f < nf; f++) {
      int c0 = f ? 0 : N - A; memset(any, 0, 8 * nbin); u64 all = 0;
      for (int c = c0; c < c0 + A; c++) { any[bin[c]] |= xa[c]; all |= xa[c]; }
      if (~all) for (int j = 0; j < 64; j++) if (~all >> j & 1) { init_lane(j); cool[j] = T0; ok &= ~(1ULL << j); restarts++; }
      for (int b = 0; b < nbin; b++) e[b] = ok;
      for (int m = 1; m <= wm; m++) { u64 *pv = prev + ((size_t)f * (wm + 1) + m) * nbin;
        for (int b = 0; b < nbin; b++) { e[b] &= ~any[(b + m - 1) % nbin]; cnt[m] += __builtin_popcountll(e[b]); births[m] += __builtin_popcountll(e[b] & ~pv[b]); pv[b] = e[b]; } }
    }
    samples += (double)__builtin_popcountll(ok) * nf * nbin;
  }
  printf("# bandp: (%d,%d),(0,%d) nl=%d ndice=%d A=%d girth^2=%d length=%.3f gens=%ld lanes=64 faces=%d bins=%d (cells per bin:", H_, K_, D_, NL, NDICE, A, VA * VA + VA * VB + VB * VB, LT, gens, nf, nbin);
  for (int b = 0; b < nbin && b < 6; b++) printf(" %d", bcnt[b]); printf(" ...) restarts=%ld samples=%.4g\n", restarts, samples);
  printf("# width(units) cells~ count  P(empty)  -lnP  err  appearances  mean_duration(gens)\n");
  for (int m = 1; m <= wm; m++) if (cnt[m] > 0) printf("%.1f %.1f %.0f %.4g %.4f %.4f %.0f %.3f\n", m * BW, (double)A * m * BW / LT, cnt[m], cnt[m] / samples, -log(cnt[m] / samples),
    1 / sqrt(births[m] > 0 ? births[m] : 1), births[m], cnt[m] / (births[m] > 0 ? births[m] : 1));
}

/* ---- band experiment ---- */
static void cmd_band(double width, int T, int reps, int depth) {
  int f0 = N - A; const double BW = 0.5; int nbin = (int)ceil(LT / BW - 1e-9);
  int *bin = malloc(sizeof(int) * A), *bcnt = calloc(nbin, sizeof(int));
  for (int c = 0; c < A; c++) { int b = (int)(XI[f0 + c] / BW); if (b >= nbin) b = nbin - 1; bin[c] = b; bcnt[b]++; }
  int tstep = T > 400 ? T / 200 : 1; int nt = T / tstep + 1;
  double *prof = calloc((size_t)nt * nbin, sizeof(double)); double *bandpop = calloc(nt, sizeof(double)), *gaplen = calloc(nt, sizeof(double)), *nheal = calloc(nt, sizeof(double)), *ndead = calloc(nt, sizeof(double));
  int nband = 0; for (int c = 0; c < A; c++) if (XI[f0 + c] < width) nband++;
  long nl = 0;
  for (int r = 0; r < reps; r++) {
    init_all(); for (int g = 0; g < 800; g++) step();
    for (int dl = 0; dl < depth; dl++) { int l0 = N - A * (dl + 1); for (int c = 0; c < A; c++) if (XI[l0 + c] < width) xa[l0 + c] = 0; }
    u64 healed = 0;
    for (int g = 0; g <= T; g++) {
      if (g % tstep == 0) { int ti = g / tstep;
        u64 any[nbin]; memset(any, 0, sizeof any); u64 top = 0;
        for (int c = 0; c < A; c++) { u64 w = xa[f0 + c]; prof[(size_t)ti * nbin + bin[c]] += __builtin_popcountll(w); any[bin[c]] |= w; top |= w;
          if (XI[f0 + c] < width) bandpop[ti] += __builtin_popcountll(w); }
        ndead[ti] += __builtin_popcountll(~top);
        for (int j = 0; j < 64; j++) { /* longest cyclic run of empty bins */
          int best = 0, run = 0; for (int b = 0; b < 2 * nbin; b++) { if (!((any[b % nbin] >> j) & 1)) { run++; if (run > best) best = run; } else run = 0; }
          if (best > nbin) best = nbin; gaplen[ti] += best * BW; if (best == 0) healed |= 1ULL << j; }
        nheal[ti] += __builtin_popcountll(healed);
      }
      if (g < T) step();
    }
    nl += 64;
  }
  printf("# band: A=%d girth^2=%d length=%.3f width=%.2f (%d face cells killed, depth %d) lanes=%ld binwidth=%.2f\n", A, VA * VA + VA * VB + VB * VB, LT, width, nband, depth, nl, BW);
  printf("# t bandpop/ncells gaplen(longest run of empty 0.5-bins) frac_nogap frac_face_dead | profile density per bin\n");
  for (int ti = 0; ti < nt; ti++) { printf("%d %.4f %.3f %.4f %.4f |", ti * tstep, bandpop[ti] / nl / (nband ? nband : 1), gaplen[ti] / nl, nheal[ti] / nl, ndead[ti] / nl);
    for (int b = 0; b < nbin; b++) printf(" %.3f", prof[(size_t)ti * nbin + b] / nl / (bcnt[b] ? bcnt[b] : 1)); putchar('\n'); }
}

int main(int argc, char **argv) {
  if (argc < 6) { fprintf(stderr, "usage: see header\n"); return 2; }
  const char *cmd = argv[1]; H_ = atoi(argv[2]); K_ = atoi(argv[3]); D_ = atoi(argv[4]); NL = atoi(argv[5]);
  if (!strcmp(cmd, "trace")) { NDICE = 0; seedrng(strtoull(argv[6], 0, 10)); build(argc > 8 && !strcmp(argv[8], "bad")); cmd_trace(atoi(argv[7])); return 0; }
  if (!strcmp(cmd, "geom")) { NDICE = 0; build(0); printf("# A=%d girth vector (%d,%d) girth %.4f length %.4f\n# face-cell-index a x y xi eta\n", A, VA, VB, GIRTH, LT);
    for (int a = 0; a < 3; a++) for (int x = 0; x < H_; x++) for (int y = 0; y < D_; y++) { int c = idx(NL - 1, a, x, y); printf("%d %d %d %d %.4f %.4f\n", c - (N - A), a, x, y, XI[c], ETA[c]); } return 0; }
  NDICE = atoi(argv[6]); seedrng(strtoull(argv[7], 0, 10)); build(0); NW = (N + 63) / 64;
  if (!strcmp(cmd, "brute")) cmd_brute(atoi(argv[8]), atol(argv[9]), argc > 10 ? fopen(argv[10], "w") : NULL);
  else if (!strcmp(cmd, "ffs")) { const char *pfile = argc > 11 ? argv[11] : NULL; if (pfile && !strcmp(pfile, "-")) pfile = NULL; PATHS = pfile != NULL;
    cmd_ffs(atoi(argv[8]), atoi(argv[9]), atoi(argv[10]), pfile, argc > 12 ? atoi(argv[12]) : 1000, argc > 13 ? atoi(argv[13]) : 0, argc > 14 ? atoi(argv[14]) : 0); }
  else if (!strcmp(cmd, "clone")) cmd_clone(atoi(argv[8]), atoi(argv[9]), atoi(argv[10]));
  else if (!strcmp(cmd, "bandp")) cmd_bandp(atol(argv[8]), atoi(argv[9]), argc > 10 ? atoi(argv[10]) : 12);
  else if (!strcmp(cmd, "band")) cmd_band(atof(argv[8]), atoi(argv[9]), atoi(argv[10]), argc > 11 ? atoi(argv[11]) : 1);
  else { fprintf(stderr, "unknown command\n"); return 2; }
  return 0;
}
