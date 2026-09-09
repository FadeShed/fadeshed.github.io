#!/usr/bin/env python3
"""Apply narrow-screen corrections to the pinned publication sources."""
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
p.write_text(s)
p=ROOT/'qa.py';s=p.read_text()
needle="                    check(f'No overflow {product or \"home\"} {width}',page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'))"
replacement='''                    overflow=page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                    if overflow:
                        page.screenshot(path=str(report/f'overflow-{product.strip("/") or "home"}-{width}.png'),full_page=True)
                        detail=page.evaluate("""Array.from(document.querySelectorAll('body *')).filter(e=>{const r=e.getBoundingClientRect();return r.width&&r.right>innerWidth+1}).map(e=>({tag:e.tagName,class:e.className,w:e.getBoundingClientRect().width,right:e.getBoundingClientRect().right,text:e.textContent.slice(0,80)})).slice(0,25)""")
                    else: detail=[]
                    check(f'No overflow {product or "home"} {width}',not overflow,detail)'''
if s.count(needle)!=1: raise RuntimeError('Expected viewport check')
p.write_text(s.replace(needle,replacement,1))
