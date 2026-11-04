"""Prepare explicit local VoiceStudio API requests; never starts a service or TTS job."""
from urllib.parse import urlsplit
import math,io,wave
def speech_request(base_url,engine,text,voice='default',speed=1.0):
 u=urlsplit(base_url)
 if u.scheme not in ('http','https') or u.hostname not in ('localhost','127.0.0.1','::1') or u.username or u.password or u.query or u.fragment:raise ValueError('Explicit loopback server only; no credentials in URL')
 if not isinstance(engine,str) or not engine.strip():raise ValueError('Select reviewed engine; no implicit default model')
 if not isinstance(text,str) or not text.strip() or len(text)>4096:raise ValueError('Text required, maximum4096characters')
 if isinstance(speed,bool) or not isinstance(speed,(int,float)) or not math.isfinite(speed) or not .25<=speed<=4:raise ValueError('Invalid speed')
 if not isinstance(voice,str) or not voice.strip():raise ValueError('Explicit voice or default preset required')
 return {'method':'POST','url':base_url.rstrip('/')+'/v1/audio/speech','json':{'model':engine,'input':text,'voice':voice,'response_format':'wav','speed':speed,'denoise':False,'preprocess_prompt':False},'state':'prepared_not_sent','review_required':['engine availability/license','original versus generated voice','provider cost if engine is remote'],'scope':'Local request planner, not a running/native VoiceStudio integration'}
def pcm_wav_info(payload):
 if not isinstance(payload,bytes) or payload[:4]!=b'RIFF' or payload[8:12]!=b'WAVE':raise ValueError('Not a WAV response; do not rename MP3/JSON to WAV')
 try:
  with wave.open(io.BytesIO(payload),'rb') as w:
   data={'frames':w.getnframes(),'sample_rate':w.getframerate(),'channels':w.getnchannels(),'sample_width':w.getsampwidth()}
   if not data['frames'] or not data['sample_rate']:raise ValueError('Empty WAV')
   if len(w.readframes(data['frames']))!=data['frames']*data['channels']*data['sample_width']:raise ValueError('Truncated WAV')
 except wave.Error as e:raise ValueError('PCM WAV subset required; transcode other valid subtypes explicitly') from e
 data['duration_seconds']=data['frames']/data['sample_rate'];return data
