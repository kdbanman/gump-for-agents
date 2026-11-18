"""Audit of push 8b: push 7's line with E and n holes, from the cells in the push's JSON (line0 and the flips of the
cases of objects/read-echo-B-line.json; for n > 4 the holes continue 6 units apart, as the push's README section 1).
q.c stepper (checked against the oracle on this line by check_q.py)."""
import functools
import qa
from qa import pk, up, run, xor, tr

_ob = qa.obj('read-echo-B-line')
LINE0 = pk([tuple(c) for c in _ob['line0']])
E_CELLS = [(65, 2, -62), (66, 0, -63), (66, 0, -61)]
H0 = (99, 2, -96)
assert [tuple(c) for c in _ob['cases'][3]['store']['flips'][0][1]] == E_CELLS + [tr(H0, 6 * j) for j in range(4)]


@functools.lru_cache(None)
def standing(n, gen=900):
    k = run(LINE0, 1)
    k = xor(k, pk(E_CELLS + [tr(H0, 6 * j) for j in range(n)]))
    return run(k, gen - 1)


if __name__ == '__main__':
    import rd
    for n in range(0, 10):
        k = standing(n)
        print(f'n={n}: {len(k)} cells at generation 900, period {rd.period(k)}; units 30..60: {qa.letters(k, 30, 60)}  0..90: {qa.letters(k, 0, 90)}')
