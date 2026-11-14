#!/usr/bin/env python3
"""Negative control for ts.py validate: tile the (5,1),(0,4) slab's soup with the coset representatives of the
wrong lattice (5,0),(0,4). Must MISMATCH.   python3 research/audit/shape/negctl.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ts, geom_check as gc
orig = gc.in_lat
gc.in_lat = lambda v, L: orig(v, (5, 0, 4)) if L == (5, 1, 4) and v != (20, 0) and v != (0, 20) else orig(v, L)
print('negative control (must be False):', ts.validate((5, 1, 4), 200, 20))
