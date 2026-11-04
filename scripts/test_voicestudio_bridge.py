import unittest,io,wave
from voicestudio_bridge import speech_request,pcm_wav_info
class VoiceStudioTests(unittest.TestCase):
 def test_request_is_local_prepared_and_no_implicit_dsp(self):
  r=speech_request('http://127.0.0.1:8000','reviewed-engine','Teste.');self.assertEqual(r['state'],'prepared_not_sent');self.assertFalse(r['json']['denoise']);self.assertEqual(r['json']['speed'],1)
 def test_no_external_or_embedded_secret(self):
  for u in ('https://external.example','http://user:secret@localhost:8000','file:///x','http://127.0.0.1:8000?key=x'):
   with self.assertRaises(ValueError):speech_request(u,'engine','test')
 def test_no_implicit_default_engine(self):
  with self.assertRaises(ValueError):speech_request('http://localhost:8000','','test')
 def test_empty_and_long_text(self):
  for text in ('','x'*4097):
   with self.assertRaises(ValueError):speech_request('http://localhost:8000','engine',text)
 def test_speed_validation(self):
  for v in (float('nan'),float('inf'),0,True):
   with self.assertRaises(ValueError):speech_request('http://localhost:8000','engine','test',speed=v)
 def test_wrong_container_rejected(self):
  for data in (b'ID3fake',b'{"error":"failed"}',b'<html>error</html>',b''):
   with self.assertRaises(ValueError):pcm_wav_info(data)
 def test_duration_measured_from_real_header(self):
  b=io.BytesIO()
  with wave.open(b,'wb') as w:w.setparams((1,2,24000,0,'NONE','not compressed'));w.writeframes(b'\0'*4800)
  self.assertEqual(pcm_wav_info(b.getvalue())['duration_seconds'],.1)
 def test_truncated_pcm_blocks(self):
  b=io.BytesIO()
  with wave.open(b,'wb') as w:w.setparams((1,2,24000,0,'NONE','not compressed'));w.writeframes(b'\0'*4800)
  with self.assertRaises(ValueError):pcm_wav_info(b.getvalue()[:-20])
if __name__=='__main__':unittest.main(verbosity=2)
