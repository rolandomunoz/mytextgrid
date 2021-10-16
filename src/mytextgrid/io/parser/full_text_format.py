"""Parse TextGrid files in full text format into TextGrid objects"""
import decimal
import os
import json
import re
import chardet
from mytextgrid.core.textgrid import TextGrid
decimal.getcontext().prec = 16

def read_from_file(path, encoding = None):
    """
    Read a TextGrid file and return a TextGrid object.

    Parameters
    ----------
        path : str
            The path of the TextGrid file.
        encoding : str, default None, detect automatically the encoding.
            The name of the encoding used to decode the file. See the codecs module for the list
            supported encodings.

    Returns
    -------
        :class:`mytextgrid.TextGrid`
            A TextGrid instance.
    """
    parser = FullTextParser()
    textgrid_json = parser.full_textgrid_to_json(path, encoding)
    return parser.json_to_textgrid(textgrid_json)

class FullTextParser:
    """
    This class implements methods for parsing TextGrid in full text format.
    """
    def __init__(self):
        self._pattern_dict = {
        'file_type': re.compile('File type = "(?P<file_type>.+)"'),
        'object_class': re.compile('Object class = "(?P<object_class>.+)"'),
        'tg_xmin': re.compile('xmin = (?P<tg_xmin>.+) '),
        'tg_xmax': re.compile('xmax = (?P<tg_xmax>.+) '),
        'tier_exists': re.compile(r'tiers? <(?P<tier_exists>.+)> '),
        'tiers': re.compile(r'size = (?P<tiers>\d+) '),
        'tier_loc': re.compile(r' {4}item [(?P<tier_loc>\d+)]'),
        'tier_class': re.compile(' {8}class = "(?P<tier_class>.+)" '),
        'tier_name': re.compile(' {8}name = "(?P<tier_name>.+)" '),
        'tier_xmin': re.compile(' {8}xmin = (?P<tier_xmin>.+) '),
        'tier_xmax': re.compile(' {8}xmax = (?P<tier_xmax>.+) '),
        'intervals': re.compile(r' {8}intervals: size = (?P<intervals>\d+) '),
        'interval_loc': re.compile(r' {8}intervals [(?P<interval_loc>\d+)]:'),
        'interval_xmin': re.compile(' {12}xmin = (?P<interval_xmin>.+) '),
        'interval_xmax': re.compile(' {12}xmax = (?P<interval_xmax>.+) '),
        'interval_text': re.compile(' {12}text = "(?P<interval_text>.*)" '),
        'points': re.compile(r' {8}points: size = (?P<points> \d+) '),
        'point_loc': re.compile(r' {8}points [(?P<point_loc>\d+)]:'),
        'point_number': re.compile(' {12}number = (?P<point_number>.+) '),
        'point_mark': re.compile(' {12}mark = "(?P<point_mark>.*)" ')
        }

    def _parse_line(self, line):
        """
        Test if a list of patterns stored in dictonary match a text line.

        Parameters
        ----------
        line : str
            Any line in full textgrid format that comes from a TextGrid file.

        Returns
        -------
            (key, match), tuple of (str, re.Match)
                Return the key of the pattern that matches the line and the `re.Match`.
                If no key matches the line, return (None, None)
        """
        for key, pattern in self._pattern_dict.items():
            match = pattern.match(line)
            if match:
                return key, match
        return None, None

    def full_textgrid_to_json(self, path, encoding = None):
        """
        Parse a full text TextGrid file into a JSON formatted str.

        Parameters
        ----------
        path : str
            A JSON formatted str created from a TextGrid file.
        encoding : str, default None, detect automatically the encoding.
            The name of the encoding used to decode the file. See the codecs module for the list
            supported encodings.

        Returns
        -------
            TextGrid
                A TextGrid with the JSON formatted str content.

        See also
        --------
        mytextgrid.Parser.full_textgrid_to_json : Returns a JSON formatted str created from a
        TextGrid file.
        """
        basename = os.path.splitext(os.path.basename(path))[0]

        textgrid = {'basename':basename,
            'path':path,
            'xmin':None,
            'xmax':None,
            'tiers':[]
            }

        # Open file
        if encoding is None:
            encoding = self._detect_encoding(path)

        with open(path, 'r', encoding = encoding) as file_object:
            line = file_object.readline()
            while line:
                key, match = self._parse_line(line)

                # Check header
                if key == 'file_type':
                    file_type = match.group('file_type')
                    if not file_type == 'ooTextFile':
                        raise OSError(f'The file {path} is not a Praat object.')
                if key == 'object_class':
                    object_class = match.group('object_class')
                    if not object_class == 'TextGrid':
                        raise OSError(f'The file {path} is not a TextGrid.')

                # TextGrid info
                if key == 'tg_xmin':
                    textgrid['xmin'] = match.group('tg_xmin')

                if key == 'tg_xmax':
                    textgrid['xmax'] = match.group('tg_xmax')

                # Tier info
                if key == 'tier_class':
                    textgrid['tiers'].append(
                        {
                        'class': match.group('tier_class'),
                        'tier_name':None,
                        'items':[]
                        })

                if key == 'tier_name':
                    textgrid['tiers'][-1]['tier_name'] = match.group('tier_name')

                # Item content
                if key == 'interval_xmin':
                    textgrid['tiers'][-1]['items'].append(
                        {
                        'xmin':match.group('interval_xmin'),
                        'xmax':None,
                        'text':None
                        })

                if key == 'interval_xmax':
                    textgrid['tiers'][-1]['items'][-1]['xmax'] = match.group('interval_xmax')

                if key == 'interval_text':
                    a= match.group('interval_text')
                    textgrid['tiers'][-1]['items'][-1]['text'] = match.group('interval_text')

                if key == 'point_number':
                    textgrid['tiers'][-1]['items'].append(
                        {'number':match.group('point_number'),
                        'mark':None
                        })

                if key == 'point_mark':
                    textgrid['tiers'][-1]['items'][-1]['mark'] = match.group('point_mark')
                line = file_object.readline()
        return json.dumps(textgrid)

    @staticmethod
    def json_to_textgrid(textgrid_json_str):
        """
        Build and return a TextGrid from a JSON formatted str.

        Parameters
        ----------
        textgrid_json_str : str
            A JSON formatted str created by `self.full_textgrid_to_json`.

        Returns
        -------
            TextGrid
                A TextGrid with the JSON formatted str content.
        """
        textgrid = json.loads(textgrid_json_str)

        # Init TextGrid object

        textgrid_obj = TextGrid(
            name = textgrid['basename'],
            xmin = decimal.Decimal(textgrid['xmin']),
            xmax = decimal.Decimal(textgrid['xmax'])
            )

        for tier in textgrid['tiers']:
            tier_class = tier['class']
            tier_name = tier['tier_name']

            if tier_class == 'IntervalTier':
                # Insert interval tier
                tier_obj = textgrid_obj.insert_interval_tier(tier_name)

                # Insert interval
                for loc, item in enumerate(tier['items']):
                    # Insert boundary.
                    if not loc == 0:
                        tier_obj.insert_boundaries(
                            decimal.Decimal(item['xmin'])
                        )
                    # Insert text
                    tier_obj.set_text(loc, item['text'])

            if tier_class == 'TextTier':
                # Insert tier
                tier_obj = textgrid_obj.insert_point_tier(tier_name)
                for item in tier['items']:
                    # Insert Point
                    tier_obj.insert_point(
                        decimal.Decimal(item['number']),
                        item['mark']
                    )
        return textgrid_obj

    @staticmethod
    def _detect_encoding(path):
        """
        Detect and return a file encoding.

        Parameters
        ----------
        path : str
            The path of a text file.

        Returns
        -------
            str
                The detected encoding name of the specified file.
        """
        with open(path, 'rb') as file_object:
            rawdata = file_object.read()
            result = chardet.detect(rawdata)
            return result.get('encoding')
