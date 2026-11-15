// r3_ex.c: ex2.c (this directory) with faces of up to 127 cells (7-bit counts) and dumps of deep excursions.
//   r3_ex GRAPH run SEED P GENS OUT EXT SAMP SAMPK DUMP MAXD H T0 PBAR EXOUT M3 DXOUT
//   Everything of ex2 unchanged (P histogram and tables now to P = 127). DXOUT: for every excursion whose P reaches
//   <= M3, the face-orbit representative's cell states (bit k = k-th cell of that face's list in the graph file, 16
//   bytes per generation) at every generation from the first with P <= M3 to the end of the excursion inclusive (cap
//   512, flagged), preceded by int32 {lane, orbit, end (1 recovered, 2 dead, 3 censored), minP, len, truncated,
//   generation of the first dumped state, age then}. Shares no code with research/dying/ex3.c.
// ex2.c header follows.
// ex2.c: dy.c plus excursion tables of each face orbit's population P (one face per orbit) at every generation.
//   ex2 GRAPH run SEED P GENS OUT EXT SAMP SAMPK DUMP MAXD H T0 PBAR EXOUT
//   An excursion starts at a generation with P < PBAR after a generation with P >= PBAR, both at age > T0; it ends
//   recovered (P >= PBAR), dead (P = 0) or censored (the life ends otherwise, or the job ends). Its minimum P and end
//   are tallied per life and added at the life's end to the table of that life's end type (1 F, 3 X, 4 S, 5 open),
//   with the life's exposure (face-orbit generations at age > T0), its P histogram over that exposure, and its
//   face-orbit deaths at age > T0. EXOUT (text): "E type exposure deaths", "H type P count", "X type minP rec dead cens".
// Built from:
// dy.c: research/audit/symmetric/st.c (the review's independent stepper, validated against reference/oracle.py)
// with three outputs added for the review of research/dying; dynamics, RNG and the lives file OUT unchanged
// (OUT is byte-identical to st's for the same arguments: checked by cmp). Shares no code with sy.c or sd.c.
//   dy GRAPH run SEED P GENS OUT EXT SAMP SAMPK DUMP MAXD H T0
//     EXT : per record of OUT, int32 {lane, generation at the event}
//     SAMP: every SAMPK generations, every lane: int32 {lane, generation, age} + face-union state (bit k of the
//           k-th cell of U, U = sorted union of the face cell lists)
//     DUMP: the first MAXD lives ending F or X (type 1, 3) at age > T0: int32 {record index, lane, age, type,
//           face mask, generation} + H face-union states, lags j = 0..H-1 generations before the event
//           (lag 0 = the generation at which a face is first empty; events are checked every generation)
// Original st.c header follows.
// st.c: independent bit-sliced gump stepper on a full (unreduced) finite system with symmetric soups.
// Review of research/theory/symmetric; shares no code with sy.c.
//   st GRAPH run SEED P GENS OUT      W*64 replicas (W below), each GENS generations of renewal lives
//   st GRAPH trace SEED P GENS        lane 0 only: prints the live cell indices at every generation (validation)
// Soup: one Bernoulli(P) draw per orbit (all cells of an orbit equal), 24-bit binary-expansion construction.
// Events checked EVERY generation: face death (a face's cells all dead), transverse firewall (three cyclically
// consecutive dead layers of one family, slabs), settled (Brent: snapshot at ages 1,2,4,8,..., equality test each
// generation). Records (16 bytes): age (u32; for S the snapshot age), type (1 F, 2 W, 3 F+W same gen, 4 S, 5 open),
// mask of faces dead at the event (u16), detection age for S (u32).
// With LADDER=K in the environment: snapshots at ages 1, then age + max(1, age/K); for S the 4th field is then the
// previous snapshot age (a lower bound on the settling age when the period is below the rung gap).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define W 4
typedef uint64_t u64;
static u64 s[4];
static inline u64 rotl(u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static u64 nxt(void) { u64 r = rotl(s[1] * 5, 7) * 9, t = s[1] << 17; s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2]; s[0] ^= s[3]; s[2] ^= t; s[3] = rotl(s[3], 45); return r; }
static u64 sm(u64 *x) { u64 z = (*x += 0x9e3779b97f4a7c15ULL); z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL; z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; return z ^ (z >> 31); }
static int pbits[24];
static u64 bern(void) { u64 r = 0; for (int k = 23; k >= 0; k--) { u64 u = nxt(); r = pbits[k] ? (r | u) : (r & u); } return r; }

int N, NO, NF, *nb, *orb, **face, *flen, *forb, NT, *tL, ***tl, **tlen;
int main(int argc, char **argv) {
    FILE *g = fopen(argv[1], "r");
    if (fscanf(g, "%d %d", &N, &NO) != 2) return 1;
    nb = malloc(sizeof(int) * N * 12); orb = malloc(sizeof(int) * N);
    for (int i = 0; i < N * 12; i++) if (fscanf(g, "%d", &nb[i]) != 1) return 1;
    for (int i = 0; i < N; i++) if (fscanf(g, "%d", &orb[i]) != 1) return 1;
    if (fscanf(g, "%d", &NF) != 1) return 1;
    face = malloc(sizeof(int *) * NF); flen = malloc(sizeof(int) * NF); forb = malloc(sizeof(int) * NF);
    for (int f = 0; f < NF; f++) { if (fscanf(g, "%d", &flen[f]) != 1) return 1; face[f] = malloc(sizeof(int) * flen[f]); for (int k = 0; k < flen[f]; k++) if (fscanf(g, "%d", &face[f][k]) != 1) return 1; }
    for (int f = 0; f < NF; f++) if (fscanf(g, "%d", &forb[f]) != 1) return 1;
    if (fscanf(g, "%d", &NT) != 1) return 1;
    tL = malloc(sizeof(int) * (NT + 1)); tl = malloc(sizeof(int **) * (NT + 1)); tlen = malloc(sizeof(int *) * (NT + 1));
    for (int t = 0; t < NT; t++) {
        if (fscanf(g, "%d", &tL[t]) != 1) return 1; tl[t] = malloc(sizeof(int *) * tL[t]); tlen[t] = malloc(sizeof(int) * tL[t]);
        for (int l = 0; l < tL[t]; l++) { if (fscanf(g, "%d", &tlen[t][l]) != 1) return 1; tl[t][l] = malloc(sizeof(int) * tlen[t][l]); for (int k = 0; k < tlen[t][l]; k++) if (fscanf(g, "%d", &tl[t][l][k]) != 1) return 1; }
    }
    fclose(g);
    char *isU = calloc(N, 1); for (int f = 0; f < NF; f++) for (int k = 0; k < flen[f]; k++) isU[face[f][k]] = 1;
    int NU = 0, *U = malloc(sizeof(int) * N); for (int i = 0; i < N; i++) if (isU[i]) U[NU++] = i;
    int trace = !strcmp(argv[2], "trace");
    u64 seed = strtoull(argv[3], 0, 10); double P = atof(argv[4]); long long GENS = atoll(argv[5]);
    for (int i = 0; i < 4; i++) s[i] = sm(&seed);
    double pp = P; for (int k = 0; k < 24; k++) { pp *= 2; pbits[k] = pp >= 1; if (pp >= 1) pp -= 1; }
    // state arrays: [cell][W], plus a zero cell at index N
    u64 *x = calloc((size_t)(N + 1) * W, 8), *y = calloc((size_t)(N + 1) * W, 8), *snap = calloc((size_t)N * W, 8), *ob = malloc(sizeof(u64) * NO);
    u64 snapok[W] = {0};
    uint32_t age[W * 64], snapage[W * 64], prevsnap[W * 64], nextsnap[W * 64];
    int LAD = getenv("LADDER") ? atoi(getenv("LADDER")) : 0;   // 0: Brent (powers of two); K: next snapshot at age + max(1, age/K)
    for (int l = 0; l < W * 64; l++) { prevsnap[l] = 0; nextsnap[l] = 1; }
    FILE *out = trace ? 0 : fopen(argv[6], "wb");
    FILE *ext = 0, *smp = 0, *dmp = 0; long SAMPK = 0, MAXD = 0, T0 = 512; int HH = 1;
    if (!trace) { ext = fopen(argv[7], "wb"); smp = fopen(argv[8], "wb"); SAMPK = atol(argv[9]); dmp = fopen(argv[10], "wb");
        MAXD = atol(argv[11]); HH = atoi(argv[12]); T0 = atol(argv[13]); if (!ext || !smp || !dmp) return 2; }
    double PBAR = trace ? 0 : atof(argv[14]);
    int M3 = trace ? -1 : atoi(argv[16]); FILE *dxo = trace ? 0 : fopen(argv[17], "wb");
    static unsigned char dbuf[256][8][512][16]; static int drec[256][8], dlen[256][8], dtr[256][8], dg0[256][8], da0[256][8];
    long ndx = 0;
    int NOF = 0, orep[8]; for (int f = 0; f < NF; f++) { int seen = 0; for (int k = 0; k < NOF; k++) if (forb[orep[k]] == forb[f]) seen = 1; if (!seen) orep[NOF++] = f; }
    static long TX[6][128][4], TE[6], TD[6], TH[6][128], LX[256][128][4], LE[256], LD[256], LH[256][128];
    static int inexc[256][8], minp[256][8], prevok[256][8];
    int NUB = (NU + 7) / 8; unsigned char *ub = malloc(NUB);
    u64 *ring = calloc((size_t)HH * NU * W, 8); long ndump = 0;
    // initial soups for all lanes
    for (int w = 0; w < W; w++) { for (int o = 0; o < NO; o++) ob[o] = bern(); for (int i = 0; i < N; i++) x[i * W + w] = ob[orb[i]]; }
    for (int l = 0; l < W * 64; l++) { age[l] = 0; snapage[l] = 0; }
    long long nrec = 0;
    for (long long gen = 0; gen < GENS; gen++) {
        if (trace) { printf("%lld", gen); for (int i = 0; i < N; i++) if (x[i * W] & 1) printf(" %d", i); printf("\n"); }
        // step
        for (int i = 0; i < N; i++) {
            const int *q = nb + i * 12;
            for (int w = 0; w < W; w++) {
                u64 b0 = 0, b1 = 0, b2 = 0, b3 = 0;
                for (int k = 0; k < 12; k++) { u64 a = x[q[k] * W + w], c0 = b0 & a; b0 ^= a; u64 c1 = b1 & c0; b1 ^= c0; u64 c2 = b2 & c1; b2 ^= c1; b3 |= c2; }
                u64 xi = x[i * W + w];
                y[i * W + w] = (~b3 & b2 & ~b1) | (xi & ~b3 & ~b2 & b1 & b0);
            }
        }
        u64 *t = x; x = y; y = t;
        for (int l = 0; l < W * 64; l++) age[l]++;
        if (trace) continue;
        long long gabs = gen + 1;
        { u64 *rr = ring + (size_t)(gabs % HH) * NU * W; for (int k = 0; k < NU; k++) for (int w = 0; w < W; w++) rr[k * W + w] = x[U[k] * W + w]; }
        if (gabs % SAMPK == 0) for (int l = 0; l < W * 64; l++) {
            int w = l / 64, b = l % 64; memset(ub, 0, NUB);
            for (int k = 0; k < NU; k++) if ((x[U[k] * W + w] >> b) & 1) ub[k >> 3] |= (unsigned char)(1u << (k & 7));
            int32_t hd[3] = {l, (int32_t)gabs, (int32_t)age[l]}; fwrite(hd, 4, 3, smp); fwrite(ub, 1, NUB, smp); }
        // face-orbit populations and excursions
        for (int o = 0; o < NOF; o++) {
            int f = orep[o]; u64 c[W][7]; memset(c, 0, sizeof c);
            for (int k = 0; k < flen[f]; k++) for (int w = 0; w < W; w++) { u64 car = x[face[f][k] * W + w]; for (int bb = 0; bb < 7 && car; bb++) { u64 tt = c[w][bb] & car; c[w][bb] ^= car; car = tt; } }
            for (int l = 0; l < W * 64; l++) {
                int w = l / 64, bb = l % 64, P = 0; for (int k = 0; k < 7; k++) P |= (int)((c[w][k] >> bb) & 1) << k;
                int ok = (long)age[l] > T0;
                if (ok) { LE[l]++; LH[l][P]++; if (P == 0) LD[l]++; }
                int startx = 0;
                if (inexc[l][o]) { if (P < minp[l][o]) minp[l][o] = P; }
                else if (ok && prevok[l][o] && P < PBAR) { if (P == 0) LX[l][0][2]++; else { inexc[l][o] = 1; minp[l][o] = P; startx = 1; } }
                if (inexc[l][o] || (P == 0 && drec[l][o])) {
                    if (!drec[l][o] && P <= M3) { drec[l][o] = 1; dlen[l][o] = 0; dtr[l][o] = 0; dg0[l][o] = (int)gabs; da0[l][o] = (int)age[l]; }
                    if (drec[l][o]) { if (dlen[l][o] < 512) { unsigned char *dd = dbuf[l][o][dlen[l][o]]; memset(dd, 0, 16);
                            for (int k = 0; k < flen[f]; k++) if ((x[face[f][k] * W + w] >> bb) & 1) dd[k >> 3] |= (unsigned char)(1u << (k & 7));
                            dlen[l][o]++; } else dtr[l][o] = 1; }
                }
                if (inexc[l][o] && !startx) {
                    int en = 0;
                    if (P == 0) { LX[l][minp[l][o]][2]++; inexc[l][o] = 0; en = 2; } else if (P >= PBAR) { LX[l][minp[l][o]][1]++; inexc[l][o] = 0; en = 1; }
                    if (en && drec[l][o]) { int32_t hh[8] = {l, o, en, minp[l][o], dlen[l][o], dtr[l][o], dg0[l][o], da0[l][o]}; fwrite(hh, 4, 8, dxo);
                        fwrite(dbuf[l][o], 16, dlen[l][o], dxo); drec[l][o] = 0; ndx++; }
                }
                prevok[l][o] = ok && P >= PBAR;
            }
        }
        // events
        for (int w = 0; w < W; w++) {
            u64 fdead[16], anyf = 0;
            for (int f = 0; f < NF; f++) { u64 a = 0; for (int k = 0; k < flen[f]; k++) a |= x[face[f][k] * W + w]; fdead[f] = ~a; anyf |= ~a; }
            u64 fw = 0;
            for (int tt = 0; tt < NT; tt++) {
                int L = tL[tt]; u64 dl[64];
                for (int l = 0; l < L; l++) { u64 a = 0; for (int k = 0; k < tlen[tt][l]; k++) a |= x[tl[tt][l][k] * W + w]; dl[l] = ~a; }
                for (int l = 0; l < L; l++) fw |= dl[l] & dl[(l + 1) % L] & dl[(l + 2) % L];
            }
            u64 diff = 0; for (int i = 0; i < N; i++) diff |= x[i * W + w] ^ snap[i * W + w];
            u64 settled = snapok[w] & ~diff & ~anyf & ~fw;
            u64 end = anyf | fw | settled;
            u64 restart = 0;
            for (int b = 0; b < 64; b++) {
                int l = w * 64 + b; u64 m = 1ULL << b;
                if (end & m) {
                    uint32_t rec[4]; int ty; uint32_t fm = 0;
                    for (int f = 0; f < NF; f++) if (fdead[f] & m) fm |= 1u << f;
                    if ((anyf & m) && (fw & m)) ty = 3; else if (anyf & m) ty = 1; else if (fw & m) ty = 2; else ty = 4;
                    rec[0] = ty == 4 ? snapage[l] : age[l]; rec[1] = ty; rec[2] = fm; rec[3] = (LAD && ty == 4) ? prevsnap[l] : age[l];
                    fwrite(rec, 4, 4, out);
                    { int32_t e2[2] = {l, (int32_t)gabs}; fwrite(e2, 4, 2, ext); }
                    if ((ty == 1 || ty == 3) && (long)age[l] > T0 && ndump < MAXD) {
                        int32_t hd[6] = {(int32_t)nrec, l, (int32_t)age[l], ty, (int32_t)fm, (int32_t)gabs}; fwrite(hd, 4, 6, dmp);
                        for (int j = 0; j < HH; j++) { const u64 *rr = ring + (size_t)(((gabs - j) % HH + HH) % HH) * NU * W; memset(ub, 0, NUB);
                            for (int k = 0; k < NU; k++) if ((rr[k * W + w] >> b) & 1) ub[k >> 3] |= (unsigned char)(1u << (k & 7));
                            fwrite(ub, 1, NUB, dmp); }
                        ndump++; }
                    nrec++;
                    for (int o = 0; o < NOF; o++) { if (inexc[l][o]) LX[l][minp[l][o]][3]++;
                        if (drec[l][o]) { int32_t hh[8] = {l, o, 3, minp[l][o], dlen[l][o], dtr[l][o], dg0[l][o], da0[l][o]}; fwrite(hh, 4, 8, dxo);
                            fwrite(dbuf[l][o], 16, dlen[l][o], dxo); drec[l][o] = 0; ndx++; }
                        inexc[l][o] = 0; prevok[l][o] = 0; }
                    TE[ty] += LE[l]; TD[ty] += LD[l]; LE[l] = 0; LD[l] = 0;
                    for (int P = 0; P < 128; P++) { TH[ty][P] += LH[l][P]; LH[l][P] = 0; for (int e = 0; e < 4; e++) { TX[ty][P][e] += LX[l][P][e]; LX[l][P][e] = 0; } }
                    restart |= m; age[l] = 0; snapage[l] = 0; prevsnap[l] = 0; nextsnap[l] = 1;
                }
            }
            // snapshots: lanes whose age is a power of two (and not restarting)
            u64 take = 0;
            for (int b = 0; b < 64; b++) { int l = w * 64 + b; if ((restart >> b) & 1) continue;
                int due = LAD ? (age[l] == nextsnap[l]) : (age[l] && !(age[l] & (age[l] - 1)));
                if (due) { take |= 1ULL << b; prevsnap[l] = snapage[l]; snapage[l] = age[l]; nextsnap[l] = LAD ? age[l] + (age[l] / LAD > 1 ? age[l] / LAD : 1) : 0; } }
            if (take) for (int i = 0; i < N; i++) snap[i * W + w] = (snap[i * W + w] & ~take) | (x[i * W + w] & take);
            snapok[w] = (snapok[w] | take) & ~restart;
            if (restart) { for (int o = 0; o < NO; o++) ob[o] = bern(); for (int i = 0; i < N; i++) x[i * W + w] = (x[i * W + w] & ~restart) | (ob[orb[i]] & restart); }
        }
    }
    if (!trace) {
        for (int l = 0; l < W * 64; l++) { uint32_t rec[4] = {age[l], 5, 0, age[l]}; fwrite(rec, 4, 4, out); }
        for (int l = 0; l < W * 64; l++) { int32_t e2[2] = {l, (int32_t)GENS}; fwrite(e2, 4, 2, ext); }
        for (int l = 0; l < W * 64; l++) for (int o = 0; o < NOF; o++) if (drec[l][o]) { int32_t hh[8] = {l, o, 3, minp[l][o], dlen[l][o], dtr[l][o], dg0[l][o], da0[l][o]};
            fwrite(hh, 4, 8, dxo); fwrite(dbuf[l][o], 16, dlen[l][o], dxo); ndx++; }
        fclose(dxo);
        for (int l = 0; l < W * 64; l++) { for (int o = 0; o < NOF; o++) if (inexc[l][o]) LX[l][minp[l][o]][3]++;
            TE[5] += LE[l]; TD[5] += LD[l]; for (int P = 0; P < 128; P++) { TH[5][P] += LH[l][P]; for (int e = 0; e < 4; e++) TX[5][P][e] += LX[l][P][e]; } }
        FILE *xo = fopen(argv[15], "w"); fprintf(xo, "nof %d pbar %g t0 %ld\n", NOF, PBAR, T0);
        for (int ty = 1; ty < 6; ty++) { fprintf(xo, "E %d %ld %ld\n", ty, TE[ty], TD[ty]);
            for (int P = 0; P < 128; P++) { if (TH[ty][P]) fprintf(xo, "H %d %d %ld\n", ty, P, TH[ty][P]);
                if (TX[ty][P][1] | TX[ty][P][2] | TX[ty][P][3]) fprintf(xo, "X %d %d %ld %ld %ld\n", ty, P, TX[ty][P][1], TX[ty][P][2], TX[ty][P][3]); } }
        fclose(xo);
        fclose(out); fclose(ext); fclose(smp); fclose(dmp);
        printf("{\"records\": %lld, \"gens\": %lld, \"lanes\": %d, \"dumped\": %ld, \"NU\": %d, \"deep\": %ld}\n", nrec, GENS, W * 64, ndump, NU, ndx);
    }
    return 0;
}
