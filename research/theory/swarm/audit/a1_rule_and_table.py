"""A1.  The edge row of the 2D rule over a drive b: the table a(x,k), the alive-sets, safe and inert cells,
the anchor.  Everything is re-derived from the birth/survival lists of B34/S234.

Run:  python3 a1_rule_and_table.py
"""
from fractions import Fraction as Fr
from audit_lib import rule2d, alive_prob_table

ok = True

# threshold form used in the journals: alive next iff n <= 4 and n + x >= 3
for x in (0, 1):
    for n in range(0, 9):
        ok &= rule2d(x, n) == (1 if (n <= 4 and n + x >= 3) else 0)
print("threshold form 'n<=4 and n+x>=3' equals B34/S234 on n=0..8:", ok)

# confinement: a dead cell of row -1 has at most 2 live neighbours ((x,0) and (x,1)); row -2 at most 1 ((x,0))
print("row -1 cannot be born (needs 3, sees <= 2):", all(rule2d(0, n) == 0 for n in range(0, 3)))

# alive-sets A(x,k) = {b : alive next}
A = {(x, k): [b for b in range(3) if rule2d(x, k + b)] for x in (0, 1) for k in range(5)}
print("alive-sets A(x,k):")
for x in (1, 0):
    print("  x=%d:" % x, [A[(x, k)] for k in range(5)])
claimed = {(1, 0): [2], (1, 1): [1, 2], (1, 2): [0, 1, 2], (1, 3): [0, 1], (1, 4): [0],
           (0, 0): [], (0, 1): [2], (0, 2): [1, 2], (0, 3): [0, 1], (0, 4): [0]}
ok &= A == claimed
print("equal to the sets claimed (prob. entry 6 / theorems.md Lemma A):", A == claimed)
c02 = all((0 in A[xk]) or (2 in A[xk]) for xk in A if xk != (0, 0))
ok &= c02
print("every alive-set except (dead,0) contains 0 or 2:", c02)

# the table for a symbolic law pi: check at three exact laws
for pi in [(Fr(1, 2), Fr(0), Fr(1, 2)), (Fr(1, 4), Fr(1, 2), Fr(1, 4)), (Fr(1, 5), Fr(1, 2), Fr(3, 10))]:
    a = alive_prob_table(pi)
    p0, p1, p2 = pi
    cl = [[0, p2, p1 + p2, p0 + p1, p0], [p2, p1 + p2, 1, p0 + p1, p0]]
    ok &= a == cl
    print("pi =", [str(z) for z in pi], " table = claim 1 of probability/claims.md:", a == cl)
a = alive_prob_table((Fr(1, 2), Fr(0), Fr(1, 2)))
print("anchor table  live:", [str(z) for z in a[1]], " dead:", [str(z) for z in a[0]])

# minimal non-forced probability: each non-forced outcome (alive or dead) has probability >= min(pi0, pi2)
pi = (Fr(1, 5), Fr(1, 2), Fr(3, 10))
a = alive_prob_table(pi)
m = min(min(v, 1 - v) for row in a for v in row if 0 < v < 1)
print("least probability of a non-forced outcome at pi=(1/5,1/2,3/10):", m, ">= min(pi0,pi2) =", min(pi[0], pi[2]))
ok &= m >= min(pi[0], pi[2])
print("A1 ALL OK" if ok else "A1 FAILED")
