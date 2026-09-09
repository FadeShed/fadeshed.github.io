#!/usr/bin/env python3
"""Rebuild and check the editable portal sources without altering the supplied preview."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lang', choices=('en', 'fr'), default='en')
    parser.add_argument('--renderer', type=Path, default=Path(__file__).resolve().parent / 'lightwebpres')
    parser.add_argument('--output', type=Path, required=True, help='New directory for native pages and audit logs')
    args = parser.parse_args()
    package = Path(__file__).resolve().parents[1]
    output = args.output.expanduser().resolve()
    engine = args.renderer.expanduser().resolve(strict=True)
    if output.exists():
        parser.error('The output directory already exists. Choose a new directory.')
    source = package / 'sources' / args.lang
    if not (source/'series.json').is_file() or not engine.is_file():
        parser.error('A complete source edition and a renderer file are required.')
    if any(p.is_symlink() for p in source.rglob('*')):
        parser.error('Unexpected symlink in source edition.')
    output.mkdir(parents=True)
    checks = []
    with tempfile.TemporaryDirectory(prefix='lwp-preview-', dir=output) as temp:
        project = Path(temp)/'project'
        shutil.copytree(source, project)
        env = os.environ.copy()
        env['TMPDIR'] = temp
        for label, command in [
            ('build',['build',str(project),'--lang',args.lang,'--output',str(output/'public')]),
            ('audit-strict',['audit',str(project),'--lang',args.lang,'--strict']),
            ('verify',['verify',str(project),'--lang',args.lang,'--output',str(output/'public')])
        ]:
            try:
                result = subprocess.run([sys.executable,str(engine),*command], cwd=temp, env=env,
                                        capture_output=True,text=True,timeout=240)
            except subprocess.TimeoutExpired:
                parser.exit(1, 'Native build exceeded its time limit.\n')
            (output/(label+'.log')).write_text(result.stdout+result.stderr,encoding='utf-8')
            checks.append({'check':label,'passed':result.returncode==0})
            (output/'report.json').write_text(json.dumps({
                'language':args.lang, 'renderer_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),
                'checks':checks,
                'scope':'Native source pages only. Shared FadeShed navigation, galleries, builders, guides and comparison resources are present in the supplied public/ snapshot, not recreated by this helper.'
            },ensure_ascii=False,indent=2)+'\n')
            if result.returncode:
                parser.exit(1,f'{label} failed: inspect {output/(label+".log")}\n')
    print(output/'public')
    print('Native source preview built; the complete integrated proposal remains in the package public/.')


if __name__ == '__main__':
    main()
