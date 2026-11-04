"""Download the previously inspected public snapshot, verifying byte counts/LFS hashes.

No authentication, custom code loading, mutable main ref, or installation is used.
Weights stay in ignored models/. Existing complete files must match the manifest.
"""
from pathlib import Path
import hashlib,json,urllib.request,time
R=Path(__file__).resolve().parents[1]
M=json.loads((R/'estudo/qwen3-tts/resultados/model-metadata.json').read_text(encoding='utf8'))
DEST=R/'models/qwen3-tts-1.7b-customvoice';DEST.mkdir(parents=True,exist_ok=True)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as stream:
  for block in iter(lambda:stream.read(8*1024*1024),b''):h.update(block)
 return h.hexdigest()
results=[]
for f in M['files']:
 path=(DEST/f['path']).resolve()
 if not path.is_relative_to(DEST.resolve()):raise RuntimeError('Path outside model snapshot')
 path.parent.mkdir(parents=True,exist_ok=True)
 expected=(f.get('lfs') or {}).get('sha256')
 if path.exists():
  if path.stat().st_size!=f['size'] or (expected and sha(path)!=expected):raise RuntimeError('Existing snapshot differs: '+f['path'])
  print('Existing verified:',f['path'],flush=True)
 else:
  partial=path.with_name(path.name+'.partial')
  url=f"https://huggingface.co/{M['model_id']}/resolve/{M['revision']}/{f['path']}"
  print('Downloading:',f['path'],'bytes',f['size'],flush=True)
  received=0;printed=0;started=time.monotonic()
  with urllib.request.urlopen(url,timeout=90) as response,partial.open('wb') as out:
   while block:=response.read(8*1024*1024):
    out.write(block);received+=len(block)
    if received-printed>=256*1024*1024:
     print(f'{f["path"]}: {received/f["size"]:.0%}, {received/(time.monotonic()-started)/2**20:.1f}MiB/s',flush=True);printed=received
  if received!=f['size']:raise RuntimeError('Size mismatch: '+f['path'])
  if expected and sha(partial)!=expected:raise RuntimeError('LFS SHA mismatch: '+f['path'])
  partial.replace(path)
 results.append({'path':f['path'],'size':path.stat().st_size,'sha256':sha(path),'lfs_hash_verified':bool(expected)})
receipt={'model':M['model_id'],'revision':M['revision'],'files':results,'network':'public HTTPS, no credentials','download_complete':True}
(DEST/'snapshot-manifest.json').write_text(json.dumps(receipt,indent=2),encoding='utf8')
print('Complete snapshot, hashes verified.',flush=True)
