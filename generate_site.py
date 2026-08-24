"""
Generates the static PyActivities site from activities_data.json.

Run this locally whenever you add/edit an activity in activities_data.json:
    python3 generate_site.py

It's a convenience — you can also just duplicate and hand-edit one of the
generated activities/*.html files directly (including right in GitHub's
web editor) without ever running this script. Both approaches produce
plain static files; nothing here needs a server.
"""
import json
import html
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "activities_data.json")

# Add a new category here and give some activities that "category" value
# in activities_data.json — a page for it is generated automatically.
CATEGORIES = {
    "turtle": {
        "label": "Python Turtle",
        "tagline": "Turtle graphics activities — draw, debug, and build with turtle.",
    },
    "debug": {
        "label": "Debug Activities",
        "tagline": "Short programs with a bug hiding in them — find it, fix it, then extend it.",
    },
}

HEAD = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
<link rel="stylesheet" href="{root}style.css">"""

SCRIPTS = """<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
<script src="{root}copy.js"></script>"""


def topbar(root):
    return f"""<div class="topbar"><div class="shell">
  <a class="brand" href="{root}index.html"><span class="dot"></span> PyActivities</a>
  <a class="pill" href="{root}index.html">Categories</a>
</div></div>"""


def footer():
    return '<footer>Debug it. Extend it. Make it yours &mdash; then run it in Thonny.</footer>'


def page(title, root, body):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
{HEAD.format(root=root)}
</head>
<body>
{topbar(root)}
<main class="shell">
{body}
</main>
{footer()}
{SCRIPTS.format(root=root)}
</body>
</html>"""


def activity_card(a):
    return f"""<a class="card" href="activities/{a['slug']}.html">
  <div class="tags">
    <span class="tag {a['kind']}">{a['kind']}</span>
    <span class="tag level">{a['level']}</span>
  </div>
  <h3>{html.escape(a['title'])}</h3>
  <p>{html.escape(a['summary'])}</p>
</a>"""


def category_card(cat_slug, cat, count):
    return f"""<a class="card catcard" href="{cat_slug}.html">
  <div class="eyebrow">{count} activit{'y' if count == 1 else 'ies'}</div>
  <h3>{html.escape(cat['label'])}</h3>
  <p>{html.escape(cat['tagline'])}</p>
  <span class="catcard-go">Browse &rarr;</span>
</a>"""


def build_index(activities):
    counts = {}
    for a in activities:
        counts[a["category"]] = counts.get(a["category"], 0) + 1

    cards = "\n".join(
        category_card(slug, cat, counts.get(slug, 0))
        for slug, cat in CATEGORIES.items()
    )
    body = f"""<section class="hero">
  <div class="eyebrow">// debug it. extend it. make it yours.</div>
  <h1>Python activities to copy into Thonny and take apart.</h1>
  <p>Pick a category below. Each activity starts out slightly wrong or slightly incomplete &mdash; copy or download the code, open it in Thonny, and get it working, then push it further.</p>
</section>

<div class="howto">
  <div class="eyebrow">How to use these with Thonny</div>
  <ol>
    <li>Don't have Thonny yet? Install it free from <a href="https://thonny.org" target="_blank" rel="noopener">thonny.org</a>.</li>
    <li>Open an activity, then either click <code>Copy code</code> and paste it into a new Thonny file, or click <code>Download .py</code> and open that file in Thonny directly.</li>
    <li>In Thonny, save the file into your own folder first (<code>File &rarr; Save As</code>) so you're editing your own copy, not the original.</li>
    <li>Press <code>F5</code> (or the green Run arrow) to run it, read the instructions on the page, and start debugging or extending.</li>
  </ol>
</div>

<div class="section-head">
  <h2>Categories</h2>
</div>
<div class="grid">
{cards}
</div>"""
    return page("PyActivities — debug and extend Python", "", body)


def build_category(cat_slug, cat, activities):
    cards = "\n".join(activity_card(a) for a in activities)
    body = f"""<a class="backlink" href="index.html">&larr; All categories</a>
<div class="section-head">
  <div>
    <div class="eyebrow">Category</div>
    <h1 style="margin-bottom:.15em;">{html.escape(cat['label'])}</h1>
    <p style="margin:0;">{html.escape(cat['tagline'])}</p>
  </div>
  <span class="eyebrow">{len(activities)} activities</span>
</div>
<div class="grid">
{cards}
</div>"""
    return page(f"{cat['label']} — PyActivities", "", body)


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

    body = f"""<a class="backlink" href="../{a['category']}.html">&larr; Back to {html.escape(cat['label'])}</a>
<div class="tags" style="margin-bottom:10px;">
  <span class="tag {a['kind']}">{a['kind']}</span>
  <span class="tag level">{a['level']}</span>
</div>
<h1>{html.escape(a['title'])}</h1>
<p style="max-width:60ch;">{html.escape(a['summary'])}</p>

<div class="instructions"><div class="eyebrow">Instructions</div>{html.escape(a['instructions'])}</div>

{asset_block}

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
    return page(f"{a['title']} — PyActivities", root, body)


def main():
    with open(DATA_PATH) as f:
        activities = json.load(f)

    with open(os.path.join(BASE_DIR, "index.html"), "w") as f:
        f.write(build_index(activities))

    for cat_slug, cat in CATEGORIES.items():
        cat_activities = [a for a in activities if a["category"] == cat_slug]
        with open(os.path.join(BASE_DIR, f"{cat_slug}.html"), "w") as f:
            f.write(build_category(cat_slug, cat, cat_activities))

    act_dir = os.path.join(BASE_DIR, "activities")
    os.makedirs(act_dir, exist_ok=True)
    for a in activities:
        with open(os.path.join(act_dir, f"{a['slug']}.html"), "w") as f:
            f.write(build_activity(a))

    print(f"Generated index.html, {len(CATEGORIES)} category pages, and {len(activities)} activity pages.")


if __name__ == "__main__":
    main()
