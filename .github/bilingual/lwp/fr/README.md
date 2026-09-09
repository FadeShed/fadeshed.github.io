# Le site GitHub Pages de LightWebPres

Le site public est lui-même une série LightWebPres : un index natif, six
articles en français et un kit d’identité autonome. Le moteur `lightwebpres`
est utilisé sans modification. Aucun framework web, paquet Python, police
externe ou CDN n’est nécessaire à la construction du site.

## Construire et lire

Depuis la racine du dépôt, avec Python 3.8 ou ultérieur :

```bash
python3 tools/build_website.py
python3 tools/check_website.py generated/site
python3 -m http.server 8000 --bind 127.0.0.1 --directory generated/site
```

Ouvrir `http://localhost:8000/`. Le double-clic sur `generated/site/index.html`
convient aux pages générées ; le constructeur `web/` exige HTTP(S).

La sortie complète est `generated/site/`. Ne jamais la modifier à la main.
La construction travaille dans un dossier temporaire, appelle `build`,
`audit --strict` et `verify` avec la même langue, puis remplace la sortie
validée. Un dossier existant sans le marqueur `.lightwebpres-website` ne sera
pas effacé. `--output /chemin/vers/un/nouveau/site` choisit une autre sortie.

## Les sources

| Chemin | Responsabilité |
| --- | --- |
| `website/series.json` | Ordre des parcours et texte de l’accueil natif. |
| `website/sources/*.md` | Texte des six parcours. |
| `website/templates/kits/lightwebpres-site/1.0.0/` | Fragments de contenu, géométrie contrainte et deux thèmes typés complets. |
| `website/templates/custom.css` | Adaptation explicite du shell et de l’impression. Aucun remplacement du runtime. |
| `website/example/` | Vrai projet téléchargeable et véritable page de démonstration. |
| `tools/build_website.py` | Orchestration de la construction, des copies et des archives. |
| `tools/check_website.py` | Contrôle statique des liens, des ancres, des assets et des téléchargements. |
| `tools/check_website_browser.py` | Contrôle facultatif dans Chromium ; exige le Playwright Python et Chromium. |
| `.github/workflows/pages.yml` | Construction sur push/PR et publication de main. |

Le build ajoute dans sa copie de travail les deux captures existantes de
`generated/`, sans en créer une seconde source suivie. Il régénère le guide
par `tools/build_guide.py` et la galerie par `lightwebpres theme gallery`.
Les documents originaux et les skills sont copiés, pas réécrits. Le guide
conserve son identité de documentation et sa langue d’origine, l’anglais.

L’exemple de code affiché dans l’accueil est un extrait. Il respecte les
champs sur une ligne et mène à la vraie démo. Dans les exemples au sein d’un
article LWP, les marqueurs sont échappés en HTML : le parseur détecte les
marqueurs de fiche et les séparateurs **avant** de traiter les code fences.
Les afficher naïvement dans une fence peut changer le type de la fiche.

## Publier sur GitHub Pages

La cible prévue est le site de projet du dépôt `Fade78/lightwebpres` :
`https://fade78.github.io/lightwebpres/`. Ce chemin est une cible, pas une
attestation que le site a été déployé.

Dans GitHub, choisir **Settings → Pages → Build and deployment → Source →
GitHub Actions**. Ajouter les sources à la branche `main`, avec le workflow.
Les pull requests construisent et vérifient, mais ne déploient pas.
Le workflow installe Playwright et Chromium uniquement pour tester le site
assemblé, y compris une véritable compilation ZIP dans Pyodide. Un échec
de ce contrôle empêche la publication ; le build local reste sans dépendances.
Le job de déploiement de `main` n’écrit que sur Pages ; il ne crée aucun tag
ou release et ne modifie aucun paramètre du dépôt.

Le workflow reprend les actions du guide officiel GitHub, consulté le
9 septembre 2026 :
https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

Les liens du site sont relatifs. Tester également un hébergement sous le
préfixe `/lightwebpres/`. Une nouvelle construction remplace tout l’artefact :
les fichiers périmés n’y restent pas. Le script ne supprime jamais des sources.

## Vérifier et maintenir

```bash
python3 tests/run_tests.py
python3 -m py_compile lightwebpres tools/build_website.py tools/check_website.py
python3 tools/check_refs.py
python3 tools/build_website.py
python3 tools/check_website.py generated/site
python3 tools/check_website_browser.py generated/site --screenshots /tmp/lwp-site-captures
```

Les contrôles navigateur facultatifs servent les fichiers sous un préfixe
de site de projet, inspectent les vues mobile et bureau, la navigation au
clavier, le changement d’apparence et le constructeur Pyodide. L’installation
de Playwright est réservée aux tests : elle ne fait pas partie du build.
Le workflow suit aussi la procédure officielle de tests navigateur :
https://playwright.dev/python/docs/ci-intro

Sur un poste de test sans ces dépendances :

```bash
python3 -m pip install 'playwright>=1.56,<2'
python3 -m playwright install --with-deps chromium
```

`--chromium /chemin/vers/chromium` utilise un navigateur déjà installé.
Le mode explicite `--render-only` est réservé aux environnements qui
interdisent la navigation du navigateur. Il rend les HTML en mémoire,
avec les images locales embarquées uniquement dans le document de test,
mesure la mise en page, teste les apparences et l’aide, puis contrôle les
entrées HTTP avec Python. Il **ne valide pas** la navigation par URL,
la persistance des préférences, le plein écran ni Pyodide de bout en bout.
`--report /chemin/rapport.json` enregistre les contrôles et les omissions.

`build-info.json` expose la version, son statut lu dans `CHANGELOG.md` et les
empreintes des sources. Le téléchargement CLI contient **ce moteur exact**,
pas une promesse de dernière release. Les licences accompagnent toutes les
archives qui redistribuent l’exécutable. `site-sources.zip` est explicitement
un ajout à une copie du dépôt, pas un dépôt complet autonome.

## Limites conservées volontairement

Le site n’ajoute aucun service d’analyse d’audience, moteur de recherche
distant ni téléchargement de police. Les commandes de présentation,
le stockage des préférences et les fonctions de partage sont ceux de LWP.
Le constructeur web reste celui de `web/`, avec ses fichiers Pyodide locaux.
Les rapports de contraste des thèmes ne certifient pas le CSS personnalisé ;
la vérification visuelle et clavier reste nécessaire.
