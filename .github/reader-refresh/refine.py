#!/usr/bin/env python3
"""Refine touch reader integration and exercise the native modal dismissal."""
from pathlib import Path
root=Path(__file__).resolve().parent
p=root/'qa.py';s=p.read_text()
for old,new in [
 ("page.locator('#navMenu').click()", "page.locator('#presenterMenu').click(position={'x':4,'y':4});expect(page.locator('#presenterMenu')).not_to_be_visible()"),
 ("page.locator('#navMenu').tap()", "page.locator('#presenterMenu').tap(position={'x':4,'y':4});expect(page.locator('#presenterMenu')).not_to_be_visible()")
]:
 if s.count(old)!=1:raise RuntimeError('Expected one native backdrop check: '+old)
 s=s.replace(old,new,1)
needle="                expect(page.locator('.fs-reader-open')).to_be_visible();page.locator('.fs-reader-open').tap();"
replacement="""                expect(page.locator('.fs-reader-open')).to_be_visible()
                check('Touch entry does not overlap native navigation '+lang,page.evaluate(\"\"\"()=>{const a=document.querySelector('.fs-reader-open').getBoundingClientRect(),b=document.querySelector('#navMenu').getBoundingClientRect();return !b.width||a.right<=b.left||b.right<=a.left||a.bottom<=b.top||b.bottom<=a.top}\"\"\"))
                page.locator('.fs-reader-open').tap();"""
if s.count(needle)!=1:raise RuntimeError('Expected one touch entry check')
p.write_text(s.replace(needle,replacement,1))
p=root/'reader-site.css';s=p.read_text()
needle='.fs-reader-open{position:fixed;right:16px;'
if s.count(needle)!=1:raise RuntimeError('Expected one reader entry position')
p.write_text(s.replace(needle,'.fs-reader-open{position:fixed;right:80px;',1))
