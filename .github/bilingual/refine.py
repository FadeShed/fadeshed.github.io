#!/usr/bin/env python3
"""Refine translated layouts and demo chrome without modifying application code."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=ROOT/'language.css'
p.write_text(p.read_text()+'''
@media(max-width:520px){
 html[data-fs-page="index.html"] .hero h1{font-size:clamp(2.65rem,16.2vw,4.5rem)}
 html[data-fs-page="index.html"] .shed-rule h2{font-size:clamp(1.65rem,8vw,2.1rem);overflow-wrap:anywhere}
 html[data-fs-page="index.html"] .shed-rule>div{min-width:0}
}
''')
p=ROOT/'pasteberth-demo-fr.js';s=p.read_text()
s=s.replace(" .replace(/^Download (.+)$/,'Télécharger $1')", " .replace(/^Download (\\d+) files as ZIP$/,'Télécharger $1 fichiers en ZIP').replace(/^Download (.+)$/,'Télécharger $1')")
s=s.replace("function refresh(){",'''const css=document.createElement('style');css.textContent='.tab-zone-main:empty::before{content:"Sélectionnez une zone pour l’ouvrir"}';document.head.append(css);
const nativeConfirm=window.confirm.bind(window);
window.confirm=message=>nativeConfirm(tr(String(message))
 .replace(/^Delete (\\d+) selected files from the disk\\?$/,'Supprimer du disque les $1 fichiers sélectionnés ?')
 .replace(/^Delete (.+) from the disk\\?$/,'Supprimer $1 du disque ?')
 .replace(/^(.+) retains at most (\\d+) items\\. (?:this upload|\\d+ uploads) will remove (\\d+) oldest managed items?\\. Continue\\?$/,'$1 conserve au plus $2 fichiers. Cet envoi supprimera les $3 plus anciens fichiers gérés. Continuer ?'));
function refresh(){''')
p.write_text(s)
p=ROOT/'qa.py';s=p.read_text()
s=s.replace("if overflow:page.screenshot(path=str(report/f'overflow-{locale}-{route.strip(\"/\") or \"home\"}-{width}.png'),full_page=True)",'''if overflow:
                            page.screenshot(path=str(report/f'overflow-{locale}-{route.strip("/") or "home"}-{width}.png'),full_page=True)
                            (report/'overflow.json').write_text(json.dumps(page.evaluate("""Array.from(document.querySelectorAll('body *')).filter(e=>{let r=e.getBoundingClientRect();return r.width&&r.right>innerWidth+1}).map(e=>({tag:e.tagName,class:e.className,width:e.getBoundingClientRect().width,text:e.textContent.slice(0,120)})).slice(0,30)"""),ensure_ascii=False,indent=2))''')
p.write_text(s)
# Preserve the entry fragment through the bundled reader's initial index update.
p=ROOT/'build.py';s=p.read_text()
s=s.replace("const u=new URL(location.href), q=u.searchParams.get('lang');", "const u=new URL(location.href), q=u.searchParams.get('lang');window.__fsEntryHash=u.hash;")
p.write_text(s)
p=ROOT/'language.js';s=p.read_text()
old="refresh();window.addEventListener('hashchange',refresh);"
new="""refresh();window.addEventListener('hashchange',refresh);
function restoreEntry(){
 const entry=window.__fsEntryHash;
 if(entry&&document.querySelector('section.slide')&&!new URL(location.href).searchParams.has('lang')){
  requestAnimationFrame(()=>{
   let id;try{id=decodeURIComponent(entry.slice(1))}catch{return}
   const target=document.getElementById(id);
   if(!target)return;
   if(location.hash!==entry)history.replaceState(history.state,'',location.pathname+location.search+entry);
   target.scrollIntoView({behavior:'instant',block:'start'});
   window.dispatchEvent(new HashChangeEvent('hashchange'));
  });
 }
}
if(document.readyState==='complete')restoreEntry();else window.addEventListener('load',restoreEntry,{once:true});"""
if old not in s:raise RuntimeError('Language readiness hook changed')
p.write_text(s.replace(old,new,1))
p=ROOT/'language.css';p.write_text(p.read_text()+'''
/* Keep the edition control reachable without scrolling away from the current card. */
body:not(.lwp-index) .lwp-web-nav>.fs-language{position:fixed;top:16px;right:24px;z-index:35;background:#14171b;--fs-ink:#edf1f4}
@media(max-width:750px){body:not(.lwp-index) .lwp-web-nav>.fs-language{top:10px;right:12px}}
''')
