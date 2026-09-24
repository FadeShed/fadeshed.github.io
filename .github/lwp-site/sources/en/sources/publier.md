<!-- lwp:meta -->
page_title: Verify, then publish — LightWebPres
page_desc: The right directory, the right checks, and links that stay stable.
card_title: Verify, then publish
card_desc: The right directory, the right checks, and links that stay stable.
card_label: 05 / PUBLISH
nav_title: Verify, then publish
nav_desc: The right directory, the right checks, and links that stay stable.
---

<!-- lwp:slide:cover -->
slug: ouverture
kicker: 05 / PUBLISH
# Your files.<br>Your hosting.<br>Your address.
summary: The output is static. Readers need neither a Python engine nor an application server.

---

<!-- lwp:slide -->
slug: verifier-la-sortie
kicker: BEFORE GOING LIVE
## Audit and verify answer different questions.
summary: The first inspects sources and rendering. The second compares published files with what the engine would rebuild.
source: <a href="guide/guide.html#7-verify-and-publish">Guide · Verify and publish</a>.

```bash
python3 lightwebpres build my-series --lang en
python3 lightwebpres audit my-series --lang en --strict
python3 lightwebpres verify my-series --lang en
```

Without `--strict`, **audit can exit with code zero despite warnings**. `verify` requires the same language and rendering options as the build, including `--single-html` and `--inline-images` when used.

If your output is already tracked in Git, run `verify` **before** rebuilding so you do not erase evidence of drift.

---

<!-- lwp:slide -->
slug: deux-livraisons
kicker: CHOOSE THE DELIVERABLE
## A website or one HTML. The sources stay the same.
summary: Organizing the content and delivering the files are different choices.

**Linked pages:** publish the output directory. Readers can open an article at its own address and use the series index to choose another.

**Combined HTML:** gather the series into one file. Its embedded index lets readers switch articles deliberately; the articles are not stacked into one endless deck.

<a href="demo/index.html">Open the multipage example →</a> · <a href="downloads/publication.html" download>Get the same series in HTML ↓</a>

---

<!-- lwp:slide -->
slug: bon-dossier
kicker: WHAT GOES TO YOUR HOST
## Publish public/. Not your whole project.
summary: Keep HTML pages, referenced images and kit assets together.
source: <a href="guide/guide.html#7-verify-and-publish">Guide · Publish the output, not the project</a>.

```text
public/
  index.html
  ma-page.html
  img/
  assets/presentations/
```

The HTML can also be read locally. But a local address is not a public one: a QR code to share requires an HTTP(S) URL reachable from the recipient's device.

Removing a source does not automatically delete an old hosted file. Review what `clean` proposes and what remains on the host.

---

<!-- lwp:slide -->
slug: html-unique
kicker: A FILE TO SEND OR KEEP
## Build the file. Verify the same file.
summary: Use a separate output directory and the same options for building and verification.

```bash
python3 lightwebpres build my-series --lang en --single-html publication.html --inline-images --output shared
python3 lightwebpres verify my-series --lang en --single-html publication.html --inline-images --output shared
```

Open `shared/publication.html`. `--inline-images` embeds supported local images and resources; it is not a promise to capture every external dependency. Before sending the file, test it without a network and keep any remaining referenced resources with it.

Keep the source project too: the published HTML is a deliverable, not your editable master.

---

<!-- lwp:slide -->
slug: github-pages
kicker: THIS SITE, IN PRACTICE
## GitHub Pages receives an already-built output.
summary: The supplied workflow builds the site with the repository engine, checks the result and publishes only the generated artifact.
source: <a href="https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages">GitHub documentation · Custom workflows</a>; <a href="downloads/site-sources.zip">This site's sources and workflow</a>.

```bash
python3 tools/build_website.py
python3 tools/check_website.py generated/site
```

In the GitHub repository, select **Settings → Pages → Source → GitHub Actions**. The `.github/workflows/pages.yml` file separates verification, building and deployment; it does not create a release.

Internal paths stay relative so they work under `/lightwebpres/`, not just at a domain root.

---

<!-- lwp:slide -->
slug: limites
kicker: PUBLISH WITHOUT FALSE PROMISES
## Public means public.
summary: The format renders trusted sources. It does not sanitize HTML or turn tags into access rights.
source: <a href="reference/README.md">README · Safety and License</a>; <a href="reference/COPYING.EXCEPTION">Output Exception</a>.

`note:` notes are embedded, and the speaker panel appears on the same screen as the presentation. Tags filter views; they do not protect content.

The program is licensed under **GPL v3 or later with the Output Exception**. The exception lets you choose the distribution terms for normal presentations; the redistributed engine remains under the GPL. Keep the licence texts with the executable.

---

<!-- lwp:slide:series-nav -->
slug: continuer
