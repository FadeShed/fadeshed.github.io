#!/usr/bin/env python3
"""HTTP and browser checks of the exact public publication directory."""
import argparse
import functools
import hashlib
import http.server
import json
import re
import threading
import urllib.parse
import zipfile
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, expect


def run(root, report, base_url=None):
    report.mkdir(parents=True,exist_ok=True)
    results=[]
    def check(name, value, detail=''):
        results.append({'check':name,'passed':bool(value),'detail':str(detail)})
        print(('PASS ' if value else 'FAIL ')+name, flush=True)
        if not value: raise AssertionError(name+': '+str(detail))
    errors=[]
    for f in root.rglob('*.html'):
        if f.name.endswith('.template.html'): continue
        s=BeautifulSoup(f.read_text(),'html.parser')
        for e in s.find_all(['a','img','link','script','iframe']):
            ref=e.get('href') if e.name in ['a','link'] else e.get('src')
            if not ref or ref.startswith(('#','data:','blob:','http:','https:','mailto:','javascript:')): continue
            u=urllib.parse.urlsplit(ref)
            p=(root/u.path.lstrip('/')) if ref.startswith('/') else (f.parent/urllib.parse.unquote(u.path))
            if not p.exists(): errors.append((str(f.relative_to(root)),ref))
    check('Local HTML links and assets exist',not errors,errors[:20])
    for n in ['demarrage.zip','lightwebpres-cli.zip','site-sources.zip','skills.zip']:
        with zipfile.ZipFile(root/'lightwebpres/downloads'/n) as z: check('ZIP intact: '+n,z.testzip() is None)
    for n in ['decouvrir.html','demarrer.html','ecrire.html','apparence.html','publier.html','ressources.html','demo/ma-page.html','guide/guide.html','themes.html','web/index.html','web/vendor/pyodide/pyodide.asm.wasm']:
        check('LWP original feature retained: '+n,(root/'lightwebpres'/n).is_file())
    for n in ['llms.txt','fileshed/llms.txt','pasteberth/llms.txt','lightwebpres/llms.txt']:
        text=(root/n).read_text()
        check('Markdown index: '+n,text.startswith('# ') and '\n> ' in text and '\n## ' in text and '](' in text)
    for n in ['index.html','fileshed/index.html','pasteberth/index.html','lightwebpres/index.html']:
        text=(root/n).read_text()
        check('No private documentation links: '+n,'fadeshed-internal' not in text)
    check('No visible demo version badge','brand-version">' not in (root/'pasteberth/demo.html').read_text())
    server=None
    if base_url is None:
        class Quiet(http.server.SimpleHTTPRequestHandler):
            def log_message(self,*args): pass
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root)))
        threading.Thread(target=server.serve_forever,daemon=True).start()
        base_url='http://127.0.0.1:'+str(server.server_port)+'/'
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            for product in ['', 'fileshed/','pasteberth/','lightwebpres/']:
                for width in [320,390,768,1024,1440]:
                    ctx=browser.new_context(viewport={'width':width,'height':960 if width>600 else 844},locale='fr-FR')
                    page=ctx.new_page(); js_errors=[]; page.on('pageerror',lambda e:js_errors.append(str(e)))
                    response=page.goto(base_url+product,wait_until='networkidle',timeout=60000)
                    check(f'HTTP {product or "home"} {width}',response.status==200)
                    overflow=page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                    if overflow:
                        page.screenshot(path=str(report/f'overflow-{product.strip("/") or "home"}-{width}.png'),full_page=True)
                        detail=page.evaluate("""Array.from(document.querySelectorAll('body *')).filter(e=>{const r=e.getBoundingClientRect();return r.width&&r.right>innerWidth+1}).map(e=>({tag:e.tagName,class:e.className,w:e.getBoundingClientRect().width,right:e.getBoundingClientRect().right,text:e.textContent.slice(0,80)})).slice(0,25)""")
                    else: detail=[]
                    check(f'No overflow {product or "home"} {width}',not overflow,detail)
                    if product:
                        expect(page.locator('.fs-home').first).to_be_visible()
                        check(f'Parent navigation {product} {width}',page.locator('.fs-home').first.evaluate('(e)=>new URL(e.href).pathname')=='/')
                    if width in [390,1440]: page.screenshot(path=str(report/f'{product.strip("/") or "fadeshed"}-{width}.png'))
                    check(f'No JS error {product or "home"} {width}',not js_errors,js_errors)
                    ctx.close()
            ctx=browser.new_context(viewport={'width':1440,'height':960},locale='fr-FR',accept_downloads=True)
            page=ctx.new_page(); runtime_errors=[]; page.on('pageerror',lambda e:runtime_errors.append(str(e)))
            page.goto(base_url+'pasteberth/',wait_until='networkidle')
            check('Pasteberth defaults to EN for a French browser',page.locator('html').get_attribute('lang')=='en')
            page.locator('[data-lang="fr"]').first.click()
            check('Explicit FR selection',page.locator('html').get_attribute('lang')=='fr')
            page.reload(wait_until='networkidle')
            check('Language selection persists',page.locator('html').get_attribute('lang')=='fr')
            page.goto(base_url+'pasteberth/?lang=en',wait_until='networkidle')
            check('URL language overrides saved choice',page.locator('html').get_attribute('lang')=='en')
            page.locator('[data-kind="pdf"]').click()
            with page.expect_download() as d: page.locator('#download-sample').click()
            downloaded=d.value.path()
            check('Sample PDF downloads',Path(downloaded).read_bytes().startswith(b'%PDF'))
            page.locator('#project-name').fill('new-project')
            check('TOML generator updates ID','new-project-' in page.locator('#generated-id').inner_text())
            with page.expect_download() as d: page.locator('#download-config').click()
            import tomllib
            config=tomllib.loads(Path(d.value.path()).read_text())
            check('Generated configuration is TOML','zone_collection' in config and 'groups' in config)
            page.locator('#add-project').click()
            expect(page.locator('#new-zone-pill')).to_be_visible()
            check('New-project simulation completes','4 zones' in page.locator('#zone-count').inner_text())
            page.locator('#launch-demo').click()
            frame=page.frame_locator('#demo-frame')
            expect(frame.locator('.zone').first).to_be_visible(timeout=20000)
            check('Integrated demo loads',frame.locator('.zone').count()>0)
            check('No version displayed by the demo',frame.locator('.brand-version').count()==0)
            page.locator('[data-scene="overview"]').click()
            expect(frame.locator('.zone')).to_have_count(3)
            page.locator('[data-scene="selection"]').click()
            expect(frame.locator('.selection-summary-name')).to_have_count(2)
            zip_button=frame.get_by_role('button',name=re.compile('ZIP',re.I))
            with page.expect_download() as d: zip_button.first.click()
            with zipfile.ZipFile(d.value.path()) as z:
                check('Demo selection downloads a valid ZIP',z.testzip() is None and any(n.endswith('.pdf') for n in z.namelist()) and any(n.endswith('.xlsx') for n in z.namelist()))
            page.locator('[data-scene="focus"]').click()
            zone=frame.locator('.zone').first
            zone.locator('.zone-upload-btn').click()
            frame.locator('#file-picker').set_input_files({'name':'qa-example.txt','mimeType':'text/plain','buffer':b'Example added to the in-memory demo.\n'})
            expect(frame.locator('.fname').filter(has_text='qa-example.txt')).to_be_visible()
            check('Demo upload appears',True)
            zone.locator('.comment-btn').click();zone.locator('textarea').fill('Ready to review')
            zone.locator('.comment-save-btn').click()
            expect(zone.locator('.comment-text')).to_have_text('Ready to review')
            check('Demo comment saved',True)
            # Studio has an unused target name for the uploaded sample.
            zone.locator('.transfer-target').select_option('studio-ignoredbygit-exchange')
            zone.locator('.copy-transfer-btn').click()
            page.locator('[data-scene="overview"]').click()
            expect(frame.locator('.zone[data-zone="studio-ignoredbygit-exchange"] .thumb-wrap[data-item-id="qa-example.txt"]')).to_be_visible()
            check('Demo copies between zones',True)
            page.screenshot(path=str(report/'pasteberth-demo.png'))
            page.locator('#reset-demo').click()
            expect(frame.locator('.tab-zone-link').first).to_be_visible()
            check('Demo reset removes added files',frame.locator('.thumb-wrap[data-item-id="qa-example.txt"]').count()==0)
            check('No runtime JS errors',not runtime_errors,runtime_errors)
            ctx.close()
            # Mobile menu remains an explicit usable navigation, not hidden links.
            ctx=browser.new_context(viewport={'width':390,'height':844})
            page=ctx.new_page();page.goto(base_url+'pasteberth/',wait_until='networkidle')
            page.locator('#menu-toggle').click();expect(page.locator('#mobile-nav')).to_be_visible()
            page.keyboard.press('Escape');expect(page.locator('#mobile-nav')).to_be_hidden()
            check('Pasteberth mobile menu and Escape',True)
            ctx.close()
            # A real generated LWP article, including navigation and theme selection.
            ctx=browser.new_context(viewport={'width':1440,'height':960},accept_downloads=True)
            page=ctx.new_page();page.goto(base_url+'lightwebpres/demo/ma-page.html',wait_until='networkidle')
            check('LWP demo article has multiple slides',page.locator('section.slide').count()>=3)
            page.keyboard.press('ArrowRight')
            page.wait_for_function('scrollY > 10')
            check('LWP slide navigation works',True)
            page.keyboard.press('h');expect(page.locator('#helpOverlay')).to_be_visible()
            page.keyboard.press('Escape')
            page.keyboard.press('c');expect(page.locator('#themeMenu')).to_be_visible()
            page.keyboard.press('Escape')
            check('LWP help and appearance controls work',True)
            page.goto(base_url+'lightwebpres/web/',wait_until='networkidle',timeout=90000)
            expect(page.locator('#zipBuildBtn')).to_be_enabled(timeout=90000)
            check('Local Pyodide builder initializes',True)
            page.locator('#zipInput').set_input_files(str(root/'lightwebpres/downloads/demarrage.zip'))
            with page.expect_download(timeout=90000) as d: page.locator('#zipBuildBtn').click()
            with zipfile.ZipFile(d.value.path()) as z:
                check('Browser builder produces a valid site ZIP',z.testzip() is None and any(n.endswith('.html') for n in z.namelist()))
            ctx.close();browser.close()
    except Exception as exc:
        import traceback
        (report/'failure.txt').write_text(traceback.format_exc())
        results.append({'check':'Complete browser workflow','passed':False,'detail':str(exc)})
        raise
    finally:
        if server: server.shutdown()
        data={'checks':len(results),'passed':sum(r['passed'] for r in results),'results':results,'base_url':base_url,'scope':'Static links, local HTTP and Chromium. No production backend or native clipboard validation.'}
        (report/'report.json').write_text(json.dumps(data,indent=2)+'\n')
    print('ALL CHECKS PASSED',len(results),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('report',type=Path);ap.add_argument('--base-url')
    a=ap.parse_args();run(a.root,a.report,a.base_url)
