#!/usr/bin/env python3
"""The landing page in the form the claude.ai artifact host wants for the page itself.

    python3 site/build.py --artifact && python3 site/artifact_page.py

The host wraps the published page in its own <!doctype html><html><head>…</head><body> skeleton (charset and
viewport metas, a small reset), so the page itself must come without those tags; the other pages are published as
supporting files, are served as they are, and keep theirs. This writes research/scratch/site/artifact-page/index.html
(git-ignored): site/dist-artifact/index.html with its doctype, html, head and body tags and its charset and viewport
metas removed, everything else byte for byte. Publish that file as the page, with root site/dist-artifact and the
paths of site/dist-artifact/FILES.json as the supporting files.
"""
import pathlib, re
here = pathlib.Path(__file__).resolve().parent
src = (here / "dist-artifact" / "index.html").read_text()
out = src
for pat in (r"<!doctype html>\s*", r"<html[^>]*>\s*", r"<head>\s*", r"</head>\s*", r"<body[^>]*>\s*", r"</body>\s*", r"</html>\s*",
            r'<meta charset="utf-8">\s*', r'<meta name="viewport"[^>]*>\s*'):
    out, n = re.subn(pat, "", out, count=1, flags=re.I)
    assert n == 1, pat
assert out.lstrip().startswith("<title>") and not re.search(r"<(!doctype|html|head|body)\b", out, re.I)
dst = here.parent / "research" / "scratch" / "site" / "artifact-page" / "index.html"
dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text(out)
print("wrote", dst, len(out), "bytes; removed", len(src) - len(out), "bytes of wrapper")
