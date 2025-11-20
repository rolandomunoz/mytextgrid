from mytextgrid.core.textgrid_abstract import TextGridAbstract
from mytextgrid.io.writer import write_json
from mytextgrid.io.writer import write_textgrid

def create_textgrid(xmin = 0, xmax = 1):
    """
    Create and return an empty TextGrid.

    An empty TextGrid does not contain any tier.

    Parameters
    ----------
    xmin : int, float, str or :class:`decimal.Decimal`, default 0
        The starting time of the TextGrid.
    xmax : int, float, str or :class:`decimal.Decimal`, default 1
        The ending time of the TextGrid.

    Returns
    -------
        :class:`mytextgrid.io.textgrid.TextGrid`
            A TextGrid instance.
    """
    return TextGrid(xmin, xmax)

class TextGrid(TextGridAbstract):
    """
    A class representation for a TextGrid.
    """
    def write(self, path, format_ = 'long', encoding = 'utf-8'):
        """
        Write a TextGrid object as a text file.

        Parameters
        ----------
        path : str or :class:`pathlib.Path`
            The path where the TextGrid file will be written.
        short_format : bool, default False
            ``True`` to output TextGrid file in long format. ``False`` for short format.
        encoding : str, default 'utf-8'
            The encoding of the file.
        """
        write_textgrid(self, path, format_, encoding)

    def write_as_json(self, *args, **kwds):
        """
        Write a TextGrid object as a JSON file.

        Parameters
        ----------
        path : str or :class:`pathlib.Path`
            The path where the JSON file will be written.
        encoding : str, default utf-8
            The encoding of the resulting file.
        """
        write_json(self, *args, **kwds)
