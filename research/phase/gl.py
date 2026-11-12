"""Small numpy toolkit for the bulk-phase study (research/phase/).

State = bool array V[a, i, j, k] (a = face normal axis 0..2, cube index i,j,k), periodic
(torus) unless noted.  V[a,i,j,k] is the face 2(i,j,k)+e_a in doubled coordinates.
Neighbourhood (docs/AUTOMATON.md §2), written once for all a with (a,b,c) cyclic:
    A[i ± e_b ± e_c]                      (4 coplanar, corner-sharing)
    B[0], B[-e_b], B[+e_a], B[e_a - e_b]  (4 perpendicular, normal b)
    C[0], C[-e_c], C[+e_a], C[e_a - e_c]  (4 perpendicular, normal c)
Validated bit-for-bit against engine/ on tori by check_numpy.py.
"""
import numpy as np

E = np.eye(3, dtype=int)


def sh(A, d):
    """A[x + d] (periodic)."""
    return np.roll(A, tuple(-int(x) for x in d), axis=(0, 1, 2))


def counts(V):
    """Live-neighbour count of every cell, int8 array like V."""
    V8 = V.astype(np.int8)
    N = np.zeros(V.shape, np.int8)
    for a in range(3):
        b, c = (a + 1) % 3, (a + 2) % 3
        A, B, C = V8[a], V8[b], V8[c]
        n = np.zeros(A.shape, np.int8)
        for sb in (1, -1):
            for sc in (1, -1):
                n += sh(A, sb * E[b] + sc * E[c])
        n += B + sh(B, -E[b]) + sh(B, E[a]) + sh(B, E[a] - E[b])
        n += C + sh(C, -E[c]) + sh(C, E[a]) + sh(C, E[a] - E[c])
        N[a] = n
    return N


def parse_rule(rule):
    b, s = rule.upper().split('/')
    def bits(t):
        t = t[1:]
        if ',' in t:
            return {int(x) for x in t.split(',') if x}
        return {int(ch) for ch in t}
    return bits(b), bits(s)


def make_table(rule):
    B, S = parse_rule(rule)
    tb = np.zeros(13, bool); ts = np.zeros(13, bool)
    tb[list(B)] = True; ts[list(S)] = True
    return tb, ts


def step(V, table=None, N=None):
    if table is None:
        table = make_table('B45/S345')
    tb, ts = table
    if N is None:
        N = counts(V)
    return np.where(V, ts[N], tb[N])


# ---------------------------------------------------------------- snapshots
def read_snapshot(path):
    raw = open(path, 'rb').read()
    head, payload = raw.split(b'\n\n', 1)
    meta = {}
    for line in head.decode().splitlines()[1:]:
        k, *v = line.split()
        meta[k] = v
    NX, NY, NZ = map(int, meta['dims'])
    nbytes = int(meta['bytes'][0])
    payload = payload[:nbytes]
    total = (3 * NX * NY * NZ + 7) // 8
    if meta['encoding'][0] == 'raw':
        buf = np.frombuffer(payload, np.uint8)
    else:
        out = bytearray(); p = 0
        def varint():
            nonlocal p
            v = 0; s = 0
            while True:
                b = payload[p]; p += 1
                v |= (b & 0x7f) << s; s += 7
                if b < 0x80:
                    return v
        while len(out) < total:
            z = varint(); out += bytes(z)
            if len(out) >= total:
                break
            L = varint(); out += payload[p:p + L]; p += L
        buf = np.frombuffer(bytes(out[:total]), np.uint8)
    bits = np.unpackbits(buf, bitorder='little')[:3 * NX * NY * NZ]
    V = bits.reshape(3, NZ, NY, NX).transpose(0, 3, 2, 1).astype(bool)
    if meta['boundary'][0] == 'torus':   # re-index by absolute cube coordinate mod dims
        V = np.roll(V, tuple(int(o) for o in meta['origin']), axis=(1, 2, 3))
    return V, meta


def write_snapshot(path, V, boundary='torus', origin=(0, 0, 0), rule='B45/S345', gen=0):
    _, NX, NY, NZ = V.shape
    bits = V.transpose(0, 3, 2, 1).reshape(-1).astype(np.uint8)
    buf = np.packbits(bits, bitorder='little').tobytes()
    hdr = (f"GUMP-SNAPSHOT 1\nboundary {boundary}\ndims {NX} {NY} {NZ}\n"
           f"origin {origin[0]} {origin[1]} {origin[2]}\nrule {rule}\ngen {gen}\n"
           f"population {int(V.sum())}\nencoding raw\nbytes {len(buf)}\n\n")
    open(path, 'wb').write(hdr.encode() + buf)


def soup(n, p, rng):
    return rng.random((3, n, n, n)) < p
