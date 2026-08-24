# PyActivities (static site)

A plain webpage listing your Python activities. Students open an
activity, read the instructions, copy or download the code, and run it
locally in **Thonny** — nothing to install on your end beyond putting
these files somewhere public, and nothing to install on the students'
end beyond Thonny itself.

There's no server, no accounts, no database — just HTML, CSS, and a
little JS for the Copy/Download buttons.

## Put it on GitHub Pages (free, ~5 minutes)

1. Create a new GitHub repository and upload everything in this folder
   to it (drag-and-drop works fine on github.com, or `git push` if you're
   comfortable with that).
2. In the repo, go to **Settings → Pages**.
3. Under **Source**, choose **Deploy from a branch**, pick the `main`
   branch and the `/ (root)` folder, then **Save**.
4. GitHub gives you a URL like `https://yourusername.github.io/your-repo/`
   within a minute or two — that's what you share with students.

That's the whole deployment. No build step, no environment variables, no
server to keep running.

## Adding a new activity

You don't need to run anything on your computer to do this — you can
edit files directly on github.com if you'd rather not use a text editor.

**Easiest way:** duplicate an existing page in `activities/` (e.g. copy
`activities/ukraine-flag.html` to `activities/my-new-activity.html`),
then edit the title, tags, instructions, and the code inside the
`<pre><code>` block **and** inside the hidden `<textarea>` right below it
(both need to have the same code — the visible block is what students
read, the textarea is what the Copy/Download buttons actually use). Then
add a matching card link to it on `index.html`.

**If you're comfortable running a script:** edit `activities_data.json`
(add a new entry with `slug`, `title`, `kind`, `level`, `summary`,
`instructions`, `starter_code`, and optionally `asset_filename`), then
run:

```bash
python3 generate_site.py
```

This regenerates `index.html` and every page in `activities/` from that
one JSON file — much less error-prone than hand-editing HTML once you
have more than a few activities. Either approach is fine; use whichever
you're more comfortable with.

## Activities that use an image (like the Envelope Challenge)

If an activity's code loads a background image (`screen.bgpic(...)`),
its page shows a note with a download link for that image. Make sure
students save the image in the **same folder** as their `.py` file
before running it in Thonny — `bgpic()` looks for the file by name in
the current working directory.

## Files

```
index.html              Library page
activities/*.html       One page per activity
assets/                 Images used by activities (e.g. envelopebg.png)
style.css               Shared styles
copy.js                 Copy-to-clipboard / download-as-.py buttons
activities_data.json    Source data (used by generate_site.py)
generate_site.py        Optional: regenerates the HTML from the JSON
```
