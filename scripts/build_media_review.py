"""Build a reviewable UTF-8 diff without staging, committing or publishing."""
from pathlib import Path
import json,hashlib,subprocess,difflib,re
R=Path(__file__).resolve().parents[1];O=R/'out/lote-17-22-review';O.mkdir(parents=True,exist_ok=True)
G=['git','-c','safe.directory='+R.as_posix(),'-C',str(R)]
files=sorted(set(subprocess.check_output([*G,'ls-files','--modified','--others','--exclude-standard','-z']).decode('utf8').strip('\0').split('\0')))
parts=[];manifest=[];links=0;errors=[]
for name in files:
 p=R/name
 if not p.is_file():continue
 old=subprocess.run([*G,'show','HEAD:'+name],capture_output=True).stdout
 new=p.read_bytes()
 try:a=old.decode('utf8');b=new.decode('utf8')
 except UnicodeDecodeError:raise RuntimeError('Unexpected binary in review: '+name)
 parts.extend(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='a/'+name,tofile='b/'+name))
 manifest.append({'path':name,'bytes':len(new),'before_sha256':hashlib.sha256(old).hexdigest() if old else None,'after_sha256':hashlib.sha256(new).hexdigest()})
 if p.suffix=='.md':
  for match in re.finditer(r'\[[^\]]+\]\(([^)]+)\)',b):
   link=match[1].strip('<>').split('#')[0]
   if not link or link.startswith(('https:','http:','mailto:')):continue
   links+=1
   if not (p.parent/link).resolve().exists():errors.append({'file':name,'link':link})
(O/'CHANGES.patch').write_text(''.join(parts),encoding='utf8');(O/'MANIFEST.json').write_text(json.dumps({'base_commit':subprocess.check_output([*G,'rev-parse','HEAD'],text=True).strip(),'files':manifest,'remote_publication':'not_performed'},ensure_ascii=False,indent=2),encoding='utf8')
check={'scope':'Local Markdown links in all changed files, not web links or future clone assets','checked':links,'errors':errors,'ok':not errors}
(R/'estudo/resultados/lote-17-22-link-check.json').write_text(json.dumps(check,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'files':len(manifest),'bytes':sum(x['bytes'] for x in manifest),'markdown_links':links,'link_errors':errors,'review':str(O)},ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
