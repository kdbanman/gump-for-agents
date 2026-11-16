"""Objects used by REVIEW-signals-4 that oracle_check.py compares st.step against the oracle on."""
import st


def remove(s, cells):
    return frozenset(s) - frozenset(cells)


def controls():
    out = [('line N=9', st.line(9), 40), ('beam N=9', st.beam(9), 24), ('beam N=10', st.beam(10), 24),
           ('divider N=12', st.divider(12), 50), ('divider N=13', st.divider(13), 52)]
    # beam N=10 with two adjacent holes one generation after the stored phase
    x1 = st.step(st.beam(10))
    rk = [k for k in range(10) if st.tr(tuple(st.B['rake_cell']), k) in x1]
    out.append(('beam N=10, holes at two rakes', remove(x1, [st.tr(tuple(st.B['rake_cell']), k) for k in rk[1:3]]), 40))
    # divider N=12 with two oscillators (second one 4 units further from the gun)
    out.append(('divider N=14, two oscillators', st.divider(14) | st.trs(st.D['osc'], 10), 50))
    return out
