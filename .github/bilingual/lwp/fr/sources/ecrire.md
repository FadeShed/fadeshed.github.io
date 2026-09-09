<!-- lwp:meta -->
page_title: Le texte, avec une structure légère — LightWebPres
page_desc: Quatre types de fiches, des champs explicites et du Markdown libre.
card_title: Le texte, avec une structure légère
card_desc: Quatre types de fiches, des champs explicites et du Markdown libre.
card_label: 03 / ÉCRIRE
nav_title: Le texte, avec une structure légère
nav_desc: Quatre types de fiches, des champs explicites et du Markdown libre.
---

<!-- lwp:slide:cover -->
slug: ouverture
kicker: 03 / ÉCRIRE
# Une petite grammaire.<br>De la place<br>pour le fond.
summary: Une série contient des articles. Un article contient des fiches et, au besoin, un texte long. Voici le contrat à connaître.

---

<!-- lwp:slide -->
slug: quatre-types
kicker: LA STRUCTURE
## Quatre types de fiches. Pas de type à inventer.
summary: Chaque fiche commence par un marqueur, porte un slug explicite et se sépare de la suivante par une ligne de trois tirets.
source: <a href="reference/agent/skills/lightwebpres/SKILL.md">Skill de format · Slide types</a>.

| Type | Son rôle |
| --- | --- |
| `cover` | Un titre, un kicker et un résumé. Pas de corps libre. |
| `standard` | Le contenu : texte, chiffre clé, encadré, code, image ou tableau. |
| `series-nav` | Les liens vers les autres articles, générés depuis la série. |
| `full-article` | Un fichier Markdown de fond, inclus dans la même page. |

Le marqueur `<!-- lwp:slide -->` suffit pour une fiche standard. `series-nav` apparaît au plus une fois par article.

---

<!-- lwp:slide -->
slug: champs-avant-texte
kicker: LA RÈGLE QUI ÉVITE LES SURPRISES
## Les champs d’abord. Le texte ensuite.
summary: Dès qu’une ligne n’est plus un champ reconnu, le reste de la fiche devient du texte libre. Le parseur ne revient pas en arrière.
source: <a href="reference/agent/skills/lightwebpres/SKILL.md">Skill de format · The one idea that matters most</a>.

<pre><code>&lt;!-- lwp:slide --&gt;
slug: mon-idee
kicker: Un point essentiel
## Un titre qui dit quelque chose
summary: Une phrase qui pose le contexte.
fact-label: À retenir

Le corps accepte le **Markdown**.
Les champs ci-dessus, eux, ne le rendent pas.</code></pre>

Un champ scalaire occupe **une seule ligne physique**. Seuls `note:` et `comment:` acceptent des continuations indentées. Un champ placé après le corps sera du texte, pas un réglage.

---

<!-- lwp:slide -->
slug: fichier-complet
kicker: LE PLUS PETIT EXEMPLE UTILE
## Un fichier que vous pouvez construire.
summary: Voici le début d’un article, pas seulement une fiche isolée.
source: <a href="reference/agent/skills/lightwebpres/SKILL.md">Skill de format · Anatomy of a file et Adding an article</a>.

<pre><code>&lt;!-- lwp:meta --&gt;
page_title: Ma première page
&#45;&#45;&#45;

&lt;!-- lwp:slide:cover --&gt;
slug: bienvenue
# Ma première page
summary: Une idée à lire et à présenter.</code></pre>

Enregistrez-le dans `sources/ma-page.md`. Dans le tableau `articles` de `series.json`, ajoutez `{"page_source": "ma-page.md"}`. Les noms de fichiers sont simples, sans chemin.

Le `slug` est l’adresse de la fiche : conservez-le même si son titre change.

---

<!-- lwp:slide -->
slug: notes-et-liens
kicker: DES LIMITES EXPLICITES
## Ce qui se voit, ce qui se publie.
summary: Les notes de présentation sont dans le HTML. Les commentaires de travail restent dans les sources.
source: <a href="reference/agent/skills/lightwebpres/SKILL.md">Skill de format · Speaker notes et Full-article file</a>.

| Écriture | Ce que le lecteur reçoit |
| --- | --- |
| `note:` | Une note accessible dans le panneau présentateur. Elle n’est pas privée. |
| `comment:` | Rien : le commentaire n’est pas publié. |
| `[titre](https://…)` | Un lien Markdown HTTP(S). |
| `<a href="page.html">Titre</a>` | Un lien local écrit en HTML. |

Un lien Markdown relatif ne devient pas un lien cliquable. Un simple `---` découpe les fiches : utilisez `<hr>` pour une ligne visuelle dans le corps.

---

<!-- lwp:slide -->
slug: texte-long
kicker: AU-DELÀ DES FICHES
## La synthèse n’a pas à porter toute l’explication.
summary: Une fiche peut renvoyer à un texte long inclus dans le même article. Son fichier ne contient que du Markdown, sans marqueur LWP.
source: <a href="reference/agent/skills/lightwebpres/SKILL.md">Skill de format · The full-article file</a> ; <a href="reference/agent/skills/sourced-presentation/SKILL.md">Méthode éditoriale facultative</a>.

<pre><code>&lt;!-- lwp:slide:full-article --&gt;
slug: explication-complete
article: explication.md</code></pre>

Le fichier `sources/explication.md` peut développer les sources, les exemples et les limites que les fiches résument. Le guide officiel fait exactement cela.

<div class="lwp-web-actions"><a class="lwp-web-button" href="guide/guide.html">Lire le guide dans LightWebPres ↗</a><a href="ressources.html#skills">Choisir le bon skill →</a></div>

---

<!-- lwp:slide:series-nav -->
slug: continuer
