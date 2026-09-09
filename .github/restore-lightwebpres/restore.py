#!/usr/bin/env python3
"""Reproduce the supplied portal and prepare a verified commit, without moving refs.

The compressed overlay contains the original website sources, not a new design.
All build inputs and all 58 output files must match the supplied archive.
The GitHub connector can publish the resulting commit after reviewing this run.
No private repository is read, and no branch or Pages setting is changed here.
"""
import base64
import hashlib
import json
import lzma
import os
from pathlib import Path, PurePosixPath
import subprocess
import tempfile
import time
import urllib.error
import urllib.request

HERE = Path(__file__).resolve().parent
REPOSITORY = 'FadeShed/fadeshed.github.io'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def contained(root, name):
    relative = PurePosixPath(name)
    if relative.is_absolute() or '..' in relative.parts or not relative.parts:
        raise ValueError('Unsafe archive path: ' + name)
    target = root.joinpath(*relative.parts)
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError('Escaping archive path: ' + name)
    return target


def command(*args, cwd=None):
    subprocess.run(list(map(str, args)), cwd=cwd, check=True, timeout=600)


def api(path, data=None):
    payload = None if data is None else json.dumps(data).encode('utf-8')
    request = urllib.request.Request(
        'https://api.github.com/repos/' + REPOSITORY + path,
        data=payload,
        headers={
            'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
            'Accept': 'application/vnd.github+json',
            'Content-Type': 'application/json',
            'X-GitHub-Api-Version': '2022-11-28',
        },
        method='GET' if data is None else 'POST',
    )
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if error.code not in (429, 500, 502, 503, 504) or attempt == 3:
                raise
            time.sleep(5 * (attempt + 1))


def main():
    if os.environ.get('GITHUB_REPOSITORY') != REPOSITORY:
        raise RuntimeError('This restoration is restricted to the website repository')
    manifest = json.loads((HERE / 'manifest.json').read_text(encoding='utf-8'))
    if manifest['source_repository'] != 'Fade78/lightwebpres':
        raise RuntimeError('Unexpected source repository')
    revision = manifest['source_commit']
    if len(revision) != 40 or any(c not in '0123456789abcdef' for c in revision):
        raise RuntimeError('A full pinned source commit is required')
    encoded = ''.join((HERE / ('overlay-%02d.b64' % i)).read_text().strip()
                      for i in range(1, 5))
    packed = base64.b64decode(encoded, validate=True)
    if digest(packed) != manifest['overlay_sha256']:
        raise RuntimeError('Source overlay checksum mismatch')
    overlay = json.loads(lzma.decompress(packed).decode('utf-8'))
    parent = os.environ['GITHUB_SHA']
    with tempfile.TemporaryDirectory(prefix='lightwebpres-restore-') as temporary:
        root = Path(temporary)
        source = root / 'source'
        command('git', 'init', '-q', source)
        command('git', '-C', source, 'fetch', '--depth=1',
                'https://github.com/Fade78/lightwebpres.git', revision)
        command('git', '-C', source, 'checkout', '--detach', '-q', 'FETCH_HEAD')
        for name, text in overlay.items():
            path = contained(source, name)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(text.encode('utf-8'))
        for name, expected in manifest['inputs'].items():
            path = contained(source, name)
            if not path.is_file() or digest(path.read_bytes()) != expected:
                raise RuntimeError('Build input differs from supplied archive: ' + name)
        output = root / 'portal'
        command('python3', source / 'tools/build_website.py', '--output', output)
        command('python3', source / 'tools/check_website.py', output)
        files = {p.relative_to(output).as_posix(): p for p in output.rglob('*') if p.is_file()}
        if set(files) != set(manifest['output']):
            raise RuntimeError('Restored file set differs: ' + repr(set(files) ^ set(manifest['output'])))
        for name, expected in manifest['output'].items():
            if digest(files[name].read_bytes()) != expected:
                raise RuntimeError('Generated file differs from supplied archive: ' + name)
        print('All %d original files reproduced byte for byte.' % len(files), flush=True)
        if api('/git/ref/heads/main')['object']['sha'] != parent:
            raise RuntimeError('main changed during reconstruction; refusing to overwrite newer work')
        base_tree = api('/git/commits/' + parent)['tree']['sha']
        entries = []
        known = {}
        for name, path in sorted(files.items()):
            data = path.read_bytes()
            sha = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            if sha not in known:
                result = api('/git/blobs', {
                    'content': base64.b64encode(data).decode('ascii'), 'encoding': 'base64'})
                if result['sha'] != sha:
                    raise RuntimeError('Uploaded blob checksum mismatch: ' + name)
                known[sha] = True
            entries.append({'path': 'lightwebpres/' + name, 'mode': '100644',
                            'type': 'blob', 'sha': sha})
            print('Verified object: %s (%d bytes)' % (name, len(data)), flush=True)
        tree = api('/git/trees', {'base_tree': base_tree, 'tree': entries})
        commit = api('/git/commits', {
            'message': 'Restore the complete supplied LightWebPres portal\n\n'
                       'Restore all 58 files byte for byte: the original identity, six '
                       'articles, demo, guide, gallery, downloads, and local Pyodide builder. '
                       'Preserve the existing Markdown indexes and the other minisites.',
            'tree': tree['sha'], 'parents': [parent]})
        print('RESTORED_COMMIT_SHA=' + commit['sha'], flush=True)
        print('PARENT_COMMIT_SHA=' + parent, flush=True)
        summary = os.environ.get('GITHUB_STEP_SUMMARY')
        if summary:
            Path(summary).write_text(
                '# LightWebPres restoration verified\n\n'
                + 'All 58 files match the supplied archive byte for byte.\n\n'
                + 'Prepared commit: `' + commit['sha'] + '`\n\n'
                + 'Parent: `' + parent + '`\n\n'
                + 'No branch has been moved by this job.\n', encoding='utf-8')


if __name__ == '__main__':
    main()
