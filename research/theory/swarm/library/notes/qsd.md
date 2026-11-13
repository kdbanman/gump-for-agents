# Quasi-stationary distributions

Request (lead, item 8). Tags: **[paper]**, **[secondary: X]**.

S. Méléard and D. Villemonais, "Quasi-stationary distributions and population processes", Probab. Surv. 9
(2012), 340–410; arXiv:1112.4732. Read: arXiv PDF, §2.1 (definitions, Propositions 1–3), §3 (finite state
space: Theorems 7–9 and Remark 3). The rest (birth–death and diffusion processes) not read.

## Statements [paper]

Z a Markov process on E ∪ {0}, 0 absorbing, E* = E ∖ {0}, T₀ the absorption time, almost surely finite.

- α on E* is a **QSD** if P_α(Z_t ∈ A | T₀ > t) = α(A) for all t, A. A **QLD** is a limit of
  P_μ(Z_t ∈ · | T₀ > t) for some initial μ; the **Yaglom limit** is that limit from point masses, when it
  exists and does not depend on the point.
- **Proposition 1.** α is a QLD iff it is a QSD. "Yaglom limit ⇒ QSD ⇔ QLD"; there are processes with
  infinitely many QSDs.
- **Proposition 2.** If α is a QSD there is θ(α) > 0 with P_α(T₀ > t) = e^{−θ(α)t} exactly.
- **Theorem 7 (finite state space; "originally proved by Darroch and Seneta").** If the process is irreducible
  and aperiodic before extinction (some P_{t₀} restricted to E* has all entries positive), the Yaglom limit α
  exists and is the unique QSD; there is a probability π on E* with e^{θ(α)t} P_i(Z_t = j) → π_i α_j and
  P_i(T₀ > t + s)/P_j(T₀ > t) → (π_i/π_j) e^{−θ(α)s}. Proof: Perron–Frobenius for the sub-Markovian semigroup;
  α is the left and π the (normalised) right principal eigenvector, e^{−θ} the principal eigenvalue.
- **Remark 3.** sup_{i,j} |P_i(Z_t = j | T₀ > t) − α_j| ≤ C e^{−(χ − θ(α))t}, where χ − θ(α) is the gap between
  the first and second eigenvalues of the generator. If χ − θ ≫ θ the process relaxes to the QSD long before
  it dies; if χ − θ ≪ θ it dies before relaxing; in between "the constant C … plays a main role".
- **Theorem 9.** The process conditioned never to die (the Q-process) exists under the same hypotheses.

The survey works in continuous time; it cites both originals: J. N. Darroch and E. Seneta, "On
quasi-stationary distributions in absorbing discrete-time finite Markov chains", J. Appl. Probab. 2 (1965),
88–100, and the continuous-time sequel, J. Appl. Probab. 4 (1967), 192–196. Neither was opened (publisher).
In discrete time Proposition 2 reads P_α(T₀ > n) = λⁿ with λ the principal eigenvalue (the board's wording:
"exactly geometric with 1 − λ = Σ μ(x) d(x)"); I state that from the board, not from Darroch–Seneta.

**Not obtained:** P. Collet, S. Martínez, J. San Martín, *Quasi-Stationary Distributions: Markov Chains,
Diffusions and Dynamical Systems* (Springer 2013). Not open.

## Does it apply here?

- To a **dice model** of a face or edge that is a finite Markov chain: yes, provided the chain restricted to
  the non-empty states is irreducible and aperiodic. That proviso is not automatic: the board records states
  from which the true rule never empties an edge (debris touching every edge); a dice model can inherit closed
  classes of survivors, and then there is no absorption with probability one, or several QSDs.
- To the **deterministic rule in a finite vessel**: no. [mine] A deterministic map is a 0/1 matrix with one
  entry per row; restricted to the non-absorbed states its non-zero eigenvalues are roots of unity, so there
  is no QSD with 0 < λ < 1 (the same fact from the open-systems side, with a source for the criterion, is in
  `escape-rates.md` B1).
- Remark 3 is the precise form of the question "which τ?": a hazard measured among replicas older than T₀ is
  the QSD rate only if T₀ exceeds the relaxation time 1/(χ − θ), and is meaningful only if that time is much
  shorter than 1/θ. The contact-process theorems (`contact-finite.md` §3, Proposition 1.2) are proofs of
  exactly this separation in a monotone model.

## Corrections to this repository

- `requests.md` item 8: "Méléard–Villemonais survey (arXiv 1112.4732)" is right; published as Probab. Surv. 9
  (2012) 340–410. "Darroch–Seneta 1965" is the discrete-time paper; there is a 1967 continuous-time one.
- `PRIOR-ART.md` §3 cites the Collet–Martínez–San Martín book for "the killing time started in a QSD is
  exactly exponential". A source that can be opened for that sentence is Méléard–Villemonais, Proposition 2.
