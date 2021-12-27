"""Create and manipulate TextGrid objects.
"""
import decimal
from mytextgrid.io import export
from mytextgrid.core.interval_tier import IntervalTier
from mytextgrid.core.point_tier import PointTier

decimal.getcontext().prec = 16

def create_textgrid(name, xmin = 0, xmax = 1):
    """
    Create and return an empty TextGrid.

    By using this function, you will create an empty TextGrid.
    In order to make this instance useful, add tiers and text content.

    Parameters
    ----------
    name : str
        The name of the TextGrid.
    xmin : float, default 0
        The starting time of the TextGrid.
    xmax : float, default 1
        The ending time of the TextGrid.

    Returns
    -------
        :class:`mytextgrid.TextGrid`
            A TextGrid instance.
    """
    return TextGrid(name, xmin, xmax)

class TextGrid:
    """
    A class representation for a TextGrid.
    """
    def __init__(self, name= "", xmin = 0, xmax = 1):
        self.name = name
        self.xmin = decimal.Decimal(str(xmin))
        self.xmax = decimal.Decimal(str(xmax))
        self.tiers = []

    def __len__(self):
        return len(self.tiers)

    def __iter__(self):
        return iter(self.tiers)

    def __getitem__(self, key):
        return self.tiers[key]

    def describe(self):
        """
        Display compactly the attributes and structure of TextGrid.

        Show tier information: position, type, name and size.

        Examples
        --------
        First, read or create a :meth:`~mytextgrid.TextGrid`.
    
        >>> # Creating TextGrid
        >>> tg = mytextgrid.create_textgrid('perro', 0, 1)
        >>> # Inserting tiers
        >>> tg.insert_point_tier("tone")
        >>> tg.insert_interval_tier("segment")
        >>> tg.insert_point('tone', 0.66, "H")
        >>> # Insert content into the created tiers
        >>> tg.insert_point('tone', 0.9, "L")
        >>> tg.insert_boundaries('segment', 0.23, 0.30, 0.42, 0.62, 0.70, 0.82, 0.98)
        >>> tg.set_interval_text('segment', 1, 'e', 'l', 'p', 'e', 'rr', 'o')

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
        size = len(self)

        summary = []
        for index, tier in enumerate(self):
            tier_class = 'IntervalTier' if tier.is_interval else 'TextTier'
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
            f'    Name:                  {self.name}\n'
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
        return self.xmax - self.xmin

    def insert_tier(self, name, is_interval = True, position = None):
        """
        Insert an interval tier into TextGrid at specified position.

        Parameters
        ----------
        name : str
            The name of the inserted tier.
        is_interval : bool
            If True, insert an IntervalTier. Otherwise, return a PointTier.
        position : int, default None, meaning the last position.
            The position of the inserted tier. Must verify 0 <= position <= len(TextGrid).

        Returns
        -------
        IntervalTier
            An empty tier.
        """
        if position is None:
            position = len(self)

        self._eval_tier_position(position)
        self._eval_tiername(name)

        if is_interval:
            # Insert IntervalTier
            tier = IntervalTier(name, self.xmin, self.xmax)
        else:
            # Insert PointTier
            tier = PointTier(name, self.xmin, self.xmax)
        self.tiers.insert(position, tier)

        return self[position]

    def insert_interval_tier(self, name, position = None):
        """
        Insert an interval tier into TextGrid at specified position.

        Parameters
        ----------
        name : str
            The name of the inserted tier.
        position : int, default None, meaning the last position.
            The position of the inserted tier. Must verify 0 <= position <= len(TextGrid).

        Returns
        -------
        :class:`~mytextgrid.core.textgrid.IntervalTier`
            An empty tier.

        See Also
        ---------
        mytextgrid.TextGrid.insert_boundaries: Insert one or more boundaries.
        mytextgrid.TextGrid.set_interval_text: Set the text for one or more of intervals.
        """
        return self.insert_tier(name, True, position)

    def insert_point_tier(self, name, position = None):
        """
        Insert a point tier into TextGrid at specified position.

        Parameters
        ----------
        name : str
            The name of the inserted tier.
        position : int, default None, meaning the last position.
            The position of the inserted tier. Must verify 0 <= position <= len(TextGrid).

        Returns
        -------
        PointTier
            An empty tier.
        """
        return self.insert_tier(name, False, position)

    def insert_boundaries(self, tier, *times):
        """
        Search for an interval tier and insert one or more boundaries at the specified times.

        Parameters
        ----------
        tier : int or str
            A position or name of a tier stored in TextGrid.
        *times : iterable
            The time at which a boundary will be inserted in the selected tier.

        See Also
        ---------
        mytextgrid.TextGrid.set_interval_text: Set the text for one or more of intervals

        Examples
        --------
        >>> tg = mytextgrid.create_textgrid('banana', 0, 1)
        >>> tg.insert_interval_tier('segment')

        With the ``tier`` parameter, we specify the tier in which boundaries will be inserted.
        Then, we provide the time boundaries in the ``*times`` place.

        >>> tg.insert_boundaries('segment', 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.9)

        We can also pass an iterable object in the ``*times`` parameter.

        >>> times = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.9]
        >>> tg.insert_boundaries('segment', *times)
        """
        tier_obj = self.get_tier(tier)

        # Raise an error if not an interval tier
        if not isinstance(tier_obj, IntervalTier):
            raise TypeError(f'Cannot add a boundary on tier {tier},'
            'because that tier is not an interval tier.')

        # Add boundarys
        tier_obj.insert_boundaries(*times)

    def insert_point(self, tier, time, text = ""):
        """
        Search for a point tier and insert a point at the specified time.

        Parameters
        ----------
        tier : int or str
            A position or name of a tier stored in the TextGrid.
        time : float or :class:`decimal.Decimal`
            The time at which a :class:`~point_tier.Point` item will be inserted in the ``tier``.
        text : str, default ''
            The text content that will be store in the :class:`~point_tier.Point`
        """
        tier_obj = self.get_tier(tier)

        # Raise an error if not an point tier
        if not isinstance(tier_obj, PointTier):
            raise TypeError(f'Cannot add a boundary on tier {tier},'
            'because that tier is not an interval tier.')

        # Add boundary
        tier_obj.insert_point(time, text)

    def set_interval_text(self, tier, interval_position, *text_items):
        """
        Search for an interval tier and set the text of one or more of its intervals.

        If more than one text item is provided, intervals will be set from left to right
        counting from the starting `interval_position`.

        Parameters
        ----------
        tier : int or str
            A position or name of a tier stored in the TextGrid.
        interval_position : int
            The start position where text items will be inserted in the ``tier``.
        *text_items
            The text items that will be inserted.
        """
        tier_obj = self.get_tier(tier)
        # Raise an error if not an interval tier
        if not isinstance(tier_obj, IntervalTier):
            raise TypeError(f'Tier {tier} is an interval tier.')
        tier_obj.set_text(interval_position, *text_items)

    def remove_tier(self, tier):
        """
        Search for the specified tier and remove it from TextGrid.

        Parameters
        ----------
        tier : int or str
            The position or name of a tier stored in the TextGrid.
        """
        target_tier = self.get_tier(tier)
        for index, current_tier in enumerate(self):
            if target_tier is current_tier:
                self.tiers.pop(index)

    def get_tier(self, tier):
        """
        Search into the TextGrid for the specified tier and return it.

        By using this method, you will get access to a tier stored
        within the TextGrid by its position or name. In the case
        where two o more tiers have the same name, this methods
        will return only the first occurrence.

        Parameters
        ----------
        tier : int or str
            The position or name of a tier stored in the TextGrid.

        Returns
        -------
        :class:`~mytextgrid.core.interval_tier.IntervalTier` or :class:`~mytextgrid.core.interval_tier.PointTier`
            A tier stored in the TextGrid.
        """
        if isinstance(tier, int):
            if tier < 0:
                raise ValueError('Tier position must be a positive integer')
            tier_position = tier
        elif isinstance(tier, str):
            tier_position = None
            for index, tier_ in enumerate(self):
                if tier_.name == tier:
                    tier_position = index
                    break
        else:
            raise TypeError('tier must be a string or an integer')

        # Raise an error if tier does not exist or it is out of range
        if tier_position is None:
            raise NameError(f'The specified tier name {tier} does not exist')
        if tier_position > len(self):
            raise IndexError(f'The specified tier number {tier_position}'
            'exceeds the number of tiers {len(self)}')
        return self[tier_position]

    def to_textgrid(self, path, encoding = 'utf-8'):
        """
        Write TextGrid to a text file.

        Parameters
        ----------
        path : str
            The path where the TextGrid file will be created.
        encoding : str, default utf-8
            The encoding of the resulting file.
        """
        export.to_textgrid(self, path, encoding)

    def to_csv(self, path, encoding = 'utf-8'):
        """
        Convert TextGrid to a csv file.

        Parameters
        ----------
        path : str
            The path where the delimited text file will be created.
        encoding : str, default utf-8
            The encoding of the resulting file.
        """
        export.to_csv(self, path, encoding)

    def to_json(self, path, encoding = 'utf-8'):
        """
        Write TextGrid to a json file.

        Parameters
        ----------
        path : str
            The path where the delimited text file will be created.
        encoding : str, default utf-8
            The encoding of the resulting file
        """
        export.to_json(self, path, encoding)

    @staticmethod
    def _eval_tier_position(tier_position):
        if isinstance(tier_position, int):
            if tier_position < 0:
                raise ValueError('Tier position must be a positive integer')
        else:
            raise TypeError('Tier position must be a positive integer')

    @staticmethod
    def _eval_tiername(name):
        if " " in name:
            raise SyntaxError('Tier names must not contain white spaces')
