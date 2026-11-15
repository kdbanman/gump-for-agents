#!/usr/bin/env python3
"""Words of holes, exhaustively, with st.step (oracle-checked).
  python3 holes.py beam N          every subset of the rakes of beam(N) one generation after the stored phase
                                   (rake cell (1,0,4) removed from the chosen f units) - 2^R words;
  python3 holes.py line N T0       every subset of the mirror rakes on line(N) at odd generation T0 (cell
                                   hole_start of the chosen rakes removed);
  python3 holes.py divider N T0..T1  every subset of the rakes on the divider at each odd generation in T0..T1
                                   (upstream and downstream of the oscillator), hole_start cell removed;
  python3 holes.py divflip N T0 T1 every single live cell of units 0..N+2 outside the oscillator support removed,
                                   and every dead cell of units 1..N-1 inside the 3x3 tube added, at each
                                   generation T0..T1 (one-cell flips anywhere on the divider's wire and gun).
Outcome of a word: 'heal' = identical to the undisturbed orbit at the end (and for the last 16 generations);
otherwise the period of the end state and whether the oscillator (divider) and the gun survive."""
import sys, os, itertools, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import st


def classify(ref, x, t_start, extra, gz):
    """ref: undisturbed orbit list (long enough); x: disturbed state at t_start."""
    G = len(ref) - 1
    xs = [x]
    for t in range(t_start, G):
        xs.append(st.step(xs[-1]))
    # xs[i] is generation t_start + i
    if all(xs[-1 - i] == ref[G - i] for i in range(16)):
        first = next(i for i in range(len(xs)) if all(xs[j] == ref[t_start + j] for j in range(i, len(xs))))
        return ('heal', t_start + first)
    p = next((p for p in range(1, 41) if xs[-1] == xs[-1 - p]), None)
    g = gz(xs[-1]) == gz(ref[G]) and gz(xs[-2]) == gz(ref[G - 1])
    return ('changed', p, 'gun alive' if g else 'gun changed', extra(xs[-1]))


mode = sys.argv[1]; N = int(sys.argv[2])
cnt = collections.Counter(); bad = []
if mode == 'beam':
    G = 4 * N + 60
    ref = st.run(st.beam(N), G)
    rc = tuple(st.B['rake_cell'])
    rk = [k for k in range(N) if st.tr(rc, k) in ref[1]]
    print(f'beam N={N}: rakes at units {rk}')
    gz = lambda s: frozenset(c for c in s if st.U(c) <= 0)
    for r in range(len(rk) + 1):
        for sub in itertools.combinations(rk, r):
            x = ref[1] - frozenset(st.tr(rc, k) for k in sub)
            out = classify(ref, x, 1, lambda s: None, gz)
            key = (rk[0] in sub, out[0], out[2] if out[0] == 'changed' else '')
            cnt[key] += 1
            if out[0] != 'heal' and rk[0] not in sub:
                bad.append((sub, out))
elif mode in ('line', 'divider'):
    obj = st.line if mode == 'line' else st.divider
    hs = tuple(st.L['hole_start'])
    T0 = int(sys.argv[3]); T1 = int(sys.argv[4]) if len(sys.argv) > 4 else T0
    G = T1 + 2 * N + 80
    ref = st.run(obj(N), G)
    if mode == 'divider':
        fo = [st.trs(st.D['osc'], N)]
        for _ in range(7):
            fo.append(st.step(fo[-1]))
        sup = frozenset().union(*fo)
        extra = lambda s: 'osc kept' if frozenset(c for c in s if c in sup) in fo else 'osc changed'
    else:
        sup = frozenset(); extra = lambda s: None
    gz = lambda s: frozenset(c for c in s if c[0] >= 2 * N and c not in sup)
    for T in range(T0, T1 + 1, 2):
        rk = [k for k in range(0, N) if st.tr(hs, k) in ref[T]]
        for r in range(len(rk) + 1):
            for sub in itertools.combinations(rk, r):
                x = ref[T] - frozenset(st.tr(hs, k) for k in sub)
                out = classify(ref, x, T, extra, gz)
                near = max(rk) in sub
                key = (T, 'nearest-to-gun removed' if near else 'nearest kept', out[0]) + (out[1:] if out[0] == 'changed' else ())
                cnt[key] += 1
                if out[0] != 'heal' and not near:
                    bad.append((T, sub, out))
        print(f'{mode} N={N} T={T}: rakes (hole_start live) at units {rk}', flush=True)
elif mode == 'divflip':
    T0, T1 = int(sys.argv[3]), int(sys.argv[4])
    G = T1 + 2 * N + 80
    ref = st.run(st.divider(N), G)
    fo = [st.trs(st.D['osc'], N)]
    for _ in range(7):
        fo.append(st.step(fo[-1]))
    sup = frozenset().union(*fo)
    extra = lambda s: 'osc kept' if frozenset(c for c in s if c in sup) in fo else 'osc changed'
    gz = lambda s: frozenset(c for c in s if c[0] >= 2 * N and c not in sup)
    tube = [c for c in itertools.product(range(-2, 2 * N + 8), range(-1, 6), range(-2 * N - 8, 8))
            if sum(v & 1 for v in c) == 1 and 1 <= c[0] + c[1] + c[2] <= 5 and 1 <= c[0] - c[1] + c[2] <= 5]
    for T in range(T0, T1 + 1):
        flips = [c for c in ref[T] if c not in sup and 0 <= st.U(c) <= N + 2]
        flips += [c for c in tube if c not in ref[T] and 1 <= st.U(c) <= N - 1 and c not in sup]
        for c in flips:
            x = ref[T] ^ {c}
            out = classify(ref, x, T, extra, gz)
            key = (out[0],) + (out[1:] if out[0] == 'changed' else ())
            cnt[key] += 1
            if out[0] == 'changed' and out[3] == 'osc kept' and out[2] == 'gun alive':
                bad.append((T, c, out))
        print(f'divflip N={N} T={T}: {len(flips)} flips', flush=True)
for k, v in sorted(cnt.items(), key=str):
    print(v, k)
print('words that do not heal although the rake nearest the gun is kept' if mode != 'divflip' else 'flips leaving osc and gun alive in a changed state', len(bad))
for b in bad[:30]:
    print('  ', b)
