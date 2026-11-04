"""Read public model metadata only; never download weights."""
from pathlib import Path
import json,urllib.request
root=Path(__file__).resolve().parents[1]/'estudo/qwen3-tts/resultados';root.mkdir(parents=True,exist_ok=True)
url='https://huggingface.co/api/models/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice?blobs=true'
with urllib.request.urlopen(url,timeout=30) as response:data=json.load(response)
result={'url':url,'model_id':data['id'],'revision':data['sha'],'license':data.get('cardData',{}).get('license'),'files':[{'path':f['rfilename'],'size':f.get('size'),'lfs':f.get('lfs')} for f in data.get('siblings',[])],'weights_downloaded':False}
(root/'model-metadata.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps({'revision':result['revision'],'license':result['license'],'weight_bytes':sum(f['size'] or 0 for f in result['files'] if f['path'].endswith('.safetensors')),'weights_downloaded':False}))
