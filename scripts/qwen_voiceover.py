"""Offline Qwen CustomVoice boundary. No model download or original-speech replacement.

The contract can be tested without torch. Actual synthesis needs a complete local
snapshot and the optional Qwen runtime; --preflight never imports the heavy stack.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json,math,re,sys,time,wave

LANGUAGES={'Chinese','English','Japanese','Korean','German','French','Russian','Portuguese','Spanish','Italian','Auto'}
SPEAKERS={'Vivian','Serena','Uncle_Fu','Dylan','Eric','Ryan','Aiden','Ono_Anna','Sohee'}

def validate_request(data):
    if not isinstance(data,dict):raise ValueError('Request must be an object')
    if type(data.get('schema_version'))!=int or data['schema_version']!=1 or data.get('purpose')!='new_voiceover':raise ValueError('Only explicit new_voiceover requests supported')
    for key in ('text','model_snapshot','model_revision'):
        if not isinstance(data.get(key),str) or not data[key].strip():raise ValueError('Missing '+key)
    if not re.fullmatch('[0-9a-f]{40}',data['model_revision']):raise ValueError('Model revision must be a pinned40hex commit, separate from code revision')
    if len(data['text'])>2000:raise ValueError('Split narration into reviewed segments, maximum2000characters per request')
    if data.get('language') not in LANGUAGES:raise ValueError('Unsupported language')
    if data.get('speaker') not in SPEAKERS:raise ValueError('Unsupported study speaker; fine-tuned speakers need a new contract')
    if data.get('model_size') not in ('0.6B','1.7B'):raise ValueError('Unsupported model size')
    if not isinstance(data.get('instruct',''),str):raise ValueError('instruct must be text')
    if data['model_size']=='0.6B' and data.get('instruct','').strip():raise ValueError('0.6B discards instruct upstream; expressive control requires1.7B')
    limit=data.get('max_new_tokens',512)
    if type(limit)!=int or not 1<=limit<=4096:raise ValueError('Invalid max_new_tokens')
    seed=data.get('seed',0)
    if type(seed)!=int or not 0<=seed<2**32:raise ValueError('Invalid seed')
    if data.get('device','cpu') not in ('cpu','cuda:0'):raise ValueError('Unsupported device in this study')
    if data.get('dtype','float32') not in ('float32','float16','bfloat16'):raise ValueError('Invalid dtype')
    return dict(data)

def preflight(request):
    r=validate_request(request);root=Path(r['model_snapshot']).expanduser()
    missing=[n for n in ('torch','transformers','soundfile','qwen_tts') if importlib.util.find_spec(n) is None]
    issues=['Missing optional dependency: '+n for n in missing]
    if not root.is_dir():issues.append('Local model snapshot absent; no automatic download')
    else:
        config=root/'config.json'
        if not config.is_file():issues.append('Model config absent')
        else:
            c=json.loads(config.read_text(encoding='utf8'))
            if c.get('tts_model_type')!='custom_voice':issues.append('Expected CustomVoice snapshot')
            expected='0b6' if r['model_size']=='0.6B' else '1b7'
            if c.get('tts_model_size')!=expected:issues.append('Model size differs from request')
        if not list(root.glob('*.safetensors')):issues.append('Model weights absent')
        if not (root/'speech_tokenizer/config.json').is_file():issues.append('Speech tokenizer absent')
    return {'ready':not issues,'issues':issues,'model_revision':r['model_revision'],'scope':'Dependency/file preflight; memory, latency and voice quality require a real inference test.'}

def write_pcm24(path,samples,sr):
    if type(sr)!=int or not 8000<=sr<=192000:raise ValueError('Invalid returned sample rate')
    values=list(samples)
    if not values or any(not isinstance(v,(float,int)) or not math.isfinite(v) or abs(v)>1 for v in values):raise ValueError('Empty, nonfinite or clipped waveform; no silent normalization')
    path=Path(path)
    # Exclusive creation prevents overwriting a source or previously generated take.
    with path.open('xb') as stream:
        with wave.open(stream,'wb') as out:
            out.setparams((1,3,sr,0,'NONE','not compressed'))
            out.writeframes(b''.join(int(round(v*8388607)).to_bytes(3,'little',signed=True) for v in values))
    return {'frames':len(values),'sample_rate':sr,'channels':1,'sample_width':3,'duration_seconds':len(values)/sr,'peak':max(abs(v) for v in values),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

def synthesize(request,output):
    r=validate_request(request);check=preflight(r)
    if not check['ready']:raise RuntimeError(json.dumps(check))
    output=Path(output)
    if output.suffix.lower()!='.wav' or output.exists() or output.with_suffix('.json').exists():raise ValueError('New WAV and sidecar paths required')
    import os
    os.environ['HF_HUB_OFFLINE']='1';os.environ['TRANSFORMERS_OFFLINE']='1'
    import torch
    from qwen_tts import Qwen3TTSModel
    torch.manual_seed(r.get('seed',0))
    started=time.monotonic()
    model=Qwen3TTSModel.from_pretrained(str(Path(r['model_snapshot']).resolve()),device_map=r.get('device','cpu'),dtype=getattr(torch,r.get('dtype','float32')),attn_implementation='eager',local_files_only=True)
    wavs,sr=model.generate_custom_voice(text=r['text'],language=r['language'],speaker=r['speaker'],instruct=r.get('instruct',''),non_streaming_mode=True,max_new_tokens=r.get('max_new_tokens',512))
    if len(wavs)!=1:raise RuntimeError('Unexpected batch size')
    result=write_pcm24(output,wavs[0].tolist(),int(sr))
    result.update(request=r,elapsed_seconds=time.monotonic()-started,review_state='pending_human_listening',word_timestamps=None,truncation_verified=False,notes=['Seed does not guarantee cross-device determinism','Do not infer word times or final duration from text/token budget','Preserve original speech; generated narration is a separate asset'])
    output.with_suffix('.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('request');p.add_argument('--preflight',action='store_true');p.add_argument('--output')
    a=p.parse_args();r=json.loads(Path(a.request).read_text(encoding='utf8'))
    if a.preflight:
        result=preflight(r);print(json.dumps(result,ensure_ascii=False,indent=2));return 0 if result['ready'] else 2
    if not a.output:p.error('--output is required for synthesis')
    print(json.dumps(synthesize(r,a.output),ensure_ascii=False,indent=2));return 0

if __name__=='__main__':sys.exit(main())
