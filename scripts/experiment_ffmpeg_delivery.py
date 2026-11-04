from pathlib import Path
import subprocess,json,hashlib,time,re
from fractions import Fraction
from ffmpeg_delivery import delivery_args
R=Path(__file__).resolve().parents[1];O=R/'out/ffmpeg'/str(time.time_ns());O.mkdir(parents=True)
B=Path(r'C:\Users\giorg\Desktop\FÊNIX DOCS\codex Motionmaxxing\tools\ffmpeg\ffmpeg-9.0.2-essentials_build\bin');F=B/'ffmpeg.exe';P=B/'ffprobe.exe'
def run(args):return subprocess.run([str(a) for a in args],capture_output=True,text=True,encoding='utf8',errors='replace',check=True)
def probe(path,*flags):return json.loads(run([P,'-v','error',*flags,'-of','json',path]).stdout)
master=O/'master.mkv';output=O/'delivery.mp4'
generate=[F,'-v','error','-n','-f','lavfi','-i','testsrc2=size=320x180:rate=30:duration=6','-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=6','-map','0:v','-map','1:a','-c:v','libx264','-preset','ultrafast','-crf','0','-pix_fmt','yuv444p10le','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','pcm_s24le',master]
generate[-1:-1]=['-vf','format=yuv444p10le,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709']
run(generate);source_hash=hashlib.sha256(master.read_bytes()).hexdigest();metadata=probe(master,'-show_streams','-show_format')
args=delivery_args(F,master,output,metadata);run(args);actual=probe(output,'-show_streams','-show_format')
streams=actual['streams'];v=next(s for s in streams if s['codec_type']=='video');a=next(s for s in streams if s['codec_type']=='audio')
assert v['codec_name']=='h264' and int(v['nb_frames'])==180 and a['codec_name']=='aac' and a['sample_rate']=='48000'
assert abs(float(actual['format']['duration'])-6)<1/30
assert all(v.get(k)=='bt709' for k in ('color_transfer','color_primaries','color_space'))
frames=probe(output,'-select_streams','v:0','-show_frames')['frames'];pts=[Fraction(f['best_effort_timestamp_time']) for f in frames]
assert len(pts)==180 and all(abs(float(y-x)-1/30)<.00001 for x,y in zip(pts,pts[1:]))
packets=probe(output,'-show_packets')['packets'];packet_checks={}
for index in (v['index'],a['index']):
 dts=[int(p['dts']) for p in packets if p['stream_index']==index and 'dts' in p];ok=all(y>x for x,y in zip(dts,dts[1:]));assert ok;packet_checks[str(index)]={'count':len(dts),'strict_dts':ok,'first':dts[0],'last':dts[-1]}
decode=run([F,'-v','error','-i',output,'-f','null','-'])
measure=run([F,'-hide_banner','-i',output,'-vn','-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'])
matches=re.findall(r'\{\s*"input_i".*?\}',measure.stderr,re.S);loudness=json.loads(matches[-1]) if matches else None;assert loudness is not None
assert hashlib.sha256(master.read_bytes()).hexdigest()==source_hash
report={'scope':'Synthetic SDR/CFR encode/decode/timestamp/audio measurement; not mobile/perceptual/HDR validation','ffmpeg_version':run([F,'-version']).stdout,'binary_sha256':hashlib.sha256(F.read_bytes()).hexdigest(),'generate_args':list(map(str,generate)),'delivery_args':args,'source_sha256':source_hash,'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'master_unchanged':True,'source_probe':metadata,'delivery_probe':actual,'decoded_frames':len(pts),'packet_checks':packet_checks,'decode_exit':decode.returncode,'audio_measurement':loudness,'audio_measurement_scope':'Input metrics from null-sink loudnorm probe; no normalization applied to saved delivery','source_precision_note':'Testsrc fixture promoted to10bit for pathway testing; not proof of10bit camera detail or HDR quality'}
E=R/'estudo/ffmpeg/resultados';E.mkdir(parents=True,exist_ok=True);(E/'native-delivery.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'video':v['codec_name'],'audio':a['codec_name'],'frames':len(pts),'duration':actual['format']['duration'],'decode_exit':decode.returncode,'loudness_input_i':loudness['input_i'],'master_unchanged':True}))
