#!/usr/bin/env python3
"""Refresh the public portal from a pinned upstream renderer and bilingual sources."""
from pathlib import Path
import argparse,base64,hashlib,importlib.util,json,os,re,shutil,subprocess,sys,zipfile
from bs4 import BeautifulSoup, NavigableString
HERE=Path(__file__).resolve().parent
LWP_REV='ec24ec481ee3b0083cb520398d4bea82885df8bf'
ENGINE_SHA='7e63cf4b13882f1318a5a9630bbe389cd9d2b71a583790e9021604aba321f250'
PUBLIC=['.nojekyll','README.md','index.html','index.md','llms.txt','style.css','assets','fileshed','pasteberth','lightwebpres','fr']

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def copytree(src,dst):
    if src.is_symlink() or any(p.is_symlink() for p in src.rglob('*')):raise ValueError('Symlink in input')
    shutil.copytree(src,dst,dirs_exist_ok=True)

def run(engine,*args,env=None):
    e=os.environ.copy();e.update(env or {});e['TMPDIR']=str(engine.parent/'work/tmp');Path(e['TMPDIR']).mkdir(parents=True,exist_ok=True)
    c=subprocess.run([sys.executable,str(engine),*map(str,args)],env=e,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
    print(c.stdout[-1800:],flush=True)
    if c.returncode:raise RuntimeError('LWP command failed: '+repr(args)+'\n'+c.stdout)

def audit_demo(engine,series,locale):
    c=subprocess.run([sys.executable,str(engine),'audit',str(series),'--lang',locale],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
    print(c.stdout,flush=True)
    warnings=[x for x in c.stdout.splitlines() if x.startswith('[WARNING]')]
    if c.returncode or any('library.md: slide 4 (comparison), table 1: ESTIMATE' not in x for x in warnings):raise RuntimeError('Unexpected demo audit finding: '+c.stdout)

def writejson(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def zipdir(dest,root):
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file() and not p.is_symlink() and not any(x.startswith('.lwp-') or x=='__pycache__' for x in p.parts):z.write(p,p.relative_to(root))

def clean_html(s,locale):
    for x in list(s.select('.version-tag,.build-stamp,.brand-version')):x.decompose()
    for stamp in s.select('.help-stamp'):
        for text in list(stamp.find_all(string=True,recursive=False)):
            if re.search(r'\bv?\d+\.\d+\.\d+',str(text)):text.extract()
    # Editorial source numbers are not rewritten inside code, licenses or kit identifiers.
    for text in list(s.find_all(string=True)):
        if text.find_parent(['script','style','pre','code']):continue
        val=str(text)
        if re.search(r'(?:LightWebPres|Moteur|Engine)\s*v?0\.\d+\.\d+',val):
            text.replace_with(re.sub(r'(LightWebPres|Moteur|Engine)\s*v?0\.\d+\.\d+',r'\1',val))
    for a in s.select('a[href="build-info.json"]'):
        a['href']='https://github.com/Fade78/lightwebpres';a.string='Projet LightWebPres' if locale=='fr' else 'LightWebPres project'
    return s

def guide_sources(root,locale,ed):
    target=HERE/'guide-source'/locale
    if (target/'guide.md').exists():return target
    target.mkdir(parents=True,exist_ok=True)
    s=BeautifulSoup((root/('fr' if locale=='fr' else '')/'lightwebpres/guide/guide.html').read_text(),'html.parser')
    title='Guide de LightWebPres' if locale=='fr' else 'LightWebPres guide'
    text=ed.meta(title,'Lire, créer et publier.' if locale=='fr' else 'Read, create and publish.','GUIDE')
    for sec in s.select('section.slide'):
        slug=sec.get('id');classes=sec.get('class',[])
        if 'slide-series-nav' in classes:continue
        content=sec.select_one('.lwp-doc-content')
        if content is None:raise ValueError('Missing guide content for '+str(slug))
        for node in content.select('.fs-reference-lang'):node.decompose()
        if 'full-article' in classes:
            for node in content.select('.slide-kicker'):node.decompose()
            (target/'article.md').write_text(content.decode_contents())
            continue
        heading=content.find(['h1','h2']);heading_text=heading.decode_contents() if heading else title
        if heading:heading.decompose()
        kicker=content.select_one('.slide-kicker');kicker_text=kicker.get_text(' ',strip=True) if kicker else ''
        if kicker:kicker.decompose()
        summary=content.select_one('.summary');summary_text=summary.decode_contents() if summary else ''
        if summary:summary.decompose()
        text+=ed.slide(slug,heading_text,summary_text,content.decode_contents(),kind='cover' if 'slide-cover' in classes else '',kicker=kicker_text)
    text+=ed.slide('reader-controls','La lecture, à votre échelle.' if locale=='fr' else 'Reading, at your scale.',
        'Touchez le menu du lecteur : le zoom ne nécessite pas de clavier.' if locale=='fr' else 'Tap the reader menu: zoom does not require a keyboard.',
        ('Utilisez **−**, **+** et **Réinitialiser** pour le zoom de présentation ; le pourcentage indique son niveau. Le pincement reste le zoom natif du navigateur. Le menu propose aussi l’ajustement du texte et le défilement local des tableaux larges. Ces choix durent dans la page chargée, pas après son rechargement. Les cellules restent dans le document : la coupure visuelle ne supprime pas leur contenu.' if locale=='fr' else 'Use **−**, **+** and **Reset** for presentation zoom; the percentage shows its level. Pinch remains native browser zoom. The menu also offers text fitting and local scrolling for wide tables. These choices last in the loaded page, not after reloading it. Table cells remain in the document: visual clipping does not remove their content.'))
    text+='<!-- lwp:slide:full-article -->\nslug: guide-complet\narticle: article.md\n\n---\n\n<!-- lwp:slide:series-nav -->\nslug: la-serie\n'
    (target/'guide.md').write_text(text)
    article=(target/'article.md').read_text();note='<section id="reader-controls-detail"><h2>'+('Contrôles de lecture au toucher' if locale=='fr' else 'Touch reader controls')+'</h2><p>'+('Le menu du lecteur donne accès aux boutons de zoom − / + / Réinitialiser, au pourcentage, à l’ajustement du texte et au défilement local des tableaux. Aucun clavier n’est nécessaire pour ces commandes. Le pincement appartient au navigateur. Les choix de lecture sont propres à la page chargée.' if locale=='fr' else 'The reader menu provides zoom − / + / Reset, the current percentage, text fitting and local table scrolling. These controls do not require a keyboard. Pinch belongs to the browser. Reading choices belong to the currently loaded page.')+'</p></section>'
    (target/'article.md').write_text(note+article)
    return target

def build_guide(root,upstream,engine,dest,locale,tmp,b,ed):
    source=guide_sources(root,locale,ed);series=tmp/('guide-'+locale)
    run(engine,'init',series,'--preset','lightwebpres-docs@0.1.0/docs','--lang',locale,env={'LWP_IDENTITY_KITS_DIR':str(upstream/'examples/kits')})
    for f in ['guide.md','article.md']:shutil.copyfile(source/f,series/'sources'/f)
    copytree(root/('fr' if locale=='fr' else '')/'lightwebpres/guide/img',series/'sources/img')
    conf={'series_meta':{'title':'LightWebPres','subtitle':'Le guide' if locale=='fr' else 'The guide','presentation_preset':'lightwebpres-docs@0.1.0/docs','scroll_duration':0},'articles':[{'page_source':'guide.md','page_dest':'guide.html'}]}
    writejson(series/'series.json',conf)
    # Keep the already translated long-form manual; rebuild its reader and revise reading guidance.
    if locale=='fr':
        for p in (series/'templates/kits').rglob('*.html'):
            x=BeautifulSoup(p.read_text(),'html.parser');b.text_translate(x,b.read_json(b.HERE/'translations/guide-ui-fr.json'));p.write_text(str(x))
    run(engine,'build',series,'--lang',locale,'--output',dest/'guide')
    run(engine,'verify',series,'--lang',locale,'--output',dest/'guide')
    return series

def main(root,upstream,output):
    root=root.resolve();upstream=upstream.resolve();output=output.resolve()
    if output.exists():raise ValueError('Output must be new')
    engine=upstream/'lightwebpres'
    if hashlib.sha256(engine.read_bytes()).hexdigest()!=ENGINE_SHA:raise ValueError('Unexpected renderer bytes; review before rebuilding')
    output.mkdir(parents=True)
    for name in PUBLIC:
        src=root/name
        if src.is_dir():copytree(src,output/name)
        elif src.is_file():shutil.copyfile(src,output/name)
    b=module('bilingual',root/'.github/bilingual/build.py');ed=module('editorial',HERE/'editorial.py')
    work=HERE/'work'
    if work.exists():shutil.rmtree(work)
    work.mkdir()
    source_root=work/'sources'
    if source_root.exists():shutil.rmtree(source_root)
    copytree(root/'.github/bilingual/lwp',source_root);ed.apply(source_root);ed.specimen(source_root)
    native_results=[]
    for locale,prefix in [('en',''),('fr','fr')]:
        edition=output/prefix;dest=edition/'lightwebpres';series=source_root/locale
        img=series/'sources/img';img.mkdir(exist_ok=True)
        for name in ['product-responsive.png','themes-featured.png']:shutil.copyfile(upstream/'generated'/name,img/name)
        # Temporary preview is replaced by real paired browser captures after building.
        from PIL import Image
        Image.open(upstream/'generated/product-responsive.png').convert('RGB').save(img/'reader-preview.webp',quality=90)
        # Clean stale cache files in the disposable series only.
        for p in series.rglob('.lwp-*'):
            if p.is_file():p.unlink()
        run(engine,'build',series,'--lang',locale,'--output',dest)
        run(engine,'audit',series,'--lang',locale,'--strict');run(engine,'verify',series,'--lang',locale,'--output',dest)
        example=series/'example'
        for name in ['lightwebpres','COPYING','COPYING.EXCEPTION','THIRD-PARTY-NOTICES.md']:shutil.copyfile(upstream/name,example/name)
        run(engine,'build',example,'--lang',locale,'--output',dest/'demo');audit_demo(engine,example,locale);run(engine,'verify',example,'--lang',locale,'--output',dest/'demo')
        copytree(dest/'demo',example/'public')
        zipdir(dest/'downloads/demarrage.zip',example);zipdir(dest/'downloads/library-project.zip',example)
        build_guide(root,upstream,engine,dest,locale,work,b,ed)
        run(engine,'theme','gallery',dest/'themes.html','--lang',locale)
        # Current original source references, legal notices, agent skills and browser support files.
        for name in ['README.md','GUIDE.md','GLOSSARY.md','specifications.md','AGENTS.md','DECISIONS.md','CHANGELOG.md','COPYING','COPYING.EXCEPTION','THIRD-PARTY-NOTICES.md']:
            if (upstream/name).exists():shutil.copyfile(upstream/name,dest/'reference'/name)
        copytree(upstream/'agent/skills',dest/'reference/agent/skills')
        for name in ['app.py','git_sync.py','index.html','lwp_banner.svg','lwp_logo_icon.svg']:shutil.copyfile(upstream/'web'/name,dest/'web'/name)
        copytree(upstream/'web/vendor',dest/'web/vendor')
        for name in ['lightwebpres','COPYING','COPYING.EXCEPTION','THIRD-PARTY-NOTICES.md']:shutil.copyfile(upstream/name,dest/'web'/name)
        pack=work/('cli-'+locale);pack.mkdir(exist_ok=True)
        for name in ['lightwebpres','COPYING','COPYING.EXCEPTION','THIRD-PARTY-NOTICES.md']:shutil.copyfile(upstream/name,pack/name)
        zipdir(dest/'downloads/lightwebpres-cli.zip',pack);zipdir(dest/'downloads/skills.zip',upstream/'agent/skills')
        # Source archive remains reconstructible with the current engine.
        (series/'build-site.py').write_text('import subprocess,sys\nsubprocess.run([sys.executable,"lightwebpres","build",".","--lang","'+locale+'"],check=True)\n')
        shutil.copyfile(engine,series/'lightwebpres');shutil.copyfile(upstream/'COPYING',series/'COPYING');shutil.copyfile(upstream/'COPYING.EXCEPTION',series/'COPYING.EXCEPTION')
        zipdir(dest/'downloads/site-sources.zip',series)
        for page in sorted(dest.rglob('*.html')):
            if 'reference' in page.relative_to(dest).parts:continue
            rel=page.relative_to(edition).as_posix();s=BeautifulSoup(page.read_text(),'html.parser')
            # Skip example files generated from extracted raw HTML only as references, not readers.
            if not s.html or not s.body:continue
            if rel=='lightwebpres/themes.html' and locale=='fr':b.text_translate(s,b.read_json(b.HERE/'translations/gallery-fr.json'))
            if rel=='lightwebpres/web/index.html':b.builder_translate(s,locale)
            if rel.startswith('lightwebpres/guide/') and locale=='fr':b.text_translate(s,b.read_json(b.HERE/'translations/guide-ui-fr.json'))
            s=clean_html(b.decorate(s,rel,locale),locale)
            if s.select_one('section.slide'):
                css=s.new_tag('link',attrs={'rel':'stylesheet','href':'/assets/reader-site.css'});s.head.append(css)
                js=s.new_tag('script',src='/assets/reader-site.js',defer=True);s.body.append(js)
            page.write_text(str(s))
        info={'renderer_commit':LWP_REV,'renderer_sha256':ENGINE_SHA,'language':locale,'editorial_source':'.github/reader-refresh','native_portal_strict_audit':True,'native_demo_warnings':['intentional scrollable comparison table width estimate'],'guide_regenerated':True}
        writejson(dest/'build-info.json',info);native_results.append(info)
        # Keep the documentation indexes evergreen; source repositories retain exact technical history.
        overview=f'''# LightWebPres\n\n> {('Des documents à lire, à présenter et à partager. Des sources modifiables pour créer, organiser, concevoir et automatiser.' if locale=='fr' else 'Documents to read, present and share. Editable sources to write, organize, design and automate.')}\n\n{('Statut : **Bêta**.' if locale=='fr' else 'Status: **Beta**.')}\n\n'''
        for r in ed.ROLES:overview+='## '+(r[2] if locale=='fr' else r[1])+'\n\n'+(r[8] if locale=='fr' else r[7])+'\n\n'
        overview+=('## Pour commencer\n\n' if locale=='fr' else '## Start here\n\n')
        links=[('index.html','LightWebPres'),('usages.html','Usages' if locale=='fr' else 'Use cases'),('demo/library.html','Dossier interactif' if locale=='fr' else 'Interactive briefing'),('demarrer.html','Créer' if locale=='fr' else 'Create'),('guide/guide.html','Guide'),('web/','Constructeur navigateur' if locale=='fr' else 'Browser builder')]
        for url,label in links:overview+=f'- [{label}]({url})\n'
        (dest/'index.md').write_text(overview)
        llms=f'# LightWebPres\n\n> '+('Outil de génération de pages à lire, présenter et publier à partir de sources Markdown. Bêta.','Markdown-based documents for reading, presentation and static publishing. Beta.')[locale=='en']+'\n\n'
        llms+=('Le lecteur utilise son navigateur. Le constructeur web et le CLI utilisent le même moteur ; l’agent de rédaction et l’hébergement sont externes. Les tags filtrent des contenus rédigés, ils ne traduisent pas et ne contrôlent pas les accès. Les notes sont publiées ; le moteur n’est pas un assainisseur HTML.\n\n' if locale=='fr' else 'Readers use their browser. The web builder and CLI share the same engine; authoring agents and hosting are external. Tags filter authored content, not translate it or control access. Notes are published; the engine is not an HTML sanitizer.\n\n')
        llms+='## '+('Parcours' if locale=='fr' else 'Routes')+'\n\n'
        for url,label in [('index.md','Overview' if locale=='en' else 'Présentation')]+links:llms+=f'- [{label}](https://fadeshed.github.io/{prefix+"/" if prefix else ""}lightwebpres/{url})\n'
        llms+='\n## '+('Références techniques originales' if locale=='fr' else 'Original technical references')+'\n\n'
        for n in ['README.md','GUIDE.md','GLOSSARY.md','agent/skills/lightwebpres/SKILL.md']:llms+=f'- [{n}](https://raw.githubusercontent.com/Fade78/lightwebpres/main/{n})\n'
        (dest/'llms.txt').write_text(llms)
        for p in dest.rglob('.lwp-*'):
            if p.is_file():p.unlink()
    # Export source material separately from generated runtime. No old nav.js overrides.
    for locale in ['en','fr']:
        target=root/'.github/bilingual/lwp'/locale
        copytree(source_root/locale,target)
        for n in ['lightwebpres','build-site.py','COPYING','COPYING.EXCEPTION']:
            q=target/n
            if q.exists():q.unlink()
        if (target/'example/public').exists():shutil.rmtree(target/'example/public')
        for n in ['lightwebpres','COPYING','COPYING.EXCEPTION','THIRD-PARTY-NOTICES.md']:
            q=target/'example'/n
            if q.exists():q.unlink()
    for p in (root/'.github/bilingual/lwp').rglob('.lwp-*'):
        if p.is_file():p.unlink()
    for edition in [output,output/'fr']:
        shutil.copyfile(HERE/'reader-site.css',edition/'assets/reader-site.css');shutil.copyfile(HERE/'reader-site.js',edition/'assets/reader-site.js')
        # Finish the outstanding sandbox integration without weakening its network policy.
        p=edition/'pasteberth/demo.html';s=BeautifulSoup(p.read_text(),'html.parser')
        for n in list(s.select('link[rel="stylesheet"]')):
            if 'assets/minisites.css' in n.get('href',''):
                style=s.new_tag('style');style.string=(edition/'assets/minisites.css').read_text();n.replace_with(style)
        for n in list(s.select('script[src]')):
            if 'assets/minisites.js' in n.get('src',''):
                script=s.new_tag('script');script.string=(edition/'assets/minisites.js').read_text();n.replace_with(script)
        for im in s.select('.fs-utility img'):im['src']='data:image/webp;base64,'+base64.b64encode((edition/'assets/fadeshed-mark.webp').read_bytes()).decode()
        p.write_text(str(clean_html(s,'fr' if edition==output/'fr' else 'en')))
    from evergreen import update_public_docs
    update_public_docs(output)
    writejson(HERE/'engine-lock.json',{'repository':'Fade78/lightwebpres','commit':LWP_REV,'sha256':ENGINE_SHA})
    writejson(HERE/'native-checks.json',native_results)
    refresh_manifest(output)
    print('REFRESH_READY',str(output),flush=True)

def refresh_manifest(output):
    data={'schema':1,'default_language':'en','french_prefix':'/fr/','engine_sha256':ENGINE_SHA,'files':{p.relative_to(output).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in output.rglob('*') if p.is_file() and p.relative_to(output).as_posix()!='assets/bilingual-manifest.json'}}
    writejson(output/'assets/bilingual-manifest.json',data)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--upstream',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();main(a.root,a.upstream,a.output)
