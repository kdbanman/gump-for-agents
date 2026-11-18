# ref-boom: referee's review of `research/blast/boom` (INTERIM, 04:53 UTC; 63-cell runs still going)

Own stepper `rb.c` (written from docs/AUTOMATON.md and reference/oracle.py; boom's code neither read nor run),
validated state for state against the oracle with a failing negative control on the 48-, 57-, 63- and 75-cell tori
(`python3 val.py 4 0 4 1000`, `… 1 4 21 1200`, `… 1 7 19 1000`, `… 1 9 25 1000`, each also with `neg`).

So far [measured, 48 cells, 2.5e9 face-generations, 122,130 deaths; `sh run.sh; python3 an.py r48`]:
- ln τ = 9.9267 ± 0.0029 (anchor 9.9251).
- Claim 1 at 48 cells CONFIRMED: one hump, mean launch 0.7380 ± 0.0002 of A, s.d. 0.0639·A, 97.8% above 0.60·A.
- Claim 3 at 48 cells CONFIRMED: layers 1–4 at the launch 0.738/0.637/0.561/0.504; one generation before
  0.524/0.399/0.354/0.376 (living 0.515/0.434/0.405/0.415); after 0.222/0.152/0.189/0.299. All generations with the
  same over-full face have 0.523/0.427/0.388/0.405 one generation before: a third of the under-fill is generic.
- Claim 4 at 48 cells CONFIRMED (`./rbi island 4 0 4 301 300 …; python3 ani.py i48`): clusters alone fail
  0.899, 0.631, 0.282, 0.085 (sizes 1, 2, 3, 4–6), 0.005 (7–12), 0.000 (> 12).
- Claim 2: pending.
