#!/usr/bin/env python3
"""Build explicit English/French microsite editions from reviewed public inputs.

English retains the canonical URLs; /fr/ is the explicit French edition.
The existing LightWebPres engine is not changed. Main articles and examples are
rebuilt from translated Markdown; reference guide/gallery translations are
versioned publication catalogs. Backend programs and legal notices stay intact.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup, NavigableString, Comment

HERE=Path(__file__).resolve().parent
PUBLIC=['index.html','index.md','style.css','llms.txt','.nojekyll','assets','fileshed','pasteberth','lightwebpres']
BASE='https://fadeshed.github.io/'
ENGINE_SHA='5e702fed91c8694a794f0b0c8a0daa8a517d95904ed4269954c3aef835793191'


def read_json(path): return json.loads(path.read_text(encoding='utf-8'))
def dump(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def soup(text):return BeautifulSoup(text,'html.parser')
def put_html(e,text):
    e.clear()
    for x in list(soup(text).contents): e.append(x)
def serialize(s):return s.decode(formatter='minimal')
def text_translate(s, translations):
    normalized={' '.join(k.split()):v for k,v in translations.items()}
    for t in list(s.find_all(string=True)):
        if isinstance(t,Comment) or not t.parent or t.find_parent(['script','style','svg','pre','code']):continue
        v=str(t); key=v.strip()
        replacement=translations.get(key,normalized.get(' '.join(key.split())))
        if replacement is not None:
            t.replace_with(v[:len(v)-len(v.lstrip())]+replacement+v[len(v.rstrip()):])
    for e in s.find_all(True):
        for attr in ['title','aria-label','alt','placeholder','content']:
            value=e.get(attr)
            if isinstance(value,str):
                replacement=translations.get(value.strip(),normalized.get(' '.join(value.split())))
                if replacement is not None:e[attr]=replacement

def translate_blocks(s,translations):
    for e in list(s.select('p,h1,h2,h3,h4,th,td,li')):
        if not e.parent or e.find_parent(['pre','code','script','style']):continue
        key=e.decode_contents().strip()
        if key in translations:put_html(e,translations[key])

def language_pack(s,locale):
    node=s.select_one('#lwp-language-data')
    if node is None:return
    data=json.loads(node.string or node.get_text());data['default']=locale;data['auto']=False
    node.string=json.dumps(data,ensure_ascii=False).replace('</','<\\/')
    strings=data['packs'][locale]['strings']
    for e in s.find_all(True):
        for attr,key in list(e.attrs.items()):
            if attr=='data-lwp-i18n' and key in strings:put_html(e,strings[key])
            elif attr.startswith('data-lwp-i18n-') and key in strings:e[attr[len('data-lwp-i18n-'):]]=strings[key]

def relative_path(target,path):return os.path.relpath(target,Path(path).parent).replace(os.sep,'/')

def product_for(path):
    first=Path(path).parts[0]
    return {'fileshed':'FileShed','pasteberth':'Pasteberth','lightwebpres':'LightWebPres'}.get(first,'FadeShed')

def switch_html(path,locale):
    # Links remain usable with JavaScript and storage disabled.
    target_en='/'+path;target_fr='/fr/'+path
    if path.endswith('index.html'):
        target_en=target_en[:-10];target_fr=target_fr[:-10]
    return ('<nav class="fs-language" aria-label="'+('Langue' if locale=='fr' else 'Language')+'">'
            +f'<a data-fs-lang="en" lang="en" hreflang="en" href="{target_en}" aria-label="English"'+(' aria-current="true"' if locale=='en' else '')+'>EN</a>'
            +'<span aria-hidden="true">|</span>'
            +f'<a data-fs-lang="fr" lang="fr" hreflang="fr" href="{target_fr}" aria-label="Français"'+(' aria-current="true"' if locale=='fr' else '')+'>FR</a></nav>')

def crumb_html(path,locale,dark=False):
    home='/fr/' if locale=='fr' else '/';product=product_for(path)
    if product=='FadeShed':return ''
    phome=home+Path(path).parts[0]+'/'
    return '<div class="fs-breadcrumb'+(' fs-on-dark' if dark else '')+'" role="navigation" aria-label="'+('Fil d’Ariane' if locale=='fr' else 'Breadcrumb')+'">'+f'<a class="fs-home" href="{home}" aria-label="'+('Accueil FadeShed' if locale=='fr' else 'FadeShed home')+'"><img src="/assets/fadeshed-mark.webp" width="32" height="30" alt=""><span>Fade<strong>Shed</strong></span></a><span class="fs-separator" aria-hidden="true">/</span>'+f'<a class="fs-product" href="{phome}">{product}</a><span class="fs-status">'+(('Retraité' if locale=='fr' else 'Retired') if product=='FileShed' else ('Bêta' if locale=='fr' else 'Beta'))+'</span></div>'

# Runs before any product runtime; no persistence or browser-language guessing.
EARLY='''(() => {const u=new URL(location.href), q=u.searchParams.get('lang');window.__fsEntryHash=u.hash;
const fr=u.pathname==='/fr'||u.pathname.startsWith('/fr/');
if(q==='en'||q==='fr'){const p=u.pathname.replace(/^\\/fr(?=\\/|$)/,'')||'/';
const target=(q==='fr'?'/fr':'')+p;u.searchParams.delete('lang');
if(target!==u.pathname||location.search.includes('lang=')){u.pathname=target;location.replace(u.href);}}
})();'''


def decorate(s,path,locale):
    s.html['lang']=locale;s.html['data-fs-locale']=locale;s.html['data-fs-page']=path
    if path=='pasteberth/demo.html':s.body['class']=list(s.body.get('class',[]))+['fs-pbdemo']
    if not s.head or not s.body:raise ValueError('Incomplete HTML: '+path)
    # Remove obsolete auto/saved locale bootstrap, not the interactive renderer.
    for e in list(s.select('script')):
        text=e.string or ''
        if 'Only explicit choices are persisted' in text or 'pb-lang' in text or e.get('id')=='fs-language-route':e.decompose()
        elif 'minisites.js' in e.get('src','') or 'language.js' in e.get('src',''):e.decompose()
    for e in list(s.select('link[rel="canonical"], link[hreflang],.fs-language')):e.decompose()
    for e in list(s.select('link[rel="stylesheet"]')):
        if 'assets/minisites.css' in e.get('href',''):e.decompose()
    route=s.new_tag('script',id='fs-language-route');route.string=EARLY;s.head.insert(0,route)
    embedded=s.new_tag('script');embedded.string="if(window!==window.top)document.documentElement.setAttribute('data-fs-embedded','true');";s.head.insert(1,embedded)
    for e in s.select('svg,symbol'):
        if e.has_attr('viewbox'):e['viewBox']=e.attrs.pop('viewbox')
    s.head.append(s.new_tag('link',attrs={'rel':'stylesheet','href':'/assets/minisites.css?v=bilingual-1'}))
    url=BASE+('fr/' if locale=='fr' else '')+path
    if path.endswith('index.html'):url=url[:-10]
    s.head.append(s.new_tag('link',attrs={'rel':'canonical','href':url}))
    for lang in ['en','fr','x-default']:
        link=BASE+('fr/' if lang=='fr' else '')+path
        if path.endswith('index.html'):link=link[:-10]
        s.head.append(s.new_tag('link',attrs={'rel':'alternate','hreflang':lang,'href':link}))
    for e in list(s.select('.fs-breadcrumb')):e.replace_with(soup(crumb_html(path,locale,'fs-on-dark' in e.get('class',[]))))
    # Preserve existing product layouts and add the same switch to their header.
    p=product_for(path);selector=switch_html(path,locale)
    if p=='FadeShed':
        h=s.select_one('.site-header');h['class']=h.get('class',[])+['fs-home-header','fs-on-dark'];h.append(soup(selector))
    elif p=='Pasteberth' and path.endswith('/index.html'):
        controls=s.select_one('.header-actions')
        if controls:
            old=controls.select_one('.language')
            if old:old.replace_with(soup(selector))
            else:controls.insert(0,soup(selector))
    elif p=='FileShed':
        header=s.select_one('header.nav');header.select_one('.fs-breadcrumb').insert_after(soup(selector))
    else:
        h=s.select_one('.lwp-web-nav')
        if h:
            brand=h.select_one('.lwp-web-brand')
            if brand:brand.replace_with(soup(crumb_html(path,locale,True)))
            h.append(soup(selector))
        else:
            h=s.select_one('.fs-utility')
            if not h:
                h=s.new_tag('header',attrs={'class':'fs-utility fs-on-dark fs-floating'})
                put_html(h,crumb_html(path,locale,True));s.body.insert(0,h)
            h.append(soup(selector))
    # Preserve active language for explicit root-relative in-site links; assets stay shared.
    for a in s.select('a[href]'):
        if a.has_attr('data-fs-lang'):continue
        h=a['href']
        if h.startswith(BASE):h='/'+h[len(BASE):]
        if h.startswith('/') and not h.startswith('//') and not h.startswith('/assets/'):
            h=re.sub(r'^/fr(?=/|$)','',h) or '/'
            a['href']=('/fr' if locale=='fr' else '')+h
        # References are original source documents, not translated presentation pages.
        if locale=='fr' and ('github.com/Fade78/' in a.get('href','')) and ('.md' in a['href'] or '/COPYING' in a['href']):
            source_lang='fr' if 'specifications.md' in a['href'] else 'en'
            a['hreflang']=source_lang
            if source_lang=='en' and not a.select_one('.fs-reference-lang'):
                marker=s.new_tag('small',attrs={'class':'fs-reference-lang','aria-label':'ressource en anglais'});marker.string=' EN';a.append(marker)
    if locale=='fr':
        generic={'Breadcrumb':'Fil d’Ariane','FadeShed home':'Accueil FadeShed','Back to FadeShed':'Retour à FadeShed','← Back to FadeShed':'← Retour à FadeShed','For agents':'Pour les agents','Source ↗':'Code source ↗','Beta':'Bêta','Retired':'Retraité','Language':'Langue'}
        text_translate(s,generic)
    language_pack(s,locale)
    script=s.new_tag('script',src='/assets/minisites.js?v=bilingual-1',defer=True);s.body.append(script)
    return s


def run(engine,*args):
    env={k:v for k,v in os.environ.items() if not k.startswith('LWP_')};env['TERM']='dumb'
    result=subprocess.run([sys.executable,str(engine),*map(str,args)],capture_output=True,text=True,env=env,timeout=180)
    if result.returncode:raise RuntimeError(' '.join(map(str,args))+'\n'+result.stdout+result.stderr)
    return result.stdout


def zip_tree(path,root):
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(root.rglob('*')):
            if not p.is_file() or p.is_symlink() or any(v.startswith('.lwp-') or v=='__pycache__' for v in p.parts):continue
            i=zipfile.ZipInfo(p.relative_to(root).as_posix(),date_time=(1980,1,1,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o100644<<16;z.writestr(i,p.read_bytes())


def build_lwp(root,out,locale,temp):
    engine=root/'lightwebpres/web/lightwebpres'
    if hashlib.sha256(engine.read_bytes()).hexdigest()!=ENGINE_SHA:raise ValueError('Engine changed; review the translation build before continuing')
    series=temp/('series-'+locale);shutil.copytree(HERE/'lwp'/locale,series)
    img=series/'sources/img';img.mkdir(exist_ok=True)
    for name in ['product-responsive.png','themes-featured.png']:shutil.copyfile(root/'lightwebpres/img'/name,img/name)
    # Pin the original build identity without calling it the latest release.
    conf=read_json(series/'series.json');conf['series_meta']['version']=('Moteur 0.56.0 · version de travail' if locale=='fr' else 'Engine 0.56.0 · development build');dump(series/'series.json',conf)
    dest=out/'lightwebpres';run(engine,'build',series,'--lang',locale,'--output',dest)
    run(engine,'audit',series,'--lang',locale,'--strict');run(engine,'verify',series,'--lang',locale,'--output',dest)
    example=series/'example'
    for name in ['lightwebpres','COPYING','COPYING.EXCEPTION','THIRD-PARTY-NOTICES.md']:shutil.copyfile(root/'lightwebpres/web'/name,example/name)
    run(engine,'build',example,'--lang',locale,'--output',dest/'demo')
    run(engine,'audit',example,'--lang',locale,'--strict');run(engine,'verify',example,'--lang',locale,'--output',dest/'demo')
    for p in (dest/'demo').glob('*.html'):
        target=example/'public'/p.name;target.parent.mkdir(exist_ok=True);shutil.copyfile(p,target)
    (example/('LIRE-MOI.txt' if locale=='fr' else 'README.txt')).write_text(('Depuis ce dossier :\n' if locale=='fr' else 'From this directory:\n')+f'python3 lightwebpres build . --lang {locale}\n'+('Puis ouvrir public/index.html. Modifiez sources/ma-page.md ; gardez les slugs stables.\n' if locale=='fr' else 'Then open public/index.html. Edit sources/ma-page.md; keep its slugs stable.\n'))
    zip_tree(dest/'downloads/demarrage.zip',example)
    run(engine,'theme','gallery',dest/'themes.html','--lang',locale)
    info=read_json(dest/'build-info.json');info['language']=locale;info['edition']='static-bilingual';info['translation_sources']='.github/bilingual';info['checks']={'articles_build_audit_verify':True,'example_build_audit_verify':True};info.pop('inputs',None);dump(dest/'build-info.json',info)
    for p in dest.rglob('.lwp-*'):
        if p.is_file():p.unlink()
    print('Native article/demo build, audit, verify:',locale,flush=True)


def guide_translate(s):
    catalog=read_json(HERE/'translations/guide-fr.json');ui=read_json(HERE/'translations/guide-ui-fr.json')
    blocks={}
    if s.select('section.slide'):
        originals=[]
        for e in s.select('section.slide p,section.slide h1,section.slide h2,section.slide h3,section.slide h4,section.slide th,section.slide td,section.slide li'):
            if e.find_parent(['code','pre']) or e.find(['p','h1','h2','h3','h4','table','ul','ol']):continue
            if not e.get_text(strip=True):continue
            v=e.decode_contents()
            if v and v not in originals:originals.append(v)
        actual=hashlib.sha256(json.dumps(originals,ensure_ascii=False).encode()).hexdigest()
        if actual!=catalog['source_blocks_sha256']:raise ValueError('Guide content changed; refresh the translation catalog instead of misapplying indices')
        blocks={originals[int(i)]:v for i,v in catalog['translations'].items()}
    translate_blocks(s,blocks);text_translate(s,ui)
    plain={" ".join(soup(k).get_text(" ",strip=True).split()):soup(v).get_text(" ",strip=True) for k,v in {**blocks,**ui}.items()}
    def localize_preview(value):
        if isinstance(value,dict):return {k:localize_preview(v) for k,v in value.items()}
        if isinstance(value,list):return [localize_preview(v) for v in value]
        if isinstance(value,str):return plain.get(" ".join(value.split()),value)
        return value
    if s.body and s.body.has_attr('data-lwp-tag-preview'):
        s.body['data-lwp-tag-preview']=json.dumps(localize_preview(json.loads(s.body['data-lwp-tag-preview'])),ensure_ascii=False)

    for el in s.select('script[type="application/json"]'):
        if el.get('id')=='lwp-language-data':continue
        def walk(x):
            if isinstance(x,dict):return {k:walk(v) for k,v in x.items()}
            if isinstance(x,list):return [walk(v) for v in x]
            if isinstance(x,str):
                if x in ui:return ui[x]
                if '<' in x and ('<p' in x or '<section' in x or '<h' in x):
                    frag=soup(x);translate_blocks(frag,blocks);text_translate(frag,ui);return serialize(frag)
            return x
        el.string=json.dumps(walk(json.loads(el.string)),ensure_ascii=False).replace('</','<\\/')


def builder_translate(s,locale):
    if locale=='fr':
        text_translate(s,read_json(HERE/'translations/builder-fr.json'))
        for script in s.select('script:not([src])'):
            t=script.string or ''
            if 'function setStatus' not in t:continue
            # The wrapper UI is localized; the Python executable remains byte-identical.
            t=t.replace('statusEl.textContent = text;','statusEl.textContent = window.fsBuilderText(text);')
            t=re.sub(r"(\.textContent\s*=\s*)'([^'\n]*)'",lambda m:m[1]+"window.fsBuilderText("+json.dumps(m[2])+")",t)
            t=t.replace("prompt('Copy this command:', cmd)","prompt('Copiez cette commande :', cmd)")
            t=t.replace("outro.textContent = 'Then open ' + openUrl + ' in your browser.';","outro.textContent = 'Puis ouvrez ' + openUrl + ' dans votre navigateur.';")
            # Guard is prose assembled across lines, translate it as one source-level message.
            t=re.sub(r"intro\.textContent\s*=.*?;\n    statusEl.appendChild\(intro\);", "intro.textContent = 'Cette page nécessite un serveur HTTP(S), ainsi que les fichiers Pyodide et le programme LightWebPres voisins. Son ouverture en file:// ne peut pas fonctionner. Exécutez cette commande dans un terminal :';\n    statusEl.appendChild(intro);",t,flags=re.S)
            script.string=t
        helper=s.new_tag('script');helper.string=(HERE/'builder-ui-fr.js').read_text();s.head.append(helper)
    for select in s.select('#zipLangSelect,#gitLangSelect'):
        for option in select.select('option'):
            option.attrs.pop('selected',None)
            if option.get('value')==locale:option['selected']=''


def main(root,output):
    root=root.resolve();output=output.resolve()
    if output.exists():raise ValueError('Use a fresh output directory')
    output.mkdir(parents=True)
    for name in PUBLIC:
        src=root/name
        if src.is_symlink():raise ValueError('Symlink in public input')
        if src.is_dir():shutil.copytree(src,output/name)
        elif src.is_file():shutil.copyfile(src,output/name)
    fr=output/'fr';fr.mkdir()
    for name in PUBLIC:
        src=output/name
        if src.is_dir():shutil.copytree(src,fr/name)
        elif src.is_file():shutil.copyfile(src,fr/name)
    with tempfile.TemporaryDirectory(prefix='bilingual-') as d:
        tmp=Path(d)
        for locale,edition in [('en',output),('fr',fr)]:
            build_lwp(root,edition,locale,tmp)
            for path in ['index.html','fileshed/index.html']:
                s=soup((edition/path).read_text())
                if locale=='fr':text_translate(s,read_json(HERE/'translations'/('home-fr.json' if path=='index.html' else 'fileshed-fr.json')))
                (edition/path).write_text(serialize(decorate(s,path,locale)))
            path='pasteberth/index.html';s=soup((edition/path).read_text())
            if locale=='fr':
                s.title.string='Pasteberth — Vos fichiers, prêts pour la suite.'
                s.select_one('meta[name="description"]')['content']='Collez, déposez et retrouvez vos fichiers entre navigateurs, presse-papiers et répertoires. Pasteberth, un point de passage sur votre infrastructure.'
            if locale=='fr':
                text_translate(s,{'01 / PASTEBERTH WORKSPACE':'01 / ESPACE PASTEBERTH','NEW':'NOUVEAU'})
                n=s.select('.demo-notes > p')[1];put_html(n,'La démonstration utilise le français. La copie dépend des permissions du navigateur. Changer de langue recharge la démonstration et efface les ajouts.')
            else:
                n=s.select('.demo-notes > p')[1];put_html(n,'Copying depends on browser permissions. Changing language reloads the demo and clears additions.')
            (edition/path).write_text(serialize(decorate(s,path,locale)))
            dp=edition/'pasteberth/demo.html';ds=soup(dp.read_text())
            if locale=='fr':
                ds.title.string='Pasteberth — démonstration locale'
                # Group names remain original data; the adapter recognizes translated tab labels.
                for node in ds.select('script'):
                    text=node.string or ''
                    if 'function group(name)' in text:node.string=text.replace('b.textContent.startsWith(name)','(b.dataset.fsOriginalText||b.textContent).startsWith(name)')
                shortcut=ds.select_one('.help') or ds.select_one('footer')
                if shortcut:
                    put_html(shortcut,'Sélectionnez une zone ou utilisez les touches 1 à 9. Ctrl/Commande+V colle dans la zone active ; C copie la référence. Maj-clic sélectionne une plage ; Ctrl/Commande-clic ajoute des éléments. A ouvre les zones, U les ferme. Vous pouvez aussi déposer directement un fichier dans une zone.')
                node=ds.new_tag('script');node.string=(HERE/'pasteberth-demo-fr.js').read_text();ds.body.append(node)
            dp.write_text(serialize(decorate(ds,'pasteberth/demo.html',locale)))
            for p in sorted((edition/'lightwebpres').rglob('*.html')):
                if 'reference' in p.relative_to(edition).parts:continue
                rel=p.relative_to(edition).as_posix();s=soup(p.read_text())
                if rel.startswith('lightwebpres/guide/') and locale=='fr':guide_translate(s)
                if rel=='lightwebpres/themes.html' and locale=='fr':text_translate(s,read_json(HERE/'translations/gallery-fr.json'))
                if rel=='lightwebpres/web/index.html':builder_translate(s,locale)
                p.write_text(serialize(decorate(s,rel,locale)))
    # A single locale-aware integration layer, never a copy of application code.
    for edition in [output,fr]:
        (edition/'assets/minisites.css').write_text((root/'assets/minisites.css').read_text()+'\n'+(HERE/'language.css').read_text())
        (edition/'assets/minisites.js').write_text((HERE/'language.js').read_text())
    # Machine indexes remain plain Markdown; explicit routes are discoverable.
    for path in ['llms.txt','fileshed/llms.txt','pasteberth/llms.txt','lightwebpres/llms.txt']:
        for locale,edition in [('en',output),('fr',fr)]:
            p=edition/path;t=p.read_text();topic=path.rsplit('/',1)[0]+'/' if '/' in path else ''
            t+='\n## Website languages\n\n- [English presentation]('+BASE+topic+'): canonical English edition, also used when no language is specified.\n- [Présentation française]('+BASE+'fr/'+topic+'): édition française explicite ; la navigation conserve cette langue.\n'
            p.write_text(t)
    manifest={p.relative_to(output).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in output.rglob('*') if p.is_file()}
    dump(output/'assets/bilingual-manifest.json',{'schema':1,'default_language':'en','french_prefix':'/fr/','engine_sha256':ENGINE_SHA,'files':manifest})
    print('Bilingual public output:',output, 'files:',len(manifest),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();main(a.root,a.output)
