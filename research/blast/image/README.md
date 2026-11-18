# blast/image: the density law of a wrapped face, from its own image

Agent `image` of the blast of 2026-11-18. Question: derive ρ = ρ∞ − Σ_v f(|v|²) (research/wraplocal) from
quantities measured on a face WITHOUT the loop. Marks: [proved], [measured], [conjectured].

RESULTS_PLACEHOLDER

## The identity [proved; checked by brute force on small automata]

Let T be a face torus with a loop vector v, and C its cover unwrapped along v (the same slab with v replaced by
K·v, K ≥ 2; K → ∞ is a face without that loop). Start both from a soup (independent cells) at generation 0 and
look at whole histories x(c, t), 0 ≤ t ≤ t₁. The probability of a history is a product of local factors: the
soup weight of each cell, and for every cell and generation the indicator "x(c, t+1) = rule(x on c and its 12
neighbours at t)". Cut the tube across v into m ≥ 2 bands of cells s₀, …, s_{m−1}, each band **two graph steps
thick** (an inner and an outer half, so that the neighbours of every cell of band j lie in bands j or j ± 1 and each
rule factor touches at most two consecutive bands). Then

    P_T(s₀, …, s_{m−1}) = Π_j 𝒯(s_j, s_{j+1}) / Tr 𝒯^m      (s_m ≡ s₀),

with 𝒯 a non-negative transfer matrix on band histories, and the cover has the same 𝒯 on K·m bands. Comparing the
two products term by term (three lines),

    P_T(s₀, …, s_{m−1}) = P_C(s₀, …, s_{m−1}, and s_m = s₀) / [π(s₀) · Z],        Z = Σ_s P_C(s_m = s | s₀ = s),

where π(s) is the cover's probability of the band history s (for finite K: 𝒯^{(K−1)m}(s, s)/Tr 𝒯^{Km} in place of
π(s)·const). In words: **a torus is its cover conditioned on the seam's whole history recurring one loop along,
divided by how likely that seam history is.** Summing over the bands between,

    P_T(seam history = s) = π(s) · Q(s) / Z,     Q(s) = P_C(s_m = s | s₀ = s) / π(s)     ("recurrence ratio"),

and for any window W of cells and generations inside the seam, exactly,

    P_T(pattern π on W) = P_C(π on W) · E_C[ Q | π on W ] / Z.                                   (★)

Nothing here is specific to gump: it holds for any deterministic or probabilistic cellular automaton started from a
product measure, at every finite time, and so for the long-lived living state.

`python3 research/blast/image/chk_identity.py` (1 s): elementary automata 110, 30, 22 on rings of 4–6 cells against
their 2- and 3-fold covers, every history enumerated: the ratio P_T / P_C(·, seam recurs) depends on the strip's
history only through the seam's (largest spread 3 × 10⁻¹⁵), and with a seam ONE cell thick (not a separator) it
does not (spread 0.84): PASS.

What (★) says about the law:
- **Loops add** to first order: a torus with several short loops has one recurrence factor per loop direction, and
  Q − 1 is small.
- **Per cell, whatever the tube's length**: Q is a property of the seam, local along the tube.
- **The rate e^(−2.3|v|)** is the decay of the dependence between a band of the loop-free face and its translate by
  v, patterns and histories included: the gap of 𝒯. It is a *static* property of the loop-free living state's
  space-time measure, not a signal travelling round: hence no trace of the speed limit, and a Euclidean
  dependence on |v| rather than on the graph distance.
- **The pair correlation need not carry it.** f is Cov_C(x_c, Q)/Z: the excess recurrence of whole patterns,
  weighted by whether their centre is alive. The one-cell window gives f₁ = −C(v)(1−2ρ)/(ρ(1−ρ)) ≈ 0.14·C(v),
  which is 10⁻⁵ or less.
- **Sign**: f > 0 iff the patterns (histories) that recur at distance v more often than chance are emptier at
  their centre than the average pattern.

## The lowest-order formula and its test [measured]

If the rest of the seam is independent of the window and of its image, E_C[Q | π on W] is the window's own
recurrence ratio r_W(π) = P_C(pattern at W+v is π | pattern at W is π)/P_C(π), and (★) becomes a formula in
loop-free quantities with nothing fitted:

    f_W(v) = ρ − Σ_π x_c(π) P₂(π,π)/P(π) / Σ_π P₂(π,π)/P(π),

P the law of the window's pattern and P₂ the joint law of the patterns at W and W+v. It converges to f as W grows
to the seam. Windows tried: `c1` the cell; `c7` the cell and its 6 in-layer neighbours; `c10` the cell and its 9
neighbours in the slab (which fixes the cell's next state); `h6` the cell at 6 consecutive generations.

TABLE_PLACEHOLDER

## Method

- Vessel: the 8-layer slab on the torus (13,0),(0,13) (507 cells per face; shortest loop² 169; for every v used
  the nearest other image is ≥ |v| + 2.5 away, asserted in `img.py`). Graph from
  `research/audit/shape/geom_check.my_slab` (AUTOMATON.md's cube-index table).
- Stepper: bit-sliced numpy, 64 replicas per word (the scheme of research/wraplocal/live.py, retyped in `img.py`).
  `python3 research/blast/image/img.py check 13 0 13 1000` and `check 11 0 11 1000`: replica 0 equals
  `reference/oracle.py` cell for cell at each of 1,000 generations; with one neighbour entry replaced it fails
  at generation 2. PASS (5 s).
- Run: `python3 research/blast/image/img.py run 13 0 13 64 300 210 4 11` (4,096 replicas from 0.4 soups, 300
  generations of burn-in, a snapshot every 4 generations; about 6 minutes of one core), then
  `python3 research/blast/image/img.py ana research/scratch/blast/image/rec_13_0_13_s11.npz`. Patterns are
  tabulated per class (face, axis) of the cell; errors are the scatter of 4 blocks of 1,024 replicas.

## Not checked

NOTCHECKED_PLACEHOLDER
