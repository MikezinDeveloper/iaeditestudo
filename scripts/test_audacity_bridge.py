import tempfile,unittest
from pathlib import Path
from audacity_bridge import quote_path,wire_command,require_success,normalization_plan
class AudacityBoundaryTests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory(dir=Path(__file__).parent);self.addCleanup(self.t.cleanup);self.r=Path(self.t.name);self.source=self.r/'original.wav';self.source.write_bytes(b'preserved source')
  self.catalog={'Import2':[],'SelectAll':[],'Export2':['Filename','NumChannels'],'Normalize':['ApplyGain','PeakLevel','RemoveDcOffset','StereoIndependent']}
 def test_plan_requires_native_catalog(self):
  with self.assertRaises(ValueError):normalization_plan(self.source,self.r/'out.wav',{})
 def test_cannot_assume_effect_parameters(self):
  self.catalog['Normalize']=[]
  with self.assertRaises(ValueError):normalization_plan(self.source,self.r/'out.wav',self.catalog)
 def test_preserve_original_and_no_processing_claim(self):
  p=normalization_plan(self.source,self.r/'out.wav',self.catalog);self.assertEqual(p['native_execution'],'not_performed');self.assertEqual(self.source.read_bytes(),b'preserved source');self.assertFalse((self.r/'out.wav').exists())
 def test_no_overwrite(self):
  with self.assertRaises(ValueError):normalization_plan(self.source,self.source,self.catalog)
 def test_quote_injection_rejected(self):
  for s in ('x"\nDelete:','x\0y','x\rfoo'):
   with self.assertRaises(ValueError):quote_path(s)
 def test_framing_is_platform_specific_utf8(self):
  self.assertEqual(wire_command('Help: Command="á"')[-3:],b'\r\n\0');self.assertTrue(wire_command('Help:',False).endswith(b'\n'))
 def test_buffer_limit(self):
  with self.assertRaises(ValueError):wire_command('á'*600)
 def test_failure_and_truncated_response_block(self):
  for response in ('','BatchCommand finished: Failed!','OK','BatchCommand finished: OK\nerror'):
   with self.assertRaises(RuntimeError):require_success(response)
  self.assertTrue(require_success('result\nBatchCommand finished: OK\n\n'))
 def test_nonfinite_gain_rejected(self):
  for v in (float('nan'),float('inf'),True,1):
   with self.assertRaises(ValueError):normalization_plan(self.source,self.r/'out.wav',self.catalog,v)
if __name__=='__main__':unittest.main(verbosity=2)
