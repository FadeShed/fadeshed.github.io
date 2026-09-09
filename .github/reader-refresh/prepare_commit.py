#!/usr/bin/env python3
"""Upload verified public output objects; leave moving main to the connector."""
import base64,hashlib,json,os,time,urllib.request,urllib.error
from pathlib import Path
REPO='FadeShed/fadeshed.github.io'
def api(path,data=None):
    r=urllib.request.Request('https://api.github.com/repos/'+REPO+path,data=None if data is None else json.dumps(data).encode(),headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json','Content-Type':'application/json'},method='GET' if data is None else 'POST')
    for i in range(4):
        try:
            with urllib.request.urlopen(r,timeout=180) as f:return json.load(f)
        except urllib.error.HTTPError as e:
            if e.code not in [429,500,502,503,504] or i==3:raise
            time.sleep((i+1)*3)
def main():
    if os.environ.get('GITHUB_REPOSITORY')!=REPO:raise ValueError('Wrong repository')
    parent=os.environ['GITHUB_SHA'];root=Path(os.environ['RUNNER_TEMP'])/'publication'
    report=json.loads((Path(os.environ['RUNNER_TEMP'])/'qa/report.json').read_text())
    if report['checks']!=report['passed']:raise ValueError('Tests failed')
    if api('/git/ref/heads/main')['object']['sha']!=parent:raise ValueError('main changed')
    base=api('/git/commits/'+parent)['tree']['sha']
    previous={x['path']:x['sha'] for x in api('/git/trees/'+base+'?recursive=1')['tree'] if x['type']=='blob'}
    files={p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file()}
    # Only public build inputs; never stage checkout internals, caches or temporary work.
    source_roots=[Path('.github/reader-refresh'),Path('.github/bilingual/lwp')]
    for folder in source_roots:
        for p in folder.rglob('*'):
            parts=p.relative_to(folder).parts
            if p.is_file() and not any(x in ['work','__pycache__','public'] or x.startswith('.lwp') for x in parts):files[p.as_posix()]=p
    entries=[];known=set(previous.values())
    for name,path in sorted(files.items()):
        if path.is_symlink() or '..' in Path(name).parts:raise ValueError(name)
        b=path.read_bytes();sha=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        if previous.get(name)==sha:continue
        if sha not in known:
            actual=api('/git/blobs',{'encoding':'base64','content':base64.b64encode(b).decode()})['sha']
            if actual!=sha:raise ValueError('Blob mismatch')
            known.add(sha)
        entries.append({'path':name,'mode':'100644','type':'blob','sha':sha})
    tree=api('/git/trees',{'base_tree':base,'tree':entries})
    commit=api('/git/commits',{'tree':tree['sha'],'parents':[parent],'message':'Refresh the complete bilingual LightWebPres portal around real uses\n\nRebuild the reader, guide, examples, gallery and browser builder from the checked upstream main. Add six audience journeys, a rich interactive brief and visible touch access to native zoom. Keep both static languages and original technical provenance, while removing release numbers from editorial pages. Finish the embedded Pasteberth navigation without changing its sandbox policy.'})
    print('PUBLICATION_COMMIT='+commit['sha'],flush=True)
    print('PARENT_COMMIT='+parent,flush=True)
    print('UPDATED_FILES='+str(len(entries)),flush=True)
    (Path(os.environ['RUNNER_TEMP'])/'qa/prepared-commit.json').write_text(json.dumps({'sha':commit['sha'],'parent':parent,'changed_files':len(entries),'checks':report['checks']},indent=2)+'\n')
if __name__=='__main__':main()
