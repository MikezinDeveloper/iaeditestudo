import copy,tempfile,unittest
from pathlib import Path
from ffmpeg_delivery import delivery_args
class DeliveryTests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory(dir=Path(__file__).parent);self.addCleanup(self.t.cleanup);self.r=Path(self.t.name);self.src=self.r/'master.mkv';self.src.write_bytes(b'master')
  self.m={'streams':[dict(codec_type='video',width=1920,height=1080,color_transfer='bt709',color_primaries='bt709',color_space='bt709',r_frame_rate='30000/1001',avg_frame_rate='30000/1001')]}
 def test_timebase_only_video(self):
  a=delivery_args('ffmpeg',self.src,self.r/'out.mp4',self.m);self.assertIn('-enc_time_base:v',a);self.assertNotIn('-enc_time_base',a);self.assertEqual(a[a.index('-enc_time_base:v')+1],'1001:30000')
 def test_no_source_overwrite(self):
  with self.assertRaises(ValueError):delivery_args('ffmpeg',self.src,self.src,self.m)
 def test_existing_delivery_preserved(self):
  out=self.r/'out.mp4';out.write_bytes(b'approved')
  with self.assertRaises(ValueError):delivery_args('ffmpeg',self.src,out,self.m)
  self.assertEqual(out.read_bytes(),b'approved')
 def test_hdr_or_unspecified_not_retagged(self):
  for trc in ('arib-std-b67','smpte2084','unknown'):
   m=copy.deepcopy(self.m);m['streams'][0]['color_transfer']=trc
   with self.assertRaises(ValueError):delivery_args('ffmpeg',self.src,self.r/'out.mp4',m)
 def test_no_implicit_resize_for_odd_width(self):
  self.m['streams'][0]['width']=1919
  with self.assertRaises(ValueError):delivery_args('ffmpeg',self.src,self.r/'out.mp4',self.m)
 def test_clock_mismatch_blocks(self):
  self.m['streams'][0]['avg_frame_rate']='24000/1001'
  with self.assertRaises(ValueError):delivery_args('ffmpeg',self.src,self.r/'out.mp4',self.m)
 def test_argument_list_keeps_path_as_one_item(self):
  a=delivery_args('ffmpeg',self.src,self.r/'output with spaces.mp4',self.m);self.assertEqual(a[-1],str((self.r/'output with spaces.mp4').resolve()));self.assertIn('-n',a)
if __name__=='__main__':unittest.main(verbosity=2)
