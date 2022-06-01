from mytextgrid.io.parser import full_text_format

def read_from_file(path, encoding = None):
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
    textgrid_dict = full_text_format.textgrid_to_dict(path, encoding)
    textgrid_obj = full_text_format.dict_to_textgrid(textgrid_dict)
    return textgrid_obj
