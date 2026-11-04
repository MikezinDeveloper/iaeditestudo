import unittest
from fractions import Fraction
from rife_bridge import schedule
class RifeClockTests(unittest.TestCase):
 def test_duration_and_count(self):
  p=schedule(30,30);self.assertEqual(len(p['frames']),60);self.assertEqual(p['duration'],1);self.assertEqual(p['fps'],60)
 def test_slow_motion_requires_audio_decision(self):
  p=schedule(30,30,slow_motion=True);self.assertEqual(p['duration'],2);self.assertIn('required',p['audio_policy'])
 def test_never_interpolate_across_cut(self):
  p=schedule(4,30,cuts=[2]);self.assertEqual(p['frames'][3]['action'],'hold');self.assertEqual(p['frames'][3]['left'],1)
 def test_source_frames_preserved(self):
  p=schedule(4,30,4);self.assertEqual([(c['left'],c['action']) for c in p['frames'][::4]],[(i,'original') for i in range(4)])
 def test_last_frame_held_not_shortened(self):self.assertEqual(schedule(3,30)['frames'][-1]['action'],'hold')
 def test_rational_clock(self):self.assertEqual(schedule(30,'30000/1001')['duration'],Fraction(1001,1000))
 def test_invalid_inputs(self):
  for args in [(1,30),(2,0),(2,30,3)]:
   with self.assertRaises(ValueError):schedule(*args)
if __name__=='__main__':unittest.main(verbosity=2)
