#!/usr/bin/env python3
"""Every object of research/atlas/catalogue.jsonl certified by Lean's kernel as an oscillator of exactly its period.

    python3 research/blast/lean/census_check.py OUTDIR [--limit N]

For each object (cells = phase 0, period P) this writes, in chunks of 100 to OUTDIR/Census_k.lean,

    def L_<id> : List Gump.Pt := [cells]
    theorem cat_<id> : 0 < P ∧ run (lcfg L_<id>) P = lcfg L_<id> ∧
        ∀ k, 0 < k → k < P → run (lcfg L_<id>) k ≠ lcfg L_<id> :=
      Gump.Bits.oscCert_spec L_<id> P (by decide +kernel)

and checks each chunk with `lake env lean` (the kernel evaluates the bit-parallel orbit, `Gump.Bits.bstep`, proved
equal to `Gump.step` by `Gump.Bits.bstep_spec`), then prints the axioms of the first and last theorem of each chunk.
A chunk that fails is re-checked object by object to name the objects that fail. Bulk files go to OUTDIR
(use research/scratch/blast/lean/census, which git ignores).
"""
import json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')


def lean_name(i):
    return re.sub(r'[^A-Za-z0-9_]', '_', i)


def theorem(r):
    n = lean_name(r['id'])
    pts = ', '.join(f'⟨{x}, {y}, {z}⟩' for x, y, z in r['cells'])
    P = r['period']
    return (f"def L_{n} : List Pt := [{pts}]\n"
            f"theorem cat_{n} : 0 < {P} ∧ run (lcfg L_{n}) {P} = lcfg L_{n} ∧\n"
            f"    ∀ k, 0 < k → k < {P} → run (lcfg L_{n}) k ≠ lcfg L_{n} :=\n"
            f"  Gump.Bits.oscCert_spec L_{n} {P} (by decide +kernel)\n")


def check(path):
    t = time.time()
    r = subprocess.run(['lake', 'env', 'lean', path], capture_output=True, text=True, cwd=HERE)
    return r.returncode == 0 and 'error' not in r.stdout, r.stdout + r.stderr, time.time() - t


def write(path, rows, axioms):
    with open(path, 'w') as f:
        f.write('import Gump.Bits\nopen Gump\n\n')
        for r in rows:
            f.write(theorem(r) + '\n')
        for r in axioms:
            f.write(f'#print axioms cat_{lean_name(r["id"])}\n')


def main():
    out = sys.argv[1]
    lim = int(sys.argv[sys.argv.index('--limit') + 1]) if '--limit' in sys.argv else None
    os.makedirs(out, exist_ok=True)
    rows = [json.loads(l) for l in open(os.path.join(ROOT, 'research', 'atlas', 'catalogue.jsonl'))]
    if lim:
        rows = rows[:lim]
    t0 = time.time()
    ok_n, bad, axioms = 0, [], set()
    for c in range(0, len(rows), 100):
        chunk = rows[c:c + 100]
        path = os.path.join(out, f'Census_{c // 100}.lean')
        write(path, chunk, [chunk[0], chunk[-1]])
        ok, txt, dt = check(path)
        axioms |= set(re.findall(r"depends on axioms: \[([^\]]*)\]", txt))
        if ok:
            ok_n += len(chunk)
        else:
            for r in chunk:
                p1 = os.path.join(out, 'one.lean')
                write(p1, [r], [])
                if check(p1)[0]:
                    ok_n += 1
                else:
                    bad.append(r['id'])
        print(f'chunk {c // 100}: objects {c}..{c + len(chunk) - 1}, {"ok" if ok else "FAILED"}, {dt:.0f}s', flush=True)
    periods = {}
    for r in rows:
        periods[r['period']] = periods.get(r['period'], 0) + 1
    print(f'census: {ok_n} of {len(rows)} catalogued objects certified by the kernel as oscillators of exactly their '
          f'listed period (periods: {dict(sorted(periods.items()))}); failed: {bad}; axioms seen: {sorted(axioms)}; '
          f'{time.time() - t0:.0f}s')
    sys.exit(0 if not bad and ok_n == len(rows) else 1)


if __name__ == '__main__':
    main()
