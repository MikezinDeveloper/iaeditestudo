from pathlib import Path
import wave,math,struct,subprocess,json,hashlib,sys
from auto_editor_bridge import edl
R=Path(__file__).resolve().parents[1];O=R/'out/auto-editor';O.mkdir(parents=True,exist_ok=True)
binary=R.parent/'research-tools/auto-editor/auto-editor.exe';source=O/'silence-tone-fixture.wav';sr=48000
with wave.open(str(source),'wb') as w:
 w.setparams((1,2,sr,0,'NONE','not compressed'));w.writeframes(b''.join(struct.pack('<h',int(.25*32767*math.sin(2*math.pi*440*i/sr)) if 1<=i/sr<2 or 3<=i/sr<4 else 0) for i in range(6*sr)))
out=O/'candidate.json';args=[str(binary),str(source),'--edit','audio:threshold=0.05','--margin','0.1s','--smooth','0','--export','v1','--output',str(out),'--no-open']
p=subprocess.run(args,capture_output=True,text=True,encoding='utf8',errors='replace');evidence={'command':args,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'fixture':'6s mono48kPCM16; tones1–2s/3–4s, other samples zero; not speech','input_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
if p.returncode:print(json.dumps(evidence));raise SystemExit(p.returncode)
data=json.loads(out.read_text());plan=edl(data);evidence.update(native_edl=data,duration_seconds=float(plan['duration']),source_unchanged=hashlib.sha256(source.read_bytes()).hexdigest()==evidence['input_sha256'])
assert 2<float(plan['duration'])<3,'Unexpected cut duration'
assert evidence['source_unchanged']
render_args=[str(binary),str(out),'--output',str(O/'cut.wav'),'--no-open']
render=subprocess.run(render_args,capture_output=True,text=True,encoding='utf8',errors='replace')
evidence['render']={'command':render_args,'exit_code':render.returncode,'stdout':render.stdout,'stderr':render.stderr}
if render.returncode:raise RuntimeError(evidence['render'])
probe=R.parent.parent/'Desktop' # Tool path remains explicit for this recorded Windows environment.
probe=Path(r'C:\Users\giorg\Desktop\FÊNIX DOCS\codex Motionmaxxing\tools\ffmpeg\ffmpeg-9.0.2-essentials_build\bin\ffprobe.exe')
measured=json.loads(subprocess.check_output([str(probe),'-v','error','-show_format','-show_streams','-of','json',str(O/'cut.wav')]))
evidence['render']['probe']=measured
assert abs(float(measured['format']['duration'])-float(plan['duration']))<1/30
report=R/'estudo/auto-editor/resultados/native-experiment.json';report.parent.mkdir(parents=True,exist_ok=True);report.write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'native_exit':p.returncode,'output_duration_seconds':evidence['duration_seconds'],'chunks':data['chunks']}))
