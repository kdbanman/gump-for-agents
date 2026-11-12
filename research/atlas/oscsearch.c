/* Exhaustive enumeration of periodic patterns (still lifes and oscillators) of gump, by size.
 *
 * Search space: every orbit of period dividing P whose UNION of phases U has |U| <= N cells and is
 * connected under R = "within graph distance 2 in the 12-neighbour graph".  Every periodic pattern
 * is a disjoint union of R-separated such orbits (R-separated parts cannot influence each other),
 * so this is complete.  Printed: each orbit with exact period P (or every period dividing P with
 * -a), once per class up to translations x O_h x phase shift.
 *
 * Method: each cell carries P phase bits (unknown/0/1).  Constraint (c,t) ties x_t(c), x_{t+1}(c)
 * and the number of live neighbours of c at phase t (allowed sets: 1->1 {3,4,5}; 1->0 not {3,4,5};
 * 0->1 {4,5}; 0->0 not {4,5}); interval propagation on [L, L+U].  Translation and phase are fixed by
 * making the lexicographically smallest cell p0 of U live at phase 0 (three runs, one per axis of p0).
 * Leaf: every bit of every cell within distance 2 of U is decided; remaining unknown bits are 0.
 * Orientation/phase: printed only if the leaf's own (identity, shift 0) key is the minimum key over
 * all 48 x P transforms that keep "lex-min cell of U is live at phase 0".
 *
 * -k: kagome mode: only cells of the {111} layer through p0 (normal (1,1,1)) may be live; the
 *     symmetry group is that layer's stabiliser in O_h (axis permutations x {+1,-1}, order 12).
 * usage: oscsearch P N [-a] [-k] [axis]
 * output: "per nU pops=a,b,.. : x,y,z:bits ..." (bits: phase t is bit t)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { UNK = 0, ON = 1, OFF = 2 };
static int B, N, P, S, allper, kag;
static unsigned char *st, *Lc, *Uc, *ax, *nlb, *claim;
static int nb[3][12], nbd[3][12][3];
static int *trail, tp, *queue, qh, qt;
static int un[256], nun;
static long long nodes, leaves, printed, cnt[64][9];
static unsigned short A[2][2];

#define ST(t, c) st[(size_t)(t) * S + (c)]
#define LC(t, c) Lc[(size_t)(t) * S + (c)]
#define UC(t, c) Uc[(size_t)(t) * S + (c)]

static int setbit(int c, int t, int v) {
    if (v == ON) {
        if (nlb[c] == 0) { if (nun >= N) return 0; un[nun++] = c; }
        nlb[c]++;
    }
    ST(t, c) = v; trail[tp++] = t * S + c;
    int a = ax[c];
    for (int k = 0; k < 12; k++) {
        int n = c + nb[a][k];
        UC(t, n)--; if (v == ON) LC(t, n)++;
        queue[qt++] = t * S + n;
    }
    queue[qt++] = t * S + c;
    queue[qt++] = ((t + P - 1) % P) * S + c;
    return 1;
}

static void undo(int mark) {
    while (tp > mark) {
        int e = trail[--tp]; int t = e / S, c = e % S; int v = ST(t, c), a = ax[c];
        for (int k = 0; k < 12; k++) { int n = c + nb[a][k]; UC(t, n)++; if (v == ON) LC(t, n)--; }
        if (v == ON) { nlb[c]--; if (nlb[c] == 0) nun--; }
        ST(t, c) = UNK;
    }
}

static int forcenb(int c, int t, int v) {
    int a = ax[c];
    for (int k = 0; k < 12; k++) { int n = c + nb[a][k]; if (ST(t, n) == UNK && !setbit(n, t, v)) return 0; }
    return 1;
}

static int propagate(void) {
    while (qh < qt) {
        int e = queue[qh++]; int t = e / S, c = e % S;
        if (ax[c] == 3) continue;
        int x = ST(t, c), y = ST((t + 1) % P, c), l = LC(t, c), u = UC(t, c);
        unsigned short R = (unsigned short)(((1u << (l + u + 1)) - 1) & ~((1u << l) - 1));
        if (x != UNK && y != UNK) {
            unsigned short F = R & A[x == ON][y == ON];
            if (!F) return 0;
            if (u) {
                if (F == (1u << l)) { if (!forcenb(c, t, OFF)) return 0; }
                else if (F == (1u << (l + u))) { if (!forcenb(c, t, ON)) return 0; }
            }
        } else if (x != UNK) {
            int xx = x == ON;
            if ((R & A[xx][1]) == R) { if (!setbit(c, (t + 1) % P, ON)) return 0; }
            else if (!(R & A[xx][1])) { if (!setbit(c, (t + 1) % P, OFF)) return 0; }
        } else if (y != UNK) {
            int yy = y == ON;
            int f0 = (R & A[0][yy]) != 0, f1 = (R & A[1][yy]) != 0;
            if (!f0 && !f1) return 0;
            if (!f0) { if (!setbit(c, t, ON)) return 0; }
            else if (!f1) { if (!setbit(c, t, OFF)) return 0; }
        }
    }
    return 1;
}

/* lower bound on new union cells needed (disjoint packing of unmet minimum counts) */
static int bound_ok(void) {
    int need = 0, ncl = 0; static int cl[1 << 16];
    for (int i = 0; i < nun; i++) {
        int c0 = un[i], a0 = ax[c0];
        for (int j = -1; j < 12; j++) {
            int c = j < 0 ? c0 : c0 + nb[a0][j]; int a = ax[c];
            for (int t = 0; t < P; t++) {
                int x = ST(t, c), y = ST((t + 1) % P, c);
                if (x == UNK || y == UNK || UC(t, c) == 0) continue;
                int l = LC(t, c), u = UC(t, c);
                unsigned short R = (unsigned short)(((1u << (l + u + 1)) - 1) & ~((1u << l) - 1));
                unsigned short F = R & A[x == ON][y == ON];
                if (!F) return 0;
                int mn = __builtin_ctz(F); int k = mn - l; if (k <= 0) continue;
                int hit = 0, free_in_union = 0;
                for (int q = 0; q < 12; q++) { int n = c + nb[a][q]; if (ST(t, n) != UNK) continue;
                    if (nlb[n]) free_in_union++; else if (claim[n]) { hit = 1; break; } }
                if (hit) continue;
                k -= free_in_union; if (k <= 0) continue;
                need += k;
                for (int q = 0; q < 12; q++) { int n = c + nb[a][q]; if (ST(t, n) == UNK && !nlb[n]) { claim[n] = 1; cl[ncl++] = n; } }
            }
        }
    }
    for (int i = 0; i < ncl; i++) claim[cl[i]] = 0;
    return nun + need <= N;
}

/* branching: returns encoded (t*S+c) of an unknown bit, or -1 at a leaf */
static int choose(void) {
    int best = -1, bs = 1 << 30;
    for (int i = 0; i < nun; i++) {
        int c0 = un[i], a0 = ax[c0];
        for (int j = -1; j < 12; j++) {
            int c = j < 0 ? c0 : c0 + nb[a0][j]; int a = ax[c];
            for (int t = 0; t < P; t++) {
                if (ST(t, c) == UNK) { int sc = j < 0 ? 5 : 40; if (sc < bs) { bs = sc; best = t * S + c; } continue; }
                if (UC(t, c) == 0) continue;
                int x = ST(t, c), y = ST((t + 1) % P, c);
                int sc;
                if (y == UNK) sc = 45;
                else {
                    int l = LC(t, c), u = UC(t, c);
                    unsigned short R = (unsigned short)(((1u << (l + u + 1)) - 1) & ~((1u << l) - 1));
                    unsigned short F = R & A[x == ON][y == ON];
                    if (!F) continue;
                    int mn = __builtin_ctz(F);
                    int hi = 31 - __builtin_clz((unsigned)F);
                    if (mn > l) sc = u - (mn - l);
                    else if (hi < l + u) sc = 20 + (hi - l);
                    else sc = 50 + u;
                }
                if (sc < bs) {
                    for (int q = 0; q < 12; q++) { int n = c + nb[a][q]; if (ST(t, n) == UNK) { bs = sc; best = t * S + n; break; } }
                }
            }
        }
    }
    return best;
}

static int cmpll(const void *a, const void *b) { long long x = *(const long long *)a, y = *(const long long *)b; return (x > y) - (x < y); }
static int perms[6][3] = {{0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0}};

static void leaf(void) {
    int n = nun; int Pc[256][3]; int bits[256];
    for (int i = 0; i < n; i++) {
        int c = un[i]; Pc[i][0] = c / (B * B); Pc[i][1] = (c / B) % B; Pc[i][2] = c % B;
        int b = 0; for (int t = 0; t < P; t++) if (ST(t, c) == ON) b |= 1 << t; bits[i] = b;
    }
    /* exact period */
    int per = P;
    for (int d = 1; d < P; d++) {
        if (P % d) continue;
        int ok = 1;
        for (int i = 0; i < n && ok; i++) { int b = bits[i]; int r = ((b >> d) | (b << (P - d))) & ((1 << P) - 1); if (r != b) ok = 0; }
        if (ok) { per = d; break; }
    }
    if (!allper && per != P) return;
    long long own[256], cur[256], best[256]; int have = 0;
    for (int pi = 0; pi < 6; pi++) for (int sg = 0; sg < 8; sg++) for (int s = 0; s < P; s++) {
        if (kag && sg != 0 && sg != 7) continue;
        int Q[256][3]; int mn[3] = {1 << 30, 1 << 30, 1 << 30};
        for (int i = 0; i < n; i++) for (int k = 0; k < 3; k++) { Q[i][k] = ((sg >> k) & 1 ? -1 : 1) * Pc[i][perms[pi][k]]; if (Q[i][k] < mn[k]) mn[k] = Q[i][k]; }
        for (int k = 0; k < 3; k++) mn[k] = (mn[k] >= 0) ? (mn[k] / 2) * 2 : -(((-mn[k]) + 1) / 2) * 2;
        for (int i = 0; i < n; i++) {
            long long code = ((long long)(Q[i][0] - mn[0]) * 1024 + (Q[i][1] - mn[1])) * 1024 + (Q[i][2] - mn[2]);
            int b = bits[i]; int r = ((b >> s) | (b << (P - s))) & ((1 << P) - 1);
            cur[i] = code * 256 + r;
        }
        qsort(cur, n, sizeof(long long), cmpll);
        if (!(cur[0] & 1)) continue;   /* lex-min union cell must be live at phase 0 */
        if (pi == 0 && sg == 0 && s == 0) memcpy(own, cur, sizeof(long long) * n);
        int lt = !have;
        if (have) for (int i = 0; i < n; i++) { if (cur[i] != best[i]) { lt = cur[i] < best[i]; break; } }
        if (lt) { memcpy(best, cur, sizeof(long long) * n); have = 1; }
    }
    if (memcmp(best, own, sizeof(long long) * n)) return;
    printed++; cnt[n][per]++;
    int pops[8] = {0};
    for (int i = 0; i < n; i++) for (int t = 0; t < P; t++) if (best[i] >> t & 1) pops[t]++;
    printf("%d %d pops=", per, n);
    for (int t = 0; t < per; t++) printf(t ? ",%d" : "%d", pops[t]);
    printf(" :");
    for (int i = 0; i < n; i++) { long long code = best[i] >> 8; printf(" %lld,%lld,%lld:%lld", code >> 20, (code >> 10) & 1023, code & 1023, best[i] & 255); }
    printf("\n"); fflush(stdout);
}

static void search(void) {
    nodes++;
    if (!bound_ok()) return;
    int e = choose();
    if (e < 0) { leaves++; leaf(); return; }
    int t = e / S, c = e % S;
    int mark = tp;
    qh = qt = 0; if (setbit(c, t, OFF) && propagate()) search();
    undo(mark);
    qh = qt = 0; if (setbit(c, t, ON) && propagate()) search();
    undo(mark); qh = qt = 0;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: oscsearch P N [-a] [axis]\n"); return 1; }
    P = atoi(argv[1]); N = atoi(argv[2]); int only = -1;
    for (int i = 3; i < argc; i++) { if (!strcmp(argv[i], "-a")) allper = 1; else if (!strcmp(argv[i], "-k")) kag = 1; else only = atoi(argv[i]); }
    for (int x = 0; x < 2; x++) for (int y = 0; y < 2; y++) {
        unsigned short m = 0;
        for (int k = 0; k <= 12; k++) {
            int nx = x ? (k >= 3 && k <= 5) : (k == 4 || k == 5);
            if (nx == y) m |= 1 << k;
        }
        A[x][y] = m;
    }
    B = 8 * N + 24; S = B * B * B;
    st = calloc((size_t)P * S, 1); Lc = calloc((size_t)P * S, 1); Uc = calloc((size_t)P * S, 1);
    ax = malloc(S); nlb = calloc(S, 1); claim = calloc(S, 1);
    trail = malloc(sizeof(int) * (size_t)P * S / 4); queue = malloc(sizeof(int) * 16000000);
    for (int a = 0; a < 3; a++) {
        int b = (a + 1) % 3, c = (a + 2) % 3, k = 0;
        for (int sb = -2; sb <= 2; sb += 4) for (int sc = -2; sc <= 2; sc += 4) { int d[3] = {0}; d[b] = sb; d[c] = sc; memcpy(nbd[a][k++], d, sizeof d); }
        for (int sa = -1; sa <= 1; sa += 2) for (int t = 0; t < 2; t++) for (int s2 = -1; s2 <= 1; s2 += 2) {
            int d[3] = {0}; d[a] = sa; d[t ? c : b] = s2; memcpy(nbd[a][k++], d, sizeof d); }
        for (int j = 0; j < 12; j++) nb[a][j] = (nbd[a][j][0] * B + nbd[a][j][1]) * B + nbd[a][j][2];
    }
    for (int x = 0; x < B; x++) for (int y = 0; y < B; y++) for (int z = 0; z < B; z++) {
        int i = (x * B + y) * B + z;
        int edge = (x < 3 || y < 3 || z < 3 || x >= B - 3 || y >= B - 3 || z >= B - 3);
        int o = (x & 1) + (y & 1) + (z & 1);
        ax[i] = (edge || o != 1) ? 3 : ((x & 1) ? 0 : (y & 1) ? 1 : 2);
    }
    int c0 = B / 2; c0 -= c0 & 1;
    for (int a = 0; a < 3; a++) {
        if (only >= 0 && a != only) continue;
        int p[3] = {c0, c0, c0}; p[a]++;
        int p0 = (p[0] * B + p[1]) * B + p[2];
        for (int t = 0; t < P; t++) for (int i = 0; i < S; i++) {
            ST(t, i) = (ax[i] == 3 || i < p0 || (kag && i / (B * B) + (i / B) % B + i % B != p[0] + p[1] + p[2])) ? OFF : UNK; LC(t, i) = 0;
        }
        for (int t = 0; t < P; t++) for (int i = 0; i < S; i++) {
            if (ax[i] == 3) { UC(t, i) = 0; continue; }
            int u = 0; for (int k = 0; k < 12; k++) if (ST(t, i + nb[ax[i]][k]) == UNK) u++;
            UC(t, i) = u;
        }
        tp = 0; nun = 0; qh = qt = 0;
        if (setbit(p0, 0, ON) && propagate()) search();
        undo(0);
        fprintf(stderr, "axis %d done: nodes %lld leaves %lld printed %lld\n", a, nodes, leaves, printed);
    }
    for (int n = 0; n <= N; n++) for (int d = 1; d <= P; d++) if (cnt[n][d]) fprintf(stderr, "n=%d period=%d classes=%lld\n", n, d, cnt[n][d]);
    return 0;
}
