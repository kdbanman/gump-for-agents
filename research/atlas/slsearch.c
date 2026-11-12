/* Exhaustive still-life enumeration for gump (B45/S345 on the faces of the cubic honeycomb).
 *
 * Search space: every finite still life S with |S| <= N whose live cells are connected under
 * R = "neighbours, or share a common neighbour" (distance <= 2 in the 12-neighbour graph).
 * Every still life is a disjoint union of R-separated R-connected still lifes, so this is complete.
 * Each class up to translations x O_h (48) is printed exactly once.
 *
 * Method: decision tree over cell states (live/dead) with unit propagation of the rule's
 * constraints (live: 3<=n<=5, dead: n not in {4,5}).  Translation is fixed by making the
 * lexicographically smallest live cell p0 (three runs, one per normal axis of p0).
 * A node is a leaf when every cell within graph distance 2 of a live cell is decided; the
 * leaf's live set is then a still life (all constraints are checked by propagation), and every
 * R-connected still life with lex-min cell p0 is reached by exactly one leaf.  Orientation:
 * a solution is printed only if its own normal form equals its canonical form (min over 48).
 *
 * Mode 1 ("strong", -s): live cells are linked if neighbours, or if they share a dead neighbour
 * with >= 6 live neighbours.  Every STRICT still life is strongly connected (if S splits into two
 * strongly-separated parts, every dead cell seeing both sees <= 3 from each, so each part is a
 * still life on its own).  Leaf rule: a dead neighbour x of a live cell stays pending only while
 * L(x)+U(x) >= 6; completeness for strongly-connected S follows because a strong link through x
 * needs count_S(x) >= 6 <= L+U.
 *
 * usage: slsearch N [axis] [-s]   prints "n x,y,z x,y,z ..." per class; stats on stderr
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { UNK = 0, LIVE = 1, DEAD = 2 };
static int B, N;
static unsigned char *st, *Lc, *Uc, *ax;
static int nb[3][12];          /* index deltas */
static int nbd[3][12][3];      /* coordinate deltas */
static int *trail, tp, *queue, qh, qt;
static int lv[64], nlive;
static long long nodes, leaves, printed;
static long long count_by_n[64];
static int strong;

static inline int IDX(int x, int y, int z) { return (x * B + y) * B + z; }

static int axis_from_xyz(int x, int y, int z) {
    int o = (x & 1) + (y & 1) + (z & 1);
    if (o != 1) return 3;
    return (x & 1) ? 0 : (y & 1) ? 1 : 2;
}

static int assign(int c, int s) {
    if (s == LIVE) { if (nlive >= N) return 0; lv[nlive++] = c; }
    st[c] = s; trail[tp++] = c;
    int a = ax[c];
    for (int k = 0; k < 12; k++) {
        int n = c + nb[a][k];
        Uc[n]--; if (s == LIVE) Lc[n]++;
        if (st[n] != UNK) queue[qt++] = n;
    }
    queue[qt++] = c;
    return 1;
}

static void undo(int mark) {
    while (tp > mark) {
        int c = trail[--tp]; int s = st[c]; int a = ax[c];
        for (int k = 0; k < 12; k++) { int n = c + nb[a][k]; Uc[n]++; if (s == LIVE) Lc[n]--; }
        if (s == LIVE) nlive--;
        st[c] = UNK;
    }
}

static int propagate(void) {
    while (qh < qt) {
        int q = queue[qh++]; int l = Lc[q], u = Uc[q], h = l + u; int a = ax[q];
        if (st[q] == LIVE) {
            if (l > 5 || h < 3) return 0;
            if (u > 0 && (h == 3 || l == 5)) {
                int s = (h == 3) ? LIVE : DEAD;
                for (int k = 0; k < 12; k++) { int n = q + nb[a][k]; if (st[n] == UNK && !assign(n, s)) return 0; }
            }
        } else if (st[q] == DEAD) {
            if (l >= 4 && h <= 5) return 0;
            if (u > 0) {
                int s = -1;
                if (l == 3 && h < 6) s = DEAD;          /* must stay <= 3 */
                else if (l >= 4 && l <= 5 && h == 6) s = LIVE; /* must reach 6 */
                if (s >= 0)
                    for (int k = 0; k < 12; k++) { int n = q + nb[a][k]; if (st[n] == UNK && !assign(n, s)) return 0; }
            }
        }
    }
    return 1;
}

/* canonical form */
static int perms[6][3] = {{0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0}};
static int cmpint(const void *a, const void *b) { int x = *(const int *)a, y = *(const int *)b; return (x > y) - (x < y); }
static void normal_form(int n, int (*p)[3], int *out) {
    int mn[3] = {1 << 30, 1 << 30, 1 << 30};
    for (int i = 0; i < n; i++) for (int k = 0; k < 3; k++) if (p[i][k] < mn[k]) mn[k] = p[i][k];
    for (int k = 0; k < 3; k++) mn[k] = (mn[k] >= 0) ? (mn[k] / 2) * 2 : -(((-mn[k]) + 1) / 2) * 2;
    for (int i = 0; i < n; i++) {
        int x = p[i][0] - mn[0], y = p[i][1] - mn[1], z = p[i][2] - mn[2];
        out[i] = (x * 1024 + y) * 1024 + z;
    }
    qsort(out, n, sizeof(int), cmpint);
}

static void leaf(void) {
    int n = nlive; int P[64][3], Q[64][3]; int own[64], cur[64], best[64];
    for (int i = 0; i < n; i++) { int c = lv[i]; P[i][0] = c / (B * B); P[i][1] = (c / B) % B; P[i][2] = c % B; }
    normal_form(n, P, own);
    memcpy(best, own, sizeof(int) * n);
    for (int pi = 0; pi < 6; pi++) for (int sg = 0; sg < 8; sg++) {
        for (int i = 0; i < n; i++) for (int k = 0; k < 3; k++) Q[i][k] = ((sg >> k) & 1 ? -1 : 1) * P[i][perms[pi][k]];
        normal_form(n, Q, cur);
        for (int i = 0; i < n; i++) { if (cur[i] != best[i]) { if (cur[i] < best[i]) memcpy(best, cur, sizeof(int) * n); break; } }
    }
    if (memcmp(best, own, sizeof(int) * n) != 0) return;
    printed++; count_by_n[n]++;
    printf("%d", n);
    for (int i = 0; i < n; i++) printf(" %d,%d,%d", best[i] >> 20, (best[i] >> 10) & 1023, best[i] & 1023);
    printf("\n");
}

/* lower bound on live cells still to be added: greedy packing of pending demands whose
   unknown neighbourhoods are pairwise disjoint (live cells needing 3-L, dead cells at 4-5 needing 6-L) */
static unsigned char *claim;
static int claimed[4096], ncl;
static int bound_ok(void) {
    int need = 0; ncl = 0;
    for (int pass = 0; pass < 2; pass++)
    for (int i = 0; i < nlive; i++) {
        int c = lv[i], a = ax[c];
        if (pass == 0) {
            int k = 3 - Lc[c]; if (k <= 0) continue;
            int hit = 0; for (int j = 0; j < 12; j++) { int n = c + nb[a][j]; if (st[n] == UNK && claim[n]) { hit = 1; break; } }
            if (hit) continue;
            need += k;
            for (int j = 0; j < 12; j++) { int n = c + nb[a][j]; if (st[n] == UNK) { claim[n] = 1; claimed[ncl++] = n; } }
        } else {
            for (int j = 0; j < 12; j++) {
                int d = c + nb[a][j]; if (st[d] != DEAD || Lc[d] < 4 || Lc[d] > 5 || Uc[d] == 0 || claim[d] == 2) continue;
                int ad = ax[d], hit = 0;
                for (int t = 0; t < 12; t++) { int n = d + nb[ad][t]; if (st[n] == UNK && claim[n] == 1) { hit = 1; break; } }
                claim[d] = 2; claimed[ncl++] = d;
                if (hit) continue;
                need += 6 - Lc[d];
                for (int t = 0; t < 12; t++) { int n = d + nb[ad][t]; if (st[n] == UNK) { claim[n] = 1; claimed[ncl++] = n; } }
            }
        }
    }
    for (int i = 0; i < ncl; i++) claim[claimed[i]] = 0;
    return nlive + need <= N;
}

/* choose the branching cell: an unknown neighbour of the pending cell with least slack.
   Pending = live cell with unknown neighbours, or dead neighbour of a live cell with unknown neighbours. */
static int choose(void) {
    int bestc = -1, bestscore = 1 << 30;
    for (int i = 0; i < nlive; i++) {
        int c = lv[i], a = ax[c];
        if (Uc[c]) {
            int l = Lc[c], u = Uc[c];
            int score = (l < 3) ? (u - (3 - l)) : (l == 4 ? 300 + u : 400 + u);
            if (score < bestscore) { bestscore = score; bestc = c; }
        }
        for (int k = 0; k < 12; k++) {
            int d = c + nb[a][k]; if (st[d] != DEAD || Uc[d] == 0) continue;
            int l = Lc[d], u = Uc[d];
            if (strong && l + u < 6) continue;
            int score = (l >= 4) ? (u - (6 - l)) : (l == 3 ? 200 + u : 500 + 10 * (3 - l) + u);
            if (score < bestscore) { bestscore = score; bestc = d; }
        }
    }
    if (bestc < 0) return -1;
    int a = ax[bestc];
    for (int k = 0; k < 12; k++) { int n = bestc + nb[a][k]; if (st[n] == UNK) return n; }
    return -1;
}

static void search(void) {
    nodes++;
    if (!bound_ok()) return;
    int b = choose();
    if (b < 0) { leaves++; leaf(); return; }
    int mark = tp;
    qh = qt = 0;
    if (assign(b, LIVE) && propagate()) search();
    undo(mark); qh = qt = 0;
    if (assign(b, DEAD) && propagate()) search();
    undo(mark); qh = qt = 0;
}

int main(int argc, char **argv) {
    N = atoi(argv[1]);
    int only = -1;
    for (int i = 2; i < argc; i++) { if (!strcmp(argv[i], "-s")) strong = 1; else only = atoi(argv[i]); }
    B = 8 * N + 24; if (B & 1) B++;
    long S = (long)B * B * B;
    st = calloc(S, 1); Lc = calloc(S, 1); Uc = calloc(S, 1); ax = malloc(S); claim = calloc(S, 1);
    trail = malloc(sizeof(int) * S / 4); queue = malloc(sizeof(int) * 4000000);
    for (int a = 0; a < 3; a++) {
        int b = (a + 1) % 3, c = (a + 2) % 3, k = 0;
        for (int sb = -2; sb <= 2; sb += 4) for (int sc = -2; sc <= 2; sc += 4) { int d[3] = {0}; d[b] = sb; d[c] = sc; memcpy(nbd[a][k++], d, sizeof d); }
        for (int sa = -1; sa <= 1; sa += 2) for (int t = 0; t < 2; t++) for (int s2 = -1; s2 <= 1; s2 += 2) {
            int d[3] = {0}; d[a] = sa; d[t ? c : b] = s2; memcpy(nbd[a][k++], d, sizeof d); }
        for (int j = 0; j < 12; j++) nb[a][j] = (nbd[a][j][0] * B + nbd[a][j][1]) * B + nbd[a][j][2];
    }
    for (int x = 0; x < B; x++) for (int y = 0; y < B; y++) for (int z = 0; z < B; z++) {
        int i = IDX(x, y, z);
        int edge = (x < 3 || y < 3 || z < 3 || x >= B - 3 || y >= B - 3 || z >= B - 3);
        ax[i] = edge ? 3 : axis_from_xyz(x, y, z);
    }
    int c0 = B / 2; /* even */
    for (int a = 0; a < 3; a++) {
        if (only >= 0 && a != only) continue;
        int p[3] = {c0, c0, c0}; p[a]++;
        int p0 = IDX(p[0], p[1], p[2]);
        memset(st, UNK, S); memset(Lc, 0, S);
        for (long i = 0; i < S; i++) {
            if (ax[i] == 3) { st[i] = DEAD; continue; }
            if (i < p0) st[i] = DEAD;
        }
        for (long i = 0; i < S; i++) {
            if (ax[i] == 3) { Uc[i] = 0; continue; }
            int u = 0; for (int k = 0; k < 12; k++) if (st[i + nb[ax[i]][k]] == UNK) u++;
            Uc[i] = u;
        }
        /* note: pre-dead cells are not on the trail and are never undone */
        tp = 0; nlive = 0; qh = qt = 0;
        if (assign(p0, LIVE) && propagate()) search();
        undo(0);
        fprintf(stderr, "axis %d done: nodes %lld leaves %lld printed %lld\n", a, nodes, leaves, printed);
    }
    for (int n = 0; n <= N; n++) if (count_by_n[n]) fprintf(stderr, "n=%d classes=%lld\n", n, count_by_n[n]);
    return 0;
}
