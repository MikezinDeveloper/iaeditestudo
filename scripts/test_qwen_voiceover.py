import copy,importlib.util,json,tempfile,unittest,wave
from pathlib import Path
from qwen_voiceover import validate_request,preflight,write_pcm24

class QwenBoundaryTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(dir=Path(__file__).parent);self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
  self.r=dict(schema_version=1,purpose='new_voiceover',text='Cada decisão muda o resultado.',language='Portuguese',speaker='Ryan',model_size='1.7B',model_snapshot=str(self.root/'absent'),model_revision='0'*40,instruct='Tom sério, natural e firme.',max_new_tokens=256,seed=1)
 def test_portuguese_request_preserves_text_and_intent(self):
  original=copy.deepcopy(self.r);self.assertEqual(validate_request(self.r),original);self.assertEqual(self.r,original)
 def test_smaller_model_cannot_silently_discard_emotion(self):
  self.r['model_size']='0.6B'
  with self.assertRaises(ValueError):validate_request(self.r)
  self.r['instruct']='';self.assertEqual(validate_request(self.r)['model_size'],'0.6B')
 def test_no_source_cleanup_or_voice_clone_disguised_as_tts(self):
  for purpose in ('cleanup','clone','replace_original',None):
   self.r['purpose']=purpose
   with self.assertRaises(ValueError):validate_request(self.r)
 def test_model_snapshot_missing_never_reports_ready(self):
  p=preflight(self.r);self.assertFalse(p['ready']);self.assertIn('Local model snapshot absent; no automatic download',p['issues'])
 def test_invalid_types_and_limits_rejected(self):
  for key,value in [('text',' '),('language','pt-BR'),('speaker','invented'),('max_new_tokens',True),('max_new_tokens',0),('seed',-1),('dtype','int4'),('device','unknown'),('model_revision','main'),('schema_version',True)]:
   with self.subTest(key=key,value=value):
    r=copy.deepcopy(self.r);r[key]=value
    with self.assertRaises(ValueError):validate_request(r)
 def test_pcm_duration_and_rate_measured_from_samples(self):
  p=self.root/'synthetic-contract-only.wav';r=write_pcm24(p,[0,.25,-.25,0]*2400,24000)
  self.assertAlmostEqual(r['duration_seconds'],.4)
  with wave.open(str(p),'rb') as f:self.assertEqual((f.getnframes(),f.getsampwidth(),f.getframerate()),(9600,3,24000))
 def test_never_overwrite_existing_audio(self):
  p=self.root/'source.wav';p.write_bytes(b'original')
  with self.assertRaises(FileExistsError):write_pcm24(p,[.2],24000)
  self.assertEqual(p.read_bytes(),b'original')
 def test_reject_nonfinite_and_clipped_without_artifact(self):
  p=self.root/'bad.wav'
  for samples in ([],[float('nan')],[float('inf')],[1.1]):
   with self.assertRaises(ValueError):write_pcm24(p,samples,24000)
   self.assertFalse(p.exists())
 def test_actual_model_type_checked_even_if_dependencies_absent(self):
  root=self.root/'snapshot';root.mkdir();(root/'config.json').write_text(json.dumps({'tts_model_type':'base','tts_model_size':'0b6'}));self.r['model_snapshot']=str(root)
  p=preflight(self.r);self.assertIn('Expected CustomVoice snapshot',p['issues']);self.assertIn('Model size differs from request',p['issues'])

if __name__=='__main__':unittest.main(verbosity=2)
