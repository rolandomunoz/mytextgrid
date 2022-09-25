"""
Export TextGrid files to other formats
"""
import csv
import json
from jinja2 import Environment, PackageLoader, select_autoescape
from pathlib import Path

def to_textgrid(textgrid_obj, dst_path, encoding = 'utf-8'):
    env = Environment(
        loader=PackageLoader('mytextgrid.io'),
        autoescape=select_autoescape()
    )
    env.trim_blocks = True
    env.lstrip_blocks  = True

    # Variales
    dict_ = textgrid_obj.to_dict()
    template = env.get_template('long_textgrid_format.TextGrid.jinja')
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

def to_json(textgrid_obj, path, encoding = 'utf-8'):
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
    textgrid = {
        'xmin': str(textgrid_obj.xmin),
        'xmax': str(textgrid_obj.xmax),
        'tiers': []
        }
    for tier in textgrid_obj:
        tier_class = 'IntervalTier' if tier.is_interval() else 'TextTier'

        textgrid['tiers'].append(
            {
            'class':tier_class,
            'name':tier.name,
            'items':[]
            }
            )

        for item in tier:
            if tier.is_interval():
                # If IntervalTier
                textgrid['tiers'][-1]['items'].append(
                {
                'xmin':str(item.xmin),
                'xmax':str(item.xmax),
                'text':item.text
                }
                )
            else:
                # If PointTier
                textgrid['tiers'][-1]['items'].append(
                {
                'number':str(item.time),
                'mark':item.text
                }
                )

        with open(path, 'w', encoding = encoding) as file_object:
            json.dump(textgrid, file_object, ensure_ascii = False, indent = 4)
