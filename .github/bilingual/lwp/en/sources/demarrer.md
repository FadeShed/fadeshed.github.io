<!-- lwp:meta -->
page_title: Your first page — LightWebPres
page_desc: Two commands to explore. A complete example to get started.
card_title: Your first page
card_desc: Two commands to explore. A complete example to get started.
card_label: 02 / GET STARTED
nav_title: Your first page
nav_desc: Two commands to explore. A complete example to get started.
---

<!-- lwp:slide:cover -->
slug: ouverture
kicker: 02 / GET STARTED
# Two commands.<br>And something<br>to show.
summary: Python 3.8 or later is enough for the command line. No additional Python packages are required.

---

<!-- lwp:slide -->
slug: installer
kicker: 01 / GET THE ENGINE
## One Python file, not a toolchain.
summary: Download an archive from GitHub releases, then extract the lightwebpres file.
source: <a href="reference/README.md">README · Quickstart</a>; <a href="reference/CHANGELOG.md">Repository changelog</a>.

<div class="lwp-web-actions"><a class="lwp-web-button" href="https://github.com/Fade78/lightwebpres/releases">Browse releases ↗</a><a href="downloads/lightwebpres-cli.zip" download>Engine used by this site ↓</a></div>

The local download contains this site's exact engine and its licences. Its `VERSION.txt` file records the version and status from the changelog; it does not claim to be the latest published release.

On Windows, replace `python3` with `python` or `py`.

---

<!-- lwp:slide -->
slug: deux-commandes
kicker: 02 / BUILD THE DEMO
## One directory. Three articles. Ready to open.
summary: Run these commands from the directory containing the lightwebpres file.
source: <a href="reference/README.md">README · Quickstart</a>.

```bash
python3 lightwebpres init my-series
python3 lightwebpres demo my-series --lang en
```

Then open **my-series/public/index.html** in your browser.

`demo` creates the examples **and builds them**. No local server is needed to read this HTML. The command refuses to overwrite existing work.

---

<!-- lwp:slide -->
slug: votre-texte
kicker: 03 / REPLACE THE EXAMPLE
## The starting point is a complete project.
summary: The archive below contains ma-page.md, series.json, the engine and its licences. Not a fragment you have to guess around.
source: <a href="reference/GUIDE.md">Guide · First personal article</a>; <a href="downloads/demarrage.zip">This site's starter project</a>.

<div class="lwp-web-actions"><a class="lwp-web-button" href="downloads/demarrage.zip" download>Download the project ↓</a><a href="demo/ma-page.html">Open its output →</a></div>

Extract the archive, enter the `demarrage` directory, then edit `sources/ma-page.md`. To build your version:

```bash
python3 lightwebpres build . --lang en
```

Open **public/index.html**. Articles are declared and ordered in `series.json`.

---

<!-- lwp:slide -->
slug: verifier
kicker: 04 / CLOSE THE LOOP
## Building is not a substitute for checking.
summary: Audit reports source and rendering problems. Verify compares the pages with their sources.
source: <a href="guide/guide.html#7-verify-and-publish">Guide · Verify and publish</a>.

```bash
python3 lightwebpres audit . --lang en --strict
python3 lightwebpres verify . --lang en
```

Keep the same language and rendering options for building and verification. Read the pages too: valid source is not a guarantee of readability.

<div class="lwp-web-actions"><a href="ecrire.html">Understand the format →</a><a href="publier.html">Prepare to publish →</a></div>

---

<!-- lwp:slide -->
slug: navigateur
kicker: THE OTHER WAY IN
## No terminal? Build in the tab.
summary: The web builder runs the same Python engine under Pyodide. Drop the project ZIP, get a ZIP of its pages.
source: <a href="guide/guide.html#9-build-in-the-browser">Guide · Build in the browser</a>.

<div class="lwp-web-actions"><a class="lwp-web-button" href="web/index.html">Open the web builder ↗</a></div>

The builder must be served over **HTTP(S)**; double-clicking its HTML does not work. It loads its local Pyodide files when opened. A ZIP build stays in the tab; GitLab synchronization contacts the configured instance.

This builder is not the separate `lightwebpres-gui` project.

---

<!-- lwp:slide:series-nav -->
slug: continuer
