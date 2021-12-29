import sys
import os
import unittest
import decimal
mytextgrid_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, mytextgrid_path)
from mytextgrid.core import interval_tier
decimal.getcontext().prec = 16

class TestIntervalTier(unittest.TestCase):

    def test_init_tier(self):
        tier = interval_tier.IntervalTier('rolando', 0, 1)
        self.assertEqual(tier.name, 'rolando')
        self.assertEqual(tier.xmin, 0)
        self.assertEqual(tier.xmax, 1)
        self.assertEqual(len(tier), 1)

    def test_add_boundary(self):
        tier = interval_tier.IntervalTier('rolando', 0, 1)

        times = [
            decimal.Decimal('0.45'),
            decimal.Decimal('0.3'),
            decimal.Decimal('0.5324338183183182'),
            decimal.Decimal('0.931313')
        ]

        # Add boundary
        for time in times:
            tier.insert_boundary(time)

        self.assertEqual(tier.insert_boundary('0.84'), (3, 4))
        tier.remove_boundary('0.84')

        # Test general attributes after adding boundaries
        self.assertEqual(tier.name, 'rolando')
        self.assertEqual(tier.xmin, 0)
        self.assertEqual(tier.xmax, 1)
        self.assertEqual(len(tier), 5) # number of intervals

        # Check if boundaries exist
        times.append(tier.xmax)
        new_times=times.copy()
        new_times.sort()
        for index, interval in enumerate(tier):
            self.assertEqual(interval.xmax, new_times[index])

        # Check if NameError on an existing boundary
        with self.assertRaises(ValueError):
            for time in times:
                tier.insert_boundary(time)

            # Add boundary at start and end
            tier.insert_boundary(0)
            tier.insert_boundary(1)

            # Add boundaries outside the range
            tier.insert_boundary(-0.0000001)
            tier.insert_boundary(2)

if __name__ == '__main__':
    unittest.main()

#position = tier.get_interval_at_time(0.5)
#tier.set_interval_text(position, 'Huaiwa')
#position = tier.get_interval_at_time(0.1)
#tier.set_interval_text(position, 'Aarone')
#position = tier.get_interval_at_time(0.95)
#tier.set_interval_text(position, 'Erick')

#tier.move_boundary(0.3, 0.34)
#print(tier)
