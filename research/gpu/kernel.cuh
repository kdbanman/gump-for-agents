/* kernel.cuh: gump (B45/S345) replicas on a finite cell graph, one 32-bit word = 32 replicas per GPU thread.
 *
 * Same scheme as research/fluct/fl.c (replica r lives in bit r%32 of word-column r/32 of every node), laid out
 * node-major: state[i * WT + w], WT = number of word-columns = number of threads. A thread reads and writes only
 * its own column, so threads never communicate: a launch steps `gens` generations with no synchronisation at all.
 * Neighbour index n is a sentinel row that is zero forever (cells outside the vessel, dead by T2).
 *
 * Per generation and per column the kernel also forms, for every face group f, the OR of the new state over the
 * group's nodes (a face layer is extinct iff its bit is 0), and the XOR against the state two generations back
 * (period 1 or 2 iff 0). A replica whose face dies (kind 1) or that settles (kind 2) is frozen (state forced to 0)
 * and its event generation recorded; the host reseeds frozen replicas between launches. freeze = 0 turns events
 * and freezing off (plain stepping, for validation).
 *
 * Written so that it compiles both with NVRTC (CUDA) and as plain C (CPU check against fl.c, see cpu.c).
 */
#ifdef __CUDACC_RTC__
#define DEV __device__ __forceinline__
#define LDG(p) __ldg(p)
#define FFS(x) __ffs(x)
typedef unsigned long long u64;
#else
#include <stddef.h>
#include <stdint.h>
#define DEV static inline
#define LDG(p) (*(p))
#define FFS(x) __builtin_ffs(x)
typedef uint64_t u64;
#endif
typedef unsigned int u32;

#define FA(a, b, c, s, k) { u32 _x = (a) ^ (b); s = _x ^ (c); k = ((a) & (b)) | (_x & (c)); }

/* the carry-save tree of fl.c / rep.c: 12 inputs -> 4-bit count (b3 b2 b1 b0), then B45/S345 */
DEV u32 rule12(u32 x0, u32 x1, u32 x2, u32 x3, u32 x4, u32 x5, u32 x6, u32 x7, u32 x8, u32 x9, u32 x10, u32 x11, u32 me) {
  u32 s0, c0, s1, c1, s2, c2, s3, c3, o1, t4, b0, t5, u0, f0, u1, f1, b1, f2, b2, b3;
  FA(x0, x1, x2, s0, c0); FA(x3, x4, x5, s1, c1); FA(x6, x7, x8, s2, c2); FA(x9, x10, x11, s3, c3);
  FA(s0, s1, s2, o1, t4); b0 = o1 ^ s3; t5 = o1 & s3;
  FA(c0, c1, c2, u0, f0); FA(c3, t4, t5, u1, f1); b1 = u0 ^ u1; f2 = u0 & u1;
  FA(f0, f1, f2, b2, b3);
  return ~b3 & ((b2 & ~b1) | (me & ~b2 & b1 & b0));
}

/* step column w for `gens` generations. cur/nxt: the two buffers (cur holds the present state, nxt the state one
 * generation earlier). frz: frozen replicas (in/out). ev_t[r], ev_k[r] written for replicas frozen here. */
DEV void run_column(int w, int WT, int n, const int *nb, const unsigned char *fmask, int nf,
                    u32 *cur, u32 *nxt, int gens, int freeze, u32 *frz_io, u32 *ev_t, unsigned char *ev_k) {
  u32 frz = frz_io[w];
  const size_t S = (size_t)WT;
  for (int t = 1; t <= gens; t++) {
    u32 g0 = 0, g1 = 0, g2 = 0, g3 = 0, g4 = 0, g5 = 0, g6 = 0, g7 = 0, dif = 0;
    const u32 *cw = cur + w; u32 *nw = nxt + w;
    for (int i = 0; i < n; i++) {
      const int *q = nb + 12 * i;
      u32 r = rule12(cw[S * LDG(q + 0)], cw[S * LDG(q + 1)], cw[S * LDG(q + 2)], cw[S * LDG(q + 3)],
                     cw[S * LDG(q + 4)], cw[S * LDG(q + 5)], cw[S * LDG(q + 6)], cw[S * LDG(q + 7)],
                     cw[S * LDG(q + 8)], cw[S * LDG(q + 9)], cw[S * LDG(q + 10)], cw[S * LDG(q + 11)],
                     cw[S * i]) & ~frz;
      u32 old = nw[S * i];
      dif |= r ^ old;
      nw[S * i] = r;
      unsigned m = LDG(fmask + i);
      if (m) {
        if (m & 1) g0 |= r; if (m & 2) g1 |= r; if (m & 4) g2 |= r; if (m & 8) g3 |= r;
        if (m & 16) g4 |= r; if (m & 32) g5 |= r; if (m & 64) g6 |= r; if (m & 128) g7 |= r;
      }
    }
    { u32 *tmp = cur; cur = nxt; nxt = tmp; }
    u32 dead = ~g0;
    if (nf > 1) dead |= ~g1; if (nf > 2) dead |= ~g2; if (nf > 3) dead |= ~g3; if (nf > 4) dead |= ~g4;
    if (nf > 5) dead |= ~g5; if (nf > 6) dead |= ~g6; if (nf > 7) dead |= ~g7;
    u32 newly = freeze ? (dead | ~dif) & ~frz : 0;
    while (newly) {
      int b = FFS(newly) - 1;
      ev_t[32 * w + b] = (u32)t;
      ev_k[32 * w + b] = (dead >> b & 1) ? 1 : 2;
      newly &= newly - 1;
      frz |= 1u << b;
    }
  }
  frz_io[w] = frz;
}

DEV u64 mix64(u64 z) {
  z += 0x9E3779B97F4A7C15ULL;
  z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
  z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
  return z ^ (z >> 31);
}

/* soup bit of node i for replica r: Bernoulli(thr / 2^64) on seedable nodes. Seed and replica are hashed in turn
 * (an earlier version combined them as seed ^ (r << 32), which made (seed, r) and (seed', r ^ seed ^ seed') collide
 * when seeds were themselves shifted by 32: parallel runs with seeds 1, 2, 3 repeated each other's soups). */
DEV int soup_bit(u64 seed, int r, int i, u64 thr) { return mix64(mix64(mix64(seed) + (u64)r) + (u64)i) < thr; }

#ifdef __CUDACC_RTC__
extern "C" __global__ void gump_run(int n, int WT, const int *__restrict__ nb, const unsigned char *__restrict__ fmask,
                                    int nf, u32 *A, u32 *B, int parity, int gens, int freeze, u32 *frz, u32 *ev_t,
                                    unsigned char *ev_k) {
  int w = blockIdx.x * blockDim.x + threadIdx.x;
  if (w >= WT) return;
  run_column(w, WT, n, nb, fmask, nf, parity ? B : A, parity ? A : B, gens, freeze, frz, ev_t, ev_k);
}

/* reseed replicas reps[0..nrep) with a soup (written to both buffers, so period checks start clean); one thread per
 * (replica, node); replicas sharing a word are written with atomics */
extern "C" __global__ void gump_reseed(int n, int WT, const unsigned char *__restrict__ seedable, u32 *A, u32 *B,
                                       const int *__restrict__ reps, int nrep, u64 seed, u64 thr, int layout) {
  long long idx = (long long)blockIdx.x * blockDim.x + threadIdx.x;
  if (idx >= (long long)nrep * n) return;
  int k = (int)(idx / n), i = (int)(idx % n), r = reps[k];
  u32 mask = 1u << (r & 31);
  size_t o = layout ? (size_t)(r >> 5) * (n + 1) + i : (size_t)i * WT + (r >> 5);   /* layout 1: kernel_shared */
  if (seedable[i] && soup_bit(seed, r, i, thr)) { atomicOr(A + o, mask); atomicOr(B + o, mask); }
  else { atomicAnd(A + o, ~mask); atomicAnd(B + o, ~mask); }
}
#endif
