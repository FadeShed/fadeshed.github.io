from html import escape

TEXT={
'en':{
 'skip':'Skip to content','nav':['Use cases','Identities','Create','Documentation'],
 'eyebrow':'ONE CONTENT. MANY WAYS FORWARD.',
 'title':'One document.<br>Read. Present.<br><em>Publish.</em>',
 'lead':'A course, a research brief, a project update. Keep the main ideas, the sources and the full story together — in pages your audience can open in a browser.',
 'cta':'Explore a document','cta2':'Find your use case',
 'reassure':'No installation for your readers. Editable sources for you.',
 'landscape':'Present on a screen','portrait':'Read on a phone','heroalt':'The same article displayed in landscape and portrait',
 'strip':['Your text, not a locked slide deck.','One article, several identities.','Files you can keep and share.'],
 'journeylabel':'THE WHOLE STORY STAYS TOGETHER',
 'journeytitle':'An overview for the room.<br>Depth for the reader.',
 'journeytext':'Cards give a talk its rhythm. Sources and long-form text give people somewhere to return. Long content scrolls; it is not cut down to fit a slide.',
 'phases':[('Before','Set the context.','Send a brief to read before the conversation.'),('During','Follow the ideas.','Present the same document, one card at a time.'),('After','Return to the detail.','Leave the explanation and references within reach.')],
 'roleslabel':'START WITH THE WORK YOU DO','rolestitle':'There is more than<br>one way to use it.',
 'rolesintro':'Write, teach, organize, design, automate or share. These are routes you can combine — not categories you have to fit.',
 'roles':[
 ('read','Read & present','For a reader, speaker or facilitator','A briefing to read before the meeting, follow during it and consult afterwards.','Explore the reading route'),
 ('write','Write & explain','For an author, teacher or researcher','Keep your key ideas, references and longer explanation in one editable article.','Explore the writing route'),
 ('organize','Organize knowledge','For a documentation owner or editor','Reuse the same article in a short briefing and a larger collection. Change the journey, not the canonical text.','Explore the collection route'),
 ('design','Design an identity','For a designer or a team','Give documents their own typography, layouts and signature — then share that identity with other authors.','Explore the design route'),
 ('automate','Automate a workflow','For a developer, integrator or agent operator','Turn recurring source updates into documents you can build, check and hand over.','Explore the automation route'),
 ('publish','Publish & keep','For a maintainer or independent author','Deliver pages and their assets. Keep the source project for the next edit, migration or backup.','Explore the publishing route')],
 'identitylabel':'SAME WORDS. DIFFERENT PRESENCE.','identitytitle':'Give your work<br>its own identity.',
 'identityintro':'Not just another colour. A layout, a masthead, a reading rhythm. Compare the same article under three presentation choices.',
 'identities':[
 ('native','Original','A clear starting point.','The native layout keeps the document simple, with the Light theme.','Native LightWebPres layout in its Light theme'),
 ('docs','Documentation','A recognizable collection.','A blue frame, a logo and a footer bring the document into a coherent publishing identity.','The same article in the LightWebPres documentation identity'),
 ('field-notes','Field Notes','A composed visual language.','A ruled frame, a compass and typewriter typography come together from three source kits.','The same article in the composed Field Notes identity')],
 'openidentity':'Open this presentation','identityhint':'Each view contains the same article. Open one to use its native reader controls.',
 'concepts':[('Theme','Colours, fonts and typed visual properties.'),('Preset','A selection of layouts, chrome and an initial theme.'),('Identity Kit','Those resources and assets, packaged to reuse and share.')],
 'moreappearance':'Explore themes and identity composition',
 'authorlabel':'YOUR WAY OF WORKING. THE SAME SOURCES.','authortitle':'Write it yourself.<br>Or work with an agent.',
 'authorintro':'Three alternatives lead to the same editable project. You can change the way you create without changing the content model.',
 'actors':[('You write','Write and revise in your usual editor.'),('You steer an agent','Brief, review and revise with an external agent.'),('An agent works autonomously','Give an external agent a task and boundaries.')],
 'or':'or','converge':'All three produce','project':'Your editable project',
 'sourceparts':['LWP Markdown','Images','Series configuration'],
 'engine':'One engine. Two ways to build.',
 'browser':'In the browser','browserdesc':'Build a source-project ZIP in the tab and take away its pages.',
 'cli':'With the command line','clidesc':'Use local files, scripts and repeatable build checks.',
 'boundary':'LightWebPres builds the document. Your authoring agent is external.',
 'fullworkflow':'Explore the authoring workflow',
 'keeplabel':'YOU KEEP THE PROJECT. THEY GET THE DOCUMENT.',
 'keeptitle':'A result to hand over.<br>Not a service to keep running.',
 'sourcetitle':'What you keep','sourcetext':'Your editable text, images, series structure and appearance resources. Everything you need to revise the work and build again.',
 'resulttitle':'What your readers receive','resulttext':'HTML pages carrying their CSS and JavaScript, with any referenced images and identity assets. Open them in a browser or publish the output directory.',
 'sourcecta':'Get the example sources','resultcta':'Open the finished document',
 'keepnote':'Keep the whole output directory when assets are separate. The published pages are not a replacement for your authoring sources.',
 'docslabel':'GO AS FAR AS YOU NEED','docstitle':'The full toolkit.<br>Not just the first screen.',
 'docsintro':'Keep exploring the complete portal: writing, collections, appearance, publishing and integration.',
 'resources':[('guide/guide.html','Read the guide','The complete manual, in a document you can present.'),('themes.html','Browse the theme gallery','Compare the visual choices and their components.'),('web/','Build in the browser','From a prepared source project to a ZIP of pages.')],
 'endtitle':'Start with a document.<br><em>Make the next one yours.</em>',
 'footer':'A FadeShed tool. Read, present and share.', 'license':'Licences & notices', 'source':'Project source',
},
'fr':{
 'skip':'Aller au contenu','nav':['Usages','Identités','Créer','Documentation'],
 'eyebrow':'UN MÊME CONTENU. PLUSIEURS POSSIBILITÉS.',
 'title':'Un même contenu.<br>À lire. À présenter.<br><em>À publier.</em>',
 'lead':'Un cours, une synthèse de recherche, un point de projet. Gardez les idées principales, les sources et le récit complet ensemble — dans des pages que chacun ouvre avec son navigateur.',
 'cta':'Explorer un document','cta2':'Trouver mon usage',
 'reassure':'Rien à installer pour vos lecteurs. Des sources modifiables pour vous.',
 'landscape':'Présenter sur grand écran','portrait':'Lire sur téléphone','heroalt':'Le même article affiché en paysage et en portrait',
 'strip':['Votre texte, pas des diapositives figées.','Un article, plusieurs identités.','Des fichiers à garder et à partager.'],
 'journeylabel':'LE RÉCIT COMPLET RESTE ACCESSIBLE',
 'journeytitle':'La vue d’ensemble pour la salle.<br>Les détails pour le lecteur.',
 'journeytext':'Les fiches donnent un rythme à la présentation. Les sources et le texte long permettent d’y revenir. Un contenu long se fait défiler : il n’est pas raccourci pour tenir dans une diapositive.',
 'phases':[('Avant','Poser le contexte.','Envoyez un dossier à lire avant la discussion.'),('Pendant','Suivre les idées.','Présentez le même document, fiche après fiche.'),('Après','Retrouver les détails.','Laissez les explications et les références à portée de main.')],
 'roleslabel':'PARTEZ DE CE QUE VOUS VOULEZ FAIRE','rolestitle':'Plusieurs usages.<br>Une place pour le vôtre.',
 'rolesintro':'Écrire, enseigner, organiser, concevoir, automatiser ou partager. Des parcours à combiner, pas des cases dans lesquelles entrer.',
 'roles':[
 ('read','Lire et présenter','Pour un lecteur, intervenant ou animateur','Un dossier à lire avant une réunion, à suivre pendant et à consulter après.','Explorer le parcours de lecture'),
 ('write','Écrire et expliquer','Pour un auteur, enseignant ou chercheur','Réunissez les idées clés, les références et les explications dans un article modifiable.','Explorer le parcours de rédaction'),
 ('organize','Organiser les connaissances','Pour un responsable documentaire','Réutilisez le même article dans un dossier court et une collection plus vaste. Changez le parcours, pas le texte de référence.','Explorer le parcours documentaire'),
 ('design','Concevoir une identité','Pour un designer ou une équipe','Donnez aux documents leur typographie, leur mise en page et leur signature. Transmettez ensuite cette identité à d’autres auteurs.','Explorer le parcours de conception'),
 ('automate','Automatiser une production','Pour un développeur ou un intégrateur','Transformez des mises à jour récurrentes en documents à construire, à vérifier et à transmettre.','Explorer le parcours d’automatisation'),
 ('publish','Publier et conserver','Pour un mainteneur ou un auteur indépendant','Livrez les pages et leurs ressources. Gardez le projet source pour la prochaine révision, migration ou sauvegarde.','Explorer le parcours de publication')],
 'identitylabel':'LES MÊMES MOTS. UNE AUTRE PRÉSENCE.','identitytitle':'Donnez une identité<br>à vos documents.',
 'identityintro':'Pas seulement une autre couleur. Un cadre, une signature, un rythme de lecture. Comparez le même article sous trois présentations.',
 'identities':[
 ('native','Original','Un point de départ sobre.','La mise en page native privilégie la simplicité, avec le thème clair.', 'Mise en page native de LightWebPres avec son thème clair'),
 ('docs','Documentation','Une collection reconnaissable.','Un cadre bleu, un logo et un pied de page inscrivent le document dans une identité éditoriale cohérente.','Le même article dans l’identité documentaire de LightWebPres'),
 ('field-notes','Field Notes','Une identité composée.','Un cadre de carnet, une boussole et une typographie de machine à écrire réunissent les apports de trois kits sources.','Le même article dans l’identité composée Field Notes')],
 'openidentity':'Ouvrir cette présentation','identityhint':'Chaque vue contient le même article. Ouvrez-en une pour utiliser les commandes natives du lecteur.',
 'concepts':[('Thème','Les couleurs, les polices et les propriétés visuelles typées.'),('Preset','Un choix de mises en page, d’habillage et de thème initial.'),('Identity Kit','Ces ressources et éléments visuels, réunis pour être réutilisés et partagés.')],
 'moreappearance':'Explorer les thèmes et la composition d’identités',
 'authorlabel':'VOTRE MANIÈRE DE TRAVAILLER. LES MÊMES SOURCES.','authortitle':'Écrivez vous-même.<br>Ou travaillez avec un agent.',
 'authorintro':'Trois voies possibles aboutissent au même projet modifiable. Votre manière de créer peut changer sans changer le modèle de contenu.',
 'actors':[('Vous écrivez','Rédigez et révisez dans votre éditeur habituel.'),('Vous pilotez un agent','Donnez une consigne, relisez et révisez avec un agent externe.'),('Un agent travaille en autonomie','Confiez à un agent externe une tâche et ses limites.')],
 'or':'ou','converge':'Les trois produisent','project':'Votre projet modifiable',
 'sourceparts':['Markdown LWP','Images','Configuration de série'],
 'engine':'Un moteur. Deux façons de construire.',
 'browser':'Dans le navigateur','browserdesc':'Construisez un projet source ZIP dans l’onglet et récupérez les pages.',
 'cli':'En ligne de commande','clidesc':'Utilisez vos fichiers locaux, vos scripts et des contrôles reproductibles.',
 'boundary':'LightWebPres construit le document. L’agent de rédaction reste externe.',
 'fullworkflow':'Explorer le parcours de création',
 'keeplabel':'VOUS GARDEZ LE PROJET. ILS REÇOIVENT LE DOCUMENT.',
 'keeptitle':'Un résultat à transmettre.<br>Pas un service à maintenir.',
 'sourcetitle':'Ce que vous conservez','sourcetext':'Le texte modifiable, les images, l’organisation de la série et ses ressources d’apparence. De quoi réviser le travail et le reconstruire.',
 'resulttitle':'Ce que vos lecteurs reçoivent','resulttext':'Des pages HTML avec leur CSS et leur JavaScript, ainsi que les images et éléments d’identité référencés. À ouvrir dans un navigateur ou à publier avec leur dossier de sortie.',
 'sourcecta':'Récupérer les sources de l’exemple','resultcta':'Ouvrir le document terminé',
 'keepnote':'Conservez le dossier de sortie complet lorsque les ressources sont séparées. Les pages publiées ne remplacent pas les sources modifiables.',
 'docslabel':'ALLEZ AUSSI LOIN QUE NÉCESSAIRE','docstitle':'Toutes les ressources.<br>Au-delà du premier écran.',
 'docsintro':'Retrouvez le portail complet : rédaction, collections, apparence, publication et intégration.',
 'resources':[('guide/guide.html','Lire le guide','Le manuel complet, dans un document que vous pouvez présenter.'),('themes.html','Explorer la galerie','Comparez les apparences et leurs composants.'),('web/','Construire dans le navigateur','D’un projet source préparé à une archive de pages.')],
 'endtitle':'Partez d’un document.<br><em>Faites le suivant à votre façon.</em>',
 'footer':'Un outil FadeShed. Lire, présenter et partager.', 'license':'Licences et notices','source':'Code du projet',
}}


def home(lang):
 t=TEXT[lang];n=t['nav'];h=[]
 h.append(f'''<div class="lwp-web-home proposal-home"><a class="pv-skip" href="#main">{t['skip']}</a>
 <nav class="lwp-web-nav pv-top" aria-label="{'Navigation du site' if lang=='fr' else 'Site navigation'}"><a class="lwp-web-brand" href="index.html">LightWebPres</a><div class="pv-nav-links"><a href="#usages">{n[0]}</a><a href="#identities">{n[1]}</a><a href="#create">{n[2]}</a><a href="#documentation">{n[3]}</a></div></nav>
 <main class="pv-main" id="main">
 <section class="pv-hero" aria-labelledby="hero-title"><div class="pv-hero-copy"><p class="pv-eyebrow"><span></span>LIGHTWEBPRES / {'BÊTA' if lang=='fr' else 'BETA'}</p><h1 id="hero-title">{t['title']}</h1><p class="pv-lead">{t['lead']}</p><div class="pv-actions"><a class="pv-button" href="demo/library.html">{t['cta']} <span aria-hidden="true">↗</span></a><a class="pv-text-link" href="#usages">{t['cta2']} <span aria-hidden="true">↓</span></a></div><p class="pv-reassure">{t['reassure']}</p></div>
 <figure class="pv-hero-visual" aria-label="{t['heroalt']}"><div class="pv-landscape"><div class="pv-window-bar"><span class="pv-window-dots" aria-hidden="true">○ ○ ○</span><span>{t['landscape']}</span><span aria-hidden="true">↗</span></div><a href="concepts/nebula/first-page.html#travels-with-the-page"><img fetchpriority="high" src="img/concepts/nebula-landscape.webp" width="1100" height="660" alt="{t['landscape']}"/></a></div><div class="pv-portrait"><a href="concepts/nebula/first-page.html#travels-with-the-page"><img src="img/concepts/nebula-portrait.webp" width="390" height="844" alt="{t['portrait']}"/></a><span>{t['portrait']}</span></div><figcaption><span class="pv-mini-line"></span>{'Un article. Deux contextes de lecture.' if lang=='fr' else 'One article. Two reading contexts.'}</figcaption></figure></section>
 <div class="pv-value-line">{''.join('<span><b aria-hidden="true">↗</b>'+x+'</span>' for x in t['strip'])}</div>
 <section class="pv-story pv-section"><div class="pv-section-intro"><div><p class="pv-eyebrow">{t['journeylabel']}</p><h2>{t['journeytitle']}</h2></div><p>{t['journeytext']}</p></div><div class="pv-phases">''')
 for i,(tag,title,desc) in enumerate(t['phases']):
  h.append(f'<div><span class="pv-phase-n">0{i+1} / {tag}</span><h3>{title}</h3><p>{desc}</p></div>')
 h.append(f'''</div></section><section id="usages" class="pv-section pv-roles"><div class="pv-section-intro"><div><p class="pv-eyebrow">{t['roleslabel']}</p><h2>{t['rolestitle']}</h2></div><p>{t['rolesintro']}</p></div><div class="pv-role-grid">''')
 for i,(slug,title,audience,desc,label) in enumerate(t['roles']):
  h.append(f'''<a href="usages.html#{slug}" class="pv-role"><span class="pv-role-no">0{i+1}<span aria-hidden="true">↗</span></span><h3>{title}</h3><p class="pv-audience">{audience}</p><p>{desc}</p><span class="pv-role-link">{label} <span aria-hidden="true">→</span></span></a>''')
 h.append(f'''</div></section><section class="pv-section pv-identity" id="identities"><div class="pv-section-intro"><div><p class="pv-eyebrow">{t['identitylabel']}</p><h2>{t['identitytitle']}</h2></div><p>{t['identityintro']}</p></div><div class="pv-comparison"><div class="pv-identity-controls" role="group" aria-label="{'Choisir une présentation à comparer' if lang=='fr' else 'Choose a presentation to compare'}">''')
 for key,label,_,_,_ in t['identities']:
  h.append(f'<button type="button" class="pv-choice" data-choice="{key}" aria-pressed="{str(key=="native").lower()}" aria-controls="pv-panel-{key}">{label}</button>')
 h.append('</div>')
 for i,(key,label,title,desc,alt) in enumerate(t['identities']):
  h.append(f'''<div class="pv-identity-panel" data-panel="{key}" id="pv-panel-{key}"><figure><a href="concepts/{key}/first-page.html#travels-with-the-page"><img src="img/concepts/{key}.webp" width="1280" height="720" alt="{alt}" loading="lazy"/></a></figure><div class="pv-identity-copy"><span class="pv-eyebrow">0{i+1} / {label}</span><h3>{title}</h3><p>{desc}</p><a class="pv-text-link" href="concepts/{key}/first-page.html#travels-with-the-page">{t['openidentity']} ↗</a></div></div>''')
 h.append(f'</div><p class="pv-caption">{t["identityhint"]}</p><div class="pv-concepts">')
 for term,desc in t['concepts']:h.append(f'<div><h3>{term}</h3><p>{desc}</p></div>')
 h.append(f'''</div><a class="pv-text-link" href="apparence.html#composer">{t['moreappearance']} →</a></section>
 <section class="pv-section pv-author" id="create"><div class="pv-section-intro"><div><p class="pv-eyebrow">{t['authorlabel']}</p><h2>{t['authortitle']}</h2></div><p>{t['authorintro']}</p></div><div class="pv-authors">''')
 for i,(title,desc) in enumerate(t['actors']):
  h.append(f'<div class="pv-author-card"><span class="pv-author-icon" aria-hidden="true">{["Aa","Aa + ◈","◈"][i]}</span><h3>{title}</h3><p>{desc}</p></div>')
  if i<2:h.append(f'<span class="pv-or">{t["or"]}</span>')
 h.append(f'''</div><div class="pv-converge"><span aria-hidden="true">↓</span> {t['converge']} <span aria-hidden="true">↓</span></div><div class="pv-source-bar"><div><span class="pv-eyebrow">{'LES MÊMES FICHIERS' if lang=='fr' else 'THE SAME FILES'}</span><h3>{t['project']}</h3></div><div class="pv-source-parts">{''.join('<span>'+x+'</span>' for x in t['sourceparts'])}</div></div><div class="pv-build"><div><span class="pv-eyebrow">LIGHTWEBPRES</span><h3>{t['engine']}</h3></div><a href="demarrer.html#navigateur"><b>{t['browser']} ↗</b><span>{t['browserdesc']}</span></a><a href="demarrer.html#terminal"><b>{t['cli']} ↗</b><span>{t['clidesc']}</span></a></div><p class="pv-caption">{t['boundary']}</p><a class="pv-text-link" href="demarrer.html#agent">{t['fullworkflow']} →</a></section>
 <section class="pv-section pv-keep"><div class="pv-section-intro"><div><p class="pv-eyebrow">{t['keeplabel']}</p><h2>{t['keeptitle']}</h2></div></div><div class="pv-delivery"><article><span class="pv-eyebrow">{'PROJET SOURCE' if lang=='fr' else 'SOURCE PROJECT'}</span><h3>{t['sourcetitle']}</h3><div class="pv-file-list" aria-hidden="true"><span>article.md</span><span>images/</span><span>series.json</span><span>{'identité/' if lang=='fr' else 'identity/'}</span></div><p>{t['sourcetext']}</p><a class="pv-text-link" href="downloads/library-project.zip">{t['sourcecta']} ↓</a></article><article><span class="pv-eyebrow">{'DOCUMENT À DIFFUSER' if lang=='fr' else 'PUBLISHED DOCUMENT'}</span><h3>{t['resulttitle']}</h3><div class="pv-file-list" aria-hidden="true"><span>index.html</span><span>article.html</span><span>img/</span><span>assets/</span></div><p>{t['resulttext']}</p><a class="pv-text-link" href="demo/library.html">{t['resultcta']} ↗</a></article></div><p class="pv-caption">{t['keepnote']}</p></section>
 <section class="pv-section pv-documentation" id="documentation"><div class="pv-section-intro"><div><p class="pv-eyebrow">{t['docslabel']}</p><h2>{t['docstitle']}</h2></div><p>{t['docsintro']}</p></div><div class="pv-doc-cards">{{{{content}}}}</div><div class="pv-resources">''')
 for url,title,desc in t['resources']:h.append(f'<a href="{url}"><h3>{title}<span aria-hidden="true">↗</span></h3><p>{desc}</p></a>')
 h.append(f'''</div></section><section class="pv-finish"><h2>{t['endtitle']}</h2><a class="pv-button" href="demo/library.html">{t['cta']} ↗</a></section></main><footer class="pv-footer"><div><strong>LightWebPres</strong><p>{t['footer']}</p></div><div><a href="https://github.com/Fade78/lightwebpres">{t['source']}</a><a href="llms.txt">llms.txt</a><a href="reference/COPYING">{t['license']}</a></div></footer></div>''')
 return ''.join(h).replace('<section ', '<div ').replace('</section>', '</div>')
