#!/usr/bin/env python3
"""Push one verified candidate pack; the connector fast-forwards main afterward."""
import base64, hashlib, json, os, shutil, subprocess
from pathlib import Path

def main():
    root=Path.cwd();work=Path(os.environ['RUNNER_TEMP'])/'approved-lwp';out=work/'publication';qa=Path(os.environ['RUNNER_TEMP'])/'qa'
    repo=os.environ['GITHUB_REPOSITORY'];parent=os.environ['GITHUB_SHA']
    if repo!='FadeShed/fadeshed.github.io':raise RuntimeError('Wrong repository')
    report=json.loads((qa/'report.json').read_text())
    if report['checks']!=report['passed']:raise RuntimeError('Unverified publication')
    proof=json.loads((work/'publication-proof.json').read_text())
    changed=[]
    for name,sha in proof['files'].items():
        src=out/name
        if hashlib.sha256(src.read_bytes()).hexdigest()!=sha:raise RuntimeError('Output changed after testing')
        dest=root/name
        if dest.is_file() and dest.read_bytes()==src.read_bytes():continue
        dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest);changed.append(name)
    name='assets/bilingual-manifest.json';shutil.copyfile(out/name,root/name);changed.append(name)
    if not changed:raise RuntimeError('No publication changes')
    subprocess.run(['git','add','--',*changed],check=True)
    staged=subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines()
    if set(staged)!=set(changed):raise RuntimeError('Unexpected staged files')
    author=subprocess.check_output(['git','show','-s','--format=%an%n%ae',parent],text=True).splitlines()
    subprocess.run(['git','-c','user.name='+author[0],'-c','user.email='+author[1],'commit','-m','Publish approved bilingual LightWebPres portal and identity comparisons'],check=True)
    sha=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    env=os.environ.copy();token=env.pop('GH_TOKEN');encoded=base64.b64encode(('x-access-token:'+token).encode()).decode()
    env.update({'GIT_CONFIG_COUNT':'1','GIT_CONFIG_KEY_0':'http.https://github.com/.extraheader','GIT_CONFIG_VALUE_0':'AUTHORIZATION: basic '+encoded})
    remote='https://github.com/'+repo+'.git'
    actual=subprocess.check_output(['git','ls-remote',remote,'refs/heads/main'],env=env,text=True).split()[0]
    if actual!=parent:raise RuntimeError('Main advanced; retain the artifact and rebase, never force')
    subprocess.run(['git','push',remote,sha+':refs/heads/publication/lwp-approved'],env=env,check=True)
    result={'sha':sha,'parent':parent,'candidate_branch':'publication/lwp-approved','checks':report['checks'],'changed_files':staged,'main_moved':False}
    (qa/'prepared-commit.json').write_text(json.dumps(result,indent=2)+'\n');shutil.copyfile(work/'publication-proof.json',qa/'publication-proof.json')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
