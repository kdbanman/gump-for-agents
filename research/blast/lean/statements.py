#!/usr/bin/env python3
"""Writes STATEMENTS.md: for each headline theorem its Lean statement, copied verbatim from the source by this
script, next to the sentence it is meant to be and any difference in strength.

    python3 research/blast/lean/statements.py        (run from anywhere; rewrites STATEMENTS.md)

A = docs/AUTOMATON.md, section 3.  Th = research/theory/thickness.md, section 2 (section 4 where said).
The rows are kept here, in ROWS; a name that is not found in the sources is an error.
"""
import glob, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = {f: open(f).read() for f in sorted(glob.glob(os.path.join(HERE, 'Gump', '*.lean')) + glob.glob(os.path.join(HERE, 'mathlib', 'GumpMath', '*.lean')))}

def statement(name):
    for f, s in SRC.items():
        m = re.search(r'^theorem ' + re.escape(name) + r'\b', s, re.M)
        if not m: continue
        rest = s[m.start():]
        ends = [e.start() for e in (re.search(r' :=( by)?\s*\n', rest), re.search(r'\n  \| ', rest)) if e]
        return os.path.relpath(f, HERE), ' '.join(rest[:min(ends)].split())
    sys.exit(f'not found: {name}')

ROWS = [
 ('Definitions against the oracle', [
  ('mem_offsets_iff', 'A §2 and `reference/oracle.py` `offsets`: the 4 coplanar faces at ±2e_b ± 2e_c and the 8 perpendicular faces at ±e_a ± e_b, ±e_a ± e_c.', 'Same.'),
  ('isCell_iff', 'A §1: exactly one odd coordinate; `oracle.py` `masks`.', 'Same.'),
  ('rule_iff', 'A §2: a dead cell becomes live iff n ∈ {4,5}; a live cell stays live iff n ∈ {3,4,5}.', 'Same.'),
  ('nbrs_isCell', '(implicit in A §2) neighbours of a face are faces.', 'Same.'),
 ]),
 ('T1 to T4 and the hull', [
  ('layer_histogram', 'A, T1: for every cell and every d, its 12 neighbours are distributed over layers as Δs = −4: 1, −2: 2, 0: 6, +2: 2, +4: 1.', 'Same (a statement about the offsets, for each orientation and diagonal).'),
  ('Sealed.run_dead', 'A, T6: a dead sealed set stays dead whatever happens elsewhere.', 'Same. `Sealed` is defined on all points of Z³, cells or not.'),
  ('Sealed.union', 'A, T6: unions of sealed sets are sealed.', 'Same, for two sets.'),
  ('confinement', 'A, T2: if every cell with s > C is dead, that stays true forever.', 'Stronger: C is any integer, not only a lattice level.'),
  ('hull', 'A, T2: any finite pattern stays forever inside its diagonal hull, and the hull can only shrink.', 'Stated for any intersection of half-spaces d·p ≤ C d that contains the pattern; finiteness is not needed.'),
  ('firewall', 'A, T3: if three consecutive layers C+2, C+4, C+6 are all dead, they stay dead forever.', 'Stronger: the band is C < s ≤ C + 6 for any integer C.'),
  ('firewall_separates', 'A, T3: the two sides never influence each other again.', 'Stated for the side below the band; the other side is the same theorem for the opposite diagonal.'),
  ('slab_closed', 'A, T4: a pattern contained in m consecutive layers stays in those layers.', 'Same, for any integers A ≤ s ≤ B.'),
 ]),
 ('The bridge: the stepper, symmetries, finite seeds', [
  ('nbrs_symm', '(used by T5 and by the stepper) the neighbourhood is symmetric.', 'For cells; `nbrs_not_symm_off_cells` shows the hypothesis is needed.'),
  ('stepFin_config', '(the tie to the running automaton) the executable stepper misses no birth.', 'Equal to `step` as functions, with no hypothesis on the pattern.'),
  ('runFin_config', 'the same for n generations.', 'Same.'),
  ('symmetry_preserved', 'A §2: the dynamics is invariant under translations by cube steps × O_h; a seed\'s symmetry is preserved forever.', 'Every one of the 48 × even translations commutes with the dynamics. That these are all the symmetries of the lattice is not proved.'),
  ('finite_eventually_periodic', 'A, T2 consequences: every finite seed is eventually periodic.', 'Same; `eventually_periodic` adds the bound μ + T ≤ 2^N + 1 with N the number of hull cells.'),
  ('no_spaceship', 'A, T2 consequences: no spaceships.', 'Stronger: a later generation need only contain a translate of the seed.'),
  ('light_cone', 'A, speed limit: information moves at most 2 doubled units per generation in max-norm.', 'Same; `speed_two_attained` shows the bound is reached in one generation. Tightness beyond one generation is not proved.'),
  ('axis_halfspace_not_confining', 'A, T2: axis-aligned half-spaces do not confine.', 'One half-space (x > 0), with a witness.'),
  ('two_layers_not_firewall', 'A, T3: two dead layers are not enough.', 'One diagonal and one level, with a four-cell witness.'),
  ('cube_still', 'A: the 6 faces of a single cube are a still life.', '"Smallest" is not proved.'),
  ('lift_tstep', 'A §4: for even H the array-index torus is a proper torus.', 'The oracle\'s torus step, transcribed, equals `step` on the periodic lift. Even H only; the odd-H seam is not modelled.'),
  ('oscCert_spec', '(census) a cell list is an oscillator of exactly period P.', 'A certificate the kernel evaluates; used for line-C and for the 1,307 catalogue objects.'),
 ]),
 ('T5: the threshold lemma (Mathlib package)', [
  ('energy_identity', 'A, T5: for gump ΔE = D − Q exactly.', 'F = 2E, so drive and dissipation are doubled. The vessel is a finite set holding every live point of a run on the infinite lattice; tori are not covered.'),
  ('energy_bounds', '`research/theory/threshold.md`: −6N ≤ E ≤ 7N.', 'Same, doubled.'),
  ('period_two_of_no_O1', 'A, T5: an orbit with no such events from some time on has period ≤ 2 (reached within 26N + 1 further steps).', 'Same, with the bound 26N.'),
  ('oscillator_period_two', 'A, T5: every oscillator of period ≥ 3 has them.', 'Contrapositive form: an eventually periodic orbit without overcrowding events has period dividing 2.'),
  ('budget', '`threshold.md`: M/(N·T) ≤ 20·O1/(N·T) + 26/T.', 'Same, as a sum over any window. The uncapped rule U and the Goles–Olivos theorem for it are not formalised.'),
 ]),
 ('T6 in full: sealed sets', [
  ('sealed_iff_run_dead', 'Th, Lemma 1 with its converse: W is sealed iff, dead, it stays dead whatever happens elsewhere.', 'Same, for sets of cells (points that are not cells are never alive).'),
  ('exists_birth', 'Th, Lemma 1, converse: if some c ∈ W has out(c, W) ≥ 4, there is a configuration with W dead whose successor has c alive.', 'Same.'),
  ('no_finite_sealed', 'A, T6 and Th, Theorem 3: in the full lattice no finite set is sealed.', 'Stronger: any nonempty finite set of points, cells or not.'),
  ('exists_six_outside', 'Th, proof of Theorem 3: 6 of the 12 neighbours of the maximiser are outside W.', 'Same.'),
  ('slab_not_sealed_of_finite', 'A, T6 and Th, Theorem 3: in a slab of three or more layers no finite set is sealed.', 'Same; "three layers" is the hypothesis that three odd levels s, s+2, s+4 lie in [A, B].'),
  ('sealed_component_infinite', 'Th, Theorem 3 with Lemma 2: every component of a sealed set is infinite.', 'Same (full lattice); `slab_component_infinite` is the slab version.'),
  ('hull_component_touches', 'A, T6 and Th, Theorem 3: in a diagonal-hull vessel every component of a sealed set is adjacent to the outside.', 'Stronger: the cell found has at least three neighbours outside the vessel.'),
  ('torus_slab_loop', 'Th, Theorem 3: on a torus slab every component of a nonempty sealed set contains a non-contractible loop.', 'Stated on the universal cover: two different points of one component with the same image under any map with finitely many values on W. That "sealed on the torus" equals "the lift is sealed in the infinite slab" is not proved here.'),
  ('hexagon_sealed', 'A, T6 and Th, Theorem 4 (i): the 6 cells of a kagome hexagon ring form a sealed set (in one layer).', 'Every closed kagome walk of six distinct cells, in every layer of every diagonal. That such walks are exactly the hexagon rings is a modelling choice.'),
  ('layer_sealed_six', 'Th, Theorem 4 (i): no sealed set has fewer cells.', 'Stronger than the source, where minimality was a SAT search in a patch: here every nonempty finite set sealed in a layer has at least 6 cells, for every layer and diagonal.'),
  ('halfPlane_sealed', 'A, T6 and Th, Theorem 4 (ii): every half-plane of a layer is sealed.', 'Same, for any integer direction.'),
  ('layer_halfPlane_dead', 'Th, Theorem 4 (ii): a one-layer pattern never leaves the convex hull of its live cells.', 'Weaker in form: stated half-plane by half-plane. That the complement of a convex hull of lattice points is a union of integer half-planes is not formalised.'),
  ('set36_all_sealed', 'A, T6 and Th, Proposition 5: in two layers a 36-cell set is sealed.', 'Existence only, for every two-layer slab. The set is from a fresh SAT run and has not been compared with `sealed.py`\'s. Minimality (36) is not in Lean.'),
  ('sealed_iff_nine', 'A, T6 remark: "at most 3 neighbours outside" is "at least 9 inside".', 'Same.'),
  ('core_nine', 'A, T6 remark: the largest dead sealed set is the 9-core of the graph induced on the dead cells.', 'Same; `core D` is the union of the sealed subsets of D.'),
  ('core_iff_not_bp', 'A, T6 remark: it is the set never reached when the live cells are closed under bootstrap percolation with threshold 4.', 'Same; the closure is defined as the least closed superset, not by rounds.'),
  ('skeleton_mono', 'A, T6: the largest dead sealed set K(t) only grows.', 'Same; `slabSkeleton_mono` is the version inside a slab.'),
  ('pocket_autonomous', 'Th §4, reduction: the pockets a dead sealed set encloses evolve independently.', 'Same.'),
  ('finite_pocket_periodic', 'Th §4, reduction: a finite pocket is eventually periodic.', 'With the bound: transient plus period at most t₀ + 2^N.'),
  ('beyond_sealed_iff', '(new; A, T2 says only that axis-aligned half-spaces do not confine) for a primitive integer direction, the far side of a plane is sealed iff the direction is a body diagonal.', 'New. Primitivity is given by a witness w with u·w = 1; the reduction of a non-primitive direction is not proved.'),
  ('sealed_unbounded', '(new; sharpens Theorem 3) a nonempty sealed set is unbounded along every generic direction.', 'New; `slab_sealed_unbounded` is the in-plane version in thick slabs.'),
 ]),
]

out = ['# Lean statements against their sources', '',
       'Written by `python3 research/blast/lean/statements.py`; the Lean statements are copied from the files by the',
       'script. A = `docs/AUTOMATON.md` §3; Th = `research/theory/thickness.md` §2. Every theorem here is in `Axioms.lean`',
       'and `check.sh` fails if any rests on more than `propext`, `Classical.choice`, `Quot.sound`.', '']
for title, rows in ROWS:
    out += [f'## {title}', '']
    for name, src, diff in rows:
        f, st = statement(name)
        out += [f'### `{name}` (`{f}`)', '', '```lean', st, '```', '', f'- **Meant to be:** {src}', f'- **Difference:** {diff}', '']
open(os.path.join(HERE, 'STATEMENTS.md'), 'w').write('\n'.join(out))
print(sum(len(r) for _, r in ROWS), 'statements written')
