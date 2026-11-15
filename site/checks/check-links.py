#!/usr/bin/env python3
"""Link checker over the built tree.   python3 site/checks/check-links.py [--artifact]

For every file of site/dist (the app under app/ included) checks that each relative reference resolves to a file
of the tree: HTML href/src (and #anchors on overview pages: the id must exist on the target page), CSS url(),
the import map, JS `import ... from './…'` and `new URL('…', import.meta.url)`, and boot.js's per-page lists
(data-data -> data/<key>.json, data-plates -> plates/<id>.js). Fails too on any root-absolute path ("/…"), which
would break under the GitHub Pages subpath, and on external scripts or stylesheets from hosts the claude.ai
artifact host does not allow, or without an exact version. Prints the file count and total size.
With --artifact it checks site/dist-artifact/ instead, and fails too on any reference to app/, on any dotfile, and
unless FILES.json lists exactly the tree's files other than index.html and FILES.json, sorted.
"""
import json, pathlib, re, sys
from urllib.parse import urlsplit

ARTIFACT = "--artifact" in sys.argv
DIST = pathlib.Path(__file__).resolve().parent.parent / ("dist-artifact" if ARTIFACT else "dist")
if not (DIST / "index.html").exists():
    sys.exit(f"site/{DIST.name} is not built: python3 site/build.py" + (" --artifact" if ARTIFACT else ""))
bad, n_refs = [], 0
SCRIPT_HOSTS = ("https://cdnjs.cloudflare.com/", "https://cdn.jsdelivr.net/npm/", "https://unpkg.com/")
STYLE_HOSTS = ("https://fonts.googleapis.com/",)
files = sorted(f for f in DIST.rglob("*") if f.is_file())
ids_cache = {}


def ids_of(f):
    if f not in ids_cache:
        ids_cache[f] = set(re.findall(r'\sid="([^"]+)"', f.read_text(errors="replace")))
    return ids_cache[f]


def check(src, ref, kind):
    global n_refs
    if not ref or "${" in ref or ref.startswith(("data:", "blob:", "mailto:", "javascript:")):   # ${…}: built at run time
        return
    if ref.startswith(("http://", "https://", "//")):
        if kind == "script" and not ref.startswith(SCRIPT_HOSTS):
            bad.append(f"{src.relative_to(DIST)}: external script from a host the artifact does not allow: {ref}")
        if kind == "stylesheet" and not ref.startswith(STYLE_HOSTS):
            bad.append(f"{src.relative_to(DIST)}: external stylesheet not from Google Fonts: {ref}")
        if kind == "script" and not re.search(r"[@/]\d+\.\d+\.\d+", ref):
            bad.append(f"{src.relative_to(DIST)}: external script without an exact version: {ref}")
        return
    n_refs += 1
    if ARTIFACT and re.match(r"(\.\./)*app(/|$)", ref):
        bad.append(f"{src.relative_to(DIST)}: refers to the app ({ref}), which the artifact copy does not carry"); return
    if ref.startswith("/"):
        bad.append(f"{src.relative_to(DIST)}: root-absolute path {ref} (breaks under a subpath)"); return
    u = urlsplit(ref)
    if u.path == "":
        tgt = src
    else:
        tgt = (src.parent / u.path).resolve()
        if u.path.endswith("/"):
            if kind == "url" and tgt.is_dir():          # a folder base, e.g. the app's SOURCES
                return
            tgt = tgt / "index.html"
    if not tgt.is_file() or DIST.resolve() not in tgt.parents and tgt != DIST.resolve():
        bad.append(f"{src.relative_to(DIST)}: {kind} {ref} -> no such file"); return
    if u.fragment and tgt.suffix == ".html" and "app" not in tgt.relative_to(DIST.resolve()).parts:
        if u.fragment not in ids_of(tgt):
            bad.append(f"{src.relative_to(DIST)}: {ref} -> no element #{u.fragment} there")


for f in files:
    rel = f.relative_to(DIST)
    if f.suffix == ".html":
        s = f.read_text()
        for tag in re.finditer(r"<(a|link|script|img|source|iframe)\b([^>]*)>", s):
            attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', tag.group(2)))
            kind = "stylesheet" if attrs.get("rel") == "stylesheet" else tag.group(1)
            for a in ("href", "src"):
                if a in attrs:
                    check(f, attrs[a].replace("&amp;", "&"), kind)
            if "data-data" in attrs:
                root = attrs.get("data-root", "")
                for k in attrs["data-data"].split():
                    check(f, f"{root}data/{k}.{'js' if ARTIFACT else 'json'}", "script" if ARTIFACT else "fetch")
                for p in attrs.get("data-plates", "").split():
                    check(f, f"{root}plates/{p}.js", "script")
        m = re.search(r'<script type="importmap">(.*?)</script>', s, re.S)
        if m:
            for v in json.loads(m.group(1))["imports"].values():
                if v.endswith("/"):                    # a folder prefix
                    if not (f.parent / v).resolve().is_dir():
                        bad.append(f"{rel}: import map folder {v} missing")
                else:
                    check(f, v, "importmap")
        if re.search(r'''\s(?:href|src)="/[^/]''', s):
            bad.append(f"{rel}: root-absolute href/src")
    elif f.suffix == ".css":
        for ref in re.findall(r"""url\(\s*['"]?([^'")]+)""", f.read_text()):
            check(f, ref, "css url")
    elif f.suffix in (".js", ".mjs") and "vendor" not in rel.parts:
        s = f.read_text()
        for ref in re.findall(r"""(?:^|\n)\s*import\s[^'"]*?from\s*['"](\.[^'"]+)['"]""", s) + re.findall(r"""import\(\s*['"](\.[^'"]+)['"]""", s):
            check(f, ref, "import")
        for ref in re.findall(r"""new URL\(\s*['"](\.[^'"]+)['"]\s*,\s*import\.meta\.url""", s):
            check(f, ref, "url")
        for ref in re.findall(r"""fetch\(\s*['"]([^'"]+)['"]""", s):
            check(f, ref, "fetch")

if ARTIFACT:
    for f in DIST.rglob(".*"):
        bad.append(f"dotfile {f.relative_to(DIST)}")
    want = sorted(f.relative_to(DIST).as_posix() for f in files if f.relative_to(DIST).as_posix() not in ("index.html", "FILES.json"))
    if not (DIST / "FILES.json").exists() or json.loads((DIST / "FILES.json").read_text()) != want:
        bad.append("FILES.json does not list exactly the tree's files (index.html and FILES.json aside), sorted")
    for f in files:
        if f.suffix in (".html", ".css", ".js") and re.search(r"""['"(](\.\./)*app/""", f.read_text()):
            bad.append(f"{f.relative_to(DIST)}: mentions a path into app/")
total = sum(f.stat().st_size for f in files)
big = max(files, key=lambda f: f.stat().st_size)
print(f"links: {n_refs} relative references in {len(files)} files ({total / 1024:.0f} KiB; largest {big.relative_to(DIST)}, "
      f"{big.stat().st_size / 1024:.0f} KiB)")
if len(files) > 255:
    bad.append(f"{len(files)} files: more than the 255 one artifact publish takes")
for b in bad:
    print("FAIL", b)
print("links: OK" if not bad else f"links: {len(bad)} failure(s)")
sys.exit(1 if bad else 0)
