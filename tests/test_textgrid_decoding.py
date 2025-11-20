import sys
import unittest
from pathlib import Path

package_dir = Path(__file__).parent.parent.joinpath('src')
sys.path.insert(0, str(package_dir))

from mytextgrid import io

class TestTextGrid(unittest.TestCase):

    def setUp(self):
        self.file_list = [
            'files/text-linux-iso_latin1.TextGrid',
            'files/text-linux-utf8.TextGrid',
            'files/text-linux-utf16.TextGrid',
        ]

    def test_read_any_encoding(self):
        for path in self.file_list:
            tg = io.read_textgrid(path)

    def test_read_long_utf_8(self):
        pass

    def test_read_long_utf_16(self):
        pass

    def test_read_long_latin_1(self):
        pass

    def test_read_long_macroman(self):
        pass

if __name__ == '__main__':
    unittest.main()
