"""Claim 3 (README section 17): the 8|C wall counts pulses p<.  reference/oracle.py on the box torus (2L, 16, 2L)
of a ring of L units (wirec.Ring of the second review: every generation checked to stay in the 3 x 3 tube modulo
the box, which makes the box run the ring exactly).  No study code.

    python3 counter_check.py           (about 2 min)

Ring: wire 8 on units 0..w-1, wire C on w..L-1 (so walls 8|C at w and C|8 at L|0); words of B units placed in the
C part (a B unit in wire C is a p<).  For each case: the kymograph row every 2 generations is reduced to the wall
position (the first unit >= 1 that is not '8'), and the final state is compared cell for cell with the ring with
the wall moved by the number of pulses.
"""
import sys
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__file__), '..', 'signals2'))
import wirec
import r3
from r3 import uc

L = 64


def ring(w, Bs=(), wireright='C', extra8=()):
    s = set()
    for u in range(L):
        s |= uc(0x8 if (u < w or u in extra8) else ('B' if u in Bs else 0xb), u)
    return s


def run_case(R, label, w, Bs, T, expect=None, show=False):
    st = R.key(ring(w, Bs))
    try:
        out = R.run(st, T, every=2)
    except AssertionError as e:
        print(f'{label}: {e}'); return
    rows = {t: R.hexrow(S) for t, S in out.items()}
    walls = []
    for t in sorted(rows):
        r = rows[t]; i = 0
        while i < L and r[i] == '8':
            i += 1
        walls.append(i)
    n = len(Bs) if expect is None else expect
    final = out[T] == R.key(ring(w + n))
    print(f'{label}: wall {walls[0]} -> {walls[-1]} (moves at t = {[t for t, a, b in zip(sorted(rows)[1:], walls, walls[1:]) if a != b]}); '
          f'final = ring with wall at {w + n}: {final}', flush=True)
    if show or not final:
        for t in sorted(rows)[:: max(1, len(rows) // 25)]:
            print('   %4d %s' % (t, rows[t]))


def main():
    R = wirec.Ring(L)
    T = 2 * L + 8
    print('wire 8 alone on the ring stationary (2 generations):', R.run(R.key(ring(L)), 2)[2] == R.key(ring(L)))
    print('the ring with both walls, no pulse, 40 generations:', R.run(R.key(ring(16)), 40)[40] == R.key(ring(16)))
    w = 8
    for sp in (2, 3, 4, 7):
        run_case(R, f'spacing {sp}, 12 pulses', w, [30 + sp * i for i in range(12)], T)
    run_case(R, 'irregular 2,3,2,5,2,2,4,3,2,6 (11 pulses)', w, [20, 22, 25, 27, 32, 34, 36, 40, 43, 45, 51], T)
    run_case(R, '20 pulses spacing 2 (word (BC)^20)', w, [14 + 2 * i for i in range(20)], T)
    run_case(R, 'spacing 1: BB', w, [30, 31], T, show=True)
    run_case(R, 'spacing 1: BBB', w, [30, 31, 32], T, show=True)
    run_case(R, 'one pulse right at the wall (unit w)', w, [w], T)
    run_case(R, 'one pulse at unit w+1', w, [w + 1], T)
    # the wall reaches the far end: almost all of wire C used up
    run_case(R, 'wall pushed to the far wall: (BC) on units 10..62', w, list(range(10, 63, 2)), T, show=True)


if __name__ == '__main__':
    main()
