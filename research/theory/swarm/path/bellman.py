#!/usr/bin/env python3
"""Calculator for journal entry 17 (path line). No simulation: it evaluates one recursion on numbers typed in below.

Input: the local roots theta_k of the face population's pooled one-step table (the positive solution of
sum_k' T(k,k') exp(-theta (k'-k)) = 1, death counted as k' = 0) and the variance of the one-step change, as
functions of x = k/A.  Output:

  int Theta          the local-root integral (claim Th of round 3; by Proposition T an upper bound)
  block bound        sup_kappa kappa * Theta(kappa)                 (Proposition T', a lower bound)
  V(rho)             the value of the Bellman recursion  V(x) = min_y [ (y - x - b(x))^2 / (2 v(x)) + V(y) ],
                     b = Theta v / 2  (Gaussian closure of the one-step law; entry 17.5)
  the minimising path from the mean population down.

Default data: gump hull face A = 84, copied by hand from critic/to-path.md: roots at k = 5, 10, 40 and at
x = 0.15 ... 0.45, and the standard deviation of the step 2.0, 2.8, 3.8, 4.5, 5.0 at k = 5, 10, 20, 30, 40, from the
reply to round 3, section 2; the root at k = 8 (r = 0.556) and the mean population 42.45 from the reply to round 2.

    python3 bellman.py                 # the default; prints 0.2295, 0.1438, 0.218
    python3 bellman.py table.json      # {"A":…, "mean":…, "k":[…], "theta":[…], "var":[…]}  rows k >= 5 up to the mean

Conventions for a table: Theta(x) is constant below the first row given and 0 at x = mean/A; the variance is
proportional to x below the first row and flat above the last.
"""
import json
import sys

import numpy as np

trapz = getattr(np, "trapezoid", None) or np.trapz


def bellman(tx, th, vx, vv, rho, G=4000):
    xs = np.linspace(0.0, rho, G + 1)
    Th = np.interp(xs, tx, th)
    v = np.interp(xs, vx, vv)
    b = Th * v / 2
    V = np.full(G + 1, np.inf)
    V[0] = 0.0
    arg = np.zeros(G + 1, dtype=int)
    for i in range(1, G + 1):            # descent only: y < x
        c = (xs[:i] - xs[i] - b[i]) ** 2 / (2 * v[i]) + V[:i]
        arg[i] = int(c.argmin())
        V[i] = c[arg[i]]
    path = [G]
    while path[-1] > 0:
        path.append(arg[path[-1]])
    out = {
        "int_Theta": float(trapz(Th, xs)),
        "first_order": float(0.5 * trapz(np.abs(np.gradient(Th, xs)) * b, xs)),
        "block": float((xs * Th).max()),
        "block_at": float(xs[(xs * Th).argmax()]),
        "V": float(V[G]),
        "path": [float(xs[i]) for i in path],
    }
    return out


def default_data():
    A, mean = 84, 42.45
    rho = mean / A
    tx = np.array([0.0, 5 / A, 8 / A, 10 / A, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 40 / A, rho])
    th = np.array([0.607, 0.607, 0.587, 0.585, 0.573, 0.540, 0.504, 0.466, 0.411, 0.333, 0.228, 0.160, 0.0])
    vx = np.array([0.0, 5 / A, 10 / A, 20 / A, 30 / A, 40 / A, rho])
    vv = np.array([0.0, 4.0, 7.84, 14.44, 20.25, 25.0, 26.3]) / A
    return A, rho, tx, th, vx, vv


def from_table(d):
    A, mean = d["A"], d["mean"]
    rho = mean / A
    k = np.array(d["k"], float)
    keep = k < mean
    k, th, var = k[keep], np.array(d["theta"], float)[keep], np.array(d["var"], float)[keep]
    tx = np.concatenate([[0.0], k / A, [rho]])
    th = np.concatenate([[th[0]], th, [0.0]])
    vx = np.concatenate([[0.0], k / A, [rho]])
    vv = np.concatenate([[0.0], var / A, [var[-1] / A]])
    return A, rho, tx, th, vx, vv


if __name__ == "__main__":
    if len(sys.argv) > 1:
        A, rho, tx, th, vx, vv = from_table(json.load(open(sys.argv[1])))
    else:
        A, rho, tx, th, vx, vv = default_data()
    r = bellman(tx, th, vx, vv, rho)
    print(f"A = {A}, mean density rho = {rho:.4f}")
    print(f"int Theta (upper bound, Prop. T)        {r['int_Theta']:.4f}")
    print(f"block bound sup kappa Theta(kappa)      {r['block']:.4f}  at kappa = {r['block_at']:.3f}")
    print(f"first-order value int Theta - (1/2) int |Theta'| b   {r['int_Theta'] - r['first_order']:.4f}")
    print(f"Bellman value V(rho), Gaussian closure  {r['V']:.4f}")
    for fac in (0.8, 1.25):
        print(f"   with the variance multiplied by {fac}:  {bellman(tx, th, vx, vv * fac, rho)['V']:.4f}")
    pops = [round(x * A, 1) for x in r["path"]]
    print("minimising path, population at this A:", pops[: next(i for i, p in enumerate(pops) if p < 1.0) + 1])
