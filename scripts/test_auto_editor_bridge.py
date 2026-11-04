import copy,unittest
from fractions import Fraction
from auto_editor_bridge import edl,map_point
class EdlTests(unittest.TestCase):
 def setUp(self):self.data={'version':'1','source':'synthetic.wav','timebase':'30/1','chunks':[[0,30,99999],[30,60,1],[60,90,99999],[90,120,1]]}
 def test_exact_cut_duration(self):self.assertEqual(edl(self.data)['duration'],2)
 def test_point_mapping_preserves_gaps(self):
  p=edl(self.data);self.assertEqual(map_point(p,'1.5'),Fraction(1,2));self.assertIsNone(map_point(p,'.5'));self.assertEqual(map_point(p,'3.5'),Fraction(3,2))
 def test_half_open_boundaries(self):
  p=edl(self.data);self.assertEqual(map_point(p,'1'),0);self.assertIsNone(map_point(p,'2'));self.assertIsNone(map_point(p,'4'))
 def test_speed_one_point_two_once(self):self.assertEqual(edl(self.data,'1.2')['duration'],Fraction(5,3))
 def test_double_speed_blocked(self):
  with self.assertRaises(ValueError):edl(self.data,'1.2',True)
 def test_unknown_v3_not_silently_flattened(self):
  self.data['version']='3'
  with self.assertRaises(ValueError):edl(self.data)
 def test_nonfinite_and_negative_speed(self):
  for value in (float('nan'),float('inf'),0,-1,True):
   d=copy.deepcopy(self.data);d['chunks'][1][2]=value
   with self.assertRaises(ValueError):edl(d)
 def test_gaps_overlaps_and_fractional_ticks_rejected(self):
  for value in (29,31,30.5):
   d=copy.deepcopy(self.data);d['chunks'][1][0]=value
   with self.assertRaises(ValueError):edl(d)
if __name__=='__main__':unittest.main(verbosity=2)
