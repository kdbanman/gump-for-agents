#!/usr/bin/env python3
"""Assemble docs/overview/index.html from src/ and data/.   python3 docs/overview/build.py"""
import json, pathlib, datetime
here = pathlib.Path(__file__).parent
src = here / "src"
page = (src / "page.html").read_text()
data = json.loads((here / "data" / "data.json").read_text())
app = (src / "app.js").read_text().replace("/*FIGURES*/", (src / "figures.js").read_text()).replace("/*FIGURES2*/", (src / "figures2.js").read_text())
for key, fn in (("<!--MAP-->", "map.html"), ("<!--PLATES-->", "plates.html"), ("<!--LAW-->", "plates-law.html"), ("<!--REST-->", "plates-rest.html")):
    p = src / fn
    page = page.replace(key, p.read_text() if p.exists() else "")
page = page.replace("/*DATA*/null", json.dumps(data, separators=(",", ":")))
page = page.replace("/*CORE*/", (here / "gump-core.js").read_text())
page = page.replace("/*APP*/", app)
assert "</script>" not in json.dumps(data)
(here / "index.html").write_text(page)
print("wrote", here / "index.html", len(page), "bytes")
