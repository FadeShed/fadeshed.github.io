#!/usr/bin/env python3
"""Use native reader controls and retain shared navigation zoom compensation."""
from pathlib import Path
import hashlib
import json
import re


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise RuntimeError('Unexpected source baseline: ' + old[:100])
    return text.replace(old, new, 1)


def apply(root):
    root = Path(root).resolve()
    for name in ['assets', 'fr/assets', '.github/reader-refresh']:
        folder = root / name
        (folder / 'reader-site.js').write_text(
            '/* Reader interactions are provided by the native LightWebPres controls. */\n', encoding='utf-8')
        (folder / 'reader-site.css').write_text(
            '/* Keep FadeShed navigation readable during native presentation zoom. */\n'
            '.fs-floating,.lwp-web-nav>.fs-language{zoom:calc(1 / var(--lwp-presentation-zoom,1))}\n', encoding='utf-8')
    # Cached pages may still request the harmless compatibility script.
    for locale in ['', 'fr']:
        folder = root / locale / 'lightwebpres'
        for path in folder.rglob('*.html'):
            if 'reference' in path.relative_to(folder).parts:
                continue
            before = path.read_text()
            after = re.sub(r'<script\b[^>]*\bsrc="/assets/reader-site\.js"[^>]*>\s*</script>', '', before)
            if after != before:
                path.write_text(after, encoding='utf-8')
    p = root / '.github/reader-refresh/build.py'
    text = replace_once(p.read_text(),
        "                js=s.new_tag('script',src='/assets/reader-site.js',defer=True);s.body.append(js)\n", '')
    p.write_text(text)
    p = root / '.github/reader-refresh/qa.py'
    text = replace_once(p.read_text(), "                        page.locator('.fs-reader-open').click();",
        "                        check('No redundant reader control '+lang+rel,page.locator('.fs-reader-open').count()==0)\n"
        "                        page.locator('#navMenu').click();")
    start = text.index("                expect(page.locator('.fs-reader-open')).to_be_visible()")
    end = text.index("                page.locator('[data-menu-action=zoom-in]').tap()", start)
    text = text[:start] + (
        "                check('No redundant touch reader control '+lang,page.locator('.fs-reader-open').count()==0)\n"
        "                expect(page.locator('#navMenu')).to_be_visible()\n"
        "                page.locator('#navMenu').tap();expect(page.locator('#presenterMenu')).to_be_visible()\n"
    ) + text[end:]
    p.write_text(text)
    p = root / '.github/reader-refresh/capture.py'
    p.write_text(p.read_text().replace('.fs-utility,.fs-reader-open,.nav-controls', '.fs-utility,.nav-controls'))
    # Reviewed tracked sources replace the historical bootstrap overlays.
    p = root / '.github/workflows/publish-reader-refresh.yml'
    text = p.read_text()
    start = text.index('on:');end = text.index('permissions:', start)
    text = text[:start] + 'on:\n  workflow_dispatch:\n' + text[end:]
    start = text.index('      - name: Verify reviewed build sources')
    end = text.index('      - name: Pull the current LightWebPres main', start)
    p.write_text(text[:start] + text[end:])
    manifest = root / 'assets/bilingual-manifest.json'
    data = json.loads(manifest.read_text())
    for name in data['files']:
        f = root / name
        if not f.is_file() or f.is_symlink():
            raise RuntimeError('Unexpected manifest path: ' + name)
        data['files'][name] = hashlib.sha256(f.read_bytes()).hexdigest()
    manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print('Removed the redundant EN/FR control; native reader controls retained.')


if __name__ == '__main__':
    import sys
    apply(sys.argv[1] if len(sys.argv) > 1 else '.')
