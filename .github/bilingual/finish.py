#!/usr/bin/env python3
"""Complete translated reader metadata and check explicit locale routing first."""
from pathlib import Path
root=Path(__file__).resolve().parent
p=root/'language.css';p.write_text(p.read_text().replace('body:not(.lwp-index)','body:not(.index-page)'))
p=root/'build.py';s=p.read_text()
old='    translate_blocks(s,blocks);text_translate(s,ui)'
new='''    translate_blocks(s,blocks);text_translate(s,ui)
    plain={" ".join(soup(k).get_text(" ",strip=True).split()):soup(v).get_text(" ",strip=True) for k,v in {**blocks,**ui}.items()}
    def localize_preview(value):
        if isinstance(value,dict):return {k:localize_preview(v) for k,v in value.items()}
        if isinstance(value,list):return [localize_preview(v) for v in value]
        if isinstance(value,str):return plain.get(" ".join(value.split()),value)
        return value
    if s.body and s.body.has_attr('data-lwp-tag-preview'):
        s.body['data-lwp-tag-preview']=json.dumps(localize_preview(json.loads(s.body['data-lwp-tag-preview'])),ensure_ascii=False)
'''
if old not in s:raise RuntimeError('Guide translation hook changed')
p.write_text(s.replace(old,new,1))
p=root/'qa.py';s=p.read_text()
old="            browser=p.chromium.launch(headless=True)"
new=old+'''
            diagnostic=browser.new_page()
            diagnostic.add_init_script("""window.__routeTrace=[{event:'init',url:location.href}];for(const method of ['replaceState','pushState']){const original=history[method].bind(history);history[method]=function(...a){window.__routeTrace.push({event:method,from:location.href,to:a[2]});return original(...a)}};addEventListener('load',()=>window.__routeTrace.push({event:'load',url:location.href,entry:window.__fsEntryHash}));""")
            diagnostic.goto(base+'lightwebpres/ecrire.html?lang=fr#notes-et-liens',wait_until='networkidle')
            diagnostic.wait_for_timeout(1000)
            state=diagnostic.evaluate("""({url:location.href,entry:window.__fsEntryHash,lang:document.documentElement.lang,trace:window.__routeTrace,ids:Array.from(document.querySelectorAll('section.slide')).map(e=>e.id),routing:document.querySelector('#fs-language-route')?.textContent,scripts:Array.from(document.scripts).map(s=>s.src).filter(Boolean)})""")
            (report/'locale-route.json').write_text(json.dumps(state,ensure_ascii=False,indent=2))
            diagnostic.screenshot(path=str(report/'locale-route.png'))
            check('Explicit French route preserves a requested section',state['url'].endswith('/fr/lightwebpres/ecrire.html#notes-et-liens') and state['lang']=='fr',state)
            diagnostic.close()
'''
if old not in s:raise RuntimeError('Browser launch hook changed')
p.write_text(s.replace(old,new,1))
