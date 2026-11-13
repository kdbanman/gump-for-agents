/* CPU emulation of kernel_shared.cuh (PR 8) with user-level threads (ucontext), single OS thread.
 * The kernel source is included unchanged except for one textual substitution done by the driver
 * ("extern __shared__ u32 sm[];" -> "u32 *sm = g_sm;").
 * One block = K_T coroutines run round-robin; __syncthreads = yield to the scheduler, which resumes the next
 * coroutine; a full round of K_T resumes is one barrier phase (every thread runs to its next barrier, in tid order).
 * __shfl_xor_sync = write to a per-block buffer, barrier, read lane^o, barrier (valid: every call site is reached by
 * all threads of the block in the same order, and the kernel has no divergent __syncthreads).
 * A barrier-count check aborts if threads ever disagree on the number of barriers passed (a divergence the GPU
 * would deadlock or misbehave on). Shared memory is filled with garbage before each block. Blocks run in turn.
 * Faster replacement for shared_shim.cpp (pthreads), which is too slow on one core. */
#include <ucontext.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include "kernel.cuh"
struct Dim3 { int x; };
static u32 *g_sm;
static u32 shfl_buf[1024];
static int g_tid, g_bid;
static ucontext_t sched_ctx, th_ctx[1024];
static long nbar[1024];
static void cu_barrier() { nbar[g_tid]++; swapcontext(&th_ctx[g_tid], &sched_ctx); }
#define threadIdx (Dim3{g_tid})
#define blockIdx (Dim3{g_bid})
#define __syncthreads() cu_barrier()
#define __global__
#define __launch_bounds__(a, b)
#define __ffs(x) __builtin_ffs(x)
static inline u32 __shfl_xor_sync(u32, u32 v, int o) {
  int me = g_tid; shfl_buf[me] = v; cu_barrier();
  u32 r = shfl_buf[me ^ o]; cu_barrier(); return r;
}
static inline u32 atomicOr(u32 *p, u32 v) { u32 o = *p; *p = o | v; return o; }
#include "kernel_shared_sub.cuh"

struct Args { const u32 *pk, *fe; u32 *GA, *GB; int gens, freeze; u32 *frz, *ev_t; unsigned char *ev_k; };
static Args g_a;
static int done_[1024];
static void entry(int tid) {
  gump_shared(g_a.pk, g_a.fe, g_a.GA, g_a.GB, g_a.gens, g_a.freeze, g_a.frz, g_a.ev_t, g_a.ev_k);
  done_[tid] = 1;
  swapcontext(&th_ctx[tid], &sched_ctx);
}
extern "C" int run(int blocks, const u32 *pk, const u32 *fe, u32 *GA, u32 *GB, int gens, int freeze, u32 *frz,
                   u32 *ev_t, unsigned char *ev_k) {
  size_t smw = (size_t)K_WB * K_NP + 30 * K_WB;
  g_sm = (u32 *)malloc(4 * smw);
  const size_t STK = 1 << 17;
  char *stacks = (char *)malloc(STK * K_T);
  g_a = Args{pk, fe, GA, GB, gens, freeze, frz, ev_t, ev_k};
  int bad = 0;
  for (int b = 0; b < blocks; b++) {
    memset(g_sm, 0xA5, 4 * smw);
    g_bid = b;
    for (int t = 0; t < K_T; t++) {
      getcontext(&th_ctx[t]); th_ctx[t].uc_stack.ss_sp = stacks + STK * t; th_ctx[t].uc_stack.ss_size = STK;
      th_ctx[t].uc_link = NULL; makecontext(&th_ctx[t], (void (*)())entry, 1, t); done_[t] = 0; nbar[t] = 0;
    }
    for (;;) {
      int alive = 0;
      for (int t = 0; t < K_T; t++) if (!done_[t]) { g_tid = t; swapcontext(&sched_ctx, &th_ctx[t]); alive++; }
      for (int t = 1; t < K_T; t++) if (nbar[t] != nbar[0] || done_[t] != done_[0]) bad = 1;
      if (bad || !alive) break;
    }
    if (bad) break;
  }
  free(stacks); free(g_sm);
  return bad;
}
