/* cpu.c: the GPU kernel's device code (kernel.cuh) compiled as plain C, one column after another.
 * Used only to check the kernel's logic against fl.c without a GPU (check_cpu.py). */
#include "kernel.cuh"

void cpu_run(int n, int WT, const int *nb, const unsigned char *fmask, int nf, u32 *A, u32 *B, int parity, int gens,
             int freeze, u32 *frz, u32 *ev_t, unsigned char *ev_k) {
  for (int w = 0; w < WT; w++) run_column(w, WT, n, nb, fmask, nf, parity ? B : A, parity ? A : B, gens, freeze, frz, ev_t, ev_k);
}

void cpu_reseed(int n, int WT, const unsigned char *seedable, u32 *A, u32 *B, const int *reps, int nrep, u64 seed, u64 thr) {
  for (int k = 0; k < nrep; k++) for (int i = 0; i < n; i++) {
    int r = reps[k]; u32 mask = 1u << (r & 31); size_t o = (size_t)i * WT + (r >> 5);
    if (seedable[i] && soup_bit(seed, r, i, thr)) { A[o] |= mask; B[o] |= mask; } else { A[o] &= ~mask; B[o] &= ~mask; }
  }
}
