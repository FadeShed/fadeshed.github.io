/* Restore the workshop breadcrumb when a LightWebPres preset rerenders it. */
(() => {'use strict';
const script=document.currentScript,root=new URL('../',script.src),home=root.href;
function crumb(){
 const wrap=document.createElement('div');wrap.className='fs-breadcrumb';wrap.setAttribute('role','navigation');wrap.setAttribute('aria-label','Breadcrumb');
 const a=document.createElement('a');a.className='fs-home';a.href=home;a.setAttribute('aria-label','FadeShed home');
 const img=document.createElement('img');img.src=new URL('assets/fadeshed-mark.webp',root).href;img.alt='';img.width=32;img.height=30;
 const name=document.createElement('span');name.append('Fade');const strong=document.createElement('strong');strong.textContent='Shed';name.append(strong);a.append(img,name);wrap.append(a);
 const slash=document.createElement('span');slash.className='fs-separator';slash.setAttribute('aria-hidden','true');slash.textContent='/';wrap.append(slash);
 const current=document.createElement('a');current.className='fs-product';current.href=new URL('lightwebpres/',root).href;current.textContent='LightWebPres';wrap.append(current);
 const badge=document.createElement('span');badge.className='fs-status';badge.textContent='Beta';wrap.append(badge);return wrap;
}
function refresh(){document.querySelectorAll('.lwp-web-nav > .lwp-web-brand').forEach(a=>a.replaceWith(crumb()));}
refresh();let queued=false;
new MutationObserver(()=>{if(queued)return;queued=true;requestAnimationFrame(()=>{queued=false;refresh()})}).observe(document.body,{childList:true,subtree:true});
})();
