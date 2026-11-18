"""Import helper for push 7: puts research/signals on the path and, because pysat is not installed on this machine,
registers a stand-in `pysat.solvers` module so that the signals library (whose sat_pulse.py imports pysat at top
level) can be imported.  Nothing in push 7 calls a SAT solver; the stand-in raises if anything tries."""
import os, sys, types

HERE = os.path.dirname(os.path.abspath(__file__))
SIG = os.path.abspath(os.path.join(HERE, '..'))
ROOT = os.path.abspath(os.path.join(SIG, '..', '..'))
SCR = os.path.join(ROOT, 'research', 'scratch', 'signals', 'p7')
os.makedirs(SCR, exist_ok=True)
if SIG not in sys.path:
    sys.path.insert(0, SIG)
if 'pysat' not in sys.modules:
    try:
        import pysat  # noqa: F401
    except ImportError:
        m = types.ModuleType('pysat'); ms = types.ModuleType('pysat.solvers')

        class Solver:
            def __init__(self, *a, **k):
                raise RuntimeError('pysat is not installed on this machine')
        ms.Solver = Solver; m.solvers = ms
        sys.modules['pysat'] = m; sys.modules['pysat.solvers'] = ms
