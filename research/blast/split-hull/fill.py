#!/usr/bin/env python3
"""Paste the current output of levels.py (parts 2, 4, 5) into README.md between the DIPTABLE markers."""
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
out = subprocess.run([sys.executable, os.path.join(HERE, 'levels.py')], capture_output=True, text=True).stdout
p2 = out[out.index('PART 2'):out.index('PART 3')].rstrip()
p45 = out[out.index('PART 4'):].rstrip()
block = '<!-- DIPTABLE -->\n```\n' + p2 + '\n\n' + p45 + '\n```\n<!-- /DIPTABLE -->'
f = os.path.join(HERE, 'README.md'); s = open(f).read()
if '<!-- DIPTABLE -->' in s:
    s = re.sub(r'<!-- DIPTABLE -->.*?<!-- /DIPTABLE -->', lambda m: block, s, flags=re.S)
else:
    s = s.replace('DIPTABLE', block, 1)
open(f, 'w').write(s)
