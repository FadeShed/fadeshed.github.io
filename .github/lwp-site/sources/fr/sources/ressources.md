<!-- lwp:meta -->
page_title: La documentation, au bon endroit — LightWebPres
page_desc: Le manuel, le format exact, les exemples et les sources du projet.
card_title: La documentation, au bon endroit
card_desc: Le manuel, le format exact, les exemples et les sources du projet.
card_label: 06 / ALLER PLUS LOIN
nav_title: La documentation, au bon endroit
nav_desc: Le manuel, le format exact, les exemples et les sources du projet.
---

<!-- lwp:slide:cover -->
slug: ouverture
kicker: 06 / ALLER PLUS LOIN
# Pas de magie.<br>Tout se lit.<br>Tout s’inspecte.
summary: Le site donne un chemin. Les documents du dépôt restent les références. Les originaux ci-dessous sont ceux du moteur utilisé pour cette construction.

---

<!-- lwp:slide -->
slug: manuel
kicker: POUR UTILISER L’OUTIL
## Un manuel, construit avec ce qu’il explique.
summary: Le guide officiel réunit une présentation et le manuel intégral dans une même page. Il est conservé dans sa langue d’origine, l’anglais.
source: <a href="reference/README.md">README · Find your route</a> ; <a href="reference/GUIDE.md">GUIDE.md</a>.

<div class="lwp-web-resource-list"><a href="guide/guide.html"><strong>Guide interactif · EN</strong><span>Installation, écriture, apparence, publication, navigateur.</span><b aria-hidden="true">↗</b></a><a href="reference/README.md"><strong>README original · EN</strong><span>L’entrée du dépôt, sans réécriture parallèle.</span><b aria-hidden="true">↓</b></a><a href="reference/GLOSSARY.md"><strong>Glossaire</strong><span>Le sens des champs et leurs valeurs de repli.</span><b aria-hidden="true">↓</b></a><a href="reference/specifications.md"><strong>Spécification normative · FR</strong><span>Le contrat complet du format et du comportement.</span><b aria-hidden="true">↓</b></a></div>

---

<!-- lwp:slide -->
slug: skills
kicker: POUR ÉCRIRE AVEC UN AGENT
## Deux skills. Deux métiers différents.
summary: Le skill lightwebpres décrit le format exact. Sourced-presentation propose une méthode éditoriale facultative.
source: <a href="reference/agent/skills/README.md">Index des skills</a>.

<div class="lwp-web-resource-list"><a href="reference/agent/skills/lightwebpres/SKILL.md"><strong>lightwebpres / SKILL.md</strong><span>À lire pour produire la bonne syntaxe : champs, fiches, slugs et série.</span><b aria-hidden="true">↓</b></a><a href="reference/agent/skills/sourced-presentation/SKILL.md"><strong>sourced-presentation / SKILL.md</strong><span>Une méthode pour relier des fiches claires à un texte long sourcé.</span><b aria-hidden="true">↓</b></a><a href="downloads/skills.zip" download><strong>Les deux skills, avec leurs références</strong><span>Une archive complète, pas seulement les fichiers d’entrée.</span><b aria-hidden="true">↓</b></a></div>

Ignorer la méthode n’empêche pas le build. Ignorer le contrat de format conduit à écrire une syntaxe que le moteur n’accepte pas. `AGENTS.md` traite encore d’autre chose : travailler **sur le dépôt**.

---

<!-- lwp:slide -->
slug: exemples
kicker: POUR ESSAYER
## Commencez par quelque chose qui fonctionne.
summary: Ces liens mènent aux vrais outils et aux vraies sorties. Les téléchargements restent sur ce site.
source: <a href="reference/GUIDE.md">Guide · First personal article et Build in the browser</a>.

<div class="lwp-web-resource-list"><a href="demo/library.html"><strong>Un dossier à explorer</strong><span>Un exemple minimal, compilé par le moteur du dépôt.</span><b aria-hidden="true">↗</b></a><a href="themes.html"><strong>La galerie des thèmes</strong><span>Des rendus réels, avec les filtres du générateur.</span><b aria-hidden="true">↗</b></a><a href="web/index.html"><strong>Le constructeur web</strong><span>Le même moteur sous Pyodide. Nécessite HTTP(S).</span><b aria-hidden="true">↗</b></a><a href="downloads/demarrage.zip" download><strong>Le projet de démarrage</strong><span>Sources, série, moteur et licences. Modifiez, puis construisez.</span><b aria-hidden="true">↓</b></a></div>

---

<!-- lwp:slide -->
slug: ce-site
kicker: LE SITE SE MONTRE LUI-MÊME
## Lisez le site. Explorez ses sources.
summary: L’accueil est un index de série. Les parcours sont des articles LWP. Le kit, les thèmes et le CSS restent des sources inspectables.
source: <a href="downloads/site-sources.zip">Sources de construction de ce site</a> ; <a href="reference/AGENTS.md">Règles du dépôt</a>.

`series.json` ordonne les parcours. `sources/` contient leur texte. `templates/kits/lightwebpres-site/1.0.0/` porte l’identité. Le script `build-site.py` appelle le moteur sans le modifier.

Le guide et la galerie sont régénérés avec les outils existants. La construction prépare un nouveau dossier de sortie pour ne pas conserver de fichiers périmés.

<div class="lwp-web-actions"><a class="lwp-web-button" href="downloads/site-sources.zip" download>Ouvrir les coulisses ↓</a><a href="https://github.com/Fade78/lightwebpres">Voir le dépôt ↗</a></div>

---

<!-- lwp:slide -->
slug: versions
## Continuez à explorer. Partagez vos retours.
summary: Explorez les sources, suivez le projet ou décrivez un problème rencontré.

<div class="lwp-web-actions"><a class="lwp-web-button" href="https://github.com/Fade78/lightwebpres">Ouvrir le dépôt →</a></div><div class="lwp-web-actions"><a class="lwp-web-button" href="https://github.com/Fade78/lightwebpres/issues">Signaler un problème →</a></div>

---

<!-- lwp:slide:series-nav -->
slug: continuer
