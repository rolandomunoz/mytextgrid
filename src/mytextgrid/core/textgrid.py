"""
Create and manipulate TextGrid objects.
"""
import decimal
from mytextgrid.io import textgrid_out
from mytextgrid.core.interval_tier import IntervalTier
from mytextgrid.core.point_tier import PointTier
from mytextgrid.eval import obj_to_decimal
decimal.getcontext().prec = 16

def create_textgrid(xmin = 0, xmax = 1):
    """
    Create and return an empty TextGrid.

    By using this function, you will create an empty TextGrid.
    In order to make this instance useful, add tiers and text content.

    Parameters
    ----------
    xmin : float, default 0
        The starting time of the TextGrid.
    xmax : float, default 1
        The ending time of the TextGrid.

    Returns
    -------
        :class:`mytextgrid.TextGrid`
            A TextGrid instance.
    """
    return TextGrid(xmin, xmax)

class TextGrid:
    """
    A class representation for a TextGrid.
    """
    def __init__(self, xmin = 0, xmax = 1):
        if not isinstance(xmin, (int, float, str, decimal.Decimal)):
            raise TypeError('xmin MUST BE an int, float, str or decimal.Decimal.')
        if not isinstance(xmax, (int, float, str, decimal.Decimal)):
            raise TypeError('xmax MUST BE an int, float, str or decimal.Decimal.')

        xmin_ = obj_to_decimal(xmin)
        xmax_ = obj_to_decimal(xmax)
        assert xmax_ > xmin_, 'xmax MUST BE greater than xmin'

        # Attributes
        self._xmin = xmin_
        self._xmax = xmax_
        self._tiers = []

    @property
    def xmin(self):
        """
        Return the `_xmin` attribute
        """
        return self._xmin

    @property
    def xmax(self):
        """
        Return the `_xmax` attribute
        """
        return self._xmax

    @property
    def tiers(self):
        """
        Return the `_tiers` attribute
        """
        return self._tiers

    def __len__(self):
        return len(self._tiers)

    def __iter__(self):
        return iter(self._tiers)

    def __getitem__(self, key):
        return self._tiers[key]

    def describe(self):
        """
        Display compactly the attributes and structure of TextGrid.

        Show tier information: index, type, name and size.

        Examples
        --------
        First, read or create a :meth:`~mytextgrid.TextGrid`.

        >>> # Creating TextGrid
        >>> tg = mytextgrid.create_textgrid('perro', 0, 1)
        >>> # Inserting tiers
        >>> tone_tier = tg.insert_tier("tone", False)
        >>> segment_tier = tg.insert_tier("segment")
        >>> # Insert content into the created tiers
        >>> tone_tier.insert_point('tone', 0.66, "H")
        >>> tone_tier.insert_point('tone', 0.9, "L")
        >>> segment_tier.insert_boundaries('segment', 0.23, 0.30, 0.42, 0.62, 0.70, 0.82, 0.98)
        >>> segment_tier.set_interval_text('segment', 1, 'e', 'l', 'p', 'e', 'rr', 'o')

        Once this is done, use :meth:`~mytextgrid.describe`.

        >>> # Describing TextGrid
        >>> tg.describe()
        TextGrid:
            Name:                  perro
            Startig time (sec):    0
            Ending time (sec):     1
            Number of tiers:       2
        Tiers Summary:
        0	TextTier	tone	(size = 2)
        1	IntervalTier	segment	(size = 8)
        """
        size = len(self._tiers)

        summary = []
        for index, tier in enumerate(self._tiers):
            tier_class = 'IntervalTier' if tier.is_interval() else 'PointTier'
            summary.append(
                f'    {index}\t'
                f'{tier_class}\t'
                f'{tier.name}\t'
                f'(size = {len(tier)})'
                )

        summary_str = ''
        if size > 0:
            content = '\n'.join(summary)
            head = "Tiers summary:"
            summary_str = f'\n{head}\n{content}'

        message = (
            'TextGrid:\n'
            f'    Startig time (sec):    {self.xmin}\n'
            f'    Ending time (sec):     {self.xmax}\n'
            f'    Number of tiers:       {size}'
            f'{summary_str}'
            )
        print(message)

    def get_duration(self):
        """
        Return time duration in seconds.

        Returns
        -------
        :class:`decimal.Decimal`
            Time duration in seconds.

        Examples
        --------
        >>> tg = mytextgrid.create_textgrid('banana', 0, 1.2)
        >>> tg.get_duration()
        1.2
        """
        return self._xmax - self._xmin

    def insert_tier(self, name, interval_tier = True, index = None):
        """
        Insert a tier in the TextGrid.

        Parameters
        ----------
        name : str
            The name of the tier.
        interval_tier : bool
            If True, insert an :class:`IntervalTier`. Otherwise, insert a :class:`PointTier`.
        index : int, default None, meaning the last index.
            The index of the tier.

        Returns
        -------
        :class:`IntervalTier` or :class:`PointTier`
            An empty tier.
        """
        if index is None:
            index = len(self)

        if not isinstance(index, int):
            raise ValueError('index MUST BE a int value.')

        if interval_tier:
            tier = IntervalTier(name, self._xmin, self._xmax)
        else:
            tier = PointTier(name, self._xmin, self._xmax)
        self.tiers.insert(index, tier)

        return tier

    def remove_tier(self, index):
        """
        Remove a tier from the TextGrid.

        Parameters
        ----------
        tier : int
            The tier index.

        Returns
        -------
        :class:`IntervalTier` or :class:`PointTier`
            The removed tier.
        """
        return self._tiers.pop(index)

    def get_tier_by_name(self, tier_name):
        """
        Return a list of tier objects with the specified name.

        Parameters
        ----------
        tier : str
            The name of a tier stored in the TextGrid.

        Returns
        -------
        list of tiers
            A list of tiers that have the name.
        """
        if not isinstance(tier_name, str):
            raise TypeError('tier MUST BE a str')

        list_ = [tier for tier in self._tiers if tier.name == tier_name]
        return list_

    def to_dict(self):
        """
        Convert a TextGrid to a dict.
        """
        tiers_list = []
        for tier in self._tiers:
            # Collect Intervals or points into a list
            items_list = []
            for item in tier:
                if tier.is_interval():
                    item = {
                        'xmin':item.xmin,
                        'xmax':item.xmax,
                        'text':item.text
                    }
                else:
                    item = {
                        'number':item.time,
                        'mark':item.text
                    }
                items_list.append(item)

            # Put intervasl/points collection into tiers
            tiers_list.append(
                {
                    'interval_tier': tier.is_interval(),
                    'name': tier.name,
                    'items': items_list
                }
            )
        # Put tiers into TextGrid
        textgrid_dict = {
            'xmin': self._xmin,
            'xmax': self._xmax,
            'tiers': tiers_list
        }
        return textgrid_dict

    def write(self, path, short_format = False, encoding = 'utf-8'):
        """
        Write TextGrid to a text file.

        Parameters
        ----------
        path : str or :clas:`pathlib.Path`
            The path where the TextGrid file will be written.
        encoding : str, default 'utf-8'
            The encoding of the file.
        """
        textgrid_out.textgrid_to_text_file(self, path, short_format, encoding)

    def write_as_json(self, *args, **kwds):
        """
        Write TextGrid to a json file.

        Parameters
        ----------
        path : str or :clas:`pathlib.Path`
            The path where the JSON file will be written.
        encoding : str, default utf-8
            The encoding of the resulting file.
        """
        textgrid_out.textgrid_to_json(self, *args, **kwds)
