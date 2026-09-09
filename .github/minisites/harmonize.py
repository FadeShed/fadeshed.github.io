#!/usr/bin/env python3
"""Build the three public minisites from pinned, reviewed inputs.

Keeps the complete LightWebPres portal; adapts the Pasteberth site without
modifying its runtime JS/CSS. Writes only the explicit public output directory.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from bs4 import BeautifulSoup

PB_REV = '36f2da3c5b57fc35e237225b8d9bd4c3c7eeb50b'
ROOT_URL = 'https://fadeshed.github.io/'
TOP = ['index.html', 'index.md', 'style.css', 'llms.txt', '.nojekyll', 'assets', 'fileshed', 'pasteberth', 'lightwebpres']

CSS = '''/* Shared navigation, not a shared product theme. */
body.fs-fileshed .hero>*,body.fs-fileshed .section-head>*,body.fs-fileshed .workflow-grid>*,body.fs-fileshed .engineering>*,body.fs-fileshed .legacy-grid>*{min-width:0}
body.fs-fileshed pre{max-width:100%}
@media(max-width:440px){body.fs-fileshed .hero h1{font-size:clamp(3.6rem,18vw,4.8rem)}body.fs-fileshed .deliverable>div{min-width:0}body.fs-fileshed .deliverable strong{overflow-wrap:anywhere}}

.fs-breadcrumb{display:flex;align-items:center;gap:12px;min-width:0;flex-wrap:wrap;font:500 14px/1.4 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--fs-ink,#142b40)}
.fs-breadcrumb a{color:inherit;text-decoration:none;display:inline-flex;align-items:center;min-height:44px;gap:10px;font:inherit;letter-spacing:normal}
.fs-breadcrumb .fs-home{font-weight:780;white-space:nowrap}
.fs-home img{display:block;width:32px;height:30px;object-fit:contain;border:0;border-radius:0;box-shadow:none;filter:none;transform:none;clip-path:none}
.fs-home strong{color:var(--fs-accent,#be4709);font-weight:inherit}
.fs-breadcrumb .fs-separator{opacity:.5;font-weight:400}
.fs-breadcrumb .fs-product{white-space:nowrap;font-weight:550}
.fs-breadcrumb a:hover{text-decoration:underline;text-underline-offset:4px}
.fs-breadcrumb a:focus-visible,.fs-utility a:focus-visible{outline:3px solid var(--fs-focus,#3182d5);outline-offset:4px;border-radius:3px}
.fs-status{display:inline-flex;align-items:center;padding:4px 7px;border:1px solid #608674;border-radius:4px;font:700 10px/1.35 ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--fs-status-ink,#235c42);background:var(--fs-status-bg,#edf8f0)}
.fs-on-dark{--fs-ink:#edf1f4;--fs-accent:#f0bc67;--fs-focus:#badafa;--fs-status-ink:#b7eed1;--fs-status-bg:#173629}
.fs-utility{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;box-sizing:border-box;padding:10px 24px;border-bottom:1px solid #8896a333;background:var(--fs-surface,#f6f5f0);font:13px/1.4 system-ui,sans-serif}
.fs-utility.fs-on-dark{--fs-surface:#111b25;color:#edf1f4}
.fs-utility>a{color:inherit;min-height:44px;display:inline-flex;align-items:center;gap:8px;text-decoration:none}
.fs-utility.fs-floating{position:fixed;inset:0 0 auto;z-index:25;background:var(--fs-surface,#111b25);padding-block:4px}
:fullscreen .fs-utility.fs-floating{display:none}
body.fs-pasteberth .header-inner{gap:18px}
body.fs-pasteberth .fs-breadcrumb{flex-shrink:0;gap:9px}
body.fs-pasteberth .header-actions{flex-shrink:0}
body.fs-pasteberth .desktop-nav{gap:20px}
body.fs-pasteberth .hero-proof .fs-status:before{display:none}
body.fs-pasteberth .documentation-links a{color:var(--ink,#142b40)}
body.fs-pasteberth .demo-status{flex-wrap:wrap;gap:6px}
body.fs-pasteberth .demo-status>span{min-width:0}
body.fs-pasteberth .demo-notes p{max-width:760px}
body.fs-fileshed .nav>.fs-breadcrumb{flex-shrink:0}
body.fs-fileshed .nav nav a{display:inline-flex}
.lwp-web-nav>.fs-breadcrumb{--fs-ink:#eef0ed;--fs-accent:#f0bc67;--fs-focus:#d8f986;gap:10px;flex-shrink:0}
.lwp-web-nav>.fs-breadcrumb .fs-status{--fs-status-ink:#d7fca7;--fs-status-bg:#273521}
.lwp-web-nav{flex-wrap:wrap;gap:12px}
@media(max-width:1100px){body.fs-pasteberth .header-cta{display:none}body.fs-pasteberth .desktop-nav{gap:14px}}
@media(max-width:850px){body.fs-pasteberth .desktop-nav{display:none}body.fs-pasteberth .menu-toggle{display:inline-flex}}
@media(max-width:620px){.fs-breadcrumb{gap:8px;font-size:13px}.fs-home img{width:29px;height:28px}.fs-breadcrumb a{gap:7px}body.fs-pasteberth .header-inner{flex-wrap:wrap;justify-content:space-between;padding-block:8px;gap:2px 10px}body.fs-pasteberth .header-actions{margin-left:auto}body.fs-pasteberth .header-inner .fs-status{display:none}.fs-utility{padding:8px 14px}.fs-utility.fs-floating>a{display:none}.lwp-web-nav>.fs-breadcrumb{gap:7px}.lwp-web-nav .fs-status{display:none}.lwp-web-nav-links{flex-wrap:wrap}.fs-breadcrumb .fs-product{font-size:13px}body.fs-fileshed .nav{column-gap:12px}body.fs-fileshed .nav nav{flex-wrap:wrap;gap:14px}}
@media print{.fs-utility,.fs-breadcrumb{display:none!important}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
'''

JS = '''/* Restore the workshop breadcrumb when a LightWebPres preset rerenders it. */
(() => {'use strict';
const script=document.currentScript,root=new URL('../',script.src),home=root.href;
function crumb(){
 const wrap=document.createElement('div');wrap.className='fs-breadcrumb';wrap.setAttribute('role','navigation');wrap.setAttribute('aria-label','Breadcrumb');
 const a=document.createElement('a');a.className='fs-home';a.href=home;a.setAttribute('aria-label','FadeShed home');
 const img=document.createElement('img');img.src=new URL('assets/fadeshed-mark.webp',root).href;img.alt='';img.width=32;img.height=30;
 const name=document.createElement('span');name.append('Fade');const strong=document.createElement('strong');strong.textContent='Shed';name.append(strong);a.append(img,name);wrap.append(a);
 const slash=document.createElement('span');slash.className='fs-separator';slash.setAttribute('aria-hidden','true');slash.textContent='/';wrap.append(slash);
 const current=document.createElement('a');current.className='fs-product';current.href=new URL('lightwebpres/',root).href;current.textContent='LightWebPres';wrap.append(current);
 const badge=document.createElement('span');badge.className='fs-status';badge.textContent='Beta';wrap.append(badge);return wrap;
}
function refresh(){document.querySelectorAll('.lwp-web-nav > .lwp-web-brand').forEach(a=>a.replaceWith(crumb()));}
refresh();let queued=false;
new MutationObserver(()=>{if(queued)return;queued=true;requestAnimationFrame(()=>{queued=false;refresh()})}).observe(document.body,{childList:true,subtree:true});
})();
'''


def copy_public(root, output):
    if output.exists():
        raise ValueError('Output must not exist')
    output.mkdir(parents=True)
    for name in TOP:
        p=root/name
        if p.is_dir(): shutil.copytree(p,output/name)
        elif p.is_file(): shutil.copy2(p,output/name)


def breadcrumb(product, home='../', product_href=None, status=None, dark=False):
    cls='fs-breadcrumb'+(' fs-on-dark' if dark else '')
    current=(f'<a class="fs-product" href="{product_href}">{product}</a>' if product_href else f'<span class="fs-product" aria-current="page">{product}</span>')
    badge=f'<span class="fs-status">{status}</span>' if status else ''
    return f'<div class="{cls}" role="navigation" aria-label="Breadcrumb"><a class="fs-home" href="{home}" aria-label="FadeShed home"><img src="{home}assets/fadeshed-mark.webp" width="32" height="30" alt=""><span>Fade<strong>Shed</strong></span></a><span class="fs-separator" aria-hidden="true">/</span>{current}{badge}</div>'


def both(fr,en):
    return f'<span class="fr" lang="fr">{fr}</span><span class="en" lang="en">{en}</span>'


def fragment(text):
    return BeautifulSoup(text,'html.parser')


def set_html(el,text):
    if el is None: raise ValueError('Expected element is missing')
    el.clear()
    for child in list(fragment(text).contents): el.append(child)


def head_link(soup, **attrs):
    soup.head.append(soup.new_tag('link',attrs=attrs))


def pasteberth(output, src):
    dest=output/'pasteberth'
    names=(src/'site/publish-files.txt').read_text().splitlines()
    for name in names:
        p=src/name
        if not p.is_file() or p.is_symlink() or p.resolve()!=src.resolve()/name: raise ValueError(name)
        if name.startswith('site/assets/') or name in ['site/index.html','site/demo.html','site/LICENSE-Pasteberth.txt']:
            target=dest/name.removeprefix('site/')
        elif not name.startswith('site/'):
            target=dest/'reference'/name
        else: continue
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(p,target)
    s=BeautifulSoup((dest/'index.html').read_text(),'html.parser')
    s.body['class']=list(s.body.get('class',[]))+['fs-pasteberth']
    s.select_one('.header-inner > .brand').replace_with(fragment(breadcrumb('Pasteberth',status='Beta')))
    head_link(s,rel='stylesheet',href='../assets/minisites.css?v=20260909')
    head_link(s,rel='canonical',href=ROOT_URL+'pasteberth/')
    head_link(s,rel='describedby',href='llms.txt',type='text/markdown')
    head_link(s,rel='alternate',href='index.md',type='text/markdown')
    proof=s.select_one('.hero-proof')
    proof.append(fragment('<span class="fs-status">Beta</span>'))
    for img in s.select('img[data-alt-en], img[data-alt-fr]'):
        if 'historical' in img.get('alt','').lower() or '2.1.18' in img.get('alt',''):
            img['alt']='A Pasteberth project zone with images, text and documents'
            img['data-alt-en']=img['alt']
            img['data-alt-fr']='Une zone de projet Pasteberth avec images, texte et documents'
    set_html(s.select_one('.hero-visual figcaption'),both('Une zone de projet. Plusieurs formats.','One project zone. Several file formats.'))
    set_html(s.select_one('#interface .eyebrow'),'03 / '+both('ESSAYEZ VOTRE ESPACE','TRY THE WORKSPACE'))
    set_html(s.select_one('#interface .section-heading > p'),both('Explorez les zones, sélectionnez des fichiers et récupérez un résultat. Aucun service à installer pour essayer.','Explore the zones, select files and pick up a result. No service to install just to try it.'))
    notes=s.select('.demo-notes > p')
    set_html(notes[1],both('L’interface est en anglais. La copie dépend des permissions de votre navigateur.','The workspace interface is in English. Copying depends on your browser permissions.'))
    version=s.select_one('.version-note')
    set_html(version,'<summary>'+both('À propos de ce bac à sable','About this sandbox')+'<svg class="icon" aria-hidden="true"><use href="#i-plus"></use></svg></summary><p>'+both('Des fichiers d’exemple sont prêts à utiliser. Vos ajouts restent en mémoire et disparaissent à la réinitialisation ou au rechargement. Les chemins sont fictifs.','Sample files are ready to use. Your additions stay in memory and disappear on reset or reload. Paths are fictional.')+'</p><p>'+both('Limites de la démo : 8 Mio par fichier et 32 Mio de fichiers au total. L’authentification et le stockage persistant nécessitent votre propre service Pasteberth.','Demo limits: 8 MiB per file and 32 MiB of files in total. Authentication and persistent storage require your own Pasteberth service.')+'</p>')
    set_html(s.select_one('#image-dialog .dialog-top > span'),both('Votre espace de travail','Your workspace'))
    note=s.select_one('.getting-started p.muted')
    set_html(note,both('Serveur officiellement pris en charge : Linux. Consultez le guide pour les conditions de déploiement et les systèmes de fichiers.','Officially supported server platform: Linux. See the guide for deployment and filesystem requirements.'))
    docs=s.select_one('#documentation')
    set_html(docs.select_one('p'),both('Choisissez le guide adapté à votre prochaine étape.','Choose the guide for your next step.'))
    routes=[
        ('Utiliser Pasteberth','Use Pasteberth','docs/using-pasteberth.md','Coller, sélectionner et récupérer','Paste, select and retrieve'),
        ('Vos projets','Your projects','docs/provisioning.md','Une convention, des zones découvertes','One convention, discovered zones'),
        ('Intégrer vos outils','Integrate your tools','docs/integrations.md','CLI, fichiers, HTTP et MCP','CLI, files, HTTP and MCP'),
        ('Déployer le service','Deploy the service','docs/deployment.md','Configuration, accès et stockage','Configuration, access and storage'),
        ('Toutes les recettes','All documentation','GUIDE.md','Les parcours et références techniques','Task guides and technical references'),
        ('Pour les agents','For agents',None,'Aperçu et documentation en Markdown','Overview and documentation in Markdown')]
    cards=''.join('<a href="'+('https://github.com/Fade78/pasteberth/blob/main/'+path if path else 'llms.txt')+'"><strong>'+both(fr,en)+'</strong><span>'+both(descfr,descen)+'</span></a>' for fr,en,path,descfr,descen in routes)
    set_html(docs.select_one('.documentation-links'),cards)
    for p in docs.find_all('p',recursive=False)[1:]: p.decompose()
    for a in s.find_all('a',href=True):
        href=a['href']
        if href.startswith('../docs/') or href in ['../GUIDE.md','../CHANGELOG.md']:
            a['href']='https://github.com/Fade78/pasteberth/blob/main/'+href[3:]
        elif href=='PROVENANCE.md': a.decompose()
    footer=s.select_one('.footer-top')
    footer.select_one('.brand').replace_with(fragment(breadcrumb('Pasteberth')))
    footer.select_one('nav').append(fragment('<a href="llms.txt">llms.txt</a>'))
    bottom=s.select_one('.footer-bottom')
    set_html(bottom,'<span>'+both('Des fichiers ordinaires. Des passages plus simples.','Ordinary files. Easier handoffs.')+'</span><span>Pasteberth · Beta · <a href="LICENSE-Pasteberth.txt">AGPL-3.0-or-later</a></span>')
    html=str(s)
    assert not re.search(r'2\.1\.(?:18|19|21)|historical|provenance|not a mockup',html,re.I)
    (dest/'index.html').write_text(html+'\n')
    demo=(dest/'demo.html').read_text()
    demo,n=re.subn(r'<span class="brand-version">[^<]*</span>','',demo)
    assert n==1
    # A remembered Overview group has no tab-zone links. Wait for group tabs,
    # choose Projects, then announce readiness. This also makes Reset reliable.
    old="const timer=setInterval(()=>{if(document.querySelector('.tab-zone-link')){clearInterval(timer);focus();parent.postMessage({type:'pb-demo-ready'},'*');}},60);"
    new="const timer=setInterval(()=>{if(!document.querySelector('.group-tab'))return;focus();if(!document.querySelector('.tab-zone-link'))return;clearInterval(timer);parent.postMessage({type:'pb-demo-ready'},'*');},60);"
    if demo.count(old)!=1: raise ValueError('Expected embedded adapter startup')
    demo=demo.replace(old,new,1)
    adapter=dest/'assets/demo-adapter.js'
    adapter_text=adapter.read_text()
    if adapter_text.count(old)!=1: raise ValueError('Expected standalone adapter startup')
    adapter.write_text(adapter_text.replace(old,new,1))
    (dest/'demo.html').write_text(demo)
    (dest/'assets/site.js').write_text((dest/'assets/site.js').read_text().replace('website v2.1','website'))
    # All embedded runtime functionality is retained; only its visible badge is omitted.
    (dest/'llms.txt').write_text('''# Pasteberth

> Pasteberth stages, exchanges and retrieves files and clipboard content across working contexts, using ordinary filesystem directories.

Status: **Beta**. Use it alone, between people, between agents, or with scripts and other tools. Web, filesystem, CLI, HTTP API and MCP are access choices, not assigned participant roles. PDFs, workbooks, archives and other allowed files are useful without document-format interpretation; previews and clipboard copying depend on content and browser capabilities.

A managed item is a data file plus a coherent JSON sidecar. Publication is explicit. `register FILE` validates a completed local file and creates or refreshes its sidecar, without rewriting data or contacting the daemon. `drop` always contacts the daemon, even when direct local staging avoids an HTTP payload transfer. MCP exposes only `drop` to a known zone; use HTTP or filesystem interfaces for other operations.

Collections discover eligible existing leaf directories by configured conventions. Project templates can create them without per-project Pasteberth configuration changes. Service reads trigger discovery, with background scans for Web overviews and visible-browser polling; there is no instantaneous filesystem watcher. Discovery does not register the files inside a zone. Groups are views, not ACLs. Comments and transfers allow optional workflows without assignments or approvals. Retention can remove older items: this is a working area, not backup or permanent storage.

## Discover and use

- [Overview](https://fadeshed.github.io/pasteberth/index.md): purposes, publication, retrieval and boundaries.
- [Interactive sandbox](https://fadeshed.github.io/pasteberth/#interface): sample files, selection, transfers and downloads; browser-memory simulation, not the deployed service.
- [Documentation map](https://fadeshed.github.io/pasteberth/reference/GUIDE.md): choose a task and its reference.
- [Concepts](https://fadeshed.github.io/pasteberth/reference/docs/concepts.md): artifacts, zones, groups and optional workflows.
- [Using Pasteberth](https://fadeshed.github.io/pasteberth/reference/docs/using-pasteberth.md): paste, select, inspect, copy and download.
- [Project provisioning](https://fadeshed.github.io/pasteberth/reference/docs/provisioning.md): configure collections once and provision eligible exchange directories.

## Integrate and deploy

- [Integrations](https://fadeshed.github.io/pasteberth/reference/docs/integrations.md): interfaces, locality and daemon dependencies.
- [Safe local registration](https://fadeshed.github.io/pasteberth/reference/docs/recipes/register-file.md): avoid data and sidecar collisions; registration is not managed replacement.
- [CLI](https://fadeshed.github.io/pasteberth/reference/docs/reference/cli.md): exact commands and exit codes.
- [HTTP API](https://fadeshed.github.io/pasteberth/reference/docs/reference/api.md): browsing, retrieval and managed operations.
- [MCP](https://fadeshed.github.io/pasteberth/reference/docs/reference/mcp.md): publication tool and partial-success behavior.
- [Deployment](https://fadeshed.github.io/pasteberth/reference/docs/deployment.md): Linux support, configuration, permissions, authentication and HTTPS.

## Optional

- [Current-result recipe](https://fadeshed.github.io/pasteberth/reference/docs/recipes/current-result.md): explicit replacement of managed items.
- [Free-form zone workflow](https://fadeshed.github.io/pasteberth/reference/docs/recipes/zone-workflow.md): use comments and transfers without imposed process.
- [Upstream source and releases](https://github.com/Fade78/pasteberth): match technical documentation to your installed revision.
- [FadeShed](https://fadeshed.github.io/llms.txt): related tools.
''')
    (dest/'index.md').write_text('''# Pasteberth

> Your files. Ready for what is next.

**Beta.** Pasteberth is a self-hosted place to stage and retrieve working files across browsers, clipboards, terminals and filesystems. A person, an agent or a script can use whichever interface fits. It is useful alone as well as between participants.

## Put it down once; pick it up your way

Paste a screenshot or text, drop a PDF or workbook, or publish a script's output. Retrieve supported content through the clipboard, copy a server-side filesystem reference, download the file, or collect a selection as a ZIP when enabled. A copied reference is not a public URL: its consumer needs filesystem access to that path. Pasteberth stores arbitrary allowed files, but does not edit their document formats.

## Try the workspace

The [interactive demo](https://fadeshed.github.io/pasteberth/#interface) includes sample files, project views, selection, comments, transfers and downloads. Additions remain in the browser tab's memory and disappear on reset or reload. The sandbox is not an authenticated or persistent Pasteberth installation.

## Ordinary files, explicit publication

A managed item consists of a data file and its JSON sidecar. `register FILE` creates or refreshes the sidecar of a completed local regular file without rewriting data or contacting the daemon. It does not apply the running daemon's retention or per-zone free-space policy. Use a fresh name and the [safe registration recipe](reference/docs/recipes/register-file.md) rather than overwriting an existing managed pair.

`drop` asks the daemon to publish; even direct local staging still contacts it. HTTP supports the documented browsing and managed operations. MCP currently exposes only `drop` to a known zone. None of these interfaces assigns a human or agent to a particular side.

## Project conventions

A collection can discover existing exchange directories such as `/repo/<project>/ignoredbygit/exchange`. Configure the rule and a group once; project templates provide eligible directories and permissions. A later overview refresh exposes new matching zones. This is request-triggered scanning, not an instantaneous watcher. Discovery creates neither projects nor managed files. Groups can provide focused views without duplicating data.

## Context, not an imposed process

Zones can be organized by project, subject or stage. Comments can carry context; copies and moves can support review. There is no enforced order, assignment or approval system. Retention can delete older items, and multi-file operations may partially succeed. Important deliverables belong in durable storage outside the working area.

## Documentation

- [Task map](reference/GUIDE.md)
- [Using Pasteberth](reference/docs/using-pasteberth.md)
- [Integrations](reference/docs/integrations.md)
- [Project provisioning](reference/docs/provisioning.md)
- [Deployment and trust boundaries](reference/docs/deployment.md)
- [Agent index](llms.txt)

The service uses shared authentication, not individual accounts or per-zone ACLs. The documentation snapshot describes the pinned source used for this site; follow the release matching your installation. Pasteberth is AGPL-3.0-or-later.
''')


def fileshed(output):
    dest=output/'fileshed/index.html'
    s=BeautifulSoup(dest.read_text(),'html.parser')
    s.body['class']=list(s.body.get('class',[]))+['fs-fileshed']
    s.select_one('header > .parent').replace_with(fragment(breadcrumb('FileShed')))
    head_link(s,rel='stylesheet',href='../assets/minisites.css?v=20260909')
    footnote=s.select_one('.source-notes > .footnote')
    if footnote: set_html(footnote,'Explore the project records for its implementation, examples and technical history. <a href="overview.md">Read the detailed overview.</a>')
    s.select_one('.records a:last-child b').string='Technical overview'
    s.select_one('.records a:last-child span').string='Capabilities and documentation →'
    dest.write_text(str(s)+'\n')


def lightwebpres(output):
    root=output/'lightwebpres'
    # Original article HTML, embedded runtime, source downloads and layouts remain.
    for path in root.rglob('*.html'):
        rel=path.relative_to(root)
        depth=len(rel.parts)-1
        home='../'*(depth+1)
        product='./' if depth==0 else '../'*depth
        text=path.read_text()
        if 'assets/minisites.css' in text: continue
        links=f'<link rel="stylesheet" href="{home}assets/minisites.css?v=20260909">'
        if depth==0:
            links+='<link rel="describedby" href="llms.txt" type="text/markdown">'
        links+=f'<script defer src="{home}assets/minisites.js?v=20260909"></script>'
        text=text.replace('</head>',links+'\n</head>',1)
        # Target rendered navigation only, not the embedded format/runtime data.
        match=re.search(r'(<nav\b[^>]*class="lwp-web-nav"[^>]*>)(.*?)(</nav>)',text,re.S)
        if match:
            inner=re.sub(r'<a\b[^>]*class="lwp-web-brand"[^>]*>.*?</a>',breadcrumb('LightWebPres',home,product_href='index.html' if path.name!='index.html' else None,status='Beta',dark=True),match[2],count=1,flags=re.S)
            text=text[:match.start()]+match[1]+inner+match[3]+text[match.end():]
        else:
            floating=depth>0 and rel.parts[0] in ['guide','demo']
            cls='fs-utility fs-on-dark'+(' fs-floating' if floating else '')
            bar=f'<header class="{cls}">'+breadcrumb('LightWebPres',home,product_href=product,status='Beta',dark=True)+f'<a href="{product}">← LightWebPres</a></header>'
            text=re.sub(r'(<body\b[^>]*>)',lambda m:m[1]+bar,text,count=1)
        path.write_text(text)
    # All reader-facing paths now exist locally, including the full source guides.
    p=root/'llms.txt'
    text=p.read_text()
    base='https://raw.githubusercontent.com/Fade78/lightwebpres/a43cb344f34f6a8d282f8d1dc9b54863103dc795/'
    text=text.replace(base,ROOT_URL+'lightwebpres/reference/')
    text=text.replace('## Start here','''## Try and explore

- [Full product portal](https://fadeshed.github.io/lightwebpres/): six paths through reading, authoring, appearance and publishing; the supplied portal is in French.
- [Interactive example](https://fadeshed.github.io/lightwebpres/demo/ma-page.html): one document to read in portrait or present in landscape.
- [Rendered guide](https://fadeshed.github.io/lightwebpres/guide/guide.html): full operational manual as a LightWebPres document.
- [Theme gallery](https://fadeshed.github.io/lightwebpres/themes.html): inspect built-in themes in rendered examples.
- [Browser builder](https://fadeshed.github.io/lightwebpres/web/): build a series in a tab with the bundled engine and local Pyodide assets; HTTP(S) required.

## Start here''')
    p.write_text(text)


def build(root, src, output):
    copy_public(root,output)
    (output/'assets/minisites.css').write_text(CSS)
    (output/'assets/minisites.js').write_text(JS)
    pasteberth(output,src)
    fileshed(output)
    lightwebpres(output)
    # Retain the root product index, but link to actual installed experiences.
    p=output/'llms.txt'
    text=p.read_text()
    text=text.replace('## Read the overviews','''## Explore the products

- [FileShed workbench](https://fadeshed.github.io/fileshed/): retired Open WebUI add-on, illustrated with data pipelines and deliverables.
- [Pasteberth demo](https://fadeshed.github.io/pasteberth/#interface): an interactive browser-memory workspace with sample files.
- [LightWebPres portal](https://fadeshed.github.io/lightwebpres/): complete supplied portal, articles, demonstration, guide, downloads and browser builder.

## Read the overviews''')
    p.write_text(text)
    (output/'assets/minisites-build.json').write_text(json.dumps({'pasteberth_source':PB_REV,'lightwebpres':'restored supplied portal; shared navigation overlay only','languages':{'home':'en','fileshed':'en','pasteberth':'en, fr by explicit choice','lightwebpres':'fr; supplied portal preserved'},'entrypoints':['/fileshed/','/pasteberth/','/lightwebpres/']},indent=2)+'\n')
    print('Built complete minisites and shared navigation:',output)


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=Path,required=True)
    ap.add_argument('--pasteberth-source',type=Path)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    if args.pasteberth_source: build(args.root,args.pasteberth_source,args.output)
    else:
        with tempfile.TemporaryDirectory() as tmp:
            src=Path(tmp)/'pasteberth'
            subprocess.run(['git','init','-q',str(src)],check=True)
            subprocess.run(['git','-C',str(src),'fetch','--depth=1','https://github.com/Fade78/pasteberth.git',PB_REV],check=True)
            subprocess.run(['git','-C',str(src),'checkout','--detach','-q','FETCH_HEAD'],check=True)
            build(args.root,src,args.output)
