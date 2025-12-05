"""Parse TextGrid files in long and short formats.
"""
from mytextgrid.io.utils import detect_textgrid_encoding, is_textgrid_file

_DECIMAL_CHARS = {'.', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}

def parse_textgrid_file(fpath, encoding=None):
    """
    Parse a TextGrid file in long or short formats to a dict.
    """
    if not is_textgrid_file(fpath, False):
        return None

    if encoding is None:
        encoding = detect_textgrid_encoding(fpath)

    with open(fpath, 'r', encoding=encoding) as f:
        raw_text = f.read()

    label_list = []
    # SOT: Start of Label
    # CT: collect Label
    # EOT: End of Label
    # EON:
    # '0000 0000' = ~CL, ~SOL, ~EOL
    # '0000 0001' = ~CL, ~SOL, EOL
    # '0000 0010' = ~CL, SOL, ~EOL
    # '0000 0011' = ~CL, SOL, EOL
    #'GLOBAL_XMIN' -> 'GLOBAL_XMAX'
    #'GLOBAL_XMAX' -> 'GLOBAL_SIZE'
    #'GLOBAL_SIZE' -> 'TIER_CLASS'
    #'TIER_CLASS' -> 'TIER_NAME'
    #'TIER_NAME'
    #'ITEM_TEXT'
    #'ITEM_XMAX'

    state = 'GLOBAL_XMIN'
    sub_state = 'start' # {'start', 'store', 'finish'}

    _buffer = []
    dictgrid = {}
    skip_character = False
    for ind, char in enumerate(raw_text):
        if skip_character:
            skip_character = False
            continue

        if state == 'GLOBAL_XMIN':

            if sub_state == 'start':
                if char.isdecimal():
                    sub_state = 'store'
                    _buffer = []

            if sub_state == 'store':
                if char in _DECIMAL_CHARS:
                    _buffer.append(char)
                else:
                    sub_state = 'finish'

            if sub_state == 'finish':
                dictgrid['xmin'] = ''.join(_buffer)
                state = 'GLOBAL_MAX'
                sub_state = 'start'

        elif state == 'GLOBAL_MAX':

            if sub_state == 'start':
                if char.isdecimal():
                    sub_state = 'store'
                    _buffer = []

            if sub_state == 'store':
                if char in _DECIMAL_CHARS:
                    _buffer.append(char)
                else:
                    sub_state = 'finish'

            if sub_state == 'finish':
                dictgrid['xmax'] = ''.join(_buffer)
                state = 'GLOBAL_SIZE'
                sub_state = 'start'

        elif state == 'GLOBAL_SIZE':

            if sub_state == 'start':
                if char.isdecimal():
                    sub_state = 'store'
                    _buffer = []

            if sub_state == 'store':
                if char.isdecimal():
                    _buffer.append(char)
                else:
                    sub_state = 'finish'

            if sub_state == 'finish':
                tier_index = 0
                global_size = int(''.join(_buffer))
                dictgrid['size'] = global_size
                dictgrid['tiers'] = [None]*global_size

                state = 'TIER_CLASS'
                sub_state = 'start'

        elif state == 'TIER_CLASS':
            if tier_index >= global_size:
                state = 'END'
                sub_state = ''

            if sub_state == 'start':
                if char == '"':
                    sub_state = 'store'
                    _buffer = []
                    continue # Do not include the starting quotation mark

            if sub_state == 'store':
                if char == '"':
                    sub_state = 'finish'
                else:
                    _buffer.append(char)

            if sub_state == 'finish':
                dictgrid['tiers'][tier_index] = {}
                dictgrid['tiers'][tier_index]['tier_class'] = ''.join(_buffer)
                state = 'TIER_NAME'
                sub_state = 'start'

        elif state == 'TIER_NAME':
            if sub_state == 'start':
                if char == '"':
                    sub_state = 'store'
                    _buffer = []
                    continue # Do not include the starting quotation mark

            if sub_state == 'store':
                if char == '"':
                    next_char = raw_text[ind + 1] if ind + 1 < len(raw_text) else ''
                    if next_char == '"':
                        _buffer.append(char)
                        skip_character = True
                    else:
                        sub_state = 'finish'
                else:
                    _buffer.append(char)

            if sub_state == 'finish':
                dictgrid['tiers'][tier_index]['tier_name'] = ''.join(_buffer)
                state = 'TIER_XMIN'
                sub_state = 'start'

        elif state == 'TIER_XMIN':
            if sub_state == 'start':
                if char.isdecimal():
                    sub_state = 'store'
                    _buffer = []

            if sub_state == 'store':
                if char in _DECIMAL_CHARS:
                    _buffer.append(char)
                else:
                    sub_state = 'finish'

            if sub_state == 'finish':
                dictgrid['tiers'][tier_index]['tier_xmin'] = ''.join(_buffer)
                state = 'TIER_XMAX'
                sub_state = 'start'

        elif state == 'TIER_XMAX':
            if sub_state == 'start':
                if char.isdecimal():
                    sub_state = 'store'
                    _buffer = []

            if sub_state == 'store':
                if char in _DECIMAL_CHARS:
                    _buffer.append(char)
                else:
                    sub_state = 'finish'

            if sub_state == 'finish':
                dictgrid['tiers'][tier_index]['tier_xmax'] = ''.join(_buffer)
                state = 'TIER_SIZE'
                sub_state = 'start'

        elif state == 'TIER_SIZE':
            if sub_state == 'start':
                if char.isdecimal():
                    sub_state = 'store'
                    _buffer = []

            if sub_state == 'store':
                if char.isdecimal():
                    _buffer.append(char)
                else:
                    sub_state = 'finish'

            if sub_state == 'finish':
                item_index = 0
                tier_size = int(''.join(_buffer))
                dictgrid['tiers'][tier_index]['tier_size'] = tier_size
                dictgrid['tiers'][tier_index]['items'] = [None]*tier_size
                if dictgrid['tiers'][tier_index]['tier_class'] == 'IntervalTier':
                    state = 'ITEM_XMIN'
                elif dictgrid['tiers'][tier_index]['tier_class'] == 'TextTier':
                    state = 'ITEM_NUMBER'
                else:
                    state = ''
                sub_state = 'start'

        elif state == 'ITEM_NUMBER':
            if sub_state == 'start':
                if char.isdecimal():
                    sub_state = 'store'
                    _buffer = []

            if sub_state == 'store':
                if char in _DECIMAL_CHARS:
                    _buffer.append(char)
                elif char == ']':
                    sub_state = 'start'
                else:
                    sub_state = 'finish'

            if sub_state == 'finish':
                dictgrid['tiers'][tier_index]['items'][item_index] = {}
                dictgrid['tiers'][tier_index]['items'][item_index]['item_point'] = ''.join(_buffer)
                state = 'ITEM_TEXT'
                sub_state = 'start'

        elif state == 'ITEM_XMIN':
            if sub_state == 'start':
                if char.isdecimal():
                    sub_state = 'store'
                    _buffer = []

            if sub_state == 'store':
                if char in _DECIMAL_CHARS:
                    _buffer.append(char)
                elif char == ']':
                    sub_state = 'start'
                else:
                    sub_state = 'finish'

            if sub_state == 'finish':
                dictgrid['tiers'][tier_index]['items'][item_index] = {}
                dictgrid['tiers'][tier_index]['items'][item_index]['item_xmin'] = ''.join(_buffer)
                state = 'ITEM_XMAX'
                sub_state = 'start'

        elif state == 'ITEM_XMAX':

            if sub_state == 'start':
                if char.isdecimal():
                    sub_state = 'store'
                    _buffer = []

            if sub_state == 'store':
                if char in _DECIMAL_CHARS:
                    _buffer.append(char)
                elif char == ']':
                    sub_state = 'start'
                else:
                    sub_state = 'finish'

            if sub_state == 'finish':
                dictgrid['tiers'][tier_index]['items'][item_index]['item_xmax'] = ''.join(_buffer)
                state = 'ITEM_TEXT'
                sub_state = 'start'

        elif state == 'ITEM_TEXT':
            if item_index >= tier_size:
                state = 'TIER_CLASS'
                sub_state = 'start'
                continue

            if sub_state == 'start':
                if char == '"':
                    sub_state = 'store'
                    _buffer = []
                    continue # Do not include the starting quotation mark

            if sub_state == 'store':
                if char == '"':
                    next_char = raw_text[ind + 1] if ind + 1 < len(raw_text) else ''
                    if next_char == '"':
                        _buffer.append(char)
                        skip_character = True
                    else:
                        sub_state = 'finish'
                else:
                    _buffer.append(char)

            if sub_state == 'finish':
                dictgrid['tiers'][tier_index]['items'][item_index]['item_text'] = ''.join(_buffer)
                item_index += 1
                if item_index < tier_size:
                    if dictgrid['tiers'][tier_index]['tier_class'] == 'IntervalTier':
                        state = 'ITEM_XMIN'
                    elif dictgrid['tiers'][tier_index]['tier_class'] == 'TextTier':
                        state = 'ITEM_NUMBER'
                    else:
                        state = ''
                else:
                    item_index += 0
                    tier_index += 1
                    state = 'TIER_CLASS'
                sub_state = 'start'

    return dictgrid
