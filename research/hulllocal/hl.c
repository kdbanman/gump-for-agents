// Bit-sliced gump (B45/S345) on an arbitrary 12-neighbour cell graph, 64 replicas per uint64 word, with the
// per-cell occupation statistics of research/hulllocal. Built by hl.py (gcc -O3 -march=native -shared).
// nb[i*12 + j] = neighbour j of cell i, or n (a dead cell: X[n*W + w] == 0 always).
// inl[i]: 12-bit mask of the neighbours that lie in cell i's own layer (w.r.t. its designated diagonal).
// faces: CSR (fptr[F+1], fidx) of the face layers; a replica is retired (alive bit cleared) at the end of the first
// generation in which any face layer is empty, and contributes nothing from that generation on.
#include <stdint.h>
#include <string.h>

typedef uint64_t u64;

static void step(int n, int W, const int *nb, const u64 *X, u64 *Y, const u64 *alive, int acc, const int *inl,
                 double *live, double *birth, double *dsum, double *dinsum, double *dcnt, double *l35) {
    for (int i = 0; i < n; i++) {
        const int *q = nb + 12 * i;
        int m = inl[i];
        for (int w = 0; w < W; w++) {
            u64 c0 = 0, c1 = 0, c2 = 0, c3 = 0, i0 = 0, i1 = 0, i2 = 0;
            for (int j = 0; j < 12; j++) {
                u64 v = X[(size_t)q[j] * W + w];
                u64 t = c0 & v; c0 ^= v; v = t; t = c1 & v; c1 ^= v; v = t; t = c2 & v; c2 ^= v; c3 |= t;
                if (m >> j & 1) {
                    u64 u = X[(size_t)q[j] * W + w];
                    u64 s = i0 & u; i0 ^= u; u = s; s = i1 & u; i1 ^= u; i2 |= s;
                }
            }
            u64 x = X[(size_t)i * W + w];
            u64 n45 = ~c3 & c2 & ~c1;
            u64 n3 = ~c3 & ~c2 & c1 & c0;
            u64 y = n45 | (x & n3);
            Y[(size_t)i * W + w] = y;
            if (acc) {
                u64 a = alive[w], d = ~x & a;
                live[i] += __builtin_popcountll(x & a);
                birth[i] += __builtin_popcountll(y & ~x & a);
                dcnt[i] += __builtin_popcountll(d);
                dsum[i] += __builtin_popcountll(d & c0) + 2.0 * __builtin_popcountll(d & c1) +
                           4.0 * __builtin_popcountll(d & c2) + 8.0 * __builtin_popcountll(d & c3);
                dinsum[i] += __builtin_popcountll(d & i0) + 2.0 * __builtin_popcountll(d & i1) +
                             4.0 * __builtin_popcountll(d & i2);
                l35[i] += __builtin_popcountll(x & a & (n45 | n3));
            }
        }
    }
}

// Run `gens` generations from X (in place, (n+1)*W words). Accumulate only when acc != 0.
// popsum[f], pop2[f]: sum of the face-f population and its square over alive replica-generations.
// exposure: alive replica-generations (accumulated). Returns nothing; alive[] updated.
void run(int n, int W, const int *nb, const int *inl, u64 *X, u64 *Xt, u64 *alive, int F, const int *fptr,
         const int *fidx, int gens, int acc, double *live, double *birth, double *dsum, double *dinsum, double *dcnt,
         double *l35, double *popsum, double *pop2, double *exposure) {
    int cnt[64];
    for (int g = 0; g < gens; g++) {
        if (acc) {
            for (int w = 0; w < W; w++) *exposure += __builtin_popcountll(alive[w]);
            for (int f = 0; f < F; f++)
                for (int w = 0; w < W; w++) {
                    memset(cnt, 0, sizeof cnt);
                    for (int k = fptr[f]; k < fptr[f + 1]; k++) {
                        u64 v = X[(size_t)fidx[k] * W + w] & alive[w];
                        while (v) { cnt[__builtin_ctzll(v)]++; v &= v - 1; }
                    }
                    u64 a = alive[w];
                    for (int b = 0; b < 64; b++)
                        if (a >> b & 1) { popsum[f] += cnt[b]; pop2[f] += (double)cnt[b] * cnt[b]; }
                }
        }
        step(n, W, nb, X, Xt, alive, acc, inl, live, birth, dsum, dinsum, dcnt, l35);
        memcpy(X, Xt, (size_t)n * W * sizeof(u64));
        for (int f = 0; f < F; f++)
            for (int w = 0; w < W; w++) {
                u64 o = 0;
                for (int k = fptr[f]; k < fptr[f + 1]; k++) o |= X[(size_t)fidx[k] * W + w];
                alive[w] &= o;
            }
    }
}
