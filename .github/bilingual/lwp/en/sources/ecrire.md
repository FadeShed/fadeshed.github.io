<!-- lwp:meta -->
page_title: Text, with a little structure — LightWebPres
page_desc: Four card types, explicit fields and free-form Markdown.
card_title: Text, with a little structure
card_desc: Four card types, explicit fields and free-form Markdown.
card_label: 03 / WRITE
nav_title: Text, with a little structure
nav_desc: Four card types, explicit fields and free-form Markdown.
---

<!-- lwp:slide:cover -->
slug: ouverture
kicker: 03 / WRITE
# A small grammar.<br>Room for<br>the substance.
summary: A series contains articles. An article contains cards and, when needed, a long-form text. Here is the contract to know.

---

<!-- lwp:slide -->
slug: quatre-types
kicker: THE STRUCTURE
## Four card types. No new type to invent.
summary: Each card starts with a marker, has an explicit slug, and is separated from the next by a line of three hyphens.
source: <a href="reference/agent/skills/lightwebpres/SKILL.md">Format skill · Slide types</a>.

| Type | Its role |
| --- | --- |
| `cover` | A title, a kicker and a summary. No free-form body. |
| `standard` | Content: text, a key number, a callout, code, an image or a table. |
| `series-nav` | Links to the other articles, generated from the series. |
| `full-article` | A long-form Markdown file, included in the same page. |

The `<!-- lwp:slide -->` marker is enough for a standard card. `series-nav` appears at most once per article.

---

<!-- lwp:slide -->
slug: champs-avant-texte
kicker: THE RULE THAT PREVENTS SURPRISES
## Fields first. Text afterwards.
summary: As soon as a line is no longer a recognized field, the rest of the card becomes free-form text. The parser does not go back.
source: <a href="reference/agent/skills/lightwebpres/SKILL.md">Format skill · The one idea that matters most</a>.

<pre><code>&lt;!-- lwp:slide --&gt;
slug: my-idea
kicker: A key point
## A title that says something
summary: A sentence that sets the context.
fact-label: Remember

The body accepts **Markdown**.
The fields above do not render it.</code></pre>

A scalar field occupies **one physical line**. Only `note:` and `comment:` accept indented continuations. A field placed after the body becomes text, not a setting.

---

<!-- lwp:slide -->
slug: fichier-complet
kicker: THE SMALLEST USEFUL EXAMPLE
## A file you can build.
summary: This is the start of an article, not just an isolated card.
source: <a href="reference/agent/skills/lightwebpres/SKILL.md">Format skill · Anatomy of a file and Adding an article</a>.

<pre><code>&lt;!-- lwp:meta --&gt;
page_title: My first page
&#45;&#45;&#45;

&lt;!-- lwp:slide:cover --&gt;
slug: welcome
# My first page
summary: An idea to read and present.</code></pre>

Save it in `sources/ma-page.md`. In the `articles` array of `series.json`, add `{"page_source": "ma-page.md"}`. Filenames are simple names, without a path.

The `slug` is the card's address: keep it even when its title changes.

---

<!-- lwp:slide -->
slug: notes-et-liens
kicker: EXPLICIT BOUNDARIES
## What is visible, what is published.
summary: Presentation notes are in the HTML. Working comments stay in the sources.
source: <a href="reference/agent/skills/lightwebpres/SKILL.md">Format skill · Speaker notes and Full-article file</a>.

| Written as | What the reader receives |
| --- | --- |
| `note:` | A note accessible in the speaker panel. It is not private. |
| `comment:` | Nothing: the comment is not published. |
| `[title](https://…)` | An HTTP(S) Markdown link. |
| `<a href="page.html">Title</a>` | A local link written in HTML. |

A relative Markdown link does not become a clickable link. A plain `---` splits cards: use `<hr>` for a visual rule inside the body.

---

<!-- lwp:slide -->
slug: texte-long
kicker: BEYOND THE CARDS
## The summary need not carry the whole explanation.
summary: A card can point to a long-form text included in the same article. Its file contains only Markdown, without LWP markers.
source: <a href="reference/agent/skills/lightwebpres/SKILL.md">Format skill · The full-article file</a>; <a href="reference/agent/skills/sourced-presentation/SKILL.md">Optional editorial method</a>.

<pre><code>&lt;!-- lwp:slide:full-article --&gt;
slug: full-explanation
article: explanation.md</code></pre>

The `sources/explanation.md` file can develop the sources, examples and limits that the cards summarize. The official guide does exactly that.

<div class="lwp-web-actions"><a class="lwp-web-button" href="guide/guide.html">Read the guide in LightWebPres ↗</a><a href="ressources.html#skills">Choose the right skill →</a></div>

---

<!-- lwp:slide:series-nav -->
slug: continuer
