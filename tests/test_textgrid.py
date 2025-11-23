import sys
import unittest
import hashlib
from pathlib import Path
from copy import copy
from decimal import Decimal
from decimal import getcontext

src_dir = Path(__file__).parent.parent.joinpath('src')
sys.path.insert(0, str(src_dir))

from mytextgrid import create_textgrid
from mytextgrid import read_textgrid

getcontext().prec = 16

class TestTextGrid(unittest.TestCase):

    def setUp(self):
        self.textgrid = create_textgrid(0, 1)
        phon_tier = self.textgrid.insert_tier('phon')
        self.textgrid.insert_tier('word')
        self.textgrid.insert_tier('word', False)
        self.textgrid.insert_tier('word')
        self.textgrid.insert_tier('phrase', False, -10)
        self.textgrid.insert_tier('comments about word')

        lindex, _ = phon_tier.insert_boundary(0.1)
        phon_tier.insert_boundary(0.2)
        phon_tier.insert_boundary(0.3)
        phon_tier.insert_boundary(0.4)

        phon_tier.set_text_at_index(lindex, 'a', 'b', 'c', 'd')

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
        self.assertEqual(self.textgrid.duration(), 1)

    def test_get_tier_by_name(self):
        self.assertEqual(len(self.textgrid.get_tier_by_name('word')), 3)

        path_in = Path(__file__).parent / 'files' / 'empty_tier.TextGrid'
        textgrid_new = read_textgrid(path_in)

        self.assertEqual(textgrid_new[0].name, '')
        self.assertEqual(textgrid_new[1].name, ' luis')
        self.assertEqual(textgrid_new[2].name, 'luis alberto')
        self.assertEqual(textgrid_new[3].name, 'rolando ')

    def test_to_dict(self):
        a = self.textgrid.to_dict()

    def test_write_files(self):
        files_dir = Path(__file__).parent / 'files'
        output_dir = files_dir.parent / 'results'
        output_dir.mkdir(parents=True, exist_ok=True)

        names = (
            'Mary_John_bell-2.TextGrid',
            'Mary_John_bell-1.TextGrid',
            'empty_tier.TextGrid'
        )
        for name in names:
            path_in = files_dir / name
            path_out = output_dir.joinpath(name).with_suffix('.TextGrid')
            json_out = output_dir.joinpath(name).with_suffix('.json')

            textgrid_new = read_textgrid(path_in)
            textgrid_new.write(path_out)
            textgrid_new.write_as_json(json_out)

            a = calculate_sha256(path_in)
            b = calculate_sha256(path_out)


        tg = create_textgrid(0, 10)
        tg.write(output_dir / 'empty.TextGrid')

    def test_parent_child_item(self):
        """
        Verify that the interval and point items return their textgrid
        and tier container.
        """
        for tier in self.textgrid:
            textgrid = tier.textgrid()
            self.assertEqual(self.textgrid, textgrid)
            for item in tier:
                self.assertEqual(item.tier(), tier)
                self.assertEqual(item.textgrid(), self.textgrid)

def calculate_sha256(path):
    with open(path, 'rb') as f:
        digest = hashlib.file_digest(f, 'sha256')
    return digest.hexdigest()

if __name__ == '__main__':
    unittest.main()
