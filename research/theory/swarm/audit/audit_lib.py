"""Auditor's own tools for AUDIT-theoremA.md.  Written from the statements audited, not from any other
agent's code.  Rows of a ring Z_L are integers: bit y = cell y.

Conventions
  2D rule B34/S234: a cell with state x and n live neighbours is alive next iff (x=0, n in {3,4}) or
  (x=1, n in {2,3,4}).  Neighbourhood ("cross"): (+-1,0), (+-2,0), (0,+-1), (0,+-2).
  Edge row = row 0; rows -1, -2 are dead for ever; rows 1, 2 lie beneath.
  k = live cells among the four in-row neighbours y+-1, y+-2;  b = live cells among (y,1), (y,2).
"""
import itertools
import numpy as np


def rule2d(x, n):
    """B34/S234, from the birth and survival lists (not from the threshold form)."""
    return 1 if ((x == 0 and n in (3, 4)) or (x == 1 and n in (2, 3, 4))) else 0


def bit(S, y, L):
    return (S >> (y % L)) & 1


def kcount(S, y, L):
    return bit(S, y - 2, L) + bit(S, y - 1, L) + bit(S, y + 1, L) + bit(S, y + 2, L)


def step_row(S, b, L):
    """One generation of the edge row S over the drive b (sequence of b_y in {0,1,2})."""
    out = 0
    for y in range(L):
        if rule2d(bit(S, y, L), kcount(S, y, L) + b[y]):
            out |= 1 << y
    return out


def alive_prob_table(pi):
    """a[x][k] = P(alive next | x, k) when b has law pi = (pi0, pi1, pi2); derived from rule2d."""
    return [[sum(pi[b] for b in range(3) if rule2d(x, k + b)) for k in range(5)] for x in range(2)]


def local_kernel_E1(pi):
    """q[w] for window w = (x_{y-2}, x_{y-1}, x_y, x_{y+1}, x_{y+2}) -> P(y alive next)."""
    a = alive_prob_table(pi)
    q = np.zeros((2,) * 5)
    for w in itertools.product((0, 1), repeat=5):
        q[w] = a[w[2]][w[0] + w[1] + w[3] + w[4]]
    return q


def local_kernel_OP5(p):
    """Five-parent oriented site percolation: alive next w.p. p iff some cell of the window is alive."""
    q = np.zeros((2,) * 5)
    for w in itertools.product((0, 1), repeat=5):
        q[w] = p if any(w) else 0.0
    return q


def local_kernel_OP2(p):
    """Two-parent oriented site percolation on a ring: (i,t+1) open w.p. p iff i or i+1 occupied at t."""
    q = np.zeros((2,) * 5)
    for w in itertools.product((0, 1), repeat=5):
        q[w] = p if (w[2] or w[3]) else 0.0
    return q


def dense_kernel(L, q):
    """Full 2^L x 2^L transition matrix on subsets of Z_L (L >= 5), cells independent given S."""
    N = 1 << L
    Q = np.ones((N, N))
    Sp = np.arange(N)
    for S in range(N):
        row = np.ones(N)
        for y in range(L):
            w = tuple(bit(S, y + d, L) for d in (-2, -1, 0, 1, 2))
            a = q[w]
            row *= np.where((Sp >> y) & 1, a, 1.0 - a)
        Q[S] = row
    return Q


def apply_kernel(f, L, q):
    """(Qf)(S) = sum_{S'} prod_y q_y(S'_y | S) f(S'), by summing out one cell of S' at a time.
    f: array of length 2^L indexed by S' (bit y = cell y).  Memory 2^(L+4) doubles.  L >= 5."""
    # tensor with axis label y for S'_y ("t-axes", labels 0..L-1) and L+y for S_y ("s-axes")
    g = np.asarray(f, dtype=float).reshape((2,) * L)
    # reshape of an index S' = sum bit_y 2^y in C order puts bit L-1 first: axes are (L-1, ..., 0)
    labels = list(range(L - 1, -1, -1))
    qq = np.stack([1.0 - q, q])          # qq[t, w0..w4]
    for y in range(L):
        win = [L + ((y + d) % L) for d in (-2, -1, 0, 1, 2)]
        out = [l for l in labels if l != y]
        for l in win:
            if l not in out:
                out.append(l)
        g = np.einsum(g, labels, qq, [y] + win, out)
        labels = out
    # now labels are a permutation of the s-axes L..2L-1; bring to order (2L-1, ..., L) and flatten
    order = [labels.index(L + y) for y in range(L - 1, -1, -1)]
    return np.transpose(g, order).reshape(-1)


def perron(L, q, tol=1e-13, maxit=20000, verbose=False):
    """Largest eigenvalue of the kernel restricted to non-empty states, by power iteration from 1.
    Returns (lam_lo, lam_hi, v, iterations): Collatz-Wielandt bounds min/max of (Qv)/v over states with
    v > 0 (valid for an irreducible non-negative matrix and a positive vector)."""
    N = 1 << L
    v = np.ones(N)
    v[0] = 0.0
    lo = hi = None
    for it in range(1, maxit + 1):
        w = apply_kernel(v, L, q)
        w[0] = 0.0
        r = w[1:] / v[1:]
        lo, hi = r.min(), r.max()
        v = w / w[1:].max()
        if verbose and it % 20 == 0:
            print(it, lo, hi, hi - lo, flush=True)
        if hi - lo < tol * hi:
            break
    return lo, hi, v, it


def survival_curve(L, q, start, tmax):
    """P_start(T > t), t = 0..tmax, exactly (floating point), by iterating the kernel on indicator of alive."""
    N = 1 << L
    v = np.ones(N)
    v[0] = 0.0
    out = [v[start]]
    for _ in range(tmax):
        v = apply_kernel(v, L, q)
        v[0] = 0.0
        out.append(v[start])
    return np.array(out)
