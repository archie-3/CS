# Computing Lab

My teaching website, hosted free on GitHub Pages: https://archie-3.github.io/CS/

## What's on the site

| Page | What it is |
|---|---|
| `index.html` | Home page: year groups and their topics (plus Bebras) |
| `cyber.html`, `hardware.html`, `bebras.html` | Topic pages |
| `turtle.html`, `debug.html` | Python activity topic pages |
| `activities/*.html` | One page per Python activity (copy the code into Thonny) |
| `cyber-lab.html`, `hardware-lab.html`, `wolf-vault.html`, … | Lesson labs and revision sites |

Only lesson tasks, copyable code and revision go here. No slides, plans, feedback or tests.

## The look

- `site.css`: the shared frame (the **Computing Lab** Home button on every page), the home page, the topic pages and one look per topic (`t-turtle`, `t-debug`, `t-cyber`, `t-hw`, `t-bebras`).
- `style.css`: the Python activity pages (dark code boxes, copy buttons).

## Updating the site

Edit the lists at the top of `generate_site.py` (years, topics, pages) or the activities in `activities_data.json`, then run:

```bash
python3 generate_site.py
```

It rebuilds the home page, the topic pages and the activity pages, and adds the Home bar to the lab and revision pages. Then commit and push (or upload the changed files on github.com).

New websites are tried out as Claude prototypes first, then added here once they have been tested in a lesson.
