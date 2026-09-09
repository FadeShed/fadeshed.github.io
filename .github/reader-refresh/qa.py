#!/usr/bin/env python3
"""Verify the public EN/FR portal, native touch zoom and existing product journeys."""
import argparse,functools,hashlib,http.server,json,re,threading,traceback,urllib.parse,zipfile
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright,expect
ENGINE='7e63cf4b13882f1318a5a9630bbe389cd9d2b71a583790e9021604aba321f250'
CHAPTERS=['decouvrir.html','usages.html','demarrer.html','ecrire.html','apparence.html','publier.html','ressources.html']
EXTRA=['demo/library.html','demo/ma-page.html','demo/index.html','guide/guide.html','guide/index.html','themes.html','web/index.html']

def serve(root):
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    return server,f'http://127.0.0.1:{server.server_port}/'

def run(root,report,base=None):
    root=root.resolve();report.mkdir(parents=True,exist_ok=True);checks=[];server=None;page=None
    if base is None:server,base=serve(root)
    base=base.rstrip('/')+'/'
    def check(name,ok,detail=''):
        checks.append({'check':name,'passed':bool(ok),'detail':str(detail)[:1500]})
        (report/'report.json').write_text(json.dumps({'checks':len(checks),'passed':sum(x['passed'] for x in checks),'base_url':base,'results':checks},ensure_ascii=False,indent=2))
        print(('PASS ' if ok else 'FAIL ')+name,flush=True)
        if not ok:raise AssertionError(name+': '+str(detail))
    try:
        for prefix in ['', 'fr/']:
            d=root/(prefix+'lightwebpres')
            check('Renderer bytes '+prefix,hashlib.sha256((d/'web/lightwebpres').read_bytes()).hexdigest()==ENGINE)
            with zipfile.ZipFile(d/'downloads/lightwebpres-cli.zip') as z:check('CLI archive uses same renderer '+prefix,hashlib.sha256(z.read('lightwebpres')).hexdigest()==ENGINE)
            for name in ['demarrage.zip','library-project.zip','skills.zip','site-sources.zip']:
                with zipfile.ZipFile(d/'downloads'/name) as z:check('Download intact '+prefix+name,z.testzip() is None)
            for rel in ['index.html','fileshed/index.html','pasteberth/index.html']+['lightwebpres/'+p for p in ['index.html']+CHAPTERS+EXTRA]:
                f=root/(prefix+rel);s=BeautifulSoup(f.read_text(),'html.parser');bad=[]
                for el in s.find_all(['a','img','link','script','iframe']):
                    ref=el.get('href') if el.name in ['a','link'] else el.get('src')
                    if not ref or ref.startswith(('#','data:','blob:','http:','https:','javascript:','mailto:')):continue
                    p=urllib.parse.unquote(urllib.parse.urlsplit(ref).path)
                    target=root/p.lstrip('/') if p.startswith('/') else f.parent/p
                    if not target.exists():bad.append(ref)
                check('Local links '+prefix+rel,not bad,bad)
                # Licenses, example kit identifiers and runtime manifests are not prose versions.
                for el in s.select('script,style,pre,code'):el.decompose()
                text=s.get_text(' ',strip=True)
                check('No product release number '+prefix+rel,not re.search(r'(?:LightWebPres\s+v?\d+\.\d+|\b0\.(?:56|57)\.0\b|\b1\.(?:0\.5|1\.0)\b)',text))
                check('No internal repository link '+prefix+rel,'fadeshed-internal-docs' not in f.read_text())
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            for lang,prefix in [('en',''),('fr','fr/')]:
                for route in ['', 'fileshed/', 'pasteberth/', 'lightwebpres/']:
                    for width in [320,390,768,1440]:
                        ctx=browser.new_context(viewport={'width':width,'height':900 if width>700 else 844},locale='fr-FR')
                        page=ctx.new_page();err=[];page.on('pageerror',lambda e:err.append(str(e)))
                        res=page.goto(base+prefix+route,wait_until='networkidle',timeout=60000)
                        check(f'HTTP {lang} {route} {width}',res.status==200)
                        check(f'Language {lang} {route} {width}',page.locator('html').get_attribute('lang')==lang)
                        expect(page.locator('.fs-language').first).to_be_visible()
                        check(f'No overflow {lang} {route} {width}',page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),page.evaluate('({width:innerWidth,scroll:document.documentElement.scrollWidth})'))
                        check(f'Images decoded {lang} {route} {width}',page.locator('img').evaluate_all('ns=>ns.filter(e=>e.getBoundingClientRect().width>0&&!e.loading.includes("lazy")).every(e=>e.complete&&e.naturalWidth>0)'))
                        if route=='lightwebpres/':
                            check(f'Role entry points {lang} {width}',page.locator('.fs-role-card').count()==6)
                            check(f'No terminal-first hero {lang} {width}',page.locator('.lwp-web-home-grid pre').count()==0)
                        if width in [390,1440]:page.screenshot(path=str(report/f'{lang}-{route.strip("/") or "home"}-{width}.png'),full_page=route=='lightwebpres/')
                        check(f'No runtime error {lang} {route} {width}',not err,err);ctx.close()
                ctx=browser.new_context(viewport={'width':1440,'height':960},locale='fr-FR',accept_downloads=True);page=ctx.new_page();err=[];page.on('pageerror',lambda e:err.append(str(e)))
                for rel in CHAPTERS+EXTRA:
                    response=page.goto(base+prefix+'lightwebpres/'+rel,wait_until='networkidle',timeout=90000)
                    check(f'Complete portal {lang} {rel}',response.status==200 and page.locator('html').get_attribute('lang')==lang)
                    expect(page.locator('.fs-language').first).to_be_visible()
                    if page.locator('section.slide').count():
                        check('Native zoom controls '+lang+rel,page.locator('#presenterMenu [data-menu-action=zoom-in]').count()==1)
                        page.locator('.fs-reader-open').click();expect(page.locator('#presenterMenu')).to_be_visible();page.locator('#presenterMenu').click(position={'x':4,'y':4});expect(page.locator('#presenterMenu')).not_to_be_visible()
                # Existing Pasteberth sandbox: keep operations and resolve the blocked chrome.
                page.goto(base+prefix+'pasteberth/',wait_until='networkidle');page.locator('#launch-demo').click()
                frame=page.frame_locator('#demo-frame');expect(frame.locator('.zone').first).to_be_visible(timeout=15000)
                check('Embedded nav hidden '+lang,not frame.locator('.fs-utility').is_visible())
                check('Demo pictures decoded '+lang,frame.locator('img').evaluate_all('ns=>ns.filter(e=>e.getBoundingClientRect().width>0).every(e=>e.complete&&e.naturalWidth>0)'))
                page.locator('[data-scene=selection]').click();expect(frame.locator('.selection-summary-name')).to_have_count(2)
                with page.expect_download() as download:frame.locator('.zone').first.get_by_role('button',name=re.compile('ZIP')).first.click()
                with zipfile.ZipFile(download.value.path()) as z:check('Pasteberth selection ZIP '+lang,z.testzip() is None and len(z.namelist())==2)
                page.locator('[data-scene=focus]').click();frame.locator('.zone-upload-btn').first.click();frame.locator('#file-picker').set_input_files({'name':'reader-check.txt','mimeType':'text/plain','buffer':b'Synthetic browser check\n'})
                expect(frame.locator('.zone').first.locator('.fname')).to_have_text('reader-check.txt')
                frame.locator('.comment-btn').first.click();frame.locator('textarea').first.fill('Note');frame.locator('.comment-save-btn').first.click();expect(frame.locator('.comment-text').first).to_have_text('Note')
                page.locator('[data-scene=overview]').click();page.locator('#reset-demo').click();expect(frame.locator('.tab-zone-link').first).to_be_visible(timeout=15000)
                check('Pasteberth reset '+lang,frame.locator('.thumb-wrap[data-item-id="reader-check.txt"]').count()==0)
                # Build the actual rich example using the updated engine in Pyodide.
                page.goto(base+prefix+'lightwebpres/web/',wait_until='networkidle');expect(page.locator('#zipBuildBtn')).to_be_enabled(timeout=120000)
                check('Builder output locale '+lang,page.locator('#zipLangSelect').input_value()==lang)
                page.locator('#zipInput').set_input_files(root/(prefix+'lightwebpres/downloads/library-project.zip'))
                with page.expect_download(timeout=120000) as download:page.locator('#zipBuildBtn').click()
                with zipfile.ZipFile(download.value.path()) as z:
                    found=[n for n in z.namelist() if n.endswith('/library.html') or n=='library.html']
                    check('Actual rich browser build '+lang,bool(found) and z.testzip() is None)
                    built=z.read(found[0]).decode();check('Browser output native touch zoom '+lang,'data-menu-action="zoom-in"' in built and 'lang="'+lang+'"' in built)
                check('No interactive runtime errors '+lang,not err,err);ctx.close()
                # Touch interaction tests deliberately use taps, not keyboard shortcuts.
                ctx=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,locale='fr-FR');page=ctx.new_page()
                page.goto(base+prefix+'lightwebpres/demo/library.html',wait_until='networkidle')
                expect(page.locator('.fs-reader-open')).to_be_visible()
                check('Touch entry does not overlap native navigation '+lang,page.evaluate("""()=>{const a=document.querySelector('.fs-reader-open').getBoundingClientRect(),b=document.querySelector('#navMenu').getBoundingClientRect();return !b.width||a.right<=b.left||b.right<=a.left||a.bottom<=b.top||b.bottom<=a.top}"""))
                page.locator('.fs-reader-open').tap();expect(page.locator('#presenterMenu')).to_be_visible()
                page.locator('[data-menu-action=zoom-in]').tap();expect(page.locator('#menuZoomValue')).to_have_text('110%')
                check('Touch zoom increases '+lang,page.evaluate('parseFloat(document.documentElement.style.zoom)>1'))
                page.screenshot(path=str(report/f'{lang}-touch-zoom.png'))
                page.locator('[data-menu-action=zoom-out]').tap();expect(page.locator('#menuZoomValue')).to_have_text('100%')
                page.locator('[data-menu-action=zoom-in]').tap();page.locator('[data-menu-action=zoom-reset]').tap();expect(page.locator('#menuZoomValue')).to_have_text('100%')
                check('Touch zoom resets '+lang,page.evaluate('!document.documentElement.style.zoom||Number(document.documentElement.style.zoom)===1'))
                menu=page.locator('#presenterMenu').bounding_box();check('Touch menu fits screen '+lang,menu['x']>=0 and menu['x']+menu['width']<=391,menu)
                # Select table scrolling explicitly through the same native reader menu.
                page.locator('#menuTableMode').select_option('scroll');page.locator('#presenterMenu').tap(position={'x':4,'y':4});expect(page.locator('#presenterMenu')).not_to_be_visible()
                page.locator('#comparison').scroll_into_view_if_needed();page.wait_for_timeout(250)
                table=page.locator('#comparison .lwp-table-viewport')
                check('Wide table scroll mode '+lang,table.evaluate('e=>getComputedStyle(e).overflowX==="auto"'))
                table.evaluate('e=>e.scrollLeft=e.scrollWidth');check('Wide table actually scrolls '+lang,table.evaluate('e=>e.scrollWidth>e.clientWidth && e.scrollLeft>0'))
                page.screenshot(path=str(report/f'{lang}-touch-table.png'))
                # Regression scenario from the earlier multi-contact handling, not a real pinch test.
                page.goto(base+prefix+'lightwebpres/demo/library.html',wait_until='networkidle');page.wait_for_timeout(350)
                before=page.evaluate('scrollY')
                page.evaluate('''()=>{const el=document.querySelector('#opening');const t=(id,x)=>new Touch({identifier:id,target:el,clientX:x,clientY:300,pageX:x,pageY:300});const a=t(1,320),b=t(2,160),c=t(1,60);el.dispatchEvent(new TouchEvent('touchstart',{bubbles:true,touches:[a],changedTouches:[a]}));el.dispatchEvent(new TouchEvent('touchstart',{bubbles:true,touches:[a,b],changedTouches:[b]}));el.dispatchEvent(new TouchEvent('touchend',{bubbles:true,touches:[b],changedTouches:[c]}));el.dispatchEvent(new TouchEvent('touchend',{bubbles:true,touches:[],changedTouches:[b]}));}''')
                page.wait_for_timeout(500);check('Multitouch does not advance '+lang,abs(page.evaluate('scrollY')-before)<3)
                ctx.close()
            # Explicit locale, stable anchors, no hidden saved preference overriding a neutral URL.
            ctx=browser.new_context(locale='fr-FR');page=ctx.new_page();page.goto(base+'fr/pasteberth/');page.evaluate("localStorage.setItem('pb-lang','fr');localStorage.setItem('fadeshed-language','fr')")
            for route in ['', 'fileshed/','pasteberth/','lightwebpres/']:
                page.goto(base+route,wait_until='networkidle');check('Neutral URL is English '+route,page.locator('html').get_attribute('lang')=='en')
            page.goto(base+'lightwebpres/ecrire.html?lang=fr#notes-et-liens',wait_until='networkidle');page.wait_for_url('**/fr/lightwebpres/ecrire.html#notes-et-liens');check('Explicit FR deep link',page.locator('html').get_attribute('lang')=='fr')
            page.locator('.fs-language').first.locator('[data-fs-lang=en]').click();page.wait_for_url('**/lightwebpres/ecrire.html#notes-et-liens');check('Switch preserves section',page.locator('html').get_attribute('lang')=='en');ctx.close()
            for lang,prefix in [('en',''),('fr','fr/')]:
                ctx=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844});page=ctx.new_page()
                page.goto(base+prefix+'lightwebpres/');expect(page.locator('.fs-language').first).to_be_visible()
                page.locator('.fs-language').first.locator('[data-fs-lang='+('fr' if lang=='en' else 'en')+']').click();check('No-JS language switch '+lang,page.locator('html').get_attribute('lang')!=lang);ctx.close()
            browser.close()
    except Exception:
        (report/'failure.txt').write_text(traceback.format_exc())
        if page:
            try:page.screenshot(path=str(report/'failure.png'),full_page=True)
            except Exception:pass
        check('Complete reader refresh suite',False,traceback.format_exc())
    finally:
        if server:server.shutdown()
    return checks

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('report',type=Path);p.add_argument('--base-url');a=p.parse_args();run(a.root,a.report,a.base_url)
