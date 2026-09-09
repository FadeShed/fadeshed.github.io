<section id="reader-controls-detail"><h2>Touch reader controls</h2><p>The reader menu provides zoom − / + / Reset, the current percentage, text fitting and local table scrolling. These controls do not require a keyboard. Pinch belongs to the browser. Reading choices belong to the currently loaded page.</p></section> 
<h1>LightWebPres — Guide</h1>
<p>The operational manual for LightWebPres: create a series, add your content, configure its presentation, check the output and publish it. It covers the terminal and browser tools, not editorial craft. For exact parser rules use the <a href="https://github.com/Fade78/lightwebpres/blob/main/agent/skills/lightwebpres/SKILL.md">format reference</a>; for normative contracts use <a href="https://github.com/Fade78/lightwebpres/blob/main/specifications.md">specifications.md</a> (French).</p>
<ol>
<li><a href="#1-start-with-a-working-site" onclick="document.getElementById(this.hash.slice(1)).focus(); document.activeElement.scrollIntoView({behavior: 'instant'}); return false;">Start with a working site</a></li>
<li><a href="#2-make-your-first-personal-article" onclick="document.getElementById(this.hash.slice(1)).focus(); document.activeElement.scrollIntoView({behavior: 'instant'}); return false;">Make your first personal article</a></li>
<li><a href="#3-understand-page-anatomy" onclick="document.getElementById(this.hash.slice(1)).focus(); document.activeElement.scrollIntoView({behavior: 'instant'}); return false;">Understand page anatomy</a></li>
<li><a href="#4-organize-a-series-and-tags" onclick="document.getElementById(this.hash.slice(1)).focus(); document.activeElement.scrollIntoView({behavior: 'instant'}); return false;">Organize a series and tags</a></li>
<li><a href="#5-choose-presets-themes-and-customization" onclick="document.getElementById(this.hash.slice(1)).focus(); document.activeElement.scrollIntoView({behavior: 'instant'}); return false;">Choose presets, themes and customization</a></li>
<li><a href="#6-set-languages-and-typography" onclick="document.getElementById(this.hash.slice(1)).focus(); document.activeElement.scrollIntoView({behavior: 'instant'}); return false;">Set languages and typography</a></li>
<li><a href="#7-verify-and-publish" onclick="document.getElementById(this.hash.slice(1)).focus(); document.activeElement.scrollIntoView({behavior: 'instant'}); return false;">Verify and publish</a></li>
<li><a href="#8-present-print-and-share" onclick="document.getElementById(this.hash.slice(1)).focus(); document.activeElement.scrollIntoView({behavior: 'instant'}); return false;">Present, print and share</a></li>
<li><a href="#9-build-in-the-browser" onclick="document.getElementById(this.hash.slice(1)).focus(); document.activeElement.scrollIntoView({behavior: 'instant'}); return false;">Build in the browser</a></li>
<li><a href="#10-automate-and-maintain" onclick="document.getElementById(this.hash.slice(1)).focus(); document.activeElement.scrollIntoView({behavior: 'instant'}); return false;">Automate and maintain</a></li>
<li><a href="#11-troubleshooting-and-references" onclick="document.getElementById(this.hash.slice(1)).focus(); document.activeElement.scrollIntoView({behavior: 'instant'}); return false;">Troubleshooting and references</a></li>
</ol>
<h2 id="1-start-with-a-working-site" tabindex="-1">1. Start with a working site</h2>
<p>Follow the <a href="https://github.com/Fade78/lightwebpres/blob/main/README.md#quickstart">README quickstart</a> to acquire the single executable and run <code>init</code> then <code>demo</code>. You need Python 3.8+ with its standard library, no additional packages. <code>demo</code> already builds the site; do not run <code>build</code> again until you change something. Open <code>my-series/public/index.html</code>.</p>
<p>Commands in this guide run from the directory containing <code>lightwebpres</code> and <code>my-series/</code>. On Windows, use <code>python lightwebpres</code> (or <code>py lightwebpres</code>). Examples using <code>./lightwebpres</code> assume Unix and <code>chmod +x lightwebpres</code>; <code>python3 lightwebpres</code> works without the executable bit.</p>
<p><code>init</code> scaffolds a working project — <code>sources/</code> (empty, for your <code>.md</code> files), <code>templates/</code> (your customization surface: <code>settings.conf</code> and <code>custom.css</code>, plus optional versioned <code>themes/*.conf</code>, see section 5), empty <code>interface/</code>, <code>typography/</code> and legacy <code>language/</code> directories, an empty <code>public/</code> for the build to write into, a starter <code>series.json</code>, and a copy of the <code>lightwebpres</code> executable itself with its <code>COPYING</code> and <code>COPYING.EXCEPTION</code> beside it, so the project directory is self-sufficient and the copy travels with its licence.</p>
<p>The navigation script and built-in language packs stay inside the executable so upgrades reach the series without refreshing local copies. For deliberate overrides, use <code>template show</code>/<code>template write</code> (section 10). <code>init --preset</code> can also install an Identity Kit and its declared starter (section 5).</p>
<p>The quickstart uses <code>--lang en</code> explicitly. Without it or <code>LWP_LANG</code>, the browser chooses the interface language; typography is already fixed at build time. Section 6 explains the two layers and custom packs.</p>
<p><code>demo</code> only works after <code>init</code> and refuses to overwrite existing work. It drops three example articles (first, middle and last position in the navigation) plus a captioned image, so you have something real to look at before writing your own.</p>
<p>With <code>demo --dry-run</code>, the files and build are only journaled as a plan; the existing on-disk series is not built in place of the planned demo.</p>
<p><code>build</code> reads <code>series.json</code> and every article it lists, and writes <code>public/*.html</code> plus <code>public/index.html</code>. A generated <code>README.md</code> lands beside <code>series.json</code>, at the root of the series rather than in <code>public/</code> — it describes the series to whoever opens the repository, not to whoever visits the site. Open the index locally; no server is needed. Referenced images are separate assets by default. The publication chapter covers single-file delivery, output switches and cleanup; start by adding your own article below.</p>
<h2 id="2-make-your-first-personal-article" tabindex="-1">2. Make your first personal article</h2>
<p>Keep the demo as a reference and add one article beside it. The following small example describes the output files, so it needs no external image or second Markdown file. Its tracked source also produces this manual's captures: <a href="https://github.com/Fade78/lightwebpres/blob/main/examples/first-article/sources/first-page.md">examples/first-article/sources/first-page.md</a>.</p>
<h3>Create the source</h3>
<p>Create <code>my-series/sources/first-page.md</code> in your editor with this content:</p>
<pre><code class="language-markdown">
&lt;!-- lwp:meta --&gt;
page_title: My first page
---

&lt;!-- lwp:slide:cover --&gt;
slug: first-page
kicker: Getting started
# My first page
summary: A small site I can read, present and share.

---

&lt;!-- lwp:slide --&gt;
slug: travels-with-the-page
kicker: Portable output
## The runtime travels with the page
summary: Open the HTML without installing LightWebPres.
highlight: 1 HTML
highlight-caption: per article, with CSS and JavaScript inside
fact-label: Keep the assets too

Local images stay beside the page in **img/**.
Publish the whole **public/** directory, not just its index.

---

&lt;!-- lwp:slide:series-nav --&gt;
slug: explore-the-series
  </code></pre>
<h3>Register it in the series</h3>
<p>Open <code>my-series/series.json</code>. Append this object to its existing <code>articles</code> array, adding a comma after the preceding object:</p>
<pre><code class="language-json">
{"page_source": "first-page.md"}
  </code></pre>
<p>Keep the demo entries and <code>series_meta</code>; do not replace the whole file with that one object. Only a bare filename belongs in <code>page_source</code>, not <code>sources/first-page.md</code>. The array order is the index and navigation order.</p>
<p>For a series containing <strong>only</strong> your article, this is a complete alternative <code>series.json</code> (the unused demo sources can stay on disk):</p>
<pre><code class="language-json">
{
  "series_meta": {"title": "My first series"},
  "articles": [{"page_source": "first-page.md"}]
}
  </code></pre>
<h3>Build, open and verify</h3>
<pre><code class="language-bash">
python3 lightwebpres build my-series --lang en --open
python3 lightwebpres audit my-series --lang en
python3 lightwebpres verify my-series --lang en
  </code></pre>
<p>If automatic opening is unavailable, open <code>my-series/public/index.html</code> manually, then select <strong>My first page</strong>. Its direct file is <code>my-series/public/first-page.html</code>; the content card is <code>first-page.html#travels-with-the-page</code>. Check the title, the content card and the links to the demo articles. <code>audit</code> reports warnings; read them even when its exit code is zero. <code>verify</code> should report no drift after this build.</p>
<p>Edit the title or body and repeat this loop. Keep each published <code>slug:</code> stable: changing a title does not change its address. Once you no longer want the demo in the site, remove its entries from <code>articles</code>, build again, then review <code>clean</code> before removing old output (section 7).</p>
<p>The same content card, built with the <code>nebula</code> theme, in two browser viewports. This is a Chromium comparison, not a photograph of a device:</p>
<p align="center">
<img alt="The same Nebula content card shown in real landscape and emulated portrait browser viewports" src="img/product-responsive.png" width="100%"/>
</p>
<h2 id="3-understand-page-anatomy" tabindex="-1">3. Understand page anatomy</h2>
<p>A page is a sequence of <strong>slides</strong>, separated by <code>---</code>, preceded by one metadata block. There are four slide types, and inside a standard slide a small set of named components. This section names them and says how you reach each one; <code>agent/skills/lightwebpres/SKILL.md</code> carries the exact syntax and every edge case.</p>
<p><strong>The four slide types.</strong></p>
<table class="comparison-table">
<thead>
<tr>
<th>Type</th>
<th>Carries</th>
<th>How many</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>cover</code></td>
<td><code>slug</code>, <code>kicker</code>, <code>tags:</code>, <code># Title</code>, <code>summary</code>, <code>slide-layout</code>, <code>slide-header</code>, <code>slide-footer</code>, <code>comment</code>, <code>note</code></td>
<td>any number, anywhere — it is a look, not a structural marker</td>
</tr>
<tr>
<td>standard <em>(the default)</em></td>
<td><code>slug</code>, <code>kicker</code>, <code>tags:</code>, <code>## Title</code>, <code>summary</code>, <code>highlight</code>, <code>highlight-caption</code>, <code>fact-label</code>, <code>fact-variant</code>, <code>source</code>, <code>slide-layout</code>, <code>slide-header</code>, <code>slide-footer</code>, <code>comment</code>, <code>note</code>, then free Markdown</td>
<td>as many as you want</td>
</tr>
<tr>
<td><code>series-nav</code></td>
<td><code>slug</code>, <code>tags:</code>, <code>slide-layout</code>, <code>slide-header</code>, <code>slide-footer</code>, <code>comment:</code> — the navigation itself is generated from <code>series.json</code></td>
<td>0 or 1 per article</td>
</tr>
<tr>
<td><code>full-article</code></td>
<td><code>slug</code>, <code>article: filename.md</code>, <code>tags:</code>, <code>slide-layout</code>, <code>slide-header</code>, <code>slide-footer</code> and <code>comment:</code></td>
<td>any number, each with its own file</td>
</tr>
</tbody>
</table>
<p>Four, and only four. Mistype one — <code>&lt;!-- lwp:slide:covre --&gt;</code> — and the build stops and tells you which slide, what you wrote, and what the four names are. You will not find out from the page.</p>
<p><strong>The components inside a standard slide.</strong></p>
<table class="comparison-table">
<thead>
<tr>
<th>Component</th>
<th>What it is for</th>
<th>How you reach it</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>fact box</strong></td>
<td>the slide's claim, set off from the page</td>
<td>free Markdown text after a <code>fact-label:</code> line</td>
</tr>
<tr>
<td><strong>key figure</strong></td>
<td>one number that carries the slide</td>
<td><code>highlight:</code> (+ optional <code>highlight-caption:</code>)</td>
</tr>
<tr>
<td><strong>source</strong></td>
<td>where the claim comes from</td>
<td><code>source:</code></td>
</tr>
<tr>
<td><strong>comparison table</strong></td>
<td>a grid of verdicts read at a glance</td>
<td>a Markdown table; cells take <code>yes</code> / <code>no</code> / <code>partial</code> classes via inline HTML</td>
</tr>
<tr>
<td><strong>figure</strong></td>
<td>a captioned image</td>
<td><code>![alt](img/x.png "Caption")</code> alone on its line; add <code>{50%}</code> for general image zoom or <code>{width=50% align=right}</code> for the extended format</td>
</tr>
<tr>
<td><strong>headings</strong></td>
<td>structure within the fact-box body</td>
<td><code>#</code> <code>##</code> <code>###</code> <code>####</code> <code>#####</code> <code>######</code> — up to level 6; <code>#</code>–<code>###</code> are true headings, <code>####</code> renders as a bold-font paragraph (not <code>&lt;strong&gt;</code> emphasis), <code>#####</code>/<code>######</code> as plain paragraphs</td>
</tr>
<tr>
<td><strong>quote, code, list</strong></td>
<td>ordinary prose furniture</td>
<td>ordinary Markdown</td>
</tr>
<tr>
<td><strong>note</strong></td>
<td>a reference the reader can reach</td>
<td><code>[^label]</code> in the text, <code>[^label]: body</code> on its own line</td>
</tr>
<tr>
<td><strong>long-form article</strong></td>
<td>the piece the cards summarise</td>
<td>a <code>full-article</code> slide pointing at a second <code>.md</code> file</td>
</tr>
</tbody>
</table>
<p>Keep these parser boundaries in mind:</p>
<ul>
<li><strong>Images have a short and an extended display suffix.</strong> Put <code>{50%}</code> after the image for general image zoom, or use validated pairs such as <code>{width=50% height=auto align=right}</code>. <code>width</code> and <code>height</code> accept safe CSS lengths; <code>zoom</code> accepts a percentage; <code>align</code> is for standalone figures. An inline image can use the size values but not <code>align</code>.</li>
<li><strong>The switch from fields to free text is one-way, within a slide.</strong> Once a line is not a <code>field:</code> line, everything after it is prose — so a <code>highlight:</code> placed after a paragraph is published as the literal text <code>highlight: 3 000 W</code>. Fields first, prose after.</li>
<li>Structural fields occupy one physical line, except <code>note:</code> and <code>comment:</code>: an indented continuation line belongs to the preceding note/review field.</li>
<li><strong>A field is a value, not Markdown.</strong> <code>summary: un **gras**</code> publishes the asterisks. The border is not where you would guess, either: a field passes raw HTML straight through, so finding that <code>&lt;br&gt;</code> works there says nothing about <code>**</code>. <code>audit</code> names fields carrying Markdown markup that they will not render.</li>
<li><strong>A fact box appears only with <code>fact-label:</code>.</strong> Free text without it renders as plain paragraphs — which is often what you want.</li>
</ul>
<p><strong>Notes.</strong> <code>[^label]</code> calls a note, <code>[^label]: text</code> on its own line is its body. The label is a key, and a valid one is never displayed — the reader sees a position — so you never renumber when you insert one. Valid means word characters only: letters, digits and <code>_</code>, accents and non-Latin scripts included, but no <code>-</code>, no space, no punctuation. A label outside that is neither a note nor an error: the call ships as literal text, the body renders as an ordinary paragraph, and the label is the one thing on the page the reader was never meant to see. By default a body lands at the foot of the unit that called it (the card, or the end of the long-form article) and numbering restarts in each card, because a card is shareable on its own and a reader may arrive at it having read nothing else. <code>notes_placement: page</code> in the meta block instead collects every body into one notes section at the end of the page; <code>notes_tooltip: on</code> additionally puts the text on the call. <code>audit</code> names a label outside the pattern, a call with no body, a body nothing calls, and a body written inside a raw HTML block (where it ships as literal text).</p>
<p>Both note settings can be set in <code>series_meta</code>; article metadata wins over that series default. The built-in defaults are <code>notes_placement: local</code> and <code>notes_tooltip: off</code>. Calls and note bodies link in both directions.</p>
<p><strong>What a card's link is.</strong> Every card has its own address — <code>article.html#barrage-de-vajont</code> — and the share button in the corner copies it, or shows it as a QR code you can point a phone at or print. The share action is on the index too, where slide scope is disabled: there is no slide to share, and the series scope already names the page you are on. That address is the <code>slug:</code> line you write on the card, and nothing else: it is not the card's position and not its title, so you can reorder the deck, insert a card, rewrite a heading, or drop a card with <code>tags: excluded</code>, and the links you have already given out still land where they did.</p>
<p><code>slug:</code> is required. A card without one stops the build, which names the command that fixes it in one pass: <code>lightwebpres series slug set</code> writes a slug into every card that has none. It is the only command that edits your articles — a build never rewrites its own inputs — and what it writes is a random eight-character name, because a name derived from the title would look as though it still followed the title. Rename it to something readable before you publish: <code>slug: barrage-de-vajont</code> is worth more than <code>slug: 3f7c1a9e</code>, and the value is the identity from then on.</p>
<p>Two cards on one slug is a build error, not a <code>-2</code> appended in silence. <code>slug_prefix:</code> in the meta block (or in <code>series_meta</code>) puts a namespace in front of every address on the page, which is what a series whose pages reuse card names (<code>intro</code>, <code>sources</code>) needs.</p>
<p><code>lightwebpres series slug</code> lists every card of the series and the name it is published under, without building anything.</p>
<p>Register every article that should appear in navigation in <code>series.json</code> — next section.</p>
<p><code>comment:</code> is a source-only review field, accepted on every slide and in article/series metadata. It is never published, not even in the HTML source. <code>note:</code> is different: on a cover or standard slide it is embedded in the HTML for the speaker panel (section 8). Both support indented continuation lines.</p>
<p>For editor or agent integrations, <code>lightwebpres contract --format text</code> describes the versioned <code>lightwebpres.slide-draft/1</code> contract: accepted and required fields, cardinalities, source order, empty-value rules, reserved IDs and parseable skeletons. JSON is the default. <code>--article first-page.md</code> avoids slugs already declared in that source. It writes nothing.</p>
<p>A <code>full-article</code> slide needs <code>article: filename.md</code>, pointing to a separate plain Markdown file under <code>sources/</code>, with no LWP metadata or slide markers. Omitting <code>article:</code> is fatal; an explicitly empty <code>article:</code> warns and omits that unfinished slide. A non-empty reference to a missing file is fatal.</p>
<p>Markdown supports lists, tables, blockquotes, inline/fenced code and raw HTML. A linked standalone image, <code>[![alt](img/x.png "Caption")](https://example.org)</code>, keeps its caption outside the link; a mid-sentence image stays inline and its title is a tooltip. Relative Markdown links are not converted: use raw <code>&lt;a href="other.html"&gt;Other page&lt;/a&gt;</code> for local links. Headings at levels 4-6 render as paragraphs, not semantic headings. See the format reference for converter limits; this is not a general CommonMark implementation.</p>
<p>For comparison tables, wrap a cell value in <code>&lt;span class="yes"&gt;Yes&lt;/span&gt;</code>, <code>no</code> or <code>partial</code> to add a verdict treatment with a shape marker, not color alone. A <code>col-signal</code> class on a header emphasizes its column; that requires a raw HTML table because Markdown cannot attach a class to a header cell.</p>
<h2 id="4-organize-a-series-and-tags" tabindex="-1">4. Organize a series and tags</h2>
<h3>Variants in one article</h3>
<p><code>tags:</code> is a slide header field, not an instance styling tag. Its value is a space-separated list of case-insensitive variant names. Unicode letters, digits, <code>-</code>, and <code>_</code> are allowed, except that a name cannot start with <code>_</code>. The field is one physical line, like every structural field.</p>
<ul>
<li>No <code>tags:</code> (or an empty value) means <code>default</code>, the shared content.</li>
<li><code>tags: excluded</code> removes the slide during the build; it is never emitted.</li>
<li>Other tags are written to the section's <code>data-tags</code> attribute and filtered in the browser.</li>
<li>Press <strong>L</strong> to open the variant menu. It is hidden for a single-variant article and persists the choice in <code>localStorage['lwp-active-tag']</code>.</li>
<li>The selected tag shows its own slides and shared <code>default</code> slides; counts, navigation, anchors, and the presenter panel use the visible slides.</li>
</ul>
<p><code>tag:</code> is not a field, and not an alias for one. Use <code>kicker:</code> for the label above a slide title, and <code>tags:</code> for variant filtering. A <code>tag:</code> line becomes body text on a standard slide; on a cover, <code>build</code> reports the unknown field and prints the two choices.</p>
<p>For language-specific typography, map tags to packs in <code>series_meta</code>:</p>
<pre><code class="language-json">
{
  "series_meta": {
    "lang_tags": {"fr": "fr", "en": "en"}
  },
  "articles": [{"page_source": "guide.md"}]
}
  </code></pre>
<p>The first mapped language tag on a slide selects its typography pack. A slide without a mapped language tag uses the build's <code>--lang</code>/<code>LWP_LANG</code> fallback. The built-in <code>fr</code> and <code>en</code> packs come from the executable; another pack name refers to <code>typography/&lt;name&gt;.json</code>, or to the legacy <code>language/&lt;name&gt;.json</code>, in your series. The browser locale does not change this typography choice. <code>audit</code> reports invalid tags and missing packs without blocking, while <code>build</code> rejects malformed declarations.</p>
<h3>Register articles and inspect resolved metadata</h3>
<p><code>series.json</code> lists the articles and holds series-wide metadata:</p>
<pre><code class="language-json">
{
  "series_meta": {
    "title": "My article series",
    "subtitle": "Series subtitle",
    "intro": "Series introduction.",
    "scroll_duration": 200,
    "lang_tags": {"fr": "fr", "en": "en"}
  },
  "themes": ["essential", "family:terrain"],
  "articles": [
    {"page_source": "apple-pie.md"}
  ]
}
  </code></pre>
<p><code>page_source</code> — a bare filename, no path — is the only field ever required here. Each article is self-described: <code>page_dest</code> (the output HTML name), <code>page_title</code>/<code>page_desc</code>, <code>card_title</code>/<code>card_desc</code>/ <code>card_label</code>, <code>nav_title</code>/<code>nav_desc</code>, and the editorial fields (<code>author</code>/<code>license</code>, defaulting series-wide from <code>series_meta</code>, and <code>date</code>) all resolve from the article's own meta block and cover slide, and any of them can be overridden per entry here when you want <code>series.json</code> to have the final say. <code>status</code> says what each article is worth to the series: <code>active</code> (the default), <code>draft</code> — still an article of the series, kept out of the output until <code>--include-drafts</code> previews it with a banner — or <code>ignored</code>, which takes it out of the chain entirely without deleting the entry and everything you configured on it. The array order is the navigation and index order. The full fallback chain per field is in <code>GLOSSARY.md</code>.</p>
<p><code>lightwebpres status my-series --format json</code> also carries the tag inventory used by the build. For the focused view, use <code>lightwebpres series tags my-series</code>: it reports effective article and slide visibility by tag, separates <code>active</code>, <code>draft</code>, and <code>ignored</code>, and shows what the default selection will actually publish. Add <code>--tag fr</code> to keep one row.</p>
<p><code>status</code> lists articles in array order, each resolved value and where it came from: JSON entry, article metadata, content, derived field or built-in default. An unreadable source remains listed with fallback values and a stderr warning. Neither <code>status</code> nor <code>series tags</code> builds or writes anything.</p>
<p>Article metadata can also declare <code>tags: fr</code>: that gate must match the selected tag <strong>and</strong> at least one non-excluded slide must accept it. Untagged articles have no article gate. <code>series_meta.default_tag</code> sets the initial selection (default: <code>default</code>); a valid saved reader choice wins. Selecting <code>default</code> shows only shared slides, not every variant. <code>build</code> and <code>audit</code> warn if a selectable tag has no effective slide, or an article has no non-excluded slide. Use <code>series tags --format json</code> for status totals, shared slides and default output; <code>--tag fr</code> narrows the tag rows without changing series totals.</p>
<h2 id="5-choose-presets-themes-and-customization" tabindex="-1">5. Choose presets, themes and customization</h2>
<h3>Identities, presets and themes</h3>
<p><strong>Identity</strong> groups presentation choices. The native identity, <strong>LightWebPres</strong>, provides <code>builtin/standard</code> and the minimal <strong>Light</strong> theme. <strong>Commons</strong> contains the global theme catalogue and presets that bind those themes to native layouts. An <strong>Identity Kit</strong> is a self-contained versioned collection of layouts, headers, footers, assets, typed themes and constrained structural CSS. <strong>Preset</strong> selects a layout/chrome configuration and a base <strong>Theme</strong>; it does not generate every possible combination of those resources.</p>
<p>LWP owns the page shell, navigation and JavaScript. Kit fragments have <code>{{content}}</code>, <code>{{slide_header}}</code> and <code>{{slide_footer}}</code> slots; the index receives only <code>{{content}}</code>. A kit can use local files or native references <code>builtin:standard</code> for layouts and <code>builtin:light</code> for themes. A native layout inside a kit keeps that kit's chrome. Kits cannot depend on Commons or other kits, extend them, or declare provenance, parentage or authenticity. Resource origins are computed by the loaders.</p>
<p>The only persisted selection is <code>series_meta.presentation_preset</code>: <code>builtin/standard</code>, <code>commons/&lt;id&gt;</code> or <code>id@MAJOR.MINOR.PATCH/preset</code>. The identity is inferred from this reference. The selection belongs neither in article metadata nor in an <code>articles[]</code> entry. Omission selects <code>builtin/standard</code> implicitly. <code>init --preset builtin/standard</code> and <code>series preset set --preset builtin/standard</code> persist that explicit reference; plain <code>init</code> leaves the field absent. Neither native choice vendors resources.</p>
<pre><code class="language-json">
{
  "series_meta": {
    "presentation_preset": "corporate@1.0.0/brief"
  }
}
  </code></pre>
<p>The kit manifest's <code>label</code> names the identity, not whichever preset happens to be initial. Its optional <code>default_preset</code> names a local preset, otherwise the first preset in manifest order is used. <code>slide_layouts</code> and <code>slide_chrome</code> declare preset defaults in that manifest only.</p>
<p><code>slide-layout</code>, <code>slide-header</code> and <code>slide-footer</code> work on all four slide types. They override the selected preset's defaults for one slide, not through an author JSON cascade. The preset's theme supplies the typed base unless <code>settings.conf</code> explicitly selects another theme. Precedence is: base theme &lt; <code>settings.conf</code> pins &lt; article <code>style.*</code> &lt; instance styles; <code>templates/custom.css</code> remains the final advanced CSS layer. Assets are published under <code>public/assets/presentations/&lt;id&gt;/&lt;version&gt;/...</code>, or embedded by <code>--inline-images</code>.</p>
<pre><code class="language-bash">
./lightwebpres preset list
./lightwebpres preset show builtin/standard
./lightwebpres series preset my-series
./lightwebpres series preset set my-series --preset builtin/standard --use-preset-theme
./lightwebpres init my-series --preset builtin/standard
  </code></pre>
<p><code>series preset set</code> vendors and selects without applying a starter. It preserves pins and <code>custom.css</code>; with an explicit <code>theme:</code> in <code>settings.conf</code>, it requires <code>--keep-theme</code> or <code>--use-preset-theme</code>, which removes that line. <code>--keep-theme</code> requires an explicit <code>theme:</code>. Kits live under <code>kits/&lt;id&gt;/&lt;version&gt;/</code> in a catalogue and <code>templates/kits/&lt;id&gt;/&lt;version&gt;/</code> once vendored. <code>LWP_IDENTITY_KITS_DIR</code> replaces the user catalogue location; an id/version collision shadows the entire kit. See <code>specifications.md</code> §9.9 for manifest, validation and security details.</p>
<p>For a kit preset, <code>init --preset</code> validates and vendors the complete kit, writes the selector and generates settings from its theme. It applies the declared starter unless <code>--no-starter</code> is passed. Neither option changes the meaning of the <code>template</code> commands. Choose an installed selector from <code>preset list</code>; <code>corporate@1.0.0/brief</code> is illustrative, not a supplied kit. Native selection needs no files. Both <code>init</code> and <code>series preset set</code> vendor a Commons descriptor and its selected external theme snapshot, if any; a native or embedded theme needs no snapshot copy. An identical local dependency is reused, while a conflicting file is refused.</p>
<p>The guide itself uses the tracked kit <code>examples/kits/lightwebpres-docs/0.1.0/</code>. <code>tools/build_guide.py</code> vendors it into a temporary series and publishes its assets with the guide. It is an inspectable kit example, not another source of this manual.</p>
<h3>Add a Commons preset</h3>
<p>Commons themes use the global <code>themes/</code> catalogue, <code>LWP_THEMES_DIR</code> and a series' <code>templates/themes/</code>. Preset descriptors use a separate Commons root: installed <code>commons/presets/</code> beside the executable or below <code>&lt;prefix&gt;/share/lightwebpres/</code>, then the user root <code>LWP_COMMONS_DIR</code>, then <code>templates/commons/presets/</code> in the series. User defaults are <code>$XDG_DATA_HOME/lightwebpres/commons/</code> (normally under <code>~/.local/share</code>) or <code>%APPDATA%/lightwebpres/commons/</code>. A nearer descriptor replaces the whole entry.</p>
<p>For example, <code>templates/commons/presets/reading.json</code> contains:</p>
<pre><code class="language-json">
{
  "schema": "lightwebpres.commons-preset/1",
  "id": "reading",
  "label": "Reading",
  "description": "Native layouts with a light reading theme.",
  "theme": "builtin:light"
}
  </code></pre>
<p>All five keys are required; no other key is accepted, including <code>starters</code>. The <code>id</code> matches the filename; <code>theme</code> is a global theme slug or <code>builtin:light</code>. Select it with <code>./lightwebpres series preset set my-series --preset commons/reading</code>. If the series has an explicit theme, also choose <code>--keep-theme</code> or <code>--use-preset-theme</code>.</p>
<h3>Compose a kit</h3>
<p><code>kit compose</code> builds an autonomous kit from an explicit recipe. This complete <code>recipe.json</code> needs no source files:</p>
<pre><code class="language-json">
{
  "schema": "lightwebpres.kit-composition/1",
  "sources": {},
  "manifest": {
    "schema": "lightwebpres.identity-kit/1",
    "id": "brief",
    "version": "1.0.0",
    "label": "Brief",
    "default_preset": "reading",
    "layouts": {
      "cover": {"default": "builtin:standard"},
      "standard": {"default": "builtin:standard"},
      "series-nav": {"default": "builtin:standard"},
      "full-article": {"default": "builtin:standard"},
      "index": "builtin:standard"
    },
    "themes": {"light": "builtin:light"},
    "structure_css": "structure.css",
    "presets": {
      "reading": {
        "label": "Reading",
        "description": "Native layouts with a fixed editorial footer.",
        "theme": "light",
        "slide_layouts": {
          "cover": "default",
          "standard": "default",
          "series-nav": "default",
          "full-article": "default"
        },
        "slide_chrome": {"all": {"footer": "Brief"}}
      }
    }
  },
  "files": {
    "structure.css": {"text": ".lwp-presentation--brief { gap: 1rem; }\n"}
  }
}
  </code></pre>
<pre><code class="language-bash">
./lightwebpres kit compose recipe.json --output kits --dry-run
./lightwebpres kit compose recipe.json --output kits
LWP_IDENTITY_KITS_DIR="$PWD/kits" ./lightwebpres init my-brief --preset brief@1.0.0/reading
  </code></pre>
<p>The result is <code>kits/brief/1.0.0/</code>. The recipe requires exactly <code>schema</code>, <code>sources</code>, <code>manifest</code> and <code>files</code>. To reuse declared source files, <code>sources</code> maps an alias to a relative kit path contained below the recipe directory; <code>files</code> maps a destination to <code>{"source":"alias","path":"local/path"}</code>, <code>{"file":"local/path"}</code> or <code>{"text":"content"}</code>. A <code>.css</code> destination also accepts <code>{"parts":[...]}</code> with a non-empty list of those descriptors; files read by <code>parts</code> must also have a <code>.css</code> extension. A source kit's declared <code>structure_css</code> file is recognized by its manifest role regardless of suffix. Only matching class tokens in its selectors are rebound to the target kit's scope, including escaped tokens; comments, strings, attribute values and declarations are preserved. Other copied files are not rebound. The full final manifest must name all final local references explicitly: there is no guessed remapping or dependency closure.</p>
<p>Publication is staged outside the output catalogue on the same filesystem; <code>--dry-run</code> validates in disposable system temporary storage and creates no output. An output catalogue at a filesystem or mount root is refused: choose a subdirectory within that filesystem. Existing kit destinations are refused. The composed kit needs no source kit at build time and carries no provenance record.</p>
<h3>Keep alternate presentations available</h3>
<p>A series has one primary presentation, but a build can carry other named presets for the reader to choose without rebuilding. A kit or Commons primary also makes the compatible native <code>builtin/standard</code> available automatically, after the declared alternatives. Put other alternatives at the root of <code>series.json</code>, or pass them for one build:</p>
<pre><code class="language-json">
{
  "series_meta": {
    "presentation_preset": "lightwebpres-docs@0.1.0/docs"
  },
  "presentation_presets": [
    "builtin/standard"
  ]
}
  </code></pre>
<pre><code class="language-bash">
./lightwebpres build my-series --presentation-presets builtin/standard
  </code></pre>
<p>The primary preset is always emitted first and remains the no-JavaScript fallback. The CLI list overrides the JSON list; it adds alternatives rather than replacing the primary. Duplicate selectors are removed, and an unknown selector fails before output is written. The preset must be available in the effective catalogue. Listing <code>builtin/standard</code> explicitly is optional for a kit or Commons preset. If a slide uses a kit-only <code>slide-layout</code>, <code>slide-header</code> or <code>slide-footer</code>, the implicit default is omitted with a warning; explicitly requesting <code>builtin/standard</code> keeps the normal validation error.</p>
<p>When alternatives exist, <strong>C</strong> opens the Appearance picker with <strong>Identity</strong>, <strong>Preset</strong> and <strong>Theme</strong> controls. The selected preset changes the whole deck, including the index, and lasts across pages in the current browser session. It does not edit the series. If <code>settings.conf</code> names an explicit <code>theme:</code>, that theme remains fixed; otherwise the preset's typed theme follows the selected presentation until the reader chooses an explicit theme. <strong>Follow preset</strong> resets that explicit runtime choice. All themes of every selected kit are published under kit-qualified names, even if no selected preset uses them.</p>
<p>The <strong>Applicable</strong>, <strong>Current identity</strong> and <strong>All</strong> filters only narrow published choices. Applicable means typed compatibility, not brand matching; Current identity means resource ownership. Identity labels stay fixed when the preset or theme changes. The initial/default marker describes a selection, not another identity. The picker does not invent a cross-product of presets and themes or fetch additional catalogue entries.</p>
<p>For color and typography changes, choose the smallest value override that does the job before adding CSS rules.</p>
<h3>Pick a theme (the whole series)</h3>
<p>Dozens of colour themes are preconfigured — too many to pick from a list, so you find one by facet: which family it belongs to, whether its background is light or dark, and what hue that background carries.</p>
<pre><code class="language-bash">
./lightwebpres theme list                                     # the whole catalogue, with facets
./lightwebpres theme list --family terrain                    # one editorial family
./lightwebpres theme list --polarity dark --hue green          # just the ones you mean
./lightwebpres theme gallery                             # every theme, rendered
  </code></pre>
<p>The Commons theme catalogue combines the embedded themes with complete UTF-8 <code>.conf</code> snapshots from the installed and user roots; a series can add its own <code>templates/themes/</code> snapshots on top. <code>LWP_THEMES_DIR</code> replaces the user root. The order is embedded, installed, user, series, and a collision replaces the whole lower entry rather than inheriting it. Use <code>builtin:&lt;slug&gt;</code> to select an embedded theme hidden by a local file.</p>
<p>Installed themes live under <code>&lt;prefix&gt;/share/lightwebpres/themes/</code> for FHS installations, or a sibling <code>themes/</code> beside a standalone executable. The user root is <code>$XDG_DATA_HOME/lightwebpres/themes/</code> on Unix (normally under <code>~/.local/share</code>) or <code>%APPDATA%/lightwebpres/themes/</code> on Windows. Only direct <code>.conf</code> files are loaded. <code>theme path</code> reports the roots. Global <code>theme</code> reports do not include a series' vendored layer; <code>series theme</code> does.</p>
<p>Apply one at init time, or change your mind later:</p>
<pre><code class="language-bash">
./lightwebpres init my-series --theme evergreen
./lightwebpres series theme set my-series --theme crimson
  </code></pre>
<p>A theme is a word in a data file: <code>series theme set</code> rewrites the one <code>theme:</code> line of <code>templates/settings.conf</code> and nothing else. No CSS is touched — the stylesheet is composed in memory at every build.</p>
<p>By default, the build embeds the essential runtime theme bundle for the reader; <code>--no-essential-theme</code> opts out, while explicit selections add to or shape the catalogue:</p>
<pre><code class="language-bash">
./lightwebpres build my-series --lang en --themes print-ink,print-grey
./lightwebpres build my-series --lang en --themes all
  </code></pre>
<p>Or keep the selection in the root of <code>series.json</code>:</p>
<pre><code class="language-json">
"themes": ["essential", "background:light", "bgh:red"]
  </code></pre>
<p><code>essential</code> embeds Monochrome, Monochrome Night and Print Ink. A selector <code>X:Y</code> can use <code>background</code>/<code>bg</code>, <code>family</code>/<code>fam</code>, or <code>background hue</code>/<code>bgh</code>; each selector adds its matching themes and duplicates are removed. An explicit CLI <code>--themes</code> overrides the JSON list.</p>
<p>Create or make a theme portable explicitly:</p>
<pre><code class="language-bash">
./lightwebpres theme create my-theme --from evergreen
./lightwebpres theme migrate my-series
./lightwebpres theme vendor my-series --themes my-theme,evergreen
./lightwebpres theme path
  </code></pre>
<p><code>theme create</code> writes a complete editable snapshot, <code>theme migrate</code> keeps only the selected theme and explicit pins in an old scaffold, and <code>theme vendor</code> copies complete snapshots into the series. No theme file uses <code>extends</code>.</p>
<p>The effective theme in <code>templates/settings.conf</code> is always included as the first base choice, even if it is not in the list. When that file has property pins, the first runtime choice is named <code>custom(&lt;theme&gt;)</code> and the raw base theme is also present; those settings pins apply only to the custom choice. The setting is read at build time, so an author's edit remains the source of truth. <code>style.*</code> page properties and theme variables declared in <code>custom.css</code> are left alone while a reader switches. <strong>C</strong> opens the searchable Appearance picker when the build carries presentation or theme alternatives, and otherwise has nothing to open. <strong>M</strong> opens the global presenter menu; the same menu is available from the bottom-right navigation button. The selection lasts for the other pages of the same deck in the current browser session. The session key includes the deck identity and catalogue digest, so another deck on the same origin or a changed local snapshot cannot reuse an old choice. Each theme choice previews its resolved background, including its gradient, with matching foreground ink. The menu actions carry icons and their keyboard shortcuts, including <strong>I</strong> on Scroll. In the theme picker and that presenter menu, focus starts at the first useful control. In the presenter menu, left/right stay on the current row while up/down move to the nearest control on the adjacent rendered row. <code>Tab</code>, <code>Home</code> and <code>End</code> still move through the controls, and <code>Enter</code>/<code>Space</code> activate the focused one.</p>
<p>These commands inspect and select existing theme values. They do not design, retune or repair a palette. Use <code>theme show</code> to read the measured contrast of the shipped theme, or of the effective theme after the series' pins. <code>audit</code> reads the same resolved sheet without being asked, and speaks only when something has stopped working — a navigation control you cannot see, text the colour of its own ground, a size under the readability floor. It warns; it never refuses, and no shipped theme trips it.</p>
<pre><code class="language-bash">
./lightwebpres theme show evergreen
./lightwebpres series theme my-series --format json
  </code></pre>
<p>The report gives WCAG levels <strong>per category</strong>, with the measured pairs and ratios, not a blanket accessibility grade. It measures the resolved typed properties, not arbitrary rules in <code>custom.css</code>. No palette is rewritten, hidden or refused for its score, and the scores are not put on published pages. Inspect the actual page after customization.</p>
<p>The catalogue includes original palettes and ports such as Nord, Dracula, Solarized, Gruvbox and Catppuccin. <code>family</code> uses <code>desk</code>, <code>light</code>, <code>terrain</code>, <code>heat</code>, <code>pop</code>, <code>ported</code>, <code>print</code>; polarity and background hue are computed. The <a href="https://github.com/Fade78/lightwebpres/blob/main/generated/themes-gallery.png">compact catalogue</a> gives an overview; open <a href="https://github.com/Fade78/lightwebpres/blob/main/generated/themes-gallery.html">the HTML gallery</a> in a browser to filter real covers, cards with notes, page-wide notes and long-form text.</p>
<h3>Why essential themes ship by default</h3>
<p>Every build embeds the <code>essential</code> bundle on its own — Monochrome, Monochrome Night and Print Ink — so the picker is functional on any page without the author opting in. Three reasons, in order:</p>
<ul>
<li><strong>Accessibility.</strong> Monochrome is high-contrast ink with no hue; Monochrome Night is the same on a dark ground, for low-vision or light-sensitive readers; Print Ink is pure black on white, the highest contrast the page carries. A reader who cannot read the deck as drawn has an alternative that does not depend on the author having planned for them.</li>
<li><strong>Print.</strong> Print Ink is drawn for paper — pure white ground, black ink — and is available without an author-supplied theme selection. Press <strong>C</strong>, select <strong>Print Ink</strong>, then print with <code>Ctrl</code>/<code>Cmd</code>+<code>P</code>. Printing preserves the active theme; it does not select Print Ink automatically.</li>
<li><strong>Sobriety.</strong> Monochrome and Print Ink carry no hue, so the essential set never clashes with a series built around one. The author's chosen theme remains primary; the three are alternatives, never a replacement.</li>
</ul>
<p>Opt out when the page should be static or carry a custom selection:</p>
<pre><code class="language-bash">
./lightwebpres build my-series --lang en --no-essential-theme
./lightwebpres verify my-series --lang en --no-essential-theme
./lightwebpres watch my-series --lang en --no-essential-theme
  </code></pre>
<p>With the flag, the page carries no runtime picker unless <code>--themes</code> or <code>series.json["themes"]</code> adds one. Without it, the essential three ship on every build, deduplicated against the primary theme — so a series whose effective theme is already one of them does not see it twice.</p>
<h3>Change one phrase (an instance tag)</h3>
<p>Inside any free text, for the one place that needs it:</p>
<pre><code class="language-markdown">
A {color:call}critical{/color} figure, set in {mono}fixed pitch{/mono}.
  </code></pre>
<p><code>{color:…}</code> and <code>{font:…}</code> take either a shared name (<code>mark</code>, <code>call</code>, <code>mono</code>, …) or a literal; <code>{sc}</code>, <code>{u}</code>, <code>{strike}</code> and <code>{mono}</code> take no value. A bad value is a build error naming the file, never a silent no-op, and <code>audit</code> counts them per article so you know where to look when you change theme.</p>
<p><strong>Alignment is the one block-level tag</strong>, because <code>text-align</code> on an inline span does nothing. Opener and closer each go alone on their line:</p>
<pre><code class="language-markdown">
{align:center}
This paragraph is centred, and so is the next one.
{/align}
  </code></pre>
<p>Values: <code>left | center | right | justify</code>. Everything inside the block aligns, table cells included.</p>
<h3>Change one page (<code>style.*</code> in its meta block)</h3>
<p>Any property, scoped to that page only:</p>
<pre><code>
&lt;!-- lwp:meta --&gt;
page_title: The apple pie
style.cover.bg.angle: 90deg
style.page.content-max: 60ch
  </code></pre>
<p>And <code>fact-variant: warning</code> on a standard slide gives that one fact box a named look, rather than a hand-tuned colour.</p>
<h3>Change the whole series (<code>templates/settings.conf</code>)</h3>
<p>Every visual decision is a typed property, <code>component.axis: value</code>, and <code>settings.conf</code> lists <strong>all</strong> of them, commented out, at the values of the theme you chose — the complete surface is under your eyes, no documentation needed. Uncomment a line to <strong>pin</strong> it: it survives every theme change and every executable upgrade, because <code>lightwebpres</code> never rewrites your file.</p>
<p>Two properties control the fact-box bold (<code>**text**</code> in a fact-box):</p>
<ul>
<li><code>fact.strong.pad</code> — the side padding of the highlight box around the bold text (default <code>max(3px, 0.375vmin)</code>, automatically 0 on themes with no highlight ground).</li>
<li><code>fact.strong.absorb-punct</code> — <code>on</code> (default) absorbs the punctuation that follows a bold run into the highlight (<code>**2000**,</code> → the comma is highlighted too); <code>off</code> leaves the Markdown as written.</li>
</ul>
<pre><code>
# kicker.fg: ink-quiet      ← the scaffold, showing the theme's value
kicker.fg: call             ← uncommented: yours, and it stays
  </code></pre>
<p>A bare word like <code>call</code> is looked up among the theme's shared values (<code>color.call</code>, since <code>fg</code> is a colour axis); a literal like <code>#8A4B00</code> works anywhere a colour does. A mistyped key or value is a named build error pointing at the file and key. An empty value on a known property, such as <code>page.bg:</code>, removes that pin and lets the selected theme provide the value; an unknown key is still an error.</p>
<p>Three properties people look for by name: <strong><code>page.content-max</code></strong> is the text column width, <code>84vw</code> by default — proportional to the window, with no ceiling, so a deck shown full screen uses the screen. Every type size is proportional too — the kicker, the fact label, the key figure's caption and the slide number as much as the title — which is what keeps the line length steady and the proportions between them fixed as the screen grows. Each size has a floor in pixels, and the floor is what governs a phone. <strong><code>page.block-max</code></strong> is the width of the things that are not running text — a table, a code block, a figure — sized by what they hold rather than by a count of characters; it carries a floor as well as a ceiling — <code>min(84vw, max(1100px, 102vmin))</code> — so a table grows with the text inside it and still stops before the window edge. <strong><code>page.hyphens</code></strong> (<code>manual | auto</code>) controls whether words break at end of line; it is <code>manual</code>, and nothing turns it on for you.</p>
<p>After a <code>series theme set</code>, <code>audit</code> will note that the scaffold's <em>comments</em> show the old theme's values; <code>template update --scaffold</code> realigns them while keeping every pinned line.</p>
<p>Shared theme values are <code>color.page</code>, <code>color.ink</code>, <code>color.ink-quiet</code>, <code>color.mark</code>, <code>color.call</code>, <code>color.affirm</code>, <code>color.nav</code> and the four font stacks <code>font.text</code>, <code>font.display</code>, <code>font.ui</code>, <code>font.mono</code>. Change a component property rather than its shared color when only that component should move:</p>
<pre><code class="language-conf">
verdict.partial.fg: #8A4B00
summary.fg: #10151B
link.decoration-color: mark
  </code></pre>
<p><code>color.nav</code> controls navigation furniture, not body text. Body and source links retain surrounding ink and use an underline; <code>link.decoration-color</code> changes that underline. Glyph-owning components expose <code>shadow.fg</code>, <code>blur</code>, <code>dx</code>, <code>dy</code> for halos (for example <code>title1.shadow.fg: #33FF8866</code>). An inherited text shadow resolves its size at the ancestor, not separately for each glyph. Raised components expose elevation color, blur, offsets and spread, with hover axes on interactive cards/buttons. Use the generated settings scaffold for exact names rather than inventing CSS variables.</p>
<h3>Rules rather than values (<code>templates/custom.css</code>)</h3>
<p>Full CSS, no subset, appended after the composed stylesheet so your rules win ties. <code>init</code> creates it strictly empty, because "appended" means appended verbatim: anything the tool wrote in there as advice to you would be published to every reader of every page. <code>settings.conf</code> can carry five hundred comment lines precisely because it is parsed and this file is not. New selectors, media queries, <code>@font-face</code> (name the family at the head of a stack in <code>settings.conf</code>, declare the face here). The composed sheet's <code>--component-axis</code> variables are usable in it (<code>border-color: var(--color-mark)</code>), and that is the recommended way to follow the theme.</p>
<p>Behaviour is the third surface, and it isn't in your series by default: the navigation script lives in the executable. <code>template write nav.js</code> puts a copy under <code>templates/</code> if you want to change it, and it then overrides the navigation wholesale — there is no partial override. The page and index HTML structure is fixed, not a template.</p>
<h2 id="6-set-languages-and-typography" tabindex="-1">6. Set languages and typography</h2>
<p>Interface strings and typography are independent domains: <code>interface/{lang}.json</code> and <code>typography/{lang}.json</code>. French and English are embedded in the executable. Without <code>--lang</code> or <code>LWP_LANG</code>, pages embed both interface vocabularies: the browser chooses French for <code>fr-*</code> locales and English otherwise. An explicit language locks the interface. Typography is applied at build time and never re-run when the browser locale changes.</p>
<pre><code class="language-bash">
./lightwebpres build my-series --lang en
./lightwebpres template show interface/fr.json
./lightwebpres template write typography/fr.json my-series
  </code></pre>
<p>Write only a domain you intend to customize. Interface strings merge key by key; typography <code>rules</code> replace the base rules wholesale. Legacy unified <code>language/{lang}.json</code> files remain supported; split files win for their own domain. <code>--language-file path</code> on <code>build</code>/<code>verify</code> explicitly selects a unified pack at the highest priority. <code>LWP_INTERFACE_DIR</code>, <code>LWP_TYPOGRAPHY_DIR</code> and <code>LWP_LANGUAGE_DIR</code> relocate the domains; specifications.md §2.3 and §19 give the schemas and installed-pack lookup.</p>
<p>For multilingual slides, <code>series_meta.lang_tags</code>, such as <code>{"fr": "fr", "en": "en"}</code>, maps tags to typography packs. The first mapped tag on the slide wins; otherwise <code>--lang</code>/<code>LWP_LANG</code> supplies the fallback. An unknown language ultimately falls back to English. Add rules for another language in its pack, not by changing the engine.</p>
<p>Typography upgrades existing spaces to non-breaking ones; it never invents spacing or thousands grouping, and preserves existing non-breaking spaces. French handles <code>; : ! ?</code>, guillemets, <code>%</code>, spaced incise dashes, grouped thousands (<code>170 000</code>), number/unit words including millions and dollars, and <code>×</code>/<code>≈</code> before a number. English has its own smaller set: metric units, unit words, initials, operators and spaced dashes. Rules affect text, not HTML tag syntax.</p>
<p>To disable selected categories for one article, set metadata:</p>
<pre><code class="language-text">
typo_units: off
typo_thousands: off
  </code></pre>
<p>Use <code>typo: off</code> for every rule on that article, or <code>--no-typography</code> on <code>build</code>/<code>verify</code>/<code>watch</code> for the entire run. A category switch acts on the pack in force; English has no thousands rule to disable. The full rule lists are in specifications.md §4.5, §7.5 and §19.6.</p>
<h2 id="7-verify-and-publish" tabindex="-1">7. Verify and publish</h2>
<p>Two different checks, for two different moments:</p>
<pre><code class="language-bash">
./lightwebpres audit my-series --lang en    # source and render warnings
./lightwebpres verify my-series --lang en   # does output match the sources?
  </code></pre>
<p><code>audit</code> renders the series in memory and writes nothing. It checks every listed article, including drafts and <code>ignored</code> entries; it does not need an <code>--include-drafts</code> option. Read three kinds of report:</p>
<ul>
<li><strong>Sources and overrides:</strong> missing covers, instance tags, malformed metadata or tags, missing language packs, ignored cover fields, legacy <code>style.css</code>, retired CSS variables with their replacements, stale scaffold comments and symlinks that leave their logical roots.</li>
<li><strong>Resolved styles:</strong> an invisible navigation control, text matching its background, or a size below the readability floor after theme, settings and article styles compose. Valid individual values can still combine badly.</li>
<li><strong>Rendered output:</strong> build failures and an image inventory with inline/figure counts, unused sources and missing referenced assets. If rendering fails, unknown usage is reported as unavailable, not falsely called unused.</li>
</ul>
<p>Plain <code>audit</code> exits zero even when rendering fails. <code>--strict</code> makes warnings and render failures non-zero CI results. <code>--templates</code> limits the check to the presentation layer, including resolved styles, without rendering or per-article checks. It is cheaper than the full audit, which costs about a build.</p>
<p><code>verify</code> asks the other question: it rebuilds every article in memory and compares it against <code>public/</code> (ignoring build stamps and surrounding whitespace), exiting non-zero the moment anything differs — wire it in before <code>build</code> to catch a <code>public/</code> that was hand-edited or never rebuilt after a source change.</p>
<p>Use the same supported rendering options as the build, including <code>--lang</code>, <code>--themes</code> and <code>--no-essential-theme</code>. <strong><code>verify</code> does not accept <code>--inline-images</code></strong> and cannot reproduce that build mode: embedded images or presentation assets can therefore report drift even with unchanged sources. Use a separate, non-inline build output for this CI check.</p>
<h3>Asking why a value is what it is</h3>
<p>Most of what ends up on a page was never written on that page: a title falls back through <code>series.json</code>, the meta block and the cover slide, a colour falls through <code>settings.conf</code>, the theme and the built-in defaults. When the result surprises you, ask:</p>
<pre><code class="language-bash">
./lightwebpres resolve my-series page_title --article first-page.md
./lightwebpres resolve my-series kicker.fg
  </code></pre>
<p>Nothing tells it what kind of name you passed — the name does. A dot means a theme property, an underscore an article or series field, a hyphen a slide field.</p>
<p>The answer shows the level that decided <strong>and every level that didn't</strong>, strongest first:</p>
<pre><code>
kicker.fg — theme property
  value: #BF616AFF
  from:  settings
  via:   color.call

  cascade, strongest first:
    instance  —
    article   —
  &gt; settings  call
    theme     —
    default   ink-quiet
  </code></pre>
<p>That second half is the one that solves problems. A line you wrote that changed nothing shows up here as a level holding nothing — still commented out, or beaten by a <code>series.json</code> entry you had forgotten.</p>
<p>A slide field has no cascade, so <code>resolve fact-label</code> answers with the list of slides that set it instead — across the series, or within one article with <code>--article</code>. Add <code>--format json</code> for a machine, and pass <code>--article</code> to a theme property to fold that page's own <code>style.*</code> lines into the chain.</p>
<h3>Publish the output, not the project</h3>
<p>Upload the contents of <code>public/</code> to a static host: the article HTML files, <code>index.html</code>, referenced <code>img/</code> files and any <code>assets/presentations/</code> files. The generated series README lives beside <code>series.json</code>, not inside <code>public/</code>. No Python server or LightWebPres runtime is needed on the host. Reopen the hosted index, follow an article link and test a slide link from another device. Local <code>file://</code> viewing works, but does not make an address reachable by a phone.</p>
<p>By default, only referenced images are copied from <code>sources/img/</code>; unused source files are not published and existing output assets are left in place. <code>--inline-images</code> embeds Markdown images from cards and included long-form files as data URIs, with no copied <code>img/</code> directory. Base64 adds roughly a third to image size before serving compression. Raw HTML images with relative paths cannot be inlined: the build names and rejects them rather than leaving references to an absent asset directory. Keep a non-inline output for <code>verify</code>.</p>
<p>Output switches on <code>build</code> and <code>watch</code>: <code>--no-index</code> skips <code>index.html</code>, <code>--no-readme</code> skips the series README, <code>--no-nav</code> leaves a placed <code>series-nav</code> without generated links, <code>--drafts-only</code> previews only drafts, and <code>--open</code> opens the result. <code>build --include-drafts</code> includes drafts alongside active articles; <code>verify</code> supports that selection too. <code>--slides-page-numbers on</code> engraves top-right numbering (off by default, independent of the live counter).</p>
<p>A single article can set <code>page_dest: index.html</code> to become the directory's landing page; no redundant one-card index is then generated. In a multi-article series that name is reserved when an index is generated. <code>--no-index</code> leaves it available. Duplicate destinations (case-insensitive), unsafe filenames, malformed JSON, missing slugs and duplicate slugs are fatal. Generated HTML is checked for tag balance before writing; that is not a security sanitizer.</p>
<p>Removing an article from the array, marking it draft/ignored, or dropping an image reference does not erase an old published file. Review the manifest-based cleanup after a build:</p>
<pre><code class="language-bash">
./lightwebpres clean my-series          # preview orphan removal
./lightwebpres clean my-series --force  # remove the listed orphan output
  </code></pre>
<p>Review the host's stale files too: uploading new files alone does not remove old ones. In particular the browser GitLab push never deletes files.</p>
<h3>Trust and licensing</h3>
<p>Build only trusted content. Raw HTML, including scripts, passes through; <code>custom.css</code> and a local <code>nav.js</code> are author-controlled code. Sanitize upstream CMS exports, translations or other untrusted inputs before building. Symlinks out of source roots are followed and reported by <code>audit</code>, not sandboxed. Tags filter views, not access: only <code>excluded</code> slides are omitted at build time. Speaker notes are public HTML; <code>comment:</code> fields are not published.</p>
<p>The program is GPL v3 or later, with the <a href="https://github.com/Fade78/lightwebpres/blob/main/COPYING.EXCEPTION">Output Exception</a>. Your generated presentations may use your chosen terms, commercially or not; the exception does not cover a generator using output as templates. The executable copied by <code>init</code> is still GPL code: keep <code>COPYING</code> and <code>COPYING.EXCEPTION</code> with it when distributing a series repository. See the <a href="https://github.com/Fade78/lightwebpres/blob/main/README.md#license">README licence summary</a> and <a href="https://github.com/Fade78/lightwebpres/blob/main/THIRD-PARTY-NOTICES.md">third-party notices</a>.</p>
<h2 id="8-present-print-and-share" tabindex="-1">8. Present, print and share</h2>
<p>Every page the build writes is a self-contained deck — keyboard, mouse, and touch all work, the index included: it is a page like any other, and its step is one article card at a time. The controls below let the speaker drive the deck without looking at the screen.</p>
<h3>Keyboard</h3>
<table class="comparison-table">
<thead>
<tr>
<th>Key</th>
<th>Action</th>
</tr>
</thead>
<tbody>
<tr>
<td>↓ / PageDown / →</td>
<td>Next slide — on the index, next article card</td>
</tr>
<tr>
<td>↑ / PageUp / ← / Backspace</td>
<td>Previous slide — on the index, previous article card</td>
</tr>
<tr>
<td>Home</td>
<td>Beginning of the page — first slide on an article; top on the index</td>
</tr>
<tr>
<td>Ctrl/Cmd+Home</td>
<td>Back to the series index — on the index: top of the page</td>
</tr>
<tr>
<td>End or Ctrl/Cmd+End</td>
<td>Last slide. On the index: last article card</td>
</tr>
<tr>
<td>+ / - / =</td>
<td>Enlarge / reduce / reset the page zoom (the page only; Ctrl/Cmd +/- remains the browser zoom)</td>
</tr>
<tr>
<td>F</td>
<td>Fullscreen (Esc to exit)</td>
</tr>
<tr>
<td>I</td>
<td>Toggle between the configured smooth slide glide and an instant jump</td>
</tr>
<tr>
<td>C</td>
<td>Open the compiled theme picker</td>
</tr>
<tr>
<td>M</td>
<td>Open the presenter menu</td>
</tr>
<tr>
<td>S</td>
<td>Open sharing for the series, article or current slide</td>
</tr>
<tr>
<td>B</td>
<td>Black pause screen (press again to dismiss)</td>
</tr>
<tr>
<td>W</td>
<td>White pause screen (press again to dismiss)</td>
</tr>
<tr>
<td>T</td>
<td>Theme-background pause screen (press again to dismiss)</td>
</tr>
<tr>
<td>N</td>
<td>Toggle the speaker panel: the current slide's notes and the next slide's title (no panel content on the index, which has no slides)</td>
</tr>
<tr>
<td>0–9 then Enter</td>
<td>Jump straight to slide N (1-based) — for decks of ten slides and up; inert on the index, which has no slides</td>
</tr>
<tr>
<td>L</td>
<td>Open the variant menu when the article carries at least two tags across its slides</td>
</tr>
<tr>
<td>H</td>
<td>Open the help overlay, which lists every key on this table</td>
</tr>
<tr>
<td>Esc</td>
<td>Leave fullscreen; also closes the speaker panel</td>
</tr>
</tbody>
</table>
<p>Every navigation action leaves its selected target visible. An index card or a series-navigation card is kept entirely inside the viewport when it fits. A slide taller than the screen is the necessary exception: it enters with its top aligned to the top of the viewport, then its bounded reading steps finish with its top or bottom aligned to the corresponding viewport edge.</p>
<p>When the help overlay is open, its scrollable foreground owns the arrow, PageUp/PageDown, Home/End and Space keys. The same is true of the speaker panel when it has focus; while that panel is merely open and unfocused, the arrows keep navigating the deck.</p>
<p>The B/W/T pause screens hide the slide so the audience's eye comes back to the speaker — the same feature PowerPoint and Keynote call "blank". T uses the theme's own background colour, so a dark theme pauses on a dark screen rather than flashing white.</p>
<h3>Speaker panel and slide counter</h3>
<p>A small <code>X / N</code> counter sits in the bottom-left corner and fades out with the other chrome when the mouse is idle. Type a slide number and press <strong>Enter</strong> to jump there — handy once a deck passes ten slides and the arrow-key walk becomes a slog. That live counter is <strong>always</strong> shown — except on the index, where there is nothing to count — and is independent of the engraved top-right <code>NN / NN</code> slide number, which is opt-in (off by default) and turned on only by <code>--slides-page-numbers on</code>, the article front-matter <code>slide_page_numbers</code>, or <code>series_meta.slide_page_numbers</code> (see specifications.md §3.3.5). Press <strong>N</strong> to open the speaker panel: it shows the current slide's <code>note:</code> field (the speaker note you wrote for that slide, see below) and the title of the next slide. The panel opens in the same page, so anyone watching the projected or shared screen sees it too. It follows navigation; press <strong>N</strong> again to close it. There is no separate private presenter window.</p>
<p>A speaker note is a <code>note:</code> field on the slide — distinct from a <code>[^n]</code> footnote, which is a <em>source</em> note printed for the reader:</p>
<pre><code class="language-markdown">
&lt;!-- lwp:slide --&gt;
slug: speaker-example
kicker: Two
## Slide two
note: Mention the 2020 study — the audience asked for it last time.
  Follow up with the 2023 replication.
  If time runs short, skip the appendix.
  </code></pre>
<p>The <code>note:</code> value is embedded in the HTML as a hidden element and displayed by the presenter panel. Anyone with the page can open the panel or inspect its source: do not put confidential content in <code>note:</code>.</p>
<p>A <code>note:</code> may run over several lines: any line that starts with whitespace continues the note, and an indented blank line marks a paragraph break. The block ends at the first non-indented, non-empty line (the next field or the slide's body), so the continuation lines are never captured as slide content.</p>
<h3>Printing and PDF</h3>
<p>Each page is print-ready. <strong>Print</strong> from the browser (Ctrl/Cmd+P) and choose "Save as PDF": every slide lands on its own sheet, the navigation chrome is stripped, and the theme colours are kept. A short slide no longer blanks a page — each sheet sizes to its own content.</p>
<p>For black ink on white, press <strong>C</strong> and select <strong>Print Ink</strong> before opening the print dialog. It is included by default in the essential theme bundle; printing does not switch to it automatically.</p>
<h3>Mouse</h3>
<table class="comparison-table">
<thead>
<tr>
<th>Gesture</th>
<th>Action</th>
</tr>
</thead>
<tbody>
<tr>
<td>Single click on content</td>
<td>Next slide (configured glide, 200ms default)</td>
</tr>
<tr>
<td>Right-click on content</td>
<td>Previous slide (configured glide, 200ms default)</td>
</tr>
<tr>
<td>Click during the glide</td>
<td>Jump straight to that click's target</td>
</tr>
<tr>
<td>Middle button anywhere</td>
<td>Exit fullscreen on its own; to enter, press the middle button, then click left inside the window</td>
</tr>
<tr>
<td>Click in the bottom-right corner</td>
<td>Toggle the navigation buttons (hide/show)</td>
</tr>
</tbody>
</table>
<p>Clicks on links, images, buttons, and the share popover are not intercepted — they keep working. The right-click to go back is the remote-mouse use case: the speaker with a wireless mouse in hand left-clicks to advance, right-clicks to go back — two distinct buttons, no aiming. The native context menu is suppressed on slide content so right-click is a clean back gesture. A click lands instantly on the next card and glides to it over the configured duration (200 ms by default); a click that arrives while the deck is still gliding does not wait — it jumps straight to its target, so two clicks in quick succession land two pages on, and a right-click during the glide returns you to the card you left. The middle button only leaves fullscreen by itself: browsers refuse <code>requestFullscreen()</code> from any non-left event, so entering is a two-step gesture — middle button to arm the intent, then a left click inside the window (a right click in the same window goes to the index instead). The wheel itself keeps scrolling; the ⛶ button and F stay direct entries. Esc exits fullscreen. The cursor hides after 1 second of idleness in fullscreen. A left click on an existing selection just dismisses the highlight — no step — and a right-click on a selection opens the browser's own menu, the deck stepping aside. Two clicks in quick succession are two steps: the deck never treats a double click as anything else.</p>
<h3>Touch (phone, tablet)</h3>
<table class="comparison-table">
<thead>
<tr>
<th>Gesture</th>
<th>Action</th>
</tr>
</thead>
<tbody>
<tr>
<td>Swipe left</td>
<td>Next slide — on the index, next article card</td>
</tr>
<tr>
<td>Swipe right</td>
<td>Previous slide — on the index, previous article card</td>
</tr>
<tr>
<td>Tap on content</td>
<td>Next slide — on the index, next article card</td>
</tr>
<tr>
<td>Double tap</td>
<td>Show or hide the navigation immediately</td>
</tr>
<tr>
<td>Press and hold</td>
<td>Select text and open the copy menu — the deck does not take it</td>
</tr>
</tbody>
</table>
<h3>Navigation buttons</h3>
<p>The round buttons in the bottom-right corner form one column: from bottom to top, Menu, down, up and fullscreen. The arrows are grayed when they cannot move further. The series-index action, share, Scroll (also <strong>I</strong>) and the variant filter are actions in the presenter menu, which also carries the themes, help, notes and pause screens. The same controls sit on the index, where previous and next step one article card at a time. After 3 seconds of mouse idleness they fade out, and the cursor goes with them: the speaker does not want chrome on the wall. In fullscreen both go after 1 second. Move the mouse to bring the buttons back; the cursor waits for 250ms of continuous movement, so a knock against the desk does not put it on the wall.</p>
<p>On a phone or a tablet they fade after the same three seconds. A <strong>double tap</strong> toggles them immediately: visible navigation disappears at once; hidden navigation returns and starts a fresh countdown. If the first tap has already started a slide or scroll, recognizing the pair cancels that movement and restores the fiche and position from before the first tap. A touch or a scroll restarts the countdown while the controls are still up, so they never vanish under your finger; once they are gone they no longer answer a touch at all, so the corner of your own text is safe to touch. Fullscreen is the ⛶ button in that bar rather than the middle button: the middle button alone only exits fullscreen — entering is the two-step, middle button then a left click. With a mouse, clicking the corner (not a button) toggles their current visibility.</p>
<p>Text selection, long press and the copy menu remain the browser's. The navigation double tap is recognized from touch events themselves, not from the delayed clicks a browser synthesizes, so those clicks cannot advance the deck after the first tap has been restored.</p>
<h3>Share a series, an article or a slide</h3>
<p>Press <strong>S</strong> or choose Share in <strong>M</strong>. Select the scope, then copy the link or show its locally generated QR code. Series points to <code>index.html</code>, article to the current page, and slide to the current <code>slug:</code> anchor. On the index, article points to the index itself and slide scope is disabled. Slugs, not slide positions or headings, keep previously shared addresses stable.</p>
<p>QR sharing needs an HTTP(S) address reachable from the receiving phone. A local file or loopback URL is not such an address; the UI explains the local address instead of offering a misleading QR link. Publish first, then test the hosted address. No QR service receives the link.</p>
<p>Fullscreen is a deliberate <strong>F</strong>/button gesture, not a consequence of rotating a phone. It requests a screen wake lock where supported; otherwise the operating system may still dim the display. The scrollbar fades with the navigation without changing layout. Entering/leaving fullscreen and clicking in the button corner reveal the controls immediately.</p>
<p>The configured slide glide defaults to <code>200</code> ms. Set <code>series_meta.scroll_duration</code> or pass <code>--scroll-duration milliseconds</code> on <code>build</code>/<code>verify</code>/<code>watch</code>; <code>0</code> is instant. The Scroll action in <strong>M</strong>, also <strong>I</strong>, switches between that configured duration and <code>0</code> and shows the active value.</p>
<h2 id="9-build-in-the-browser" tabindex="-1">9. Build in the browser</h2>
<p><code>web/index.html</code> runs the same executable, unmodified, inside vendored <a href="https://pyodide.org" rel="noopener" target="_blank">Pyodide</a> (CPython compiled to WebAssembly). Two tabs share one engine load:</p>
<ul>
<li><strong>Upload a zip:</strong> select a series archive and download a zip of <code>public/</code>. The build stays in the tab. Archives over 500 MiB compressed or uncompressed are refused before extraction; Pyodide loads locally, not from a CDN.</li>
<li><strong>Sync with GitLab:</strong> configure your instance, repository and credentials, pull the series, build and push. Requests go directly to GitLab, without a third-party proxy. Push creates/updates files and never deletes them. Up to 100 file actions are batched per commit; larger pushes create several commits. This is a local precaution, not a GitLab file-count limit. The REST client does not supply automatic throttling/retries; instance request-size and rate limits still apply.</li>
</ul>
<h3>Serve the browser tool</h3>
<p>Unlike generated articles, the builder must be served over HTTP(S), not opened with <code>file://</code>, because browsers block Pyodide asset loading there. From a source checkout, serve the directory containing both <code>lightwebpres</code> and <code>web/</code>:</p>
<pre><code class="language-bash">
python3 -m http.server 8000 --bind 127.0.0.1 --directory /path/to/lightwebpres
  </code></pre>
<p>Open <code>http://localhost:8000/web/index.html</code>. A mistaken <code>file://</code> opening shows a fix command computed from the page's location, with a Copy button.</p>
<p>For deployment, keep <code>vendor/</code>, <code>app.py</code> and <code>git_sync.py</code> with the page. It looks for the executable first at <code>./lightwebpres</code>, then <code>../lightwebpres</code>. The first layout serves the contents of <code>web/</code> as a site root with the executable alongside; the second is the repository layout above. Missing executable and <code>.mjs</code> MIME errors are covered in specifications.md §23.6 and §23.7. <code>web/.htaccess</code> supplies Apache MIME handling where overrides are allowed. This lightweight builder is not the separate <code>lightwebpres-gui</code> editor project.</p>
<h2 id="10-automate-and-maintain" tabindex="-1">10. Automate and maintain</h2>
<p>Every CLI command runs unattended. <code>verify</code> fails on output drift; <code>audit --strict</code> fails on warnings, including render failures. Plain <code>audit</code> reports without failing. The CLI has no third-party dependency or network requirement at build time, so a Python runner can build upstream Markdown. Sanitize untrusted upstream HTML first (section 7).</p>
<h3>Build in CI</h3>
<p><code>init --gitlab-ci</code> optionally writes this build-and-artifact job. It does not configure a public hosting deployment; a plain <code>init</code> emits no CI file.</p>
<pre><code class="language-yaml">
stages:
  - build

build:
  stage: build
  image: python:3.12-slim
  script:
    - python3 lightwebpres build . --lang fr
  artifacts:
    paths:
      - public/
  </code></pre>
<p>The Python command works on other runners too. If <code>public/</code> is committed, check it <strong>before</strong> rebuilding, so build does not erase evidence of drift:</p>
<pre><code class="language-yaml">
  script:
    - python3 lightwebpres verify . --lang fr
    - python3 lightwebpres build . --lang fr
  </code></pre>
<p>A fresh checkout with no committed output needs a build, not that initial drift gate. Match rendering options in <code>verify</code>, including language, themes and <code>--no-essential-theme</code>. It cannot reproduce <code>--inline-images</code>.</p>
<h3>Watch, target builds and record provenance</h3>
<pre><code class="language-bash">
./lightwebpres watch my-series --lang en --serve --port 8000 --open
./lightwebpres build my-series --lang en --only first-page.md
  </code></pre>
<p><code>watch</code> polls sources, <code>series.json</code>, templates and presentation dependencies, split and legacy language packs. It notices new files and keeps watching after a failed rebuild. Serving is opt-in, on <code>127.0.0.1</code>; it is a local preview, not a public deployment server.</p>
<p><code>--only</code> targets one article only when the navigation cache is safe. It still refreshes derived outputs (index, README and assets according to options, manifest and cache); changes affecting index/navigation trigger a full build. <code>--nav-cache path</code> relocates the fingerprint, normally <code>.lwp-cache/nav.json</code>. That cache is derived state and can be deleted, not hand-edited. <code>--build-stamp</code> records version and time on the pages; <code>--build-stamp-minimal</code> keeps a marker without either and takes precedence. <code>status: draft</code> and <code>ignored</code> control which articles enter normal output (section 4).</p>
<h3>Paths and CLI conventions</h3>
<table class="comparison-table">
<thead>
<tr>
<th>Variable</th>
<th>Replaces</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>LWP_SERIES_DIR</code></td>
<td>Default series directory when no directory argument is given</td>
</tr>
<tr>
<td><code>LWP_SOURCES_DIR</code>, <code>LWP_TEMPLATES_DIR</code>, <code>LWP_OUTPUT_DIR</code></td>
<td>Source, customization and output roots</td>
</tr>
<tr>
<td><code>LWP_INTERFACE_DIR</code>, <code>LWP_TYPOGRAPHY_DIR</code>, <code>LWP_LANGUAGE_DIR</code></td>
<td>Split or legacy language roots</td>
</tr>
<tr>
<td><code>LWP_LANG</code></td>
<td>Build language fallback and explicit interface language</td>
</tr>
<tr>
<td><code>LWP_THEMES_DIR</code>, <code>LWP_IDENTITY_KITS_DIR</code>, <code>LWP_COMMONS_DIR</code></td>
<td>User theme, Identity Kit and Commons preset catalogues</td>
</tr>
</tbody>
</table>
<p>Default series subdirectories live under the selected series root. An explicit relative <code>--output path</code> is relative to the current working directory, <strong>not</strong> to the series argument. Use absolute paths in pipelines when the working directory is not fixed.</p>
<p><code>--lang</code>, <code>--quiet</code>, <code>--verbose</code>, <code>--no-color</code>, <code>--timestamp</code> and <code>--dry-run</code> can precede the command; the value nearest the command wins. <code>--quiet</code> suppresses progress, not warnings or requested report values. <code>--verbose</code> adds detail; <code>--timestamp</code> prefixes logs with RFC 3339 timestamps. <code>--dry-run</code> journals writes without touching disk. <code>--option=value</code> and <code>--option value</code> are equivalent. Unknown or misplaced options are fatal. <code>--version</code> is a leading action, not a command modifier.</p>
<p>Shortcuts such as <code>build</code> also have canonical forms such as <code>series build</code>. Retired spellings (<code>install</code>, <code>check</code>, <code>themes</code>, <code>theme-info</code>, <code>set-theme</code>, <code>series-info</code>, <code>refresh-templates</code>, <code>themes-gallery</code>) fail with the replacement command; do not use them in scripts. Run <code>python3 lightwebpres --help</code> for the full command/option matrix, or <code>python3 lightwebpres build --help</code> for context.</p>
<h3>Upgrade the executable and templates</h3>
<p>Replace the project's executable with a newer release, read <code>CHANGELOG.md</code>, then audit, rebuild and inspect the output. The composed stylesheet and built-in navigation/language packs follow the executable. Your theme choice, property pins and <code>custom.css</code> remain yours.</p>
<p>A tool-owned file installed by <code>template write</code> takes precedence over the built-in copy. Builds warn when it differs, even with <code>--quiet</code>; the tool cannot tell a stale override from an intentional customization. Older series (before v0.40.0) received copies automatically. To resume following built-ins:</p>
<pre><code class="language-bash">
./lightwebpres template update my-series
./lightwebpres template update my-series --scaffold
  </code></pre>
<p>An identical tool-owned copy is removed. A differing <code>nav.js</code> is backed up as <code>nav.js.bak</code> and removed. Differing interface or typography packs are kept and reported; compare against <code>template show</code> before deleting them. Packs for languages not shipped by the tool are left alone. Missing <code>settings.conf</code> and <code>custom.css</code> are created. <code>--scaffold</code> also refreshes the commented settings surface while keeping every pinned line.</p>
<p><code>template show nav.js</code>, <code>template show interface/en.json</code> and <code>template show typography/en.json</code> print built-ins without a series. Use <code>template write &lt;file&gt; my-series</code> to install a copy to modify, and <code>--force</code> only to replace an existing copy. Legacy <code>fr.json</code>/<code>en.json</code> remain supported.</p>
<h3>Shell completion</h3>
<p><code>lightwebpres completion --shell bash</code> (or <code>zsh</code>) prints a script that makes your shell complete commands, subcommands, and options when you press Tab. Install it by adding this line to your <code>~/.bashrc</code> or <code>~/.zshrc</code>:</p>
<pre><code class="language-bash">
eval "$(lightwebpres completion --shell bash)"
  </code></pre>
<p>Then <code>lightwebpres &lt;Tab&gt;</code> proposes <code>init</code>, <code>build</code>, <code>verify</code>, <code>audit</code>, <code>theme</code>, <code>series</code>, etc.; <code>lightwebpres series &lt;Tab&gt;</code> proposes <code>build</code>, <code>theme</code>, <code>status</code>, <code>resolve</code>...; and <code>lightwebpres build --&lt;Tab&gt;</code> proposes <code>--lang</code>, <code>--output</code>, <code>--no-typography</code>, etc.</p>
<p>The script is generated from the tool's own command tables, so it stays in sync with whatever commands the version you are running knows about.</p>
<h2 id="11-troubleshooting-and-references" tabindex="-1">11. Troubleshooting and references</h2>
<h3>When something does not work</h3>
<table class="comparison-table">
<thead>
<tr>
<th>Symptom</th>
<th>Check or fix</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>lightwebpres: command not found</code></td>
<td>Use <code>python3 lightwebpres</code>, <code>./lightwebpres</code> or its actual path; a bare name needs <code>PATH</code> configuration.</td>
</tr>
<tr>
<td><code>Permission denied</code> on Unix</td>
<td><code>chmod +x lightwebpres</code>, or invoke through Python.</td>
</tr>
<tr>
<td>Windows cannot launch the file</td>
<td>Use <code>python lightwebpres</code> or the <code>py lightwebpres</code> launcher; Windows does not use the shebang.</td>
</tr>
<tr>
<td><code>python3: command not found</code></td>
<td>Try <code>python</code> or <code>py</code> and check its version; install Python 3.8+ if absent.</td>
</tr>
<tr>
<td>Target directory is not empty</td>
<td>Prefer a new directory. Inspect existing files before deliberately choosing <code>init --force</code>.</td>
</tr>
<tr>
<td>Interface language surprises you</td>
<td>Without an explicit language the browser chooses; use <code>--lang en</code> or <code>fr</code> to lock it (section 6).</td>
</tr>
<tr>
<td>A <code>field:</code> line is literal text</td>
<td>Fields must precede body prose (section 3).</td>
</tr>
<tr>
<td>A note definition is literal text</td>
<td>Move it out of a raw HTML block; labels allow letters, digits and underscores, not hyphens.</td>
</tr>
<tr>
<td>A note marker is not a link</td>
<td>Define it in the same locality; <code>audit</code> names unmatched calls.</td>
</tr>
<tr>
<td>A title or color ignores your edit</td>
<td><code>resolve my-series page_title --article first-page.md</code> or <code>resolve my-series kicker.fg</code> shows the winning and losing levels.</td>
</tr>
<tr>
<td>An article is absent</td>
<td>Check registration, <code>status</code>, article tags and effective slides with <code>status</code> and <code>series tags</code>.</td>
</tr>
<tr>
<td>An old page remains online</td>
<td>Review local <code>clean</code>, then remove stale files on the host too (section 7).</td>
</tr>
<tr>
<td><code>verify</code> reports drift after an unchanged build</td>
<td>Match rendering options; inline-image builds need a separate non-inline verification output.</td>
</tr>
<tr>
<td>Builder fails under <code>file://</code> or on <code>.mjs</code></td>
<td>Serve the builder and check executable placement/MIME types (section 9).</td>
</tr>
</tbody>
</table>
<h3>Command routes</h3>
<table class="comparison-table">
<thead>
<tr>
<th>Task</th>
<th>Commands and chapter</th>
</tr>
</thead>
<tbody>
<tr>
<td>Create and preview</td>
<td><code>init</code>, <code>demo</code>, <code>build</code>, <code>watch</code> (1, 2, 10)</td>
</tr>
<tr>
<td>Inspect content and names</td>
<td><code>status</code>, <code>series tags</code>, <code>series slug</code>, <code>resolve</code>, <code>contract</code> (3, 4, 7)</td>
</tr>
<tr>
<td>Fill missing slide identities</td>
<td><code>series slug set --dry-run</code>, then <code>series slug set</code> (3)</td>
</tr>
<tr>
<td>Select a presentation</td>
<td><code>preset list/show</code>, <code>series preset</code>, <code>series preset set</code> (5)</td>
</tr>
<tr>
<td>Choose or carry themes</td>
<td><code>theme list/show/gallery/create/migrate/vendor/path</code>, <code>series theme</code>, <code>series theme set</code> (5)</td>
</tr>
<tr>
<td>Check and remove stale output</td>
<td><code>audit</code>, <code>verify</code>, <code>clean</code> (7)</td>
</tr>
<tr>
<td>Manage overrides</td>
<td><code>template show/write/update</code> (10)</td>
</tr>
<tr>
<td>Discover syntax</td>
<td><code>--help</code>, contextual <code>--help</code>, <code>--version</code>, <code>completion</code> (10)</td>
</tr>
</tbody>
</table>
<p><code>theme create</code> additionally accepts <code>--label</code>, <code>--family</code>, <code>--source</code>, <code>--note</code>, <code>--output</code> (a <code>&lt;slug&gt;.conf</code> destination) and <code>--force</code>. <code>theme show --all</code> describes the catalogue; <code>--format json</code> makes reports machine-readable. <code>theme vendor --force</code> replaces existing vendored snapshots. <code>theme gallery --output path</code> chooses its HTML destination. These catalogue operations are explicit: a normal build does not overwrite your theme files.</p>
<h3>Deeper reference</h3>
<ul>
<li><strong><code>SKILL.md</code></strong> (<code>agent/skills/lightwebpres/</code>) — the precise mechanics of the article format: every slide type and field, the meta block, the field/free-text switch, typography and its opt-outs, <code>series.json</code> wiring. Read it before writing or debugging an article by hand, or point an agent at it.</li>
<li><a href="https://github.com/Fade78/lightwebpres/blob/main/agent/skills/sourced-presentation/SKILL.md">Guest sourced-presentation skill</a> is an optional, independent editorial method, not a product requirement.</li>
<li><strong><code>specifications.md</code></strong> (in French) — the complete, authoritative reference: exact algorithms, every parser edge case, the full <code>series.json</code> and language-file schemas, the browser tool's internals.</li>
<li><strong><code>lightwebpres --help</code></strong> — every command, every flag, every environment variable.</li>
<li><a href="https://github.com/Fade78/lightwebpres/blob/main/GLOSSARY.md">GLOSSARY.md</a> lists field meanings, defaults and fallback chains.</li>
<li><a href="https://github.com/Fade78/lightwebpres/blob/main/AGENTS.md">AGENTS.md</a> describes contributor rules and regeneration commands; <a href="https://github.com/Fade78/lightwebpres/blob/main/DECISIONS.md">DECISIONS.md</a> records decisions and outstanding work.</li>
</ul>