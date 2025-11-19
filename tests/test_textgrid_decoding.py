import sys
import unittest

package_dir = Path(__file__).parent.parent.joinpath('src')
sys.path.insert(0, str(package_dir))

from mytextgrid import read_from_file

class TestTextGrid(unittest.TestCase):

    def setUp(self):
        self.file_list = [
            'text-linux-iso_latin1.TextGrid',
            'text-linux-macroman.TextGrid',
            'text-linux-utf8.TextGrid',
            'text-linux-window_latin1.TextGrid',
        ]

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
