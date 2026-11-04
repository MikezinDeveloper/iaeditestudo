"""Execute the upstream ElevenLabs example method with a fake SDK; no network/key use."""
from pathlib import Path
import ast,argparse,sys,types,os,json,hashlib
from unittest.mock import patch
p=argparse.ArgumentParser();p.add_argument('checkout');a=p.parse_args();source=Path(a.checkout)/'backend/services/plugin_sdk.py';tree=ast.parse(source.read_text(encoding='utf8'))
node=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='ElevenLabsPlugin');node.decorator_list=[];node.bases=[ast.Name(id='object',ctx=ast.Load())]
module=ast.fix_missing_locations(ast.Module(body=[node],type_ignores=[]));namespace={};exec(compile(module,str(source),'exec'),namespace)
calls=[]
class Client:
 def __init__(self,**kwargs):self.text_to_speech=types.SimpleNamespace(convert=lambda **kw:(calls.append(kw) or [b'fake-audio']))
fake=types.ModuleType('elevenlabs');fake.ElevenLabs=Client
with patch.dict(sys.modules,{'elevenlabs':fake}),patch.dict(os.environ,{'ELEVENLABS_API_KEY':'test-only-not-a-secret'}):
 result=namespace['ElevenLabsPlugin']().generate('Teste.',language='pt',speed=1.2)
assert result==b'fake-audio' and len(calls)==1
assert 'language' not in calls[0] and 'speed' not in calls[0]
assert calls[0]['output_format']=='mp3_44100_128'
report={'scope':'Upstream method executed with fake SDK and fake key; no ElevenLabs account/network/audio generation','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'request_fields':sorted(calls[0]),'language_forwarded':False,'speed_forwarded':False,'format_requested':calls[0]['output_format'],'passed':True}
out=Path(__file__).resolve().parents[1]/'estudo/voicestudio/resultados';out.mkdir(parents=True,exist_ok=True);(out/'plugin-control-flow.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report,indent=2))
