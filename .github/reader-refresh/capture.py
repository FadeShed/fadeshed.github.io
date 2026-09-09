#!/usr/bin/env python3
"""Make two real viewport captures of the public example for each edition."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import argparse,io,zipfile
from qa import serve
from build import refresh_manifest

def run(output,root):
    server,base=serve(output)
    try:
        with sync_playwright() as p:
            b=p.chromium.launch(headless=True)
            for lang,prefix in [('en',''),('fr','fr/')]:
                shots=[]
                for width,height,anchor in [(1280,800,'opening'),(390,844,'purpose')]:
                    ctx=b.new_context(viewport={'width':width,'height':height},has_touch=True)
                    page=ctx.new_page();page.goto(base+prefix+'lightwebpres/demo/library.html#'+anchor,wait_until='networkidle')
                    page.add_style_tag(content='.fs-utility,.nav-controls{visibility:hidden!important}html{scroll-behavior:auto!important}')
                    page.evaluate('(id)=>{let e=document.getElementById(id);window.scrollTo(0,Math.ceil(e.getBoundingClientRect().top+scrollY)+2)}',anchor)
                    page.wait_for_timeout(250);shots.append(Image.open(io.BytesIO(page.screenshot())).convert('RGB'));ctx.close()
                canvas=Image.new('RGB',(1100,780),'#10161f');draw=ImageDraw.Draw(canvas)
                desktop=shots[0].resize((920,575),Image.Resampling.LANCZOS);phone=shots[1].resize((256,554),Image.Resampling.LANCZOS)
                draw.rounded_rectangle((30,61,966,652),radius=14,fill='#3b4c5b');canvas.paste(desktop,(38,69))
                draw.rounded_rectangle((806,145,1078,715),radius=22,fill='#607383');canvas.paste(phone,(814,153))
                dest=output/(prefix+'lightwebpres/img/reader-preview.webp');canvas.save(dest,quality=92)
                src=root/'.github/bilingual/lwp'/lang/'sources/img/reader-preview.webp';src.write_bytes(dest.read_bytes())
                # Match the downloadable editable source to the illustration that is published.
                zpath=output/(prefix+'lightwebpres/downloads/site-sources.zip')
                with zipfile.ZipFile(zpath) as z:entries=[(n,z.read(n)) for n in z.namelist() if n!='sources/img/reader-preview.webp']
                with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
                    for name,data in entries:z.writestr(name,data)
                    z.writestr('sources/img/reader-preview.webp',dest.read_bytes())
            b.close()
        refresh_manifest(output)
    finally:server.shutdown()
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('output',type=Path);ap.add_argument('root',type=Path);a=ap.parse_args();run(a.output.resolve(),a.root.resolve())
