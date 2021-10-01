import unittest
import MyTextGrid.point_tier
import decimal
decimal.getcontext().prec = 16

class TestIntervalTier(unittest.TestCase):

  def test_init_tier(self):
    tier = MyTextGrid.point_tier.PointTier('tone', 0, 1)
    self.assertEqual(tier.name, 'tone')
    self.assertEqual(tier.xmin, 0)
    self.assertEqual(tier.xmax, 1)
    self.assertEqual(len(tier), 0)

  def test_add_boundary(self):
    tier.insert_point(0.12, 'H')
    tier.insert_point(0.9, 'L')
    tier.insert_point(0.121, 'L')
    tier.insert_point(0.1201, 'H')
    tier.insert_point(0.12003, 'L')
    a=tier.get_label_of_point(3)
    time=tier.get_time_of_point(3)
    tier.set_point_text(3, 'dasdas')