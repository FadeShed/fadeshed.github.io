<!-- lwp:meta -->
page_title: LightWebPres guide — LightWebPres
page_desc: Read, create and publish.
card_title: LightWebPres guide
card_desc: Read, create and publish.
card_label: GUIDE
nav_title: LightWebPres guide
nav_desc: Read, create and publish.
---

<!-- lwp:slide:cover -->
slug: lightwebpres
kicker: Product manual
# LightWebPres
summary: One Markdown source for reading and presenting. Start with this overview, then use the complete operational manual below.

 



---

<!-- lwp:slide -->
slug: ce-qu-il-fait
kicker: Output
## Pages that carry their runtime

 

<div class="fact-box">
<div class="fact-label">What to publish</div>
<div class="fact-content"> <p>Each article is an HTML file with its CSS and JavaScript inside. The build also derives a series index and navigation. Publish <strong>public/,</strong> including referenced images and Identity Kit assets, to a static host.</p>
<p>Readers need a browser, not Python or LightWebPres. The source remains plain text; the manual describes how to operate the tool, not an editorial method.</p></div>
</div>
<p class="source">Source : Guide, chapters 1 and 7</p>

---

<!-- lwp:slide -->
slug: trois-commandes
kicker: Start
## Two commands to see a working site

 

<div class="fact-box">
<div class="fact-label">Demo first, then your own article</div>
<div class="fact-content"> <p>Run <code>python3 lightwebpres init my-series</code>, then <code>python3 lightwebpres demo my-series --lang en</code>. <strong>Demo already builds.</strong> Open <code>my-series/public/index.html</code>.</p>
<p>Next, create <code>sources/first-page.md</code>, register its filename in <code>series.json</code> and run <code>build --lang en --open</code>. The manual supplies the complete source and JSON, followed by <code>audit</code> and <code>verify</code>. No extra build belongs before that edit.</p></div>
</div>
<p class="source">Source : Guide, chapters 1 and 2</p>

---

<!-- lwp:slide -->
slug: anatomie
kicker: Anatomy
## Four slide types, one source file

 

<div class="highlight"><span class="highlight-figure">4</span><span class="highlight-caption">cover, standard, series-nav and full-article</span></div>
<div class="fact-box">
<div class="fact-label">Fields first, body after</div>
<div class="fact-content"> <p>A cover supplies the title. A standard slide accepts text, images, tables, notes and optional named components. A series-nav slide generates links; a full-article slide includes a separate plain Markdown file.</p>
<p>Every slide declares its stable <code>slug:</code>. Fields occupy one physical line, except indented continuations of <code>note:</code> and <code>comment:</code>. Once free text starts, later field-looking lines are text too.<sup class="note-call"><a href="#note-anatomie-1" id="noteref-anatomie-1" role="doc-noteref">1</a></sup></p>
<div class="notes-local">
<ol class="note-body">
<li id="note-anatomie-1" role="doc-footnote"><span class="note-num">1</span><code>lightwebpres contract</code> exposes accepted fields and parseable skeletons. <code>note:</code> is public HTML for the speaker panel; <code>comment:</code> is source-only. Footnotes such as this one are reader-visible references, not speaker notes.<a aria-label="Back to the text" class="note-back" data-lwp-i18n-aria-label="note_back" href="#noteref-anatomie-1" role="doc-backlink">↩</a></li>
</ol>
</div></div>
</div>
<p class="source">Source : Guide, chapter 3</p>

---

<!-- lwp:slide -->
slug: tags
kicker: Series
## Order articles and inspect their visibility

 

<div class="fact-box">
<div class="fact-label">Registration and filtering are separate</div>
<div class="fact-content"> <p>The <code>articles</code> array in <code>series.json</code> fixes the index and navigation order. Only <code>page_source</code> is required per entry. <code>status</code> shows resolved metadata; <code>series tags</code> reports effective article and slide visibility without building.</p>
<p>Article tags gate the article, slide tags gate its content. Untagged slides are shared with non-default selections. <strong>L</strong> opens the reader's tag menu; <code>excluded</code> removes a slide at build time. Tags are not access control.</p></div>
</div>
<p class="source">Source : Guide, chapter 4</p>

---

<!-- lwp:slide -->
slug: identity-kits
kicker: Identity
## One identity, named presets and themes

 

<div class="fact-box">
<div class="fact-label">Inner structure, not a replacement runtime</div>
<div class="fact-content"> <p>A self-contained Identity Kit supplies layouts, chrome, assets and typed themes. LWP keeps the page shell, navigation and script. Select a preset through <code>series_meta.presentation_preset</code>: <code>builtin/standard</code>, <code>commons/id</code>, or <code>id@version/preset</code>. Omission selects native Standard with minimal Light; Commons presets bind global themes to native layouts. Identity is inferred from the reference, and its label stays fixed when the selection changes.</p>
<p>Keep alternatives at the root of <code>series.json</code> with <code>presentation_presets</code>, or pass <code>--presentation-presets</code> to <code>build</code>, <code>verify</code> or <code>watch</code>. A kit or Commons primary also adds compatible <code>builtin/standard</code> after those choices; a kit-only slide layout or chrome override makes that implicit candidate unavailable and is reported as a warning. The primary stays first; <strong>C</strong> opens Identity, Preset and Theme choices and switches the whole deck without changing its sources. The session choice is scoped to that deck as well as its catalogue. Applicable / Current identity / All filter published choices by typed compatibility or ownership, not brand. Follow preset resets an explicit runtime theme choice.</p>
<p>Use <code>preset list</code>, <code>preset show</code> and <code>series preset set</code> to inspect or change the choice. <code>init --preset</code> can also apply the kit's starter. <code>kit compose</code> builds an autonomous kit from explicit files and a complete final manifest. Per-slide <code>slide-layout</code>, <code>slide-header</code> and <code>slide-footer</code> override defaults.</p></div>
</div>
<p class="source">Source : Guide, chapter 5</p>

---

<!-- lwp:slide -->
slug: gestes
kicker: Customization
## Change the smallest layer that does the job

 

<div class="fact-box">
<div class="fact-label">Values first, advanced CSS when needed</div>
<div class="fact-content"> <p>A theme sets the base. <code>settings.conf</code> pins values for the series; <code>style.*</code> metadata changes one page; instance tags change one phrase. The compiler checks typed property names and values. <code>custom.css</code> adds unrestricted rules after the composed stylesheet.</p>
<p><code>resolve</code> explains a surprising value, including the levels that lost. <code>series theme</code> measures the effective typed colors; it does not certify arbitrary custom CSS or repair a palette.</p></div>
</div>
<p class="source">Source : Guide, chapter 5</p>

---

<!-- lwp:slide -->
slug: themes
kicker: Reading and presenting
## Keep alternatives within reach

 

<div class="fact-box">
<div class="fact-label">The same page, a different viewing choice</div>
<div class="fact-content"> <p><strong>C</strong> opens the theme picker. Monochrome, Monochrome Night and Print Ink ship by default; <code>--no-essential-theme</code> opts out. Select Print Ink before printing when you want black on white: printing keeps the active theme.</p>
<p><strong>M</strong> opens the presenter menu, <strong>F</strong> requests fullscreen, <strong>H</strong> lists the controls and <strong>S</strong> shares a link or QR code. A projected screen also shows an open speaker panel: <strong>N</strong> is not a private presenter window.</p></div>
</div>
<p class="source">Source : Guide, chapters 5 and 8</p>

---

<!-- lwp:slide -->
slug: pipeline
kicker: Automation
## One engine at the terminal or in a browser

 

<div class="fact-box">
<div class="fact-label">Build, inspect, maintain</div>
<div class="fact-content"> <p>The CLI runs unattended with Python's standard library. <code>watch</code> rebuilds on edits; <code>--only</code> targets an article when the navigation cache is safe. Language packs separate interface strings from build-time typography.</p>
<p>The browser builder runs the same executable under Pyodide: upload a series zip, or pull/build/push with GitLab. Serve the builder over HTTP(S). Sanitize untrusted input upstream: raw HTML is passed through by the engine.</p></div>
</div>
<p class="source">Source : Guide, chapters 6, 9 and 10</p>

---

<!-- lwp:slide -->
slug: verifications
kicker: Publication
## Two checks answer different questions

 

<div class="fact-box">
<div class="fact-label">Match the check to the question</div>
<div class="fact-content"> <p><code>audit</code> renders in memory and reports source and style warnings without writing output. Plain audit exits zero; <code>--strict</code> turns warnings into a gate. <code>verify</code> compares a fresh in-memory render with the files on disk and fails on drift. Use the same supported rendering options as the build.</p>
<p><strong>Inspect the rendered page before publishing.</strong> Verify cannot reproduce <code>--inline-images</code>. Removing an article does not delete an old hosted file; review <code>clean</code> locally and the host's stale files separately.</p></div>
</div>
<p class="source">Source : Guide, chapter 7</p>

---

<!-- lwp:slide -->
slug: reader-controls
## Reading, at your scale.
summary: Tap the reader menu: zoom does not require a keyboard.

Use **−**, **+** and **Reset** for presentation zoom; the percentage shows its level. Pinch remains native browser zoom. The menu also offers text fitting and local scrolling for wide tables. These choices last in the loaded page, not after reloading it. Table cells remain in the document: visual clipping does not remove their content.

---

<!-- lwp:slide:full-article -->
slug: guide-complet
article: article.md

---

<!-- lwp:slide:series-nav -->
slug: la-serie
