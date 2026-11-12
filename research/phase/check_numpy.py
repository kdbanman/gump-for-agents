"""Check gl.step against the engine on tori: snapshot in -> engine k gens -> compare.
usage: python3 check_numpy.py [GUMP_BINARY]"""
import subprocess, sys, os, tempfile
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import gl

G = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '../../engine/target/release/gump')
tmp = tempfile.mkdtemp()
rng = np.random.default_rng(5)
ok = True
for (n, rule, p) in [(8, 'B45/S345', 0.3), (12, 'B45/S345', 0.45), (10, 'B4/S2345', 0.3), (9, 'B3/S23', 0.2), (14, 'B567/S3456', 0.5)]:
    V = gl.soup(n, p, rng)
    a = os.path.join(tmp, 'a.gump'); b = os.path.join(tmp, 'b.gump')
    gl.write_snapshot(a, V, rule=rule)
    subprocess.run([G, 'run', '--snapshot', a, '--torus', str(n), '--rule', rule, '--gens', '7',
                    '--no-halt', '--snapshot-out', b], check=True, capture_output=True)
    W, _ = gl.read_snapshot(b)
    tab = gl.make_table(rule)
    for _ in range(7):
        V = gl.step(V, tab)
    same = np.array_equal(V, W)
    ok &= same
    print(n, rule, p, 'pop', int(V.sum()), 'match' if same else 'MISMATCH')
print('ALL OK' if ok else 'FAIL')
