/* fd.c: referee's stepper for face deaths.  Written from docs/AUTOMATON.md and reference/oracle.py alone.
   Generic graph stepper (B45/S345, 12 neighbours, neighbour id N = dead outside), 256 replicas bit-sliced.

   gcc -O3 -march=native -o fd fd.c
   fd GEOM trace SEED REPLICA GENS OUT          one replica's state per generation (N bytes each), no restarts
   fd GEOM run SEED SECONDS LGAP OSUB CSUB OUTPREFIX

   run: every replica starts from a soup of density 0.375, burns in BURN = 1000 generations (a face lost in
   burn-in restarts the replica, uncounted); after that every generation of the replica is exposure, the first
   generation in which a face layer is empty is that face's death, and the replica restarts.
   tau_face = F * exposure / deaths.  Written: OUTPREFIX.tal (tallies, text), OUTPREFIX.win (windows, binary).
*/
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <math.h>
typedef uint64_t u64;
typedef u64 vec __attribute__((vector_size(32)));
#define NR 256
#define MAXN 1024
#define MAXF 8
#define MAXA 128
#define HL 16
#define PL 64
#define PW 48
#define BURN 1000
#define SETTLE 2520
#define NP 128
static int N, F, A[MAXF], nb[MAXN][12], fc[MAXF][MAXA];
static vec *S, *T, *hist[HL], *snap;
static uint8_t Ph[MAXF][NR][PL];
static u64 rs;
static inline u64 rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs * 0x2545F4914F6CDD1DULL; }
#define W(v, w) (((u64 *)&(v))[w])

static void step(void) {
    for (int i = 0; i < N; i++) {
        const int *n = nb[i];
        vec n0 = S[n[0]], n1 = S[n[1]], n2 = S[n[2]], n3 = S[n[3]], n4 = S[n[4]], n5 = S[n[5]];
        vec n6 = S[n[6]], n7 = S[n[7]], n8 = S[n[8]], n9 = S[n[9]], n10 = S[n[10]], n11 = S[n[11]];
        vec s1, c1, s2, c2, s3, c3, s4, c4, sA, cA, b0, cB, t1, d1, t2, d2, b1, d3, b2, b3, t_;
#define FA(s, c, x, y, z) { t_ = (x) ^ (y); s = t_ ^ (z); c = ((x) & (y)) | (t_ & (z)); }
#define HA(s, c, x, y) { s = (x) ^ (y); c = (x) & (y); }
        FA(s1, c1, n0, n1, n2) FA(s2, c2, n3, n4, n5) FA(s3, c3, n6, n7, n8) FA(s4, c4, n9, n10, n11)
        FA(sA, cA, s1, s2, s3) HA(b0, cB, sA, s4)
        FA(t1, d1, c1, c2, c3) FA(t2, d2, c4, cA, cB)
        HA(b1, d3, t1, t2)
        FA(b2, b3, d1, d2, d3)
        vec x = S[i];
        vec n45 = ~b3 & b2 & ~b1;            /* 4 or 5 */
        vec n3_ = ~b3 & ~b2 & b1 & b0;       /* 3 */
        T[i] = n45 | (x & n3_);
    }
    vec *q = S; S = T; T = q;
    memset(&S[N], 0, sizeof(vec));
}

static void soup(int r) {
    int w = r >> 6; u64 m = 1ULL << (r & 63);
    for (int i = 0; i < N; i++) {
        u64 x = rnd() >> 20;
        if (((x | (x >> 1)) & (x >> 2)) & 1) W(S[i], w) |= m; else W(S[i], w) &= ~m;
    }
}

int main(int argc, char **argv) {
    if (argc < 4) return 1;
    FILE *g = fopen(argv[1], "r");
    if (!g || fscanf(g, "%d %d", &N, &F) != 2) return 2;
    for (int i = 0; i < N; i++) for (int j = 0; j < 12; j++) if (fscanf(g, "%d", &nb[i][j]) != 1) return 2;
    for (int f = 0; f < F; f++) { if (fscanf(g, "%d", &A[f]) != 1) return 2; for (int j = 0; j < A[f]; j++) if (fscanf(g, "%d", &fc[f][j]) != 1) return 2; }
    fclose(g);
    S = aligned_alloc(32, (MAXN + 1) * sizeof(vec)); T = aligned_alloc(32, (MAXN + 1) * sizeof(vec));
    snap = aligned_alloc(32, (MAXN + 1) * sizeof(vec));
    for (int h = 0; h < HL; h++) hist[h] = aligned_alloc(32, (MAXN + 1) * sizeof(vec));
    memset(S, 0, (MAXN + 1) * sizeof(vec)); memset(T, 0, (MAXN + 1) * sizeof(vec));
    rs = strtoull(argv[3], 0, 10) * 0x9E3779B97F4A7C15ULL + 0x1234567ULL;
    for (int i = 0; i < 20; i++) rnd();
    for (int r = 0; r < NR; r++) soup(r);

    if (!strcmp(argv[2], "trace")) {
        int R = atoi(argv[4]), G = atoi(argv[5]);
        FILE *o = fopen(argv[6], "wb");
        uint8_t buf[MAXN];
        for (int t = 0; t <= G; t++) {
            for (int i = 0; i < N; i++) buf[i] = (W(S[i], R >> 6) >> (R & 63)) & 1;
            fwrite(buf, 1, N, o);
            step();
        }
        fclose(o);
        return 0;
    }

    if (!strcmp(argv[2], "island")) {
        /* fd GEOM island SEED BATCHES K c1 ... cK : after 1000 generations of burn-in, in every replica keep ONE live
           cell of face 0, chosen at random among the live ones of the K candidates, and kill every other cell of face 0
           (the face layer only).  Then run until face 0 is empty (dead) or has >= P0 cells again (regrown), 400 generations at most. */
        int B = atoi(argv[4]), K = atoi(argv[5]), cand[MAXA];
        for (int k = 0; k < K; k++) cand[k] = atoi(argv[6 + k]);
        int a = A[0], P0 = (int)(0.476 * a + 0.999);
        long trials = 0, regrown = 0, died = 0, undecided = 0, skipped = 0;
        for (int b = 0; b < B; b++) {
            for (int r = 0; r < NR; r++) soup(r);
            for (int t = 0; t < BURN; t++) step();
            static int st[NR];
            for (int r = 0; r < NR; r++) {
                int w = r >> 6; u64 m = 1ULL << (r & 63); int live[MAXA], nl = 0;
                for (int k = 0; k < K; k++) if (W(S[cand[k]], w) & m) live[nl++] = cand[k];
                int pop = 0; for (int j = 0; j < a; j++) if (W(S[fc[0][j]], w) & m) pop++;
                int anyempty = 0;
                for (int f = 1; f < F; f++) { int q = 0; for (int j = 0; j < a; j++) if (W(S[fc[f][j]], w) & m) q++; if (!q) anyempty = 1; }
                if (nl == 0 || pop < P0 - 8 || anyempty) { st[r] = 3; skipped++; continue; }
                int keep = live[rnd() % nl];
                for (int j = 0; j < a; j++) if (fc[0][j] != keep) W(S[fc[0][j]], w) &= ~m;
                st[r] = 0; trials++;
            }
            for (int t = 0; t < 400; t++) {
                step();
                for (int r = 0; r < NR; r++) if (st[r] == 0) {
                    int w = r >> 6; u64 m = 1ULL << (r & 63); int pop = 0;
                    for (int j = 0; j < a; j++) if (W(S[fc[0][j]], w) & m) pop++;
                    if (pop == 0) { st[r] = 1; died++; } else if (pop >= P0) { st[r] = 2; regrown++; }
                }
            }
            for (int r = 0; r < NR; r++) if (st[r] == 0) undecided++;
        }
        double q = (double)regrown / trials;
        printf("trials %ld regrown %ld died %ld undecided %ld skipped %ld  share regrown %.4f +- %.4f\n", trials, regrown, died, undecided, skipped, q, sqrt(q * (1 - q) / trials));
        return 0;
    }
    double secs = atof(argv[4]);
    long LGAP = atol(argv[5]), OSUB = atol(argv[6]), CSUB = atol(argv[7]);
    char fn[512];
    snprintf(fn, sizeof fn, "%s.win", argv[8]);
    FILE *wout = fopen(fn, "wb");
    int a = A[0];
    for (int f = 0; f < F; f++) if (A[f] != a) return 3;
    int P0 = (int)(0.476 * a + 0.999);                 /* excursion threshold: 30 of 63, 29 of 60 */
    int OF44 = (44 * a + 31) / 63, OF46 = (46 * a + 31) / 63, HALF = (a + 1) / 2;
    int LEV[4] = {(16 * a + 31) / 63, (12 * a + 31) / 63, (8 * a + 31) / 63, (4 * a + 31) / 63};
    static u64 h1[NP][NP], h2[NP][NP], nreach[NP], ndead[NP], cnt1[4][2][2], cnt2[4][2][2], cnt4[4][2][2];
    static double acc[33]; static u64 accn; static double accs;
    static int age[NR];
    static uint8_t inexc[MAXF][NR], minp[MAXF][NR], reached[MAXF][NR], pre1[MAXF][NR], pre2[MAXF][NR], pre4[MAXF][NR];
    u64 exposure = 0, deaths = 0, burnloss = 0, settled = 0, gen = 0, nwin[4] = {0, 0, 0, 0}, falls = 0, censored = 0;
    int nbytes = (N + 7) / 8;
    time_t t0 = time(0);
    memcpy(snap, S, (MAXN + 1) * sizeof(vec));

#define DUMP(type, f, r) { \
        uint8_t hd[16]; hd[0] = type; hd[1] = f; hd[2] = (r) & 255; hd[3] = (r) >> 8; \
        uint32_t ag = age[r]; memcpy(hd + 4, &ag, 4); memcpy(hd + 8, &gen, 8); fwrite(hd, 1, 16, wout); \
        uint8_t pb[PW]; for (int k = 0; k < PW; k++) pb[k] = Ph[f][r][(gen - (PW - 1) + k) % PL]; fwrite(pb, 1, PW, wout); \
        uint8_t sb[MAXN / 8 + 1]; \
        for (int k = 0; k < HL; k++) { vec *hh = hist[(gen - (HL - 1) + k) % HL]; memset(sb, 0, nbytes); \
            for (int i = 0; i < N; i++) if ((W(hh[i], (r) >> 6) >> ((r) & 63)) & 1) sb[i >> 3] |= 1 << (i & 7); \
            fwrite(sb, 1, nbytes, wout); } }

    for (;;) {
        if ((gen & 1023) == 0 && difftime(time(0), t0) >= secs) break;
        for (int r = 0; r < NR; r++) if (age[r] >= BURN) exposure++;
        step(); gen++;
        memcpy(hist[gen % HL], S, N * sizeof(vec));
        for (int r = 0; r < NR; r++) age[r]++;
        static uint8_t dead[NR];
        memset(dead, 0, NR);
        int slot = gen % PL, s1 = (gen - 1) % PL, s2 = (gen - 2) % PL, s3 = (gen - 3) % PL, s4 = (gen - 4) % PL;
        for (int f = 0; f < F; f++) {
            vec c[7]; for (int k = 0; k < 7; k++) c[k] = (vec){0, 0, 0, 0};
            for (int j = 0; j < a; j++) { vec carry = S[fc[f][j]]; for (int k = 0; k < 7; k++) { vec t = c[k] & carry; c[k] ^= carry; carry = t; } }
            for (int w = 0; w < 4; w++) {
                u64 c0 = W(c[0], w), c1 = W(c[1], w), c2 = W(c[2], w), c3 = W(c[3], w), c4 = W(c[4], w), c5 = W(c[5], w), c6 = W(c[6], w);
                for (int b = 0; b < 64; b++) {
                    int r = w * 64 + b;
                    int p = ((c0 >> b) & 1) | (((c1 >> b) & 1) << 1) | (((c2 >> b) & 1) << 2) | (((c3 >> b) & 1) << 3) | (((c4 >> b) & 1) << 4) | (((c5 >> b) & 1) << 5) | (((c6 >> b) & 1) << 6);
                    uint8_t *ph = Ph[f][r];
                    ph[slot] = p;
                    if (p == 0) dead[r] |= 1;
                    if (age[r] < BURN + 8) continue;
                    int p1 = ph[s1], p2 = ph[s2], p3 = ph[s3], p4 = ph[s4];
                    h1[p1][p]++; h2[p2][p]++;
                    if (p1 - p >= HALF) falls++;
                    if (!inexc[f][r]) {
                        if (p < P0 && p1 >= P0) { inexc[f][r] = 1; minp[f][r] = P0; reached[f][r] = pre1[f][r] = pre2[f][r] = pre4[f][r] = 0; }
                    }
                    if (inexc[f][r]) {
                        for (int j = 0; j < 4; j++) if (p <= LEV[j] && !(reached[f][r] & (1 << j))) {
                            reached[f][r] |= 1 << j;
                            if (p1 >= OF44) pre1[f][r] |= 1 << j;
                            if (p1 >= OF44 || p2 >= OF44) pre2[f][r] |= 1 << j;
                            if (p1 >= OF44 || p2 >= OF44 || p3 >= OF44 || p4 >= OF44) pre4[f][r] |= 1 << j;
                        }
                        if (p < minp[f][r]) minp[f][r] = p;
                        if (p >= P0 || p == 0) {
                            int fatal = (p == 0);
                            for (int q = minp[f][r]; q < P0; q++) { nreach[q]++; if (fatal) ndead[q]++; }
                            for (int j = 0; j < 4; j++) if (reached[f][r] & (1 << j)) {
                                cnt1[j][(pre1[f][r] >> j) & 1][fatal]++; cnt2[j][(pre2[f][r] >> j) & 1][fatal]++; cnt4[j][(pre4[f][r] >> j) & 1][fatal]++;
                            }
                            inexc[f][r] = 0;
                        }
                    }
                    if (r < 32 && age[r] >= BURN + 40 && p > 0) {
                        for (int k = 0; k <= 32; k++) acc[k] += (double)p * ph[(gen - k) % PL];
                        accs += p; accn++;
                    }
                    if (age[r] >= BURN + 64 && p > 0) {
                        int p8 = ph[(gen - 8) % PL], p7 = ph[(gen - 7) % PL];
                        if (p8 >= OF46 && rnd() % OSUB == 0) { DUMP('O', f, r); nwin[1]++; }
                        if (p8 - p7 >= HALF && rnd() % CSUB == 0) { DUMP('C', f, r); nwin[2]++; }
                    }
                }
            }
        }
        if (gen % LGAP == 0) {
            int r = rnd() % NR, f = rnd() % F;
            if (age[r] >= BURN + 64 && !dead[r]) { DUMP('L', f, r); nwin[3]++; }
        }
        for (int r = 0; r < NR; r++) if (dead[r]) {
            if (age[r] > BURN) {
                for (int f = 0; f < F; f++) if (Ph[f][r][slot] == 0) { deaths++; DUMP('D', f, r); nwin[0]++; }
                    else if (inexc[f][r]) censored++;
            } else burnloss++;
            soup(r); age[r] = 0;
            for (int f = 0; f < F; f++) inexc[f][r] = 0;
        }
        if (gen % SETTLE == 0) {
            vec eq = (vec){~0ULL, ~0ULL, ~0ULL, ~0ULL};
            for (int i = 0; i < N; i++) eq &= ~(S[i] ^ snap[i]);
            for (int r = 0; r < NR; r++) if ((W(eq, r >> 6) >> (r & 63)) & 1) {
                if (age[r] > BURN) settled++;
                soup(r); age[r] = 0;
                for (int f = 0; f < F; f++) inexc[f][r] = 0;
            }
            memcpy(snap, S, (MAXN + 1) * sizeof(vec));
        }
    }
    fclose(wout);
    snprintf(fn, sizeof fn, "%s.tal", argv[8]);
    FILE *o = fopen(fn, "w");
    fprintf(o, "N %d F %d A %d P0 %d OF44 %d OF46 %d HALF %d LEV %d %d %d %d\n", N, F, a, P0, OF44, OF46, HALF, LEV[0], LEV[1], LEV[2], LEV[3]);
    fprintf(o, "gen %llu exposure %llu deaths %llu burnloss %llu settled %llu falls %llu censored %llu windows D %llu O %llu C %llu L %llu\n",
            (unsigned long long)gen, (unsigned long long)exposure, (unsigned long long)deaths, (unsigned long long)burnloss,
            (unsigned long long)settled, (unsigned long long)falls, (unsigned long long)censored,
            (unsigned long long)nwin[0], (unsigned long long)nwin[1], (unsigned long long)nwin[2], (unsigned long long)nwin[3]);
    fprintf(o, "acc %llu %.0f", (unsigned long long)accn, accs);
    for (int k = 0; k <= 32; k++) fprintf(o, " %.0f", acc[k]);
    fprintf(o, "\n");
    for (int q = 0; q < P0; q++) fprintf(o, "exc %d %llu %llu\n", q, (unsigned long long)nreach[q], (unsigned long long)ndead[q]);
    for (int j = 0; j < 4; j++) for (int pr = 0; pr < 2; pr++) for (int ft = 0; ft < 2; ft++)
        fprintf(o, "pre %d %d %d %llu %llu %llu\n", LEV[j], pr, ft, (unsigned long long)cnt1[j][pr][ft], (unsigned long long)cnt2[j][pr][ft], (unsigned long long)cnt4[j][pr][ft]);
    for (int p = 0; p <= a; p++) for (int q = 0; q <= a; q++) if (h1[p][q] || h2[p][q])
        fprintf(o, "h %d %d %llu %llu\n", p, q, (unsigned long long)h1[p][q], (unsigned long long)h2[p][q]);
    fclose(o);
    return 0;
}
