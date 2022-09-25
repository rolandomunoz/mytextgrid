import sys
import pathlib
import unittest
from copy import copy
from decimal import Decimal
from decimal import getcontext
mytextgrid_path = str(pathlib.Path(__file__).parent.parent.joinpath('src'))
sys.path.insert(0, mytextgrid_path)
from mytextgrid.core.interval_tier import IntervalTier
getcontext().prec = 16

class TestIntervalTier(unittest.TestCase):

    def setUp(self):
        self.tier = IntervalTier('palabra', -0.05, 1)
        self.tier.insert_boundary(0.1)
        self.tier.insert_boundary(0.2)
        self.tier.insert_boundary(0.3)
        self.tier.insert_boundary(0.4)
        self.tier.insert_boundary(0.5)
        self.tier.insert_boundary(0.6)
        self.tier.set_text_at_index(1, 'p', 'e', 'r', 'r','o')

    def set_attributes(self):
        self.assertEqual(self.tier.name, 'palabra')
        self.assertEqual(self.tier.xmin, Decimal(-0.05))
        self.assertEqual(self.tier.xmax, Decimal(1))
        self.assertEqual(self.tier.get_duration(), Decimal(1.05))
        self.assertEqual(len(self.tier), 6)

    def test_add_boundary(self):
        # Create tier object
        tier = IntervalTier('rolando', 0, 1)

        times = [
            Decimal('0.45'),
            Decimal('0.3'),
            Decimal('0.5324338183183182'),
            Decimal('0.931313')
        ]
        for time in times:
            tier.insert_boundary(time)

        # Check if NameError on an existing boundary
        with self.assertRaises(ValueError):
            for time in times:
                tier.insert_boundary(time)

            # Add boundary at start and end
            tier.insert_boundary(tier.xmin)
            tier.insert_boundary(tier.xmax)

            # Add boundaries outside the range
            tier.insert_boundary(-0.0000001)
            tier.insert_boundary(2)

    def test_remove_boundary(self):
        tier = copy(self.tier)

        list1 = [(-0.05, 0.1), (0.1, 0.2), (0.2, 0.3), (0.3, 0.4), (0.4, 0.5), (0.5, 0.6), (0.6, 1)]
        for index, interval in enumerate(tier):
            tuple_src = (interval.xmin, interval.xmax)
            tuple_dst = (Decimal(str(list1[index][0])), Decimal(str(list1[index][1])))
            self.assertEqual(tuple_src, tuple_dst)

        tier.remove_boundary(0.5)
        list2 = [(-0.05, 0.1), (0.1, 0.2), (0.2, 0.3), (0.3, 0.4), (0.4, 0.6), (0.6, 1)]
        for index, interval in enumerate(tier):
            tuple_src = (interval.xmin, interval.xmax)
            tuple_dst = (Decimal(str(list2[index][0])), Decimal(str(list2[index][1])))
            self.assertEqual(tuple_src, tuple_dst)

        with self.assertRaises(ValueError):
            tier.remove_boundary(tier.xmin) # start of tier
            tier.remove_boundary(tier.xmax) # End of tier
            tier.remove_boundary(0.15) # middle value
            tier.remove_boundary(-10) # Out of tier range
            tier.remove_boundary(12) # Out of tier range

    def test_move_boundary(self):
        tier = copy(self.tier)

        # Move boundary
        list1 = [(-0.05, 0.1), (0.1, 0.2), (0.2, 0.3), (0.3, 0.4), (0.4, 0.5), (0.5, 0.6), (0.6, 1)]
        for index, interval in enumerate(tier):
            tuple_src = (interval.xmin, interval.xmax)
            tuple_dst = (Decimal(str(list1[index][0])), Decimal(str(list1[index][1])))
            self.assertEqual(tuple_src, tuple_dst)

        tier.move_boundary(0.2, 0.25)
        list2 = [(-0.05, 0.1), (0.1, 0.25), (0.25, 0.3), (0.3, 0.4), (0.4, 0.5), (0.5, 0.6), (0.6, 1)]
        for index, interval in enumerate(tier):
            tuple_src = (interval.xmin, interval.xmax)
            tuple_dst = (Decimal(str(list2[index][0])), Decimal(str(list2[index][1])))
            self.assertEqual(tuple_src, tuple_dst)

        with self.assertRaises(ValueError):
            tier.move_boundary(tier.xmin, 0.15) # start of tier
            tier.move_boundary(tier.xmax, 2) # End of tier
            tier.move_boundary(0.4, 0.55) # out of right neighbor
            tier.move_boundary(0.4, 0.26) # out of left neighbor
            tier.move_boundary(-10, 0.14) # Out of tier range
            tier.move_boundary(12, 1) # Out of tier range
            tier.move_boundary(0.51, 0.52) # Boundary does not exist

    def test_get_index_at_time_boundary(self):
        tier = copy(self.tier)
        self.assertEqual(tier.get_index_at_time_boundary('0.1'), 1) # Boundary
        self.assertIsNone(tier.get_index_at_time_boundary(tier.xmin)) # Start of tier
        self.assertIsNone(tier.get_index_at_time_boundary(tier.xmax)) # End of tier
        self.assertIsNone(tier.get_index_at_time_boundary(0.15)) # No boundary
        self.assertIsNone(tier.get_index_at_time_boundary(-10)) # Outside the tier range
        self.assertIsNone(tier.get_index_at_time_boundary(12)) # Outside the tier range

    def test_get_index_at_time(self):
        tier = copy(self.tier)
        self.assertEqual(tier.get_index_at_time(tier.xmin), 0) # Start
        self.assertEqual(tier.get_index_at_time(tier.xmax), 6) # End
        self.assertEqual(tier.get_index_at_time(0.15), 1)
        self.assertIsNone(tier.get_index_at_time(-10))
        self.assertIsNone(tier.get_index_at_time(12))

    def test_get_interval_at_time(self):
        tier = copy(self.tier)
        self.assertEqual(tier.get_interval_at_time(tier.xmin), tier[0]) # At the start of the tier
        self.assertEqual(tier.get_interval_at_time(tier.xmax), tier[len(tier)-1]) # At the end of the tier
        self.assertEqual(tier.get_interval_at_time(0.15), tier[1]) # At the end of the tier
        self.assertIsNone(tier.get_interval_at_time(-10))
        self.assertIsNone(tier.get_interval_at_time(12))

    def test_set_text(self):
        with self.assertRaises(IndexError):
            self.tier.set_text_at_index(-1, 'p', 'e', 'r', 'o', 's')
            self.tier.set_text_at_index(10, 'p', 'e', 'r', 'o', 's')
            self.tier.set_text_at_index(10, ['p', 'e', 'r', 'o', 's'])
            self.tier.set_text_at_index(10, ('p', 'e', 'r', 'o', 's'))

if __name__ == '__main__':
    unittest.main()
