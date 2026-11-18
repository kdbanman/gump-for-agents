#!/usr/bin/env python3
"""Put pool192.py's output into README section 11 (between markers).   python3 fill11.py"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
t = subprocess.run([sys.executable, os.path.join(HERE, 'pool192.py')], capture_output=True, text=True); assert t.returncode == 0, t.stderr
p = os.path.join(HERE, 'README.md'); s = open(p).read()
a, b = '<!-- SEC11-BEGIN -->', '<!-- SEC11-END -->'
s = s.split(a)[0] + a + '\n' + t.stdout + b + s.split(b)[1]
open(p, 'w').write(s); print(t.stdout)
