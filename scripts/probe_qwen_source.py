"""Exercise the upstream wrapper's Python control flow with doubles, NOT inference.

Extracts a function from an independently checked-out Apache-2.0 source at runtime;
does not vendor upstream code. Tensor/model outputs below are explicitly doubles.
"""
import argparse,ast,json,types,hashlib
from pathlib import Path

def run(root):
    source=Path(root)/'qwen_tts/inference/qwen3_tts_model.py';text=source.read_text(encoding='utf8')
    cls=next(n for n in ast.parse(text).body if isinstance(n,ast.ClassDef) and n.name=='Qwen3TTSModel')
    function=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='generate_custom_voice')
    function.decorator_list=[];function.returns=None
    for arg in (*function.args.args,*function.args.kwonlyargs):arg.annotation=None
    if function.args.kwarg:function.args.kwarg.annotation=None
    module=ast.fix_missing_locations(ast.Module(body=[function],type_ignores=[]));namespace={};exec(compile(module,str(source),'exec'),namespace)
    calls=[]
    class ModelDouble:
        tts_model_type='custom_voice';tts_model_size='1b7';tokenizer_type='qwen3_tts_tokenizer_12hz'
        def generate(self,**kwargs):calls.append(kwargs);return ['codes-double'],None
    model=ModelDouble();model.speech_tokenizer=types.SimpleNamespace(decode=lambda v:(['waveform-double'],24000))
    def language_check(v):
        if any(n not in ('Portuguese','English','Auto') for n in v):raise ValueError('test language constraint')
    wrapper=types.SimpleNamespace(model=model,_ensure_list=lambda x:x if isinstance(x,list) else [x],_validate_languages=language_check,_validate_speakers=lambda v:None,_build_assistant_text=lambda t:t,_build_instruct_text=lambda t:'instruction:'+t,_tokenize_texts=lambda v:[['token-double'] for _ in v],_merge_generate_kwargs=lambda **kw:kw)
    fn=namespace['generate_custom_voice'];results=[]
    fn(wrapper,text='Teste.',language='Portuguese',speaker='Ryan',instruct='Firm')
    results.append({'case':'1.7B passes instruct tokens','passed':calls[-1]['instruct_ids']==[['token-double']]})
    model.tts_model_size='0b6';fn(wrapper,text='Teste.',language='Portuguese',speaker='Ryan',instruct='Firm')
    results.append({'case':'0.6B discards instruction upstream','passed':calls[-1]['instruct_ids']==[None]})
    model.tts_model_type='base'
    try:fn(wrapper,text='Teste.',language='Portuguese',speaker='Ryan');rejected=False
    except ValueError:rejected=True
    results.append({'case':'Base cannot masquerade as CustomVoice','passed':rejected})
    return {'scope':'Upstream wrapper control-flow execution with doubles; no tensor computation, weights, tokenizer, inference, audio or quality validation','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'results':results,'passed':all(x['passed'] for x in results)}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('checkout');p.add_argument('--out');a=p.parse_args();r=run(a.checkout)
    if a.out:Path(a.out).write_text(json.dumps(r,indent=2),encoding='utf8')
    print(json.dumps(r,indent=2));raise SystemExit(0 if r['passed'] else 1)
