"""Import the inspected Auto-Editor v1 linear EDL; retain exact source/output clocks."""
from fractions import Fraction
import math
def edl(data,global_speed='1',already_retimed=False):
 if data.get('version')!='1':raise ValueError('Only v1 linear chunks supported; do not flatten v3 layers/transitions')
 tb=Fraction(str(data['timebase']));speed=Fraction(str(global_speed))
 if tb<=0 or speed<=0:raise ValueError('Positive timebase/speed required')
 if already_retimed and speed!=1:raise ValueError('Do not retime an already retimed source again')
 source=data.get('source')
 if not isinstance(source,str) or not source:raise ValueError('Missing source')
 chunks=data.get('chunks');segments=[];clock=Fraction(0);last=0
 if not isinstance(chunks,list) or not chunks:raise ValueError('Chunks required')
 for chunk in chunks:
  if len(chunk)!=3:raise ValueError('Chunk must be[start,end,speed]')
  a,b,v=chunk
  if type(a)!=int or type(b)!=int or a!=last or b<=a:raise ValueError('Contiguous integer source chunks required')
  if isinstance(v,bool) or not isinstance(v,(float,int)) or not math.isfinite(v) or v<=0:raise ValueError('Invalid chunk speed')
  last=b
  if v==99999:continue
  effective=Fraction(str(v))*speed;duration=Fraction(b-a,1)/tb/effective
  segments.append({'source_start':Fraction(a,1)/tb,'source_end':Fraction(b,1)/tb,'output_start':clock,'output_end':clock+duration,'speed':effective});clock+=duration
 return {'source':source,'segments':segments,'duration':clock,'timebase':tb,'scope':'Candidate cuts; amplitude is not semantic speech detection'}
def map_point(plan,seconds):
 t=Fraction(str(seconds))
 for s in plan['segments']:
  if s['source_start']<=t<s['source_end']:return s['output_start']+(t-s['source_start'])/s['speed']
 return None
