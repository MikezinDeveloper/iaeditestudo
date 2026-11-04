"""Canonical SRT interchange subset; not a port of Subtitle Edit's tolerant parser."""
from fractions import Fraction
import math,re,json,argparse
from pathlib import Path
TIME=re.compile(r'^(\d{2,}):([0-5]\d):([0-5]\d),(\d{3})$')
def ms(s):
 m=TIME.fullmatch(s)
 if not m:raise ValueError('Canonical hh:mm:ss,mmm required')
 h,mi,se,sub=map(int,m.groups());return ((h*60+mi)*60+se)*1000+sub
def stamp(value):
 if type(value)!=int or value<0:raise ValueError('Nonnegative integer milliseconds required')
 h,x=divmod(value,3600000);mi,x=divmod(x,60000);se,x=divmod(x,1000);return f'{h:02}:{mi:02}:{se:02},{x:03}'
def validate(cues):
 seen=set();last=-1;warnings=[]
 for c in cues:
  if c['id'] in seen:raise ValueError('Duplicate cue id')
  seen.add(c['id'])
  if type(c['start_ms'])!=int or type(c['end_ms'])!=int or c['start_ms']<0 or c['end_ms']<=c['start_ms']:raise ValueError('Invalid cue interval')
  if c['start_ms']<last:raise ValueError('Cue order invalid')
  if not c['text'].strip():raise ValueError('Empty cue text')
  last=c['start_ms']
 for a,b in zip(cues,cues[1:]):
  if b['start_ms']<a['end_ms']:warnings.append({'type':'overlap','ids':[a['id'],b['id']]})
 return warnings
def parse(text):
 text=text.lstrip('\ufeff').replace('\r\n','\n').strip();cues=[]
 if not text:return cues
 for block in re.split(r'\n\s*\n',text):
  lines=block.splitlines()
  if len(lines)<3 or not lines[0].isdigit() or int(lines[0])<1:raise ValueError('Number/time/text expected')
  pieces=lines[1].split(' --> ')
  if len(pieces)!=2:raise ValueError('Canonical arrow required; repair in Subtitle Edit first')
  cues.append(dict(id=int(lines[0]),start_ms=ms(pieces[0]),end_ms=ms(pieces[1]),text='\n'.join(lines[2:])))
 validate(cues);return cues
def serialize(cues):
 validate(cues);return '\n\n'.join(f"{c['id']}\n{stamp(c['start_ms'])} --> {stamp(c['end_ms'])}\n{c['text']}" for c in cues)+'\n'
def frame_cues(cues,fps):
 validate(cues);rate=Fraction(str(fps))
 if rate<=0 or rate>240:raise ValueError('Invalid rational fps')
 return [dict(c,from_frame=math.floor(Fraction(c['start_ms'],1000)*rate),end_frame_exclusive=math.ceil(Fraction(c['end_ms'],1000)*rate)) for c in cues]
def retime(cues,speed='1',offset_ms=0):
 validate(cues);speed=Fraction(str(speed))
 if speed<=0 or type(offset_ms)!=int:raise ValueError('Invalid mapping')
 result=[dict(c,start_ms=round(Fraction(c['start_ms'],1)/speed)+offset_ms,end_ms=round(Fraction(c['end_ms'],1)/speed)+offset_ms) for c in cues]
 validate(result);return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('srt');p.add_argument('--fps',default='30');a=p.parse_args();c=parse(Path(a.srt).read_text(encoding='utf-8-sig'));print(json.dumps({'cues':frame_cues(c,a.fps),'warnings':validate(c),'scope':'Canonical SRT import; no ASR, word timings, burn-in or native app execution'},ensure_ascii=False,indent=2))
