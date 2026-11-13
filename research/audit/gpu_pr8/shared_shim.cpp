/* CPU emulation of kernel_shared.cuh (PR 8): the kernel source is included unchanged except for one textual
 * substitution done by shared_cpu_check.py ("extern __shared__ u32 sm[];" -> "u32 *sm = g_sm;").
 * One block = K_T POSIX threads; __syncthreads = a block-wide barrier; __shfl_xor_sync = write to a per-block
 * buffer, barrier, read lane^o, barrier (valid because every call site is reached by all threads of the block in
 * the same order); atomicOr = a real atomic. Shared memory is filled with garbage before each block so that reads of
 * uninitialised shared memory would show. Blocks run one after another. */
#include <pthread.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "kernel.cuh"
struct Dim3 { int x; };
static pthread_barrier_t bar;
static u32 *g_sm;
static u32 shfl_buf[1024];
static thread_local int t_tid, t_bid;
#define threadIdx (Dim3{t_tid})
#define blockIdx (Dim3{t_bid})
#define __syncthreads() pthread_barrier_wait(&bar)
#define __global__
#define __launch_bounds__(a, b)
#define __ffs(x) __builtin_ffs(x)
static inline u32 __shfl_xor_sync(u32, u32 v, int o) {
  shfl_buf[t_tid] = v; pthread_barrier_wait(&bar);
  u32 r = shfl_buf[t_tid ^ o]; pthread_barrier_wait(&bar); return r;
}
static inline u32 atomicOr(u32 *p, u32 v) { return __atomic_fetch_or(p, v, __ATOMIC_SEQ_CST); }
#include "kernel_shared_sub.cuh"

struct Args { const u32 *pk, *fe; u32 *GA, *GB; int gens, freeze; u32 *frz, *ev_t; unsigned char *ev_k; int tid, bid; };
static void *thr(void *p) {
  Args *a = (Args *)p; t_tid = a->tid; t_bid = a->bid;
  gump_shared(a->pk, a->fe, a->GA, a->GB, a->gens, a->freeze, a->frz, a->ev_t, a->ev_k);
  return NULL;
}
extern "C" void run(int blocks, const u32 *pk, const u32 *fe, u32 *GA, u32 *GB, int gens, int freeze, u32 *frz,
                    u32 *ev_t, unsigned char *ev_k) {
  size_t smw = (size_t)K_WB * K_NP + 30 * K_WB;
  g_sm = (u32 *)malloc(4 * smw);
  pthread_t th[K_T]; Args a[K_T];
  for (int b = 0; b < blocks; b++) {
    memset(g_sm, 0xA5, 4 * smw);
    pthread_barrier_init(&bar, NULL, K_T);
    for (int t = 0; t < K_T; t++) { a[t] = Args{pk, fe, GA, GB, gens, freeze, frz, ev_t, ev_k, t, b}; pthread_create(&th[t], NULL, thr, &a[t]); }
    for (int t = 0; t < K_T; t++) pthread_join(th[t], NULL);
    pthread_barrier_destroy(&bar);
  }
  free(g_sm);
}
