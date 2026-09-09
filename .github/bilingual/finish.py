#!/usr/bin/env python3
"""Complete translated reader metadata and verify explicit locale routing."""
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
'''
if old not in s:raise RuntimeError('Browser launch hook changed')
s=s.replace(old,new,1)
needle="page.goto(base+'lightwebpres/ecrire.html?lang=fr#notes-et-liens',wait_until='networkidle');page.wait_for_url"
replacement="""page.goto(base+'lightwebpres/ecrire.html?lang=fr#notes-et-liens',wait_until='networkidle');(report/'actual-switch-route.json').write_text(json.dumps(page.evaluate(\"({url:location.href,entry:window.__fsEntryHash,lang:document.documentElement.lang,storage:Object.fromEntries(Object.entries(localStorage))})\"),ensure_ascii=False,indent=2));page.wait_for_url"""
if needle not in s:raise RuntimeError('Final route check changed')
p.write_text(s.replace(needle,replacement,1))
# Align the requested card after the reader's initial animated scroll settles.
p=root/'language.js';s=p.read_text()
start=s.index('function restoreEntry(){');end=s.index('// Preserve the logical slide',start)
s=s[:start]+'''function restoreEntry(){
 const entry=window.__fsEntryHash;
 if(!entry||!document.querySelector('section.slide')||new URL(location.href).searchParams.has('lang'))return;
 let cancelled=false;
 const cancel=()=>{cancelled=true};
 const inputs=['wheel','touchstart','pointerdown','keydown'];
 inputs.forEach(type=>window.addEventListener(type,cancel,{once:true,passive:true}));
 const duration=Number(document.body.getAttribute('data-lwp-scroll-duration'))||200;
 Promise.resolve(document.fonts?.ready).then(()=>setTimeout(()=>{
  inputs.forEach(type=>window.removeEventListener(type,cancel));
  if(cancelled)return;
  let id;try{id=decodeURIComponent(entry.slice(1))}catch{return}
  const target=document.getElementById(id);
  if(!target)return;
  // Fractional layout must not leave the preceding card at the viewport edge.
  const top=Math.ceil(target.getBoundingClientRect().top+window.scrollY)+2;
  window.scrollTo({top:top,left:0,behavior:'instant'});
  if(location.hash!==entry)history.replaceState(history.state,'',location.pathname+location.search+entry);
  refresh();
 },Math.min(Math.max(duration,0),2000)+100));
}
if(document.readyState==='complete')restoreEntry();else window.addEventListener('load',restoreEntry,{once:true});
''' + s[end:]
p.write_text(s)
