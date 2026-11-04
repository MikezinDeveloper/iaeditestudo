"""Audacity scripting boundary; never assumes an installed/native DSP session.

Emit inspectable commands only after a caller supplies the native command catalog.
No original speech, application preferences or existing project is modified here.
"""
from pathlib import Path
import json,math,sys

def quote_path(value):
    s=str(value).replace('\\','/')
    if any(c in s for c in ('"','\r','\n','\0')):raise ValueError('Path contains a scripting delimiter')
    return '"'+s+'"'

def wire_command(command,windows=True):
    if not isinstance(command,str) or any(c in command for c in ('\r','\n','\0')):raise ValueError('One command per request')
    data=(command+ ('\r\n\0' if windows else '\n')).encode('utf8')
    if len(data)>1023:raise ValueError('Request exceeds inspected pipe buffer')
    return data

def require_success(response):
    if not isinstance(response,str) or len(response)>4*1024*1024:raise ValueError('Invalid response size/type')
    lines=[v.strip() for v in response.splitlines() if v.strip()]
    if not lines or lines[-1]!='BatchCommand finished: OK':raise RuntimeError('Audacity did not confirm command success')
    return response

def normalization_plan(source,target,catalog,peak_db=-1.0,channels=1):
    source=Path(source).resolve();target=Path(target).resolve()
    if not source.is_file():raise ValueError('Source absent')
    if source==target or target.exists():raise ValueError('New output required; preserve source')
    if target.suffix.lower()!='.wav' or channels not in (1,2):raise ValueError('Explicit WAV output and channels1/2 required')
    if isinstance(peak_db,bool) or not isinstance(peak_db,(int,float)) or not math.isfinite(peak_db) or not -24<=peak_db<=0:raise ValueError('Invalid peak target')
    needed={'Import2','SelectAll','Normalize','Export2'}
    if not needed.issubset(catalog):raise ValueError('Native command catalog incomplete; query GetInfo first')
    if not {'ApplyGain','PeakLevel','RemoveDcOffset','StereoIndependent'}.issubset(catalog['Normalize']):raise ValueError('Normalize parameters must be verified against native catalog')
    commands=[f'Import2: Filename={quote_path(source)}','SelectAll:',f'Normalize: ApplyGain=1 PeakLevel={peak_db} RemoveDcOffset=1 StereoIndependent=0',f'Export2: Filename={quote_path(target)} NumChannels={channels}']
    for c in commands:wire_command(c)
    return {'commands':commands,'source':str(source),'output':str(target),'native_execution':'not_performed','scope':'Peak normalization only; no noise reduction, LUFS matching or perceptual approval','export_parameters':'Export2 inherits native encoder/preferences; probe output before using it'}

def readiness():
    if sys.platform!='win32':return {'ready':False,'reason':'POSIX FIFO transport not implemented by this bounded adapter'}
    paths=[r'\\.\pipe\ToSrvPipe',r'\\.\pipe\FromSrvPipe']
    return {'ready':all(Path(p).exists() for p in paths),'paths':paths,'scope':'Pipe presence only; requires a dedicated Audacity session and catalog probe before mutations.'}

if __name__=='__main__':print(json.dumps(readiness(),ensure_ascii=False,indent=2))
