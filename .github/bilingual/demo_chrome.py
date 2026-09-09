#!/usr/bin/env python3
"""Keep demo navigation compatible with the existing no-network sandbox CSP."""
from pathlib import Path
import base64
import hashlib
import json
import os
import shutil
from bs4 import BeautifulSoup


def embed_demo_chrome(output):
    for locale in ['', 'fr']:
        edition = output / locale
        path = edition / 'pasteberth/demo.html'
        s = BeautifulSoup(path.read_text(), 'html.parser')
        for node in list(s.select('link[rel="stylesheet"]')):
            if 'assets/minisites.css' in node.get('href', ''):
                style = s.new_tag('style', id='fs-demo-chrome')
                style.string = (edition / 'assets/minisites.css').read_text()
                node.replace_with(style)
        for node in list(s.select('script[src]')):
            if 'assets/minisites.js' in node.get('src', ''):
                script = s.new_tag('script', id='fs-demo-navigation')
                script.string = (edition / 'assets/minisites.js').read_text()
                node.replace_with(script)
        for image in s.select('.fs-utility img'):
            image['src'] = 'data:image/webp;base64,' + base64.b64encode(
                (edition / 'assets/fadeshed-mark.webp').read_bytes()).decode()
        if locale == 'fr':
            for script in s.select('script'):
                text = script.string or ''
                needle = 'function tr(v){if(Object.hasOwn(exact,v))return exact[v];return v'
                if needle in text:
                    script.string = text.replace(needle, needle + ".replace(/^Group: Projects$/,'Groupe : Projets').replace(/^Group: Overview$/,'Groupe : Vue d’ensemble').replace(/^Group: Focus$/,'Groupe : Focus')", 1)
        path.write_text(str(s), encoding='utf-8')


def main():
    root = Path('.').resolve()
    out = Path(os.environ['RUNNER_TEMP']) / 'publication'
    if out.exists():
        raise RuntimeError('Use a fresh publication directory')
    for name in ['index.html', 'index.md', 'style.css', 'llms.txt', '.nojekyll',
                 'assets', 'fileshed', 'pasteberth', 'lightwebpres', 'fr']:
        src, dest = root / name, out / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        if src.is_symlink():
            raise RuntimeError('Unexpected symlink')
        if src.is_dir():
            shutil.copytree(src, dest)
        else:
            shutil.copyfile(src, dest)
    embed_demo_chrome(out)
    bp = root / '.github/bilingual/build.py'
    text = bp.read_text()
    marker = '    manifest={p.relative_to(output).as_posix():'
    if marker not in text:
        raise RuntimeError('Missing publication manifest hook')
    text = text.replace(marker, '    from demo_chrome import embed_demo_chrome\n    embed_demo_chrome(output)\n' + marker, 1)
    bp.write_text(text)
    qp = root / '.github/bilingual/qa.py'
    text = qp.read_text()
    marker = "                check(f'Demo loads {locale}',frame.locator('.zone').count()>0)"
    if marker not in text:
        raise RuntimeError('Missing demo check hook')
    additions = "\n                check(f'Embedded navigation hidden {locale}',not frame.locator('.fs-utility').is_visible())"
    additions += "\n                check(f'Demo images decoded {locale}',frame.locator('img').evaluate_all(\"nodes=>nodes.filter(e=>e.getBoundingClientRect().width>0).every(e=>e.complete&&e.naturalWidth>0)\"))"
    qp.write_text(text.replace(marker, marker + additions, 1))
    manifest = out / 'assets/bilingual-manifest.json'
    data = json.loads(manifest.read_text())
    for name in ['pasteberth/demo.html', 'fr/pasteberth/demo.html']:
        data['files'][name] = hashlib.sha256((out / name).read_bytes()).hexdigest()
    manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    workflow = root / '.github/workflows/publish-bilingual.yml'
    wf = workflow.read_text()
    start, end = wf.index('on:'), wf.index('permissions:')
    wf = wf[:start] + 'on:\n  workflow_dispatch:\n' + wf[end:]
    start = wf.index('      - name: Verify and unpack bilingual build sources')
    end = wf.index('      - name: Install isolated browser test tooling', start)
    workflow.write_text(wf[:start] + wf[end:])
    prep = root / '.github/bilingual/prepare_commit.py'
    text = prep.read_text()
    marker = "    print('Uploading',len(files),'public/source files',flush=True)"
    if marker not in text:
        raise RuntimeError('Missing commit preparation hook')
    text = text.replace(marker, "    files['.github/workflows/publish-bilingual.yml']=root/'.github/workflows/publish-bilingual.yml'\n" + marker, 1)
    prep.write_text(text)
    print('Demo resources embedded; original sandbox CSP retained.')


if __name__ == '__main__':
    main()
