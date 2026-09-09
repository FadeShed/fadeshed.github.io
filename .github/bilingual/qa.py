#!/usr/bin/env python3
"""Exercise both static editions over HTTP, locally or on deployed Pages."""
import argparse,functools,hashlib,http.server,json,re,threading,urllib.parse,zipfile
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright,expect


def run(root,report,base=None):
    report.mkdir(parents=True,exist_ok=True);results=[];server=None;browser=None
    def check(name,condition,detail=''):
        results.append({'check':name,'passed':bool(condition),'detail':str(detail)[:3000]})
        print(('PASS ' if condition else 'FAIL ')+name,flush=True)
        (report/'report.json').write_text(json.dumps({'checks':len(results),'passed':sum(x['passed'] for x in results),'results':results},ensure_ascii=False,indent=2))
        if not condition:raise AssertionError(name+': '+str(detail))
    if base is None:
        class Quiet(http.server.SimpleHTTPRequestHandler):
            def log_message(self,*a):pass
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root)))
        threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
    base=base.rstrip('/')+'/'
    routes=['','fileshed/','pasteberth/','lightwebpres/']
    lwp=['decouvrir.html','demarrer.html','ecrire.html','apparence.html','publier.html','ressources.html','demo/ma-page.html','demo/index.html','guide/guide.html','guide/index.html','themes.html','web/']
    errors=[]
    for rel in ['index.html','fileshed/index.html','pasteberth/index.html','pasteberth/demo.html']+['lightwebpres/'+(n+'index.html' if n.endswith('/') else n) for n in ['index.html']+lwp]:
        for prefix in ['', 'fr/']:
            file=root/(prefix+rel)
            if not file.is_file():
                if rel=='lightwebpres/':continue
                errors.append((prefix+rel,'missing'));continue
            s=BeautifulSoup(file.read_text(),'html.parser')
            for e in s.find_all(['a','img','script','link','iframe']):
                ref=e.get('href') if e.name in ['a','link'] else e.get('src')
                if not ref or ref.startswith(('#','data:','blob:','http:','https:','javascript:','mailto:')):continue
                u=urllib.parse.urlsplit(ref);p=(root/u.path.lstrip('/')) if u.path.startswith('/') else file.parent/urllib.parse.unquote(u.path)
                if not p.exists():errors.append((prefix+rel,ref))
    check('All public page links and local assets resolve',not errors,errors[:25])
    for prefix in ['', 'fr/']:
        for name in ['demarrage.zip','lightwebpres-cli.zip','site-sources.zip','skills.zip']:
            with zipfile.ZipFile(root/(prefix+'lightwebpres/downloads/'+name)) as z:check('ZIP intact '+prefix+name,z.testzip() is None)
        for n in lwp:check('Complete portal resource '+prefix+n,(root/(prefix+'lightwebpres/'+n)).exists())
    check('Copied application engines unchanged',(root/'lightwebpres/web/lightwebpres').read_bytes()==(root/'fr/lightwebpres/web/lightwebpres').read_bytes())
    check('Pasteberth original frontend unchanged',(root/'pasteberth/assets/product/app.js').read_bytes()==(root/'fr/pasteberth/assets/product/app.js').read_bytes())
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            diagnostic=browser.new_page(locale='fr-FR')
            diagnostic.add_init_script("""window.__routeTrace=[{event:'init',url:location.href}];for(const method of ['replaceState','pushState']){const original=history[method].bind(history);history[method]=function(...a){window.__routeTrace.push({event:method,from:location.href,to:a[2]});return original(...a)}};addEventListener('load',()=>window.__routeTrace.push({event:'load',url:location.href,entry:window.__fsEntryHash}));""")
            diagnostic.goto(base+'fr/pasteberth/',wait_until='networkidle')
            diagnostic.evaluate("localStorage.setItem('pb-lang','fr');localStorage.setItem('pasteberth-site-language-choice','fr');localStorage.setItem('fadeshed-language','fr')")
            for route in routes:diagnostic.goto(base+route,wait_until='networkidle')
            diagnostic.goto(base+'lightwebpres/ecrire.html?lang=fr#notes-et-liens',wait_until='networkidle')
            diagnostic.wait_for_timeout(1500)
            state=diagnostic.evaluate("""({url:location.href,entry:window.__fsEntryHash,storage:Object.fromEntries(Object.entries(localStorage)),lang:document.documentElement.lang,trace:window.__routeTrace,ids:Array.from(document.querySelectorAll('section.slide')).map(e=>e.id),routing:document.querySelector('#fs-language-route')?.textContent,scripts:Array.from(document.scripts).map(s=>s.src).filter(Boolean)})""")
            (report/'locale-route.json').write_text(json.dumps(state,ensure_ascii=False,indent=2))
            diagnostic.screenshot(path=str(report/'locale-route.png'))
            check('Explicit French route preserves a requested section',state['url'].endswith('/fr/lightwebpres/ecrire.html#notes-et-liens') and state['lang']=='fr',state)
            diagnostic.close()

            for locale,prefix in [('en',''),('fr','fr/')]:
                for route in routes:
                    for width in [320,390,768,1024,1440]:
                        context=browser.new_context(viewport={'width':width,'height':960 if width>=768 else 844},locale='fr-FR',accept_downloads=True)
                        page=context.new_page();err=[];page.on('pageerror',lambda e:err.append(str(e)))
                        response=page.goto(base+prefix+route,wait_until='networkidle',timeout=60000)
                        check(f'HTTP {locale} {route or "home"} {width}',response.status==200)
                        check(f'Locale {locale} {route or "home"} {width}',page.locator('html').get_attribute('lang')==locale)
                        overflow=page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
                        if overflow:
                            page.screenshot(path=str(report/f'overflow-{locale}-{route.strip("/") or "home"}-{width}.png'),full_page=True)
                            (report/'overflow.json').write_text(json.dumps(page.evaluate("""Array.from(document.querySelectorAll('body *')).filter(e=>{let r=e.getBoundingClientRect();return r.width&&r.right>innerWidth+1}).map(e=>({tag:e.tagName,class:e.className,width:e.getBoundingClientRect().width,text:e.textContent.slice(0,120)})).slice(0,30)"""),ensure_ascii=False,indent=2))
                        check(f'No overflow {locale} {route or "home"} {width}',not overflow,page.evaluate('({scroll:document.documentElement.scrollWidth,width:innerWidth})'))
                        expect(page.locator('.fs-language').first).to_be_visible()
                        check(f'Selected switch {locale} {route or "home"} {width}',page.locator('.fs-language').first.locator('[aria-current]').get_attribute('data-fs-lang')==locale)
                        if route:
                            check(f'Localized parent {locale} {route} {width}',page.locator('.fs-home').first.evaluate('(e)=>new URL(e.href).pathname')=='/'+prefix)
                        if width in [390,1440]:page.screenshot(path=str(report/f'{locale}-{route.strip("/") or "home"}-{width}.png'))
                        check(f'No JavaScript error {locale} {route or "home"} {width}',not err,err)
                        context.close()
                ctx=browser.new_context(viewport={'width':1440,'height':960},locale='fr-FR',accept_downloads=True)
                page=ctx.new_page();runtime=[];page.on('pageerror',lambda e:runtime.append(str(e)))
                for name in lwp:
                    page.goto(base+prefix+'lightwebpres/'+name,wait_until='networkidle',timeout=90000)
                    check(f'LWP page locale {locale} {name}',page.locator('html').get_attribute('lang')==locale)
                    expect(page.locator('.fs-language').first).to_be_visible()
                    check(f'LWP paired page {locale} {name}',page.locator('.fs-language').first.locator('[data-fs-lang="'+('fr' if locale=='en' else 'en')+'"]').evaluate('(e)=>new URL(e.href).pathname').replace('/fr/','/')==('/lightwebpres/'+name).removesuffix('index.html'))
                    if name=='guide/index.html' and locale=='fr':check('French guide introduction translated','One Markdown source' not in page.locator('body').inner_text())
                    if name=='themes.html':
                        expected='Fond' if locale=='fr' else 'Background';check(f'Gallery controls {locale}',expected in page.locator('body').inner_text())
                    if name=='web/':expect(page.locator('#zipBuildBtn')).to_be_enabled(timeout=90000)
                page.goto(base+prefix+'pasteberth/',wait_until='networkidle')
                page.locator('[data-kind="pdf"]').click()
                with page.expect_download() as event:page.locator('#download-sample').click()
                check('PDF sample '+locale,Path(event.value.path()).read_bytes().startswith(b'%PDF'))
                page.locator('#project-name').fill('new-project')
                expect(page.locator('#generated-id')).to_contain_text('new-project')
                with page.expect_download() as event:page.locator('#download-config').click()
                import tomllib
                check('Generated TOML '+locale,bool(tomllib.loads(Path(event.value.path()).read_text()).get('zone_collection')))
                page.locator('#add-project').click();expect(page.locator('#new-zone-pill')).to_be_visible(timeout=10000)
                page.locator('#launch-demo').click();frame=page.frame_locator('#demo-frame');expect(frame.locator('.zone').first).to_be_visible(timeout=15000)
                check('Demo language '+locale,frame.locator('html').get_attribute('lang')==locale)
                check('No demo version '+locale,frame.locator('.brand-version').count()==0)
                page.locator('[data-scene="selection"]').click();expect(frame.locator('.selection-summary-name')).to_have_count(2)
                with page.expect_download() as event:frame.locator('.zone').first.get_by_role('button',name=re.compile('ZIP')).first.click()
                with zipfile.ZipFile(event.value.path()) as z:check('Demo selection ZIP '+locale,z.testzip() is None and len(z.namelist())==2)
                page.locator('[data-scene="focus"]').click()
                frame.locator('.zone-upload-btn').first.click();frame.locator('#file-picker').set_input_files({'name':'test-bilingual.txt','mimeType':'text/plain','buffer':b'Bilingual synthetic test.\n'})
                expect(frame.locator('.zone').first.locator('.fname')).to_have_text('test-bilingual.txt')
                frame.locator('.comment-btn').first.click();frame.locator('textarea').first.fill('Test de commentaire');frame.locator('.comment-save-btn').first.click();expect(frame.locator('.comment-text').first).to_have_text('Test de commentaire')
                frame.locator('.transfer-target').first.select_option('studio-ignoredbygit-exchange');frame.locator('.copy-transfer-btn').first.click()
                page.locator('[data-scene="overview"]').click();expect(frame.locator('.zone')).to_have_count(3)
                check('Copy between zones '+locale,frame.locator('.zone[data-zone="studio-ignoredbygit-exchange"] .thumb-wrap[data-item-id="test-bilingual.txt"]').count()==1)
                page.locator('#reset-demo').click();expect(frame.locator('.tab-zone-link').first).to_be_visible(timeout=15000)
                check('Demo reset '+locale,frame.locator('.thumb-wrap[data-item-id="test-bilingual.txt"]').count()==0)
                if locale=='fr':
                    body=frame.locator('body').inner_text();check('French demo controls',('Ajouter des fichiers' in body) and ('Copy link' not in body),body[:500])
                page.screenshot(path=str(report/f'{locale}-pasteberth-demo.png'))
                page.goto(base+prefix+'lightwebpres/demo/ma-page.html',wait_until='networkidle');check('Example slides retained '+locale,page.locator('section.slide').count()>=3)
                page.keyboard.press('ArrowRight');page.keyboard.press('h');expect(page.locator('#helpOverlay')).to_be_visible();check('Localized LWP help '+locale,page.locator('#helpTitle').inner_text()==('Raccourcis clavier' if locale=='fr' else 'Keyboard shortcuts'));page.keyboard.press('Escape')
                page.keyboard.press('c');expect(page.locator('#themeMenu')).to_be_visible();page.keyboard.press('Escape')
                page.goto(base+prefix+'lightwebpres/web/',wait_until='networkidle');expect(page.locator('#zipBuildBtn')).to_be_enabled(timeout=90000)
                check('Builder default output language '+locale,page.locator('#zipLangSelect').input_value()==locale)
                check('Localized builder label '+locale,page.locator('#zipBuildBtn').inner_text()==('Construire' if locale=='fr' else 'Build'))
                page.locator('#zipInput').set_input_files(root/(prefix+'lightwebpres/downloads/demarrage.zip'))
                with page.expect_download(timeout=90000) as event:page.locator('#zipBuildBtn').click()
                with zipfile.ZipFile(event.value.path()) as z:
                    names=z.namelist();html=[n for n in names if n.endswith('ma-page.html')]
                    check('Actual browser build '+locale,bool(html) and z.testzip() is None)
                    check('Browser-built locale '+locale,'lang="'+locale+'"' in z.read(html[0]).decode())
                check('No interaction JS errors '+locale,not runtime,runtime)
                ctx.close()
            # Neutral paths deliberately ignore previously selected language.
            ctx=browser.new_context(locale='fr-FR');page=ctx.new_page()
            page.goto(base+'fr/pasteberth/',wait_until='networkidle')
            page.evaluate("localStorage.setItem('pb-lang','fr');localStorage.setItem('pasteberth-site-language-choice','fr');localStorage.setItem('fadeshed-language','fr')")
            for route in routes:
                page.goto(base+route,wait_until='networkidle');check('Neutral URL always English '+route,page.locator('html').get_attribute('lang')=='en')
            page.goto(base+'lightwebpres/ecrire.html?lang=fr#notes-et-liens',wait_until='networkidle');(report/'actual-switch-route.json').write_text(json.dumps(page.evaluate("({url:location.href,entry:window.__fsEntryHash,lang:document.documentElement.lang,storage:Object.fromEntries(Object.entries(localStorage))})"),ensure_ascii=False,indent=2));page.wait_for_url('**/fr/lightwebpres/ecrire.html#notes-et-liens');check('Query FR selects full French edition',page.locator('html').get_attribute('lang')=='fr')
            page.locator('.fs-language').first.locator('[data-fs-lang=en]').click();page.wait_for_url('**/lightwebpres/ecrire.html#notes-et-liens');check('Switch retains article and fragment',page.locator('html').get_attribute('lang')=='en')
            page.goto(base+'fr/lightwebpres/?lang=en',wait_until='networkidle');page.wait_for_url('**/lightwebpres/');check('Explicit EN overrides French path',page.locator('html').get_attribute('lang')=='en')
            page.goto(base+'fr/');page.locator('a[href="fileshed/"]').first.click();check('French home to product remains French','/fr/fileshed/' in page.url)
            ctx.close()
            for locale,prefix in [('en',''),('fr','fr/')]:
                ctx=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844});page=ctx.new_page()
                for route in routes:
                    page.goto(base+prefix+route,wait_until='load');check('No-JS edition '+locale+route,page.locator('html').get_attribute('lang')==locale);expect(page.locator('.fs-language').first).to_be_visible()
                page.locator('.fs-language').first.locator('[data-fs-lang="'+('fr' if locale=='en' else 'en')+'"]').click();check('No-JS switch '+locale,page.locator('html').get_attribute('lang')!=locale);ctx.close()
            browser.close()
    except Exception as e:
        import traceback
        (report/'failure.txt').write_text(traceback.format_exc())
        results.append({'check':'Complete bilingual suite','passed':False,'detail':str(e)})
        (report/'report.json').write_text(json.dumps({'checks':len(results),'passed':sum(x['passed'] for x in results),'results':results,'base_url':base},ensure_ascii=False,indent=2))
        raise
    finally:
        if server:server.shutdown()
    return results

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('report',type=Path);ap.add_argument('--base-url');a=ap.parse_args();run(a.root,a.report,a.base_url)
