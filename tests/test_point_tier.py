import sys
import pathlib
import unittest
from decimal import Decimal
from decimal import getcontext
mytextgrid_path = str(pathlib.Path(__file__).parent.parent.joinpath('src'))
sys.path.insert(0, mytextgrid_path)
from mytextgrid.core.point_tier import PointTier
getcontext().prec = 16

class TestIntervalTier(unittest.TestCase):

    def setUp(self):
        self.point_tier = PointTier('Tone', 0, 1)
        self.point_tier.insert_point(0.1, 'L')
        self.point_tier.insert_point(0.4, 'H')
        self.point_tier.insert_point(0.7, 'L')

    def test_init(self):
        point_tier = PointTier('Tone', -1, 0)
        with self.assertRaises(AssertionError):
            point_tier = PointTier('Tone', 0, 0)

    def set_attributes(self):
        self.assertEqual(tier.name, 'Tone')
        self.assertEqual(tier.xmin, 0)
        self.assertEqual(tier.xmax, 1)
        self.assertEqual(len(tier), 3)

    def test_add_boundary(self):
        tier = self.point_tier
        tier.insert_point(0.12, 'H')
        tier.insert_point(0.121, 'L')
        tier.insert_point(0.1201, 'H')
        tier.insert_point(0.12003, 'L')
        tier.insert_points(0.6, 0.8, 0.9)

        # Raise ValueError when a point is inserted at a duplicated time
        with self.assertRaises(ValueError):
            tier.insert_point(0.12, 'H')
            tier.insert_point(0.12003, 'H')

    def test_get_index_at_time(self):
        tier = self.point_tier
        index = tier.get_index_at_time(0.1)
        index = tier.get_index_at_time(0.111)

    def test_get_point_at_time(self):
        tier = self.point_tier
        time = tier.get_point_at_time(0.1)

if __name__ == '__main__':
    unittest.main()
