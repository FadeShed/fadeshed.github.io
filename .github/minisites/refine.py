#!/usr/bin/env python3
"""Apply reviewed responsive and sandbox-adapter fixes to publication sources."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=ROOT/'harmonize.py'
s=p.read_text()
needle="CSS = '''/* Shared navigation, not a shared product theme. */"
replacement=needle+'''
body.fs-fileshed .hero>*,body.fs-fileshed .section-head>*,body.fs-fileshed .workflow-grid>*,body.fs-fileshed .engineering>*,body.fs-fileshed .legacy-grid>*{min-width:0}
body.fs-fileshed pre{max-width:100%}
@media(max-width:440px){body.fs-fileshed .hero h1{font-size:clamp(3.6rem,18vw,4.8rem)}body.fs-fileshed .deliverable>div{min-width:0}body.fs-fileshed .deliverable strong{overflow-wrap:anywhere}}
'''
if s.count(needle)!=1: raise RuntimeError('Expected stylesheet source')
s=s.replace(needle,replacement,1)
needle="    (dest/'demo.html').write_text(demo)"
replacement='''    # A remembered Overview group has no tab-zone links. Wait for group tabs,
    # choose Projects, then announce readiness. This also makes Reset reliable.
    old="const timer=setInterval(()=>{if(document.querySelector('.tab-zone-link')){clearInterval(timer);focus();parent.postMessage({type:'pb-demo-ready'},'*');}},60);"
    new="const timer=setInterval(()=>{if(!document.querySelector('.group-tab'))return;focus();if(!document.querySelector('.tab-zone-link'))return;clearInterval(timer);parent.postMessage({type:'pb-demo-ready'},'*');},60);"
    if demo.count(old)!=1: raise ValueError('Expected embedded adapter startup')
    demo=demo.replace(old,new,1)
    adapter=dest/'assets/demo-adapter.js'
    adapter_text=adapter.read_text()
    if adapter_text.count(old)!=1: raise ValueError('Expected standalone adapter startup')
    adapter.write_text(adapter_text.replace(old,new,1))
    (dest/'demo.html').write_text(demo)'''
if s.count(needle)!=1: raise RuntimeError('Expected demo write')
p.write_text(s.replace(needle,replacement,1))
p=ROOT/'qa.py';s=p.read_text()
needle="                    check(f'No overflow {product or \"home\"} {width}',page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'))"
replacement='''                    overflow=page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                    if overflow:
                        page.screenshot(path=str(report/f'overflow-{product.strip("/") or "home"}-{width}.png'),full_page=True)
                        detail=page.evaluate("""Array.from(document.querySelectorAll('body *')).filter(e=>{const r=e.getBoundingClientRect();return r.width&&r.right>innerWidth+1}).map(e=>({tag:e.tagName,class:e.className,w:e.getBoundingClientRect().width,right:e.getBoundingClientRect().right,text:e.textContent.slice(0,80)})).slice(0,25)""")
                    else: detail=[]
                    check(f'No overflow {product or "home"} {width}',not overflow,detail)'''
if s.count(needle)!=1: raise RuntimeError('Expected viewport check')
s=s.replace(needle,replacement,1)
needle='    finally:\n        if server: server.shutdown()'
replacement='''    except Exception as exc:
        import traceback
        (report/'failure.txt').write_text(traceback.format_exc())
        results.append({'check':'Complete browser workflow','passed':False,'detail':str(exc)})
        raise
    finally:
        if server: server.shutdown()'''
if s.count(needle)!=1: raise RuntimeError('Expected report finalizer')
p.write_text(s.replace(needle,replacement,1))
