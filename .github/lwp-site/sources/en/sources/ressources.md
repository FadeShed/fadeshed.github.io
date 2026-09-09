<!-- lwp:meta -->
page_title: Documentation in the right place — LightWebPres
page_desc: The manual, exact format, examples and project sources.
card_title: Documentation in the right place
card_desc: The manual, exact format, examples and project sources.
card_label: 06 / GO FURTHER
nav_title: Documentation in the right place
nav_desc: The manual, exact format, examples and project sources.
---

<!-- lwp:slide:cover -->
slug: ouverture
kicker: 06 / GO FURTHER
# No magic.<br>Read it.<br>Inspect it.
summary: The site provides a route. The repository documents remain the references. Choose the reference for the task at hand.

---

<!-- lwp:slide -->
slug: manuel
kicker: TO USE THE TOOL
## A manual built with the tool it explains.
summary: The official guide combines a presentation and the complete manual in one page. The original technical references remain available in their source language.
source: <a href="reference/README.md">README · Find your route</a>; <a href="reference/GUIDE.md">GUIDE.md</a>.

<div class="lwp-web-resource-list"><a href="guide/guide.html"><strong>Interactive guide · EN</strong><span>Installation, writing, appearance, publishing and browser builds.</span><b aria-hidden="true">↗</b></a><a href="reference/README.md"><strong>Original README · EN</strong><span>The repository entry point.</span><b aria-hidden="true">↓</b></a><a href="reference/GLOSSARY.md"><strong>Glossary · EN</strong><span>Field meanings and fallback values.</span><b aria-hidden="true">↓</b></a><a href="reference/specifications.md"><strong>Normative specification · FR</strong><span>The full format and behaviour contract.</span><b aria-hidden="true">↓</b></a></div>

---

<!-- lwp:slide -->
slug: skills
kicker: TO WRITE WITH AN AGENT
## Two skills. Two different jobs.
summary: The lightwebpres skill describes the exact format. Sourced-presentation offers an optional editorial method.
source: <a href="reference/agent/skills/README.md">Skill index</a>.

<div class="lwp-web-resource-list"><a href="reference/agent/skills/lightwebpres/SKILL.md"><strong>lightwebpres / SKILL.md</strong><span>Read this to produce the correct syntax: fields, cards, slugs and series.</span><b aria-hidden="true">↓</b></a><a href="reference/agent/skills/sourced-presentation/SKILL.md"><strong>sourced-presentation / SKILL.md</strong><span>A method for connecting clear cards to a sourced long-form text.</span><b aria-hidden="true">↓</b></a><a href="downloads/skills.zip" download><strong>Both skills, with their references</strong><span>A complete archive, not just the entry files.</span><b aria-hidden="true">↓</b></a></div>

Skipping the method does not prevent a build. Ignoring the format contract leads to syntax the engine will not accept. `AGENTS.md` addresses something else again: working **on the repository**.

---

<!-- lwp:slide -->
slug: exemples
kicker: TO TRY IT
## Start with something that works.
summary: These links lead to the tools and their output. Downloads stay on this site.
source: <a href="reference/GUIDE.md">Guide · First personal article and Build in the browser</a>.

<div class="lwp-web-resource-list"><a href="demo/library.html"><strong>An illustrated briefing</strong><span>A minimal example compiled by the repository engine.</span><b aria-hidden="true">↗</b></a><a href="themes.html"><strong>The theme gallery</strong><span>Rendered pages with the generator's filters.</span><b aria-hidden="true">↗</b></a><a href="web/index.html"><strong>The web builder</strong><span>The same engine under Pyodide. Requires HTTP(S).</span><b aria-hidden="true">↗</b></a><a href="downloads/demarrage.zip" download><strong>The starter project</strong><span>Sources, series, engine and licences. Edit, then build.</span><b aria-hidden="true">↓</b></a></div>

---

<!-- lwp:slide -->
slug: ce-site
kicker: THE SITE DEMONSTRATES ITSELF
## Read the site. Explore its sources.
summary: The home page is a series index. The routes are LWP articles. The kit, themes and CSS remain inspectable sources.
source: <a href="downloads/site-sources.zip">This site's build sources</a>; <a href="reference/AGENTS.md">Repository rules</a>.

`series.json` orders the routes. `sources/` contains their text. `templates/kits/lightwebpres-site/1.0.0/` carries the identity. The `build-site.py` script calls the engine without modifying it.

The guide and gallery are regenerated with existing tools. The build prepares a new output directory so stale files are not retained.

<div class="lwp-web-actions"><a class="lwp-web-button" href="downloads/site-sources.zip" download>Explore the sources ↓</a><a href="https://github.com/Fade78/lightwebpres">Browse the repository ↗</a></div>

---

<!-- lwp:slide -->
slug: versions
## Keep exploring. Share what you find.
summary: Browse the source, follow the project or describe a problem you encounter.

<div class="lwp-web-actions"><a class="lwp-web-button" href="https://github.com/Fade78/lightwebpres">Open the repository →</a></div><div class="lwp-web-actions"><a class="lwp-web-button" href="https://github.com/Fade78/lightwebpres/issues">Report an issue →</a></div>

---

<!-- lwp:slide:series-nav -->
slug: continuer
