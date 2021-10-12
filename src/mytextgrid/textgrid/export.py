"""Export TextGrid files to other formats"""
import csv
import json

def to_textgrid(textgrid_obj, path, encoding = 'utf-8'):
    """Write TextGrid to a text file.

    Parameters
    ----------
    textgrid_obj : TextGrid
        Data stored in a TextGrid.
    path : str
        The path where the TextGrid file will be created.
    encoding : str, default utf-8
        The encoding of the resulting file.
    """
    tg_header = ['File type = "ooTextFile"',
        'Object class = "TextGrid"\n',
        f'xmin = {textgrid_obj.xmin} ',
        f'xmax = {textgrid_obj.xmax} ',
        'tiers? <exists> ',
        f'size = {len(textgrid_obj)} ',
        'item []: ']

    with open(path, 'w', encoding = encoding) as file:
        for line in tg_header:
            file.write(line + '\n')

        for tier_position, tier in enumerate(textgrid_obj, start = 1):
            if tier.is_interval():
                tier_class, items_name = ('IntervalTier', 'intervals')
            else:
                tier_class, items_name = ('TextTier', 'points')

            file.write(f'    item [{tier_position}]:\n'.format())
            file.write(f'        class = "{tier_class}" \n')
            file.write(f'        name = "{tier.name}" \n')
            file.write(f'        xmin = {tier.xmin} \n')
            file.write(f'        xmax = {tier.xmax} \n')
            file.write(f'        {items_name}: size = {len(tier)} \n')

            if tier.is_interval():
                # IntervalTier class
                for item_position, item in enumerate(tier, start = 1):
                    file.write(f'        intervals [{item_position}]:\n')
                    file.write(f'            xmin = {item.xmin} \n')
                    file.write(f'            xmax = {item.xmax} \n')
                    file.write(f'            text = "{item.text}" \n')
            else:
                # PointTier class
                for item_position, item in enumerate(tier, start = 1):
                    file.write(f'        points [{item_position}]:\n')
                    file.write(f'            number = {item.time} \n')
                    file.write(f'            mark = "{item.text}" \n')

def to_csv(textgrid_obj, path, encoding = 'utf-8'):
    """Write TextGrid to a csv file.

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
    By using this method, `TextGrid` is converted to a table where non-empty items (`Interval`
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
    """Write TextGrid to a json file.

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
        json.dump(textgrid, file_object, indent = 4)
