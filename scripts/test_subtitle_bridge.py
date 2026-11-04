import unittest
from subtitle_bridge import parse,serialize,frame_cues,retime,validate
S='1\n00:00:01,001 --> 00:00:02,002\nNão perca o sentido.\nSegunda linha.\n\n2\n00:00:02,500 --> 00:00:03,000\nDireção é diferente.\n'
class SubtitleTests(unittest.TestCase):
 def test_roundtrip_preserves_unicode_and_lines(self):
  c=parse(S);self.assertEqual(parse(serialize(c)),c);self.assertEqual(c[0]['text'],'Não perca o sentido.\nSegunda linha.')
 def test_bom_and_crlf(self):self.assertEqual(parse('\ufeff'+S.replace('\n','\r\n')),parse(S))
 def test_malformed_time_not_silently_repaired(self):
  for old,new in [('01,001','61,001'),(' --> ',' -> '),('01,001','01.001')]:
   with self.assertRaises(ValueError):parse(S.replace(old,new))
 def test_reverse_or_zero_cue_rejected(self):
  with self.assertRaises(ValueError):parse(S.replace('00:00:02,002','00:00:00,000'))
 def test_duplicate_ids_rejected(self):
  with self.assertRaises(ValueError):parse(S.replace('\n2\n','\n1\n'))
 def test_rational_frame_bounds_are_outward(self):
  c=frame_cues(parse(S),'30000/1001');self.assertEqual((c[0]['from_frame'],c[0]['end_frame_exclusive']),(30,60))
 def test_speed_is_explicit_and_does_not_mutate_original(self):
  c=parse(S);r=retime(c,'1.2');self.assertEqual(c[0]['start_ms'],1001);self.assertEqual(r[0]['start_ms'],834)
 def test_negative_offset_not_clamped(self):
  with self.assertRaises(ValueError):retime(parse(S),offset_ms=-2000)
 def test_overlap_is_warning_not_erased_dialogue(self):
  c=parse(S.replace('00:00:02,500','00:00:01,900'));self.assertEqual(validate(c)[0]['type'],'overlap');self.assertEqual(len(c),2)
 def test_no_fps_change_to_source_milliseconds(self):
  c=parse(S);a=frame_cues(c,'24');b=frame_cues(c,'60');self.assertEqual(a[0]['start_ms'],b[0]['start_ms']);self.assertNotEqual(a[0]['from_frame'],b[0]['from_frame'])
if __name__=='__main__':unittest.main(verbosity=2)
