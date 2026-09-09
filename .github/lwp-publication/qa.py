#!/usr/bin/env python3
"""Run existing product regressions plus approved LightWebPres comparison tests."""
import argparse, hashlib, json, re, traceback, urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, expect
ENGINE='bdbb84bc6fee5e27927ddc3d65bcd1d963adcff6350b0c1b16fdc36a9771b974'

def run(root,report,base):
    root=root.resolve();report.mkdir(parents=True,exist_ok=True)
    baseline=Path(__file__).resolve().parents[1]/'reader-refresh/qa.py'
    source=baseline.read_text()
    if source.count("page.locator('.fs-role-card').count()==6")!=1:raise RuntimeError('Unexpected inherited QA baseline')
    source=source.replace("page.locator('.fs-role-card').count()==6", "page.locator('.pv-role').count()==6")
    source=source.replace("page.locator('.lwp-web-home-grid pre').count()==0", "page.locator('.pv-hero pre').count()==0")
    # This approved renderer has a separate native Size and tables dialog.
    source=source.replace('#presenterMenu [data-menu-action=zoom-in]', '#readingMenu [data-menu-action=zoom-in]')
    source=source.replace("page.locator('#navMenu').tap();expect(page.locator('#presenterMenu')).to_be_visible()", "page.locator('#navMenu').tap();expect(page.locator('#presenterMenu')).to_be_visible();page.locator('#menuReading').tap();expect(page.locator('#readingMenu')).to_be_visible()")
    source=source.replace("page.locator('#presenterMenu').bounding_box()", "page.locator('#readingMenu').bounding_box()")
    source=source.replace("page.locator('#presenterMenu').tap(position={'x':4,'y':4});expect(page.locator('#presenterMenu')).not_to_be_visible()", "page.locator('#readingMenu').tap(position={'x':4,'y':4});expect(page.locator('#readingMenu')).not_to_be_visible()")
    source=source.replace("parseFloat(document.documentElement.style.zoom)>1", "parseFloat(getComputedStyle(document.documentElement).getPropertyValue(\"--lwp-presentation-zoom\"))>1")
    source=source.replace("!document.documentElement.style.zoom||Number(document.documentElement.style.zoom)===1", "parseFloat(getComputedStyle(document.documentElement).getPropertyValue(\"--lwp-presentation-zoom\"))===1")
    suite={'__name__':'reader_regressions','__file__':str(baseline)}
    exec(compile(source,str(baseline),'exec'),suite);suite['ENGINE']=ENGINE
    checks=suite['run'](root,report,base)
    srv=None
    if base is None:srv,base=suite['serve'](root)
    base=base.rstrip('/')+'/'
    def check(name,ok,detail=''):
        checks.append({'check':name,'passed':bool(ok),'detail':str(detail)[:1500]})
        (report/'report.json').write_text(json.dumps({'checks':len(checks),'passed':sum(c['passed'] for c in checks),'base_url':base,'results':checks},ensure_ascii=False,indent=2)+'\n')
        print(('PASS ' if ok else 'FAIL ')+name,flush=True)
        if not ok:raise AssertionError(name+': '+str(detail))
    try:
        html_cache={};references=0;errors=[]
        for folder in ['lightwebpres','fr/lightwebpres']:
            for path in (root/folder).rglob('*.html'):
                if 'reference' in path.relative_to(root).parts:continue
                parsed=BeautifulSoup(path.read_text(),'html.parser')
                for el in parsed.find_all(['a','img','script','link','iframe']):
                    href=el.get('href') if el.name in ['a','link'] else el.get('src')
                    if not href or href.startswith(('data:','blob:','http:','https:','mailto:','javascript:','tel:')):continue
                    u=urllib.parse.urlsplit(href);relative=urllib.parse.unquote(u.path)
                    target=(root/relative.lstrip('/') if relative.startswith('/') else path.parent/relative) if relative else path
                    if target.is_dir():target=target/'index.html'
                    target=target.resolve();references+=1
                    if not target.is_relative_to(root) or not target.is_file():errors.append((str(path.relative_to(root)),href));continue
                    if u.fragment and target.suffix=='.html':
                        if target not in html_cache:html_cache[target]={e.get('id') for e in BeautifulSoup(target.read_text(),'html.parser').find_all(id=True)}
                        if urllib.parse.unquote(u.fragment) not in html_cache[target]:errors.append((str(path.relative_to(root)),href))
        check('Local assets, pages and anchors across LWP',not errors,{'references':references,'errors':errors[:15]})
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            for lang,prefix in [('en',''),('fr','fr/')]:
                for width in [390,1440]:
                    page=browser.new_page(viewport={'width':width,'height':844 if width==390 else 960},locale='fr-FR')
                    err=[];page.on('pageerror',lambda e:err.append(str(e)))
                    page.goto(base+prefix+'lightwebpres/',wait_until='networkidle')
                    check(f'Approved homepage {lang} {width}',page.locator('.proposal-home').count()==1)
                    check(f'Three identity choices {lang} {width}',page.locator('[data-choice]').count()==3)
                    for choice in ['native','docs','field-notes']:
                        page.locator('[data-choice="'+choice+'"]').click()
                        panel=page.locator('[data-panel="'+choice+'"]');expect(panel).to_be_visible()
                        check(f'Identity illustration {lang} {width} {choice}',panel.locator('img').evaluate_all('ns=>ns.length>0&&ns.every(e=>e.complete&&e.naturalWidth>0)'))
                        check(f'Comparator selection {lang} {width} {choice}',page.locator('[data-choice="'+choice+'"]').get_attribute('aria-pressed')=='true')
                    page.locator('[data-choice=native]').focus();page.keyboard.press('ArrowRight')
                    check(f'Keyboard comparator {lang} {width}',page.locator('[data-choice=docs]').get_attribute('aria-pressed')=='true')
                    page.screenshot(path=str(report/f'{lang}-identities-{width}.png'))
                    page.locator('[data-choice=native]').click();page.evaluate('scrollTo(0,0)');page.screenshot(path=str(report/f'{lang}-approved-home-{width}.png'),full_page=True)
                    check(f'Comparison runtime {lang} {width}',not err,err);page.close()
                page=browser.new_page(viewport={'width':1280,'height':720})
                for identity in ['native','docs','field-notes','nebula']:
                    res=page.goto(base+prefix+'lightwebpres/concepts/'+identity+'/first-page.html',wait_until='networkidle')
                    check(f'Real comparison page {lang} {identity}',res.status==200 and page.locator('html').get_attribute('lang')==lang)
                    check(f'Native menu available {lang} {identity}',page.locator('#navMenu').count()==1 and page.locator('.fs-reader-open').count()==0)
                page.close()
            browser.close()
    except Exception:
        (report/'proposal-failure.txt').write_text(traceback.format_exc());raise
    finally:
        if srv:srv.shutdown()

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('report',type=Path);ap.add_argument('--base-url');a=ap.parse_args();run(a.root,a.report,a.base_url)
