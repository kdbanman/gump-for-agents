/* gs.c: gump on a vessel graph, 64 replicas bit-sliced; tallies the one-step map (P,B)->(P',B') of every face.
   Rule B45/S345 on 12 neighbours (docs/AUTOMATON.md). Graph from build_vessel.py.
   gs graph seed gens burn out.txt [boxP boxB]      tally run
   gs graph seed G validate init.txt dump.txt       replicas 0 and 63 from init.txt (2 lines of live indices), dump each generation
   A face dies when its layer is empty: the replica is restarted from 50% noise and burnt in (burn generations, untallied).
   Replicas whose whole state equals itself 120 or 2520 generations earlier are restarted too (settled; counted). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <immintrin.h>
#define MAXN 4096
#define MAXF 8
#define MAXL 128
static int N, NF, nb[MAXN][12], nl[MAXF][3], lst[MAXF][3][MAXL];
static uint64_t SA[MAXN + 1], SB[MAXN + 1], snap1[MAXN + 1], snap2[MAXN + 1], rs[4];
static int64_t T[2][MAXL][MAXL][6], HB[MAXL][MAXL], PH[MAXL];
static inline uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static inline uint64_t rnd(void) {
  uint64_t r = rotl(rs[1] * 5, 7) * 9, t = rs[1] << 17;
  rs[2] ^= rs[0]; rs[3] ^= rs[1]; rs[1] ^= rs[2]; rs[0] ^= rs[3]; rs[2] ^= t; rs[3] = rotl(rs[3], 45); return r; }
static void seedrng(uint64_t s) { for (int i = 0; i < 4; i++) { s += 0x9e3779b97f4a7c15ULL; uint64_t z = s;
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL; z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; rs[i] = z ^ (z >> 31); } }
#define CSA(h, l, a, b, c) { uint64_t u_ = (a) ^ (b); h = ((a) & (b)) | (u_ & (c)); l = u_ ^ (c); }
static void step(const uint64_t *s, uint64_t *o) {
  for (int i = 0; i < N; i++) { const int *q = nb[i];
    uint64_t c1, c2, c3, c4, c5, c6, s1, s2, s3, s4, t1, d1, d2, d3, u1, u2, ones, twos, fours, eights, x = s[i];
    CSA(c1, s1, s[q[0]], s[q[1]], s[q[2]]); CSA(c2, s2, s[q[3]], s[q[4]], s[q[5]]);
    CSA(c3, s3, s[q[6]], s[q[7]], s[q[8]]); CSA(c4, s4, s[q[9]], s[q[10]], s[q[11]]);
    CSA(c5, t1, s1, s2, s3); ones = t1 ^ s4; c6 = t1 & s4;
    CSA(d1, u1, c1, c2, c3); CSA(d2, u2, c4, c5, c6); twos = u1 ^ u2; d3 = u1 & u2;
    CSA(eights, fours, d1, d2, d3);
    o[i] = ~eights & ((fours & ~twos) | (x & ~fours & twos & ones)); }
  o[N] = 0; }
static void vcount(const uint64_t *s, const int *idx, int m, uint8_t *out) {
  uint64_t lv[9][3]; int cnt[9] = {0}; uint64_t c[9];
  for (int i = 0; i < m; i++) { uint64_t w = s[idx[i]]; int l = 0;
    for (;;) { lv[l][cnt[l]++] = w; if (cnt[l] < 3) break;
      uint64_t h, lo; CSA(h, lo, lv[l][0], lv[l][1], lv[l][2]); lv[l][0] = lo; cnt[l] = 1; w = h; l++; } }
  for (int l = 0; l < 8; l++) {
    if (cnt[l] == 3) { uint64_t h, lo; CSA(h, lo, lv[l][0], lv[l][1], lv[l][2]); c[l] = lo; lv[l + 1][cnt[l + 1]++] = h; }
    else if (cnt[l] == 2) { c[l] = lv[l][0] ^ lv[l][1]; lv[l + 1][cnt[l + 1]++] = lv[l][0] & lv[l][1]; }
    else if (cnt[l] == 1) c[l] = lv[l][0]; else c[l] = 0; }
  for (int k = 0; k < 8; k++) { uint64_t v = 0;
    for (int b = 0; b < 8; b++) v |= _pdep_u64((c[b] >> (8 * k)) & 0xff, 0x0101010101010101ULL) << b;
    memcpy(out + 8 * k, &v, 8); } }
static uint8_t C0[MAXF][3][64], C1[MAXF][3][64];
static uint8_t ring[64][MAXF][32][3];   /* last 32 generations of (P, B, B2) of every face, dumped at its death if GS_DUMP is set */
static void counts(const uint64_t *s, uint8_t c[MAXF][3][64]) {
  for (int f = 0; f < NF; f++) for (int j = 0; j < 3; j++) vcount(s, lst[f][j], nl[f][j], c[f][j]); }
static void restart(uint64_t *s, int r) { uint64_t m = 1ULL << r; for (int i = 0; i < N; i++) s[i] = (s[i] & ~m) | (rnd() & m); }
int main(int argc, char **argv) {
  FILE *g = fopen(argv[1], "r"); if (!g) return 1;
  if (fscanf(g, "%d %d", &N, &NF) != 2) return 1;
  for (int i = 0; i < N; i++) for (int j = 0; j < 12; j++) if (fscanf(g, "%d", &nb[i][j]) != 1) return 1;
  for (int f = 0; f < NF; f++) for (int j = 0; j < 3; j++) { if (fscanf(g, "%d", &nl[f][j]) != 1) return 1;
      for (int k = 0; k < nl[f][j]; k++) if (fscanf(g, "%d", &lst[f][j][k]) != 1) return 1; }
  fclose(g);
  seedrng(strtoull(argv[2], 0, 10)); long gens = atol(argv[3]);
  uint64_t *cur = SA, *nxt = SB;
  for (int i = 0; i < N; i++) cur[i] = rnd(); cur[N] = 0;
  if (!strcmp(argv[4], "validate")) {
    FILE *in = fopen(argv[5], "r"), *out = fopen(argv[6], "w"); char *line = malloc(1 << 20); int reps[2] = {0, 63};
    for (int k = 0; k < 2; k++) { if (!fgets(line, 1 << 20, in)) return 1; uint64_t m = 1ULL << reps[k];
      for (int i = 0; i < N; i++) cur[i] &= ~m;
      for (char *p = strtok(line, " \n"); p; p = strtok(0, " \n")) cur[atoi(p)] |= m; }
    for (long t = 0; t <= gens; t++) {
      for (int k = 0; k < 2; k++) { for (int i = 0; i < N; i++) if ((cur[i] >> reps[k]) & 1) fprintf(out, "%d ", i); fprintf(out, "\n"); }
      step(cur, nxt); uint64_t *tmp = cur; cur = nxt; nxt = tmp; }
    fclose(out); return 0; }
  int burn0 = atoi(argv[4]), burn[64], bp = -99, bb = -99;
  if (argc > 7) { bp = atoi(argv[6]); bb = atoi(argv[7]); }
  for (int r = 0; r < 64; r++) burn[r] = burn0;
  int64_t expo = 0, deaths = 0, settled = 0, restarts = 0;
  FILE *dump = getenv("GS_DUMP") ? fopen(getenv("GS_DUMP"), "w") : 0; long ndump = 0;
  uint8_t (*cc)[3][64] = C0, (*cn)[3][64] = C1;
  counts(cur, cc); memcpy(snap1, cur, sizeof SA); memcpy(snap2, cur, sizeof SA);
  for (long t = 1; t <= gens; t++) {
    step(cur, nxt); counts(nxt, cn); int any = 0;
    for (int r = 0; r < 64; r++) { int dead = 0;
      if (burn[r]) { burn[r]--; for (int f = 0; f < NF; f++) if (cn[f][0][r] == 0) dead = 1; }
      else { expo++;
        for (int f = 0; f < NF; f++) { int P = cc[f][0][r], Pn = cn[f][0][r]; PH[P]++;
          for (int d = 0; d < 2; d++) { int B = cc[f][1 + d][r], Bn = cn[f][1 + d][r]; int64_t *q = T[d][P][B];
            q[0]++; q[1] += Pn; q[2] += Bn; q[3] += Pn * Pn; q[4] += Bn * Bn; q[5] += Pn * Bn;
            if (d == 0 && abs(P - bp) <= 1 && abs(B - bb) <= 2) HB[Pn][Bn]++; }
          if (Pn == 0) { deaths++; dead = 1;
            if (dump && ndump < 50000) { ndump++; for (int j = 24; j >= 1; j--) { uint8_t *e = ring[r][f][(t - j) & 31];
                fprintf(dump, "%d %d %d ", e[0], e[1], e[2]); } fprintf(dump, "\n"); } } } }
      for (int f = 0; f < NF; f++) { uint8_t *e = ring[r][f][t & 31]; e[0] = cn[f][0][r]; e[1] = cn[f][1][r]; e[2] = cn[f][2][r]; }
      if (dead) { restart(nxt, r); burn[r] = burn0; any = 1; restarts++; } }
    if (t % 120 == 0) { uint64_t df = 0; for (int i = 0; i < N; i++) df |= nxt[i] ^ snap1[i];
      if (t % 2520 == 0) { uint64_t d2 = 0; for (int i = 0; i < N; i++) d2 |= nxt[i] ^ snap2[i]; df &= d2; }
      for (int r = 0; r < 64; r++) if (!((df >> r) & 1)) { restart(nxt, r); burn[r] = burn0; any = 1; settled++; }
      memcpy(snap1, nxt, sizeof SA); if (t % 2520 == 0) memcpy(snap2, nxt, sizeof SA); }
    if (any) counts(nxt, cn);
    uint64_t *tmp = cur; cur = nxt; nxt = tmp; uint8_t (*tc)[3][64] = cc; cc = cn; cn = tc; }
  if (dump) fclose(dump);
  FILE *out = fopen(argv[5], "w");
  fprintf(out, "# N %d NF %d A %d nB %d nB2 %d gens %ld burn %d expo %lld deaths %lld settled %lld restarts %lld box %d %d\n", N, NF,
          nl[0][0], nl[0][1], nl[0][2], gens, burn0, (long long)expo, (long long)deaths, (long long)settled, (long long)restarts, bp, bb);
  for (int d = 0; d < 2; d++) for (int P = 0; P < MAXL; P++) for (int B = 0; B < MAXL; B++) { int64_t *q = T[d][P][B];
        if (q[0]) fprintf(out, "T %d %d %d %lld %lld %lld %lld %lld %lld\n", d, P, B, (long long)q[0], (long long)q[1],
                          (long long)q[2], (long long)q[3], (long long)q[4], (long long)q[5]); }
  for (int P = 0; P < MAXL; P++) for (int B = 0; B < MAXL; B++) if (HB[P][B]) fprintf(out, "H %d %d %lld\n", P, B, (long long)HB[P][B]);
  for (int P = 0; P < MAXL; P++) if (PH[P]) fprintf(out, "P %d %lld\n", P, (long long)PH[P]);
  fclose(out); return 0; }
