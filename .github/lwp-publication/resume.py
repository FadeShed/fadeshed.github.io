#!/usr/bin/env python3
"""Recover an approved static publication from verified, immutable inputs."""
import argparse, base64, functools, hashlib, http.server, io, json, re, shutil
import subprocess, tarfile, threading, zipfile, zlib
from pathlib import Path, PurePosixPath
PACKED_SHA='647d66833451d467aa9cdf5aefedd366e0f4d65bbd575e25a39229d2e213eb2b'
TAR_SHA='b9f5b9b3cb9d27e2d2eedad41503f4bd7f20d7701de9cd5af7aa3cd7d7f59574'
DICT_SHA='050779f2bfc4d74b4bad3dc3ca18f6d8a72afee4507f200bd5ebb6f328bd0a59'
APPROVED_SHA='db3a8b0f9599e158b7dcc8ab67e364c9878d44d6e1a948a044ec88042e06356c'
ROOTS={'site':'75f146e3c0c6bdf74818c71afc4b9a84e35d1545','upstream':'a5350feee396cafed54bb1328d460659e8e7df69'}

def digest(data):return hashlib.sha256(data).hexdigest()

def safe(root,name):
    path=PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts:raise ValueError('Unsafe path: '+name)
    p=root/name
    if not p.resolve().is_relative_to(root.resolve()) or p.is_symlink():raise ValueError('Unsafe destination')
    return p

def read_ref(roots,which,name):
    if '!' in name:
        name,member=name.split('!',1)
        with zipfile.ZipFile(safe(roots[which],name)) as z:return z.read(member)
    return safe(roots[which],name).read_bytes()

def recover(root,roots,work):
    source=root/'.github/lwp-publication'
    first=(source/'part-01.txt').read_text()
    meta=json.loads(first[:first.index(',"payload":')]+'}')
    refs=json.loads(zlib.decompress(base64.b64decode(meta['dictionary'],validate=True)))
    dictionary=b''.join(read_ref(roots,r,p) for r,p in refs)
    if digest(dictionary)!=DICT_SHA:raise RuntimeError('Dictionary differs from approved immutable inputs')
    (work/'dictionary').write_bytes(dictionary)
    buf=['']*138064
    def put(at,text):
        if at<0 or at+len(text)>len(buf):raise ValueError('Invalid fragment offset')
        for i,c in enumerate(text,at):
            if buf[i] and buf[i]!=c:raise ValueError('Overlapping fragments differ')
            buf[i]=c
    put(0,first.split(',"payload":"',1)[1]);put(7017,(source/'part-02.txt').read_text())
    for i in range(1,6):put(22017+(i-1)*4500,(source/f'rest-{i:02}.txt').read_text())
    for i,at,n in [(6,44517,4218),(7,49017,4500),(8,53517,1763),(9,58017,3531),(10,62517,4500)]:
        put(at,(source/f'rest-{i:02}.txt').read_text()[:n])
    for i in range(1,13):put(67017+(i-1)*2000,(source/f'end-{i:02}.txt').read_text())
    repairs=zlib.decompress(b''.join((source/f'repair-{i}.bin').read_bytes() for i in range(1,5)))
    for patch in json.loads(repairs):put(patch['at'],patch['data'])
    if not all(buf):raise RuntimeError('Missing publication fragments')
    packed=base64.b64decode(''.join(buf),validate=True)
    if digest(packed)!=PACKED_SHA:raise RuntimeError('Publication transport hash differs')
    (work/'payload.zst').write_bytes(packed)
    subprocess.run(['zstd','-d','--long=27','--patch-from='+str(work/'dictionary'),str(work/'payload.zst'),'-o',str(work/'payload.tar')],check=True)
    if digest((work/'payload.tar').read_bytes())!=TAR_SHA:raise RuntimeError('Unpacked publication hash differs')
    with tarfile.open(work/'payload.tar') as tar:
        for member in tar:
            if not member.isfile() or not re.fullmatch(r'recipe\.json|objects/[a-f0-9]{64}',member.name):raise RuntimeError('Unexpected archive entry')
            data=tar.extractfile(member).read()
            p=safe(work,member.name);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    recipe=json.loads((work/'recipe.json').read_text())
    if recipe['approved_package_sha256']!=APPROVED_SHA or recipe['site_base']!=ROOTS['site'] or recipe['upstream_base']!=ROOTS['upstream']:raise RuntimeError('Unapproved recipe')
    if len(recipe['outputs'])!=416 or len(recipe['objects'])!=237:raise RuntimeError('Incomplete recipe')
    return recipe

def serve(root):
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
    srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root)))
    threading.Thread(target=srv.serve_forever,daemon=True).start()
    return srv,f'http://127.0.0.1:{srv.server_port}/'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('site',type=Path);ap.add_argument('upstream',type=Path);ap.add_argument('work',type=Path);ap.add_argument('--offline-approved',type=Path)
    a=ap.parse_args();root=a.root.resolve();roots={'site':a.site.resolve(),'upstream':a.upstream.resolve()};work=a.work.resolve();work.mkdir(exist_ok=False)
    recipe=recover(root,roots,work)
    out=work/'publication';out.mkdir()
    for name in ['.nojekyll','index.html','index.md','llms.txt','style.css','assets','fileshed','pasteberth','lightwebpres','fr']:
        src=root/name;dest=out/name
        if src.is_symlink() or (src.is_dir() and any(p.is_symlink() for p in src.rglob('*'))):raise RuntimeError('Unexpected input symlink')
        if src.is_dir():shutil.copytree(src,dest)
        elif src.is_file():shutil.copyfile(src,dest)
    objects=recipe['objects'];cache={};changes=[];raster=[]
    def resolve(key):
        if key in cache:return cache[key]
        d=objects[key];kind=d['kind']
        if kind=='literal':data=(work/'objects'/key).read_bytes()
        elif kind=='copy':data=read_ref(roots,d['root'],d['path'])
        elif kind=='zip-copy':
            source=safe(roots[d['root']],d['path']).read_bytes()
            if digest(source)!=d['archive_sha256']:raise RuntimeError('Wrong source ZIP')
            with zipfile.ZipFile(io.BytesIO(source)) as z:data=z.read(d['member'])
        elif kind=='zip':
            f=io.BytesIO()
            with zipfile.ZipFile(f,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
                z.comment=base64.b64decode(d.get('comment',''))
                for item in d['items']:
                    info=zipfile.ZipInfo(item['name'],tuple(item['date_time']))
                    for attr in ['compress_type','create_system','create_version','extract_version','flag_bits','volume','internal_attr','external_attr']:setattr(info,attr,item[attr])
                    for attr in ['extra','comment']:setattr(info,attr,base64.b64decode(item[attr]))
                    z.writestr(info,resolve(item['object']),compresslevel=6)
            data=f.getvalue()
        else:raise RuntimeError('Raster object not yet rendered: '+key)
        actual=digest(data)
        if actual!=key:
            if kind!='zip':raise RuntimeError('Object integrity failure '+key)
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                if z.testzip():raise RuntimeError('Damaged reconstructed ZIP')
            changes.append({'object':key,'actual':actual,'kind':'zip','reason':'Repacked with verified original members and locally rendered comparison illustrations'})
        cache[key]=data;return data
    for path,key in recipe['outputs'].items():
        if not path.startswith(('lightwebpres/','fr/lightwebpres/','.github/lwp-site/')):raise RuntimeError('Unapproved output path: '+path)
        if objects[key]['kind'] in ['render','zip']:continue
        p=safe(out,path);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(resolve(key))
    if a.offline_approved:
        for key,d in objects.items():
            if d['kind']=='render':
                name=next(p for p,k in recipe['outputs'].items() if k==key and not p.startswith('.github'))
                data=(a.offline_approved/name).read_bytes()
                if digest(data)!=key:raise RuntimeError('Approved raster mismatch')
                cache[key]=data
    else:
        from PIL import Image
        from playwright.sync_api import sync_playwright
        srv,base=serve(out)
        try:
            with sync_playwright() as pw:
                browser=pw.chromium.launch(headless=True)
                for key,d in objects.items():
                    if d['kind']!='render':continue
                    page=browser.new_page(viewport={'width':d['width'],'height':d['height']},device_scale_factor=1,locale=d['locale'])
                    response=page.goto(base+d['source']+'#travels-with-the-page',wait_until='networkidle')
                    if response.status!=200:raise RuntimeError('Missing comparison document')
                    page.evaluate('document.fonts.ready');page.wait_for_timeout(700)
                    slide=page.locator('#travels-with-the-page');slide.scroll_into_view_if_needed();page.wait_for_timeout(400)
                    if not slide.is_visible():raise RuntimeError('Comparison slide not visible')
                    raw=page.screenshot();f=io.BytesIO();Image.open(io.BytesIO(raw)).save(f,format='WEBP',quality=92,method=6);data=f.getvalue();cache[key]=data
                    (work/(key+'.webp')).write_bytes(data)
                    raster.append({'source':d['source'],'width':d['width'],'height':d['height'],'approved_sha256':key,'rendered_sha256':digest(data)})
                    page.close()
                browser.close()
        finally:srv.shutdown()
    for path,key in recipe['outputs'].items():
        p=safe(out,path);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(resolve(key))
    proof={'approved_package_sha256':APPROVED_SHA,'transport_sha256':PACKED_SHA,'payload_sha256':TAR_SHA,'dictionary_sha256':DICT_SHA,'outputs':len(recipe['outputs']),'rendered_illustrations':raster,'repacked_archives':changes,'files':{p:digest((out/p).read_bytes()) for p in recipe['outputs']},'original_files':recipe['outputs']}
    protected=[]
    for p in out.rglob('*'):
        if not p.is_file():continue
        name=p.relative_to(out).as_posix()
        if name.startswith(('lightwebpres/','fr/lightwebpres/','.github/lwp-site/')):continue
        original=root/name
        if not original.is_file() or original.read_bytes()!=p.read_bytes():raise RuntimeError('Unrelated site changed: '+name)
        protected.append(name)
    proof['unchanged_other_site_files']=len(protected)
    manifest=out/'assets/bilingual-manifest.json';m=json.loads(manifest.read_text())
    for name in proof['files']:
        if not name.startswith('.github/'):m['files'][name]=proof['files'][name]
    m['engine_sha256']=digest((out/'lightwebpres/web/lightwebpres').read_bytes())
    manifest.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
    (work/'publication-proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
    print('Recovered approved publication:',len(recipe['outputs']),'outputs;',len(protected),'unrelated files unchanged')

if __name__=='__main__':main()
