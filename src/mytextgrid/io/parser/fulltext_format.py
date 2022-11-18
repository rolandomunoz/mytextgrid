"""Parse TextGrid files in full text format into TextGrid objects"""
import decimal
import re
from io import StringIO
from pathlib import Path
import chardet
from mytextgrid.core.textgrid import TextGrid
decimal.getcontext().prec = 16

def parse_textgrid_file(path, encoding = None):
    """
    Parse a full text TextGrid file into a dict.

    Parameters
    ----------
    path : str or :class:`pathlib.Path`
        The path of the TextGrid file.
    encoding : str or None, default None
        The encoding of the TextGrid file. If None, the function will figure out
        the encoding.
    """
    if isinstance(path, str):
        path = Path(path)

    # Open file
    if encoding is None:
        encoding = _detect_encoding(path)

    with open(path, 'r', encoding = encoding) as file_object:
        dict_ = parse(file_object)
        dict_['basename'] = path.stem
        dict_['path'] = path
    return dict_

def parse(stream, name = None, path = None):
    """
    Parse a full text TextGrid file into a dict.

    {
        'basename': str,
        'path': :class:`pathlib.Path`,
        'xmin': str,
        'xmax': str,
        'tiers': [
            {
                class: str,
                tier_name: str,
                items: [
                    {
                        'xmin': str
                        'xmax': str
                        '{"text", "mark"}': str
                    },
                    .
                    .
                    .
                ]
            },
            .
            .
            .
        ]
    }

    Parameters
    ----------
    stream : str or :class:`io.StringIO`
        The content of a full-formatted TextGrid.
    name : str
        The name of the TextGrid
    path : str or :class:`pathlib.Path`
        The path of the TextGrid

    Returns
    -------
        dict
            A `dict` representation of the TextGrid file.
    """
    if isinstance(stream, str):
        stream = StringIO(stream)
    if isinstance(path, str):
        path = Path(path)

    textgrid = {
        'basename': name,
        'path': path,
        'xmin': None,
        'xmax': None,
        'tiers':[]
    }

    line = stream.readline()
    while line:
        key, match = _parse_line(line)
        # Check header
        if key == 'file_type':
            file_type = match.group(key)
            if not file_type == 'ooTextFile':
                raise OSError('The stream is not a Praat object.')

        if key == 'object_class':
            object_class = match.group(key)
            if not object_class == 'TextGrid':
                raise OSError('The stream is not a TextGrid.')

        # TextGrid info
        if key == 'tg_xmin':
            textgrid['xmin'] = match.group(key)

        if key == 'tg_xmax':
            textgrid['xmax'] = match.group(key)

        # Tier info
        if key == 'tier_class':
            textgrid['tiers'].append(
                {
                'class': match.group(key),
                'tier_name':None,
                'items': []
                }
            )

        if key == 'tier_name':
            textgrid['tiers'][-1]['tier_name'] = match.group(key)

        # Item content
        if key == 'interval_xmin':
            textgrid['tiers'][-1]['items'].append(
                {
                'xmin': match.group(key),
                'xmax': None,
                'text': None
                }
            )

        if key == 'interval_xmax':
            textgrid['tiers'][-1]['items'][-1]['xmax'] = match.group(key)

        if key == 'point_number':
            textgrid['tiers'][-1]['items'].append(
                {'number':match.group(key),
                'mark':None
                }
            )

        if key in ('interval_text', 'point_mark'):
            type_label = 'text' if key == 'interval_text' else 'mark'
            text = match.group(key).replace('""', '"')
            textgrid['tiers'][-1]['items'][-1][type_label] = text

        # If the text or mark field has multiple lines, read the those
        # lines until the last.
        if key in ('interval_text2', 'point_mark2'):
            text = match.group(key) + '\n'
            enditem_pattern = re.compile('(.*)" $')
            type_label = 'text' if key == 'interval_text2' else 'mark'
            item = textgrid['tiers'][-1]['items'][-1]

            while line:
                line = stream.readline()
                match = enditem_pattern.match(line)
                if match:
                    # Check the last character not to be a `"" \n`
                    if not line.endswith('"" \n'):
                        text = text + match.group(1)
                        item[type_label] = text.replace('""', '"')
                        break
                text = text + line
        line = stream.readline()
    return textgrid

def dict_to_textgrid(textgrid):
    """
    Build and return a :clas:`mytextgrid.TextGrid` from a dict formatted TextGrid.

    Parameters
    ----------
    textgrid : dict of a TextGrid
        A dict formatted created by :meth:`FullTextParser.full_textgrid_to_dict`.

    Returns
    -------
        :class:`mytextgrid.TextGrid`
            A TextGrid object.

    See also
    --------
    mytextgrid.Parser.full_textgrid_to_dict : Returns a dict formatted str created from a
    TextGrid file.
    """
    # Init TextGrid object
    textgrid_obj = TextGrid(
        xmin = decimal.Decimal(textgrid['xmin']),
        xmax = decimal.Decimal(textgrid['xmax'])
        )

    for tier in textgrid['tiers']:
        tier_class = tier['class']
        tier_name = tier['tier_name']

        if tier_class == 'IntervalTier':
            # Insert interval tier
            tier_obj = textgrid_obj.insert_tier(tier_name)

            # Insert interval
            for loc, item in enumerate(tier['items']):
                # Insert boundary.
                if not loc == 0:
                    tier_obj.insert_boundaries(
                        decimal.Decimal(item['xmin'])
                    )
                # Insert text
                tier_obj.set_text_at_index(loc, item['text'])

        if tier_class == 'TextTier':
            # Insert tier
            tier_obj = textgrid_obj.insert_tier(tier_name, False)
            for item in tier['items']:
                # Insert Point
                tier_obj.insert_point(
                    decimal.Decimal(item['number']),
                    item['mark']
                )
    return textgrid_obj

def _parse_line(line):
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
    _patterns_dict = {
        'file_type': re.compile('File type = "(?P<file_type>.+)"'),
        'object_class': re.compile('Object class = "(?P<object_class>.+)"'),
        'tg_xmin': re.compile('xmin = (?P<tg_xmin>.+) '),
        'tg_xmax': re.compile('xmax = (?P<tg_xmax>.+) '),
        'tier_exists': re.compile(r'tiers? <(?P<tier_exists>.+)> '),
        'tiers': re.compile(r'size = (?P<tiers>\d+) '),
        'tier_loc': re.compile(r' {4}item [(?P<tier_loc>\d+)]'),
        'tier_class': re.compile(' {8}class = "(?P<tier_class>.+)" '),
        'tier_name': re.compile(' {8}name = "(?P<tier_name>.*)" '),
        'tier_xmin': re.compile(' {8}xmin = (?P<tier_xmin>.+) '),
        'tier_xmax': re.compile(' {8}xmax = (?P<tier_xmax>.+) '),
        'intervals': re.compile(r' {8}intervals: size = (?P<intervals>\d+) '),
        'interval_loc': re.compile(r' {8}intervals [(?P<interval_loc>\d+)]:'),
        'interval_xmin': re.compile(' {12}xmin = (?P<interval_xmin>.+) '),
        'interval_xmax': re.compile(' {12}xmax = (?P<interval_xmax>.+) '),
        'interval_text': re.compile(' {12}text = "(?P<interval_text>.*)" '),
        'interval_text2': re.compile(' {12}text = "(?P<interval_text2>.*)'),
        'points': re.compile(r' {8}points: size = (?P<points> \d+) '),
        'point_loc': re.compile(r' {8}points [(?P<point_loc>\d+)]:'),
        'point_number': re.compile(' {12}number = (?P<point_number>.+) '),
        'point_mark': re.compile(' {12}mark = "(?P<point_mark>.*)" '),
        'point_mark2': re.compile(' {12}mark = "(?P<point_mark2>.*)')
    }
    for key, pattern in _patterns_dict.items():
        match = pattern.match(line)
        if match:
            return key, match
    return None, None

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
