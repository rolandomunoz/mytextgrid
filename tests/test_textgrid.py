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
from mytextgrid.io.textgrid_out import textgrid_to_json
getcontext().prec = 16

class TestTextGrid(unittest.TestCase):

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

        path_in = Path(__file__).parent / 'files' / 'empty_tier.TextGrid'
        textgrid_new = read_from_file(path_in)

        self.assertEqual(textgrid_new[0].name, '')
        self.assertEqual(textgrid_new[1].name, ' luis')
        self.assertEqual(textgrid_new[2].name, 'luis alberto')
        self.assertEqual(textgrid_new[3].name, 'rolando ')

    def test_to_dict(self):
        a = self.textgrid.to_dict()

    def test_write_files(self):
        files_dir = Path(__file__).parent / 'files'

        names = (
            'Mary_John_bell-2.TextGrid',
            'Mary_John_bell-1.TextGrid',
            'empty_tier.TextGrid'
        )
        for name in names:
            path_in = files_dir / name
            path_out = files_dir.joinpath(name).with_suffix('.TextGrid.out')
            json_out = files_dir.joinpath(name).with_suffix('.TextGrid.json')

            textgrid_new = read_from_file(path_in)
            textgrid_new.write(path_out)
            textgrid_new.write_as_json(json_out)

        tg = create_textgrid(0, 10)
        tg.write(files_dir / 'empty.TextGrid')

if __name__ == '__main__':
    unittest.main()
