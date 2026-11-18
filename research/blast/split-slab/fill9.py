#!/usr/bin/env python3
"""Put sec_table.py's tables into README section 9 (between markers).   python3 fill9.py"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
t = subprocess.run([sys.executable, os.path.join(HERE, 'sec_table.py')], capture_output=True, text=True)
assert t.returncode == 0, t.stderr
p = os.path.join(HERE, 'README.md'); s = open(p).read()
a, b = '<!-- SEC9-TABLES-BEGIN -->', '<!-- SEC9-TABLES-END -->'
assert a in s and b in s
s = s.split(a)[0] + a + '\n' + t.stdout + b + s.split(b)[1]
open(p, 'w').write(s)
print(t.stdout)
