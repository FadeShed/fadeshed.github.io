#!/usr/bin/env python3
"""Refine reader checks using the actual modal's pointer-dismiss interaction."""
from pathlib import Path
root=Path(__file__).resolve().parent
p=root/'qa.py';s=p.read_text()
for old,new in [
 ("page.locator('#navMenu').click()", "page.locator('#presenterMenu').click(position={'x':4,'y':4});expect(page.locator('#presenterMenu')).not_to_be_visible()"),
 ("page.locator('#navMenu').tap()", "page.locator('#presenterMenu').tap(position={'x':4,'y':4});expect(page.locator('#presenterMenu')).not_to_be_visible()")
]:
 if s.count(old)!=1:raise RuntimeError('Expected one native backdrop check: '+old)
 s=s.replace(old,new,1)
p.write_text(s)
