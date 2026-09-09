/* Compare actual renderings. No replacement for LightWebPres' native appearance menu. */
(() => {
 function enhance() {
  const root=document.querySelector('.proposal-home'); if(!root)return;
  const buttons=[...root.querySelectorAll('[data-choice]')];
  const panels=[...root.querySelectorAll('[data-panel]')];
  const controls=root.querySelector('.pv-identity-controls');if(!controls||!buttons.length)return;
  controls.style.display='flex';
  const select=(value)=>{
   for(const button of buttons)button.setAttribute('aria-pressed',String(button.dataset.choice===value));
   for(const panel of panels)panel.hidden=panel.dataset.panel!==value;
  };
  buttons.forEach((button,index)=>{
   button.addEventListener('click',event=>{event.stopPropagation();select(button.dataset.choice)});
   button.addEventListener('keydown',event=>{
    if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
    event.preventDefault();event.stopPropagation();
    const next=event.key==='Home'?0:event.key==='End'?buttons.length-1:(index+(event.key==='ArrowRight'?1:-1)+buttons.length)%buttons.length;
    select(buttons[next].dataset.choice);buttons[next].focus();
   });
  });
  select('native');
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhance,{once:true});else enhance();
})();
