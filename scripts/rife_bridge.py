"""Frame schedule for RIFE candidates; never calls duplication optical-flow inference."""
from fractions import Fraction
def schedule(frames,fps,factor=2,slow_motion=False,cuts=()):
 if type(frames)!=int or frames<2 or type(factor)!=int or factor not in (2,4,8):raise ValueError('At least2 frames; factors2/4/8 supported')
 rate=Fraction(str(fps))
 if rate<=0:raise ValueError('Positive source FPS required')
 cuts=set(cuts)
 if any(type(c)!=int or not 0<c<frames for c in cuts):raise ValueError('Cuts name the first frame of the new shot')
 result=[]
 for i in range(frames):
  for k in range(factor):
   interpolate=i<frames-1 and k>0 and i+1 not in cuts
   result.append({'index':i*factor+k,'left':i,'right':i+1 if interpolate else i,'t':Fraction(k,factor) if interpolate else Fraction(0),'action':'interpolate' if interpolate else ('original' if k==0 else 'hold')})
 outfps=rate if slow_motion else rate*factor
 return {'frames':result,'fps':outfps,'duration':Fraction(len(result),1)/outfps,'audio_policy':'explicit_stretch_or_mute_required' if slow_motion else 'preserve_original_duration_and_audio','tail_policy':'hold final source frame; no invented future frame'}
