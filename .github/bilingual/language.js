/* Static bilingual editions: explicit URLs, no browser or stored-language inference. */
(()=>{'use strict';
const doc=document.documentElement,locale=doc.dataset.fsLocale||'en',page=doc.dataset.fsPage||'index.html';
const prefix=locale==='fr'?'/fr/':'/',product=page.split('/')[0];
const productName={fileshed:'FileShed',pasteberth:'Pasteberth',lightwebpres:'LightWebPres'}[product];
function languageSwitch(){
 const nav=document.createElement('nav');nav.className='fs-language';nav.setAttribute('aria-label',locale==='fr'?'Langue':'Language');
 for(const l of ['en','fr']){if(l==='fr'){const sep=document.createElement('span');sep.setAttribute('aria-hidden','true');sep.textContent='|';nav.append(sep)}
 const a=document.createElement('a');a.dataset.fsLang=l;a.lang=l;a.hreflang=l;a.href=(l==='fr'?'/fr/':'/')+page.replace(/index\.html$/,'');a.textContent=l.toUpperCase();a.setAttribute('aria-label',l==='fr'?'Français':'English');if(l===locale)a.setAttribute('aria-current','true');nav.append(a)}return nav;
}
function crumb(){const d=document.createElement('div');d.className='fs-breadcrumb fs-on-dark';d.setAttribute('role','navigation');d.setAttribute('aria-label',locale==='fr'?'Fil d’Ariane':'Breadcrumb');
 const a=document.createElement('a');a.className='fs-home';a.href=prefix;a.setAttribute('aria-label',locale==='fr'?'Accueil FadeShed':'FadeShed home');
 const im=document.createElement('img');im.src='/assets/fadeshed-mark.webp';im.alt='';im.width=32;im.height=30;
 const text=document.createElement('span');text.append('Fade');const st=document.createElement('strong');st.textContent='Shed';text.append(st);a.append(im,text);d.append(a);
 const slash=document.createElement('span');slash.className='fs-separator';slash.textContent='/';slash.setAttribute('aria-hidden','true');d.append(slash);
 const p=document.createElement('a');p.className='fs-product';p.href=prefix+product+'/';p.textContent=productName;d.append(p);return d;
}
function refresh(){
 document.querySelectorAll('.lwp-web-nav').forEach(h=>{const b=h.querySelector(':scope>.lwp-web-brand');if(b)b.replaceWith(crumb());if(!h.querySelector(':scope>.fs-language'))h.append(languageSwitch());});
 document.querySelectorAll('[data-fs-lang]').forEach(a=>{
  const target=new URL(a.href,location.href);const query=new URL(location.href).searchParams;query.delete('lang');target.search=query.toString();target.hash=location.hash;a.href=target.href;
 });
}
refresh();window.addEventListener('hashchange',refresh);
function restoreEntry(){
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
// Preserve the logical slide even when the reader has not written a URL fragment.
document.addEventListener('click',e=>{const a=e.target.closest('a[data-fs-lang]');if(!a)return;
 const u=new URL(a.href);if(!location.hash){const slides=Array.from(document.querySelectorAll('section.slide[id]')).filter(x=>!x.hidden&&getComputedStyle(x).display!=='none');const visible=slides.filter(x=>{const r=x.getBoundingClientRect();return r.bottom>90&&r.top<innerHeight});visible.sort((x,y)=>Math.abs(x.getBoundingClientRect().top)-Math.abs(y.getBoundingClientRect().top));if(visible[0])u.hash=visible[0].id}a.href=u.href;
},true);
let queued=false;new MutationObserver(()=>{if(queued)return;queued=true;requestAnimationFrame(()=>{queued=false;refresh()})}).observe(document.body,{childList:true,subtree:true});
})();
