<section id="reader-controls-detail"><h2>Contrôles de lecture au toucher</h2><p>Le menu du lecteur donne accès aux boutons de zoom − / + / Réinitialiser, au pourcentage, à l’ajustement du texte et au défilement local des tableaux. Aucun clavier n’est nécessaire pour ces commandes. Le pincement appartient au navigateur. Les choix de lecture sont propres à la page chargée.</p></section> 
<h1>LightWebPres — Guide</h1>
<p>Le manuel opérationnel de LightWebPres : créer une série, ajouter du contenu, configurer sa présentation, vérifier la sortie et la publier. Il traite des outils terminal et navigateur, pas du travail éditorial. Pour les règles exactes du parseur, consultez la <a href="https://github.com/Fade78/lightwebpres/blob/main/agent/skills/lightwebpres/SKILL.md" hreflang="en">référence du format (anglais)</a> ; pour les contrats normatifs, <a href="https://github.com/Fade78/lightwebpres/blob/main/specifications.md" hreflang="fr">specifications.md</a> (français).</p>
<ol>
<li><a href="#1-start-with-a-working-site" onclick="document.getElementById(this.hash.slice(1)).focus(); document.activeElement.scrollIntoView({behavior: 'instant'}); return false;">Partir d’un site qui fonctionne</a></li>
<li><a href="#2-make-your-first-personal-article" onclick="document.getElementById(this.hash.slice(1)).focus(); document.activeElement.scrollIntoView({behavior: 'instant'}); return false;">Créer votre premier article personnel</a></li>
<li><a href="#3-understand-page-anatomy" onclick="document.getElementById(this.hash.slice(1)).focus(); document.activeElement.scrollIntoView({behavior: 'instant'}); return false;">Comprendre l’anatomie d’une page</a></li>
<li><a href="#4-organize-a-series-and-tags" onclick="document.getElementById(this.hash.slice(1)).focus(); document.activeElement.scrollIntoView({behavior: 'instant'}); return false;">Organiser une série et ses tags</a></li>
<li><a href="#5-choose-presets-themes-and-customization" onclick="document.getElementById(this.hash.slice(1)).focus(); document.activeElement.scrollIntoView({behavior: 'instant'}); return false;">Choisir presets, thèmes et personnalisation</a></li>
<li><a href="#6-set-languages-and-typography" onclick="document.getElementById(this.hash.slice(1)).focus(); document.activeElement.scrollIntoView({behavior: 'instant'}); return false;">Régler les langues et la typographie</a></li>
<li><a href="#7-verify-and-publish" onclick="document.getElementById(this.hash.slice(1)).focus(); document.activeElement.scrollIntoView({behavior: 'instant'}); return false;">Vérifier et publier</a></li>
<li><a href="#8-present-print-and-share" onclick="document.getElementById(this.hash.slice(1)).focus(); document.activeElement.scrollIntoView({behavior: 'instant'}); return false;">Présenter, imprimer et partager</a></li>
<li><a href="#9-build-in-the-browser" onclick="document.getElementById(this.hash.slice(1)).focus(); document.activeElement.scrollIntoView({behavior: 'instant'}); return false;">Construire dans le navigateur</a></li>
<li><a href="#10-automate-and-maintain" onclick="document.getElementById(this.hash.slice(1)).focus(); document.activeElement.scrollIntoView({behavior: 'instant'}); return false;">Automatiser et entretenir</a></li>
<li><a href="#11-troubleshooting-and-references" onclick="document.getElementById(this.hash.slice(1)).focus(); document.activeElement.scrollIntoView({behavior: 'instant'}); return false;">Dépannage et références</a></li>
</ol>
<h2 id="1-start-with-a-working-site" tabindex="-1">1. Partir d’un site qui fonctionne</h2>
<p>Suivez le <a href="https://github.com/Fade78/lightwebpres/blob/main/README.md#quickstart" hreflang="en">démarrage rapide du README (anglais)</a> pour récupérer l’exécutable unique et lancer <code>init</code> puis <code>demo</code>. Python 3.8+ et sa bibliothèque standard suffisent, sans paquet supplémentaire. <code>demo</code> construit déjà le site ; ne relancez pas <code>build</code> avant de modifier quelque chose. Ouvrez <code>my-series/public/index.html</code>.</p>
<p>Les commandes de ce guide se lancent depuis le dossier contenant <code>lightwebpres</code> et <code>my-series/</code>. Sous Windows, utilisez <code>python lightwebpres</code> ou <code>py lightwebpres</code>. Les exemples avec <code>./lightwebpres</code> supposent Unix et <code>chmod +x lightwebpres</code> ; <code>python3 lightwebpres</code> fonctionne sans le bit exécutable.</p>
<p><code>init</code> prépare un projet : <code>sources/</code> (vide, pour vos fichiers <code>.md</code>), <code>templates/</code> (personnalisation : <code>settings.conf</code>, <code>custom.css</code> et éventuellement <code>themes/*.conf</code> versionnés, voir section 5), les dossiers vides <code>interface/</code>, <code>typography/</code> et l’ancien <code>language/</code>, un dossier de sortie <code>public/</code> vide, un <code>series.json</code> de départ et une copie de l’exécutable <code>lightwebpres</code> avec <code>COPYING</code> et <code>COPYING.EXCEPTION</code>. Le projet est ainsi autonome et le moteur voyage avec sa licence.</p>
<p>Le script de navigation et les packs linguistiques intégrés restent dans l’exécutable : les mises à jour atteignent la série sans rafraîchir de copies locales. Pour des remplacements voulus, utilisez <code>template show</code>/<code>template write</code> (section 10). <code>init --preset</code> peut aussi installer un Identity Kit et son projet de départ déclaré (section 5).</p>
<p>Le démarrage rapide d’origine utilise explicitement <code>--lang en</code>. Sans cette option ni <code>LWP_LANG</code>, le navigateur choisit la langue d’interface ; la typographie est déjà fixée au build. La section 6 explique les deux couches et les packs personnalisés.</p>
<p><code>demo</code> fonctionne seulement après <code>init</code> et refuse d’écraser un travail existant. Il ajoute trois articles d’exemple (première, médiane et dernière position de navigation) et une image légendée, pour disposer d’un résultat concret avant de rédiger.</p>
<p>Avec <code>demo --dry-run</code>, les fichiers et le build sont seulement décrits dans un plan ; la série existante sur disque n’est pas construite à la place de la démo prévue.</p>
<p><code>build</code> lit <code>series.json</code> et tous les articles déclarés, puis écrit <code>public/*.html</code> et <code>public/index.html</code>. Un <code>README.md</code> généré est placé à côté de <code>series.json</code>, à la racine de la série plutôt que dans <code>public/</code> : il décrit la série au lecteur du dépôt, pas au visiteur du site. Ouvrez l’index localement, sans serveur. Les images référencées restent des assets séparés par défaut. Le chapitre publication couvre la livraison en fichier unique, les options de sortie et le nettoyage ; commencez par ajouter votre article ci-dessous.</p>
<h2 id="2-make-your-first-personal-article" tabindex="-1">2. Créer votre premier article personnel</h2>
<p>Gardez la démo comme référence et ajoutez un article à côté. L’exemple suivant décrit les fichiers de sortie : il n’a besoin ni d’image externe ni d’un second Markdown. Sa source suivie produit aussi les captures de ce manuel : <a href="https://github.com/Fade78/lightwebpres/blob/main/examples/first-article/sources/first-page.md" hreflang="en">examples/first-article/sources/first-page.md</a>.</p>
<h3>Créer la source</h3>
<p>Dans votre éditeur, créez <code>my-series/sources/first-page.md</code> avec ce contenu :</p>
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
<h3>Le déclarer dans la série</h3>
<p>Ouvrez <code>my-series/series.json</code>. Ajoutez cet objet au tableau <code>articles</code> existant, avec une virgule après l’objet précédent :</p>
<pre><code class="language-json">
{"page_source": "first-page.md"}
  </code></pre>
<p>Conservez les entrées de démo et <code>series_meta</code> ; ne remplacez pas tout le fichier par cet objet. <code>page_source</code> contient seulement un nom de fichier, pas <code>sources/first-page.md</code>. L’ordre du tableau est celui de l’index et de la navigation.</p>
<p>Pour une série contenant <strong>uniquement</strong> votre article, voici un autre <code>series.json</code> complet (les sources de démo inutilisées peuvent rester sur disque) :</p>
<pre><code class="language-json">
{
  "series_meta": {"title": "My first series"},
  "articles": [{"page_source": "first-page.md"}]
}
  </code></pre>
<h3>Construire, ouvrir et vérifier</h3>
<pre><code class="language-bash">
python3 lightwebpres build my-series --lang en --open
python3 lightwebpres audit my-series --lang en
python3 lightwebpres verify my-series --lang en
  </code></pre>
<p>Si l’ouverture automatique n’est pas disponible, ouvrez <code>my-series/public/index.html</code> manuellement, puis sélectionnez <strong>My first page</strong>, le titre de l’exemple. Son fichier direct est <code>my-series/public/first-page.html</code> ; la fiche de contenu est <code>first-page.html#travels-with-the-page</code>. Vérifiez le titre, la fiche et les liens vers les articles de démo. <code>audit</code> signale les avertissements : lisez-les même si le code de sortie vaut zéro. <code>verify</code> ne devrait signaler aucun écart après ce build.</p>
<p>Modifiez le titre ou le corps et répétez cette boucle. Conservez chaque <code>slug:</code> publié : changer un titre ne change pas son adresse. Pour retirer la démo du site, supprimez ses entrées de <code>articles</code>, reconstruisez, puis examinez <code>clean</code> avant de supprimer les anciennes sorties (section 7).</p>
<p>La même fiche de contenu, construite avec le thème <code>nebula</code>, dans deux tailles de fenêtre de navigateur. Il s’agit d’une comparaison Chromium, pas d’une photographie d’appareil :</p>
<p align="center">
<img alt="The same Nebula content card shown in real landscape and emulated portrait browser viewports" src="img/product-responsive.png" width="100%"/>
</p>
<h2 id="3-understand-page-anatomy" tabindex="-1">3. Comprendre l’anatomie d’une page</h2>
<p>Une page est une suite de <strong>fiches</strong>, séparées par <code>---</code> et précédées d’un bloc de métadonnées. Il existe quatre types de fiches et, dans une fiche standard, quelques composants nommés. Cette section les nomme et explique comment les utiliser ; <code>agent/skills/lightwebpres/SKILL.md</code> fournit la syntaxe exacte et les cas limites.</p>
<p><strong>Les quatre types de fiches.</strong></p>
<table class="comparison-table">
<thead>
<tr>
<th>Type</th>
<th>Champs acceptés</th>
<th>Nombre</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>cover</code></td>
<td><code>slug</code>, <code>kicker</code>, <code>tags:</code>, <code># Title</code>, <code>summary</code>, <code>slide-layout</code>, <code>slide-header</code>, <code>slide-footer</code>, <code>comment</code>, <code>note</code></td>
<td>Sans limite, à tout emplacement : c’est une apparence, pas un marqueur structurel</td>
</tr>
<tr>
<td>standard <em>(par défaut)</em></td>
<td><code>slug</code>, <code>kicker</code>, <code>tags:</code>, <code>## Title</code>, <code>summary</code>, <code>highlight</code>, <code>highlight-caption</code>, <code>fact-label</code>, <code>fact-variant</code>, <code>source</code>, <code>slide-layout</code>, <code>slide-header</code>, <code>slide-footer</code>, <code>comment</code>, <code>note</code>, puis du Markdown libre</td>
<td>Autant que nécessaire</td>
</tr>
<tr>
<td><code>series-nav</code></td>
<td><code>slug</code>, <code>tags:</code>, <code>slide-layout</code>, <code>slide-header</code>, <code>slide-footer</code>, <code>comment:</code> — la navigation elle-même est générée depuis <code>series.json</code></td>
<td>0 ou 1 par article</td>
</tr>
<tr>
<td><code>full-article</code></td>
<td><code>slug</code>, <code>article: filename.md</code>, <code>tags:</code>, <code>slide-layout</code>, <code>slide-header</code>, <code>slide-footer</code> et <code>comment:</code></td>
<td>Sans limite, chacun avec son propre fichier</td>
</tr>
</tbody>
</table>
<p>Quatre types, et seulement quatre. Une faute comme <code>&lt;!-- lwp:slide:covre --&gt;</code> arrête le build, qui indique la fiche, votre saisie et les quatre noms acceptés. Vous n’aurez pas à le découvrir dans la page.</p>
<p><strong>Les composants d’une fiche standard.</strong></p>
<table class="comparison-table">
<thead>
<tr>
<th>Composant</th>
<th>À quoi il sert</th>
<th>Comment l’utiliser</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>encadré</strong></td>
<td>L’idée de la fiche, mise en évidence</td>
<td>Texte Markdown libre après une ligne <code>fact-label:</code></td>
</tr>
<tr>
<td><strong>chiffre clé</strong></td>
<td>Un nombre qui porte la fiche</td>
<td><code>highlight:</code> (et éventuellement <code>highlight-caption:</code>)</td>
</tr>
<tr>
<td><strong>source</strong></td>
<td>L’origine de l’affirmation</td>
<td><code>source:</code></td>
</tr>
<tr>
<td><strong>tableau comparatif</strong></td>
<td>Une grille de résultats lisible d’un coup d’œil</td>
<td>Un tableau Markdown ; les cellules reçoivent les classes <code>yes</code>, <code>no</code> ou <code>partial</code> avec du HTML en ligne</td>
</tr>
<tr>
<td><strong>figure</strong></td>
<td>Une image légendée</td>
<td><code>![alt](img/x.png "Caption")</code> seul sur sa ligne ; ajoutez <code>{50%}</code> pour le zoom général ou <code>{width=50% align=right}</code> pour le format étendu</td>
</tr>
<tr>
<td><strong>titres</strong></td>
<td>Structurer le corps de l’encadré</td>
<td><code>#</code> <code>##</code> <code>###</code> <code>####</code> <code>#####</code> <code>######</code> — jusqu’au niveau 6 ; <code>#</code> à <code>###</code> sont de vrais titres, <code>####</code> devient un paragraphe en graisse forte (pas une emphase <code>&lt;strong&gt;</code>), <code>#####</code>/<code>######</code> des paragraphes ordinaires</td>
</tr>
<tr>
<td><strong>citation, code, liste</strong></td>
<td>Les éléments ordinaires du texte</td>
<td>Du Markdown ordinaire</td>
</tr>
<tr>
<td><strong>note</strong></td>
<td>Une référence accessible au lecteur</td>
<td><code>[^label]</code> dans le texte, <code>[^label]: body</code> sur sa propre ligne</td>
</tr>
<tr>
<td><strong>article de fond</strong></td>
<td>Le texte développé que les fiches résument</td>
<td>Une fiche <code>full-article</code> qui pointe vers un second fichier <code>.md</code></td>
</tr>
</tbody>
</table>
<p>Gardez ces limites du parseur en tête :</p>
<ul>
<li><strong>Les images ont un suffixe court et un suffixe étendu.</strong> Ajoutez <code>{50%}</code> après l’image pour un zoom général, ou des paires validées comme <code>{width=50% height=auto align=right}</code>. <code>width</code> et <code>height</code> acceptent des longueurs CSS sûres ; <code>zoom</code> accepte un pourcentage ; <code>align</code> concerne les figures autonomes. Une image en ligne peut utiliser les tailles, mais pas <code>align</code>.</li>
<li><strong>Le passage des champs au texte libre est définitif dans une fiche.</strong> Dès qu’une ligne n’est plus de la forme <code>field:</code>, tout ce qui suit est du texte : un <code>highlight:</code> après un paragraphe est publié littéralement comme <code>highlight: 3 000 W</code>. Les champs d’abord, le texte ensuite.</li>
<li>Les champs structurels occupent une seule ligne physique, sauf <code>note:</code> et <code>comment:</code> : une continuation indentée appartient au champ de note ou de relecture précédent.</li>
<li><strong>Un champ est une valeur, pas du Markdown.</strong> <code>summary: un **gras**</code> publie les astérisques. La frontière peut surprendre : le HTML brut passe directement dans un champ, donc le fonctionnement de <code>&lt;br&gt;</code> ne dit rien sur <code>**</code>. <code>audit</code> indique les champs qui portent une syntaxe Markdown qu’ils ne rendront pas.</li>
<li><strong>Un encadré apparaît seulement avec <code>fact-label:</code>.</strong> Sans ce champ, le texte libre devient des paragraphes ordinaires, ce qui est souvent souhaité.</li>
</ul>
<p><strong>Notes de bas de page.</strong> <code>[^label]</code> appelle une note ; <code>[^label]: text</code>, sur sa propre ligne, fournit son corps. Le label est une clé qui, lorsqu’elle est valide, n’est jamais affichée : le lecteur voit une position. Il n’est donc pas nécessaire de renuméroter après une insertion. Seuls les caractères de mot sont admis : lettres, chiffres et <code>_</code>, accents et écritures non latines inclus, mais ni <code>-</code>, espace ou ponctuation. Un label invalide n’est ni une note ni une erreur bloquante : l’appel reste littéral, le corps devient un paragraphe et le label apparaît alors qu’il ne devait pas être visible. Par défaut, le corps est placé à la fin de l’unité qui l’appelle (fiche ou article long) et la numérotation recommence dans chaque fiche, car elle peut être partagée isolément. <code>notes_placement: page</code> dans les métadonnées rassemble toutes les notes en fin de page ; <code>notes_tooltip: on</code> affiche aussi leur texte sur l’appel. <code>audit</code> signale un label invalide, un appel sans corps, un corps sans appel et un corps écrit dans un bloc HTML brut, où il reste littéral.</p>
<p>Les deux réglages de notes peuvent être placés dans <code>series_meta</code> ; les métadonnées de l’article priment. Les valeurs intégrées sont <code>notes_placement: local</code> et <code>notes_tooltip: off</code>. Appels et corps des notes sont liés dans les deux sens.</p>
<p><strong>Ce qu’est le lien d’une fiche.</strong> Chaque fiche possède une adresse, par exemple <code>article.html#barrage-de-vajont</code>. Le bouton de partage la copie ou la montre en QR code pour un téléphone ou une impression. Le partage existe aussi sur l’index, où la portée fiche est désactivée : il n’y a aucune fiche à partager et la portée série désigne déjà la page. Cette adresse vient exclusivement de la ligne <code>slug:</code>, pas de la position ni du titre. Vous pouvez réordonner le deck, insérer une fiche, réécrire un titre ou retirer une fiche avec <code>tags: excluded</code> : les liens déjà distribués gardent leur destination.</p>
<p><code>slug:</code> est obligatoire. Son absence arrête le build et indique la commande corrective : <code>lightwebpres series slug set</code> ajoute un slug aux fiches qui n’en ont pas. C’est la seule commande qui édite les articles : un build ne réécrit jamais ses entrées. Le slug ajouté est un nom aléatoire de huit caractères, car un nom dérivé du titre laisserait croire qu’il continue à le suivre. Renommez-le avant publication : <code>slug: barrage-de-vajont</code> est plus parlant que <code>slug: 3f7c1a9e</code>. Sa valeur devient ensuite son identité.</p>
<p>Deux fiches portant le même slug produisent une erreur de build, pas un suffixe <code>-2</code> silencieux. <code>slug_prefix:</code> dans les métadonnées ou dans <code>series_meta</code> ajoute un espace de noms devant chaque adresse de la page, utile lorsque plusieurs pages réutilisent des noms comme <code>intro</code> ou <code>sources</code>.</p>
<p><code>lightwebpres series slug</code> liste les fiches de la série et leur nom publié, sans rien construire.</p>
<p>Déclarez chaque article devant apparaître dans la navigation dans <code>series.json</code> : voir la section suivante.</p>
<p><code>comment:</code> est un champ de relecture réservé aux sources, accepté sur chaque fiche et dans les métadonnées d’article ou de série. Il n’est jamais publié, même dans la source HTML. <code>note:</code> est différent : sur une couverture ou une fiche standard, il est embarqué pour le panneau présentateur (section 8). Tous deux acceptent des continuations indentées.</p>
<p>Pour les intégrations d’éditeurs ou d’agents, <code>lightwebpres contract --format text</code> décrit le contrat versionné <code>lightwebpres.slide-draft/1</code> : champs acceptés et obligatoires, cardinalités, ordre des sources, valeurs vides, identifiants réservés et squelettes analysables. Le JSON est le défaut. <code>--article first-page.md</code> évite les slugs déjà présents dans cette source. La commande n’écrit rien.</p>
<p>Une fiche <code>full-article</code> nécessite <code>article: filename.md</code>, vers un fichier Markdown séparé sous <code>sources/</code>, sans métadonnées ni marqueurs LWP. L’absence de <code>article:</code> est fatale ; une valeur explicitement vide avertit et omet la fiche inachevée. Une référence non vide vers un fichier absent est fatale.</p>
<p>Le Markdown accepte listes, tableaux, citations, code en ligne ou clôturé et HTML brut. Une image autonome avec lien, <code>[![alt](img/x.png "Caption")](https://example.org)</code>, garde sa légende hors du lien ; une image dans une phrase reste en ligne et son titre devient une infobulle. Les liens Markdown relatifs ne sont pas convertis : utilisez <code>&lt;a href="other.html"&gt;Autre page&lt;/a&gt;</code> pour les liens locaux. Les titres de niveaux 4 à 6 deviennent des paragraphes, pas des titres sémantiques. La référence du format détaille les limites du convertisseur ; ce n’est pas une implémentation générale de CommonMark.</p>
<p>Pour les tableaux comparatifs, entourez la valeur d’une cellule avec <code>&lt;span class="yes"&gt;Oui&lt;/span&gt;</code>, <code>no</code> ou <code>partial</code> pour ajouter un traitement de verdict avec une forme, pas seulement une couleur. La classe <code>col-signal</code> sur un en-tête met sa colonne en évidence ; il faut un tableau HTML brut, car Markdown ne peut pas ajouter cette classe à l’en-tête.</p>
<h2 id="4-organize-a-series-and-tags" tabindex="-1">4. Organiser une série et ses tags</h2>
<h3>Des variantes dans un article</h3>
<p><code>tags:</code> est un champ d’en-tête de fiche, pas un tag de style d’instance. Sa valeur est une liste de noms de variantes, séparés par des espaces et insensibles à la casse. Lettres Unicode, chiffres, <code>-</code> et <code>_</code> sont admis, sauf en début de nom pour <code>_</code>. Comme tout champ structurel, il occupe une seule ligne physique.</p>
<ul>
<li>L’absence de <code>tags:</code>, ou une valeur vide, signifie <code>default</code>, le contenu partagé.</li>
<li><code>tags: excluded</code> retire la fiche pendant le build ; elle n’est jamais émise.</li>
<li>Les autres tags sont inscrits dans l’attribut <code>data-tags</code> de la section et filtrés dans le navigateur.</li>
<li>Appuyez sur <strong>L</strong> pour ouvrir le menu des variantes. Il est masqué si l’article n’en a qu’une et mémorise le choix dans <code>localStorage['lwp-active-tag']</code>.</li>
<li>Le tag sélectionné affiche ses fiches et les fiches communes <code>default</code> ; compteurs, navigation, ancres et panneau présentateur utilisent les fiches visibles.</li>
</ul>
<p><code>tag:</code> n’est pas un champ ni un alias. Utilisez <code>kicker:</code> pour le libellé au-dessus du titre et <code>tags:</code> pour filtrer des variantes. Une ligne <code>tag:</code> devient du texte sur une fiche standard ; sur une couverture, <code>build</code> signale le champ inconnu et affiche les deux choix.</p>
<p>Pour une typographie adaptée à la langue, associez les tags aux packs dans <code>series_meta</code> :</p>
<pre><code class="language-json">
{
  "series_meta": {
    "lang_tags": {"fr": "fr", "en": "en"}
  },
  "articles": [{"page_source": "guide.md"}]
}
  </code></pre>
<p>Le premier tag linguistique mappé d’une fiche choisit son pack typographique. Sans tag mappé, elle utilise le repli <code>--lang</code>/<code>LWP_LANG</code> du build. Les packs <code>fr</code> et <code>en</code> intégrés viennent de l’exécutable ; les autres noms désignent <code>typography/&lt;name&gt;.json</code> ou l’ancien <code>language/&lt;name&gt;.json</code> de la série. La langue du navigateur ne change pas ce choix. <code>audit</code> signale les tags invalides et packs absents sans bloquer ; <code>build</code> refuse les déclarations mal formées.</p>
<h3>Déclarer les articles et examiner les métadonnées résolues</h3>
<p><code>series.json</code> liste les articles et contient les métadonnées de la série :</p>
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
<p><code>page_source</code> — un nom de fichier sans chemin — est le seul champ obligatoire ici. Chaque article se décrit lui-même : <code>page_dest</code> (nom du HTML), <code>page_title</code>/<code>page_desc</code>, <code>card_title</code>/<code>card_desc</code>/<code>card_label</code>, <code>nav_title</code>/<code>nav_desc</code> et les champs éditoriaux (<code>author</code>/<code>license</code>, avec les défauts de <code>series_meta</code>, et <code>date</code>) se résolvent depuis ses métadonnées et sa couverture. Ils peuvent être remplacés dans l’entrée JSON pour lui donner le dernier mot. <code>status</code> définit la place de l’article : <code>active</code> par défaut, <code>draft</code> (article conservé dans la série mais hors sortie tant que <code>--include-drafts</code> ne le prévisualise pas avec un bandeau) ou <code>ignored</code> (retiré de la chaîne sans supprimer son entrée ni ses réglages). L’ordre du tableau est celui de la navigation et de l’index. Les replis de chaque champ sont détaillés dans <code>GLOSSARY.md</code>.</p>
<p><code>lightwebpres status my-series --format json</code> fournit aussi l’inventaire des tags utilisé au build. Pour une vue ciblée, utilisez <code>lightwebpres series tags my-series</code> : visibilité effective des articles et fiches par tag, distinction <code>active</code>/<code>draft</code>/<code>ignored</code> et résultat réel de la sélection par défaut. Ajoutez <code>--tag fr</code> pour ne garder qu’une ligne.</p>
<p><code>status</code> liste les articles dans l’ordre du tableau, avec chaque valeur résolue et son origine : entrée JSON, métadonnées, contenu, champ dérivé ou défaut intégré. Une source illisible reste listée avec des replis et un avertissement sur stderr. Ni <code>status</code> ni <code>series tags</code> ne construit ou n’écrit quoi que ce soit.</p>
<p>Les métadonnées d’article peuvent déclarer <code>tags: fr</code> : ce filtre doit correspondre au tag choisi <strong>et</strong> au moins une fiche non exclue doit l’accepter. Un article sans tags n’a pas ce filtre. <code>series_meta.default_tag</code> fixe la sélection initiale (<code>default</code> par défaut) ; un choix lecteur mémorisé valide prime. Choisir <code>default</code> ne montre que les fiches communes, pas toutes les variantes. <code>build</code> et <code>audit</code> avertissent si un tag sélectionnable n’a aucune fiche effective ou si un article n’a aucune fiche non exclue. <code>series tags --format json</code> expose les totaux par statut, les fiches communes et la sortie par défaut ; <code>--tag fr</code> réduit les lignes sans changer les totaux.</p>
<h2 id="5-choose-presets-themes-and-customization" tabindex="-1">5. Choisir presets, thèmes et personnalisation</h2>
<h3>Identités, presets et thèmes</h3>
<p>L’<strong>identité</strong> regroupe les choix de présentation. L’identité native <strong>LightWebPres</strong> fournit <code>builtin/standard</code> et le thème minimal <strong>Light</strong>. <strong>Commons</strong> contient le catalogue global de thèmes et les presets qui les associent aux dispositions natives. Un <strong>Identity Kit</strong> est un ensemble autonome et versionné de dispositions, en-têtes, pieds, assets, thèmes typés et CSS structurel contraint. Un <strong>preset</strong> choisit une configuration de disposition/chrome et un <strong>thème</strong> de base ; il ne génère pas toutes les combinaisons possibles.</p>
<p>LWP gère l’enveloppe de page, la navigation et le JavaScript. Les fragments de kit ont les emplacements <code>{{content}}</code>, <code>{{slide_header}}</code> et <code>{{slide_footer}}</code> ; l’index reçoit seulement <code>{{content}}</code>. Un kit peut utiliser des fichiers locaux ou les références natives <code>builtin:standard</code> pour les dispositions et <code>builtin:light</code> pour les thèmes. Une disposition native dans un kit garde le chrome de ce kit. Les kits ne peuvent pas dépendre de Commons ou d’autres kits, les étendre, ni déclarer provenance, parenté ou authenticité. Les chargeurs calculent les origines des ressources.</p>
<p>Le seul choix persisté est <code>series_meta.presentation_preset</code> : <code>builtin/standard</code>, <code>commons/&lt;id&gt;</code> ou <code>id@MAJOR.MINOR.PATCH/preset</code>. L’identité en est déduite. Ce choix n’appartient ni aux métadonnées d’article ni à une entrée <code>articles[]</code>. Son absence sélectionne implicitement <code>builtin/standard</code>. <code>init --preset builtin/standard</code> et <code>series preset set --preset builtin/standard</code> enregistrent la référence explicite ; <code>init</code> seul laisse le champ absent. Aucun de ces choix natifs ne copie de ressources.</p>
<pre><code class="language-json">
{
  "series_meta": {
    "presentation_preset": "corporate@1.0.0/brief"
  }
}
  </code></pre>
<p>Le <code>label</code> du manifeste nomme l’identité, pas le preset initial. Son <code>default_preset</code> facultatif désigne un preset local ; sinon le premier dans l’ordre du manifeste est utilisé. <code>slide_layouts</code> et <code>slide_chrome</code> déclarent les défauts du preset uniquement dans ce manifeste.</p>
<p><code>slide-layout</code>, <code>slide-header</code> et <code>slide-footer</code> fonctionnent sur les quatre types de fiches. Ils remplacent les défauts du preset pour une fiche, sans cascade JSON d’auteur. Le thème du preset fournit la base typée sauf si <code>settings.conf</code> sélectionne un autre thème. Priorité : thème de base &lt; valeurs épinglées de <code>settings.conf</code> &lt; <code>style.*</code> de l’article &lt; styles d’instance ; <code>templates/custom.css</code> reste la couche CSS avancée finale. Les assets sont publiés sous <code>public/assets/presentations/&lt;id&gt;/&lt;version&gt;/...</code> ou incorporés avec <code>--inline-images</code>.</p>
<pre><code class="language-bash">
./lightwebpres preset list
./lightwebpres preset show builtin/standard
./lightwebpres series preset my-series
./lightwebpres series preset set my-series --preset builtin/standard --use-preset-theme
./lightwebpres init my-series --preset builtin/standard
  </code></pre>
<p><code>series preset set</code> copie et sélectionne sans appliquer de projet de départ. Il conserve les valeurs épinglées et <code>custom.css</code> ; si <code>settings.conf</code> contient un <code>theme:</code> explicite, il exige <code>--keep-theme</code> ou <code>--use-preset-theme</code>, qui retire cette ligne. <code>--keep-theme</code> nécessite un <code>theme:</code> explicite. Les kits se trouvent sous <code>kits/&lt;id&gt;/&lt;version&gt;/</code> dans un catalogue, puis sous <code>templates/kits/&lt;id&gt;/&lt;version&gt;/</code> dans la série. <code>LWP_IDENTITY_KITS_DIR</code> remplace le catalogue utilisateur ; une collision id/version masque le kit entier. La spécification §9.9 détaille manifeste, validation et sécurité.</p>
<p>Pour un preset de kit, <code>init --preset</code> valide et copie le kit complet, écrit le sélecteur et génère les réglages depuis son thème. Il applique le projet de départ déclaré, sauf avec <code>--no-starter</code>. Aucune option ne change le sens des commandes <code>template</code>. Choisissez un sélecteur installé avec <code>preset list</code> ; <code>corporate@1.0.0/brief</code> est illustratif, pas un kit fourni. Le choix natif ne demande aucun fichier. <code>init</code> et <code>series preset set</code> copient le descripteur Commons et l’éventuel instantané du thème externe sélectionné ; un thème natif ou embarqué n’a pas besoin de copie. Une dépendance locale identique est réutilisée, un fichier différent est refusé.</p>
<p>Le guide utilise le kit suivi <code>examples/kits/lightwebpres-docs/0.1.0/</code>. <code>tools/build_guide.py</code> le copie dans une série temporaire et publie ses assets avec le guide. C’est un exemple de kit inspectable, pas une autre source de ce manuel.</p>
<h3>Ajouter un preset Commons</h3>
<p>Les thèmes Commons utilisent le catalogue global <code>themes/</code>, <code>LWP_THEMES_DIR</code> et les <code>templates/themes/</code> d’une série. Les descripteurs de presets ont une racine Commons séparée : <code>commons/presets/</code> installé à côté de l’exécutable ou sous <code>&lt;prefix&gt;/share/lightwebpres/</code>, puis <code>LWP_COMMONS_DIR</code>, puis <code>templates/commons/presets/</code> dans la série. Les défauts utilisateur sont <code>$XDG_DATA_HOME/lightwebpres/commons/</code> (normalement sous <code>~/.local/share</code>) ou <code>%APPDATA%/lightwebpres/commons/</code>. Un descripteur plus proche remplace l’entrée entière.</p>
<p>Par exemple, <code>templates/commons/presets/reading.json</code> contient :</p>
<pre><code class="language-json">
{
  "schema": "lightwebpres.commons-preset/1",
  "id": "reading",
  "label": "Reading",
  "description": "Native layouts with a light reading theme.",
  "theme": "builtin:light"
}
  </code></pre>
<p>Les cinq clés sont obligatoires ; aucune autre n’est acceptée, y compris <code>starters</code>. <code>id</code> correspond au nom du fichier ; <code>theme</code> est un slug du catalogue global ou <code>builtin:light</code>. Sélectionnez-le avec <code>./lightwebpres series preset set my-series --preset commons/reading</code>. Si la série possède un thème explicite, choisissez aussi <code>--keep-theme</code> ou <code>--use-preset-theme</code>.</p>
<h3>Composer un kit</h3>
<p><code>kit compose</code> construit un kit autonome depuis une recette explicite. Ce <code>recipe.json</code> complet ne nécessite aucun fichier source :</p>
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
<p>Le résultat est <code>kits/brief/1.0.0/</code>. La recette exige exactement <code>schema</code>, <code>sources</code>, <code>manifest</code> et <code>files</code>. Pour réutiliser des fichiers déclarés, <code>sources</code> associe un alias à un chemin relatif de kit sous le dossier de recette ; <code>files</code> associe une destination à <code>{"source":"alias","path":"local/path"}</code>, <code>{"file":"local/path"}</code> ou <code>{"text":"content"}</code>. Une destination <code>.css</code> accepte aussi <code>{"parts":[...]}</code>, avec une liste non vide de ces descripteurs ; les fichiers lus par <code>parts</code> doivent aussi avoir l’extension <code>.css</code>. Le fichier <code>structure_css</code> déclaré d’un kit source est reconnu par son rôle dans le manifeste, indépendamment de son suffixe. Seuls les tokens de classe correspondants de ses sélecteurs sont rattachés à la portée du kit cible, y compris les tokens échappés ; commentaires, chaînes, attributs et déclarations sont conservés. Les autres fichiers copiés ne sont pas réécrits. Le manifeste final complet doit nommer explicitement toutes les références locales finales : aucun remappage ni fermeture de dépendances n’est deviné.</p>
<p>La publication est préparée hors du catalogue de sortie, sur le même système de fichiers ; <code>--dry-run</code> valide dans un espace temporaire jetable et ne crée pas de sortie. Un catalogue placé à la racine d’un système de fichiers ou d’un point de montage est refusé : choisissez un sous-dossier. Les destinations de kit existantes sont refusées. Le kit composé n’a besoin d’aucun kit source au build et ne porte pas de registre de provenance.</p>
<h3>Garder des présentations alternatives disponibles</h3>
<p>Une série a une présentation principale, mais un build peut embarquer d’autres presets nommés que le lecteur choisira sans reconstruire. Un preset principal de kit ou de Commons rend aussi automatiquement disponible le <code>builtin/standard</code> natif compatible, après les alternatives déclarées. Placez les autres alternatives à la racine de <code>series.json</code> ou passez-les pour un build :</p>
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
<p>Le preset principal est toujours émis en premier et reste le repli sans JavaScript. La liste CLI remplace la liste JSON ; elle ajoute des alternatives, sans remplacer le principal. Les sélecteurs doublons sont supprimés ; un sélecteur inconnu échoue avant toute écriture. Le preset doit être disponible dans le catalogue effectif. Il n’est pas nécessaire de lister explicitement <code>builtin/standard</code> pour un kit ou Commons. Si une fiche utilise un <code>slide-layout</code>, <code>slide-header</code> ou <code>slide-footer</code> propre au kit, le défaut implicite est omis avec un avertissement ; demander explicitement <code>builtin/standard</code> conserve l’erreur de validation normale.</p>
<p>Avec des alternatives, <strong>C</strong> ouvre le sélecteur d’apparence : <strong>Identité</strong>, <strong>Preset</strong> et <strong>Thème</strong>. Le preset change tout le deck, index compris, et persiste entre les pages de la session navigateur. Il ne modifie pas la série. Si <code>settings.conf</code> désigne un <code>theme:</code> explicite, il reste fixe ; sinon le thème typé suit le preset jusqu’à un choix explicite du lecteur. <strong>Suivre le preset</strong> réinitialise ce choix. Tous les thèmes des kits sélectionnés sont publiés avec des noms qualifiés par kit, même si aucun preset retenu ne les utilise.</p>
<p>Les filtres <strong>Applicable</strong>, <strong>Identité courante</strong> et <strong>Tous</strong> réduisent seulement les choix publiés. Applicable signifie compatibilité typée, pas correspondance de marque ; Identité courante signifie appartenance des ressources. Les libellés d’identité restent fixes lors des changements de preset ou de thème. Le marqueur initial/par défaut décrit un choix, pas une autre identité. Le sélecteur n’invente pas de produit cartésien presets × thèmes et ne charge pas d’entrées supplémentaires.</p>
<p>Pour les couleurs et la typographie, choisissez le remplacement de valeur le plus limité qui répond au besoin avant d’ajouter du CSS.</p>
<h3>Choisir un thème pour toute la série</h3>
<p>Des dizaines de thèmes de couleurs sont préconfigurés, trop pour un choix dans une simple liste : filtrez-les par famille, fond clair ou sombre et teinte du fond.</p>
<pre><code class="language-bash">
./lightwebpres theme list                                     # the whole catalogue, with facets
./lightwebpres theme list --family terrain                    # one editorial family
./lightwebpres theme list --polarity dark --hue green          # just the ones you mean
./lightwebpres theme gallery                             # every theme, rendered
  </code></pre>
<p>Le catalogue Commons combine les thèmes intégrés et les instantanés UTF-8 <code>.conf</code> complets des racines installée et utilisateur ; la série peut ajouter ses <code>templates/themes/</code>. <code>LWP_THEMES_DIR</code> remplace la racine utilisateur. Priorité : intégré, installé, utilisateur, série ; une collision remplace l’entrée entière sans héritage. <code>builtin:&lt;slug&gt;</code> sélectionne un thème intégré masqué par un fichier local.</p>
<p>Les thèmes installés se trouvent sous <code>&lt;prefix&gt;/share/lightwebpres/themes/</code> pour FHS ou dans un dossier <code>themes/</code> voisin d’un exécutable autonome. La racine utilisateur est <code>$XDG_DATA_HOME/lightwebpres/themes/</code> sous Unix (normalement dans <code>~/.local/share</code>) ou <code>%APPDATA%/lightwebpres/themes/</code> sous Windows. Seuls les fichiers <code>.conf</code> directement présents sont lus. <code>theme path</code> indique les racines. Les rapports globaux <code>theme</code> n’incluent pas la couche locale d’une série ; <code>series theme</code> l’inclut.</p>
<p>Appliquez un thème à l’initialisation ou changez-le ensuite :</p>
<pre><code class="language-bash">
./lightwebpres init my-series --theme evergreen
./lightwebpres series theme set my-series --theme crimson
  </code></pre>
<p>Un thème est un mot dans un fichier de données : <code>series theme set</code> réécrit seulement la ligne <code>theme:</code> de <code>templates/settings.conf</code>. Aucun CSS n’est touché : la feuille de style est composée en mémoire à chaque build.</p>
<p>Par défaut, le build embarque les thèmes essentiels pour le lecteur ; <code>--no-essential-theme</code> les désactive, tandis que des sélections explicites complètent ou définissent le catalogue :</p>
<pre><code class="language-bash">
./lightwebpres build my-series --lang en --themes print-ink,print-grey
./lightwebpres build my-series --lang en --themes all
  </code></pre>
<p>Ou conservez la sélection à la racine de <code>series.json</code> :</p>
<pre><code class="language-json">
"themes": ["essential", "background:light", "bgh:red"]
  </code></pre>
<p><code>essential</code> embarque Monochrome, Monochrome Night et Print Ink. Un sélecteur <code>X:Y</code> peut utiliser <code>background</code>/<code>bg</code>, <code>family</code>/<code>fam</code> ou <code>background hue</code>/<code>bgh</code> ; chacun ajoute les thèmes correspondants et les doublons sont supprimés. Un <code>--themes</code> CLI explicite remplace la liste JSON.</p>
<p>Créer un thème ou le rendre explicitement portable :</p>
<pre><code class="language-bash">
./lightwebpres theme create my-theme --from evergreen
./lightwebpres theme migrate my-series
./lightwebpres theme vendor my-series --themes my-theme,evergreen
./lightwebpres theme path
  </code></pre>
<p><code>theme create</code> écrit un instantané complet et éditable, <code>theme migrate</code> ne conserve que le thème choisi et les valeurs explicitement épinglées d’un ancien squelette, et <code>theme vendor</code> copie des instantanés complets dans la série. Aucun fichier de thème n’utilise <code>extends</code>.</p>
<p>Le thème effectif de <code>templates/settings.conf</code> est toujours le premier choix de base, même absent de la liste. Si le fichier contient des valeurs épinglées, le premier choix lecteur s’appelle <code>custom(&lt;theme&gt;)</code> et le thème brut reste aussi présent ; ces valeurs ne s’appliquent qu’au choix personnalisé. Le réglage est lu au build : la modification de l’auteur reste la référence. Les propriétés <code>style.*</code> de page et les variables déclarées dans <code>custom.css</code> ne sont pas modifiées par le changement de thème du lecteur. <strong>C</strong> ouvre le sélecteur d’apparence avec recherche lorsqu’il existe des alternatives, sinon il n’a rien à ouvrir. <strong>M</strong> ouvre le menu présentateur, également accessible en bas à droite. Le choix dure pour les pages du même deck dans la session courante. La clé de session inclut l’identité du deck et l’empreinte du catalogue : un autre deck sur la même origine ou un instantané local modifié ne reprend pas un ancien choix. Chaque thème prévisualise son fond résolu, dégradé compris, et sa couleur de texte. Les actions portent icônes et raccourcis, dont <strong>I</strong> pour Défilement. Dans les deux menus, le focus commence au premier contrôle utile. Dans le menu présentateur, gauche/droite restent sur la ligne, haut/bas visent le contrôle le plus proche de la ligne voisine. <code>Tab</code>, <code>Home</code> et <code>End</code> parcourent les contrôles ; <code>Enter</code>/<code>Space</code> activent le contrôle ciblé.</p>
<p>Ces commandes examinent et sélectionnent des valeurs existantes ; elles ne conçoivent ni ne corrigent une palette. <code>theme show</code> donne le contraste mesuré du thème ou du thème effectif après les réglages de série. <code>audit</code> lit automatiquement la même feuille résolue et signale ce qui ne fonctionne plus : contrôle invisible, texte de la couleur du fond, taille sous le seuil de lisibilité. Il avertit sans refuser ; aucun thème fourni ne déclenche ces contrôles.</p>
<pre><code class="language-bash">
./lightwebpres theme show evergreen
./lightwebpres series theme my-series --format json
  </code></pre>
<p>Le rapport fournit les niveaux WCAG <strong>par catégorie</strong>, avec paires et ratios mesurés, pas une note globale d’accessibilité. Il mesure les propriétés typées résolues, pas le CSS arbitraire de <code>custom.css</code>. Aucune palette n’est réécrite, masquée ou refusée selon son score, et les scores ne sont pas affichés sur les pages publiées. Examinez la page après personnalisation.</p>
<p>Le catalogue contient des palettes originales et des portages comme Nord, Dracula, Solarized, Gruvbox et Catppuccin. <code>family</code> utilise <code>desk</code>, <code>light</code>, <code>terrain</code>, <code>heat</code>, <code>pop</code>, <code>ported</code>, <code>print</code> ; polarité et teinte du fond sont calculées. Le <a href="https://github.com/Fade78/lightwebpres/blob/main/generated/themes-gallery.png">catalogue compact</a> donne une vue d’ensemble ; ouvrez la <a href="https://github.com/Fade78/lightwebpres/blob/main/generated/themes-gallery.html">galerie HTML</a> pour filtrer les couvertures, fiches avec notes, notes de page et textes longs.</p>
<h3>Pourquoi les thèmes essentiels sont fournis par défaut</h3>
<p>Chaque build embarque de lui-même <code>essential</code> — Monochrome, Monochrome Night et Print Ink — pour que le sélecteur soit disponible sans option de l’auteur. Trois raisons, dans cet ordre :</p>
<ul>
<li><strong>Accessibilité.</strong> Monochrome offre un texte contrasté sans teinte ; Monochrome Night en fait autant sur fond sombre pour les lecteurs malvoyants ou sensibles à la lumière ; Print Ink est noir pur sur blanc, le contraste maximal de la page. Un lecteur qui ne peut pas lire le thème choisi dispose d’une alternative, même si l’auteur ne l’avait pas prévue.</li>
<li><strong>Impression.</strong> Print Ink est conçu pour le papier — fond blanc pur, texte noir — sans choix préalable de l’auteur. Appuyez sur <strong>C</strong>, choisissez <strong>Print Ink</strong>, puis imprimez avec <code>Ctrl</code>/<code>Cmd</code>+<code>P</code>. L’impression conserve le thème actif ; elle ne choisit pas Print Ink automatiquement.</li>
<li><strong>Sobriété.</strong> Monochrome et Print Ink n’ont pas de teinte : l’ensemble essentiel ne heurte pas la couleur d’une série. Le thème de l’auteur reste principal ; les trois autres sont des alternatives, jamais des remplacements.</li>
</ul>
<p>Désactivez-les si la page doit rester fixe ou proposer une sélection personnalisée :</p>
<pre><code class="language-bash">
./lightwebpres build my-series --lang en --no-essential-theme
./lightwebpres verify my-series --lang en --no-essential-theme
./lightwebpres watch my-series --lang en --no-essential-theme
  </code></pre>
<p>Avec cette option, aucun sélecteur n’est embarqué sauf si <code>--themes</code> ou <code>series.json["themes"]</code> en ajoute un. Sans elle, les trois essentiels sont fournis et dédupliqués avec le thème principal : s’il en fait déjà partie, il n’apparaît pas deux fois.</p>
<h3>Changer une expression avec un tag d’instance</h3>
<p>Dans le texte libre, à l’endroit qui le nécessite :</p>
<pre><code class="language-markdown">
A {color:call}critical{/color} figure, set in {mono}fixed pitch{/mono}.
  </code></pre>
<p><code>{color:…}</code> et <code>{font:…}</code> acceptent un nom partagé (<code>mark</code>, <code>call</code>, <code>mono</code>…) ou une valeur littérale ; <code>{sc}</code>, <code>{u}</code>, <code>{strike}</code> et <code>{mono}</code> n’ont pas de valeur. Une valeur invalide produit une erreur nommant le fichier, jamais un échec silencieux. <code>audit</code> les compte par article pour orienter les vérifications après un changement de thème.</p>
<p><strong>L’alignement est le seul tag de niveau bloc</strong>, car <code>text-align</code> sur un span en ligne ne fait rien. Ouverture et fermeture sont chacune seules sur leur ligne :</p>
<pre><code class="language-markdown">
{align:center}
This paragraph is centred, and so is the next one.
{/align}
  </code></pre>
<p>Valeurs : <code>left | center | right | justify</code>. Tout le bloc est aligné, cellules de tableau comprises.</p>
<h3>Changer une page avec <code>style.*</code> dans ses métadonnées</h3>
<p>Toute propriété, limitée à cette page :</p>
<pre><code>
&lt;!-- lwp:meta --&gt;
page_title: The apple pie
style.cover.bg.angle: 90deg
style.page.content-max: 60ch
  </code></pre>
<p>Et <code>fact-variant: warning</code> donne à l’encadré d’une fiche standard une apparence nommée, plutôt qu’une couleur réglée à la main.</p>
<h3>Changer toute la série avec <code>templates/settings.conf</code></h3>
<p>Chaque choix visuel est une propriété typée <code>component.axis: value</code>. <code>settings.conf</code> les liste <strong>toutes</strong> en commentaires, aux valeurs du thème choisi : l’ensemble des réglages est visible sans documentation supplémentaire. Décommentez une ligne pour l’<strong>épingler</strong> : elle survit aux changements de thème et de moteur, car <code>lightwebpres</code> ne réécrit pas votre fichier.</p>
<p>Deux propriétés contrôlent le gras d’un encadré (<code>**text**</code> dans un encadré) :</p>
<ul>
<li><code>fact.strong.pad</code> — marge latérale du fond surligné autour du gras (défaut <code>max(3px, 0.375vmin)</code>, automatiquement 0 sur les thèmes sans fond de surlignage).</li>
<li><code>fact.strong.absorb-punct</code> — <code>on</code> par défaut absorbe la ponctuation suivant un passage gras dans le surlignage (<code>**2000**,</code> surligne aussi la virgule) ; <code>off</code> conserve le Markdown tel qu’écrit.</li>
</ul>
<pre><code>
# kicker.fg: ink-quiet      ← the scaffold, showing the theme's value
kicker.fg: call             ← uncommented: yours, and it stays
  </code></pre>
<p>Un mot seul comme <code>call</code> est cherché dans les valeurs partagées du thème (<code>color.call</code>, car <code>fg</code> est un axe couleur) ; une valeur comme <code>#8A4B00</code> fonctionne partout où une couleur est attendue. Une faute de clé ou de valeur produit une erreur nommant le fichier et la clé. Une valeur vide sur une propriété connue, comme <code>page.bg:</code>, retire l’épinglage et laisse le thème fournir la valeur ; une clé inconnue reste une erreur.</p>
<p>Trois propriétés souvent recherchées : <strong><code>page.content-max</code></strong> règle la largeur du texte, <code>84vw</code> par défaut, proportionnelle à la fenêtre sans plafond pour utiliser le plein écran. Toutes les tailles sont également proportionnelles — kicker, libellé d’encadré, légende du chiffre clé et numéro de fiche comme le titre — afin de garder longueur de ligne et proportions quand l’écran grandit. Chaque taille possède un minimum en pixels qui gouverne le téléphone. <strong><code>page.block-max</code></strong> règle les éléments autres que le texte courant : tableau, code, figure, dimensionnés selon leur contenu plutôt qu’un nombre de caractères. Il comporte plancher et plafond : <code>min(84vw, max(1100px, 102vmin))</code>. Un tableau grandit avec son texte tout en s’arrêtant avant le bord. <strong><code>page.hyphens</code></strong> (<code>manual | auto</code>) contrôle la césure en fin de ligne ; il vaut <code>manual</code> et rien ne l’active à votre place.</p>
<p>Après <code>series theme set</code>, <code>audit</code> remarque que les <em>commentaires</em> du squelette montrent l’ancien thème ; <code>template update --scaffold</code> les réaligne tout en conservant les lignes épinglées.</p>
<p>Les valeurs partagées sont <code>color.page</code>, <code>color.ink</code>, <code>color.ink-quiet</code>, <code>color.mark</code>, <code>color.call</code>, <code>color.affirm</code>, <code>color.nav</code> et les quatre piles de polices <code>font.text</code>, <code>font.display</code>, <code>font.ui</code>, <code>font.mono</code>. Modifiez une propriété du composant plutôt que la couleur partagée si seul ce composant doit changer :</p>
<pre><code class="language-conf">
verdict.partial.fg: #8A4B00
summary.fg: #10151B
link.decoration-color: mark
  </code></pre>
<p><code>color.nav</code> règle les contrôles de navigation, pas le texte courant. Les liens du corps et des sources gardent le texte environnant et un soulignement ; <code>link.decoration-color</code> change ce soulignement. Les composants qui possèdent des glyphes exposent <code>shadow.fg</code>, <code>blur</code>, <code>dx</code>, <code>dy</code> pour les halos (par exemple <code>title1.shadow.fg: #33FF8866</code>). Une ombre héritée résout sa taille sur l’ancêtre, pas par glyphe. Les composants surélevés exposent couleur, flou, décalages et étalement, avec des axes de survol pour cartes et boutons. Utilisez le squelette généré pour les noms exacts plutôt que d’inventer des variables CSS.</p>
<h3>Des règles plutôt que des valeurs : <code>templates/custom.css</code></h3>
<p>Du CSS complet, sans sous-ensemble, ajouté après la feuille composée : vos règles gagnent les égalités. <code>init</code> le crée strictement vide, car son contenu est publié tel quel ; tout conseil écrit par l’outil deviendrait visible dans chaque page. <code>settings.conf</code> peut porter cinq cents lignes de commentaires parce qu’il est analysé, contrairement à ce fichier. Ajoutez sélecteurs, media queries, <code>@font-face</code> (nommez la famille en tête de pile dans <code>settings.conf</code>, déclarez-la ici). Les variables <code>--component-axis</code> de la feuille composée y sont disponibles (<code>border-color: var(--color-mark)</code>) : c’est la manière recommandée de suivre le thème.</p>
<p>Le comportement est la troisième couche, absente de la série par défaut : le script de navigation réside dans l’exécutable. <code>template write nav.js</code> en place une copie sous <code>templates/</code> pour la modifier ; elle remplace alors toute la navigation, sans remplacement partiel. La structure HTML de page et d’index est fixe, pas un modèle personnalisable.</p>
<h2 id="6-set-languages-and-typography" tabindex="-1">6. Régler les langues et la typographie</h2>
<p>Libellés d’interface et typographie sont indépendants : <code>interface/{lang}.json</code> et <code>typography/{lang}.json</code>. Le français et l’anglais sont intégrés. Sans <code>--lang</code> ni <code>LWP_LANG</code>, les pages embarquent les deux vocabulaires : le navigateur choisit le français pour les locales <code>fr-*</code>, l’anglais sinon. Une langue explicite fixe l’interface. La typographie est appliquée au build et n’est jamais recalculée lorsque la locale du navigateur change.</p>
<pre><code class="language-bash">
./lightwebpres build my-series --lang en
./lightwebpres template show interface/fr.json
./lightwebpres template write typography/fr.json my-series
  </code></pre>
<p>N’écrivez que le domaine à personnaliser. Les chaînes d’interface fusionnent clé par clé ; les <code>rules</code> typographiques remplacent entièrement les règles de base. Les anciens packs unifiés <code>language/{lang}.json</code> restent acceptés ; les fichiers séparés priment pour leur domaine. <code>--language-file path</code> sur <code>build</code>/<code>verify</code> sélectionne explicitement un pack unifié à priorité maximale. <code>LWP_INTERFACE_DIR</code>, <code>LWP_TYPOGRAPHY_DIR</code> et <code>LWP_LANGUAGE_DIR</code> déplacent les domaines ; la spécification §2.3 et §19 donne les schémas et la recherche des packs installés.</p>
<p>Pour des fiches multilingues, <code>series_meta.lang_tags</code>, par exemple <code>{"fr": "fr", "en": "en"}</code>, associe tags et packs typographiques. Le premier tag mappé de la fiche l’emporte ; sinon <code>--lang</code>/<code>LWP_LANG</code> fournit le repli. Une langue inconnue revient finalement à l’anglais. Ajoutez les règles d’une autre langue dans son pack, pas dans le moteur.</p>
<p>La typographie remplace des espaces existantes par des insécables ; elle n’invente ni espaces ni groupes de milliers et conserve les insécables existantes. Le français traite <code>; : ! ?</code>, guillemets, <code>%</code>, tirets d’incise espacés, milliers groupés (<code>170 000</code>), couples nombre/unité, millions et dollars, et <code>×</code>/<code>≈</code> avant un nombre. L’anglais utilise un ensemble plus limité : unités métriques, mots d’unités, initiales, opérateurs et tirets espacés. Les règles affectent le texte, pas la syntaxe des balises HTML.</p>
<p>Pour désactiver des catégories sur un article, utilisez les métadonnées :</p>
<pre><code class="language-text">
typo_units: off
typo_thousands: off
  </code></pre>
<p><code>typo: off</code> désactive toutes les règles de l’article ; <code>--no-typography</code> sur <code>build</code>/<code>verify</code>/<code>watch</code> agit sur toute l’exécution. Un commutateur de catégorie agit sur le pack en vigueur : l’anglais n’a pas de règle de milliers à désactiver. Les listes complètes sont dans la spécification §4.5, §7.5 et §19.6.</p>
<h2 id="7-verify-and-publish" tabindex="-1">7. Vérifier et publier</h2>
<p>Deux contrôles différents pour deux moments différents :</p>
<pre><code class="language-bash">
./lightwebpres audit my-series --lang en    # source and render warnings
./lightwebpres verify my-series --lang en   # does output match the sources?
  </code></pre>
<p><code>audit</code> rend la série en mémoire sans rien écrire. Il vérifie tous les articles déclarés, brouillons et <code>ignored</code> compris ; il n’a pas besoin de <code>--include-drafts</code>. Lisez trois types de rapports :</p>
<ul>
<li><strong>Sources et remplacements :</strong> couvertures manquantes, tags d’instance, métadonnées ou tags mal formés, packs linguistiques absents, champs de couverture ignorés, ancien <code>style.css</code>, variables CSS retirées et leurs remplacements, commentaires de squelette périmés et liens symboliques sortant des racines logiques.</li>
<li><strong>Styles résolus :</strong> contrôle de navigation invisible, texte identique au fond ou taille sous le seuil de lisibilité après composition du thème, des réglages et des styles d’article. Des valeurs individuellement valides peuvent mal se combiner.</li>
<li><strong>Rendu :</strong> échecs de build et inventaire d’images avec nombres d’images en ligne et de figures, sources inutilisées et assets référencés absents. Si le rendu échoue, l’usage inconnu est annoncé indisponible, pas faussement inutilisé.</li>
</ul>
<p><code>audit</code> seul sort avec zéro même si le rendu échoue. <code>--strict</code> transforme avertissements et erreurs de rendu en résultats CI non nuls. <code>--templates</code> limite le contrôle à la couche de présentation et aux styles résolus, sans rendu ni vérifications par article. C’est moins coûteux que l’audit complet, qui vaut environ un build.</p>
<p><code>verify</code> répond à l’autre question : il reconstruit les articles en mémoire et compare à <code>public/</code> (hors empreintes de build et espaces environnantes), puis sort non zéro au premier écart. Placez-le avant <code>build</code> pour détecter une sortie modifiée à la main ou non reconstruite après une modification de source.</p>
<p>Utilisez les mêmes options prises en charge que pour le build, notamment <code>--lang</code>, <code>--themes</code> et <code>--no-essential-theme</code>. <strong><code>verify</code> n’accepte pas <code>--inline-images</code></strong> et ne peut pas reproduire ce mode : images et assets incorporés peuvent donc signaler un écart sans changement des sources. Utilisez une sortie séparée sans incorporation pour ce contrôle CI.</p>
<h3>Demander pourquoi une valeur a été retenue</h3>
<p>Une grande partie du résultat n’est pas écrite directement sur la page : un titre vient de <code>series.json</code>, des métadonnées ou de la couverture ; une couleur vient de <code>settings.conf</code>, du thème ou des défauts. Si le résultat surprend, demandez :</p>
<pre><code class="language-bash">
./lightwebpres resolve my-series page_title --article first-page.md
./lightwebpres resolve my-series kicker.fg
  </code></pre>
<p>Aucune option ne dit quel type de nom vous avez passé : le nom le dit. Un point indique une propriété de thème, un souligné un champ d’article ou de série, un trait d’union un champ de fiche.</p>
<p>La réponse montre le niveau gagnant <strong>et tous ceux qui n’ont pas gagné</strong>, du plus fort au plus faible :</p>
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
<p>Cette seconde partie résout les problèmes. Une ligne écrite sans effet apparaît comme un niveau vide, encore commenté ou dépassé par une entrée <code>series.json</code> oubliée.</p>
<p>Un champ de fiche n’a pas de cascade : <code>resolve fact-label</code> liste donc les fiches qui le définissent, dans la série ou dans un article avec <code>--article</code>. Ajoutez <code>--format json</code> pour une machine et <code>--article</code> à une propriété de thème pour inclure les <code>style.*</code> de cette page dans la chaîne.</p>
<h3>Publier la sortie, pas le projet</h3>
<p>Envoyez le contenu de <code>public/</code> à un hébergement statique : HTML des articles, <code>index.html</code>, images <code>img/</code> référencées et fichiers <code>assets/presentations/</code>. Le README de série généré est à côté de <code>series.json</code>, pas dans <code>public/</code>. Aucun serveur Python ni moteur LightWebPres n’est nécessaire sur l’hôte. Rouvrez l’index hébergé, suivez un article et testez un lien de fiche depuis un autre appareil. La lecture <code>file://</code> fonctionne mais ne rend pas l’adresse accessible à un téléphone.</p>
<p>Par défaut, seules les images référencées sont copiées depuis <code>sources/img/</code> ; les sources inutilisées ne sont pas publiées et les assets de sortie existants restent en place. <code>--inline-images</code> embarque les images Markdown des fiches et textes longs en URI de données, sans dossier <code>img/</code> copié. Le base64 augmente la taille d’environ un tiers avant compression HTTP. Les images HTML brutes à chemin relatif ne peuvent pas être incorporées : le build les nomme et les refuse plutôt que laisser un chemin vers un dossier absent. Gardez une sortie sans incorporation pour <code>verify</code>.</p>
<p>Options de sortie de <code>build</code> et <code>watch</code> : <code>--no-index</code> omet <code>index.html</code>, <code>--no-readme</code> omet le README de série, <code>--no-nav</code> laisse une fiche <code>series-nav</code> sans liens générés, <code>--drafts-only</code> ne prévisualise que les brouillons et <code>--open</code> ouvre le résultat. <code>build --include-drafts</code> inclut les brouillons avec les articles actifs ; <code>verify</code> prend aussi ce choix en charge. <code>--slides-page-numbers on</code> inscrit les numéros en haut à droite (désactivés par défaut, indépendants du compteur dynamique).</p>
<p>Un article unique peut définir <code>page_dest: index.html</code> pour devenir l’accueil du dossier ; aucun index redondant à une carte n’est alors généré. Dans une série multiple avec index, ce nom est réservé. <code>--no-index</code> le libère. Destinations doublons sans distinction de casse, noms dangereux, JSON mal formé, slugs absents ou doublons sont fatals. L’équilibrage des balises HTML est vérifié avant écriture ; ce n’est pas un assainisseur de sécurité.</p>
<p>Retirer un article du tableau, le marquer brouillon/ignoré ou retirer une référence d’image n’efface pas un ancien fichier publié. Examinez le nettoyage fondé sur le manifeste après le build :</p>
<pre><code class="language-bash">
./lightwebpres clean my-series          # preview orphan removal
./lightwebpres clean my-series --force  # remove the listed orphan output
  </code></pre>
<p>Examinez aussi les fichiers périmés sur l’hôte : envoyer les nouveautés ne supprime pas les anciens. En particulier, le push GitLab du constructeur web ne supprime jamais de fichiers.</p>
<h3>Confiance et licences</h3>
<p>Ne construisez que du contenu de confiance. Le HTML brut, scripts compris, passe ; <code>custom.css</code> et un éventuel <code>nav.js</code> local sont du code choisi par l’auteur. Assainissez exports CMS, traductions et entrées non fiables avant le build. Les liens symboliques sortant des racines sont suivis et signalés par <code>audit</code>, pas confinés. Les tags filtrent des vues, pas les accès : seules les fiches <code>excluded</code> sont omises au build. Les notes présentateur sont du HTML public ; les champs <code>comment:</code> ne sont pas publiés.</p>
<p>Le programme est sous GPL v3 ou ultérieure, avec l’<a href="https://github.com/Fade78/lightwebpres/blob/main/COPYING.EXCEPTION" hreflang="en">Output Exception</a>. Vos présentations générées peuvent adopter les conditions de votre choix, commerciales ou non ; l’exception ne couvre pas un générateur utilisant la sortie comme modèles. L’exécutable copié par <code>init</code> reste du code GPL : conservez <code>COPYING</code> et <code>COPYING.EXCEPTION</code> lorsque vous distribuez un dépôt de série. Voir le <a href="https://github.com/Fade78/lightwebpres/blob/main/README.md#license" hreflang="en">résumé de licence du README (anglais)</a> et les <a href="https://github.com/Fade78/lightwebpres/blob/main/THIRD-PARTY-NOTICES.md" hreflang="en">notices tierces</a>.</p>
<h2 id="8-present-print-and-share" tabindex="-1">8. Présenter, imprimer et partager</h2>
<p>Chaque page produite est une présentation autonome, utilisable au clavier, à la souris et au toucher, y compris l’index : c’est une page comme les autres, dont chaque pas correspond à une carte d’article. Les commandes ci-dessous permettent de piloter la présentation sans regarder l’écran.</p>
<h3>Clavier</h3>
<table class="comparison-table">
<thead>
<tr>
<th>Touche</th>
<th>Action</th>
</tr>
</thead>
<tbody>
<tr>
<td>↓ / PageDown / →</td>
<td>Fiche suivante — sur l’index, carte d’article suivante</td>
</tr>
<tr>
<td>↑ / PageUp / ← / Backspace</td>
<td>Fiche précédente — sur l’index, carte d’article précédente</td>
</tr>
<tr>
<td>Home</td>
<td>Début de la page — première fiche d’un article ; haut de l’index</td>
</tr>
<tr>
<td>Ctrl/Cmd+Home</td>
<td>Retour à l’index de la série — sur l’index : haut de la page</td>
</tr>
<tr>
<td>End ou Ctrl/Cmd+End</td>
<td>Dernière fiche. Sur l’index : dernière carte d’article</td>
</tr>
<tr>
<td>+ / - / =</td>
<td>Agrandir, réduire ou réinitialiser le zoom de la page (uniquement la page ; Ctrl/Cmd +/- garde le zoom du navigateur)</td>
</tr>
<tr>
<td>F</td>
<td>Plein écran (Échap pour quitter)</td>
</tr>
<tr>
<td>I</td>
<td>Alterner entre le défilement fluide configuré et un saut instantané</td>
</tr>
<tr>
<td>C</td>
<td>Ouvrir le sélecteur des thèmes embarqués</td>
</tr>
<tr>
<td>M</td>
<td>Ouvrir le menu présentateur</td>
</tr>
<tr>
<td>S</td>
<td>Ouvrir le partage de la série, de l’article ou de la fiche courante</td>
</tr>
<tr>
<td>B</td>
<td>Écran de pause noir (appuyer de nouveau pour fermer)</td>
</tr>
<tr>
<td>W</td>
<td>Écran de pause blanc (appuyer de nouveau pour fermer)</td>
</tr>
<tr>
<td>T</td>
<td>Écran de pause dans la couleur du thème (appuyer de nouveau pour fermer)</td>
</tr>
<tr>
<td>N</td>
<td>Afficher ou masquer le panneau présentateur : notes de la fiche courante et titre de la suivante (pas de contenu sur l’index, qui ne contient pas de fiches)</td>
</tr>
<tr>
<td>0–9 puis Entrée</td>
<td>Aller directement à la fiche N (numérotation à partir de 1), pour les présentations d’au moins dix fiches ; sans effet sur l’index</td>
</tr>
<tr>
<td>L</td>
<td>Ouvrir le menu des variantes si les fiches de l’article portent au moins deux tags</td>
</tr>
<tr>
<td>H</td>
<td>Ouvrir l’aide qui reprend toutes les touches de ce tableau</td>
</tr>
<tr>
<td>Esc</td>
<td>Quitter le plein écran ; fermer aussi le panneau présentateur</td>
</tr>
</tbody>
</table>
<p>Chaque action de navigation laisse sa cible visible. Une carte d’index ou de navigation de série reste entièrement dans la fenêtre si sa taille le permet. Une fiche plus haute que l’écran constitue l’exception nécessaire : son sommet s’aligne sur le haut de la fenêtre, puis ses pas de lecture bornés se terminent en alignant son haut ou son bas sur le bord correspondant.</p>
<p>Quand l’aide est ouverte, son contenu défilant reçoit les flèches, PageUp/PageDown, Home/End et Espace. Il en va de même pour le panneau présentateur lorsqu’il a le focus ; s’il est seulement ouvert sans focus, les flèches continuent à parcourir la présentation.</p>
<p>Les écrans de pause B/W/T masquent la fiche pour ramener l’attention du public sur l’intervenant : c’est la fonction d’écran vide de PowerPoint et Keynote. T utilise le fond du thème ; un thème sombre se met donc en pause sur fond sombre, sans éclair blanc.</p>
<h3>Panneau présentateur et compteur de fiches</h3>
<p>Un petit compteur <code>X / N</code> apparaît en bas à gauche et s’estompe avec les autres commandes lorsque la souris est inactive. Saisissez un numéro puis <strong>Entrée</strong> pour aller à la fiche correspondante, ce qui devient pratique au-delà de dix fiches. Ce compteur dynamique est <strong>toujours</strong> affiché, sauf sur l’index où il n’y a rien à compter. Il est indépendant de la numérotation <code>NN / NN</code> gravée en haut à droite, facultative et désactivée par défaut, activable par <code>--slides-page-numbers on</code>, les métadonnées d’article <code>slide_page_numbers</code> ou <code>series_meta.slide_page_numbers</code> (voir specifications.md §3.3.5). Appuyez sur <strong>N</strong> pour ouvrir le panneau présentateur : il montre le champ <code>note:</code> de la fiche courante et le titre de la suivante. Le panneau s’ouvre dans la même page ; les personnes regardant l’écran projeté ou partagé le voient aussi. Il suit la navigation ; <strong>N</strong> le referme. Il n’existe pas de fenêtre présentateur privée séparée.</p>
<p>Une note présentateur est un champ <code>note:</code> de la fiche, distinct d’une note de bas de page <code>[^n]</code>, qui est une note de <em>source</em> imprimée pour le lecteur :</p>
<pre><code class="language-markdown">
&lt;!-- lwp:slide --&gt;
slug: speaker-example
kicker: Two
## Slide two
note: Mention the 2020 study — the audience asked for it last time.
  Follow up with the 2023 replication.
  If time runs short, skip the appendix.
  </code></pre>
<p>La valeur <code>note:</code> est incorporée dans le HTML comme élément masqué et affichée par le panneau présentateur. Toute personne possédant la page peut ouvrir ce panneau ou examiner sa source : n’y placez aucune information confidentielle.</p>
<p>Une <code>note:</code> peut s’étendre sur plusieurs lignes : une ligne commençant par un espace prolonge la note ; une ligne vide indentée sépare les paragraphes. Le bloc se termine à la première ligne non vide et non indentée (champ suivant ou corps de la fiche) ; les continuations ne deviennent donc pas le contenu de la fiche.</p>
<h3>Impression et PDF</h3>
<p>Chaque page est prête à imprimer. Lancez <strong>Imprimer</strong> dans le navigateur (Ctrl/Cmd+P), puis « Enregistrer au format PDF » : chaque fiche occupe une feuille, les commandes disparaissent et les couleurs du thème sont conservées. Une fiche courte ne laisse plus une page vide : chaque feuille s’adapte à son contenu.</p>
<p>Pour du noir sur blanc, appuyez sur <strong>C</strong> et choisissez <strong>Print Ink</strong> avant d’ouvrir l’impression. Ce thème est inclus par défaut dans le lot essentiel ; l’impression ne le sélectionne pas automatiquement.</p>
<h3>Souris</h3>
<table class="comparison-table">
<thead>
<tr>
<th>Geste</th>
<th>Action</th>
</tr>
</thead>
<tbody>
<tr>
<td>Clic simple sur le contenu</td>
<td>Fiche suivante (défilement configuré, 200 ms par défaut)</td>
</tr>
<tr>
<td>Clic droit sur le contenu</td>
<td>Fiche précédente (défilement configuré, 200 ms par défaut)</td>
</tr>
<tr>
<td>Clic pendant le défilement</td>
<td>Saut direct vers la cible du clic</td>
</tr>
<tr>
<td>Bouton central, n’importe où</td>
<td>Quitter le plein écran directement ; pour y entrer, appuyer au centre puis cliquer à gauche dans la fenêtre</td>
</tr>
<tr>
<td>Clic dans le coin inférieur droit</td>
<td>Afficher ou masquer les boutons de navigation</td>
</tr>
</tbody>
</table>
<p>Les clics sur liens, images, boutons et fenêtre de partage ne sont pas interceptés : ils gardent leur fonction. Le clic droit pour revenir convient à une souris sans fil tenue en main : clic gauche pour avancer, clic droit pour reculer, sans viser. Le menu contextuel natif est désactivé sur le contenu des fiches pour que ce geste serve au retour. Un clic sélectionne immédiatement la carte suivante puis y glisse pendant la durée configurée (200 ms par défaut). Un nouveau clic pendant ce mouvement n’attend pas : il rejoint directement sa cible ; deux clics rapprochés avancent donc de deux fiches, et un clic droit pendant le mouvement revient à la fiche quittée. Le bouton central seul ne fait que quitter le plein écran : les navigateurs refusent <code>requestFullscreen()</code> depuis un événement autre qu’un clic gauche. L’entrée demande donc deux gestes : bouton central pour armer l’intention, puis clic gauche dans la fenêtre (un clic droit à ce moment rejoint l’index). La molette continue à faire défiler ; le bouton ⛶ et F restent des accès directs. Échap quitte le plein écran. Le pointeur se masque après une seconde d’inactivité en plein écran. Un clic gauche sur une sélection existante efface seulement la surbrillance, sans avancer ; un clic droit sur une sélection ouvre le menu du navigateur. Deux clics rapprochés restent deux pas : la présentation n’attribue pas d’autre sens au double-clic.</p>
<h3>Tactile (téléphone, tablette)</h3>
<table class="comparison-table">
<thead>
<tr>
<th>Geste</th>
<th>Action</th>
</tr>
</thead>
<tbody>
<tr>
<td>Balayer vers la gauche</td>
<td>Fiche suivante — sur l’index, carte d’article suivante</td>
</tr>
<tr>
<td>Balayer vers la droite</td>
<td>Fiche précédente — sur l’index, carte d’article précédente</td>
</tr>
<tr>
<td>Toucher le contenu</td>
<td>Fiche suivante — sur l’index, carte d’article suivante</td>
</tr>
<tr>
<td>Double toucher</td>
<td>Afficher ou masquer immédiatement la navigation</td>
</tr>
<tr>
<td>Appui prolongé</td>
<td>Sélectionner du texte et ouvrir le menu de copie — la présentation ne l’intercepte pas</td>
</tr>
</tbody>
</table>
<h3>Boutons de navigation</h3>
<p>Les boutons ronds en bas à droite forment une colonne : de bas en haut, Menu, descendre, monter et plein écran. Les flèches sont grisées quand aucun déplacement supplémentaire n’est possible. L’index de série, le partage, Défilement (aussi <strong>I</strong>) et le filtre de variantes figurent dans le menu présentateur, avec les thèmes, l’aide, les notes et les écrans de pause. Les mêmes commandes sont présentes sur l’index, où précédent et suivant se déplacent d’une carte d’article. Après trois secondes d’inactivité de la souris, boutons et pointeur disparaissent : l’intervenant n’a pas besoin de commandes sur le mur. En plein écran, ce délai est d’une seconde. Bougez la souris pour faire revenir les boutons ; le pointeur attend 250 ms de mouvement continu, pour qu’un choc sur la table ne suffise pas à le faire réapparaître.</p>
<p>Sur téléphone ou tablette, les commandes s’estompent également après trois secondes. Un <strong>double toucher</strong> inverse immédiatement leur visibilité : les commandes visibles disparaissent ; les commandes cachées reviennent avec un nouveau compte à rebours. Si le premier toucher a déjà lancé un déplacement, la reconnaissance du double geste l’annule et rétablit la fiche et la position précédentes. Un toucher ou un défilement relance le délai tant que les commandes sont visibles : elles ne disparaissent pas sous le doigt. Une fois cachées, elles ne répondent plus au toucher, ce qui laisse libre le coin du contenu. Le plein écran utilise le bouton ⛶, plutôt que le bouton central : ce dernier seul quitte le plein écran ; y entrer demande le bouton central suivi d’un clic gauche. À la souris, cliquer dans le coin hors d’un bouton inverse la visibilité.</p>
<p>La sélection de texte, l’appui prolongé et le menu de copie restent ceux du navigateur. Le double toucher de navigation est reconnu à partir des événements tactiles, pas des clics différés synthétisés par le navigateur ; ces clics ne peuvent donc pas faire avancer la présentation après l’annulation du premier toucher.</p>
<h3>Partager une série, un article ou une fiche</h3>
<p>Appuyez sur <strong>S</strong> ou choisissez Partager dans <strong>M</strong>. Sélectionnez la portée, puis copiez le lien ou affichez son QR code généré localement. Série vise <code>index.html</code>, Article la page courante et Fiche l’ancre <code>slug:</code> de la fiche actuelle. Sur l’index, Article vise l’index lui-même et la portée Fiche est désactivée. Les slugs, et non les positions ou titres, stabilisent les adresses partagées.</p>
<p>Le partage QR demande une adresse HTTP(S) accessible depuis le téléphone destinataire. Une URL de fichier local ou de boucle locale ne convient pas ; l’interface l’explique au lieu de proposer un QR trompeur. Publiez d’abord, puis testez l’adresse hébergée. Aucun service QR ne reçoit le lien.</p>
<p>Le plein écran est un geste explicite via <strong>F</strong> ou un bouton, pas une conséquence de la rotation du téléphone. Il demande le maintien de l’écran allumé lorsque le navigateur le permet ; sinon, le système peut encore l’assombrir. La barre de défilement s’estompe avec la navigation sans modifier la disposition. Entrer ou sortir du plein écran et cliquer dans le coin des boutons révèle immédiatement les commandes.</p>
<p>La durée de glissement par défaut est <code>200</code> ms. Définissez <code>series_meta.scroll_duration</code> ou passez <code>--scroll-duration milliseconds</code> à <code>build</code>, <code>verify</code> ou <code>watch</code> ; <code>0</code> est instantané. L’action Défilement dans <strong>M</strong>, également <strong>I</strong>, alterne entre cette durée et <code>0</code> et affiche la valeur active.</p>
<h2 id="9-build-in-the-browser" tabindex="-1">9. Construire dans le navigateur</h2>
<p><code>web/index.html</code> exécute le même programme non modifié dans <a href="https://pyodide.org" rel="noopener" target="_blank">Pyodide</a> embarqué (CPython compilé en WebAssembly). Deux onglets partagent le même chargement du moteur :</p>
<ul>
<li><strong>Importer un ZIP :</strong> sélectionnez une archive de série et téléchargez un ZIP de <code>public/</code>. Le build reste dans l’onglet. Les archives dépassant 500 Mio, compressées ou décompressées, sont refusées avant extraction ; Pyodide se charge localement, pas depuis un CDN.</li>
<li><strong>Synchroniser avec GitLab :</strong> configurez instance, dépôt et identifiants, récupérez la série, construisez-la et envoyez-la. Les requêtes vont directement à GitLab, sans proxy tiers. L’envoi crée ou met à jour les fichiers mais ne les supprime jamais. Les actions sont groupées par 100 fichiers au plus par commit ; les envois plus gros créent plusieurs commits. C’est une précaution locale, pas une limite GitLab du nombre de fichiers. Le client REST n’assure pas de limitation automatique du débit ni de nouvelles tentatives ; les limites de taille et de débit de l’instance restent applicables.</li>
</ul>
<h3>Servir le constructeur web</h3>
<p>Contrairement aux articles générés, le constructeur doit être servi en HTTP(S), pas ouvert avec <code>file://</code>, car les navigateurs y bloquent les ressources Pyodide. Depuis les sources, servez le dossier contenant à la fois <code>lightwebpres</code> et <code>web/</code> :</p>
<pre><code class="language-bash">
python3 -m http.server 8000 --bind 127.0.0.1 --directory /path/to/lightwebpres
  </code></pre>
<p>Ouvrez <code>http://localhost:8000/web/index.html</code>. Une ouverture incorrecte en <code>file://</code> affiche une commande de correction calculée d’après l’emplacement de la page, avec un bouton Copier.</p>
<p>Pour le déploiement, conservez <code>vendor/</code>, <code>app.py</code> et <code>git_sync.py</code> avec la page. Elle recherche le programme dans <code>./lightwebpres</code>, puis <code>../lightwebpres</code>. Le premier agencement sert <code>web/</code> comme racine avec l’exécutable à côté ; le second est celui du dépôt décrit plus haut. Les erreurs de programme absent et de type MIME <code>.mjs</code> sont couvertes par specifications.md §23.6 et §23.7. <code>web/.htaccess</code> fournit la configuration MIME Apache lorsque les dérogations sont autorisées. Ce constructeur léger est distinct du projet d’éditeur <code>lightwebpres-gui</code>.</p>
<h2 id="10-automate-and-maintain" tabindex="-1">10. Automatiser et maintenir</h2>
<p>Chaque commande CLI fonctionne sans interaction. <code>verify</code> échoue en cas de divergence de sortie ; <code>audit --strict</code> échoue sur avertissement, y compris une erreur de rendu. <code>audit</code> seul signale sans échouer. Le CLI n’a ni dépendance tierce ni besoin réseau au build : un exécuteur Python peut donc traiter du Markdown amont. Assainissez d’abord le HTML amont non fiable (section 7).</p>
<h3>Construire en intégration continue</h3>
<p><code>init --gitlab-ci</code> écrit facultativement ce travail de build et d’artefact. Il ne configure pas de déploiement sur un hébergement public ; <code>init</code> seul n’émet aucun fichier CI.</p>
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
<p>La commande Python fonctionne sur d’autres exécuteurs. Si <code>public/</code> est versionné, vérifiez-le <strong>avant</strong> de reconstruire, pour ne pas effacer les traces de divergence :</p>
<pre><code class="language-yaml">
  script:
    - python3 lightwebpres verify . --lang fr
    - python3 lightwebpres build . --lang fr
  </code></pre>
<p>Un nouveau clone sans sortie versionnée demande un build, pas ce contrôle initial de divergence. Utilisez les mêmes options de rendu dans <code>verify</code>, dont langue, thèmes et <code>--no-essential-theme</code>. Il ne peut pas reproduire <code>--inline-images</code>.</p>
<h3>Surveiller, cibler les builds et conserver leur provenance</h3>
<pre><code class="language-bash">
./lightwebpres watch my-series --lang en --serve --port 8000 --open
./lightwebpres build my-series --lang en --only first-page.md
  </code></pre>
<p><code>watch</code> surveille par interrogation les sources, <code>series.json</code>, les modèles, les dépendances de présentation et les packs de langue séparés ou historiques. Il détecte les nouveaux fichiers et continue après un échec de reconstruction. Le serveur est facultatif, sur <code>127.0.0.1</code> : c’est une prévisualisation locale, pas un serveur de publication.</p>
<p><code>--only</code> cible un article uniquement si le cache de navigation est valide. Il actualise néanmoins les sorties dérivées (index, README et assets selon les options, manifeste et cache) ; une modification touchant l’index ou la navigation déclenche un build complet. <code>--nav-cache path</code> déplace l’empreinte, normalement dans <code>.lwp-cache/nav.json</code>. Ce cache est un état dérivé supprimable, pas un fichier à modifier à la main. <code>--build-stamp</code> inscrit version et date sur les pages ; <code>--build-stamp-minimal</code> garde un marqueur sans ces valeurs et prime. <code>status: draft</code> et <code>ignored</code> contrôlent les articles entrant dans la sortie normale (section 4).</p>
<h3>Chemins et conventions CLI</h3>
<table class="comparison-table">
<thead>
<tr>
<th>Variable</th>
<th>Remplace</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>LWP_SERIES_DIR</code></td>
<td>Dossier de série par défaut en l’absence d’argument de dossier</td>
</tr>
<tr>
<td><code>LWP_SOURCES_DIR</code>, <code>LWP_TEMPLATES_DIR</code>, <code>LWP_OUTPUT_DIR</code></td>
<td>Racines des sources, personnalisations et sorties</td>
</tr>
<tr>
<td><code>LWP_INTERFACE_DIR</code>, <code>LWP_TYPOGRAPHY_DIR</code>, <code>LWP_LANGUAGE_DIR</code></td>
<td>Racines de langue séparées ou historiques</td>
</tr>
<tr>
<td><code>LWP_LANG</code></td>
<td>Langue de repli du build et langue d’interface explicite</td>
</tr>
<tr>
<td><code>LWP_THEMES_DIR</code>, <code>LWP_IDENTITY_KITS_DIR</code>, <code>LWP_COMMONS_DIR</code></td>
<td>Catalogues utilisateur de thèmes, Identity Kits et presets Commons</td>
</tr>
</tbody>
</table>
<p>Les sous-dossiers de série par défaut sont sous la racine choisie. Un <code>--output path</code> relatif explicite se rapporte au répertoire de travail courant, <strong>pas</strong> à l’argument de série. Utilisez des chemins absolus dans les traitements dont le répertoire courant n’est pas fixe.</p>
<p><code>--lang</code>, <code>--quiet</code>, <code>--verbose</code>, <code>--no-color</code>, <code>--timestamp</code> et <code>--dry-run</code> peuvent précéder la commande ; la valeur la plus proche prime. <code>--quiet</code> masque la progression, pas les avertissements ou valeurs de rapport demandées. <code>--verbose</code> ajoute du détail ; <code>--timestamp</code> préfixe les journaux en RFC 3339. <code>--dry-run</code> décrit les écritures sans toucher au disque. <code>--option=value</code> et <code>--option value</code> sont équivalents. Une option inconnue ou mal placée est fatale. <code>--version</code> est une action initiale, pas un modificateur de commande.</p>
<p>Les raccourcis comme <code>build</code> ont aussi des formes canoniques comme <code>series build</code>. Les anciennes formes (<code>install</code>, <code>check</code>, <code>themes</code>, <code>theme-info</code>, <code>set-theme</code>, <code>series-info</code>, <code>refresh-templates</code>, <code>themes-gallery</code>) échouent en indiquant leur remplacement : ne les utilisez pas dans les scripts. Lancez <code>python3 lightwebpres --help</code> pour la matrice complète, ou <code>python3 lightwebpres build --help</code> pour l’aide contextuelle.</p>
<h3>Mettre à jour l’exécutable et les modèles</h3>
<p>Remplacez l’exécutable du projet par une version plus récente, lisez <code>CHANGELOG.md</code>, puis auditez, reconstruisez et examinez la sortie. La feuille de style composée et les packs intégrés de navigation et langue suivent l’exécutable. Votre thème, vos propriétés épinglées et <code>custom.css</code> restent vos choix.</p>
<p>Un fichier fourni par l’outil et installé avec <code>template write</code> prime sur sa copie intégrée. Le build avertit lorsqu’il en diffère, même avec <code>--quiet</code> ; il ne distingue pas une surcharge périmée d’une personnalisation volontaire. Les séries antérieures à v0.40.0 recevaient automatiquement ces copies. Pour reprendre les valeurs intégrées :</p>
<pre><code class="language-bash">
./lightwebpres template update my-series
./lightwebpres template update my-series --scaffold
  </code></pre>
<p>Une copie identique fournie par l’outil est supprimée. Un <code>nav.js</code> différent est sauvegardé en <code>nav.js.bak</code> puis supprimé. Les packs d’interface ou de typographie différents sont conservés et signalés ; comparez-les à <code>template show</code> avant de les supprimer. Les langues non livrées par l’outil restent intactes. Les fichiers <code>settings.conf</code> et <code>custom.css</code> absents sont créés. <code>--scaffold</code> actualise aussi la surface commentée des réglages en préservant les lignes épinglées.</p>
<p><code>template show nav.js</code>, <code>template show interface/en.json</code> et <code>template show typography/en.json</code> affichent les valeurs intégrées sans série. Utilisez <code>template write &lt;file&gt; my-series</code> pour installer une copie à modifier, et <code>--force</code> seulement pour remplacer une copie existante. Les anciens <code>fr.json</code> et <code>en.json</code> restent pris en charge.</p>
<h3>Complétion du shell</h3>
<p><code>lightwebpres completion --shell bash</code> (ou <code>zsh</code>) affiche un script qui complète commandes, sous-commandes et options à l’appui sur Tab. Installez-le en ajoutant cette ligne à <code>~/.bashrc</code> ou <code>~/.zshrc</code> :</p>
<pre><code class="language-bash">
eval "$(lightwebpres completion --shell bash)"
  </code></pre>
<p>Ensuite <code>lightwebpres &lt;Tab&gt;</code> propose <code>init</code>, <code>build</code>, <code>verify</code>, <code>audit</code>, <code>theme</code>, <code>series</code>… ; <code>lightwebpres series &lt;Tab&gt;</code> propose <code>build</code>, <code>theme</code>, <code>status</code>, <code>resolve</code>… ; et <code>lightwebpres build --&lt;Tab&gt;</code> propose <code>--lang</code>, <code>--output</code>, <code>--no-typography</code>…</p>
<p>Le script est généré à partir des tables de commandes de l’outil : il reste donc conforme aux commandes connues de la version exécutée.</p>
<h2 id="11-troubleshooting-and-references" tabindex="-1">11. Dépannage et références</h2>
<h3>En cas de problème</h3>
<table class="comparison-table">
<thead>
<tr>
<th>Symptôme</th>
<th>Contrôle ou correction</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>lightwebpres: command not found</code></td>
<td>Utilisez <code>python3 lightwebpres</code>, <code>./lightwebpres</code> ou son chemin réel ; un nom seul demande une configuration de <code>PATH</code>.</td>
</tr>
<tr>
<td><code>Permission denied</code> sous Unix</td>
<td><code>chmod +x lightwebpres</code>, ou invocation via Python.</td>
</tr>
<tr>
<td>Windows ne peut pas lancer le fichier</td>
<td>Utilisez <code>python lightwebpres</code> ou le lanceur <code>py lightwebpres</code> ; Windows n’utilise pas le shebang.</td>
</tr>
<tr>
<td><code>python3: command not found</code></td>
<td>Essayez <code>python</code> ou <code>py</code> et vérifiez sa version ; installez Python 3.8+ s’il manque.</td>
</tr>
<tr>
<td>Le dossier cible n’est pas vide</td>
<td>Préférez un nouveau dossier. Examinez les fichiers avant de choisir volontairement <code>init --force</code>.</td>
</tr>
<tr>
<td>La langue d’interface vous surprend</td>
<td>Sans langue explicite, le navigateur choisit ; utilisez <code>--lang en</code> ou <code>fr</code> pour la fixer (section 6).</td>
</tr>
<tr>
<td>Une ligne <code>field:</code> apparaît comme texte</td>
<td>Les champs doivent précéder le texte du corps (section 3).</td>
</tr>
<tr>
<td>Une définition de note apparaît comme texte</td>
<td>Sortez-la du bloc HTML brut ; les identifiants acceptent lettres, chiffres et soulignés, pas les traits d’union.</td>
</tr>
<tr>
<td>Un appel de note n’est pas un lien</td>
<td>Définissez la note dans la même portée ; <code>audit</code> nomme les appels non résolus.</td>
</tr>
<tr>
<td>Un titre ou une couleur ignore votre modification</td>
<td><code>resolve my-series page_title --article first-page.md</code> ou <code>resolve my-series kicker.fg</code> montre les niveaux gagnants et supplantés.</td>
</tr>
<tr>
<td>Un article est absent</td>
<td>Vérifiez son inscription, son <code>status</code>, ses tags et ses fiches effectives avec <code>status</code> et <code>series tags</code>.</td>
</tr>
<tr>
<td>Une ancienne page reste en ligne</td>
<td>Examinez <code>clean</code> en local, puis retirez aussi les fichiers périmés de l’hôte (section 7).</td>
</tr>
<tr>
<td><code>verify</code> signale une divergence sans modification des sources</td>
<td>Faites correspondre les options de rendu ; un build avec images incorporées demande une sortie de vérification séparée sans incorporation.</td>
</tr>
<tr>
<td>Le constructeur échoue en <code>file://</code> ou sur <code>.mjs</code></td>
<td>Servez le constructeur et vérifiez l’emplacement de l’exécutable et les types MIME (section 9).</td>
</tr>
</tbody>
</table>
<h3>Repères de commandes</h3>
<table class="comparison-table">
<thead>
<tr>
<th>Tâche</th>
<th>Commandes et chapitre</th>
</tr>
</thead>
<tbody>
<tr>
<td>Créer et prévisualiser</td>
<td><code>init</code>, <code>demo</code>, <code>build</code>, <code>watch</code> (1, 2, 10)</td>
</tr>
<tr>
<td>Examiner contenu et noms</td>
<td><code>status</code>, <code>series tags</code>, <code>series slug</code>, <code>resolve</code>, <code>contract</code> (3, 4, 7)</td>
</tr>
<tr>
<td>Compléter les identités de fiches manquantes</td>
<td><code>series slug set --dry-run</code>, puis <code>series slug set</code> (3)</td>
</tr>
<tr>
<td>Choisir une présentation</td>
<td><code>preset list/show</code>, <code>series preset</code>, <code>series preset set</code> (5)</td>
</tr>
<tr>
<td>Choisir ou emporter des thèmes</td>
<td><code>theme list/show/gallery/create/migrate/vendor/path</code>, <code>series theme</code>, <code>series theme set</code> (5)</td>
</tr>
<tr>
<td>Vérifier et supprimer les sorties périmées</td>
<td><code>audit</code>, <code>verify</code>, <code>clean</code> (7)</td>
</tr>
<tr>
<td>Gérer les surcharges</td>
<td><code>template show/write/update</code> (10)</td>
</tr>
<tr>
<td>Découvrir la syntaxe</td>
<td><code>--help</code>, <code>--help</code> contextuel, <code>--version</code>, <code>completion</code> (10)</td>
</tr>
</tbody>
</table>
<p><code>theme create</code> accepte aussi <code>--label</code>, <code>--family</code>, <code>--source</code>, <code>--note</code>, <code>--output</code> (destination <code>&lt;slug&gt;.conf</code>) et <code>--force</code>. <code>theme show --all</code> décrit le catalogue ; <code>--format json</code> rend les rapports lisibles par les machines. <code>theme vendor --force</code> remplace les instantanés déjà copiés. <code>theme gallery --output path</code> choisit la destination HTML. Ces opérations sont explicites : un build ordinaire n’écrase pas vos fichiers de thèmes.</p>
<h3>Références approfondies</h3>
<ul>
<li><strong><code>SKILL.md</code></strong> (<code>agent/skills/lightwebpres/</code>) décrit précisément le format d’article : chaque type et champ de fiche, bloc de métadonnées, transition champs/texte libre, typographie et désactivations, liens dans <code>series.json</code>. Lisez-le avant d’écrire ou déboguer un article à la main, ou indiquez-le à un agent.</li>
<li>Le <a href="https://github.com/Fade78/lightwebpres/blob/main/agent/skills/sourced-presentation/SKILL.md" hreflang="en">skill invité sourced-presentation</a> est une méthode éditoriale facultative et indépendante, pas un prérequis du produit.</li>
<li><strong><code>specifications.md</code></strong> (en français) est la référence complète faisant autorité : algorithmes exacts, cas limites du parseur, schémas complets de <code>series.json</code> et des fichiers de langue, fonctionnement interne du constructeur web.</li>
<li><strong><code>lightwebpres --help</code></strong> présente toutes les commandes, options et variables d’environnement.</li>
<li><a href="https://github.com/Fade78/lightwebpres/blob/main/GLOSSARY.md" hreflang="en">GLOSSARY.md</a> décrit le sens des champs, leurs défauts et les chaînes de repli.</li>
<li><a href="https://github.com/Fade78/lightwebpres/blob/main/AGENTS.md" hreflang="en">AGENTS.md</a> décrit les règles de contribution et de régénération ; <a href="https://github.com/Fade78/lightwebpres/blob/main/DECISIONS.md" hreflang="en">DECISIONS.md</a> consigne les décisions et travaux restants.</li>
</ul>