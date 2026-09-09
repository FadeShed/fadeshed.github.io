#!/usr/bin/env python3
"""Keep demo navigation compatible with the existing no-network sandbox CSP."""
from pathlib import Path
import ast
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
    assignments = [node for node in ast.walk(ast.parse(text)) if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='manifest' for t in node.targets)]
    if len(assignments)!=1:
        raise RuntimeError('Expected one output manifest assignment: '+repr([(getattr(n,'lineno',0),type(n).__name__) for n in assignments]))
    lines=text.splitlines(keepends=True);line=assignments[0].lineno-1;indent=lines[line][:len(lines[line])-len(lines[line].lstrip())]
    lines[line:line]=[indent+'from demo_chrome import embed_demo_chrome\n',indent+'embed_demo_chrome(output)\n'];bp.write_text(''.join(lines))
    qp = root / '.github/bilingual/qa.py'
    text=qp.read_text();calls=[]
    for node in ast.walk(ast.parse(text)):
        if isinstance(node,ast.Expr) and isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Name) and node.value.func.id=='check' and node.value.args:
            arg=node.value.args[0]
            if isinstance(arg,ast.JoinedStr) and any(isinstance(v,ast.Constant) and isinstance(v.value,str) and v.value.startswith('Demo loads') for v in arg.values):calls.append(node)
    if len(calls)!=1:raise RuntimeError('Expected one demo readiness assertion')
    lines=text.splitlines(keepends=True);line=calls[0].end_lineno;indent=lines[calls[0].lineno-1][:len(lines[calls[0].lineno-1])-len(lines[calls[0].lineno-1].lstrip())]
    lines[line:line]=[indent+"check(f'Embedded navigation hidden {locale}',not frame.locator('.fs-utility').is_visible())\n",indent+"check(f'Demo images decoded {locale}',frame.locator('img').evaluate_all(\"nodes=>nodes.filter(e=>e.getBoundingClientRect().width>0).every(e=>e.complete&&e.naturalWidth>0)\"))\n"]
    qp.write_text(''.join(lines))
    manifest = out / 'assets/bilingual-manifest.json'
    data = json.loads(manifest.read_text())
    for name in ['pasteberth/demo.html', 'fr/pasteberth/demo.html']:
        data['files'][name] = hashlib.sha256((out / name).read_bytes()).hexdigest()
    manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print('Demo resources embedded; original sandbox CSP retained.')


if __name__ == '__main__':
    main()
