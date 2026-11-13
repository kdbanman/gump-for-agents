# Threshold networks: period two, and the energy

Request (lead, item 7): Goles–Olivos 1980; Goles–Fogelman-Soulié–Pellegrin 1985; the Goles–Martínez book.
`research/theory/threshold.md` (T5) already rests on two secondary accounts and says so. I tried the primary
papers again: all are on ScienceDirect, which refuses automated clients, and the book is not open. **None of
the three primaries was obtained.** What I can add is the exact wording of the secondary sources, read by me,
and one further paper on infinite graphs.

## What the secondary sources state [paper, for each secondary source]

**C. J. Kuhlman, H. S. Mortveit, D. Murrugarra, V. S. A. Kumar, "Bifurcations in Boolean networks",
arXiv:1108.2974v2 (DMTCS proc. AP, 2012, 29–46).** Read: introduction, §3.1, start of the appendix.

- *Theorem A.1* (their condensed English version of Goles–Olivos 1981): K = {0,1}; A = (a_ij) a **real symmetric**
  n × n matrix (no condition on the diagonal); θ ∈ Rⁿ; f_i(x) = 0 if Σ_j a_ij x_j < θ_i and 1 otherwise;
  F = (f_1, …, f_n) applied synchronously. Then for every x there is s with F^{s+2}(x) = F^s(x).
  They say the original proof "only appears in French".
- *Theorem 3.1* (theirs): the same conclusion for **bi-threshold** functions: with up-thresholds k_i^↑ and
  down-thresholds k_i^↓, f_i(x) = 1 if x_i = 0 and Σ_j a_ij x_j ≥ k_i^↑; = 0 if x_i = 1 and Σ_j a_ij x_j < k_i^↓;
  = x_i otherwise (A real symmetric).
- Their references: E. Goles and J. Olivos, "Comportement périodique des fonctions à seuil binaires et
  applications", Discrete Appl. Math. 3 (1981), 93–105; E. Goles-Chacc, F. Fogelman-Soulié and D. Pellegrin,
  "Decreasing energy functions as a tool for studying threshold networks", Discrete Appl. Math. 12 (1985),
  261–277.

**E. Goles, P. Montealegre, M. Ríos-Wilson, S. Sené, "Dynamical stability of threshold networks over
undirected signed graphs", arXiv:2309.01854.** Read: §4.1.

- *Proposition 1* (attributed to their [11] = E. Goles and J. Olivos, "Periodic behaviour of generalized
  threshold functions", Discrete Math. 30 (1980)): for a threshold network T = (G, w, b) of size n and every
  x ∈ {−1, 1}ⁿ there is t with F^t(x) = F^{t+2}(x).
- *Proposition 2, 3* (attributed to their [12] = E. Goles, "Fixed point behavior of threshold functions on a
  finite set", SIAM J. Algebraic Discrete Methods): if W is positive semi-definite the network has only fixed
  points; the energy L(x) = −½ xᵀWx + bᵀx does not increase along orbits. (As printed, for threshold networks
  in their sense; I did not check what their definition assumes about the update.)

**Tamuz–Tessler 2014** (`source-requests.md` §2) attribute the Lyapunov-functional method to Goles and Olivos
and extend it to infinite graphs of slow growth, for majority.

## Does it apply here?

As `threshold.md` says: gump without the cap ("alive next iff n + x ≥ 4") is a symmetric threshold rule with
a unit diagonal, covered by Theorem A.1 as restated above (real symmetric matrix, diagonal unrestricted) on a
finite vessel. With the cap (n ≥ 6 dies) the rule is not a threshold function of a symmetric weighted sum,
and none of these statements applies; that is T5's point. Whether the cap rule is "bi-threshold" in Kuhlman
et al.'s sense: no, their rule keeps a live cell alive for all large sums.

What I could **not** verify, because the primaries are closed: the transient bound used in `threshold.md`
(26N + 1), which depends on the constants in Goles–Fogelman-Soulié–Pellegrin; and anything from the
Goles–Martínez book.

## Corrections to this repository

- `requests.md` item 7 lists "Goles–Olivos 1980". The secondary sources cite two different Goles–Olivos papers
  for the period-two theorem: Discrete Math. 30 (1980), in English, "generalized threshold functions"
  (cited by Goles et al. 2023), and Discrete Appl. Math. 3 (1981), in French (cited and translated by Kuhlman
  et al.). `threshold.md` already lists both; a paper should cite both or check which contains the statement
  for a real symmetric matrix with arbitrary diagonal (Kuhlman et al. attribute that generality to the 1981
  paper).
