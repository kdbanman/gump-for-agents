// st.c: independent bit-sliced gump stepper on a full (unreduced) finite system with symmetric soups.
// Review of research/theory/symmetric; shares no code with sy.c.
//   st GRAPH run SEED P GENS OUT      W*64 replicas (W below), each GENS generations of renewal lives
//   st GRAPH trace SEED P GENS        lane 0 only: prints the live cell indices at every generation (validation)
// Soup: one Bernoulli(P) draw per orbit (all cells of an orbit equal), 24-bit binary-expansion construction.
// Events checked EVERY generation: face death (a face's cells all dead), transverse firewall (three cyclically
// consecutive dead layers of one family, slabs), settled (Brent: snapshot at ages 1,2,4,8,..., equality test each
// generation). Records (16 bytes): age (u32; for S the snapshot age), type (1 F, 2 W, 3 F+W same gen, 4 S, 5 open),
// mask of faces dead at the event (u16), detection age for S (u32).
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
    int trace = !strcmp(argv[2], "trace");
    u64 seed = strtoull(argv[3], 0, 10); double P = atof(argv[4]); long long GENS = atoll(argv[5]);
    for (int i = 0; i < 4; i++) s[i] = sm(&seed);
    double pp = P; for (int k = 0; k < 24; k++) { pp *= 2; pbits[k] = pp >= 1; if (pp >= 1) pp -= 1; }
    // state arrays: [cell][W], plus a zero cell at index N
    u64 *x = calloc((size_t)(N + 1) * W, 8), *y = calloc((size_t)(N + 1) * W, 8), *snap = calloc((size_t)N * W, 8), *ob = malloc(sizeof(u64) * NO);
    u64 snapok[W] = {0};
    uint32_t age[W * 64], snapage[W * 64];
    FILE *out = trace ? 0 : fopen(argv[6], "wb");
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
                    rec[0] = ty == 4 ? snapage[l] : age[l]; rec[1] = ty; rec[2] = fm; rec[3] = age[l];
                    fwrite(rec, 4, 4, out); nrec++;
                    restart |= m; age[l] = 0; snapage[l] = 0;
                }
            }
            // snapshots: lanes whose age is a power of two (and not restarting)
            u64 take = 0;
            for (int b = 0; b < 64; b++) { int l = w * 64 + b; if (!((restart >> b) & 1) && age[l] && !(age[l] & (age[l] - 1))) { take |= 1ULL << b; snapage[l] = age[l]; } }
            if (take) for (int i = 0; i < N; i++) snap[i * W + w] = (snap[i * W + w] & ~take) | (x[i * W + w] & take);
            snapok[w] = (snapok[w] | take) & ~restart;
            if (restart) { for (int o = 0; o < NO; o++) ob[o] = bern(); for (int i = 0; i < N; i++) x[i * W + w] = (x[i * W + w] & ~restart) | (ob[orb[i]] & restart); }
        }
    }
    if (!trace) {
        for (int l = 0; l < W * 64; l++) { uint32_t rec[4] = {age[l], 5, 0, age[l]}; fwrite(rec, 4, 4, out); }
        fclose(out); printf("{\"records\": %lld, \"gens\": %lld, \"lanes\": %d}\n", nrec, GENS, W * 64);
    }
    return 0;
}
