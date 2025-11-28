import sys
import unittest
from pathlib import Path

pkg_dir = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(pkg_dir))
from mytextgrid import utils

class TestIsTextGrid(unittest.TestCase):
    """
    Test TextGrid.
    """
    def setUp(self):
        self.src_dir = Path(__file__).parent / 'files/encodings'
        self.fnames = [
            ("empty_file", False, ''),
            ("text-ISO_Latin_1-BIN.TextGrid", True, ''),
            ("text-ISO_Latin_1-LONG.TextGrid", True, 'windows-1252'),
            ("text-ISO_Latin_1-SHORT.TextGrid", True, 'windows-1252'),
            ("text-UTF16-BIN.TextGrid", True, ''),
            ("text-UTF16BE-LONG-CR.TextGrid", True, 'utf-16be'),
            ("text-UTF16BE-LONG-CRLF.TextGrid", True, 'utf-16be'),
            ("text-UTF16BE-LONG-LF.TextGrid", True, 'utf-16be'),
            ("text-UTF16BE-SHORT-CR.TextGrid", True, 'utf-16be'),
            ("text-UTF16BE-SHORT-CRLF.TextGrid", True, 'utf-16be'),
            ("text-UTF16BE-SHORT-LF.TextGrid", True, 'utf-16be'),
            ("text-UTF16LE-LONG-CR.TextGrid", True, 'utf-16le'),
            ("text-UTF16LE-LONG-CRLF.TextGrid", True, 'utf-16le'),
            ("text-UTF16LE-LONG-LF.TextGrid", True, 'utf-16le'),
            ("text-UTF16LE-SHORT-CR.TextGrid", True, 'utf-16le'),
            ("text-UTF16LE-SHORT-CRLF.TextGrid", True, 'utf-16le'),
            ("text-UTF16LE-SHORT-LF.TextGrid", True, 'utf-16le'),
            ("text-UTF8-BIN.TextGrid", True, ''),
            ("text-UTF8-LONG-CR.TextGrid", True, 'utf-8'),
            ("text-UTF8-LONG-CRLF.TextGrid", True, 'utf-8'),
            ("text-UTF8-LONG-LF.TextGrid", True, 'utf-8'),
            ("text-UTF8-SHORT-CR.TextGrid", True, 'utf-8'),
            ("text-UTF8-SHORT-CRLF.TextGrid", True, 'utf-8'),
            ("text-UTF8-SHORT-LF.TextGrid", True, 'utf-8'),
        ]
        self.bin_fnames = [
            "text-UTF16-BIN.TextGrid",
            "text-UTF8-BIN.TextGrid",
        ]

    def test_is_textgrid_file(self):
        for fname, is_textgrid, _ in self.fnames:
            path = self.src_dir / fname
            is_textgrid_file = utils.is_textgrid_file(path, True)
            self.assertEqual(is_textgrid_file, is_textgrid)

    def test_is_textgrid_file_include_binary(self):
        for fname in self.bin_fnames:
            path = self.src_dir / fname

            # Inclue binary files
            is_textgrid = utils.is_textgrid_file(path,
                                                 include_binary=True)
            self.assertEqual(is_textgrid, True)

            # Do not inclue binary files
            is_textgrid = utils.is_textgrid_file(path,
                                                 include_binary=False)
            self.assertEqual(is_textgrid, False)

    def test_detect_textgrid_encoding(self):
        for fname, _, encoding in self.fnames:
            path = self.src_dir / fname

            detected_encoding = utils.detect_textgrid_encoding(path)
            self.assertEqual(encoding, detected_encoding)

if __name__ == '__main__':
    unittest.main()
