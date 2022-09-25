import sys
import unittest
from pathlib import Path
from copy import copy
from decimal import Decimal
from decimal import getcontext
mytextgrid_path = str(Path(__file__).parent.parent.joinpath('src'))
sys.path.insert(0, mytextgrid_path)
from mytextgrid import create_textgrid
from mytextgrid import read_from_file
getcontext().prec = 16

class TestTextGrud(unittest.TestCase):

    def setUp(self):
        self.textgrid = create_textgrid(0, 1)
        self.textgrid.insert_tier('phon')
        self.textgrid.insert_tier('word')
        self.textgrid.insert_tier('word', False)
        self.textgrid.insert_tier('word')
        self.textgrid.insert_tier('phrase', False, -10)
        self.textgrid.insert_tier('comments about word')

    def test_init(self):
        textgrid = create_textgrid(0, 1)
        textgrid = create_textgrid(-1, 1.32)

        with self.assertRaises(AssertionError):
            textgrid = create_textgrid(1, 0) # Raise error: xmin > xmax

    def test_attribute(self):
        with self.assertRaises(AttributeError):
            self.textgrid.xmin = 1
            self.textgrid.xmax = 3
            self.textgrid.tiers = []

    def test_get_duration(self):
        self.assertEqual(self.textgrid.get_duration(), 1)

    def test_get_tier_by_name(self):
        self.assertEqual(len(self.textgrid.get_tier_by_name('word')), 3)

    def test_to_dict(self):
        a = self.textgrid.to_dict()

    def test_write(self):
        path_out = Path(__file__).parent / 'test.TextGrid'
        path_in = path_out.parent / 'Mary_John_bell-1.TextGrid'
        textgrid_new = read_from_file(path_in)
        textgrid_new.write(path_out)

if __name__ == '__main__':
    unittest.main()
