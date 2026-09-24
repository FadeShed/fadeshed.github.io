#!/usr/bin/env python3
"""Behavioural checks for the assembled bilingual site; no runtime source rewriting."""
from __future__ import annotations
import argparse
import functools
import hashlib
import http.server
import json
import os
from pathlib import Path
import re
import threading
import traceback
import urllib.parse
import zipfile
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, expect

HERE = Path(__file__).resolve().parent
CHAPTERS = ['decouvrir.html','usages.html','demarrer.html','ecrire.html','apparence.html','publier.html','ressources.html']
EXTRA = ['demo/library.html','demo/ma-page.html','demo/index.html','guide/guide.html','guide/index.html','themes.html','web/index.html']


def serve(root):
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*args): pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    return server,f'http://127.0.0.1:{server.server_port}/'


def run(root,report,base=None):
    root=root.resolve();report.mkdir(parents=True,exist_ok=True)
    server=None;page=None;checks=[]
    if base is None: server,base=serve(root)
    base=base.rstrip('/')+'/'
    engine=json.loads((HERE/'engine-lock.json').read_text())['sha256']
    def check(name,ok,detail=''):
        checks.append({'check':name,'passed':bool(ok),'detail':str(detail)[:1500]})
        (report/'report.json').write_text(json.dumps({'checks':len(checks),'passed':sum(x['passed'] for x in checks),'base_url':base,'results':checks},ensure_ascii=False,indent=2)+'\n')
        print(('PASS ' if ok else 'FAIL ')+name,flush=True)
        if not ok: raise AssertionError(name+': '+str(detail))
    try:
        errors=[];refs=0;ids={}
        for prefix in ['', 'fr/']:
            dest=root/(prefix+'lightwebpres')
            check('Renderer identity '+prefix,hashlib.sha256((dest/'web/lightwebpres').read_bytes()).hexdigest()==engine)
            for name in ['lightwebpres-cli.zip','demarrage.zip','library-project.zip','site-sources.zip','identity-examples.zip','skills.zip']:
                with zipfile.ZipFile(dest/'downloads'/name) as z:
                    check('Archive intact '+prefix+name,z.testzip() is None)
                    if name in ['lightwebpres-cli.zip','library-project.zip','site-sources.zip']:
                        check('Archive renderer '+prefix+name,hashlib.sha256(z.read('lightwebpres')).hexdigest()==engine)
            for path in dest.rglob('*.html'):
                relative=path.relative_to(dest)
                if relative.parts[0]=='reference':continue
                s=BeautifulSoup(path.read_text(),'html.parser')
                check('No private repository link '+prefix+str(relative),'fadeshed-internal-docs' not in path.read_text())
                # Combined HTML retains authored destinations in its templates.
                # The native reader maps them to views embedded in this document.
                bundle=s.select_one('#lwp-series-data');embedded={}
                if bundle:
                    data=json.loads(bundle.string)
                    check('Embedded series contract '+prefix+str(relative),data.get('version')==1 and bool(s.select_one('#lwp-series-view')))
                    embedded={v['key']:BeautifulSoup(v['content'],'html.parser') for v in data['views']}
                documents=[s]+list(embedded.values())
                for doc in documents:
                    for node in doc.find_all(['a','img','script','link','iframe']):
                        ref=node.get('href') if node.name in ['a','link'] else node.get('src')
                        if not ref or ref.startswith(('data:','blob:','http:','https:','mailto:','javascript:','tel:')):continue
                        u=urllib.parse.urlsplit(ref);p=urllib.parse.unquote(u.path);refs+=1
                        if embedded and node.name=='a' and not node.has_attr('download') and not u.query and p and not p.startswith('/'):
                            key=p[2:] if p.startswith('./') else p
                            if key=='index.html':key=data.get('home','')
                            if key in embedded:
                                if u.fragment and not embedded[key].find(id=urllib.parse.unquote(u.fragment)):errors.append((str(path.relative_to(root)),ref))
                                continue
                        if embedded and not p and u.fragment and doc is not s:
                            if not doc.find(id=urllib.parse.unquote(u.fragment)):errors.append((str(path.relative_to(root)),ref))
                            continue
                        target=(root/p.lstrip('/') if p.startswith('/') else path.parent/p) if p else path
                        if target.is_dir():target=target/'index.html'
                        target=target.resolve()
                        if not target.is_relative_to(root) or not target.is_file():errors.append((str(path.relative_to(root)),ref));continue
                        if u.fragment and target.suffix=='.html':
                            if target not in ids:ids[target]={x.get('id') for x in BeautifulSoup(target.read_text(),'html.parser').find_all(id=True)}
                            if urllib.parse.unquote(u.fragment) not in ids[target]:errors.append((str(path.relative_to(root)),ref))
                for node in s.select('script,style,pre,code'):node.decompose()
                check('Versionless public presentation '+prefix+str(relative),not re.search(r'LightWebPres\s+v?\d+\.\d+\.\d+',s.get_text(' ',strip=True)))
        check('Local pages, assets and anchors',not errors,{'references':refs,'errors':errors[:20]})
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM'))
            for lang,prefix in [('en',''),('fr','fr/')]:
                for route in ['', 'fileshed/', 'pasteberth/', 'lightwebpres/']:
                    for width in [320,390,768,1440]:
                        ctx=browser.new_context(viewport={'width':width,'height':900 if width>700 else 844},locale='fr-FR')
                        page=ctx.new_page();runtime=[];page.on('pageerror',lambda e:runtime.append(str(e)))
                        response=page.goto(base+prefix+route,wait_until='networkidle',timeout=60000)
                        check(f'HTTP and locale {lang} {route} {width}',response.status==200 and page.locator('html').get_attribute('lang')==lang)
                        expect(page.locator('.fs-language').first).to_be_visible()
                        check(f'No overflow {lang} {route} {width}',page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
                        check(f'Images decoded {lang} {route} {width}',page.locator('img').evaluate_all('ns=>ns.filter(e=>e.getBoundingClientRect().width>0&&e.loading!=="lazy").every(e=>e.complete&&e.naturalWidth>0)'))
                        if route=='lightwebpres/':
                            check(f'All role destinations {lang} {width}',all(page.locator('a[href="usages.html#'+role+'"]').count()>0 for role in ['read','write','organize','design','automate','publish']))
                            check(f'Content before terminal {lang} {width}',page.locator('.pv-hero').count()==1 and page.locator('.pv-hero pre').count()==0)
                            check(f'Identity choices {lang} {width}',page.locator('[data-choice]').count()==3)
                            for choice in ['native','docs','field-notes']:
                                button=page.locator('[data-choice="'+choice+'"]');button.click()
                                panel=page.locator('[data-panel="'+choice+'"]');expect(panel).to_be_visible()
                                panel.locator('img').first.scroll_into_view_if_needed()
                                check(f'Comparison {lang} {width} {choice}',button.get_attribute('aria-pressed')=='true' and panel.locator('img').evaluate_all('async ns=>{await Promise.all(ns.map(e=>e.decode()));return ns.every(e=>e.naturalWidth>0)}'))
                            page.locator('[data-choice=native]').focus();page.keyboard.press('ArrowRight')
                            check(f'Comparator keyboard {lang} {width}',page.locator('[data-choice=docs]').get_attribute('aria-pressed')=='true')
                            page.locator('[data-choice=native]').click()
                        if width in [390,1440]:
                            page.evaluate('scrollTo(0,0)');page.screenshot(path=str(report/f'{lang}-{route.strip("/") or "home"}-{width}.png'),full_page=route=='lightwebpres/')
                        check(f'No runtime errors {lang} {route} {width}',not runtime,runtime);ctx.close()
                ctx=browser.new_context(viewport={'width':1440,'height':960},locale='fr-FR',accept_downloads=True)
                page=ctx.new_page();runtime=[];page.on('pageerror',lambda e:runtime.append(str(e)))
                comparisons=['concepts/'+i+'/first-page.html' for i in ['native','docs','field-notes','nebula']]
                for rel in CHAPTERS+EXTRA+comparisons:
                    response=page.goto(base+prefix+'lightwebpres/'+rel,wait_until='networkidle',timeout=90000)
                    check(f'Complete localized portal {lang} {rel}',response.status==200 and page.locator('html').get_attribute('lang')==lang)
                    expect(page.locator('.fs-language').first).to_be_visible()
                    if page.locator('section.slide').count():
                        check(f'Native-only reader {lang} {rel}',page.locator('#navMenu').count()==1 and page.locator('.fs-reader-open').count()==0)
                        page.locator('#navMenu').click();expect(page.locator('#presenterMenu')).to_be_visible()
                        page.locator('#presenterMenu').click(position={'x':4,'y':4});expect(page.locator('#presenterMenu')).not_to_be_visible()
                page.goto(base+prefix+'pasteberth/',wait_until='networkidle');page.locator('#launch-demo').click()
                frame=page.frame_locator('#demo-frame');expect(frame.locator('.zone').first).to_be_visible(timeout=15000)
                check('Embedded navigation hidden '+lang,not frame.locator('.fs-utility').is_visible())
                page.locator('[data-scene=selection]').click();expect(frame.locator('.selection-summary-name')).to_have_count(2)
                with page.expect_download() as event:frame.locator('.zone').first.get_by_role('button',name=re.compile('ZIP')).first.click()
                with zipfile.ZipFile(event.value.path()) as z:check('Pasteberth selection ZIP '+lang,z.testzip() is None and len(z.namelist())==2)
                page.locator('[data-scene=focus]').click();frame.locator('.zone-upload-btn').first.click()
                frame.locator('#file-picker').set_input_files({'name':'site-check.txt','mimeType':'text/plain','buffer':b'Synthetic publication check\n'})
                expect(frame.locator('.zone').first.locator('.fname')).to_have_text('site-check.txt')
                frame.locator('.comment-btn').first.click();frame.locator('textarea').first.fill('Note');frame.locator('.comment-save-btn').first.click()
                expect(frame.locator('.comment-text').first).to_have_text('Note')
                page.locator('[data-scene=overview]').click();page.locator('#reset-demo').click();expect(frame.locator('.tab-zone-link').first).to_be_visible()
                check('Pasteberth reset '+lang,frame.locator('.thumb-wrap[data-item-id="site-check.txt"]').count()==0)
                page.goto(base+prefix+'lightwebpres/web/',wait_until='networkidle');expect(page.locator('#zipBuildBtn')).to_be_enabled(timeout=120000)
                check('Browser builder locale '+lang,page.locator('#zipLangSelect').input_value()==lang)
                page.locator('#zipInput').set_input_files(root/(prefix+'lightwebpres/downloads/library-project.zip'))
                with page.expect_download(timeout=120000) as event:page.locator('#zipBuildBtn').click()
                with zipfile.ZipFile(event.value.path()) as z:
                    names=[n for n in z.namelist() if n.endswith('/library.html') or n=='library.html']
                    check('Actual browser ZIP build '+lang,bool(names) and z.testzip() is None)
                    built=z.read(names[0]).decode();check('Built reader and language '+lang,'data-menu-action="zoom-in"' in built and 'lang="'+lang+'"' in built)
                check('No interaction runtime errors '+lang,not runtime,runtime);ctx.close()
                ctx=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,locale='fr-FR');page=ctx.new_page()
                page.goto(base+prefix+'lightwebpres/demo/library.html',wait_until='networkidle')
                page.locator('#navMenu').tap();page.locator('#menuReading').tap();expect(page.locator('#readingMenu')).to_be_visible()
                page.locator('[data-menu-action=zoom-in]').tap();expect(page.locator('#menuZoomValue')).to_have_text('110%')
                check('Touch zoom increases '+lang,page.evaluate('parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--lwp-presentation-zoom"))>1'))
                page.screenshot(path=str(report/(lang+'-touch-zoom.png')))
                page.locator('[data-menu-action=zoom-out]').tap();expect(page.locator('#menuZoomValue')).to_have_text('100%')
                page.locator('[data-menu-action=zoom-in]').tap();page.locator('[data-menu-action=zoom-reset]').tap();expect(page.locator('#menuZoomValue')).to_have_text('100%')
                box=page.locator('#readingMenu').bounding_box();check('Touch menu fits '+lang,box['x']>=0 and box['x']+box['width']<=391,box)
                page.locator('#menuTableMode').select_option('scroll');page.locator('#readingMenu').tap(position={'x':4,'y':4})
                page.locator('#comparison').scroll_into_view_if_needed();page.wait_for_timeout(200)
                table=page.locator('#comparison .lwp-table-viewport');table.evaluate('e=>e.scrollLeft=e.scrollWidth')
                check('Wide table scrolls '+lang,table.evaluate('e=>getComputedStyle(e).overflowX==="auto"&&e.scrollWidth>e.clientWidth&&e.scrollLeft>0'))
                page.goto(base+prefix+'lightwebpres/demo/library.html',wait_until='networkidle');page.wait_for_timeout(300);before=page.evaluate('scrollY')
                page.evaluate('''()=>{const el=document.querySelector('#opening');const t=(id,x)=>new Touch({identifier:id,target:el,clientX:x,clientY:300,pageX:x,pageY:300});const a=t(1,320),b=t(2,160),c=t(1,60);el.dispatchEvent(new TouchEvent('touchstart',{bubbles:true,touches:[a],changedTouches:[a]}));el.dispatchEvent(new TouchEvent('touchstart',{bubbles:true,touches:[a,b],changedTouches:[b]}));el.dispatchEvent(new TouchEvent('touchend',{bubbles:true,touches:[b],changedTouches:[c]}));el.dispatchEvent(new TouchEvent('touchend',{bubbles:true,touches:[],changedTouches:[b]}));}''')
                page.wait_for_timeout(400);check('Multitouch does not navigate '+lang,abs(page.evaluate('scrollY')-before)<3);ctx.close()
                standalone=root/(prefix+'lightwebpres/downloads/publication.html');doc=BeautifulSoup(standalone.read_text(),'html.parser')
                check('Single HTML embeds resources '+lang,not doc.select('script[src],link[rel=stylesheet][href]') and all(n.get('src','').startswith('data:') for n in doc.select('img[src]')))
                ctx=browser.new_context(locale='fr-FR');page=ctx.new_page();network=[]
                page.on('request',lambda request:network.append(request.url) if request.url.startswith(('http://','https://')) else None)
                page.goto(standalone.as_uri(),wait_until='load');expect(page.locator('.article-card').first).to_be_visible()
                page.locator('.article-card').first.click();expect(page.locator('#navMenu')).to_be_visible()
                check('Standalone reader without network '+lang,page.locator('html').get_attribute('lang')==lang and not network,network);ctx.close()
            ctx=browser.new_context(locale='fr-FR');page=ctx.new_page();page.goto(base+'fr/pasteberth/')
            page.evaluate("localStorage.setItem('pb-lang','fr');localStorage.setItem('fadeshed-language','fr')")
            for route in ['', 'fileshed/','pasteberth/','lightwebpres/']:
                page.goto(base+route,wait_until='networkidle');check('Neutral URL is English '+route,page.locator('html').get_attribute('lang')=='en')
            page.goto(base+'lightwebpres/ecrire.html?lang=fr#notes-et-liens',wait_until='networkidle');page.wait_for_url('**/fr/lightwebpres/ecrire.html#notes-et-liens')
            check('French deep link',page.locator('html').get_attribute('lang')=='fr')
            page.locator('.fs-language').first.locator('[data-fs-lang=en]').click();page.wait_for_url('**/lightwebpres/ecrire.html#notes-et-liens')
            check('Language switch retains section',page.locator('html').get_attribute('lang')=='en');ctx.close()
            for lang,prefix in [('en',''),('fr','fr/')]:
                ctx=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844});page=ctx.new_page()
                page.goto(base+prefix+'lightwebpres/');expect(page.locator('.fs-language').first).to_be_visible()
                page.locator('.fs-language').first.locator('[data-fs-lang='+('fr' if lang=='en' else 'en')+']').click()
                check('No-JS language switch '+lang,page.locator('html').get_attribute('lang')!=lang);ctx.close()
            browser.close()
    except Exception:
        (report/'failure.txt').write_text(traceback.format_exc())
        if page:
            try:page.screenshot(path=str(report/'failure.png'),full_page=True)
            except Exception:pass
        raise
    finally:
        if server:server.shutdown()
    return checks


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('root',type=Path);ap.add_argument('report',type=Path);ap.add_argument('--base-url')
    a=ap.parse_args();run(a.root,a.report,a.base_url)
