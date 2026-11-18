// rh.c -- ref-hull: an independent hull stepper and a splice-FFS sampler for gump's hull faces.
// Written from reference/oracle.py and docs/AUTOMATON.md alone (referee code; see README.md).
//   rh val R SEED GENS NEG            dump states of three lanes for validate.py (NEG=1: one swapped neighbour)
//   rh run R SEED M NS LAG STEP       one replication of the sampler; prints one RESULT line
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define W 4
#define NL (64*W)
#define MAXC 5400
#define KH 16
typedef uint64_t v4 __attribute__((vector_size(32)));

static int R, N, A, LAG = 2, nw;
static int cx[MAXC], cy[MAXC], cz[MAXC], nb[MAXC][12];
static int fc[8][256], nf[8];
static unsigned char deep[MAXC];
static uint64_t S[KH][MAXC + 1][W] __attribute__((aligned(32)));
static int idx[47][47][47];

static uint64_t rs[4];
static inline uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static inline uint64_t rnd(void) {
  uint64_t r = rotl(rs[0] + rs[3], 23) + rs[0], t = rs[1] << 17;
  rs[2] ^= rs[0]; rs[3] ^= rs[1]; rs[1] ^= rs[2]; rs[0] ^= rs[3]; rs[2] ^= t; rs[3] = rotl(rs[3], 45);
  return r;
}
static void seedrng(uint64_t s) {
  for (int i = 0; i < 4; i++) {
    s += 0x9E3779B97F4A7C15ULL; uint64_t z = s;
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL; z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL; rs[i] = z ^ (z >> 31);
  }
}
static inline double urand(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static inline long rint_(long n) { return (long)(urand() * n); }

static void build(int neg) {
  N = 0;
  for (int x = -R; x <= R; x++) for (int y = -R; y <= R; y++) for (int z = -R; z <= R; z++) {
    idx[x + R][y + R][z + R] = -1;
    if (abs(x) + abs(y) + abs(z) > R) continue;
    if ((abs(x) & 1) + (abs(y) & 1) + (abs(z) & 1) != 1) continue;
    idx[x + R][y + R][z + R] = N; cx[N] = x; cy[N] = y; cz[N] = z; N++;
  }
  for (int c = 0; c < N; c++) {
    int p[3] = {cx[c], cy[c], cz[c]};
    int a = (abs(p[0]) & 1) ? 0 : (abs(p[1]) & 1) ? 1 : 2;
    int b = (a == 0) ? 1 : 0, cc = (a == 2) ? 1 : 2;
    int k = 0, offs[12][3];
    for (int sb = 2; sb >= -2; sb -= 4) for (int sc = 2; sc >= -2; sc -= 4) {
      offs[k][0] = offs[k][1] = offs[k][2] = 0; offs[k][b] = sb; offs[k][cc] = sc; k++;
    }
    for (int sa = 1; sa >= -1; sa -= 2) for (int ti = 0; ti < 2; ti++) for (int st = 1; st >= -1; st -= 2) {
      int t = ti ? cc : b;
      offs[k][0] = offs[k][1] = offs[k][2] = 0; offs[k][a] = sa; offs[k][t] = st; k++;
    }
    for (k = 0; k < 12; k++) {
      int q[3] = {p[0] + offs[k][0], p[1] + offs[k][1], p[2] + offs[k][2]};
      int id = -1;
      if (abs(q[0]) + abs(q[1]) + abs(q[2]) <= R) id = idx[q[0] + R][q[1] + R][q[2] + R];
      nb[c][k] = id < 0 ? N : id;   // outside the hull: the dead dummy cell N
    }
    deep[c] = (p[0] + p[1] + p[2] <= R - 4 * LAG - 2);
  }
  for (int f = 0; f < 8; f++) {
    nf[f] = 0;
    int d[3] = {(f & 1) ? -1 : 1, (f & 2) ? -1 : 1, (f & 4) ? -1 : 1};
    for (int c = 0; c < N; c++) if (d[0] * cx[c] + d[1] * cy[c] + d[2] * cz[c] == R) fc[f][nf[f]++] = c;
  }
  A = nf[0];
  nw = (N + 63) / 64;
  if (neg) {  // negative control: one neighbour of one central cell replaced by a non-neighbour
    int c = idx[R + 1][R][R], o = idx[R + 5][R][R];
    fprintf(stderr, "NEG: cell %d nb[0] %d -> %d\n", c, nb[c][0], o);
    nb[c][0] = o;
  }
}

static inline v4 ld(const uint64_t *p) { v4 v; memcpy(&v, p, 32); return v; }
#define FA(x, y, z, sum, car) { v4 t_ = (x) ^ (y); sum = t_ ^ (z); car = ((x) & (y)) | ((z) & t_); }
static void step(int from, int to) {
  uint64_t (*s)[W] = S[from], (*d)[W] = S[to];
  for (int c = 0; c < N; c++) {
    const int *n = nb[c];
    v4 a0 = ld(s[n[0]]), a1 = ld(s[n[1]]), a2 = ld(s[n[2]]), a3 = ld(s[n[3]]), a4 = ld(s[n[4]]), a5 = ld(s[n[5]]);
    v4 a6 = ld(s[n[6]]), a7 = ld(s[n[7]]), a8 = ld(s[n[8]]), a9 = ld(s[n[9]]), a10 = ld(s[n[10]]), a11 = ld(s[n[11]]);
    v4 s1, c1, s2, c2, s3, c3, s4, c4, t1, d1, u1, e1, u2, e2, b2, b3;
    FA(a0, a1, a2, s1, c1) FA(a3, a4, a5, s2, c2) FA(a6, a7, a8, s3, c3) FA(a9, a10, a11, s4, c4)
    FA(s1, s2, s3, t1, d1)
    v4 b0 = t1 ^ s4, d2 = t1 & s4;
    FA(c1, c2, c3, u1, e1) FA(c4, d1, d2, u2, e2)
    v4 b1 = u1 ^ u2, e3 = u1 & u2;
    FA(e1, e2, e3, b2, b3)
    v4 x = ld(s[c]);
    v4 nx = ~b3 & ((b2 & ~b1) | (x & ~b2 & b1 & b0));   // n in {4,5}, or alive and n == 3
    memcpy(d[c], &nx, 32);
  }
}

static int P[NL];
static uint64_t ne[8][W], emp[W];
static void facestats(int h) {
  memset(P, 0, sizeof P);
  for (int f = 0; f < 8; f++) {
    for (int w = 0; w < W; w++) ne[f][w] = 0;
    for (int i = 0; i < nf[f]; i++) { const uint64_t *q = S[h][fc[f][i]]; for (int w = 0; w < W; w++) ne[f][w] |= q[w]; }
  }
  for (int i = 0; i < nf[0]; i++) {
    const uint64_t *q = S[h][fc[0][i]];
    for (int w = 0; w < W; w++) { uint64_t x = q[w]; while (x) { P[w * 64 + __builtin_ctzll(x)]++; x &= x - 1; } }
  }
  for (int w = 0; w < W; w++) { emp[w] = 0; for (int f = 0; f < 8; f++) emp[w] |= ~ne[f][w]; }
}
static inline int anyemp(int l) { return (emp[l >> 6] >> (l & 63)) & 1; }
static inline int nempty(int l) { int k = 0; for (int f = 0; f < 8; f++) if (!((ne[f][l >> 6] >> (l & 63)) & 1)) k++; return k; }
static inline void setbit(int h, int c, int l, int b) {
  uint64_t m = 1ULL << (l & 63);
  if (b) S[h][c][l >> 6] |= m; else S[h][c][l >> 6] &= ~m;
}
static double DENS = 0.35;
static void soup(int h, int l) { for (int c = 0; c < N; c++) setbit(h, c, l, urand() < DENS); }
static void extract(int h, int l, uint64_t *cfg) {
  memset(cfg, 0, nw * 8);
  for (int c = 0; c < N; c++) if ((S[h][c][l >> 6] >> (l & 63)) & 1) cfg[c >> 6] |= 1ULL << (c & 63);
}
static void loadsplice(int h, int l, const uint64_t *par, const uint64_t *don) {
  for (int c = 0; c < N; c++) { const uint64_t *src = deep[c] ? don : par; setbit(h, c, l, (src[c >> 6] >> (c & 63)) & 1); }
}
// flips mode: the parent's stored state with m distinct cells of the set FS toggled
static int FS[MAXC], nFS, mflip;
static void loadflip(int h, int l, const uint64_t *par) {
  for (int c = 0; c < N; c++) setbit(h, c, l, (par[c >> 6] >> (c & 63)) & 1);
  int ch[512];
  for (int i = 0; i < mflip; i++) {
    int c, dup;
    do { c = FS[rint_(nFS)]; dup = 0; for (int k = 0; k < i; k++) if (ch[k] == c) dup = 1; } while (dup);
    ch[i] = c; S[h][c][l >> 6] ^= 1ULL << (l & 63);
  }
}

typedef struct { uint64_t *cfg; unsigned char *pc, *mf; long n, seen, cap; } Store;
static void st_init(Store *s, long cap) { s->cfg = malloc((size_t)cap * nw * 8); s->pc = malloc(cap); s->mf = malloc(cap); s->n = s->seen = 0; s->cap = cap; }
static void st_add(Store *s, int h, int l, int pc, int mf) {   // reservoir sampling beyond the cap
  long k;
  if (s->n < s->cap) k = s->n++; else { k = rint_(s->seen + 1); if (k >= s->cap) { s->seen++; return; } }
  s->seen++;
  extract(h, l, s->cfg + (size_t)k * nw); s->pc[k] = pc; s->mf[k] = mf > 255 ? 255 : mf;
}

int main(int argc, char **argv) {
  if (argc < 5) { fprintf(stderr, "usage\n"); return 1; }
  R = atoi(argv[2]); long seed = atol(argv[3]);
  if (!strcmp(argv[1], "val")) {
    int gens = atoi(argv[4]), neg = argc > 5 ? atoi(argv[5]) : 0;
    build(neg); seedrng(seed);
    printf("%d %d\n", N, R);
    for (int c = 0; c < N; c++) printf("%d %d %d\n", cx[c], cy[c], cz[c]);
    for (int l = 0; l < NL; l++) soup(0, l);
    int lanes[3] = {0, 97, 255}, cur = 0; uint64_t cfg[(MAXC + 63) / 64];
    for (int g = 0; g <= gens; g++) {
      for (int i = 0; i < 3; i++) {
        extract(cur, lanes[i], cfg);
        printf("%d %d ", g, lanes[i]); for (int k = 0; k < nw; k++) printf("%016llx", (unsigned long long)cfg[k]); printf("\n");
      }
      int nx = (cur + 1) % KH; step(cur, nx); cur = nx;
    }
    return 0;
  }

  if (!strcmp(argv[1], "nu")) {   // plain running: dip rates at every level, all eight faces; rh nu R SEED GENS LAMA
    long G = atol(argv[4]); int lamA = atoi(argv[5]); int WIN = argc > 6 ? atoi(argv[6]) : 3; long nover = 0;
    build(0); seedrng(seed * 104729 + R);
    static int age[NL], fl[NL][8], cm[NL][8], P8[NL][8];
    static int since[NL][8]; static long Db[400]; for (int l = 0; l < NL; l++) for (int f = 0; f < 8; f++) since[l][f] = 99;
    static long D[400]; long expo = 0, deaths = 0, nP = 0, fdead = 0; double sP = 0, sP2 = 0;
    for (int l = 0; l < NL; l++) { soup(0, l); age[l] = 0; for (int f = 0; f < 8; f++) { fl[l][f] = 0; cm[l][f] = lamA; } }
    int cur = 0; clock_t t0 = clock();
    for (long g = 1; g <= G; g++) {
      int nx = (cur + 1) % KH; step(cur, nx); cur = nx;
      for (int f = 0; f < 8; f++) {   // bit-sliced population counter of face f
        v4 cnt[8]; for (int b = 0; b < 8; b++) cnt[b] = (v4){0, 0, 0, 0};
        for (int i = 0; i < nf[f]; i++) { v4 x = ld(S[cur][fc[f][i]]); for (int b = 0; b < 8; b++) { v4 t = cnt[b] & x; cnt[b] ^= x; x = t; } }
        uint64_t pl[8][W]; for (int b = 0; b < 8; b++) memcpy(pl[b], &cnt[b], 32);
        for (int l = 0; l < NL; l++) { int p = 0; for (int b = 0; b < 8; b++) p |= (int)((pl[b][l >> 6] >> (l & 63)) & 1) << b; P8[l][f] = p; }
      }
      for (int l = 0; l < NL; l++) {
        age[l]++;
        int counted = age[l] > 200, anye = 0;
        for (int f = 0; f < 8; f++) if (P8[l][f] == 0) anye = 1;
        if (counted) { expo++; for (int f = 0; f < 8; f++) { int p = P8[l][f]; sP += p; sP2 += (double)p * p; nP++; if (10 * p >= 7 * A) nover++; } }
        if (anye) {
          if (counted) { deaths++; for (int f = 0; f < 8; f++) { if (P8[l][f] == 0) fdead++; if (P8[l][f] == 0 && fl[l][f]) { D[0]++; D[cm[l][f]]--; if (since[l][f] <= WIN) { Db[0]++; Db[cm[l][f]]--; } } } }
          soup(cur, l); age[l] = 0; for (int f = 0; f < 8; f++) { fl[l][f] = 0; cm[l][f] = lamA; since[l][f] = 99; }
        } else if (age[l] >= 100) {
          for (int f = 0; f < 8; f++) {
            int p = P8[l][f];
            if (p >= lamA) { fl[l][f] = 1; cm[l][f] = lamA; }
            else if (fl[l][f] && p < cm[l][f]) { if (counted) { D[p]++; D[cm[l][f]]--; if (since[l][f] <= WIN) { Db[p]++; Db[cm[l][f]]--; } } cm[l][f] = p; }
            if (10 * p >= 7 * A) since[l][f] = 0; else if (since[l][f] < 99) since[l][f]++;
          }
        }
      }
    }
    printf("NU R %d seed %ld A %d lamA %d gens %ld expo %ld deaths %ld sumP %.1f sumP2 %.1f nP %ld sec %.1f cross", R, seed, A, lamA, G, expo, deaths, sP, sP2, nP,
           (double)(clock() - t0) / CLOCKS_PER_SEC);
    long c = 0; for (int L = 0; L < lamA; L++) { c += D[L]; printf(" %ld", c); }
    printf("\n");
    printf("NUB R %d win %d seed %ld A %d lamA %d expo %ld nover %ld deaths %ld cross", R, WIN, seed, A, lamA, expo, nover, deaths);
    c = 0; for (int L = 0; L < lamA; L++) { c += D[L]; printf(" %ld", c); }
    printf(" bust"); c = 0; for (int L = 0; L < lamA; L++) { c += Db[L]; printf(" %ld", c); }
    printf("\n");
    fprintf(stderr, "TIES R %d seed %ld first deaths %ld faces empty at those generations %ld ratio %.5f\n", R, seed, deaths, fdead, deaths ? (double)fdead / deaths : 0.0);
    return 0;
  }
  if (!strcmp(argv[1], "life")) {   // rh life R SEED GENS TMAX DENS CENSOR : hazard of the first empty face by age of the soup
    long G = atol(argv[4]); int TMAX = atoi(argv[5]); DENS = atof(argv[6]); int censor = atoi(argv[7]);
    build(0); seedrng(seed * 2713 + R);
    static long dth[4100], rsk[4100], per[4100]; long facesum = 0, ndeath = 0, reachT = 0, tie2 = 0, lateF = 0, lateD = 0, lateT = 0; double sP = 0; long nPp = 0;
    static int age[NL];
    if (TMAX > 4000) return 1;
    for (int l = 0; l < NL; l++) { soup(0, l); age[l] = 0; }
    int cur = 0; static const int lags[6] = {7, 8, 9, 10, 11, 12};
    for (long g = 1; g <= G; g++) {
      int nx = (cur + 1) % KH; step(cur, nx); cur = nx; facestats(cur);
      uint64_t pm[W] = {0, 0, 0, 0};
      if (censor) for (int q = 0; q < 6; q++) {
        v4 d = (v4){0, 0, 0, 0}; int old = (cur - lags[q] + KH) % KH;
        for (int c = 0; c < N; c++) d |= ld(S[cur][c]) ^ ld(S[old][c]);
        uint64_t w[4]; memcpy(w, &d, 32); for (int i = 0; i < W; i++) pm[i] |= ~w[i];
      }
      for (int l = 0; l < NL; l++) {
        int a = ++age[l]; rsk[a]++;
        if (a > 40 && a <= 100) { sP += P[l]; nPp++; }
        int k = anyemp(l) ? nempty(l) : 0;
        if (k) { dth[a]++; ndeath++; facesum += k; if (k >= 2) tie2++; if (a > 40) { lateD++; lateF += k; if (k >= 2) lateT++; } soup(cur, l); age[l] = 0; }
        else if (censor && a > 12 && ((pm[l >> 6] >> (l & 63)) & 1)) { per[a]++; soup(cur, l); age[l] = 0; }
        else if (a >= TMAX) { reachT++; soup(cur, l); age[l] = 0; }
      }
    }
    long nper = 0; for (int a = 0; a <= TMAX; a++) nper += per[a];
    printf("# life hull R %d A %d N %d soup %.2f censor %d seed %ld: first deaths %ld, faces empty per first death %.4f, share with two or more %.4f; after generation 40: %.4f and %.4f; censored as periodic %ld; reached TMAX %ld; face density in generations 41-100: %.4f\n",
           R, A, N, DENS, censor, seed, ndeath, (double)facesum / ndeath, (double)tie2 / ndeath, lateD ? (double)lateF / lateD : 0.0, lateD ? (double)lateT / lateD : 0.0, nper, reachT, nPp ? sP / nPp / A : 0.0);
    int step_ = TMAX <= 400 ? 20 : TMAX / 10;
    for (int a0 = 1; a0 <= TMAX; a0 += step_) {
      long d = 0, e = 0, pp = 0; for (int a = a0; a < a0 + step_ && a <= TMAX; a++) { d += dth[a]; e += rsk[a]; pp += per[a]; }
      if (d > 0) printf("  generations %4d..%4d: deaths %10ld exposure %12ld periodic %8ld  ln(8E/D) %.4f +- %.4f\n", a0, a0 + step_ - 1, d, e, pp, log(8.0 * e / d), 1 / sqrt((double)d));
    }
    return 0;
  }
  if (!strcmp(argv[1], "hole")) {   // rh hole R SEED GENS : empty rhombi of class-P unit cells on the hull's faces (all 48 images pooled)
    long G = atol(argv[4]); DENS = 0.5; build(0); seedrng(seed * 911 + R);
    int kk = (R + 1) / 2;
    enum { NT = 8 };
    static const char *tname[NT] = {"interior(margin>=2) 2x2", "interior(margin>=2) 2x3", "interior(margin>=2) 3x3", "rim 3x3 (first row on a rim, other rims >=3 rows away)", "corner 2x2", "corner 2x3", "corner 3x3", "interior(margin>=2) 1x1"};
    static const int ta[NT] = {2, 2, 3, 3, 2, 2, 3, 1}, tb[NT] = {2, 3, 3, 3, 2, 3, 3, 1};
    static int img[200000][28], imgn[200000], imgt[200000]; int nimg = 0; long nimgt[NT] = {0};
    static const int perms[6][3] = {{0, 1, 2}, {0, 2, 1}, {1, 0, 2}, {1, 2, 0}, {2, 0, 1}, {2, 1, 0}};
    for (int t = 0; t < NT; t++) for (int I0 = 0; I0 < kk; I0++) for (int J0 = 0; J0 < kk; J0++) {
      int a = ta[t], b = tb[t];
      int mmin = kk - 1 - (I0 + a - 1) - (J0 + b - 1); if (mmin < 0) continue;
      int ok;
      if (t <= 2 || t == 7) ok = (I0 >= 2 && J0 >= 2 && mmin >= 2);
      else if (t == 3) ok = (J0 == 0 && I0 >= 3 && mmin >= 3);
      else ok = (I0 == 0 && J0 == 0);
      if (!ok) continue;
      for (int sg = 0; sg < 8; sg++) for (int pi = 0; pi < 6; pi++) {
        int nc = 0;
        for (int i = I0; i < I0 + a; i++) for (int j = J0; j < J0 + b; j++) {
          int m = kk - 1 - i - j; int c0[3] = {2 * i, 2 * m, 2 * j};
          for (int q = 0; q < 3; q++) {
            int p[3] = {c0[0], c0[1], c0[2]}; p[q] += 1;
            int t3[3] = {p[perms[pi][0]], p[perms[pi][1]], p[perms[pi][2]]};
            if (sg & 1) t3[0] = -t3[0]; if (sg & 2) t3[1] = -t3[1]; if (sg & 4) t3[2] = -t3[2];
            int id = idx[t3[0] + R][t3[1] + R][t3[2] + R];
            if (id < 0) { fprintf(stderr, "bad patch cell\n"); return 2; }
            img[nimg][nc++] = id;
          }
        }
        imgn[nimg] = nc; imgt[nimg] = t; nimg++; nimgt[t]++;
      }
    }
    static long cnt[NT][8]; long gens = 0, refills = 0;
    for (int l = 0; l < NL; l++) soup(0, l);
    int cur = 0;
    for (long g = 1; g <= G; g++) {
      int nx = (cur + 1) % KH; step(cur, nx); cur = nx;
      if (g % 64 == 0) { facestats(cur); for (int l = 0; l < NL; l++) if (anyemp(l)) { soup(cur, l); refills++; } }
      if (g <= 500) continue;
      gens++;
      for (int q = 0; q < nimg; q++) {
        v4 o = ld(S[cur][img[q][0]]); for (int i = 1; i < imgn[q]; i++) o |= ld(S[cur][img[q][i]]);
        v4 e = ~o; uint64_t w[4]; memcpy(w, &e, 32);
        for (int i = 0; i < 4; i++) if (w[i]) { cnt[imgt[q]][2 * i] += __builtin_popcountll(w[i] & 0xffffffffULL); cnt[imgt[q]][2 * i + 1] += __builtin_popcountll(w[i] >> 32); }
      }
    }
    for (int t = 0; t < NT; t++) {
      printf("HOLE hull R %d seed %ld gens %ld refills %ld type %d images %ld denom %ld counts", R, seed, gens, refills, t, nimgt[t], gens * 32 * nimgt[t]);
      for (int q = 0; q < 8; q++) printf(" %ld", cnt[t][q]);
      printf(" # %s\n", tname[t]);
    }
    return 0;
  }
  // ---- run ----
  long M = atol(argv[4]); long NS = atol(argv[5]); LAG = atoi(argv[6]); int STEP = atoi(argv[7]);
  int PMODE = argc > 8 ? atoi(argv[8]) : 0, DIV = argc > 9 ? atoi(argv[9]) : 16, DL = argc > 10 ? atoi(argv[10]) : 1;
  if (LAG + 1 > KH) return 1;
  build(0); seedrng(seed * 7919 + R);
  nFS = 0;
  for (int c = 0; c < N; c++) { int sd = cx[c] + cy[c] + cz[c]; if (sd <= R - 4 * LAG - 2 && sd > R - 4 * LAG - 2 - 2 * DL) FS[nFS++] = c; }
  mflip = (PMODE == 2) ? DIV : (nFS + DIV - 1) / DIV;   // PMODE 2: DIV is the number of flips itself
  long NS0 = argc > 11 ? atol(argv[11]) : NS; long CAP = NS0 > NS ? NS0 : NS;
  clock_t t0 = clock();
  static int age[NL], flag[NL], plast[NL], mfl[NL];
  int cur = 0; long g = 0;
  for (int l = 0; l < NL; l++) { soup(0, l); age[l] = 0; flag[l] = 0; plast[l] = 0; mfl[l] = 0; }
  double sp = 0, sp2 = 0; long np = 0;
  int lamA = 1 << 30, lam0 = -1, set = 0, counting = 0;
  long expo = 0, ncross = 0, deaths = 0; double deathsw = 0;
  Store a, b; st_init(&a, CAP); st_init(&b, CAP); a.cap = NS0; b.cap = NS;
  long maxg = 2000000000L;
  while (a.seen < NS0 && g < maxg) {
    int nx = (cur + 1) % KH; step(cur, nx); cur = nx; g++; facestats(cur);
    int old = (cur - LAG + KH) % KH;
    int pilot = (g > 200 && g <= 500);
    if (g == 500 + 1 && !set) {
      double m = sp / np, sd = sqrt(sp2 / np - m * m);
      lamA = (int)floor(m + 0.5); lam0 = (int)floor(m - 1.5 * sd + 0.5); set = 1;
      for (int l = 0; l < NL; l++) flag[l] = 0;
      printf("PILOT R %d seed %ld Pbar %.3f sd %.3f lamA %d lam0 %d\n", R, seed, m, sd, lamA, lam0);
    }
    if (g == 601) counting = 1;
    for (int l = 0; l < NL; l++) {
      age[l]++;
      int p = P[l], fall = plast[l] - p; if (fall > mfl[l]) mfl[l] = fall; plast[l] = p;
      int counted = counting && age[l] > 200;
      if (counted) expo++;
      if (pilot && age[l] > 200) { sp += p; sp2 += (double)p * p; np++; }
      if (anyemp(l)) {
        if (counted) { deaths++; if (p == 0) deathsw += 1.0 / nempty(l); }
        if (set && p == 0 && flag[l] && counted) { ncross++; st_add(&a, old, l, p, mfl[l]); }
        soup(cur, l); age[l] = 0; flag[l] = 0; plast[l] = 0; mfl[l] = 0;
      } else if (set && age[l] >= 100) {
        if (p >= lamA) { flag[l] = 1; mfl[l] = 0; }
        else if (p <= lam0 && flag[l]) { flag[l] = 0; if (counted) { ncross++; st_add(&a, old, l, p, mfl[l]); } }
      }
    }
  }
  double phi0 = (double)ncross / expo;
  double tbase = (double)(clock() - t0) / CLOCKS_PER_SEC;
  // levels
  int lev[64], nlev = 0;
  for (int x = lam0; x > 4; x -= STEP) lev[nlev++] = x;
  lev[nlev++] = 0;
  printf("BASE R %d seed %ld gens %ld expo %ld cross %ld phi0 %.6g deaths %ld deathsw %.3f lnTauDirect %.4f t %.1f\n", R, seed, g, expo, ncross, phi0,
         deaths, deathsw, deaths ? log(8.0 * expo / deaths) : 0.0, tbase);
  double lnrate = log(phi0);
  long replaybad = 0, timeouts = 0, trialgens = 0;
  static int act[NL], tage[NL], tpar[NL];
  long hist[256]; memset(hist, 0, sizeof hist); double wbig = 0, wtot = 0;
  Store *sa = &a, *sb = &b;
  for (int i = 0; i + 1 < nlev; i++) {
    int lnext = lev[i + 1], last = (lnext == 0);
    long Ni = sa->n; if (Ni == 0) { lnrate = -1e9; break; }
    long *perm = malloc(Ni * sizeof(long));
    for (long k = 0; k < Ni; k++) perm[k] = k;
    for (long k = Ni - 1; k > 0; k--) { long r = rint_(k + 1), t = perm[k]; perm[k] = perm[r]; perm[r] = t; }
    sb->n = sb->seen = 0; sb->cap = NS;
    long j = 0, nsucc = 0; double sumw = 0; int nact = 0;
    for (int l = 0; l < NL; l++) act[l] = 0;
    for (;;) {
      for (int l = 0; l < NL; l++) if (!act[l] && j < M) {
        long par = perm[j % Ni], don = par;
        if (Ni > 1) while (don == par) don = rint_(Ni);
        if (PMODE == 0) loadsplice(cur, l, sa->cfg + (size_t)par * nw, sa->cfg + (size_t)don * nw);
        else loadflip(cur, l, sa->cfg + (size_t)par * nw);
        act[l] = 1; tage[l] = 0; tpar[l] = par; j++; nact++;
      }
      if (!nact) break;
      int nx = (cur + 1) % KH; step(cur, nx); cur = nx; facestats(cur);
      int old = (cur - LAG + KH) % KH;
      for (int l = 0; l < NL; l++) if (act[l]) {
        tage[l]++; trialgens++;
        if (tage[l] < LAG) continue;
        int p = P[l];
        if (tage[l] == LAG) { if (p != sa->pc[tpar[l]]) replaybad++; plast[l] = p; mfl[l] = sa->mf[tpar[l]]; }
        else { int fall = plast[l] - p; if (fall > mfl[l]) mfl[l] = fall; plast[l] = p; }
        int res = -1; double wt = 1;
        if (p == 0) { res = 1; if (last) wt = 1.0 / nempty(l); }
        else if (anyemp(l)) res = 0;
        else if (p <= lnext) res = 1;
        else if (p >= lamA) res = 0;
        else if (tage[l] > 20000) { res = 0; timeouts++; }
        if (res < 0) continue;
        if (res == 1) {
          nsucc++; sumw += wt;
          if (!last) st_add(sb, old, l, p, mfl[l]);
          else { hist[mfl[l] > 255 ? 255 : mfl[l]]++; wtot += wt; if (2 * mfl[l] >= A) wbig += wt; }
        }
        act[l] = 0; nact--;
      }
    }
    double ph = sumw / M;
    printf("STAGE R %d seed %ld i %d from %d to %d N %ld M %ld succ %ld p %.6g\n", R, seed, i, lev[i], lnext, Ni, M, nsucc, ph);
    fflush(stdout);
    if (ph <= 0) { lnrate = -1e9; break; }
    lnrate += log(ph);
    free(perm);
    Store *t = sa; sa = sb; sb = t;
  }
  // max-fall summary of sampled deaths
  long nd = 0; double mean = 0; for (int k = 0; k < 256; k++) { nd += hist[k]; mean += (double)k * hist[k]; }
  int q50 = 0, q99 = 0, mx = 0; long acc = 0;
  for (int k = 0; k < 256; k++) { acc += hist[k]; if (!q50 && acc * 2 >= nd) q50 = k; if (!q99 && acc * 100 >= nd * 99) q99 = k; if (hist[k]) mx = k; }
  printf("RESULT R %d seed %ld A %d lamA %d lam0 %d M %ld NS %ld LAG %d STEP %d PMODE %d DIV %d DL %d nS %d mflip %d phi0 %.6g lnTau %.5f deathsSampled %ld bigFallShare %.6g fallMean %.2f fallMed %d fallQ99 %d fallMax %d replaybad %ld timeouts %ld trialgens %ld expo %ld deathsDirect %ld sec %.1f\n",
         R, seed, A, lamA, lam0, M, NS, LAG, STEP, PMODE, DIV, DL, nFS, mflip, phi0, -lnrate, nd, wtot > 0 ? wbig / wtot : 0.0, nd ? mean / nd : 0.0, q50, q99, mx,
         replaybad, timeouts, trialgens, expo, deaths, (double)(clock() - t0) / CLOCKS_PER_SEC);
  return 0;
}
