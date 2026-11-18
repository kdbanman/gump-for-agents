#!/usr/bin/env python3
"""The enumeration of enum7.py for a large instance, split on balanced cells (each part a short run).

    python3 enum_split.py FRAME C K [--seed FILE.json ...] [--minutes M] [--lo L --hi H] [--solver S]

The search space is split on K region cells at generation 0 (2^K parts that partition it).  The cells are chosen from
the solutions already known (the --seed files: partial lists of earlier runs, and the part files of this run): the K
cells whose frequency among them is nearest one half.  In each part the known solutions that belong to it are blocked
first; the part is complete when the solver answers UNSAT.  Part files: scratch/FRAME_C_part{j}.json (resumable); when
every part is complete the union is written to scratch/FRAME_C.json with complete = true.
"""
import sys, os, json, time, argparse
import orc7 as O, enum7


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('frame'); ap.add_argument('C', type=int); ap.add_argument('K', type=int)
    ap.add_argument('--seed', nargs='*', default=[]); ap.add_argument('--minutes', type=float, default=9)
    ap.add_argument('--lo', type=int, default=1); ap.add_argument('--hi', type=int, default=5); ap.add_argument('--solver', default='cadical153')
    a = ap.parse_args()
    from pysat.solvers import Solver
    tube = '' if (a.lo, a.hi) == (1, 5) else f'_{a.lo}_{a.hi}'
    stem = os.path.join(O.SCR, f'{a.frame}_{a.C}{tube}')
    cells, X, f, P = enum7.build(a.frame, a.C, a.lo, a.hi)
    ci = {c: i for i, c in enumerate(cells)}
    plan = stem + '_plan.json'
    known = set()
    for fn in a.seed:
        if os.path.exists(fn):
            known |= {tuple(sorted(ci[tuple(c)] for c in e)) for e in json.load(open(fn))['list']}
    if os.path.exists(plan):
        split = json.load(open(plan))['split']
    else:
        freq = [sum(1 for s in known if i in s) / max(1, len(known)) for i in range(len(cells))]
        split = sorted(range(len(cells)), key=lambda i: abs(freq[i] - 0.5))[:a.K]
        json.dump(dict(split=split, cells=[list(cells[i]) for i in split], freq=[freq[i] for i in split]), open(plan, 'w'))
    K = len(split)
    t00 = time.time(); alldone = True; total = set()
    for j in range(2 ** K):
        pf = f'{stem}_part{j}.json'
        bits = [(j >> b) & 1 for b in range(K)]
        mine = {s for s in known if all((split[b] in s) == bool(bits[b]) for b in range(K))}
        done = False
        if os.path.exists(pf):
            d = json.load(open(pf)); done = d['complete']
            mine |= {tuple(s) for s in d['sols']}
        if not done and time.time() - t00 < 60 * a.minutes:
            t0 = time.time()
            with Solver(name=a.solver, bootstrap_with=f.cl) as sv:
                for b in range(K):
                    sv.add_clause([X[0][split[b]] if bits[b] else -X[0][split[b]]])
                for s in mine:
                    on = set(s); sv.add_clause([(-X[0][i] if i in on else X[0][i]) for i in range(len(cells))])
                n0 = len(mine)
                while True:
                    if time.time() - t00 > 60 * a.minutes:
                        break
                    if not sv.solve():
                        done = True; break
                    m = sv.get_model(); on = tuple(i for i in range(len(cells)) if m[X[0][i] - 1] > 0)
                    mine.add(on); os_ = set(on)
                    sv.add_clause([(-X[0][i] if i in os_ else X[0][i]) for i in range(len(cells))])
            json.dump(dict(complete=done, bits=bits, sols=sorted(mine)), open(pf, 'w'))
            print(f'  part {j}/{2 ** K}: {len(mine)} solutions ({len(mine) - n0} new), {"COMPLETE (UNSAT)" if done else "not complete"}, {time.time() - t0:.0f} s', flush=True)
        alldone &= done; total |= mine
    print(f'{a.frame} C={a.C} tube [{a.lo},{a.hi}]: {len(cells)} region cells; split on cells {[cells[i] for i in split]}; {len(total)} solutions; '
          f'{"ALL PARTS COMPLETE" if alldone else "NOT complete: run again"} [{a.solver}]', flush=True)
    if alldone:
        json.dump(dict(frame=a.frame, C=a.C, lo=a.lo, hi=a.hi, T=4, KS=6, solver=a.solver, complete=True, split=[list(cells[i]) for i in split],
                       list=[[list(cells[i]) for i in s] for s in sorted(total)]), open(stem + '.json', 'w'))


if __name__ == '__main__':
    main()
