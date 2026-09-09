<!-- lwp:meta -->
page_title: Vos idées. Leur propre adresse.
page_desc: Un exemple de page LightWebPres, prêt à être modifié et partagé.
---

<!-- lwp:slide:cover -->
slug: vos-idees
kicker: À vous de jouer
# Vos idées.<br>Leur propre adresse.
summary: Un texte. Une page. À lire et à présenter.

---

<!-- lwp:slide -->
slug: une-page-a-vous
kicker: Le résultat
## Une page à vous.
summary: Le navigateur lit cette page sans installer LightWebPres.
highlight: 1 HTML
highlight-caption: par article, avec son CSS et son JavaScript
fact-label: Gardez aussi les assets
source: README.md du projet LightWebPres · What you get.

Les images locales restent dans **img/**. Les assets des kits restent dans **assets/presentations/**. Publiez tout le dossier **public/**, pas uniquement son index.

---

<!-- lwp:slide -->
slug: a-vous-decrire
kicker: La suite
## À vous d’écrire.
summary: Modifiez sources/ma-page.md et reconstruisez le projet.

```bash
python3 lightwebpres build . --lang fr
```

Ouvrez ensuite `public/index.html`. Conservez les slugs déjà partagés, même si vous changez les titres.

---

<!-- lwp:slide:series-nav -->
slug: la-serie
