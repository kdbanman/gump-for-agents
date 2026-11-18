# research/blast/boom: the death rate of a wrapped face in two factors (boom, then kill)

Agent `boom` of the blast of 2026-11-18 (03:55–05:00 UTC). Standing account. Labels: **[measured]**,
**[conjectured]**; nothing here is proved. One stepper (`boom.c`; the kernel is the one of `../anatomy/an.c`),
validated by me state for state against `reference/oracle.py` for 1,000 generations on every vessel used, with a
failing negative control each time (`validate.py`; the `.val` files in scratch). All runs: one core, under 3 minutes.

## The answer in six sentences

1. **Every death of a wrapped face is launched from an over-full generation** [measured, 48–84 cells, tori and
   tubes]. Call the *launch* of a death the last generation with at least half the face alive. Its population is
   one hump at **0.738·A** (s.d. 0.056–0.064·A), the same at 48, 63, 75, 84 cells; 98% of launches are above 0.60·A.
   "Bust or no bust" (a fall of half the face) cuts this one hump in two at 58%; it is not two routes.
2. **The rate is exactly a sum over launches, 1/τ = Σ_p ν(p)·d(p)**, ν the frequency of a generation with population
   p, d the chance that it is a launch; both factors are exponential in the area at fixed θ = p/A, and
   **min_θ [I_up(θ) + J(θ)] = 0.2099 at θ = 0.74: I_up = 0.078 (37%), J = 0.132 ± 0.003 (63%)** [measured; the
   anchors' wide-face price is 0.2087]. Each extra live cell at the launch is half as frequent and twice as deadly.
3. **The launch is a breath of the top four layers that comes in one step from a normal face** [measured]: face
   0.73·A, layers 2, 3, 4 at 0.63, 0.56, 0.51 (normal 0.43, 0.41, 0.42), after a generation in which layers 2–4 were
   slightly under-full; one generation later 0.24, 0.16, 0.19, 0.29; then the face halves every generation (0.22,
   0.12, 0.064 of A) and is empty 5–7 generations after the launch, before the chaos has climbed back from below.
4. **The kill is a fragmentation** [measured]: a surviving cluster of 7 or more cells regrows the face 99.4% of the
   time whatever lies beneath, so a death needs the bust to leave only fragments (in dying states the largest
   cluster is 5 cells of 12). "Every cluster fails on its own, by its size" with nothing fitted gives d(p) within a
   factor 0.7–1.5 over two decades at 48 and 63 cells and a price of 0.22, but by cancellation of two errors of a
   factor 2–5 each (§4).
5. **No small map reproduces 0.2087 with nothing fitted** [measured]: one-variable Gaussian 0.188–0.197, with
   measured tails 0.211–0.219 (and it launches from the wrong place); two-variable (face, layer beneath) Gaussian
   **0.160–0.165** (right route, wrong price); the map with one generation of memory, measured tails, 0.191–0.194
   (right route). The sufficient state is (P(t−1), P(t)), not (P, layer beneath) (§5).
6. **A loop-12 tube booms exactly as often as a wide face and its bust leaves the same survivors; the discount is in
   the kill, in both classes of death** [measured, 54–84 cells] (§6). What in the kill grows like L² I did not find.

## 1. Vessels and lifetimes (`sh run_a.sh`, `sh run_d.sh`; ln τ_face = ln(face-generations / deaths))

| run | vessel | cells | face-gen. | deaths | ln τ here | anchor |
|---|---|---:|---:|---:|---|---|
| t48 | (4,0),(0,4) | 48 | 1.0e9 | 49,458 | 9.9182 ± 0.0045 | 9.9251 ± 0.0004 |
| tube54 | (1,4),(0,18), loop² 12 | 54 | 1.0e9 | 13,961 | 11.1973 ± 0.0085 | 11.1935 ± 0.0030 |
| t57 | (1,7),(0,19) | 57 | 1.0e9 | 7,167 | 11.8667 ± 0.0118 | 11.8751 ± 0.0004 |
| tube60 (+tube60b) | (1,8),(0,20), loop² 12 | 60 | 2.0e9 | 8,169 | 12.430 ± 0.011 | 12.4230 ± 0.0025 |
| t63 (+t63b) | (1,4),(0,21) | 63 | 3.6e9 | 6,977 | 13.148 ± 0.012 | 13.1622 ± 0.0007 |
| w72 | (1,4),(0,24), loops² 21, 21 | 72 | 2.0e9 | 598 | 15.046 ± 0.041 | wide line 15.040 |
| tube72 | (1,10),(0,24), loop² 12 | 72 | 1.5e9 | 548 | 14.846 ± 0.043 | wide line − 0.164 = 14.876 |
| t75 | (1,9),(0,25) | 75 | 1.5e9 | 242 | 15.663 ± 0.064 | 15.6442 ± 0.0030 |
| t84 | (1,4),(0,28) | 84 | 1.5e9 | 43 | 17.39 ± 0.15 | 17.5387 ± 0.0031 |
| tube84 | (1,12),(0,28), loop² 12 | 84 | 1.5e9 | 44 | 17.37 ± 0.15 | 17.3175 ± 0.0031 |
| h45, h63 | hull radius 9, 11 | 45, 63 | 0.9e9, 2.0e9 | 51,217; 2,430 | 9.8151 ± 0.0044; 13.642 ± 0.020 | 9.819; 13.633 |

t48 is 1.5 standard errors below its anchor (as anatomy's independent run was 1.5 above); everything else within 1.2.
A replica whose state repeats after 840 generations is restarted (0–34 per run; at most 1.1·10⁵ face-generations of
10⁹). Not looked for: transverse firewalls (anatomy saw 1 in 8,223 lives on the 60-cell tube).

## 2. Launches, and the sum rule by cloning (`python3 analyse.py NAME` → `out/NAME.txt`)

L = ceil(A/2). Launch = last generation with P ≥ L before the empty face; every death has one (41 of 49,458 lie
further back than the 32 recorded generations). The hump does not depend on L (L = 20…29 at 48 cells: mean launch
35.30…35.53).

| | t48 | t63 | t75 | t84 | tube60 | tube72 | tube84 |
|---|---|---|---|---|---|---|---|
| mean launch θ | 0.7382 ± 0.0003 | 0.7375 ± 0.0010 | 0.7330 ± 0.0037 | 0.739 ± 0.009 | 0.7338 ± 0.0010 | 0.7305 ± 0.0026 | 0.728 ± 0.009 |
| s.d. of the launch / A | 0.064 | 0.056 | 0.057 | 0.056 | 0.063 | 0.061 | 0.057 |
| generations launch → empty, median (10–90%) | 5 (3–10) | 5 (3–10) | 6 (4–11) | 5 (4–9) | 5 (3–10) | 6 (4–11) | 7 (4–10) |
| largest one-generation fall ≥ A/2 | 0.600 | 0.578 | 0.558 | 0.65 | 0.582 | 0.566 | 0.55 |
| Σ ν(p)·d_clone(p) as ln τ | 9.910 ± 0.071 | 13.11 ± 0.17 | 15.03 ± 0.52 | 17.50 ± 0.31 | 12.45 ± 0.12 | 15.16 ± 0.19 | 18.46 ± 0.24 (!) |

d by cloning (`boom clone`): up to 20,000 stored states per value of p ≥ 0.58·A (a uniform reservoir over the run),
each run 16 times for 40 generations: once untouched, 15 times with one flipped cell in layers 4–5 of the 8; a clone
counts if its face is empty before it is ≥ L again. [measured]
- **The sum rule holds** at 48, 60, 63, 72, 75 and the 84-cell torus within the errors. The 84-cell tube is 1.1
  too high: a handful of fatal parents, and values of p with none among 20,000 enter as zero with zero error, so the
  quoted error is too small there. d_clone(p) agrees with d from the natural deaths value by value where both exist
  (63 cells, p = 48, 50, 52: 7.6, 32.6, 125·10⁻⁴ against 7.7, 30.2, 124·10⁻⁴).
- **Bias test passed**: mean population of flipped against untouched clones 1…12 generations on differs by at most
  0.015 cells (±0.013) at every lag, for all parents and for parents above 0.68·A.
- **Clones share their fate**: the 16 clones of a parent count as 1.6 (48 cells), 2.1 (63), 2.8 (84) independent
  ones. The death is decided at the launch. This is why the two-stage estimate is no sampler (§7).

## 3. The two exponents (`python3 scale.py` → `out/scale.txt`)

ln(√A·ν(θA)) and ln d(θA) (natural deaths) against A at fixed θ; I_up and J are minus the slopes (wide tori 48, 63,
75, 84; d from 48, 63, 75; the √A makes ν a density in θ, so that I_up + J at the saddle is the slope of ln τ).

| θ | 0.68 | 0.70 | 0.72 | 0.74 | 0.76 | 0.78 | 0.80 |
|---|---|---|---|---|---|---|---|
| I_up | 0.039 | 0.051 | 0.063 | 0.078 | 0.094 | 0.112 | 0.131 |
| J (± 0.004) | 0.189 | 0.167 | 0.154 | 0.132 | 0.119 | 0.104 | 0.095 |
| I_up + J | 0.229 | 0.218 | 0.217 | **0.2099** | 0.212 | 0.216 | 0.226 |

[measured] Minimum 0.2099 at θ = 0.74, where the launches are; anchors: 0.2087 (63–111 cells), 0.2115 (48–84).
Check of `model`'s row (the PI asked): −d ln ν(xA)/dA without the √A, 63 → 84 cells, is 0.0568, 0.0765, 0.0993,
0.1266 at x = 0.70, 0.73, 0.76, 0.79 (model: 0.056, 0.075, 0.098, 0.127), and 0.0570, 0.0761, 0.0989, 0.1259 on the
tubes 60 → 84. Agreed to 0.001; not redone further.
J(θ) ≈ 0.5·(1 − θ) for θ ≥ 0.74, and 0 at θ = 1 (a full face is empty next generation).

## 4. The fatal launch and the kill (`python3 hidden.py NAME`, `python3 island.py NAME`, `python3 islandscale.py`)

[measured, natural deaths; 63 cells, launch p = 47; the same in units of A at 48 and on the 60-cell tube]

| generation | face P | layer beneath U | all states with that P |
|---|---|---|---|
| launch − 1 | 33.3 (normal 32.6) | 25.2 (normal 27.4) | P 33.0 |
| launch | 47 | **40.5** | U 30.8 ± 4.4 (+2.2 s.d.) |
| launch + 1 | 13.4 | **9.3** | U 23 for a typical fall from 47 |
| launch + 2 | 7.5 | 9.3 | |

A lower launch needs a fuller layer beneath (48 cells: (P, U) = (30, 31.4), (36, 30.7), (42, 28.0)).

**The boom is at least four layers deep, and the layers beneath are under-full one generation earlier**
(`sh run_e.sh; python3 deep.py e48 e63 e60` → `out/deep_*.txt`; populations of layers 1–4 as shares of A, means over
the natural deaths; s.d. of one layer's population in the living state: 0.087·A at 48 cells) [measured]:

| generation relative to the launch | face | layer 2 | layer 3 | layer 4 |
|---|---|---|---|---|
| living state (63 cells) | 0.517 | 0.435 | 0.406 | 0.416 |
| −2 | 0.496 | 0.419 | 0.399 | 0.407 |
| −1 | 0.525 | **0.399** | **0.355** | **0.377** |
| 0 (launch) | 0.732 | **0.637** | **0.562** | **0.507** |
| +1 | 0.230 | 0.154 | 0.191 | 0.297 |
| +2 | 0.127 | 0.158 | 0.242 | 0.347 |
| +3 | 0.070 | 0.176 | 0.311 | 0.409 |

(63-cell torus, 2,692 deaths. The 48-cell torus, 12,139 deaths: 0.731, 0.634, 0.562, 0.509 at the launch and 0.235,
0.157, 0.189, 0.293 one generation later; the 60-cell tube, 3,678 deaths: 0.728, 0.633, 0.561, 0.508 and 0.234,
0.157, 0.189, 0.297. The profile is the same share of A on every vessel to 0.005, tube or torus.)

So the launch is a breath of the top of the slab: with the face normal, layers 2–4 are a little under-full (by 0.4
to 0.6 s.d. each); one generation later all four layers are over-full together (the face and layer 2 by 2.3 s.d.,
layer 3 by 1.8, layer 4 by 1.1; given the face's population, layers 2, 3, 4 are +1.9, +1.6, +1.1 s.d.); then all
four crash, and the chaos comes back from below at about one layer in one to two generations (layer 4 is normal
again three generations after the launch, layer 3 is at three quarters, layer 2 has not moved), while the face
halves every generation. A death is the face losing that race. [conjectured] This is why five layers of true rule
are needed to reproduce the lifetime (research/theory/exponent), and why the layer beneath alone is not a
sufficient second variable.

Islands (`boom island`): each stored over-full state is stepped once; the live face cells are grouped into clusters
(connected through in-layer neighbours); the state is then run untouched, and once per cluster with every other face
cell killed (layers beneath untouched). Deterministic: in a given state a cluster regrows the face or it does not.

| cluster size, alone, over the layers the bust left | 1 | 2 | 3 | 4–6 | 7–12 | > 12 |
|---|---|---|---|---|---|---|
| fails to regrow the face | 0.90 | 0.64 | 0.28 | 0.08 | 0.006 | 0.000 |

(the same at 48, 60, 63 cells and for every p; anatomy's islands over a *stationary* layer: 0.86, 0.55, 0.22, 0.08, 0.02.)

| | typical bust from θ = 0.78 (63 cells) | the busts that kill |
|---|---|---|
| survivors / A | 0.31 | 0.19 |
| layer beneath / A | 0.36 | **0.15** |
| clusters; largest cluster / survivors | 4.6; 0.69 | 6.3; **0.43** (5 cells) |

d(p) four ways (63 cells; d_nat from all natural deaths; products over 20,000 states per p):

| p (θ) | d natural | every cluster fails alone, same state | Π fail(size), nothing fitted | the same with anatomy's table |
|---|---|---|---|---|
| 47 (0.746) | 4.0·10⁻⁴ | 1.8·10⁻³ | 3.5·10⁻⁴ | 4.4·10⁻³ |
| 49 (0.778) | 1.6·10⁻³ | 7.9·10⁻³ | 1.9·10⁻³ | 4.2·10⁻³ |
| 51 (0.810) | 5.6·10⁻³ | 2.1·10⁻² | 8.3·10⁻³ | 7.2·10⁻³ |
| 53 (0.841) | 1.7·10⁻² | 5.5·10⁻² | 2.7·10⁻² | 2.2·10⁻² |

[measured] The size-only product is within a factor 0.7–1.5 of the truth from θ = 0.71 to 0.86 at 48 and 63 cells,
and its slope in A gives J = 0.147 (0.74), 0.127 (0.76), 0.103 (0.78) against 0.132, 0.119, 0.104: price
min(I_up + J) ≈ 0.21–0.22 (`out/islandscale.txt`; the minimum 0.204 at θ = 0.70 printed there rests on a handful of
fragmented states and is noise). But the two assumptions are each false by a factor 2–5 and cancel: clusters of one
state fail *together* (P(all fail) is 2–5 × the product: they share the emptied layer beneath), and clusters that
each fail alone *survive together* 70–85% of the time (they feed each other; and in 20–30% of natural deaths some
cluster alone would have regrown: neighbours also crowd it out). So the PI's product is a good number and not the
mechanism. Anatomy's table (stationary layer beneath) is right above θ = 0.79 and 12 (48 cells) to 70 (63 cells) times too large at θ = 0.71.

## 5. Maps (`map.py`, `formula.py`, `map2.py`, `closure.py`, `map3.py`; all from the runs' own counts, nothing fitted)

| model | 48 cells | 63 cells | route |
|---|---|---|---|
| ln τ / A (truth) | 0.2066 | 0.2087 | launch 0.738·A → 0.21·A → halving |
| one variable P, Gaussian | 0.188 | 0.197 | 0.75 → 0.25 → slow decay |
| one variable P, measured one-step law (Legendre) | 0.211 | 0.219 | 0.73 → 0.27 → 11 slow steps |
| two variables (P, U), Gaussian (the PI's request) | **0.160** | **0.165** (60-cell tube 0.161) | (0.73, 0.68) → (0.24, 0.11) → starve: the right route |
| pair (P(t−1), P(t)), Gaussian | 0.163 | 0.169 | |
| pair (P(t−1), P(t)), measured law | 0.191 | 0.194 (tube 0.194) | 33 34 47 15 8 4 2 1 0: the observed path |

Plainly: **the two-variable Gaussian map does not give 0.21; it gives 0.16**, 22% low, because the upper tail is
thinner than Gaussian (its I_up at 0.74 is 0.062 against the measured 0.077) and so is the joint over-fill. It does
find the route unprompted: joint over-fill in one step from a normal state, joint crash, starvation on an empty
layer. In over-full states E[P′] = 98.2 − 1.28·P − 0.50·U (63 cells; the referee: 105.4 − 1.40·P − 0.555·B).
- The face does not breathe: the map's slope at its fixed point is −0.08 (63), −0.11 (48).
- **Which state is sufficient** (`closure.py`: d(p) of the Markov chain built on a state, against the natural deaths;
  every chain reproduces the total rate by flux balance, so only the *placement* of the launches is a test):

| chain on | d(p)/d natural at θ = 0.63, 0.71, 0.75, 0.79, 0.83 (48 cells, 49,390 deaths) | mean launch θ (48; 63) |
|---|---|---|
| P | 2.16, 0.66, 0.58, 0.62, 0.71 | 0.680; 0.647 |
| (P, U) | 1.90, 1.12, 0.82, 0.60, 0.47 | 0.707; 0.695 |
| (P(t−1), P(t)) | 1.00, 0.95, 0.99, 1.00, 0.97 | 0.733; 0.726 (truth 0.738) |

  The face population with one generation of memory is a sufficient state to a few per cent; the layer beneath, taken
  at the same time, is not (it does not know whether a thin face is thin after a bust).
  Cross-validated: the chains of one run against the natural deaths of an independent run of the same vessel
  (`python3 closure.py c48 against t48`, `… t63b against t63`): rate launched from ≥ 0.70·A, chain / natural =
  0.63 (P), 0.78 (P, U), 0.98 (pair) at 48 cells; 0.39, 0.64, 0.92 at 63 cells.
- A closed form, c = min_θ [I_up(θ) + λ·f(θ) − λ²σ²(θ)/2] with λ = 2(g − 1)/κ the extinction exponent of the bottom
  branch of the map (E[P′|q] = 1.21·q, Var = 0.87·q: λ = 0.49; the chain's own ratio of failure chances per cell 0.63:
  λ = 0.47), gives 0.215–0.225, and λ = 0.446 fits 0.2087 (`out/formula.txt`), but its minimum sits at θ = 0.60, not
  0.74: the PI's tangent estimate in other words, right in size and wrong about the route. Dead as a mechanism.

## 6. Tubes against wide faces (`scale.py`, `classrates.py`, `joint.py`, `lags.py`)

[measured] At 84 cells, tube (1,12),(0,28) against torus (1,4),(0,28), anchors' discount 0.221:
- mean per cell 0.51543 / 0.51754 (the known deficit), variance per cell **0.4022 / 0.3816** (+5.4%; tubes 60, 72,
  84: 0.4049, 0.4026, 0.4022; wide 63, 75, 84: 0.3879, 0.3841, 0.3816; the 48-cell torus with three loops² of 16:
  0.4151). The two cancel in the upper tail: ln ν tube − torus = +0.000, +0.006, +0.018 ± 0.003, +0.025 at
  θ = 0.69, 0.71, 0.74, 0.76. **The ν-part of the discount is +0.003 to +0.014 of 0.221.**
- the fall: E[P′ | p] 31.11 / 31.13 and Var 19.87 / 19.78 at p = 62; equal to 0.1% from p = 54 to 67.
- clusters after the bust and fail(size) the same on the 60-cell tube as on the 63-cell torus at equal θ.
- the joint over-fill is a little more frequent on the tube: P ≥ 0.70·A and U ≥ 0.64·A: +0.065 ± 0.011; P + U ≥
  1.35·A: +0.059 ± 0.008; ≥ 1.40·A: +0.10 ± 0.03 (fatal launches sit at P + U ≈ 1.37·A); Var(P + U)/A is 1.008
  against 0.967. Weighed properly (`python3 joint2.py tube72 w72`: the rate ratio that the frequencies of the launch
  states alone would give, with d(p, u) pooled over both shapes): **at 72 cells the frequency of P alone gives
  +0.013 ± 0.002 and the frequency of (P, U) gives +0.046 ± 0.007 of a discount of 0.164** (0.20 ± 0.06 in these
  runs). So about a quarter of the discount is a more frequent two-layer over-fill; the rest is in the kill at a
  given (P, U), or in layers I did not record.
- duration and path of the death: the same (mean launch → empty 6.2 against 6.3 generations at 60/63 cells; the
  dying face is 0.224, 0.122, 0.066 of A on tubes against 0.221, 0.118, 0.062 on wide faces one, two, three
  generations after the launch).

Rates by class against the wide faces' line (slope 0.20866 for every class, intercepts from t63, w72, t75, t84;
"bust" = largest one-generation fall ≥ A/2; ln rate tube − line):

| tube | all | bust deaths | no-bust deaths | bust share (wide faces 0.578–0.617) |
|---|---|---|---|---|
| 54 cells | +0.074 ± 0.014 | +0.082 ± 0.019 | +0.063 ± 0.022 | 0.583 ± 0.004 |
| 60 | +0.093 ± 0.016 | +0.103 ± 0.021 | +0.080 ± 0.024 | 0.582 ± 0.008 |
| 72 | +0.182 ± 0.044 | +0.158 ± 0.059 | +0.212 ± 0.067 | 0.566 ± 0.021 |
| 84 | +0.16 ± 0.15 | +0.10 ± 0.21 | +0.24 ± 0.22 | 0.55 ± 0.08 |

[measured] **The discount is not in the no-bust rate alone**: at 54 and 60 cells it is the same in both classes.
At 72–84 cells the bust share is 0.564 ± 0.020 on tubes against 0.602 ± 0.016 on wide faces (1.5σ): a tilt
towards no-bust deaths on longer tubes is not excluded. Since the launches are one hump, the two classes are one
route cut at an arbitrary fall, and I read this as: a tube changes the kill of every launch.
Not found: what in the kill carries a term growing like L². Candidates I could not test: the layers below the second
(a tube's chaos is itself wrapped), and the joint over-fill above.

## 7. The sampler (step 3): not delivered

The two-stage estimate (ν by plain running, d by cloning) is brute force with a pre-selection: clones of an
over-full state share its fate (1.6–2.8 independent ones of 16), because the death is decided in the generation of
the launch and a flipped cell in layers 4–5 reaches the face two generations later. At 84 cells d at the saddle is
2·10⁻⁵ and 20,000 parents give 0–1 fatal ones per p. I did not run 108, 120 or 144 cells (the plain runs queued for
ν at 108 and 120 were dropped when `model` reported the upper tail from the card). What would work [conjectured]:
perturb at the launch − 1 generation in the top two layers and reweight, or search initial conditions (shooting
moves on the state at launch − 1), since the rare object is a *state*, not a path.
The 120-cell tube: forecast 24.56 ± 0.04 by extrapolation of the anchors only (PREDICTIONS.md item 9).

## 8. The hull in the same language (`boom run` on hull_9, hull_11)

[measured] No hump: the launch populations of hull faces fall monotonically from A/2 (45 cells: 7,365, 5,743, 4,560,
3,109, 1,727, 710, 218 at p = 24, 26, …, 36): a hull face dies from a normal generation. Its return map has no
cliff (E[P′]/A after 0.75·A: 0.50 at 45 cells, 0.49 at 63, against 0.36 on wrapped faces). Launch → empty: median
9–10 generations. Deaths with a fall of half the face: **1.55 ± 0.05% (45 cells), 1.40 ± 0.24% (63)**: flat or
falling, so over 45–63 cells the bust route is not cheaper per cell than starvation on a hull (difference of prices
+0.006 ± 0.010 per cell); no sign of a switch. 84 cells not run (50 deaths would not measure 1.5%).

## 9. Forecasts (PREDICTIONS.md: block A commit a786dea before any run; block B commit 130a480)

Scored at the end of PREDICTIONS.md: seven hits or part-hits, four misses or part-misses, one void, three open (the 120-cell tube among them).

## 10. Not checked

- Anything above 84 cells. I_up + J rests on d at 48, 63, 75 cells; the 48-cell torus has loops² of 16.
- The clone estimate's error bars are too small where fatal parents are few (84 cells).
- Layers below the fourth, and the other face of the slab at the launch (in an 8-layer slab layer 4 of one face is
  layer 5 of the other); the spatial pattern of the over-fill; the joint frequency of the four-layer over-fill on
  tubes against wide faces (only (P, U) was counted).
- `closure.py`'s chains are built and tested on the same run (states with few visits could flatter chain 2 and
  chain PU; at 48 cells the dying states have thousands of visits each).
- The class rates at 72 and 84 cells have 500 and 44 deaths per shape.
- The binary was rebuilt by `validate.py` whenever `boom.c` had changed (counters M3/M4 at 04:08, the island mode
  at 04:16, the layer counters at 04:28, after which the 48-cell torus was validated again); the kernel never changed and each later vessel was validated on the binary that ran it; t63, t48, t84,
  tube84 were validated and run on the first build.
- No second reader for any of the Python.

## Files

`boom.c` (run / clone / island / trace), `geom.py`, `validate.py` (both copied from ../anatomy, paths changed),
`run_a.sh`, `run_d.sh`, `run_e.sh` (what was run; `run_b.sh`, `run_c.sh` were stopped unrun), `vessels.txt`, `layers.py`;
`analyse.py`, `scale.py`, `hidden.py`, `island.py`, `islandscale.py`, `map.py`, `formula.py`, `map2.py`, `map3.py`,
`closure.py`, `classrates.py`, `joint.py`, `joint2.py`, `lags.py`, `deep.py`; `out/` every table above. Bulk output:
`research/scratch/blast/boom/` (regenerate with the run scripts; same seeds).
