"""
Export TextGrid files to other formats
"""
import csv
import json
from decimal import Decimal
from jinja2 import Environment, PackageLoader, select_autoescape
from pathlib import Path

def textgrid_to_text_file(textgrid_obj, dst_path, short_format = False, encoding = 'utf-8'):
    """
    Write a TextGrid object to a text file.

    Parameters
    ----------
    textgrid_obj : 
        A TextGrid object.
    dst_path : str or :class:`pathlib.Path`
        The path where the text file will be stored.
    short_format : boolean, default `False`
        True for short format of the text file. Otherwirse, long format is applied.
    encoding: str, default 'utf-8'
        The encoding of the text file.
    """
    env = Environment(
        loader=PackageLoader('mytextgrid.io'),
        autoescape=select_autoescape()
    )
    env.trim_blocks = True
    env.lstrip_blocks  = True

    # Variales
    dict_ = textgrid_obj.to_dict()
    template_name = 'short_format.TextGrid.jinja'if short_format else 'long_format.TextGrid.jinja'
    template = env.get_template(template_name)
    textgrid_str = template.render(textgrid = dict_)

    with open(dst_path, 'w', encoding = encoding) as textfile:
        textfile.write(textgrid_str)

def to_csv(textgrid_obj, path, encoding = 'utf-8'):
    """
    Write TextGrid to a csv file.

    Parameters
    ----------
    textgrid_obj : TextGrid
        Data stored in a TextGrid.
    path : str
        The path where the delimited text file will be created.
    encoding : str, default utf-8
        The encoding of the resulting file.

    Notes
    -----
    By using this function, `TextGrid` is converted to a table where non-empty items (`Interval`
    and `Point`) become rows. Each item (row) is stored along with the tier it belongs to and
    its timestamps. When the table is done, the items (rows) are sorted by time in ascending
    order. Finally, the table is exported as a delimited text file.
    """
    table = []
    for tier in textgrid_obj:
        for item in tier:
            if item.text == '':
                continue
            if tier.is_interval():
                # IntervalTier class
                table.append([item.xmin, tier.name, item.text, item.xmax])
            else:
                # PointTier class
                table.append([item.time, tier.name, item.text, item.time])
    table.sort(key=lambda x:x[0])

    with open(path, 'w', encoding = encoding, newline = '') as file_object:
        spamwriter = csv.writer(file_object)
        spamwriter.writerow(['tmin', 'tier_name', 'text', 'tmax'])
        for row in table:
            spamwriter.writerow([str(item) for item in row])

def textgrid_to_json(textgrid_obj, path, encoding = 'utf-8'):
    """
    Write TextGrid to a json file.

    Parameters
    ----------
    textgrid_obj : TextGrid
        Data stored in a TextGrid.
    path : str
        The path where the delimited text file will be created.
    encoding : str, default utf-8
        The encoding of the resulting file.
    """
    dict_ = textgrid_obj.to_dict()
    with open(path, 'w', encoding = encoding) as file_object:
        json.dump(dict_, file_object, cls = _DecimalEncoder, ensure_ascii = False, indent = 4)

class _DecimalEncoder(json.JSONEncoder):
    """
    JSON encoder for TextGrid.
    """
    def default(self, decimal_number):
        if isinstance(decimal_number, Decimal):
            return str(decimal_number)
        else:
            return super().default(decimal_number)
