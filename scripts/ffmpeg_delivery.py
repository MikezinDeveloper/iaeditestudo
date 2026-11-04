"""Explicit SDR/CFR delivery boundary; no pretend HDR conversion or source overwrite."""
from pathlib import Path
from fractions import Fraction
def delivery_args(ffmpeg,source,target,metadata,crf=18):
 source=Path(source).resolve();target=Path(target).resolve()
 if not source.is_file() or source==target or target.exists():raise ValueError('Existing source and new output required')
 if target.suffix.lower()!='.mp4':raise ValueError('This delivery preset is MP4')
 if type(crf)!=int or not 0<=crf<=35:raise ValueError('Invalid CRF')
 videos=[s for s in metadata.get('streams',[]) if s.get('codec_type')=='video']
 if len(videos)!=1:raise ValueError('Select one final master video stream explicitly')
 v=videos[0]
 if any(type(v.get(k))!=int or v[k]<=0 or v[k]%2 for k in ('width','height')):raise ValueError('Even dimensions required; no implicit scaling')
 if any(v.get(k)!='bt709' for k in ('color_transfer','color_primaries','color_space')):raise ValueError('Input must already be verified SDR709; no tag-only tone mapping')
 rate=Fraction(v['r_frame_rate'])
 if rate<=0 or rate!=Fraction(v['avg_frame_rate']):raise ValueError('Inspect VFR/CFR clock before this bounded delivery preset')
 # Matching average/nominal rates is a necessary preflight only, not proof of CFR.
 # Actual decoded PTS intervals must also be checked by the experiment/production.
 return [str(ffmpeg),'-v','error','-n','-i',str(source),'-map','0:v:0','-map','0:a:0?','-c:v','libx264','-preset','slow','-crf',str(crf),'-pix_fmt','yuv420p','-fps_mode:v','passthrough','-enc_time_base:v',f'{rate.denominator}:{rate.numerator}','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(target)]
