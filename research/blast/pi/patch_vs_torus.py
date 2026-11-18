"""PI's arithmetic: is an empty patch of a living face 'the same object' as a closed face of that shape?
   -ln P(rhombus a x b empty in the living 12 x 12 face)  minus  ln tau_face(torus a x b), against the perimeter.
   Patch values: research/NOTEBOOK.md entries of 2026-11-14/15 (GPU and CPU combined where both exist).
   Torus values: research/constant/out/points.txt (rect column), 4x4 from the card.
   python3 research/blast/pi/patch_vs_torus.py"""
rows = [  # a, b, -lnP(patch), err, ln tau(torus), err
    (4, 4, 19.4208, 0.0050, 9.9251, 0.0004),
    (4, 5, 23.364, 0.034, 12.4865, 0.0009),
    (5, 5, 28.4, 0.6, 15.6614, 0.0026),
]
print(" a b cells perimeter  -lnP - ln tau    err")
d = []
for a, b, lp, e1, lt, e2 in rows:
    per = 2 * (a + b); x = lp - lt; e = (e1 * e1 + e2 * e2) ** .5
    d.append((per, x, e)); print(f" {a} {b} {3*a*b:5d} {per:6d} {x:14.3f} {e:8.3f}")
sig = (d[1][1] - d[0][1]) / (d[1][0] - d[0][0]); c0 = d[0][1] - sig * d[0][0]
print(f"edge cost from the two precise shapes: {sig:.3f} per lattice unit of perimeter, constant {c0:.2f}")
print(f"5x5 from them: {c0 + sig * d[2][0]:.2f}  measured {d[2][1]:.2f} +- {d[2][2]:.1f}")
print("tube1d's band of a loop^2-12 tube: constant 3.81 for two edges of length 3.464 -> %.3f per unit if there were no other constant" % (3.81 / 6.928))
