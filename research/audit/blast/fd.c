/* fd (research/audit/blast): how a face dies, recorded.  Bit-sliced B45/S345 on a vessel graph written by geom.py,
 * 512 replicas (one AVX-512 word per cell).  Each replica runs successive lives: a life starts from a 0.4 soup and
 * ends when the face layer of any face is empty (a face death) or when the state repeats after 840 generations
 * (settled); the replica is then reseeded.  Only generations at age >= BURN are counted.
 * tau_face = nfaces * exposure / deaths.
 *
 *   fd VESSEL trace INIT GENS OUT            replica 0 from the cells listed in INIT; OUT: its state, n bits a row,
 *                                            generations 0..GENS (the check against reference/oracle.py, geom.py)
 *   fd VESSEL run SEED GENS PREFIX THR [MAXD=40000] [OSUB=16] [RSUB=1009] [BURN=1000] [U0=32]
 *
 * PREFIX.sum (text): exposure, deaths, and, in ordinary time (every 8th generation, replicas of age >= BURN):
 *   H p count          face-layer population p
 *   J p q count        population p, and q one generation later        K p q count: q two generations later
 *   L lag p count      over all deaths: face-layer population p, lag generations before the first empty generation
 *   Q U m count        dips (from the first generation below U cells after one with >= U, to the next with >= U)
 *                      that recovered and whose minimum was m cells (m <= 7); U = U0 and U0 + 1.  The chance that a
 *                      dip reaching <= k cells ends in death is deaths / (deaths + sum of Q over m <= k).
 * PREFIX.rec (binary): records of the last RING = 32 generations of one replica about one face:
 *   'D' a death (the last row is the empty generation), at most MAXD of them;
 *   'O' the face layer held >= THR cells 16 generations before the last row and no face of the replica died since
 *       (one in OSUB such generations among every 8th);   'R' an arbitrary moment (every RSUB generations).
 *   header: u8 type, u8 face, u16 replica, u32 age, u64 generation;
 *   then RING rows (oldest first) of NLAY u16 layer populations; then RING rows of the cells of layers 0..NLB-1 as
 *   bits (each layer padded to a byte, cells in the vessel file's order).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint64_t u64;
typedef u64 v8 __attribute__((vector_size(64), aligned(64)));
#define NREP 512
#define RING 32
#define AFTER 16
#define NLB 3
#define MAXP 256

static u64 sm;
static inline u64 rnd(void) { u64 z = (sm += 0x9e3779b97f4a7c15ULL); z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
  z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; return z ^ (z >> 31); }

static int n, nf, nlay;
static int *nb;          /* n x 12 */
static int **lsz;        /* [face][layer] size */
static int ***lc;        /* [face][layer] cells */
static v8 *ring[RING];

static inline v8 rule(const v8 *x, v8 me) {
  /* carry-save count of 12 bits: n = b0 + 2 b1 + 4 b2 + 8 b3 */
#define FA(s, c, p, q, r) do { v8 t_ = (p) ^ (q); s = t_ ^ (r); c = ((p) & (q)) | (t_ & (r)); } while (0)
  v8 s1, c1, s2, c2, s3, c3, s4, c4, S, C5, b0, C6, t1, d1, t2, d2, b1, e, b2, b3;
  FA(s1, c1, x[0], x[1], x[2]); FA(s2, c2, x[3], x[4], x[5]); FA(s3, c3, x[6], x[7], x[8]); FA(s4, c4, x[9], x[10], x[11]);
  FA(S, C5, s1, s2, s3); b0 = S ^ s4; C6 = S & s4;
  FA(t1, d1, c1, c2, c3); FA(t2, d2, c4, C5, C6); b1 = t1 ^ t2; e = t1 & t2;
  FA(b2, b3, d1, d2, e);
  return ~b3 & ((b2 & ~b1) | (me & ~b2 & b1 & b0));     /* 4 or 5: alive; 3: alive if it was */
}
static void step(const v8 *a, v8 *b) {
  for (int i = 0; i < n; i++) {
    const int *q = nb + 12 * i;
    v8 x[12];
    for (int t = 0; t < 12; t++) x[t] = a[q[t]];
    b[i] = rule(x, a[i]);
  }
  b[n] = (v8){0};
}
static inline int bitof(const v8 *s, int cell, int r) { return (int)((s[cell][r >> 6] >> (r & 63)) & 1); }
static void setbit(v8 *s, int cell, int r, int v) {
  u64 m = 1ULL << (r & 63);
  if (v) s[cell][r >> 6] |= m; else s[cell][r >> 6] &= ~m;
}
static void reseed(v8 *s, int r) { for (int i = 0; i < n; i++) setbit(s, i, r, rnd() < (u64)(0.4 * 18446744073709551616.0)); }

static FILE *rec;
static void write_rec(char type, int f, int r, uint32_t age, u64 g) {
  uint8_t hd[16]; hd[0] = (uint8_t)type; hd[1] = (uint8_t)f; uint16_t rr = (uint16_t)r;
  memcpy(hd + 2, &rr, 2); memcpy(hd + 4, &age, 4); memcpy(hd + 8, &g, 8);
  fwrite(hd, 1, 16, rec);
  static uint8_t bits[RING][NLB][64];
  uint16_t pops[RING][16];
  memset(bits, 0, sizeof bits);
  for (int j = 0; j < RING; j++) {
    const v8 *s = ring[(g - (RING - 1 - j)) % RING];
    for (int l = 0; l < nlay; l++) {
      int c = 0;
      for (int k = 0; k < lsz[f][l]; k++) {
        int v = bitof(s, lc[f][l][k], r);
        c += v;
        if (l < NLB && v) bits[j][l][k >> 3] |= (uint8_t)(1 << (k & 7));
      }
      pops[j][l] = (uint16_t)c;
    }
    fwrite(pops[j], 2, nlay, rec);
  }
  for (int j = 0; j < RING; j++)
    for (int l = 0; l < NLB; l++) fwrite(bits[j][l], 1, (lsz[f][l] + 7) / 8, rec);
}

int main(int argc, char **argv) {
  if (argc < 6) { fprintf(stderr, "usage: see the head of fd.c\n"); return 1; }
  FILE *fp = fopen(argv[1], "rb"); if (!fp) { perror(argv[1]); return 1; }
  int32_t v;
#define RD() (fread(&v, 4, 1, fp) == 1 ? v : (fprintf(stderr, "short read\n"), exit(1), 0))
  n = RD(); nb = malloc(sizeof(int) * 12 * n);
  for (int i = 0; i < 12 * n; i++) nb[i] = RD();
  nf = RD(); nlay = RD();
  lsz = malloc(sizeof(int *) * nf); lc = malloc(sizeof(int **) * nf);
  for (int f = 0; f < nf; f++) {
    lsz[f] = malloc(sizeof(int) * nlay); lc[f] = malloc(sizeof(int *) * nlay);
    for (int l = 0; l < nlay; l++) {
      lsz[f][l] = RD(); lc[f][l] = malloc(sizeof(int) * lsz[f][l]);
      for (int k = 0; k < lsz[f][l]; k++) lc[f][l][k] = RD();
    }
  }
  fclose(fp);
  if (lsz[0][0] >= MAXP || nlay > 16) { fprintf(stderr, "face too large\n"); return 1; }
  for (int j = 0; j < RING; j++) { ring[j] = aligned_alloc(64, sizeof(v8) * (n + 1)); memset(ring[j], 0, sizeof(v8) * (n + 1)); }

  if (!strcmp(argv[2], "trace")) {
    FILE *in = fopen(argv[3], "r"); int c; while (fscanf(in, "%d", &c) == 1) setbit(ring[0], c, 0, 1); fclose(in);
    long gens = atol(argv[4]); FILE *out = fopen(argv[5], "wb");
    uint8_t *row = malloc((n + 7) / 8);
    for (long g = 0; g <= gens; g++) {
      if (g) step(ring[(g - 1) % RING], ring[g % RING]);
      memset(row, 0, (n + 7) / 8);
      for (int i = 0; i < n; i++) if (bitof(ring[g % RING], i, 0)) row[i >> 3] |= (uint8_t)(1 << (i & 7));
      fwrite(row, 1, (n + 7) / 8, out);
    }
    fclose(out); return 0;
  }

  sm = strtoull(argv[3], 0, 10) * 0x9e3779b97f4a7c15ULL + 12345;
  u64 gens = strtoull(argv[4], 0, 10);
  const char *prefix = argv[5];
  int thr = argc > 6 ? atoi(argv[6]) : (int)(0.7 * lsz[0][0] + 0.999);
  long maxd = argc > 7 ? atol(argv[7]) : 40000;
  int osub = argc > 8 ? atoi(argv[8]) : 16;
  int rsub = argc > 9 ? atoi(argv[9]) : 1009;
  uint32_t burn = argc > 10 ? (uint32_t)atoi(argv[10]) : 1000;
  int U[2]; U[0] = argc > 11 ? atoi(argv[11]) : 32; U[1] = U[0] + 1;
  static v8 armed[2][64]; static uint8_t lowmin[2][64][NREP]; static u64 Q[2][8];
  memset(lowmin, 255, sizeof lowmin);
  char path[1024]; snprintf(path, sizeof path, "%s.rec", prefix); rec = fopen(path, "wb");
  if (!rec) { perror(path); return 1; }

  static uint32_t age[NREP], lifeid[NREP];
  for (int r = 0; r < NREP; r++) reseed(ring[0], r);
  v8 *snap = aligned_alloc(64, sizeof(v8) * (n + 1)); memcpy(snap, ring[0], sizeof(v8) * (n + 1));
  static u64 H[MAXP], J[MAXP][MAXP], K[MAXP][MAXP], L[RING][MAXP];
  static uint8_t dec[3][64][NREP];                /* decoded face populations at phases 0, 1, 2; up to 64 faces */
  u64 exposure = 0, deaths = 0, young = 0, settled = 0, nD = 0, nO = 0, nR = 0, ocount = 0, rcount = 0;
  typedef struct { u64 t; int r, f; uint32_t id; } pend;
  int qcap = 1 << 16, qh = 0, qt = 0; pend *q = malloc(sizeof(pend) * qcap);
  int A = lsz[0][0];

  for (u64 g = 1; g <= gens; g++) {
    v8 *cur = ring[g % RING];
    step(ring[(g - 1) % RING], cur);
    for (int r = 0; r < NREP; r++) { age[r]++; exposure += age[r] >= burn; }
    int phase = (int)(g & 7);
    u64 dead[8] = {0}; static u64 fdead[64][8];
    for (int f = 0; f < nf; f++) {
      v8 p[8]; for (int b = 0; b < 8; b++) p[b] = (v8){0};
      for (int k = 0; k < A; k++) {
        v8 c = cur[lc[f][0][k]];
        int nbit = 32 - __builtin_clz(k + 1);
        for (int b = 0; b < nbit; b++) { v8 t = p[b] & c; p[b] ^= c; c = t; }
      }
      v8 any = p[0] | p[1] | p[2] | p[3] | p[4] | p[5] | p[6] | p[7];
      for (int w = 0; w < 8; w++) { fdead[f][w] = ~any[w]; dead[w] |= ~any[w]; }
      v8 low = ~(p[3] | p[4] | p[5] | p[6] | p[7]);          /* at most 7 cells */
      for (int u = 0; u < 2; u++) {
        v8 gt = (v8){0}, eq = ~(v8){0};
        for (int b = 7; b >= 0; b--) { if ((U[u] >> b) & 1) eq &= p[b]; else { gt |= eq & p[b]; eq &= ~p[b]; } }
        v8 ge = gt | eq, hit = ge & armed[u][f];
        for (int w = 0; w < 8; w++) for (u64 m = hit[w]; m; m &= m - 1) {
          int r = w * 64 + __builtin_ctzll(m);
          if (age[r] >= burn && lowmin[u][f][r] >= 1 && lowmin[u][f][r] <= 7) Q[u][lowmin[u][f][r]]++;
          lowmin[u][f][r] = 255;
        }
        armed[u][f] = (armed[u][f] & ~ge) | low;
        for (int w = 0; w < 8; w++) for (u64 m = low[w]; m; m &= m - 1) {
          int s = __builtin_ctzll(m), r = w * 64 + s;
          int c = (int)((p[0][w] >> s) & 1) | (int)((p[1][w] >> s) & 1) << 1 | (int)((p[2][w] >> s) & 1) << 2;
          if (c < lowmin[u][f][r]) lowmin[u][f][r] = (uint8_t)c;
        }
      }
      if (phase < 3)
        for (int r = 0; r < NREP; r++) {
          int w = r >> 6, s = r & 63, c = 0;
          for (int b = 0; b < 8; b++) c |= (int)((p[b][w] >> s) & 1) << b;
          dec[phase][f][r] = (uint8_t)c;
        }
    }
    if (phase == 2)
      for (int r = 0; r < NREP; r++) if (age[r] >= burn + 2 && !((dead[r >> 6] >> (r & 63)) & 1))
        for (int f = 0; f < nf; f++) {
          int p0 = dec[0][f][r], p1 = dec[1][f][r], p2 = dec[2][f][r];
          H[p0]++; J[p0][p1]++; K[p0][p2]++;
        }
    if (phase == 0)
      for (int r = 0; r < NREP; r++) if (age[r] >= burn + RING)
        for (int f = 0; f < nf; f++) if (dec[0][f][r] >= thr && (ocount++ % (u64)osub) == 0 && (qt + 1) % qcap != qh) {
          q[qt] = (pend){g + AFTER, r, f, lifeid[r]}; qt = (qt + 1) % qcap;
        }
    while (qh != qt && q[qh].t <= g) {
      if (q[qh].t == g && lifeid[q[qh].r] == q[qh].id) { write_rec('O', q[qh].f, q[qh].r, age[q[qh].r], g); nO++; }
      qh = (qh + 1) % qcap;
    }
    if (g % (u64)rsub == 0) {
      int r = (int)((rcount * 37) % NREP), f = (int)(rcount % (u64)nf); rcount++;
      if (age[r] >= burn + RING && !((dead[r >> 6] >> (r & 63)) & 1)) { write_rec('R', f, r, age[r], g); nR++; }
    }
    for (int w = 0; w < 8; w++) while (dead[w]) {
      int s = __builtin_ctzll(dead[w]); dead[w] &= dead[w] - 1; int r = w * 64 + s;
      if (age[r] >= burn) {
        for (int f = 0; f < nf; f++) if ((fdead[f][w] >> s) & 1) {
          deaths++;
          for (int lag = 1; lag < RING; lag++) {
            const v8 *st = ring[(g - lag) % RING]; int c = 0;
            for (int k = 0; k < A; k++) c += bitof(st, lc[f][0][k], r);
            L[lag][c]++;
          }
          if ((long)nD < maxd) { write_rec('D', f, r, age[r], g); nD++; }
        }
      } else young++;
      reseed(cur, r); age[r] = 0; lifeid[r]++;
      for (int u = 0; u < 2; u++) for (int f = 0; f < nf; f++) { armed[u][f][w] &= ~(1ULL << s); lowmin[u][f][r] = 255; }
      for (int i = 0; i < n; i++) setbit(snap, i, r, !bitof(cur, i, r));      /* never equal to the old snapshot */
    }
    if (g % 840 == 0) {
      v8 d = (v8){0};
      for (int i = 0; i < n; i++) d |= cur[i] ^ snap[i];
      for (int r = 0; r < NREP; r++) if (!((d[r >> 6] >> (r & 63)) & 1)) {
        settled++; reseed(cur, r); age[r] = 0; lifeid[r]++;
        for (int u = 0; u < 2; u++) for (int f = 0; f < nf; f++) { armed[u][f][r >> 6] &= ~(1ULL << (r & 63)); lowmin[u][f][r] = 255; }
      }
      memcpy(snap, cur, sizeof(v8) * (n + 1));
    }
    if (g % 2000000 == 0) { fprintf(stderr, "g %llu exposure %llu deaths %llu\n", (unsigned long long)g,
                                    (unsigned long long)exposure, (unsigned long long)deaths); }
  }
  fclose(rec);
  snprintf(path, sizeof path, "%s.sum", prefix); FILE *o = fopen(path, "w");
  fprintf(o, "# vessel %s seed %s gens %llu thr %d burn %u\n", argv[1], argv[3], (unsigned long long)gens, thr, burn);
  fprintf(o, "S n %d nfaces %d A %d exposure %llu deaths %llu young %llu settled %llu D %llu O %llu R %llu osub %d ocount %llu\n",
          n, nf, A, (unsigned long long)exposure, (unsigned long long)deaths, (unsigned long long)young,
          (unsigned long long)settled, (unsigned long long)nD, (unsigned long long)nO, (unsigned long long)nR, osub,
          (unsigned long long)ocount);
  for (int p = 0; p < MAXP; p++) if (H[p]) fprintf(o, "H %d %llu\n", p, (unsigned long long)H[p]);
  for (int p = 0; p < MAXP; p++) for (int s = 0; s < MAXP; s++) if (J[p][s]) fprintf(o, "J %d %d %llu\n", p, s, (unsigned long long)J[p][s]);
  for (int p = 0; p < MAXP; p++) for (int s = 0; s < MAXP; s++) if (K[p][s]) fprintf(o, "K %d %d %llu\n", p, s, (unsigned long long)K[p][s]);
  for (int lag = 1; lag < RING; lag++) for (int p = 0; p < MAXP; p++) if (L[lag][p]) fprintf(o, "L %d %d %llu\n", lag, p, (unsigned long long)L[lag][p]);
  for (int u = 0; u < 2; u++) for (int m = 1; m < 8; m++) fprintf(o, "Q %d %d %llu\n", U[u], m, (unsigned long long)Q[u][m]);
  fclose(o);
  return 0;
}
