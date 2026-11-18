#!/usr/bin/env python3
"""ext1.py (audit of push 8b, q.c): the echo read on push 7's line, beyond what the push ran.

    python3 ext1.py phases       n = 1..6, readers B13 and B8 at unit 42: the pair launched at every generation 0..7
                                 after the reader is installed, from three own units, and from both ends
    python3 ext1.py probes       single pulse, pairs 1..12 units apart, triples, from both ends (n = 1, 3)
    python3 ext1.py repeat       60 reads in a row, 56 generations apart; and a second pair 2..60 generations after the first
    python3 ext1.py units        the reader at every unit 30..56 of the lines n = 1..6: does it stand, what does it read

A launch at an odd generation uses the pulse as it is one generation after an even-generation launch (measured on
the reader alone), so that every launch is the same free signal.  Outcome codes for a probe:
  restored@t   probed run = unprobed run from generation t after the launch (so for ever); the store's tube never differed
  STORE        a cell of the store's tube differed at some generation
  CHANGED      not restored within 400 generations
and what is travelling 30 generations after the launch, in the reader's own frame."""
import sys
import qa, rd, lines
from qa import pk, up, run, xor, union, same

OWN = rd.capped(-14, 14)
OWNK = pk(OWN)


def odd_form(cells):
    """the difference one generation after flipping `cells` on the reader alone (own frame)."""
    return up(xor(run(xor(OWNK, pk(cells)), 1), run(OWNK, 1)))


def launch(P, J, cells, t0, T=400):
    """probe `cells` (own frame, even-generation form) launched t0 generations after J.  Returns (code, travelling)."""
    if (t0 + P.phase) % 2 == 0:
        fl = {t0: pk(P(cells))}
    else:
        fl = {t0: pk(P(odd_form(cells)))}        # launched one generation earlier in its even form
        # odd_form is the state at an odd own generation: flip it at t0
    r = rd.lock(J, fl, t0 + T)
    trav = rd.describe(P, r['diffs'].get(t0 + 30, pk([])))
    if r['tube']:
        return 'STORE', trav
    if r['first'] is None:
        return 'CHANGED', trav
    return f"restored@{r['first'] - t0}", trav


READERS = {'B13': (rd.B13, -1), 'B8': (rd.B8, 0)}


def joint(n, name, U=42):
    mk, ur = READERS[name]
    P = mk(U)
    v, J, R = rd.install(lines.standing(n), P, OWN)
    return P, ur, v, J


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'phases':
        for name in READERS:
            for n in range(1, 7):
                P, ur, v, J = joint(n, name)
                print(f'{name} at unit 42, n={n}: install {v}')
                for side in 'LR':
                    res = {}
                    for d in (7, 9, 10):
                        for t0 in range(8):
                            cells = rd.pR(ur - d) + rd.pR(ur - d - 1) if side == 'L' else rd.pL(ur + d) + rd.pL(ur + d + 1)
                            code, trav = launch(P, J, cells, t0)
                            # the travelling difference is named only at even own generations
                            key = (code.split('@')[0], trav.split('@')[0] if t0 % 2 == 0 else '(odd launch) ' + trav.split(',')[0])
                            res[key] = res.get(key, 0) + 1
                    print(f'   pair from the {"left" if side == "L" else "right"} end, 3 distances x 8 launch generations: ' + '; '.join(f'{v} x {k[0]} [{k[1]}]' for k, v in sorted(res.items())))
    elif cmd == 'probes':
        for name in READERS:
            for n in (1, 3):
                P, ur, v, J = joint(n, name)
                print(f'{name} at unit 42, n={n}: install {v}')
                for side in 'LR':
                    mk = (lambda j: rd.pR(ur - 9 - j)) if side == 'L' else (lambda j: rd.pL(ur + 9 + j))
                    words = {'single': [0]}
                    for s in range(1, 13):
                        words[f'pair {s} apart'] = [0, s]
                    for a in range(1, 5):
                        for b in range(1, 5):
                            words[f'triple {a},{b}'] = [0, a, a + b]
                    words['four adjacent'] = [0, 1, 2, 3]
                    words['five adjacent'] = [0, 1, 2, 3, 4]
                    for w, offs in words.items():
                        cells = set()
                        for j in offs:
                            cells ^= set(mk(j))
                        code, trav = launch(P, J, sorted(cells), 0)
                        print(f'   {side} {w:16s} {code:13s} travelling at 30: {trav}')
    elif cmd == 'repeat':
        for name in READERS:
            mk, ur = READERS[name]
            for n in (1, 2, 6):
                P, ur, v, J = joint(n, name)
                pair = pk(P(rd.pR(ur - 9) + rd.pR(ur - 10)))
                X = Y = J; outs = []
                for i in range(60):
                    X = xor(X, pair)
                    X30 = run(X, 30); Y30 = run(Y, 30)
                    outs.append(rd.describe(P, xor(X30, Y30)))
                    X = run(X30, 26); Y = run(Y30, 26)
                print(f'{name} n={n}: 60 reads 56 generations apart: outputs {sorted(set(outs))}; state after the last = unprobed: {same(run(X, 60), run(Y, 60))}')
                row = '   second pair dt after the first: '
                for dt in range(2, 62, 2):
                    r = rd.lock(J, {0: pair, dt: pair}, dt + 300)
                    ok = r['first'] is not None and not r['tube']
                    row += f" {dt}:{'ok' if ok else 'BAD'}[{rd.describe(P, r['diffs'].get(dt + 30, pk([])))}]"
                print(row)
    elif cmd == 'units':
        for name in READERS:
            mk, ur = READERS[name]
            print(f'{name}: one character per crossing unit 30..56.  install: u union, j junction, X burn or store changed, o overlap;'
                  ' read: e echo (one L pulse back, restored, tube untouched), 0 nothing travelling (restored, tube untouched), ! other')
            for n in range(1, 7):
                S = lines.standing(n)
                a = b = ''
                for U in range(30, 57):
                    P = mk(U)
                    v, J, R = rd.install(S, P, OWN, settle=160)
                    if J is None or v == 'store':
                        a += 'o' if v == 'overlap' else 'X'; b += ' '; continue
                    a += v[0]
                    code, trav = launch(P, J, rd.pR(ur - 9) + rd.pR(ur - 10), 0)
                    b += 'e' if code.startswith('restored') and trav.startswith('L@') and ' ' not in trav else '0' if code.startswith('restored') and trav == '-' else '!'
                print(f'  n={n}  line    {qa.letters(S, 30, 57)}\n       install {a}\n       read    {b}')
