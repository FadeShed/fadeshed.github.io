<!-- lwp:meta -->
page_title: Choose how to create — LightWebPres
page_desc: Browser, external agent or editor and command line: choose the path that suits your task.
card_title: Choose how to create
card_desc: Browser, external agent or editor and command line: choose the path that suits your task.
card_label: 03 / CREATE
nav_title: Choose how to create
nav_desc: Browser, external agent or editor and command line: choose the path that suits your task.
---

<!-- lwp:slide:cover -->
slug: ouverture
# Start where<br>you work.
summary: Browser, external agent or editor and command line: choose the path that suits your task.



---

<!-- lwp:slide -->
slug: navigateur
## Build in your browser.
summary: Start with a source project. Take away a folder of pages.

Download the example project, open the browser builder and select its ZIP. Choose the output language and build. The generated archive contains the pages to open or publish. ZIP builds run in this tab; there is no source upload to a build service. This is a builder, not a WYSIWYG editor: to change the text, edit the source files before rebuilding.

<div class="lwp-web-actions"><a class="lwp-web-button" href="web/">Open the browser builder →</a></div><div class="lwp-web-actions"><a class="lwp-web-button" href="downloads/library-project.zip">Get the example sources →</a></div>

---

<!-- lwp:slide -->
slug: agent
## Write yourself. Or work with an agent.
summary: The same editable files connect all three authoring paths.

You can write the article yourself, guide an external agent through revisions, or delegate a bounded task. Give the agent the format skill, allowed files and expected checks. Review its content and inspect the generated page before publishing. LightWebPres supplies the format and renderer, not the agent or its research.

<div class="lwp-web-actions"><a class="lwp-web-button" href="ressources.html#skills">Open the agent resources →</a></div>

---

<!-- lwp:slide -->
slug: terminal
## Your editor. Your automation.
summary: The command line is there when it is the right tool.

For local authoring, repeatable builds or integration with scripts, use the standalone Python executable. The following steps create a working starter; the writing and publishing chapters explain how to maintain it.

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
slug: navigateur-details
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
