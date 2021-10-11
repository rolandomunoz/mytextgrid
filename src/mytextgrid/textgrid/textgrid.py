"""Create and manipulate TextGrid objects.
"""
import decimal
from mytextgrid.textgrid import export
from mytextgrid.textgrid.interval_tier import IntervalTier
from mytextgrid.textgrid.point_tier import PointTier

decimal.getcontext().prec = 16

def create_textgrid(name, xmin = 0, xmax = 1):
    """Create and return an empty TextGrid.

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
        TextGrid
            A TextGrid instance.
    """
    return TextGrid(name, xmin, xmax)

class TextGrid:
    """A class representation for a TextGrid."""
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
        """Display compactly the structure of TextGrid.

        Show tier information: position, type, name and size.
        """
        for index, tier in enumerate(self):
            print(f'{index}\t{tier.class_}\t{tier.name}\t(size = {len(tier)})')

    def get_duration(self):
        """Return time duration in seconds.

        Returns
        -------
        float
            Time duration in seconds.
        """
        return self.xmax - self.xmin

    def insert_tier(self, name, class_ = 'interval', position = None):
        """Insert an interval tier into TextGrid at specified position.

        Parameters
        ----------
        name : str
            The name of the inserted tier.
        class_ : {'interval', 'point'}
            The class of the inserted tier.
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

        if class_ == 'interval':
            tier = IntervalTier(name, self.xmin, self.xmax)
        elif class_ == 'point':
            tier = PointTier(name, self.xmin, self.xmax)
        else:
            raise ValueError(f'class {class_} must be interval or point.')
        self.tiers.insert(position, tier)

        return self[position]

    def insert_interval_tier(self, name, position = None):
        """Insert an interval tier into TextGrid at specified position.

        Parameters
        ----------
        name : str
            The name of the inserted tier.
        position : int, default None, meaning the last position.
            The position of the inserted tier. Must verify 0 <= position <= len(TextGrid).

        Returns
        -------
        IntervalTier
            An empty tier.
        """
        return self.insert_tier(name, 'interval', position)

    def insert_point_tier(self, name, position = None):
        """Insert a point tier into TextGrid at specified position.

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
        return self.insert_tier(name, 'point', position)

    def insert_boundaries(self, tier, *times):
        """Search for an interval tier and insert one or more boundaries at the specified times.

        Parameters
        ----------
        tier : int or str
            A position or name of a tier stored in TextGrid.
        *times : iterable
            The time at which a boundary will be inserted in the selected tier.
        """
        tier_obj = self.get_tier(tier)

        # Raise an error if not an interval tier
        if not isinstance(tier_obj, IntervalTier):
            raise TypeError(f'Cannot add a boundary on tier {tier},'
            'because that tier is not an interval tier.')

        # Add boundarys
        tier_obj.insert_boundaries(*times)

    def insert_point(self, tier, time, text = ""):
        """Search for a point tier and insert a point at the specified time.

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
        """Search for an interval tier and set the text of one or more of its intervals.

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
        """Search for the specified tier and remove it from TextGrid.

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
        """Search for the specified tier and return it from TextGrid.

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
        IntervalTier or PointTier
            An interval or point tier stored in the TextGrid.
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
            raise IndexError(f'The specified tier numer {tier_position}'
            'exceeds the number of tiers {len(self)}')
        return self[tier_position]

    def to_textgrid(self, path, encoding = 'utf-8'):
        """Write TextGrid to a text file.

        Parameters
        ----------
        path : str
            The path where the TextGrid file will be created.
        encoding : str, default utf-8
            The encoding of the resulting file.
        """
        export.to_textgrid(self, path, encoding)

    def to_csv(self, path, encoding = 'utf-8'):
        """Convert TextGrid to a csv file.

        Parameters
        ----------
        path : str
            The path where the delimited text file will be created.
        encoding : str, default utf-8
            The encoding of the resulting file.
        """
        export.to_csv(self, path, encoding)

    def to_json(self, path):
        """Write TextGrid to a json file.

        Parameters
        ----------
        textgrid_obj : TextGrid
            Data stored in a TextGrid.
        path : str
            The path where the delimited text file will be created.
        encoding : str, default utf-8
            The encoding of the resulting file
        """
        export.to_json(self, path)

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
