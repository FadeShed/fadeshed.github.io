<!-- lwp:meta -->
page_title: Guide de LightWebPres — LightWebPres
page_desc: Lire, créer et publier.
card_title: Guide de LightWebPres
card_desc: Lire, créer et publier.
card_label: GUIDE
nav_title: Guide de LightWebPres
nav_desc: Lire, créer et publier.
---

<!-- lwp:slide:cover -->
slug: lightwebpres
kicker: Manuel du produit
# LightWebPres
summary: Une source Markdown pour lire et présenter. Commencez par cet aperçu, puis consultez le manuel opérationnel complet ci-dessous.

 



---

<!-- lwp:slide -->
slug: ce-qu-il-fait
kicker: Sortie
## Des pages qui emportent leur moteur de lecture

 

<div class="fact-box">
<div class="fact-label">Ce qu’il faut publier</div>
<div class="fact-content"> <p>Chaque article est un fichier HTML contenant son CSS et son JavaScript. Le build produit aussi un index de série et la navigation. Publiez <strong>public/,</strong> avec les images référencées et les assets des Identity Kits, sur un hébergement statique.</p>
<p>Les lecteurs ont besoin d’un navigateur, pas de Python ni de LightWebPres. La source reste du texte ; ce manuel explique l’utilisation de l’outil, pas une méthode éditoriale.</p></div>
</div>
<p class="source">Source : Guide, chapitres 1 et 7</p>

---

<!-- lwp:slide -->
slug: trois-commandes
kicker: Démarrer
## Deux commandes pour voir un site qui fonctionne

 

<div class="fact-box">
<div class="fact-label">La démo, puis votre article</div>
<div class="fact-content"> <p>Lancez <code>python3 lightwebpres init my-series</code>, puis <code>python3 lightwebpres demo my-series --lang fr</code>. <strong>Demo construit déjà les pages.</strong> Ouvrez <code>my-series/public/index.html</code>.</p>
<p>Créez ensuite <code>sources/first-page.md</code>, déclarez son nom dans <code>series.json</code> et lancez <code>build --lang fr --open</code>. Le manuel donne la source et le JSON complets, puis les commandes <code>audit</code> et <code>verify</code>. Aucun build supplémentaire n’est nécessaire avant cette modification.</p></div>
</div>
<p class="source">Source : Guide, chapitres 1 et 2</p>

---

<!-- lwp:slide -->
slug: anatomie
kicker: Anatomie
## Quatre types de fiches, un fichier source

 

<div class="highlight"><span class="highlight-figure">4</span><span class="highlight-caption">cover, standard, series-nav et full-article</span></div>
<div class="fact-box">
<div class="fact-label">Les champs, puis le texte</div>
<div class="fact-content"> <p>Une couverture fournit le titre. Une fiche standard accepte du texte, des images, des tableaux, des notes et des composants nommés facultatifs. Une fiche series-nav génère des liens ; une fiche full-article inclut un fichier Markdown séparé.</p>
<p>Chaque fiche déclare son <code>slug:</code> stable. Les champs occupent une seule ligne physique, sauf les continuations indentées de <code>note:</code> et <code>comment:</code>. Après le début du texte libre, les lignes ressemblant à des champs restent elles aussi du texte.<sup class="note-call"><a href="#note-anatomie-1" id="noteref-anatomie-1" role="doc-noteref">1</a></sup></p>
<div class="notes-local">
<ol class="note-body">
<li id="note-anatomie-1" role="doc-footnote"><span class="note-num">1</span><code>lightwebpres contract</code> expose les champs acceptés et des squelettes analysables. <code>note:</code> est du HTML public pour le panneau présentateur ; <code>comment:</code> reste dans les sources. Les notes de bas de page comme celle-ci sont des références accessibles au lecteur, pas des notes de présentation.<a aria-label="Revenir au texte" class="note-back" data-lwp-i18n-aria-label="note_back" href="#noteref-anatomie-1" role="doc-backlink">↩</a></li>
</ol>
</div></div>
</div>
<p class="source">Source : Guide, chapitre 3</p>

---

<!-- lwp:slide -->
slug: tags
kicker: Séries
## Ordonner les articles et examiner leur visibilité

 

<div class="fact-box">
<div class="fact-label">Inscription et filtrage sont distincts</div>
<div class="fact-content"> <p>Le tableau <code>articles</code> de <code>series.json</code> fixe l’ordre de l’index et de la navigation. Seul <code>page_source</code> est obligatoire pour chaque entrée. <code>status</code> affiche les métadonnées résolues ; <code>series tags</code> décrit la visibilité effective des articles et des fiches sans construire.</p>
<p>Les tags d’article conditionnent l’article, ceux des fiches conditionnent son contenu. Les fiches sans tag sont communes aux sélections autres que default. <strong>L</strong> ouvre le menu de tags ; <code>excluded</code> supprime une fiche au build. Les tags ne sont pas des droits d’accès.</p></div>
</div>
<p class="source">Source : Guide, chapitre 4</p>

---

<!-- lwp:slide -->
slug: identity-kits
kicker: Identité
## Une identité, des presets et des thèmes nommés

 

<div class="fact-box">
<div class="fact-label">Structure interne, sans remplacer le moteur</div>
<div class="fact-content"> <p>Un Identity Kit autonome fournit dispositions, chrome, assets et thèmes typés. LWP conserve l’enveloppe de page, la navigation et le script. Sélectionnez un preset avec <code>series_meta.presentation_preset</code> : <code>builtin/standard</code>, <code>commons/id</code> ou <code>id@version/preset</code>. Sans choix, Standard natif utilise le thème Light minimal ; les presets Commons associent des thèmes globaux aux dispositions natives. L’identité est déduite de la référence et son libellé reste fixe quand la sélection change.</p>
<p>Placez les alternatives à la racine de <code>series.json</code> avec <code>presentation_presets</code>, ou passez <code>--presentation-presets</code> à <code>build</code>, <code>verify</code> ou <code>watch</code>. Un preset principal de kit ou de Commons ajoute aussi <code>builtin/standard</code> après ces choix lorsqu’il est compatible ; une disposition ou un chrome propre au kit rend ce candidat implicite indisponible et produit un avertissement. Le choix principal reste premier ; <strong>C</strong> ouvre Identité, Preset et Thème et change tout le deck sans modifier ses sources. Le choix de session est propre au deck et à son catalogue. Applicable / Identité courante / Tous filtrent les choix publiés par compatibilité typée ou appartenance, pas par marque. Suivre le preset réinitialise un choix de thème explicite du lecteur.</p>
<p>Utilisez <code>preset list</code>, <code>preset show</code> et <code>series preset set</code> pour examiner ou modifier le choix. <code>init --preset</code> peut aussi installer le projet de départ du kit. <code>kit compose</code> construit un kit autonome à partir de fichiers explicites et d’un manifeste final complet. Les champs de fiche <code>slide-layout</code>, <code>slide-header</code> et <code>slide-footer</code> remplacent les valeurs par défaut.</p></div>
</div>
<p class="source">Source : Guide, chapitre 5</p>

---

<!-- lwp:slide -->
slug: gestes
kicker: Personnalisation
## Changer la plus petite couche qui répond au besoin

 

<div class="fact-box">
<div class="fact-label">Les valeurs d’abord, le CSS avancé si nécessaire</div>
<div class="fact-content"> <p>Un thème fournit la base. <code>settings.conf</code> épingle les valeurs de la série ; les métadonnées <code>style.*</code> modifient une page ; les tags d’instance modifient une expression. Le compilateur vérifie noms et valeurs des propriétés typées. <code>custom.css</code> ajoute des règles libres après la feuille de style composée.</p>
<p><code>resolve</code> explique une valeur surprenante, y compris les niveaux qui n’ont pas été retenus. <code>series theme</code> mesure les couleurs typées effectives ; il ne certifie pas le CSS personnalisé arbitraire et ne corrige pas une palette.</p></div>
</div>
<p class="source">Source : Guide, chapitre 5</p>

---

<!-- lwp:slide -->
slug: themes
kicker: Lire et présenter
## Garder les alternatives à portée de main

 

<div class="fact-box">
<div class="fact-label">La même page, un autre mode de lecture</div>
<div class="fact-content"> <p><strong>C</strong> ouvre le sélecteur de thèmes. Monochrome, Monochrome Night et Print Ink sont fournis par défaut ; <code>--no-essential-theme</code> les désactive. Sélectionnez Print Ink avant d’imprimer pour du noir sur blanc : l’impression conserve le thème actif.</p>
<p><strong>M</strong> ouvre le menu présentateur, <strong>F</strong> demande le plein écran, <strong>H</strong> liste les commandes et <strong>S</strong> partage un lien ou un QR code. Un écran projeté montre aussi le panneau de notes ouvert : <strong>N</strong> n’est pas une fenêtre privée de présentation.</p></div>
</div>
<p class="source">Source : Guide, chapitres 5 et 8</p>

---

<!-- lwp:slide -->
slug: pipeline
kicker: Automatisation
## Un moteur, au terminal ou dans le navigateur

 

<div class="fact-box">
<div class="fact-label">Construire, examiner, maintenir</div>
<div class="fact-content"> <p>Le CLI fonctionne sans interaction avec la bibliothèque standard Python. <code>watch</code> reconstruit après modification ; <code>--only</code> cible un article lorsque le cache de navigation le permet. Les packs linguistiques séparent les libellés d’interface de la typographie appliquée au build.</p>
<p>Le constructeur web utilise le même exécutable sous Pyodide : importez un ZIP de série, ou récupérez, construisez et envoyez avec GitLab. Servez-le en HTTP(S). Assainissez les entrées non fiables en amont : le moteur laisse passer le HTML brut.</p></div>
</div>
<p class="source">Source : Guide, chapitres 6, 9 et 10</p>

---

<!-- lwp:slide -->
slug: verifications
kicker: Publication
## Deux contrôles, deux questions différentes

 

<div class="fact-box">
<div class="fact-label">Le bon contrôle pour la bonne question</div>
<div class="fact-content"> <p><code>audit</code> rend en mémoire et signale les avertissements de source et de style sans écrire de sortie. Sans option stricte, il sort avec zéro ; <code>--strict</code> transforme les avertissements en contrôle bloquant. <code>verify</code> compare un nouveau rendu en mémoire aux fichiers sur disque et échoue en cas d’écart. Utilisez les mêmes options de rendu prises en charge que pour le build.</p>
<p><strong>Examinez les pages avant de publier.</strong> Verify ne reproduit pas <code>--inline-images</code>. Supprimer un article n’efface pas un ancien fichier hébergé ; examinez <code>clean</code> en local et les fichiers périmés de l’hôte séparément.</p></div>
</div>
<p class="source">Source : Guide, chapitre 7</p>

---

<!-- lwp:slide -->
slug: reader-controls
## La lecture, à votre échelle.
summary: Touchez le menu du lecteur : le zoom ne nécessite pas de clavier.

Utilisez **−**, **+** et **Réinitialiser** pour le zoom de présentation ; le pourcentage indique son niveau. Le pincement reste le zoom natif du navigateur. Le menu propose aussi l’ajustement du texte et le défilement local des tableaux larges. Ces choix durent dans la page chargée, pas après son rechargement. Les cellules restent dans le document : la coupure visuelle ne supprime pas leur contenu.

---

<!-- lwp:slide:full-article -->
slug: guide-complet
article: article.md

---

<!-- lwp:slide:series-nav -->
slug: la-serie
