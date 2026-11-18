// strips.c -- blast/strips: lifetimes of faces of vessels cut from gump (B45/S345 on the faces of the cubic
// honeycomb) by diagonal half-spaces, optionally periodic. Own bit-sliced graph stepper (AVX-512, 512 lanes =
// independent replicas), written from reference/oracle.py and docs/AUTOMATON.md.
//
// Vessels (doubled coordinates, exactly one odd coordinate per cell):
//   oct R          |x|+|y|+|z| <= R                                 8 faces of 3k(k+1)/2 cells, k = (R+1)/2
//   prism R L      |x+y|+|z| <= R, period L*(2,-2,0)                4 faces (strips) of w = (R+1)/2 unit rows, 3wL cells
//   tet S          side S: d.p <= S (S odd, centre a cube centre) or d.(p-(1,1,1)) <= S (S even, centre a vertex)
//                  for d = (1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)    4 faces of 3S(S+1)/2 cells
//   slab A L       8 {111} layers, period lattice A*(2,-2,0), L*(0,-2,2)   2 faces of 3AL cells ("closed tube/torus A x L")
// A face = all cells of the vessel in the outermost layer d.p = c of one of its half-spaces.
//
//   strips info VESSEL P1 P2
//   strips val  VESSEL P1 P2 SEED GENS NEG OUT     dump for validate.py (NEG=1: one swapped neighbour)
//   strips life VESSEL P1 P2 SEED T0 MAXDEATHS MAXSECS [LAGS]
// life: every lane starts from soup of density 1/2; a life ends at the first generation at which a face is empty
// (a death), or when the lane's state repeats with a period <= 12 (censored; checked every 64 generations); the
// lane is then restarted from soup. Exposure and deaths are counted for lanes older than T0 (tested every 16
// generations). tau_face = faces * exposure / deaths. For periodic vessels a "firewall" (three cyclically
// consecutive dead layers of a diagonal whose layers wind round the period; T3) is looked for every 8
// generations and, exactly, in the generation before each death; the second booking ("nofw", the lead's) ends
// a life at the first firewall or face death and counts only face deaths with no firewall in the generation
// before: tau = faces * exposure_nofw / deaths_nofw.
// LAGS=1 also prints the dying face's population at lags 1..12 before its death and the living distribution.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <math.h>
#include <immintrin.h>
#include <signal.h>
static volatile sig_atomic_t stopnow;
static void onsig(int sg) { (void)sg; stopnow = 1; }

typedef __m512i V;
#define NLANE 512
#define MAXC 6000
#define MAXF 8
#define RG 16
#define NBIN 10
#define NLAG 12
#define BX 72

static int N, NF, nh, PA, PL;
static int cx[MAXC], cy[MAXC], cz[MAXC], nb[MAXC][12];
static int hd[MAXF][3], hc[MAXF];
static int *fcell[MAXF], nfc[MAXF];
static int *hidx;
// firewall layers: up to 4 diagonal axes; cyc[ax] = number of cyclic layers (0 = not cyclic)
static const int DAX[4][3] = {{1, 1, 1}, {1, 1, -1}, {1, -1, 1}, {-1, 1, 1}};
static int cyc[4], *laycell[4][64], nlaycell[4][64], celllay[4][MAXC];

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

// the 12 neighbour offsets of a face with normal axis a, as in reference/oracle.py offsets()
static void offsets(int a, int o[12][3]) {
  int b = (a == 0) ? 1 : 0, c = (a == 2) ? 1 : 2, k = 0;
  for (int sb = 2; sb >= -2; sb -= 4) for (int sc = 2; sc >= -2; sc -= 4) {
    o[k][0] = o[k][1] = o[k][2] = 0; o[k][b] = sb; o[k][c] = sc; k++;
  }
  for (int sa = 1; sa >= -1; sa -= 2) for (int ti = 0; ti < 2; ti++) for (int st = 1; st >= -1; st -= 2) {
    int t = ti ? c : b;
    o[k][0] = o[k][1] = o[k][2] = 0; o[k][a] = sa; o[k][t] = st; k++;
  }
}
static inline int fdiv(int v, int n) { return (v >= 0) ? v / n : -((-v + n - 1) / n); }
static inline int pmod(int v, int n) { v %= n; return v < 0 ? v + n : v; }
static void canon(int *p) {
  if (PA) { int n = fdiv(p[0], 2 * PA); p[0] -= 2 * PA * n; p[1] += 2 * PA * n; }
  if (PL) { int n = fdiv(p[2], 2 * PL); p[2] -= 2 * PL * n; p[1] += 2 * PL * n; }
}
static int inside(const int *p) {
  for (int h = 0; h < nh; h++) if (hd[h][0] * p[0] + hd[h][1] * p[1] + hd[h][2] * p[2] > hc[h]) return 0;
  return 1;
}
static inline int *hx(const int *p) { return &hidx[((p[0] + BX) * (2 * BX + 1) + (p[1] + BX)) * (2 * BX + 1) + (p[2] + BX)]; }
static void addh(int a, int b, int c, int k) { hd[nh][0] = a; hd[nh][1] = b; hd[nh][2] = c; hc[nh] = k; nh++; }
static int gcdi(int a, int b) { a = abs(a); b = abs(b); while (b) { int t = a % b; a = b; b = t; } return a; }

static void build(const char *ves, int p1, int p2) {
  nh = 0; PA = PL = 0;
  if (!strcmp(ves, "oct")) { for (int f = 0; f < 8; f++) addh((f & 1) ? -1 : 1, (f & 2) ? -1 : 1, (f & 4) ? -1 : 1, p1); }
  else if (!strcmp(ves, "prism")) { addh(1, 1, 1, p1); addh(1, 1, -1, p1); addh(-1, -1, 1, p1); addh(-1, -1, -1, p1); PA = p2; }
  else if (!strcmp(ves, "tet")) {
    int e = (p1 % 2 == 0);   // even side: centred on the cube vertex (1,1,1)
    addh(1, 1, 1, p1 + (e ? 3 : 0)); addh(1, -1, -1, p1 - (e ? 1 : 0)); addh(-1, 1, -1, p1 - (e ? 1 : 0)); addh(-1, -1, 1, p1 - (e ? 1 : 0));
  }
  else if (!strcmp(ves, "slab")) { addh(1, 1, 1, 7); addh(-1, -1, -1, 7); PA = p1; PL = p2; }
  else { fprintf(stderr, "unknown vessel\n"); exit(1); }
  NF = nh;
  size_t nbox = (size_t)(2 * BX + 1) * (2 * BX + 1) * (2 * BX + 1);
  hidx = malloc(nbox * sizeof(int)); for (size_t i = 0; i < nbox; i++) hidx[i] = -1;
  N = 0;
  for (int x = -BX + 4; x <= BX - 4; x++) for (int y = -BX + 4; y <= BX - 4; y++) for (int z = -BX + 4; z <= BX - 4; z++) {
    if ((abs(x) & 1) + (abs(y) & 1) + (abs(z) & 1) != 1) continue;
    int p[3] = {x, y, z}, q[3] = {x, y, z};
    canon(q); if (q[0] != x || q[1] != y || q[2] != z) continue;
    if (!inside(p)) continue;
    if (abs(x) > BX - 8 || abs(y) > BX - 8 || abs(z) > BX - 8) { fprintf(stderr, "vessel reaches the box\n"); exit(1); }
    if (N >= MAXC - 1) { fprintf(stderr, "MAXC\n"); exit(1); }
    *hx(p) = N; cx[N] = x; cy[N] = y; cz[N] = z; N++;
  }
  for (int c = 0; c < N; c++) {
    int p[3] = {cx[c], cy[c], cz[c]}, a = (abs(p[0]) & 1) ? 0 : (abs(p[1]) & 1) ? 1 : 2, o[12][3];
    offsets(a, o);
    for (int q = 0; q < 12; q++) {
      int r[3] = {p[0] + o[q][0], p[1] + o[q][1], p[2] + o[q][2]};
      if (!inside(r)) { nb[c][q] = N; continue; }
      canon(r); int h = *hx(r);
      if (h < 0) { fprintf(stderr, "neighbour not found\n"); exit(1); }
      nb[c][q] = h;
    }
  }
  for (int f = 0; f < NF; f++) {
    fcell[f] = malloc(sizeof(int) * N); nfc[f] = 0;
    for (int c = 0; c < N; c++) if (hd[f][0] * cx[c] + hd[f][1] * cy[c] + hd[f][2] * cz[c] == hc[f]) fcell[f][nfc[f]++] = c;
  }
  // cyclic layer systems (firewalls)
  for (int ax = 0; ax < 4; ax++) {
    int g = 0;
    if (PA) g = gcdi(g, 2 * PA * (DAX[ax][0] - DAX[ax][1]));
    if (PL) g = gcdi(g, 2 * PL * (DAX[ax][2] - DAX[ax][1]));
    int isface = 0; for (int h = 0; h < nh; h++) if (abs(hd[h][0] * DAX[ax][0] + hd[h][1] * DAX[ax][1] + hd[h][2] * DAX[ax][2]) == 3) isface = 1;
    cyc[ax] = 0;
    if (isface || g < 8 || g / 2 > 64) continue;
    cyc[ax] = g / 2;
    for (int l = 0; l < cyc[ax]; l++) { laycell[ax][l] = malloc(sizeof(int) * N); nlaycell[ax][l] = 0; }
    for (int c = 0; c < N; c++) {
      int s = DAX[ax][0] * cx[c] + DAX[ax][1] * cy[c] + DAX[ax][2] * cz[c], l = (pmod(s, g) - 1) / 2;
      celllay[ax][c] = l; laycell[ax][l][nlaycell[ax][l]++] = c;
    }
  }
}

// ---- the stepper: B45/S345 on 512 lanes
#define FA(a, b, c, s, k) { s = _mm512_ternarylogic_epi64(a, b, c, 0x96); k = _mm512_ternarylogic_epi64(a, b, c, 0xE8); }
#define HA(a, b, s, k) { s = _mm512_xor_si512(a, b); k = _mm512_and_si512(a, b); }
static void step(const V *restrict s, V *restrict t) {
  for (int c = 0; c < N; c++) {
    const int *b = nb[c];
    V s1, s2, s3, s4, c1, c2, c3, c4, u, c5, b0, c6, v1, v2, d1, d2, b1, d3, b2, b3;
    FA(s[b[0]], s[b[1]], s[b[2]], s1, c1); FA(s[b[3]], s[b[4]], s[b[5]], s2, c2);
    FA(s[b[6]], s[b[7]], s[b[8]], s3, c3); FA(s[b[9]], s[b[10]], s[b[11]], s4, c4);
    FA(s1, s2, s3, u, c5); HA(u, s4, b0, c6);
    FA(c1, c2, c3, v1, d1); FA(c4, c5, c6, v2, d2); HA(v1, v2, b1, d3);
    FA(d1, d2, d3, b2, b3);
    // alive next iff count in {4,5}, or count == 3 and alive: ~b3 & ((b2 & ~b1) | (s & ~b2 & b1 & b0))
    V p = _mm512_andnot_si512(b1, b2);
    V q = _mm512_and_si512(_mm512_andnot_si512(b2, b1), _mm512_and_si512(b0, s[c]));
    t[c] = _mm512_andnot_si512(b3, _mm512_or_si512(p, q));
  }
  t[N] = _mm512_setzero_si512();
}
static inline int nzv(V v) { return _mm512_test_epi64_mask(v, v) != 0; }
static inline int popv(V v) { uint64_t w[8]; _mm512_storeu_si512((void *)w, v); int n = 0; for (int i = 0; i < 8; i++) n += __builtin_popcountll(w[i]); return n; }
static inline int getbit(const V *st, int c, int lane) { return (((const uint64_t *)&st[c])[lane >> 6] >> (lane & 63)) & 1; }

static V *S[RG];
static void soup_all(V *st) { for (int c = 0; c < N; c++) { uint64_t *w = (uint64_t *)&st[c]; for (int i = 0; i < 8; i++) w[i] = rnd(); } st[N] = _mm512_setzero_si512(); }
static void soup_lane(V *st, int lane) {
  int wi = lane >> 6, bi = lane & 63; uint64_t r = 0;
  for (int c = 0; c < N; c++) {
    if ((c & 63) == 0) r = rnd();
    uint64_t *w = (uint64_t *)&st[c];
    w[wi] = (w[wi] & ~(1ULL << bi)) | (((r >> (c & 63)) & 1ULL) << bi);
  }
}
// firewall masks for all lanes (vector)
static V firewall_v(const V *st) {
  V fw = _mm512_setzero_si512();
  for (int ax = 0; ax < 4; ax++) if (cyc[ax]) {
    V dead[64]; int n = cyc[ax];
    for (int l = 0; l < n; l++) {
      V o = _mm512_setzero_si512(); const int *lc = laycell[ax][l];
      for (int q = 0; q < nlaycell[ax][l]; q++) o = _mm512_or_si512(o, st[lc[q]]);
      dead[l] = _mm512_xor_si512(o, _mm512_set1_epi64(-1));
    }
    for (int l = 0; l < n; l++) fw = _mm512_or_si512(fw, _mm512_and_si512(dead[l], _mm512_and_si512(dead[(l + 1) % n], dead[(l + 2) % n])));
  }
  return fw;
}
static int firewall_lane(const V *st, int lane) {
  for (int ax = 0; ax < 4; ax++) if (cyc[ax]) {
    int live[64], n = cyc[ax]; memset(live, 0, sizeof live);
    for (int c = 0; c < N; c++) if (getbit(st, c, lane)) live[celllay[ax][c]] = 1;
    for (int l = 0; l < n; l++) if (!live[l] && !live[(l + 1) % n] && !live[(l + 2) % n]) return 1;
  }
  return 0;
}

static void info(void) {
  printf("N %d faces %d cells/face", N, NF); for (int f = 0; f < NF; f++) printf(" %d", nfc[f]);
  printf(" cyclic layers"); for (int ax = 0; ax < 4; ax++) printf(" %d", cyc[ax]); printf("\n");
  // classes of face cells of face 0 by (number of faces it lies in, neighbours inside the vessel, in the face layer)
  int cnt[4][13][13]; memset(cnt, 0, sizeof cnt);
  for (int q = 0; q < nfc[0]; q++) {
    int c = fcell[0][q], in = 0, inl = 0, nfa = 0;
    for (int f = 0; f < NF; f++) if (hd[f][0] * cx[c] + hd[f][1] * cy[c] + hd[f][2] * cz[c] == hc[f]) nfa++;
    for (int e = 0; e < 12; e++) { int d = nb[c][e]; if (d < N) { in++; if (hd[0][0] * cx[d] + hd[0][1] * cy[d] + hd[0][2] * cz[d] == hc[0]) inl++; } }
    cnt[nfa > 3 ? 3 : nfa][in][inl]++;
  }
  for (int a = 0; a < 4; a++) for (int i = 0; i < 13; i++) for (int j = 0; j < 13; j++) if (cnt[a][i][j])
    printf("  face 0: %3d cells lying in %d face layer(s) with %d neighbours inside, %d of them in the face layer\n", cnt[a][i][j], a, i, j);
}

int main(int argc, char **argv) {
  if (argc < 5) { fprintf(stderr, "usage: see header\n"); return 1; }
  const char *mode = argv[1], *ves = argv[2]; int p1 = atoi(argv[3]), p2 = atoi(argv[4]);
  build(ves, p1, p2);
  if (!strcmp(mode, "info")) { info(); return 0; }
  for (int r = 0; r < RG; r++) S[r] = aligned_alloc(64, sizeof(V) * (N + 1));
  if (!strcmp(mode, "val")) {
    uint64_t seed = strtoull(argv[5], 0, 10); long gens = atol(argv[6]); int neg = atoi(argv[7]); const char *out = argv[8];
    if (neg) { int c = N / 2; nb[c][0] = nb[(c + 7) % N][3]; }
    seedrng(seed); soup_all(S[0]);
    FILE *F = fopen(out, "w");
    fprintf(F, "%d %ld %d %d\n", N, gens, PA, PL);
    for (int c = 0; c < N; c++) fprintf(F, "%d %d %d\n", cx[c], cy[c], cz[c]);
    static const int lanes[3] = {0, 77, 511};
    char *buf = malloc(N + 2);
    for (long t = 0; t <= gens; t++) {
      const V *st = S[t & 1];
      for (int q = 0; q < 3; q++) { for (int c = 0; c < N; c++) buf[c] = '0' + getbit(st, c, lanes[q]); buf[N] = '\n'; fwrite(buf, 1, N + 1, F); }
      step(S[t & 1], S[(t + 1) & 1]);
    }
    fclose(F); return 0;
  }
  if (strcmp(mode, "life") || argc < 9) { fprintf(stderr, "usage: see header\n"); return 1; }
  uint64_t seed = strtoull(argv[5], 0, 10); int T0 = atoi(argv[6]); long maxd = atol(argv[7]); double maxs = atof(argv[8]);
  int dolag = argc > 9 ? atoi(argv[9]) : 0;
  int anycyc = cyc[0] || cyc[1] || cyc[2] || cyc[3];
  seedrng(seed); soup_all(S[0]);
  static long birth[NLANE], ms[NLANE]; static unsigned char mat[NLANE], fws[NLANE];
  uint64_t matw[8] = {0}, nofw[8] = {0};       // mature lanes; mature lanes with no firewall seen
  uint64_t expo = 0, expo_nf = 0, deaths = 0, deaths_nf = 0, ncens = 0, nfwseen = 0, multi = 0, early = 0;
  uint64_t bexp[NBIN] = {0}, bdth[NBIN] = {0};
  static uint64_t lagh[NLAG + 1][400], liveh[400]; uint64_t nbust = 0, nlagd = 0;
  int A = nfc[0];
  const V ones = _mm512_set1_epi64(-1), zero = _mm512_setzero_si512();
  struct timespec ts0, ts1; clock_gettime(CLOCK_MONOTONIC, &ts0);
  long t = 0; double secs = 0, nextprog = 60;
  signal(SIGTERM, onsig); signal(SIGINT, onsig);
#define ADDEXP(lane, tend) { long a0 = ms[lane] - birth[lane], a1 = (tend) - birth[lane]; \
    for (int b = 0; b < NBIN; b++) { long lo = (long)T0 << b, hi = (b == NBIN - 1) ? (1L << 62) : ((long)T0 << (b + 1)); \
      long x0 = a0 > lo ? a0 : lo, x1 = a1 < hi ? a1 : hi; if (x1 > x0) bexp[b] += x1 - x0; } }
#define RESTART(lane) { soup_lane(S[t % RG], lane); birth[lane] = t; mat[lane] = 0; fws[lane] = 0; \
    matw[(lane) >> 6] &= ~(1ULL << ((lane) & 63)); nofw[(lane) >> 6] &= ~(1ULL << ((lane) & 63)); }
  for (;;) {
    if ((t & 15) == 0) for (int l = 0; l < NLANE; l++) if (!mat[l] && t - birth[l] >= T0) {
      mat[l] = 1; ms[l] = t; matw[l >> 6] |= 1ULL << (l & 63);
      // a lane that already has a firewall when it comes of age never enters the no-firewall risk set
      if (anycyc && firewall_lane(S[t % RG], l)) fws[l] = 1; else nofw[l >> 6] |= 1ULL << (l & 63);
    }
    for (int i = 0; i < 8; i++) { expo += __builtin_popcountll(matw[i]); expo_nf += __builtin_popcountll(nofw[i]); }
    step(S[t % RG], S[(t + 1) % RG]); t++;
    const V *st = S[t % RG];
    V dead = zero, two = zero;
    for (int f = 0; f < NF; f++) {
      V o = zero; const int *fc = fcell[f];
      for (int q = 0; q < nfc[f]; q++) o = _mm512_or_si512(o, st[fc[q]]);
      V e = _mm512_xor_si512(o, ones); two = _mm512_or_si512(two, _mm512_and_si512(dead, e)); dead = _mm512_or_si512(dead, e);
    }
    if (nzv(dead)) {
      uint64_t dw[8], tw[8]; _mm512_storeu_si512((void *)dw, dead); _mm512_storeu_si512((void *)tw, two);
      for (int i = 0; i < 8; i++) { uint64_t x = dw[i]; while (x) {
        int bit = __builtin_ctzll(x), lane = 64 * i + bit; x &= x - 1;
        if (mat[lane]) {
          deaths++; ADDEXP(lane, t);
          { long a = t - birth[lane]; int b = 0; while (b < NBIN - 1 && a >= ((long)T0 << (b + 1))) b++; bdth[b]++; }
          if ((tw[i] >> bit) & 1) multi++;
          if (!fws[lane]) { if (anycyc && firewall_lane(S[(t - 1) % RG], lane)) { fws[lane] = 1; nfwseen++; } else deaths_nf++; }
          if (dolag) {
            int f0 = -1;
            for (int f = 0; f < NF && f0 < 0; f++) { int any = 0; for (int q = 0; q < nfc[f]; q++) any |= getbit(st, fcell[f][q], lane); if (!any) f0 = f; }
            int prev = 0, maxfall = 0;
            for (int lag = 1; lag <= NLAG; lag++) {
              const V *so = S[(t - lag) % RG]; int pop = 0;
              for (int q = 0; q < nfc[f0]; q++) pop += getbit(so, fcell[f0][q], lane);
              lagh[lag][pop]++; if (pop - prev > maxfall) maxfall = pop - prev; prev = pop;
            }
            nlagd++; if (2 * maxfall >= nfc[f0]) nbust++;
          }
        } else early++;
        RESTART(lane);
      } }
    }
    if (anycyc && (t & 7) == 0) {
      V fw = firewall_v(st); uint64_t fwv[8]; _mm512_storeu_si512((void *)fwv, fw);
      for (int i = 0; i < 8; i++) { uint64_t x = fwv[i] & nofw[i]; while (x) {
        int bit = __builtin_ctzll(x), lane = 64 * i + bit; x &= x - 1;
        fws[lane] = 1; nfwseen++; nofw[i] &= ~(1ULL << bit);
      } }
    }
    if ((t & 63) == 0) {
      V per = zero;
      for (int p = 1; p <= 12; p++) {
        const V *so = S[(t - p) % RG]; V diff = zero;
        for (int c = 0; c < N; c++) diff = _mm512_or_si512(diff, _mm512_xor_si512(st[c], so[c]));
        per = _mm512_or_si512(per, _mm512_xor_si512(diff, ones));
      }
      if (nzv(per)) {
        uint64_t pw[8]; _mm512_storeu_si512((void *)pw, per);
        for (int i = 0; i < 8; i++) { uint64_t x = pw[i]; while (x) {
          int bit = __builtin_ctzll(x), lane = 64 * i + bit; x &= x - 1;
          if (t - birth[lane] < 13) continue;
          if (mat[lane]) { ncens++; ADDEXP(lane, t); }
          RESTART(lane);
        } }
      }
    }
    if (dolag && (t & 127) == 0) {   // living distribution: face 0 of 16 lanes
      for (int k = 0; k < 16; k++) { int lane = (int)((t / 128 * 16 + k) % NLANE); if (!mat[lane]) continue;
        int pop = 0; for (int q = 0; q < A; q++) pop += getbit(st, fcell[0][q], lane); liveh[pop]++; }
    }
    if ((t & 4095) == 0) {
      clock_gettime(CLOCK_MONOTONIC, &ts1); secs = (ts1.tv_sec - ts0.tv_sec) + 1e-9 * (ts1.tv_nsec - ts0.tv_nsec);
      if (secs >= nextprog) { nextprog += 60; fprintf(stderr, "progress %s %d %d secs %.0f gens %ld deaths %llu exposure %llu ln_tau %.4f | nofw deaths %llu exposure %llu firewalls %llu censored %llu\n", ves, p1, p2, secs, t,
          (unsigned long long)deaths, (unsigned long long)expo, deaths ? log((double)NF * expo / deaths) : 0.0, (unsigned long long)deaths_nf, (unsigned long long)expo_nf, (unsigned long long)nfwseen, (unsigned long long)ncens); fflush(stderr); }
      if ((long)deaths >= maxd || secs >= maxs || stopnow) break;
    }
  }
  long maxage = 0;
  for (int l = 0; l < NLANE; l++) { if (mat[l]) ADDEXP(l, t); if (t - birth[l] > maxage) maxage = t - birth[l]; }
  uint64_t be = 0; for (int b = 0; b < NBIN; b++) be += bexp[b];
  printf("# life %s %d %d seed %llu T0 %d: N %d faces %d cells/face %d gens %ld secs %.1f (%.2f ns per cell-generation of 512 lanes); "
         "censored as periodic %llu; deaths before T0 %llu; deaths with two faces at once %llu; oldest lane at the end %ld; exposure by bins %llu\n",
         ves, p1, p2, (unsigned long long)seed, T0, N, NF, A, t, secs, 1e9 * secs / ((double)t * N), (unsigned long long)ncens,
         (unsigned long long)early, (unsigned long long)multi, maxage, (unsigned long long)be);
  for (int b = 0; b < NBIN; b++) if (bdth[b])
    printf("  age %8ld..: deaths %9llu exposure %14llu ln tau_face %.4f +- %.4f\n", (long)T0 << b, (unsigned long long)bdth[b],
           (unsigned long long)bexp[b], log((double)NF * bexp[b] / bdth[b]), 1 / sqrt((double)bdth[b]));
  if (deaths) printf("LIFE %s %d %d cells %d seed %llu T0 %d deaths %llu exposure %llu ln_tau_face %.4f +- %.4f",
                     ves, p1, p2, A, (unsigned long long)seed, T0, (unsigned long long)deaths, (unsigned long long)expo, log((double)NF * expo / deaths), 1 / sqrt((double)deaths));
  if (anycyc && deaths_nf) printf(" | nofw deaths %llu exposure %llu ln_tau_face %.4f +- %.4f firewalls %llu fw%% %.1f",
                     (unsigned long long)deaths_nf, (unsigned long long)expo_nf, log((double)NF * expo_nf / deaths_nf), 1 / sqrt((double)deaths_nf),
                     (unsigned long long)nfwseen, 100.0 * nfwseen / (nfwseen + deaths_nf));
  printf("\n");
  if (dolag && nlagd) {
    uint64_t nl = 0; double sm = 0; for (int p = 0; p <= A; p++) { nl += liveh[p]; sm += (double)p * liveh[p]; }
    double q[4] = {0.5, 0.9, 0.95, 0.99}; int qv[4];
    for (int k = 0; k < 4; k++) { uint64_t acc = 0; int p = 0; for (; p <= A; p++) { acc += liveh[p]; if (acc >= q[k] * nl) break; } qv[k] = p; }
    printf("LIVE %s %d %d cells %d samples %llu mean %.3f q50 %d q90 %d q95 %d q99 %d\n", ves, p1, p2, A, (unsigned long long)nl, sm / nl, qv[0], qv[1], qv[2], qv[3]);
    printf("BUST %s %d %d deaths %llu share with a one-generation fall of at least half the face %.4f\n", ves, p1, p2, (unsigned long long)nlagd, (double)nbust / nlagd);
    for (int lag = 1; lag <= NLAG; lag++) {
      uint64_t n = 0; double s = 0; for (int p = 0; p <= A; p++) { n += lagh[lag][p]; s += (double)p * lagh[lag][p]; }
      double qq[4] = {0.1, 0.5, 0.9, 0.95}; int v[4];
      for (int k = 0; k < 4; k++) { uint64_t acc = 0; int p = 0; for (; p <= A; p++) { acc += lagh[lag][p]; if (acc >= qq[k] * n) break; } v[k] = p; }
      printf("LAG %s %d %d lag %2d mean %.3f q10 %d q50 %d q90 %d q95 %d\n", ves, p1, p2, lag, s / n, v[0], v[1], v[2], v[3]);
    }
  }
  return 0;
}
