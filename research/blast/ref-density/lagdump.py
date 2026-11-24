#!/usr/bin/env python3
"""ref-density: lagged correlations of the watched face and layer 1 from a time-series dump of rd.c (gump, R = 11).

  RD_DUMP=FILE rd 11 run SEED GENS 0 1 f GENS 100000 > OUT      (64 lanes: F, full-1, core-1, min(age,255) per gen)
  python3 research/blast/ref-density/lagdump.py FILE

Prints (1) the Pearson cross-correlation corr(X(t-L), Y(t)) for L = 0..8 both ways (pairs within one life, both
times past the 200-generation ageing-in), the same quantity density's LAG lines report; (2) a Granger-style
comparison: the share of the variance of F(t) explained by F's own past (lags 1..K) and the extra share when the
layer's past is added, and the same with the roles swapped; standardized coefficients of the full VAR(K).
"""
import sys
import numpy as np

K = 4


def main():
    raw = np.fromfile(sys.argv[1], np.uint8)
    G = raw.size // 256
    d = raw[:G * 256].reshape(G, 64, 4).astype(np.float64)
    F, L1, C1, age = d[:, :, 0], d[:, :, 1], d[:, :, 2], d[:, :, 3]
    print(f"{G} generations x 64 lanes")
    names = {"F": F, "full1": L1, "core1": C1}
    Lmax = 8
    print("cross-correlation corr(X(t-L), Y(t)), L = 0..8")
    for xn, yn in (("full1", "F"), ("F", "full1"), ("core1", "F"), ("F", "core1"), ("F", "F"), ("full1", "full1"), ("core1", "core1")):
        X, Y = names[xn], names[yn]
        out = []
        for L in range(Lmax + 1):
            ok = age[L:] >= 201 + L
            x, y = X[:G - L][ok], Y[L:][ok]
            out.append(np.corrcoef(x, y)[0, 1])
        print(f"  {xn:>6s} -> {yn:<6s} " + " ".join(f"{v:+.3f}" for v in out))
    # VAR(K) on standardized series
    ok = age[K:] >= 201 + K
    def lagged(Z, l):
        return Z[K - l:G - l][ok]
    for other in ("full1", "core1"):
        Z = {"F": F, other: names[other]}
        mu = {k: v[age >= 201].mean() for k, v in Z.items()}
        sd = {k: v[age >= 201].std() for k, v in Z.items()}
        S = {k: (v - mu[k]) / sd[k] for k, v in Z.items()}
        for tgt, src in (("F", other), (other, "F")):
            y = lagged(S[tgt], 0)
            own = np.column_stack([lagged(S[tgt], l) for l in range(1, K + 1)])
            oth = np.column_stack([lagged(S[src], l) for l in range(1, K + 1)])
            r2o = 1 - np.var(y - own @ np.linalg.lstsq(own, y, rcond=None)[0]) / np.var(y)
            full = np.column_stack([own, oth])
            beta = np.linalg.lstsq(full, y, rcond=None)[0]
            r2f = 1 - np.var(y - full @ beta) / np.var(y)
            print(f"VAR({K}) {tgt:>5s}(t) on its own past: R2 {r2o:.4f}; adding {src}'s past: R2 {r2f:.4f} (+{r2f - r2o:.4f});"
                  f" coefficients own {' '.join(f'{b:+.3f}' for b in beta[:K])} | {src} {' '.join(f'{b:+.3f}' for b in beta[K:])}")


if __name__ == "__main__":
    main()
