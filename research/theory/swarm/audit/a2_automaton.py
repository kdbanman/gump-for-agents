"""A2.  The deterministic automaton A(L) run as a deterministic map, exhaustively over its initial
conditions, against the dice chain E1(1/2,0,1/2).

(a) A(L) proper: cells (x,j), x in Z_L, j = 0..H.  Row 0: B34/S234 on the cross (rows above dead).
    Row j >= 1: y'(x,j) = y(x,j+2) (rows beyond H read as 0).  Start: row 0 = S0; bits xi[x,i] written into
    rows 2i-1 and 2i.  With H = 2t the first t generations are exact.  For EVERY S0 and EVERY xi in
    {0,1}^(L*t) the map is run on the full array; checked: rows 1 and 2 at time s both equal xi[.,s+1];
    the number of xi giving each trajectory (S1..St) equals 2^(L*t) * prod Q(S_{i-1},S_i), Q built from the
    table a(x,k) at pi = (1/2,0,1/2).  (All numbers dyadic: the comparison is exact.)

(b) The variant from the uniform product measure: rows 1 and 2 copy row 3; rows >= 3 follow parity on the
    cross (alive next iff an odd number of the 8 cross neighbours is alive; they read rows 1, 2 too).
    Start: rows 0..2 fixed (several choices), rows 3..H all configurations.  Checked: the sequence
    (row 3 at times 0..t-1) takes each of its 2^(L*t) values equally often (so it is i.i.d. uniform and
    independent of the top rows), and rows 1, 2 at time s+1 equal row 3 at time s.

(c) Source Lemma 1 (S2) in its smallest two-dimensional instance, R_1(parity) for the 2D rule: row 0 by
    the rule, rows >= 1 by parity on the cross (two-way coupling: rows 1, 2 read row 0), start uniform on
    rows >= 1.  Checked: for every S0 the map (rows 1..2t at time 0) -> ((rows 1,2) at times 0..t-1) is a
    bijection, so the drive is fresh uniform dice whatever the edge does.

Run:  python3 a2_automaton.py        (about 2 minutes, < 2 GB)
"""
import sys
import numpy as np
from audit_lib import rule2d, dense_kernel, local_kernel_E1

ok = True


# ---------- generic array stepper (one array per initial condition; states uint8, shape (N, H+1, L)) ----------
def step_A(c):
    N, R, L = c.shape
    new = np.zeros_like(c)
    r0 = c[:, 0, :]
    n = (np.roll(r0, 1, 1) + np.roll(r0, -1, 1) + np.roll(r0, 2, 1) + np.roll(r0, -2, 1)
         + c[:, 1, :] + c[:, 2, :])
    alive = np.where(r0 == 1, (n >= 2) & (n <= 4), (n >= 3) & (n <= 4))
    assert all(rule2d(x, m) == int((m >= 2 and m <= 4) if x else (m >= 3 and m <= 4)) for x in (0, 1) for m in range(9))
    new[:, 0, :] = alive
    new[:, 1:R - 2, :] = c[:, 3:R, :]          # row j <- row j+2 ; the two bottom rows read 0
    return new


def rows_to_int(a):
    L = a.shape[-1]
    return (a.astype(np.int64) * (1 << np.arange(L))).sum(-1)


def part_a(L, t):
    global ok
    H = 2 * t
    nb = L * t
    N = 1 << nb
    idx = np.arange(N, dtype=np.int64)
    xi = ((idx[:, None] >> np.arange(nb)) & 1).astype(np.uint8).reshape(N, t, L)   # xi[:, i-1, x]
    Q = dense_kernel(L, local_kernel_E1((0.5, 0.0, 0.5)))
    worst = 0.0
    pair_ok = True
    for S0 in range(1 << L):
        c = np.zeros((N, H + 1, L), dtype=np.uint8)
        c[:, 0, :] = (S0 >> np.arange(L)) & 1
        for i in range(1, t + 1):
            c[:, 2 * i - 1, :] = xi[:, i - 1, :]
            c[:, 2 * i, :] = xi[:, i - 1, :]
        traj = np.zeros(N, dtype=np.int64)
        for s in range(t):
            pair_ok &= bool((c[:, 1, :] == xi[:, s, :]).all() and (c[:, 2, :] == xi[:, s, :]).all())
            c = step_A(c)
            traj = traj * (1 << L) + rows_to_int(c[:, 0, :])
        vals, counts = np.unique(traj, return_counts=True)
        # chain probability of each observed trajectory, and total mass of observed trajectories
        tot = 0.0
        for v, cnt in zip(vals, counts):
            seq = [(v >> (L * (t - 1 - s))) & ((1 << L) - 1) for s in range(t)]
            p, prev = 1.0, S0
            for S in seq:
                p *= Q[prev, S]
                prev = S
            worst = max(worst, abs(p - cnt / N))
            tot += p
        worst = max(worst, abs(tot - 1.0))
    ok &= pair_ok and worst == 0.0
    print("(a) L=%d, t=%d: all %d row-0 starts x %d bit tables; rows 1,2 = xi[.,s+1]: %s; "
          "max |count/2^(Lt) - chain probability| = %g" % (L, t, 1 << L, N, pair_ok, worst))


# ---------- packed steppers for (b), (c): each row an integer array, bit x = cell x ----------
def rot(r, d, L):
    d %= L
    m = (1 << L) - 1
    return ((r << d) | (r >> (L - d))) & m if d else r


def inrow_parity(r, L):
    return rot(r, 1, L) ^ rot(r, -1, L) ^ rot(r, 2, L) ^ rot(r, -2, L)


def edge_table(L):
    """T[S, r1, r2] = next row 0, from rule2d; in-row neighbours counted with multiplicity (L < 5 allowed)."""
    n = 1 << L
    T = np.zeros((n, n, n), dtype=np.uint8)
    for S in range(n):
        for r1 in range(n):
            for r2 in range(n):
                out = 0
                for x in range(L):
                    k = sum((S >> ((x + d) % L)) & 1 for d in (-2, -1, 1, 2))
                    b = ((r1 >> x) & 1) + ((r2 >> x) & 1)
                    if rule2d((S >> x) & 1, k + b):
                        out |= 1 << x
                T[S, r1, r2] = out
    return T


def enumerate_rows(L, nrows):
    """All configurations of nrows rows: list of nrows uint8 arrays of length 2^(L*nrows)."""
    N = 1 << (L * nrows)
    idx = np.arange(N, dtype=np.int64)
    m = (1 << L) - 1
    return [((idx >> (L * i)) & m).astype(np.uint8) for i in range(nrows)]


def part_b(L, t, tops):
    """Variant: rows 1,2 copy row 3; rows >= 3 parity on the cross.  rows 3..H enumerated, H = 3 + 2(t-1)."""
    global ok
    H = 3 + 2 * (t - 1)
    src = enumerate_rows(L, H - 2)
    N = len(src[0])
    T = edge_table(L)
    zero = np.zeros(N, dtype=np.uint8)
    for (S0, r1, r2) in tops:
        rows = [np.full(N, S0, np.uint8), np.full(N, r1, np.uint8), np.full(N, r2, np.uint8)] + [a.copy() for a in src]
        key = np.zeros(N, dtype=np.int64)
        copy_ok = True
        for s in range(t):
            key = key * (1 << L) + rows[3]
            get = lambda j: rows[j] if 0 <= j <= H else zero
            new = [T[rows[0], rows[1], rows[2]], rows[3].copy(), rows[3].copy()]
            for j in range(3, H + 1):
                new.append(inrow_parity(rows[j], L) ^ get(j - 1) ^ get(j - 2) ^ get(j + 1) ^ get(j + 2))
            r3_old = rows[3]
            rows = new
            copy_ok &= bool((rows[1] == r3_old).all() and (rows[2] == r3_old).all())
        counts = np.bincount(key, minlength=1 << (L * t))
        uni = bool((counts == N >> (L * t)).all())
        ok &= uni and copy_ok
        print("(b) L=%d, t=%d, top rows (S0,r1,r2)=(%d,%d,%d): (row 3 at times 0..%d) uniform over 2^%d values: %s"
              " (each %d times); rows 1,2 at s+1 = row 3 at s: %s" % (L, t, S0, r1, r2, t - 1, L * t, uni, N >> (L * t), copy_ok))


def part_c(L, t):
    """R_1(parity): row 0 by the rule; rows 1..H parity on the cross, reading row 0 (rows < 0 dead).  H = 2t."""
    global ok
    H = 2 * t
    src = enumerate_rows(L, H)
    N = len(src[0])
    T = edge_table(L)
    zero = np.zeros(N, dtype=np.uint8)
    allbij = True
    for S0 in range(1 << L):
        rows = [np.full(N, S0, np.uint8)] + [a.copy() for a in src]
        key = np.zeros(N, dtype=np.int64)
        for s in range(t):
            key = (key * (1 << L) + rows[1]) * (1 << L) + rows[2]
            get = lambda j: rows[j] if 0 <= j <= H else zero
            new = [T[rows[0], rows[1], rows[2]]]
            for j in range(1, H + 1):
                new.append(inrow_parity(rows[j], L) ^ get(j - 1) ^ get(j - 2) ^ get(j + 1) ^ get(j + 2))
            rows = new
        counts = np.bincount(key, minlength=N)
        allbij &= bool((counts == 1).all())
    ok &= allbij
    print("(c) L=%d, t=%d: for every S0 the map (rows 1..%d at time 0) -> (rows 1,2 at times 0..%d) is a bijection of 2^%d: %s"
          % (L, t, H, t - 1, L * H, allbij))


if __name__ == "__main__":
    part_a(5, 3)
    part_a(6, 2)
    part_a(6, 3)
    part_a(8, 2)
    part_b(5, 2, [(0b00101, 0, 0), (0b11111, 0b01010, 0b10001), (0b01110, 0b11111, 0b00011)])
    part_b(5, 3, [(0b00101, 0, 0), (0b11011, 0b10110, 0b01001)])
    part_c(5, 2)
    part_c(3, 4)
    part_c(4, 3)
    print("A2 ALL OK" if ok else "A2 FAILED")
