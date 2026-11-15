#!/usr/bin/env python3
"""The artifact page contract, checked statically on every HTML page.   python3 site/checks/check-contract.py [DIR]

DIR defaults to site/dist-artifact. For each .html file: doctype first; <meta charset>; a viewport meta with
width=device-width; a <title> of two to four words with no colon or dash explanation, within the first 8 KB; the
stylesheets it loads (local files or Google Fonts only) together define: an explicit body background from a token,
the dark theme under both `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) … }` and
`:root[data-theme="dark"]`, each with color-scheme: dark, and every token those blocks set also set on bare :root;
if the page declares claude:viewport-fit-sides, the CSS has both max(16px, env(safe-area-inset-left/right)) paddings;
external scripts only from cdnjs.cloudflare.com, cdn.jsdelivr.net/npm or unpkg.com with an exact version.
Prints each page's title. Exit status 1 on any failure.
"""
import pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent
DIST = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else SITE / "dist-artifact"
if not (DIST / "index.html").exists():
    sys.exit(f"{DIST} is not built: python3 site/build.py --artifact")
SCRIPT_HOSTS = ("https://cdnjs.cloudflare.com/", "https://cdn.jsdelivr.net/npm/", "https://unpkg.com/")
bad = []


def block_after(css, start):
    """The {...} block whose opening brace is the first at or after `start`."""
    i = css.index("{", start); d = 0
    for j in range(i, len(css)):
        d += css[j] == "{"; d -= css[j] == "}"
        if d == 0:
            return css[i + 1:j]
    return ""


def tokens(body):
    return set(re.findall(r"(--[\w-]+)\s*:", body))


for f in sorted(DIST.rglob("*.html")):
    rel = f.relative_to(DIST)
    if "app" in rel.parts:
        continue
    s = f.read_text()
    fail = lambda m: bad.append(f"{rel}: {m}")
    if not re.match(r"\s*<!doctype html>", s, re.I):
        fail("no doctype at the start")
    if not re.search(r'<meta charset="utf-8">', s, re.I):
        fail("no charset meta")
    if not re.search(r'<meta name="viewport" content="[^"]*width=device-width', s):
        fail("no viewport meta")
    t = re.search(r"<title>([^<]*)</title>", s[:8192])
    title = t.group(1).strip() if t else ""
    n = len(title.split())
    if not t or not 2 <= n <= 4 or re.search(r"[:–—]| - ", title):
        fail(f"title {title!r}: wants a name of two to four words, no colon or dash")
    css = ""
    for href in re.findall(r'<link rel="stylesheet" href="([^"]+)"', s):
        if href.startswith("https://fonts.googleapis.com/"):
            continue
        if href.startswith(("http:", "https:", "//")):
            fail(f"external stylesheet not from Google Fonts: {href}"); continue
        css += (f.parent / href).read_text()
    css += "".join(re.findall(r"<style>(.*?)</style>", s, re.S))
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    if not re.search(r"(^|[}\s])body\s*\{[^}]*background(-color)?\s*:\s*var\(--", css):
        fail("no explicit body background from a token")
    root = set().union(*[tokens(block_after(css, m.end() - 1)) for m in re.finditer(r"(^|[}\s]):root\s*\{", css)] or [set()])
    media = [m for m in re.finditer(r"@media\s*\(prefers-color-scheme:\s*dark\)\s*\{", css)]
    guarded = [block_after(block_after(css, m.end() - 1), 0) if ':root:not([data-theme="light"])' in block_after(css, m.end() - 1) else None for m in media]
    guarded = [g for g in guarded if g is not None]
    explicit = [block_after(css, m.end() - 1) for m in re.finditer(r':root\[data-theme="dark"\]\s*\{', css)]
    if not guarded:
        fail('no dark theme under @media (prefers-color-scheme: dark) :root:not([data-theme="light"])')
    if not explicit:
        fail('no dark theme under :root[data-theme="dark"]')
    if guarded and "color-scheme:dark" not in guarded[0].replace(" ", ""):
        fail("the media dark block does not set color-scheme: dark")
    if explicit and "color-scheme:dark" not in explicit[0].replace(" ", ""):
        fail('the [data-theme="dark"] block does not set color-scheme: dark')
    dark_tokens = set().union(*[tokens(b) for b in guarded + explicit] or [set()])
    if dark_tokens - root:
        fail("tokens set only in a dark block: " + " ".join(sorted(dark_tokens - root)))
    if set().union(*[tokens(b) for b in guarded] or [set()]) != set().union(*[tokens(b) for b in explicit] or [set()]):
        fail("the two dark blocks do not set the same tokens")
    if 'name="claude:viewport-fit-sides"' in s and not (
            re.search(r"padding-left:\s*max\(16px,\s*env\(safe-area-inset-left", css) and re.search(r"padding-right:\s*max\(16px,\s*env\(safe-area-inset-right", css)):
        fail("declares viewport-fit-sides without both max(16px, env(...)) side paddings")
    for src in re.findall(r'<script[^>]*\ssrc="([^"]+)"', s):
        if src.startswith(("http:", "https:", "//")):
            if not src.startswith(SCRIPT_HOSTS):
                fail(f"external script from a host the artifact does not allow: {src}")
            elif not re.search(r"[@/]\d+\.\d+\.\d+([/-]|$)", src):
                fail(f"external script without an exact version: {src}")
    print(f"{str(rel):28s} {title!r}")
for b in bad:
    print("FAIL", b)
print("contract: OK" if not bad else f"contract: {len(bad)} failure(s)")
sys.exit(1 if bad else 0)
