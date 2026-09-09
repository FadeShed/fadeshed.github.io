<!-- lwp:meta -->
page_title: Your ideas. Their own address.
page_desc: An example LightWebPres page, ready to edit and share.
---

<!-- lwp:slide:cover -->
slug: vos-idees
kicker: Over to you
# Your ideas.<br>Their own address.
summary: One text. One page. To read and present.

---

<!-- lwp:slide -->
slug: une-page-a-vous
kicker: The result
## A page of your own.
summary: The browser reads this page without installing LightWebPres.
highlight: 1 HTML
highlight-caption: per article, with its CSS and JavaScript
fact-label: Keep the assets too
source: LightWebPres project README · What you get.

Local images stay in **img/**. Kit assets stay in **assets/presentations/**. Publish the entire **public/** directory, not just its index.

---

<!-- lwp:slide -->
slug: a-vous-decrire
kicker: What is next
## Your turn to write.
summary: Edit sources/ma-page.md and rebuild the project.

```bash
python3 lightwebpres build . --lang en
```

Then open `public/index.html`. Keep previously shared slugs even when you change the titles.

---

<!-- lwp:slide:series-nav -->
slug: la-serie
