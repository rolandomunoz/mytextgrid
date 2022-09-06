import sys
import pathlib
import unittest
from decimal import Decimal
from decimal import getcontext
mytextgrid_path = str(pathlib.Path(__file__).parent.parent.joinpath('src'))
sys.path.insert(0, mytextgrid_path)
from mytextgrid.core.point_tier import Point
getcontext().prec = 16

class Testpoint(unittest.TestCase):
    """
    Test Point object methods.
    """
    def test_init(self):
        time = Decimal('5.145')
        point = Point(time, 'H')

        self.assertEqual(point.text, 'H')
        self.assertNotEqual(point.text, 'L')

        with self.assertRaises(TypeError):
            # test type errors when assigning values to attributes
            point.text = 3

        self.assertEqual(point._time, time)
        self.assertEqual(point.time, time)
        self.assertEqual(point.xmin, time)
        self.assertEqual(point.xmax, time)

        self.assertIsNot(point.time, Decimal('5.14500000000000000000003'))
        self.assertIsNot(point.xmin, Decimal('5.14500000000000000000003'))
        self.assertIsNot(point.xmax, Decimal('6.324000001'))

        # Test: do not assign a value to xmin and xmax attributes
        with self.assertRaises(AttributeError):
            point.time = Decimal('10')
            point.xmin = Decimal('0.313')
            point.xmax = Decimal('0.424')

        # Test attribute assignment
        point._time = Decimal('4.3')
        self.assertEqual(point.time, Decimal('4.3'))

if __name__ == '__main__':
    unittest.main()
