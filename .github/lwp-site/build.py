#!/usr/bin/env python3
"""Assemble the complete portal from canonical LWP sources and tracked static assets."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
PUBLIC = ('.nojekyll', 'README.md', 'index.html', 'index.md', 'llms.txt', 'style.css',
          'assets', 'fileshed', 'pasteberth', 'lightwebpres', 'fr')
LEGAL = ('COPYING', 'COPYING.EXCEPTION', 'THIRD-PARTY-NOTICES.md')


def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def copy(src: Path, dst: Path) -> None:
    if src.is_symlink() or (src.is_dir() and any(p.is_symlink() for p in src.rglob('*'))):
        raise ValueError(f'Symlink refused: {src}')
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dst, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('.git', '__pycache__', '.lwp-*'))
    else:
        shutil.copyfile(src, dst)


def zip_project(destination: Path, project: Path) -> None:
    # Reproducible archives: no current timestamps or absolute working paths.
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p in sorted(project.rglob('*')):
            if p.is_file() and not any(x.startswith('.lwp-') or x=='__pycache__' for x in p.parts):
                if p.is_symlink():
                    raise ValueError(f'Symlink refused: {p}')
                info = zipfile.ZipInfo(p.relative_to(project).as_posix(), (2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (0o100644 << 16)
                z.writestr(info, p.read_bytes())


def build(root: Path, output: Path, evidence: Path) -> None:
    root, output, evidence = root.resolve(), output.resolve(), evidence.resolve()
    if output.exists() or output == root or output.is_relative_to(HERE):
        raise ValueError('Use a new staging directory outside the canonical sources')
    lock = json.loads((HERE/'engine-lock.json').read_text())
    engine = HERE/lock['executable']
    if digest(engine) != lock['sha256']:
        raise ValueError('Renderer differs from engine-lock.json; review the update first')
    spec = importlib.util.spec_from_file_location('site_integration', HERE/'tools/site_integration.py')
    integration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(integration)
    output.mkdir(parents=True); evidence.mkdir(parents=True, exist_ok=True)
    for name in PUBLIC:
        copy(root/name, output/name)
    checks = []
    with tempfile.TemporaryDirectory(prefix='lwp-build-') as temp:
        work = Path(temp)
        env = os.environ.copy()
        env.update({'TMPDIR': temp, 'LWP_IDENTITY_KITS_DIR': str(work/'empty-kits'),
                    'LWP_THEMES_DIR': str(work/'empty-themes'), 'LWP_COMMONS_DIR': str(work/'empty-commons')})

        def command(label: str, *args: object, table_estimate: bool = False) -> None:
            result = subprocess.run([sys.executable, str(engine), *map(str, args)],
                                    cwd=work, env=env, capture_output=True, text=True, timeout=240)
            text = (result.stdout+result.stderr).replace(str(work), '<work>').replace(str(root), '<checkout>')
            (evidence/(label+'.log')).write_text(text)
            warnings = [s for s in text.splitlines() if s.startswith('[WARNING]')]
            allowed = (table_estimate and warnings and '[ERROR]' not in text and
                       all('library.md: slide 4 (comparison), table 1: ESTIMATE' in s for s in warnings))
            ok = result.returncode == 0 or bool(allowed)
            checks.append({'check': label, 'passed': ok, 'accepted_table_estimate': bool(allowed)})
            if not ok:
                raise RuntimeError(label+' failed:\n'+text[-6000:])

        def render(source: Path, label: str, lang: str, destination: Path, table=False) -> Path:
            project = work/label
            copy(source, project)
            raw = work/(label+'-output')
            command(label+'-kit', 'series', 'preset', project, '--format', 'json')
            command(label+'-audit', 'audit', project, '--lang', lang, '--strict', table_estimate=table)
            command(label+'-build', 'build', project, '--lang', lang, '--output', raw)
            command(label+'-verify', 'verify', project, '--lang', lang, '--output', raw)
            copy(raw, destination)
            return project

        for lang, prefix in [('en', ''), ('fr', 'fr')]:
            edition = output/prefix; dest = edition/'lightwebpres'
            project = render(HERE/'sources'/lang, lang+'-portal', lang, dest)
            demo = render(HERE/'sources'/lang/'example', lang+'-demo', lang, dest/'demo', table=True)
            render(HERE/'sources/guides'/lang, lang+'-guide', lang, dest/'guide')
            for identity in ('native', 'docs', 'field-notes', 'nebula'):
                render(HERE/'sources/comparisons'/lang/identity,
                       lang+'-'+identity, lang, dest/'concepts'/identity)
            command(lang+'-gallery', 'theme', 'gallery', dest/'themes.html', '--lang', lang)
            for item in ('lightwebpres', *LEGAL):
                copy(HERE/'tools'/item, dest/'web'/item)
                copy(HERE/'tools'/item, demo/item)
                copy(HERE/'tools'/item, project/item)
            # A complete series file, independently verified with exactly its build flags.
            single = work/(lang+'-single')
            options = ['--lang', lang, '--single-html', 'publication.html', '--inline-images', '--output', single]
            command(lang+'-single-build', 'build', demo, *options)
            command(lang+'-single-verify', 'verify', demo, *options)
            page = single/'publication.html'
            # Public identity policy: leave legal notices and runtime intact.
            s = integration.clean_html(BeautifulSoup(page.read_text(), 'html.parser'), lang)
            (dest/'downloads/publication.html').write_text(str(s))
            zip_project(dest/'downloads/demarrage.zip', demo)
            zip_project(dest/'downloads/library-project.zip', demo)
            project.joinpath('build-site.py').write_text(
                'import subprocess,sys\nsubprocess.run([sys.executable,"lightwebpres","build",".","--lang",'+repr(lang)+'],check=True)\n')
            zip_project(dest/'downloads/site-sources.zip', project)
            pack = work/(lang+'-cli'); pack.mkdir()
            for item in ('lightwebpres', *LEGAL): copy(HERE/'tools'/item, pack/item)
            zip_project(dest/'downloads/lightwebpres-cli.zip', pack)
            zip_project(dest/'downloads/identity-examples.zip', HERE/'sources/comparisons'/lang)
            for path in sorted(dest.rglob('*.html')):
                relative = path.relative_to(dest)
                if relative.parts[0] in ('reference', 'downloads'): continue
                s = BeautifulSoup(path.read_text(), 'html.parser')
                if not s.html or not s.body: continue
                s = integration.clean_html(integration.decorate(s, 'lightwebpres/'+relative.as_posix(), lang), lang)
                if relative.as_posix() == 'index.html':
                    script = s.new_tag('script', id='site-identity-comparison')
                    script.string = (HERE/'tools/proposal.js').read_text(); s.body.append(script)
                    delivery = s.select_one('.pv-delivery article:last-child')
                    if delivery:
                        link = s.new_tag('a', attrs={'class':'pv-text-link','href':'downloads/publication.html','download':''})
                        link.string = 'Télécharger toute la série en HTML ↓' if lang=='fr' else 'Download the complete series as HTML ↓'
                        delivery.append(link)
                path.write_text(str(s))
            info = {'renderer_commit': lock['commit'], 'renderer_sha256': lock['sha256'],
                    'language': lang, 'editorial_source': '.github/lwp-site/sources',
                    'native_portal_strict_audit': True, 'single_html_verified': True}
            (dest/'build-info.json').write_text(json.dumps(info, indent=2)+'\n')
        # No other product or workshop file is allowed to drift during an LWP build.
        protected = []
        for name in PUBLIC:
            if name in ('lightwebpres', 'fr', 'assets'): continue
            p = root/name
            protected.extend([p] if p.is_file() else [f for f in p.rglob('*') if f.is_file()])
        for name in ('fr/index.html','fr/index.md','fr/llms.txt','fr/fileshed','fr/pasteberth','fr/assets','assets'):
            p=root/name
            protected.extend([p] if p.is_file() else [f for f in p.rglob('*') if f.is_file()])
        for p in protected:
            if p.relative_to(root).as_posix() == 'assets/bilingual-manifest.json': continue
            if digest(p) != digest(output/p.relative_to(root)):
                raise RuntimeError('Unrelated file changed: '+str(p.relative_to(root)))
        manifest = output/'assets/bilingual-manifest.json'
        data = json.loads(manifest.read_text()); data['engine_sha256'] = lock['sha256']
        data['files'] = {p.relative_to(output).as_posix(): digest(p)
                         for p in sorted(output.rglob('*')) if p.is_file() and p != manifest}
        manifest.write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n')
        (evidence/'native-checks.json').write_text(json.dumps({
            'engine_sha256':lock['sha256'], 'checks':checks, 'protected_files':len(protected),
            'source':'.github/lwp-site/sources', 'scope':'Native checks before host decoration; browser QA must run on the assembled staging tree.'
        }, indent=2)+'\n')
    print('Complete portal assembled from canonical sources:', output)


if __name__ == '__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=HERE.parents[1])
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--report', type=Path, required=True)
    a=ap.parse_args();build(a.root,a.output,a.report)
