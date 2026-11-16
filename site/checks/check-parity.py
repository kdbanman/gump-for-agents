#!/usr/bin/env python3
"""Nothing lost: the built site against the last single-page overview.
    python3 site/checks/check-parity.py [--dist site/dist-artifact] [OLD.html]

OLD is the single page as it was before the split (default: `git show 2f0868d:docs/overview/index.html`, the
version of 2026-11-15 12:04 that the split started from). Checks, against site/dist (run build.py first):
  1. every plate (<section id>) of the old page appears exactly once in the new site, on one page, and its HTML is
     the old HTML byte for byte once links to plates on other pages (../<page>/index.html#id) are read back as #id;
     this covers every heading, figure, number, caption and the controls of every live demo;
  2. every figure (<figure>), canvas and button of the old page is counted again in the new site;
  3. every element id the old page's scripts look up ('#id') is looked up by a script of the page that holds it;
  4. every data key the old page's scripts read (D.key) is read by a script of some page, every page is served
     (data-data) every key its scripts read, the file exists in dist/data, and its content equals the old page's D.key;
  5. the map's 28 tiles are on the landing page, each linking to its plate's page.
Exit status 1 on any failure.
"""
import json, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent
args = sys.argv[1:]
DIST = SITE / "dist"
if "--dist" in args:
    i = args.index("--dist"); DIST = pathlib.Path(args[i + 1]).resolve(); del args[i:i + 2]
OLD_REV = "2f0868d"
# Edits made on purpose since OLD_REV, the only differences allowed: (plate, old text, new text), each occurring
# exactly once. Three sentences that pointed "below" / "above" / "at the top" to plates now on other pages.
EDITS = [
    ("rule", "the rule you meant, below</a>", "the rule you meant, on the Relatives page</a>"),
    ("fauna", "the same rule as the run at the top.", "the same rule as the run on the map page."),
    ("family", "(the 0.91 nats above)", "(the 0.91 nats on the area-law page)"),
]
# Plates added since OLD_REV, and old plates whose HTML was rewritten on purpose (each with where it comes from); the data
# keys whose content may differ from the old page's. Anything not named here must still be as it was.
NEW = {
    "wrap": "phase 2 (2026-11-15 afternoon): What a short way round costs (NB the wrapping law tested; CLAIMS WL1-WL3); rewritten the "
            "evening of 2026-11-15 around the density law (NB why a tube is cheaper; CLAIMS WL4-WL6, W13); 2026-11-16: W13 measured, the "
            "long tubes below their line, kappa 3.0 on them (NB the card's tube and wrapped faces; CLAIMS WL7, WL8)",
    "gun": "phase 2: A gun (NB the fourth signals push, reviewed; CLAIMS SG16-SG18)",
    "divider": "phase 2: A clock that edits the message (CLAIMS SG19, SG22)",
    "echo": "evening 2026-11-15: An echo, live (NB the fifth signals push reviewed; CLAIMS SG26; research/audit/signals5/end_echo.json); "
            "night 2026-11-15: its result, no gun survives an echo and the reflector works once (NB the sixth signals push reviewed; CLAIMS SG30, SG31)",
    "meetings": "night 2026-11-15: When signals meet, live (NB the sixth signals push, reviewed; CLAIMS SG28, SG29; "
                "research/signals/objects/echo-train.json, research/audit/signals6/sig6.py)",
    "ends": "evening 2026-11-15: Nothing listens (NB the fifth signals push, reviewed; CLAIMS SG23-SG25, SG27); night 2026-11-15: the events "
            "review 5 had not followed, the count an echo writes, six pushes' forecasts (NB the sixth signals push reviewed; CLAIMS SG29, SG32)",
}
CHANGED = {
    "constant": "phase 2: nine wrapped faces in place of five (NB the nine wrapped faces reviewed; CLAIMS GL3); evening 2026-11-15: one "
                "sentence on the price with no loop, if the density law holds (CLAIMS WL5); 2026-11-16: rewritten around the answer no, the "
                "prices by kind of face, the two negatives (NB the hull face of 108 cells; a living hull face …; the card's tube and wrapped "
                "faces; CLAIMS CN2-CN4, WL7, WL8)",
    "next": "phase 2: Open now, from docs/WHAT-I-SEE.md 'What I would look at next' and OPEN-PROBLEMS 9 and 13; evening 2026-11-15: the echo "
            "and the sixth push, the loop of 21 queued (W13), the price with no loop (NB why a tube is cheaper; STATUS 20:27 UTC); night 2026-11-15: "
            "the sixth push done, OPEN-PROBLEMS 13 (q)-(t) open (NB the sixth signals push reviewed); 2026-11-16: how each kind of face "
            "dies, the long tubes and the loop of 21 (OPEN-PROBLEMS 9 (k)-(m))",
}
CHANGED_DATA = {
    "tori": "nine faces, recomputed from research/data/gpu_local_eqtorus (CLAIMS GL3)",
    "project": "the ledger's counts (197 claims since 2026-11-16), the git timeline and the footer's date follow the repository",
    "forecasts": "three forecasts scored on 2026-11-16 added (NB the hull face of 108 cells; research/wrap/PREDICTIONS.md, H1-H5 and W9-W13 scored)",
    "corrections": "four corrections of 2026-11-15 afternoon added; two more in the evening (CLAIMS WL2/WL4; NB the fifth signals push reviewed); three at night (NB the sixth signals push reviewed); two on 2026-11-16 (CLAIMS CN2; NB the card's tube and wrapped faces)",
}
bad = []

if args:
    old = pathlib.Path(args[0]).read_text()
else:
    old = subprocess.check_output(["git", "show", f"{OLD_REV}:docs/overview/index.html"], cwd=SITE, text=True)


def sections(s):
    out = {}
    for m in re.finditer(r'<section class="(?:plate|hero)" id="([^"]+)">', s):
        depth, j = 0, None
        for t in re.finditer(r"</?section\b", s[m.start():]):
            depth += 1 if t.group(0) == "<section" else -1
            if depth == 0:
                j = s.index(">", m.start() + t.start()) + 1
                break
        if m.group(1) in out:
            bad.append(f"plate {m.group(1)} occurs twice on one page")
        out[m.group(1)] = s[m.start():j]
    return out


scripts = re.findall(r"<script>(.*?)</script>", old, re.S)
D_old = json.loads(scripts[0].replace("const D = ", "", 1).rstrip().rstrip(";"))
old_js = scripts[2]
old_secs = sections(old)

pages = json.loads((SITE / "pages.json").read_text())
new_secs, sec_page, page_info = {}, {}, {}
for p in pages:
    f = DIST / (p["slug"] + "/index.html" if p["slug"] else "index.html")
    s = f.read_text()
    tag = re.search(r'<script src="[^"]*assets/boot\.js" data-root="([^"]*)" data-data="([^"]*)" data-plates="([^"]*)"', s)
    keys, plates = tag.group(2).split(), tag.group(3).split()
    js = "\n".join((DIST / "plates" / (x + ".js")).read_text() for x in plates)
    page_info[p["slug"]] = dict(html=s, keys=keys, js=js)
    for k, v in sections(s).items():
        if k in new_secs:
            bad.append(f"plate {k} is on two pages ({sec_page[k] or 'index'}, {p['slug'] or 'index'})")
        new_secs[k], sec_page[k] = v, p["slug"]

# 1
for k, v in old_secs.items():
    if k not in new_secs:
        bad.append(f"plate {k} is missing"); continue
    back = re.sub(r'href="(?:\.\./)?(?:[\w-]+/)?index\.html#([\w-]+)"', r'href="#\1"', new_secs[k])
    for pid, a, b in EDITS:
        if pid == k:
            if back.count(b) != 1:
                bad.append(f"plate {k}: the allowed edit {b!r} is not there exactly once"); continue
            back = back.replace(b, a)
    if back != v and k not in CHANGED:
        bad.append(f"plate {k}: HTML differs from the old page")
    if k in CHANGED and back == v:
        bad.append(f"plate {k} is declared changed but is as it was: take it out of CHANGED")
extra = set(new_secs) - set(old_secs)
for k in sorted(extra - set(NEW)):
    bad.append(f"plate {k} is new and not declared in NEW")
for k in sorted(set(NEW) - extra):
    bad.append(f"plate {k} is declared in NEW and not in the site")
if extra:
    print("new plates, declared:", " ".join(sorted(extra)), "; changed on purpose:", " ".join(sorted(CHANGED)))

# 2
def count(rx, secs): return sum(len(re.findall(rx, v)) for v in secs.values())
counts = {}
for name, rx in (("figures", r"<figure\b"), ("canvases", r"<canvas\b"), ("buttons", r"<button\b"), ("h2 headings", r"<h2\b")):
    a = count(rx, {k: v for k, v in old_secs.items() if k not in CHANGED})
    b = count(rx, {k: new_secs[k] for k in old_secs if k in new_secs and k not in CHANGED})
    counts[name] = (a, b)
    if a != b:
        bad.append(f"{name}: {a} on the old page, {b} in the new site")

# 3
id_ref = re.compile(r"""['"]#([A-Za-z][\w-]*[A-Za-z0-9_])['"]""")
id_home = {}
for k, v in old_secs.items():
    for i in re.findall(r'\sid="([^"]+)"', v):
        id_home[i] = k
n_ids = 0
for i in sorted(set(id_ref.findall(old_js))):
    if i not in id_home or id_home[i] in CHANGED:
        continue                                       # #tip, #stamp, the map's #m-built: checked by the smoke test
    n_ids += 1
    home = sec_page.get(id_home[i])
    if home is None or i not in id_ref.findall(page_info[home]["js"]):
        bad.append(f"#{i} (plate {id_home[i]}) is no longer looked up by a script of its page")

# 4
old_keys = set(re.findall(r"\bD\.(\w+)", old_js))
served = set()
for slug, info in page_info.items():
    need = set(re.findall(r"\bD\.(\w+)", info["js"]))
    for k in need - set(info["keys"]):
        bad.append(f"page {slug or 'index'} reads D.{k} but does not fetch it")
    for k in info["keys"]:
        f, fj = DIST / "data" / (k + ".json"), DIST / "data" / (k + ".js")    # .js: the artifact copy's script form
        if f.exists():
            val = json.loads(f.read_text())
        elif fj.exists() and f'data/{k}.js"></script>' in info["html"]:
            pre = f"(self.GUMP_DATA = self.GUMP_DATA || {{}})[{json.dumps(k)}] = "
            t = fj.read_text().rstrip()
            if not (t.startswith(pre) and t.endswith(";")):
                bad.append(f"data/{k}.js is not in the expected form"); continue
            val = json.loads(t[len(pre):-1])
        else:
            bad.append(f"page {slug or 'index'} needs data {k}, which is not served to it"); continue
        if k in D_old and val != D_old[k] and k not in CHANGED_DATA:
            bad.append(f"data/{k}.json differs from the old page's D.{k}")
    served |= need
for k in sorted(old_keys - served):
    bad.append(f"D.{k}, read by the old page, is read by no page now")

# 5
old_map = re.findall(r'<a href="#([\w-]+)"[^>]*><span class="k">', re.search(r'<nav class="map".*?</nav>', old, re.S).group(0))
landing = page_info[""]["html"]
for i in old_map:
    want = (sec_page[i] + "/" if sec_page.get(i) else "") + "index.html#" + i
    if f'<a href="{want}"' not in landing:
        bad.append(f"map tile for #{i} missing or not linking to {want}")

print(f"plates: {len(old_secs)} on the old page, {sum(1 for k in old_secs if k in new_secs)} found once in the new site "
      f"({sum(1 for k in old_secs if k in new_secs and k not in CHANGED and not any(b.startswith('plate ' + k + ':') for b in bad))} byte-identical apart from the {len(EDITS)} listed edits and the {len(CHANGED)} plates declared changed)")
print("; ".join(f"{n}: {a} old, {b} new" for n, (a, b) in counts.items()))
print(f"element ids looked up by scripts: {n_ids}; data keys read by the old page: {len(old_keys)}, read now: {len(served & old_keys)}"
      f" (old D held {len(D_old)} keys; never read: {', '.join(sorted(set(D_old) - old_keys)) or 'none'})")
print(f"map tiles: {len(old_map)}")
for b in bad:
    print("FAIL", b)
print("parity: OK" if not bad else f"parity: {len(bad)} failure(s)")
sys.exit(1 if bad else 0)
