from mytextgrid.io import long

def read_textgrid(filepath, format_ = 'long', encoding = None):
    if format_ == 'long':
        return read_long(filepath, encoding)

def read_long(filepath, encoding = None):
    """
    Read a TextGrid file with full text format and return a TextGrid object.

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
    textgrid_dict = long.parse_textgrid_file(filepath, encoding)
    textgrid_obj = long.dict_to_textgrid(textgrid_dict)
    return textgrid_obj

def read_textgrid_from_stream(*args, **kwds):
    """
    Read a stream into a TextGrid object.

    Parameters
    ----------
    stream : str or :class:`io.StringIO`
        The content of a full-formatted TextGrid.
    name : str
        The name of the TextGrid.
    path : str or :class:`pathlib.Path`
        The path of the TextGrid.

    Returns
    -------
        :class:`mytextgrid.TextGrid`
            A TextGrid instance.
            A TextGrid instance.
    """
    textgrid_dict = long.parse(*args, **kwds)
    textgrid_obj = long.dict_to_textgrid(textgrid_dict)
    return textgrid_obj
