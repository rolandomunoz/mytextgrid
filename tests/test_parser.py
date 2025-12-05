import sys
import pprint
import unittest
from pathlib import Path

package_dir = Path(__file__).parent.parent.joinpath('src')
sys.path.insert(0, str(package_dir))

from mytextgrid.io import text_parser

class TestTextGridParser(unittest.TestCase):
    """
    Test Point object methods.
    """
    def setUp(self):
        self.src_dir = Path(__file__).parent / 'files/encodings'
        self.fnames = [
            #("text-UTF16BE-LONG-CR.TextGrid", True),
            #("text-UTF16LE-LONG-CR.TextGrid", True),
            #("text-UTF8-LONG-CR.TextGrid", True),
            #("text-UTF8-LONG-CRLF.TextGrid", True),
            ("text-UTF8-LONG-LF.TextGrid", True),
            #("text-UTF8-SHORT-CR.TextGrid", True),
            #("text-UTF8-SHORT-CRLF.TextGrid", True),
            ("text-UTF8-SHORT-LF.TextGrid", True),
        ]

    def test_parse_textgrid(self):
        for fname, is_textgrid in self.fnames:
            path = self.src_dir / fname
            a = text_parser.parse_textgrid_file(path)
            print()
            print('='*20, fname, '='*20)
            pprint.pp(a)

if __name__ == '__main__':
    unittest.main()
