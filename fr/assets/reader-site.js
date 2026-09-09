/* A visible site entry point to the native reader menu, including on touch screens. */
(()=>{'use strict';
const menu=document.querySelector('#presenterMenu');
if(!menu)return;
const locale=document.documentElement.lang;
const button=document.createElement('button');button.type='button';button.className='fs-reader-open';
button.textContent=locale==='fr'?'Lecture & zoom':'Reading & zoom';
button.setAttribute('aria-controls','presenterMenu');button.setAttribute('aria-haspopup','dialog');
button.addEventListener('click',()=>{
 const native=document.querySelector('#navMenu,[aria-controls="presenterMenu"]:not(.fs-reader-open)');
 if(native)native.click();
});
document.body.append(button);
})();
