import sys
import pathlib
import unittest
from decimal import Decimal
from decimal import getcontext
getcontext().prec = 16

mytextgrid_path = str(pathlib.Path(__file__).parent.parent.joinpath('src'))
sys.path.insert(0, mytextgrid_path)
from mytextgrid.core.interval_tier import Interval
from mytextgrid.core.interval_tier import IntervalTier

class TestInterval(unittest.TestCase):

    def test_init(self):
        start = Decimal('5.145')
        end = Decimal('6.324')
        interval = Interval(IntervalTier(), start, end, 'perro')

        self.assertEqual(interval.xmin, start)
        self.assertEqual(interval.xmax, end)
        self.assertEqual(interval._xmin, start)
        self.assertEqual(interval._xmax, end)
        self.assertIsNot(interval.xmin, Decimal('5.14500000000000000000003'))
        self.assertIsNot(interval.xmax, Decimal('6.324000001'))
        self.assertEqual(interval.text, 'perro')

        # Test: do not assign a value to xmin and xmax attributes
        with self.assertRaises(AttributeError):
            interval.xmin = '0.313'
            interval.xmax = '0.424'

        # test type errors when assigning values to attributes
        with self.assertRaises(TypeError):
            interval.text = 3

        # Test attribute assignment
        interval._xmin = Decimal('4.3')
        self.assertEqual(interval.xmin, Decimal('4.3'))

if __name__ == '__main__':
    unittest.main()