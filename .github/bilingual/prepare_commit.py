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
    # Store readable, reproducible maintenance scripts with the final publication.
    for p in Path('.github/bilingual').rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts:files[p.as_posix()]=p
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
    commit=api('/git/commits',{'tree':tree['sha'],'parents':[parent],'message':'Publish complete English and French editions with explicit language navigation\n\nEnglish is the canonical default; /fr/ selects French. Preserve all three microsites, the complete LightWebPres portal, demonstrations, guides, gallery and browser builder. Add a common EN | FR switch and reviewed translation sources without modifying either application engine.'})
    print('PUBLICATION_COMMIT='+commit['sha'],flush=True)
    print('PARENT_COMMIT='+parent,flush=True)
    print('UPDATED_FILES='+str(len(entries)),flush=True)
    (Path(os.environ['RUNNER_TEMP'])/'qa/prepared-commit.json').write_text(json.dumps({'sha':commit['sha'],'parent':parent,'changed_files':len(entries),'checks':report['checks']},indent=2)+'\n')
if __name__=='__main__':main()
