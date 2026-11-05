"""
Builds the Computing Lab website from the data in this file and in activities_data.json.

Run it whenever you change anything:
    python3 generate_site.py

What it makes:
  index.html            the home page (year groups and topics)
  cyber.html, hardware.html, bebras.html     topic pages
  turtle.html, debug.html                    Python activity topic pages
  activities/*.html     one page per Python activity (from activities_data.json)
It also adds the Home bar to the stand-alone lab and revision pages
(cyber-lab.html, hardware-lab.html, wolf-vault.html, ...).

To add a topic or a page: edit YEARS / TOPICS below, then run this script.
The look of the whole site lives in site.css (frame + topic looks) and style.css (Python activity pages).
"""
import json
import html
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "activities_data.json")
SITE = "Computing Lab"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lexend:wght@500;700'
         '&family=Atkinson+Hyperlegible:wght@400;700&family=JetBrains+Mono:wght@400;500'
         '&family=Chakra+Petch:wght@600;700&family=Oxanium:wght@600;700'
         '&family=Bricolage+Grotesque:opsz,wght@12..96,700&display=swap">')

# ---------- Python activity categories (from activities_data.json) ----------
CATEGORIES = {
    "turtle": {"label": "Python Turtle", "theme": "t-turtle", "year": "Year 9",
               "tagline": "Copy the starter code into Thonny, then debug it or extend it.",
               "extra": [("Python Turtle quiz and flashcards", "Revision", "y9-turtle-revision.html")]},
    "debug": {"label": "Python debug activities", "theme": "t-debug", "year": "Year 10",
              "tagline": "Short programs with a bug hiding in them. Find it, fix it, then extend it.",
              "extra": []},
}

# ---------- Topic pages ----------
# rows: (title, tag, href, [ (lesson label, #hash) ... ])
TOPICS = {
    "cyber": {"title": "Networks & Cyber Security", "year": "Year 8", "theme": "t-cyber", "stamp": "TOP SECRET",
              "lead": "Follow the packets, crack the codes, stop the hackers.",
              "rows": [("Cyber Lab", "Lab", "cyber-lab.html", [("1 Packet Journey", "packets"), ("2 Network Builder", "builder"), ("3 Binary Lab", "binary"), ("4 Hacker Hats", "hats"), ("5 Phish Spotter", "phish"), ("6 Cipher Lab", "cipher"), ("7 Password Lab", "password")]),
                       ("Cyber Agent Mission", "Lesson 7", "cyber-agent.html", []),
                       ("Cyber Revision", "Revision", "cyber-revision.html", [])]},
    "hardware": {"title": "What's inside a computer?", "year": "Year 9", "theme": "t-hw",
                 "lead": "CPU, memory, storage, the cloud and data centres.",
                 "rows": [("Hardware Lab", "Lab", "hardware-lab.html", [("1 Inside the Box", "box"), ("2 Wolf CPU", "cpu"), ("3 Memory Lab", "memory"), ("4 Storage Lab", "storage"), ("5 Cloud Lab", "cloud"), ("6 Data Centre Lab", "dc"), ("7 PC Builder", "builder")]),
                          ("Hardware Revision", "Revision", "hardware-revision.html", [])]},
    "bebras": {"title": "Bebras", "year": None, "theme": "t-bebras",
               "lead": "Puzzles for computational thinkers, for every year group.",
               "rows": [("The Wolf Vault", "Escape room", "wolf-vault.html", []),
                        ("Bebras past challenges", "Practice", "https://www.bebras.uk/index.php?action=user_competitions", [])]},
}

# ---------- Home page: year groups and their topics ----------
# (label, href, swatch colour)
YEARS = [
    ("Year 7", [("Scratch", "y7-scratch-revision.html", "#f59e0b")]),
    ("Year 8", [("micro:bit", "y8-microbit-revision.html", "#e5484d"), ("Networks & Cyber Security", "cyber.html", "#0b6f9a")]),
    ("Year 9", [("Python Turtle", "turtle.html", "linear-gradient(135deg,#d62828 50%,#1d4e9e 50%)"), ("What's inside a computer?", "hardware.html", "#1b7a52")]),
    ("Year 10", [("Key terms", "y10-key-terms-revision.html", "#7c4dcc"), ("Python debug activities", "debug.html", "#0e8f8a")]),
]
BEBRAS_ROW = [("Bebras puzzles", "bebras.html", "#2f5d46")]

LABFIX = '<style>nav a[aria-current="page"],.tab[aria-selected="true"]{background:var(--fibre)!important;border-color:var(--fibre)!important;color:var(--paper)!important}</style>'
OXANIUM = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oxanium:wght@600;700&display=swap"><style>:root{--display:"Oxanium","Segoe UI",Arial,sans-serif}</style>'
# Stand-alone pages that get the Home bar: file -> (crumb text, crumb link or None, extra <head> html)
STANDALONE = {
    "cyber-lab.html": ("Year 8 › Networks & Cyber Security", "cyber.html", LABFIX),
    "cyber-agent.html": ("Year 8 › Networks & Cyber Security", "cyber.html", LABFIX),
    "cyber-revision.html": ("Year 8 › Networks & Cyber Security", "cyber.html", LABFIX),
    "hardware-lab.html": ("Year 9 › What's inside a computer?", "hardware.html", OXANIUM + LABFIX),
    "hardware-revision.html": ("Year 9 › What's inside a computer?", "hardware.html", OXANIUM + LABFIX),
    "wolf-vault.html": ("Bebras", "bebras.html", ""),
    "y7-scratch-revision.html": ("Year 7 › Scratch", None, ""),
    "y8-microbit-revision.html": ("Year 8 › micro:bit", None, ""),
    "y9-turtle-revision.html": ("Year 9 › Python Turtle", "turtle.html", ""),
    "y10-key-terms-revision.html": ("Year 10 › Key terms", None, ""),
}

e = html.escape


def bar(root, crumb_text=None, crumb_href=None):
    crumb = ""
    if crumb_text:
        inner = f'<a href="{root}{crumb_href}">{e(crumb_text)}</a>' if crumb_href else e(crumb_text)
        crumb = f'<span class="cl-crumb">{inner}</span>'
    return (f'<div class="cl-bar" role="navigation" aria-label="Site">'
            f'<a class="cl-home" href="{root}index.html"><span class="cl-mark">&lt;/&gt;</span>{SITE}</a>{crumb}</div>')


def crumb_for(cat_slug, root):
    c = CATEGORIES[cat_slug]
    return bar(root, f"{c['year']} › {c['label']}", f"{cat_slug}.html")


def shell(title, root, body, body_class, extra_head=""):
    return f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
{FONTS}
<link rel="stylesheet" href="{root}site.css">
{extra_head}</head>
<body class="{body_class}">
{body}
</body>
</html>
"""


# Python activity pages keep their own layout (style.css + copy buttons)
HEAD = """<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
<link rel="stylesheet" href="{root}style.css">
"""
SCRIPTS = """<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
<script src="{root}copy.js"></script>"""


def page(title, root, body, theme="t-turtle", crumb=""):
    inner = f"""{crumb}
<main class="shell">
{body}
</main>
<footer>Debug it. Extend it. Make it yours, then run it in Thonny.</footer>
{SCRIPTS.format(root=root)}"""
    return shell(title, root, inner, theme, HEAD.format(root=root))


def topic_band(t):
    deco = ""
    if t["theme"] == "t-turtle":
        deco = '<div class="t-blocks" aria-hidden="true"><i style="background:#d62828"></i><i style="background:#f2c230"></i><i style="background:#fff"></i><i style="background:#1d4e9e"></i></div>'
    if t["theme"] == "t-bebras":
        deco = '<div class="t-trees" aria-hidden="true"></div>'
    stamp = f'<span class="t-stamp">{e(t["stamp"])}</span>' if t.get("stamp") else ""
    return f"""<header class="t-band">{deco}<div class="t-in">{stamp}<h1>{e(t['title'])}</h1><p>{e(t['lead'])}</p></div></header>"""


def topic_row(title, tag, href, lessons):
    ext = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
    chips = ""
    if lessons:
        chips = '<div class="t-chips">' + "".join(f'<a class="t-chip" href="{href}#{h}">{e(l)}</a>' for l, h in lessons) + "</div>"
    return f"""<div class="t-row"><div class="t-head"><span><b>{e(title)}</b><span class="t-tag">{e(tag)}</span></span><a class="t-go" href="{href}"{ext}>Open</a></div>{chips}</div>"""


def build_topic(slug, t):
    crumb = f"{t['year']} › {t['title']}" if t["year"] else t["title"]
    rows = "\n".join(topic_row(*r) for r in t["rows"])
    body = f"""{bar('', crumb)}
{topic_band(t)}
<main class="cl-wrap"><div class="t-list">{rows}</div></main>"""
    return shell(f"{t['title']} · {SITE}", "", body, f"cl topic {t['theme']}")


def build_home():
    def row(label, topics, cls=""):
        btns = "".join(f'<a class="cl-topic" href="{h}"><span class="cl-sw" style="background:{c}"></span>{e(n)}</a>' for n, h, c in topics)
        return f'<div class="cl-yr{cls}"><b>{e(label)}</b><div class="cl-topics">{btns}</div></div>'
    years = "\n".join(row(y, t) for y, t in YEARS) + "\n" + row("Bebras", BEBRAS_ROW, " cl-bebras")
    body = f"""{bar('', 'Home')}
<main class="cl-wrap">
  <div style="display:grid;gap:6px"><h1>{SITE}</h1><p class="cl-lead">Find your year, then choose your topic.</p></div>
  <div class="cl-years">
{years}
  </div>
</main>"""
    return shell(SITE, "", body, "cl")


def activity_card(a):
    return f"""<a class="card" href="activities/{a['slug']}.html">
  <div class="tags">
    <span class="tag {a['kind']}">{a['kind']}</span>
    <span class="tag level">{a['level']}</span>
  </div>
  <h3>{e(a['title'])}</h3>
  <p>{e(a['summary'])}</p>
</a>"""


HOWTO = """<div class="howto">
  <div class="eyebrow">How to use these with Thonny</div>
  <ol>
    <li>Open an activity, then click <code>Copy code</code> and paste it into a new Thonny file (or click <code>Download .py</code>).</li>
    <li>Save the file into your own folder first (<code>File &rarr; Save As</code>).</li>
    <li>Press <code>F5</code> (or the green Run arrow), read the instructions on the page, and start debugging or extending.</li>
  </ol>
</div>"""


def build_category(cat_slug, cat, activities):
    t = {"title": cat["label"], "lead": cat["tagline"], "theme": cat["theme"]}
    cards = "\n".join(activity_card(a) for a in activities)
    extra = "".join(topic_row(n, tag, h, []) for n, tag, h in cat["extra"])
    body = f"""{bar('', f"{cat['year']} › {cat['label']}")}
{topic_band(t)}
<main class="shell" style="padding-top:28px">
<div class="grid">
{cards}
</div>
{('<div class="t-list" style="margin-top:22px">' + extra + '</div>') if extra else ''}
<div style="margin-top:22px">{HOWTO}</div>
</main>
<footer>Debug it. Extend it. Make it yours, then run it in Thonny.</footer>"""
    return shell(f"{cat['label']} · {SITE}", "", body, f"cl topic {cat['theme']}", HEAD.format(root=""))


def extend_block(a):
    if a.get("extend_tiers"):
        tiers_html = ""
        for tier in a["extend_tiers"]:
            tier_name = tier["tier"]
            tier_class = tier_name.lower()
            tasks_html = "\n".join(f"<li>{html.escape(t)}</li>" for t in tier["tasks"])
            tiers_html += f"""<div class="tier tier-{tier_class}">
  <div class="tier-badge">{html.escape(tier_name)}</div>
  <ul>{tasks_html}</ul>
</div>"""
        return f"""<div class="extendblock">
  <div class="eyebrow">Once it's debugged &mdash; extension tasks</div>
  <p class="extend-lead">Work through these in order &mdash; each tier builds on the last.</p>
  <div class="tiers">{tiers_html}</div>
</div>"""
    if a.get("extend_ideas"):
        items = "\n".join(f"<li>{html.escape(i)}</li>" for i in a["extend_ideas"])
        return f"""<div class="extendblock">
  <div class="eyebrow">Once it's working, try this</div>
  <ul>{items}</ul>
</div>"""
    return ""


def build_activity(a):
    root = "../"
    code_escaped_attr = html.escape(a["starter_code"], quote=True)
    code_escaped_display = html.escape(a["starter_code"])
    filename = f"{a['slug']}.py"
    cat = CATEGORIES.get(a["category"], {"label": "Library"})

    asset_block = ""
    if a.get("asset_filename"):
        asset_block = f"""<div class="assetnote">
  This activity uses a background image. <a href="../assets/{a['asset_filename']}" download>Download {a['asset_filename']}</a> and save it in the <strong>same folder</strong> as your {filename} file &mdash; the code loads it by filename, so they need to sit side by side.
</div>"""

    target_block = ""
    if a.get("target_image"):
        target_block = f"""<figure class="targetimg">
  <div class="eyebrow">Your target picture</div>
  <img src="../assets/{a['target_image']}" alt="Target picture for {html.escape(a['title'])}">
</figure>"""

    body = f"""<a class="backlink" href="../{a['category']}.html">&larr; Back to {html.escape(cat['label'])}</a>
<div class="tags" style="margin-bottom:10px;">
  <span class="tag {a['kind']}">{a['kind']}</span>
  <span class="tag level">{a['level']}</span>
</div>
<h1>{html.escape(a['title'])}</h1>
<p style="max-width:60ch;">{html.escape(a['summary'])}</p>

<div class="instructions"><div class="eyebrow">Instructions</div>{html.escape(a['instructions'])}</div>

{asset_block}

{target_block}

<div class="codepanel">
  <div class="codebar">
    <span>{filename}</span>
    <div class="actions">
      <button onclick="copyCode('src-{a['slug']}', this)">Copy code</button>
      <button onclick="downloadCode('src-{a['slug']}', '{filename}')">Download .py</button>
    </div>
  </div>
  <pre><code class="language-python">{code_escaped_display}</code></pre>
</div>
<textarea id="src-{a['slug']}" style="position:absolute; left:-9999px; top:-9999px;" readonly>{code_escaped_attr}</textarea>

{extend_block(a)}
"""
    return page(f"{a['title']} · Computing Lab", root, body, theme=CATEGORIES[a["category"]]["theme"], crumb=crumb_for(a["category"], root))



MARK_A, MARK_B = "<!--cl-frame-->", "<!--/cl-frame-->"


def add_frame(fname, crumb_text, crumb_href, extra_head):
    path = os.path.join(BASE_DIR, fname)
    if not os.path.exists(path):
        return False
    s = open(path, encoding="utf-8").read()
    s = re.sub(re.escape(MARK_A) + ".*?" + re.escape(MARK_B), "", s, flags=re.S)
    head_bits = (f'{MARK_A}<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lexend:wght@700'
                 f'&family=Atkinson+Hyperlegible:wght@400;700&family=JetBrains+Mono:wght@500&display=swap">'
                 f'<link rel="stylesheet" href="site.css">{extra_head}{MARK_B}')
    s = s.replace("</head>", head_bits + "</head>", 1)
    # always light: these pages switch to dark only when <html> has no data-theme="light"
    if 'data-theme="light"' not in s.split("<head>")[0]:
        s = re.sub(r"<html([^>]*)>", lambda m: "<html" + m.group(1) + ' data-theme="light">', s, count=1)
    s = re.sub(r"(<body[^>]*>)\n?", lambda m: m.group(1) + "\n" + MARK_A + bar("", crumb_text, crumb_href) + MARK_B, s, count=1)
    open(path, "w", encoding="utf-8").write(s)
    return True


def write(name, text):
    with open(os.path.join(BASE_DIR, name), "w", encoding="utf-8") as f:
        f.write(text)


def main():
    with open(DATA_PATH, encoding="utf-8") as f:
        activities = json.load(f)
    write("index.html", build_home())
    for slug, t in TOPICS.items():
        write(f"{slug}.html", build_topic(slug, t))
    for cat_slug, cat in CATEGORIES.items():
        write(f"{cat_slug}.html", build_category(cat_slug, cat, [a for a in activities if a["category"] == cat_slug]))
    os.makedirs(os.path.join(BASE_DIR, "activities"), exist_ok=True)
    for a in activities:
        write(os.path.join("activities", f"{a['slug']}.html"), build_activity(a))
    # old address of the student hub now goes to the home page
    write("hub.html", '<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=index.html"><title>Computing Lab</title><a href="index.html">Computing Lab</a>')
    framed = [f for f, (c, h, x) in STANDALONE.items() if add_frame(f, c, h, x)]
    print(f"Built home, {len(TOPICS)} topic pages, {len(CATEGORIES)} Python pages, {len(activities)} activities; Home bar on {len(framed)} lab/revision pages.")


if __name__ == "__main__":
    main()
