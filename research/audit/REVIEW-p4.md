# Review of ledger row P4 (restated 2026-11-15): second, independent fit

Command: `python3 research/audit/p4_second_fit.py` (under 1 s; reads `research/scratch/phase/sk64.json` = set 1
and `research/scratch/audit_c/phase/sk64.json` = set 2). Written without reading `p4_lead_check.py` or
`c_rows/p4_oz.py`. Weighted least squares (scipy `curve_fit`, absolute sigma) of S = a + b/(1+ξ²k²) to the sphere
average at bin centres, errors = file errors × √24; bin-mean k (rebuilt from the 64³ lattice) changes ξ by ≤ 0.005.

## 1. OZ fits for k ≤ 2.5: ξ = 0.638 ± 0.013 and 0.659 ± 0.014; windows k ≤ 1.5 … 2.5 give 0.61–0.67 — **holds with a correction**
- k ≤ 2.5 (15 bins): set 1 ξ = 0.638 ± 0.013, χ² 8.2/15; set 2 ξ = 0.659 ± 0.014, χ² 22.8/15 (p = 0.09). Both match.
  S(0) = a + b = 3.09 and 3.12.
- Windows, every bin edge from k ≤ 1.46 to k ≤ 2.44: set 1 0.607–0.640, set 2 0.628–0.692 (set 2 gives 0.685 and
  0.692 at k ≤ 1.60, 1.74). So the range is **0.61–0.69**, not 0.61–0.67. Those short windows carry σ ≈ 0.035–0.06,
  so this is scatter, not a trend; ξ = 0.65 ± 0.03 still covers both sets' k ≤ 2.5 values.
- "Fits" is fair for set 1; for set 2 it is marginal (p = 0.09 at k ≤ 2.5, p = 0.03 at k ≤ 2.75).

## 2. Fit to k ≤ 3 gives 0.68–0.69 and fails (χ² ≈ 53, 59 on 19) — **holds**
- set 1 ξ = 0.681 ± 0.009, χ² 53.2/19 (p = 4e-5); set 2 ξ = 0.690 ± 0.009, χ² 58.8/19 (p = 6e-6).
- With the old errors the same fits give ± 0.002 and χ² 1276 and 1412: the old "0.68 ± 0.01" could not have come
  with a χ² check.

## 3. Old errors too small by √(2 × snapshots) = √24 — **holds** (exact, not approximate, for these bins)
- Reading the pre-fix `sk.py` (`git show 13f8732~1:research/phase/sk.py`): e² = Var_modes(S̄)/(c·cnt) with S̄ the
  12-snapshot mean, so the 1/cnt is already in Var_modes(S̄); and the c modes are c/2 independent ±k pairs.
  Correct e² = Var_modes(S̄)/(c/2). Ratio √(2·cnt) exactly; no self-conjugate modes lie at k ≤ 3 (they sit on the
  Nyquist planes, |k| ≥ π), so the factor is 4.8990 in every fitted bin.
- Inflation by S varying across a bin: the OZ model's variance over a bin's modes is ≤ 0.6 % (median 0.35 %) of the
  scatter sk.py used, so the corrected errors are too large by ≤ 0.3 %. Negligible. Anisotropy within a shell is
  not separated from this, but see the next point.
- Gaussian-field check: Var_modes(S̄)·cnt/S² has median 1.02 and 1.01 (range 0.77–1.22), as for exponential
  single-mode statistics.
- Empirical test: set 1 − set 2 cancels the 4 shared snapshots, leaving (8 − 8)/12, variance (8/144)(σ₁² + σ₂²) with
  σᵢ² = 12 eᵢ². Over the 22 sphere bins at k ≤ 3, χ²/bin = 1.06 with corrected errors (25.4 with old ones, i.e.
  24×). Cones: 1.11 (100), 1.21 (110), 1.76 (111, 21 bins). The 111 excess is unexplained (few-mode bins make the
  error estimate itself noisy, which biases χ² upward); it does not touch the sphere fits.

## 4. Cones agree with the sphere for k ≤ 1.5 (χ² 6.6, 6.2, 6.7 / 11, 11, 10; 17.8, 5.4, 2.3) — **holds with a correction**
- I reproduce the stated numbers exactly only by treating cone and sphere as independent
  (σ² = e_cone² + e_all²). But cone modes are a subset of the sphere's, so the right variance of the difference is
  σ_modes²(1/n_cone − 1/n_all), smaller. With it: set 1 χ² 5.4, 11.9, 10.9 on 11, 11, 10 (p 0.91, 0.37, 0.36);
  set 2 15.5, 12.6, 3.9 (p 0.16, 0.32, 0.95). Conclusion unchanged (isotropic at k ≤ 1.5), numbers different.

## Not checked
- The snapshots themselves, the `sk.py` FFT and phase conventions, and that the two sets share exactly 4
  snapshots (taken from the brief; the empirical test in 3 depends on it). Mode counts were checked: my lattice
  rebuild reproduces every bin count in both files for all four masks.
- Correlations between bins (each mode is in one bin, so none from binning) and between the two sets in the
  combined 0.65 ± 0.03; I did not derive the ± 0.03.
- Fits at other bin widths, or forms other than OZ.

## Suggested wording for the ledger row
"windows k ≤ 1.5 to 2.5 give 0.61–0.69"; set 2's k ≤ 2.5 fit is marginal (χ² 23/15); cone χ² should be the nested
values (5.4, 11.9, 10.9; 15.5, 12.6, 3.9).
