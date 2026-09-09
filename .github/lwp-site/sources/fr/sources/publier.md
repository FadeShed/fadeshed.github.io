<!-- lwp:meta -->
page_title: Vérifier, puis publier — LightWebPres
page_desc: Le bon dossier, les bons contrôles et des liens qui restent stables.
card_title: Vérifier, puis publier
card_desc: Le bon dossier, les bons contrôles et des liens qui restent stables.
card_label: 05 / PUBLIER
nav_title: Vérifier, puis publier
nav_desc: Le bon dossier, les bons contrôles et des liens qui restent stables.
---

<!-- lwp:slide:cover -->
slug: ouverture
kicker: 05 / PUBLIER
# Vos fichiers.<br>Votre hébergement.<br>Votre adresse.
summary: Le résultat est statique. Aucun moteur Python ni serveur applicatif n’est nécessaire chez le lecteur.

---

<!-- lwp:slide -->
slug: verifier-la-sortie
kicker: AVANT DE METTRE EN LIGNE
## Audit et verify ne répondent pas à la même question.
summary: Le premier inspecte les sources et le rendu. Le second compare les fichiers publiés à ce que le moteur reconstruirait.
source: <a href="guide/guide.html#7-verify-and-publish">Guide · Verify and publish</a>.

```bash
python3 lightwebpres build ma-serie --lang fr
python3 lightwebpres audit ma-serie --lang fr --strict
python3 lightwebpres verify ma-serie --lang fr
```

Sans `--strict`, **audit peut sortir avec un code zéro malgré ses avertissements**. `verify` demande les mêmes options de rendu que le build et ne prend pas en charge `--inline-images`.

Si votre sortie est déjà suivie dans Git, lancez `verify` **avant** de reconstruire pour ne pas effacer la preuve d’un décalage.

---

<!-- lwp:slide -->
slug: bon-dossier
kicker: CE QUI PART CHEZ L’HÉBERGEUR
## Publiez public/. Pas tout votre projet.
summary: Gardez ensemble les pages HTML, les images référencées et les assets des kits.
source: <a href="guide/guide.html#7-verify-and-publish">Guide · Publish the output, not the project</a>.

```text
public/
  index.html
  ma-page.html
  img/
  assets/presentations/
```

Le HTML se lit aussi localement. Mais une adresse locale n’est pas une adresse publique : un QR code à partager demande une URL HTTP(S) accessible depuis l’appareil du destinataire.

Retirer une source ne supprime pas automatiquement un ancien fichier hébergé. Examinez la proposition de `clean` et les fichiers restés sur l’hôte.

---

<!-- lwp:slide -->
slug: github-pages
kicker: CE SITE, CONCRÈTEMENT
## GitHub Pages reçoit une sortie déjà construite.
summary: Le workflow livré construit le site avec le moteur du dépôt, vérifie le résultat et publie uniquement l’artefact généré.
source: <a href="https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages">Documentation GitHub · Custom workflows</a> ; <a href="downloads/site-sources.zip">Sources de ce site et workflow</a>.

```bash
python3 tools/build_website.py
python3 tools/check_website.py generated/site
```

Dans le dépôt GitHub, sélectionnez **Settings → Pages → Source → GitHub Actions**. Le fichier `.github/workflows/pages.yml` sépare vérification, construction et déploiement ; il ne crée aucune release.

Les chemins internes restent relatifs pour fonctionner sous `/lightwebpres/`, pas seulement à la racine d’un domaine.

---

<!-- lwp:slide -->
slug: limites
kicker: UNE PUBLICATION SANS FAUSSE PROMESSE
## Public veut dire public.
summary: Le format rend des sources de confiance. Il ne nettoie pas le HTML et ne transforme pas les tags en droits d’accès.
source: <a href="reference/README.md">README · Safety et License</a> ; <a href="reference/COPYING.EXCEPTION">Output Exception</a>.

Les notes `note:` sont embarquées et le panneau présentateur apparaît sur le même écran que la présentation. Les tags filtrent des vues ; ils ne protègent pas le contenu.

Le programme est sous **GPL v3 ou ultérieure avec Output Exception**. L’exception laisse choisir les conditions de diffusion des présentations normales ; le moteur redistribué reste sous GPL. Conservez les textes de licence avec l’exécutable. 

---

<!-- lwp:slide:series-nav -->
slug: continuer
