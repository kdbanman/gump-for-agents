/* kernel_shared.cuh: the replica stepper with the state on-chip (compiled together with kernel.cuh, NVRTC only).
 *
 * One thread block owns WB word-columns (32*WB replicas) of the whole vessel and keeps their state in shared memory
 * for the whole launch; global memory is touched only at the start and the end. Threads split the nodes: thread tid
 * owns nodes j*T + tid (j < J), and keeps their 12 neighbour indices (16-bit pairs) in registers, together with the
 * new state and the state two generations back (for the period check). Nodes are numbered so that consecutive nodes
 * mostly have consecutive neighbours (gsim orders them by orientation, then lexicographically), which keeps the
 * shared-memory gathers nearly free of bank conflicts.
 *
 * Per generation:  A  evaluate the previous generation's face / settle reductions (every thread, redundantly, so
 *                     the freeze mask stays in registers); compute the new state into registers
 *                  B  write it to shared memory; warp-OR the XOR-against-two-back into dac[t%3]
 *                  C  warp-OR the face entries (each face's list padded to whole warps) into acc[t%3]
 * with a __syncthreads after each phase; the reduction buffers rotate over three generations so that zeroing,
 * accumulating and reading never overlap. Semantics are identical to gump_run in kernel.cuh (same events, same
 * generation numbers, same freezing); the global layout differs: state[(column * NP) + node].
 *
 * Compile-time constants (NVRTC -D, prefixed K_ to stay clear of NVRTC's own headers): K_N nodes, K_NP = K_N + 1
 * (row K_N = sentinel, zero forever), K_WB columns per block, K_T threads per block, K_J = ceil(K_N / K_T) nodes per
 * thread, K_Q face-entry slots per thread, K_NF faces; K_MINB = blocks per SM the register allocation must allow.
 */
DEV u32 warp_or(u32 v) {
#pragma unroll
  for (int o = 16; o; o >>= 1) v |= __shfl_xor_sync(0xffffffffu, v, o);
  return v;
}

#ifndef K_MINB
#define K_MINB 1
#endif
extern "C" __global__ void __launch_bounds__(K_T, K_MINB)
gump_shared(const u32 *__restrict__ pk, const u32 *__restrict__ fe, u32 *GA, u32 *GB, int gens, int freeze,
            u32 *frz_g, u32 *ev_t, unsigned char *ev_k) {
  extern __shared__ u32 sm[];
  u32 *cur = sm;                         /* K_WB * K_NP */
  u32 *acc = sm + K_WB * K_NP;               /* 3 x 8 x K_WB face ORs */
  u32 *dac = acc + 3 * 8 * K_WB;           /* 3 x K_WB settle ORs */
  const int tid = threadIdx.x, lane = tid & 31;
  const size_t gbase = (size_t)blockIdx.x * K_WB * K_NP;
  for (int k = tid; k < K_WB * K_NP; k += K_T) cur[k] = GA[gbase + k];
  for (int k = tid; k < 27 * K_WB; k += K_T) acc[k] = 0;
  u32 pkr[K_J][6], p2[K_J][K_WB], nr[K_J][K_WB], frz[K_WB], dif[K_WB], fer[K_Q];
#pragma unroll
  for (int j = 0; j < K_J; j++) {
#pragma unroll
    for (int k = 0; k < 6; k++) pkr[j][k] = pk[(j * 6 + k) * K_T + tid];
    const int i = j * K_T + tid;
#pragma unroll
    for (int w = 0; w < K_WB; w++) { p2[j][w] = i < K_N ? GB[gbase + w * K_NP + i] : 0; nr[j][w] = 0; }
  }
#pragma unroll
  for (int w = 0; w < K_WB; w++) { frz[w] = frz_g[blockIdx.x * K_WB + w]; dif[w] = 0; }
#pragma unroll
  for (int q = 0; q < K_Q; q++) fer[q] = fe[q * K_T + tid];
  __syncthreads();

  for (int t = 1;; t++) {
    /* A: evaluate generation t-1 */
    if (t > 1) {
      const int pb = (t - 1) % 3;
#pragma unroll
      for (int w = 0; w < K_WB; w++) {
        u32 dead = 0;
#pragma unroll
        for (int f = 0; f < K_NF; f++) dead |= ~acc[pb * 8 * K_WB + f * K_WB + w];
        const u32 newly = freeze ? (dead | ~dac[pb * K_WB + w]) & ~frz[w] : 0;
        if (tid == 0) {
          u32 m = newly;
          while (m) {
            const int b = __ffs(m) - 1, r = (blockIdx.x * K_WB + w) * 32 + b;
            ev_t[r] = (u32)(t - 1); ev_k[r] = (dead >> b & 1) ? 1 : 2;
            m &= m - 1;
          }
        }
        frz[w] |= newly;
      }
      if (t > gens) break;
      const int zb = (t + 1) % 3;
      for (int k = tid; k < 8 * K_WB; k += K_T) acc[zb * 8 * K_WB + k] = 0;
      if (tid < K_WB) dac[zb * K_WB + tid] = 0;
    }
#pragma unroll
    for (int j = 0; j < K_J; j++) {
      const int i = j * K_T + tid;
      if (i < K_N) {
        const u32 a0 = pkr[j][0], a1 = pkr[j][1], a2 = pkr[j][2], a3 = pkr[j][3], a4 = pkr[j][4], a5 = pkr[j][5];
        const int n0 = a0 & 0xffff, n1 = a0 >> 16, n2 = a1 & 0xffff, n3 = a1 >> 16, n4 = a2 & 0xffff, n5 = a2 >> 16,
                  n6 = a3 & 0xffff, n7 = a3 >> 16, n8 = a4 & 0xffff, n9 = a4 >> 16, n10 = a5 & 0xffff, n11 = a5 >> 16;
#pragma unroll
        for (int w = 0; w < K_WB; w++) {
          const u32 *c = cur + w * K_NP;
          const u32 me = c[i];
          const u32 r = rule12(c[n0], c[n1], c[n2], c[n3], c[n4], c[n5], c[n6], c[n7], c[n8], c[n9], c[n10], c[n11], me) & ~frz[w];
          dif[w] |= r ^ p2[j][w];
          p2[j][w] = me;
          nr[j][w] = r;
        }
      }
    }
    __syncthreads();
    /* B */
    const int cb = t % 3;
#pragma unroll
    for (int j = 0; j < K_J; j++) {
      const int i = j * K_T + tid;
      if (i < K_N) {
#pragma unroll
        for (int w = 0; w < K_WB; w++) cur[w * K_NP + i] = nr[j][w];
      }
    }
#pragma unroll
    for (int w = 0; w < K_WB; w++) {
      const u32 d = warp_or(dif[w]);
      if (lane == 0 && d) atomicOr(dac + cb * K_WB + w, d);
      dif[w] = 0;
    }
    __syncthreads();
    /* C */
#pragma unroll
    for (int q = 0; q < K_Q; q++) {
      const int node = fer[q] & 0xffff, f = fer[q] >> 16;
#pragma unroll
      for (int w = 0; w < K_WB; w++) {
        const u32 v = warp_or(cur[w * K_NP + node]);
        if (lane == 0 && v) atomicOr(acc + cb * 8 * K_WB + f * K_WB + w, v);
      }
    }
    __syncthreads();
  }
  for (int k = tid; k < K_WB * K_NP; k += K_T) GA[gbase + k] = cur[k];
#pragma unroll
  for (int j = 0; j < K_J; j++) {
    const int i = j * K_T + tid;
    if (i < K_N) {
#pragma unroll
      for (int w = 0; w < K_WB; w++) GB[gbase + w * K_NP + i] = p2[j][w];
    }
  }
  if (tid < K_WB) frz_g[blockIdx.x * K_WB + tid] = frz[tid];
}
