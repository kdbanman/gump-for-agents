# REVIEW (referee `ref-dicehull`): the hull dice chain and the 135-cell face

Interim state 05:35 UTC 2026-11-18 (jobs still running; the tables below are replaced as they finish).
Files: `geom.py`, `rd.c` (own stepper), `validate.py`, `ana.py`, `pool.py`, `hd_anc.c` (split-hull's sampler + ancestry).

## Verdict so far

- (a) CONFIRMED: the chain by my own code gives ln tau = 9.8220 +- 0.0049 (R = 9; 41,206 deaths) and 13.6550 +- 0.0129
  (R = 11; 6,010 deaths); split-hull: 9.837 +- 0.018, 13.70 +- 0.06. Against gump's anchors: +0.003 +- 0.005, +0.022 +- 0.013.
  Living state at R = 11: P-bar 31.267, sigma 5.238 (gump 31.25, 5.24).
- (c) CORRECTED: the sampler's replications are heavy-tailed, and +- 0.042 / 0.060 at R = 17 is not an honest error.
  Fresh seeds at R = 17: 29.420 +- 0.068 (26 replications; split-hull 29.453 +- 0.042; pooled 146: 29.447 +- 0.036), so the
  number itself reproduces. But (i) the dying chains of one replication descend from 26 to 44 of its 4,096 initial
  chains, effective number 5 to 13, the largest ancestor carrying 15 to 41%; (ii) split-hull's own continued run at
  R = 15 (file `sub_R15_s2.txt`, REP 4) contains one replication with a rate 17 times the median, 14% of the sum of 97:
  with it R = 15 reads 23.323 +- 0.134 instead of 23.418 +- 0.074, and R = 13 with 169 replications reads 18.184 +- 0.030
  instead of 18.234 +- 0.065. The estimator is unbiased in the rate, so a pooled value without its rare large
  replications is too HIGH in ln tau. The "+0.09 offsets" at the blind sizes are mostly this, and the R = 17 value has
  not yet seen such a replication in 146.
- (d) The owner may be told: the chain's ln tau at 135 cells is at most about 29.45 and may be lower by 0.1 to 0.3; this
  does not separate 29.163 from 29.230 and does not show "above both".
