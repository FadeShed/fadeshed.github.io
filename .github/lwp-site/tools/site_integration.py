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



def clean_html(s,locale):
    for x in list(s.select('.version-tag,.build-stamp,.brand-version')):x.decompose()
    for stamp in s.select('.help-stamp'):
        for text in list(stamp.find_all(string=True,recursive=False)):
            if re.search(r'\bv?\d+\.\d+\.\d+',str(text)):text.extract()
    # Editorial source numbers are not rewritten inside code, licenses or kit identifiers.
    for text in list(s.find_all(string=True)):
        if text.find_parent(['script','style','pre','code']):continue
        val=str(text)
        if re.search(r'(?:LightWebPres|Moteur|Engine)\s*v?0\.\d+\.\d+',val):
            text.replace_with(re.sub(r'(LightWebPres|Moteur|Engine)\s*v?0\.\d+\.\d+',r'\1',val))
    for a in s.select('a[href="build-info.json"]'):
        a['href']='https://github.com/Fade78/lightwebpres';a.string='Projet LightWebPres' if locale=='fr' else 'LightWebPres project'
    return s
