#!/usr/bin/env python3
"""Build the Gump Map site and the web app into one deployable tree.   python3 site/build.py [--no-app | --artifact]

  pages.json          the pages in order: slug, title, blurb, and per page its plates (id + its tile on the map)
  layout.html         the shell every page shares (head, header, footer, scripts)
  plates/<id>.html    one plate (a <section id="<id>">); plates/<id>.js its figures, if it has any
  assets/             shared CSS and JS (kit.js helpers, boot.js loader, the two steppers, stamp.js)
  data/<key>.json     one file per data key (written by collect/collect.py); a page fetches the keys its
                      plates' scripts read as D.<key>, found here by scanning the scripts
  ../web/dist         the interactive app, built by `node web/tools/build.mjs` (skipped with --no-app,
                      which then copies whatever web/dist holds) and copied to dist/app/

Writes site/dist/ (git-ignored): index.html, <slug>/index.html, assets/, plates/*.js, data/*.json, app/, .nojekyll.
With --artifact it writes site/dist-artifact/ instead (git-ignored; site/dist/ is left alone), the tree for the private
claude.ai artifact: the same overview pages, assets and data, but no app/ (and no App link or app card), no dotfiles,
data as script files (data/<key>.js, loaded by script tags, so no page fetches anything), and FILES.json: every file of the tree except index.html and FILES.json, sorted, for the publish call's file list.
Links between pages are written as relative paths ending in index.html (see README.md, "Link form").
Standard library only. Fails loudly on a missing plate, data key or element id.
"""
import html, json, pathlib, re, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
ARTIFACT = "--artifact" in sys.argv
DIST = HERE / ("dist-artifact" if ARTIFACT else "dist")
WEB = REPO / "web"


def die(msg):
    sys.exit("build.py: " + msg)


def esc(s):
    return html.escape(s, quote=True)


pages = json.loads((HERE / "pages.json").read_text())
layout = (HERE / "layout.html").read_text()
where = {}                                   # plate id -> slug of its page
for p in pages:
    for pl in p["plates"]:
        if pl["id"] in where:
            die(f"plate {pl['id']} is on two pages")
        where[pl["id"]] = p["slug"]
content_pages = [p for p in pages if p["slug"]]


def href(frm, slug, anchor=""):
    """Relative link from page `frm` to page `slug` (both slugs; '' is the landing page)."""
    up = "../" if frm else ""
    return up + (slug + "/" if slug else "") + "index.html" + ("#" + anchor if anchor else "")


def plate_html(pid, frm):
    f = HERE / "plates" / (pid + ".html")
    if not f.exists():
        die(f"missing {f.relative_to(REPO)}")
    s = f.read_text()
    if not re.search(r'<section class="(plate|hero)" id="%s">' % re.escape(pid), s):
        die(f"{f.name} must open with <section class=\"plate\" id=\"{pid}\">")

    def fix(m):                               # a link to a plate on another page
        a = m.group(1)
        if a in where and where[a] != frm:
            return 'href="%s"' % href(frm, where[a], a)
        return m.group(0)
    return re.sub(r'href="#([\w-]+)"', fix, s)


def tile(frm, pl):
    cls = ' class="new"' if pl.get("new") else ""
    vid = ' id="%s"' % pl["vid"] if pl.get("vid") else ""
    st = '<span class="st %s">%s</span>' % (pl["stc"], esc(pl["st"])) if pl.get("stc") else ""
    return '<a href="%s"%s><span class="k">%s</span><span class="v"%s>%s</span>%s</a>' % (
        href(frm, where[pl["id"]], pl["id"]), cls, esc(pl["k"]), vid, esc(pl["v"]), st)


def landing_map(frm):
    out = ['<section class="map-groups" id="map" aria-label="The pages">']
    for i, p in enumerate(content_pages, 1):
        tiles = "\n    ".join(tile(frm, pl) for pl in p["plates"] if pl.get("k"))
        out.append(f'''<div class="map-group">
  <div class="mg-h"><h2><a href="{href(frm, p['slug'])}">{esc(p['label'])}</a></h2><p class="cap">{esc(p['blurb'])}</p></div>
  <nav class="map" aria-label="{esc(p['label'])}">
    {tiles}
  </nav>
</div>''')
    if not ARTIFACT:
        out.append('''<div class="map-group app-card">
  <div class="mg-h"><h2><a href="app/index.html">The interactive app</a></h2><p class="cap">The automaton computed on your GPU with WebGL2 and drawn in 3D: a guided tour of nine live scenes, then free exploration and a gallery of objects from the atlas and the clockwork study.</p></div>
</div>''')
    out.append("</section>")
    return "\n".join(out)


def page_head(p):
    chips = "".join('<a href="#%s">%s</a>' % (pl["id"], esc(pl["k"])) for pl in p["plates"] if pl.get("k"))
    return f'''<header class="page-h">
  <p class="eyebrow"><b>gump</b> &nbsp;·&nbsp; B45/S345 on the faces of the cubic honeycomb</p>
  <h1>{esc(p['label'])}</h1>
  <p class="lede">{esc(p['blurb'])}</p>
  <nav class="toc" aria-label="On this page"><span class="toc-l">On this page</span>{chips}</nav>
</header>'''


def pager(p):
    i = content_pages.index(p) if p in content_pages else -1
    prev = content_pages[i - 1] if i > 0 else (pages[0] if i == 0 else None)
    nxt = content_pages[i + 1] if i + 1 < len(content_pages) else None
    cells = []
    if prev is not None:
        cells.append(f'<a class="pg-prev" href="{href(p["slug"], prev["slug"])}" rel="prev"><span class="pg-l">Previous</span><span class="pg-t">{esc(prev["label"])}</span></a>')
    if nxt is not None:
        con = f'<span class="pg-c">{esc(p["connects"])}</span>' if p.get("connects") else ""
        cells.append(f'<a class="pg-next" href="{href(p["slug"], nxt["slug"])}" rel="next"><span class="pg-l">Next</span><span class="pg-t">{esc(nxt["label"])}</span>{con}</a>')
    return '<nav class="pager" aria-label="Previous and next page">' + "".join(cells) + "</nav>"


def nav(frm):
    items = []
    for p in content_pages:
        cur = ' aria-current="page"' if p["slug"] == frm else ""
        items.append(f'      <a href="{href(frm, p["slug"])}"{cur}>{esc(p["label"])}</a>')
    if not ARTIFACT:                          # the artifact copy carries no app
        items.append(f'      <a class="nav-app" href="{"../" if frm else ""}app/index.html">App</a>')
    return "\n".join(items)


# ---------------------------------------------------------------- pages
if DIST.exists():
    shutil.rmtree(DIST)
DIST.mkdir()
used_keys, plate_js = set(), []
for p in pages:
    slug = p["slug"]
    root = "../" if slug else ""
    body = "\n\n".join(plate_html(pl["id"], slug) for pl in p["plates"])
    content = (body + "\n\n" + landing_map(slug)) if not slug else (page_head(p) + "\n\n" + body)
    scripts = [pl["id"] for pl in p["plates"] if (HERE / "plates" / (pl["id"] + ".js")).exists()] + p.get("scripts", [])
    src = "\n".join((HERE / "plates" / (s + ".js")).read_text() for s in scripts)
    keys = sorted(set(re.findall(r"\bD\.(\w+)", src)) | {"project"})      # project: the footer's stamp
    for k in keys:
        if not (HERE / "data" / (k + ".json")).exists():
            die(f"page {slug or 'index'} reads D.{k} but data/{k}.json does not exist")
    used_keys |= set(keys)
    plate_js += scripts
    page_ids = set(re.findall(r'\sid="([^"]+)"', content + layout))
    for ref in sorted(set(re.findall(r"""['"]#([A-Za-z][\w-]*[A-Za-z0-9_])['"]""", src))):
        if ref not in page_ids:
            die(f"page {slug or 'index'}: a script looks for #{ref}, which is not on the page")
    out = (layout.replace("{{title}}", esc(p["title"])).replace("{{description}}", esc(p["blurb"]))
           .replace("{{slug}}", slug or "index").replace("{{root}}", root).replace("{{nav}}", nav(slug))
           .replace("{{content}}", content).replace("{{pager}}", pager(p) if slug else "")
           .replace("{{data}}", " ".join(keys)).replace("{{scripts}}", " ".join(scripts))
           .replace("{{datatags}}", "".join(f'<script src="{root}data/{k}.js"></script>\n' for k in keys) if ARTIFACT else ""))
    dst = DIST / slug / "index.html" if slug else DIST / "index.html"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(out)

# ---------------------------------------------------------------- assets, plate scripts, data
shutil.copytree(HERE / "assets", DIST / "assets")
(DIST / "plates").mkdir()
for s in plate_js:
    shutil.copy2(HERE / "plates" / (s + ".js"), DIST / "plates" / (s + ".js"))
(DIST / "data").mkdir()
for k in sorted(used_keys):
    if ARTIFACT:                              # data as scripts: the artifact copy makes no fetch at all
        v = json.loads((HERE / "data" / (k + ".json")).read_text())
        (DIST / "data" / (k + ".js")).write_text(f"(self.GUMP_DATA = self.GUMP_DATA || {{}})[{json.dumps(k)}] = "
                                                 + json.dumps(v, separators=(",", ":"), ensure_ascii=True) + ";\n")
    else:
        shutil.copy2(HERE / "data" / (k + ".json"), DIST / "data" / (k + ".json"))
unused = sorted(f.stem for f in (HERE / "data").glob("*.json") if f.stem not in used_keys)
if unused:
    print("note: data files no page reads:", ", ".join(unused))
if not ARTIFACT:
    (DIST / ".nojekyll").write_text("")      # GitHub Pages: serve files as they are

# ---------------------------------------------------------------- the web app, under app/ (Pages tree only)
if not ARTIFACT and "--no-app" not in sys.argv:
    r = subprocess.run(["node", "tools/build.mjs"], cwd=WEB)
    if r.returncode:
        die("node web/tools/build.mjs failed (run `npm ci` in web/ first, or pass --no-app to copy web/dist as it is)")
if not ARTIFACT:
    if not (WEB / "dist" / "index.html").exists():
        die("web/dist/index.html is missing: build the app (node web/tools/build.mjs)")
    shutil.copytree(WEB / "dist", DIST / "app", ignore=shutil.ignore_patterns(".nojekyll"))
else:
    dots = [f for f in DIST.rglob(".*")]
    if dots:
        die("dotfiles in the artifact tree: " + ", ".join(str(f.relative_to(DIST)) for f in dots))
    listed = sorted(f.relative_to(DIST).as_posix() for f in DIST.rglob("*") if f.is_file() and f.relative_to(DIST).as_posix() != "index.html")
    (DIST / "FILES.json").write_text(json.dumps(listed, indent=0) + "\n")

files = [f for f in DIST.rglob("*") if f.is_file()]
print(f"wrote {DIST.relative_to(REPO)}/: {len(pages)} pages, {len(plate_js)} plate scripts, {len(used_keys)} data files, "
      f"{len(files)} files in all, {sum(f.stat().st_size for f in files) / 1024:.0f} KiB")
