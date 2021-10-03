"""Create and manipulate a TextGrid object."""
import decimal
from .interval_tier import IntervalTier
from .point_tier import PointTier
decimal.getcontext().prec = 16

def create_textgrid(name, xmin = 0, xmax = 1):
    """Create an empty TextGrid object"""
    return TextGrid(name, xmin, xmax)

class TextGrid:
    """A class representation for a TextGrid object."""
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

    def struct(self):
        """"Display compactly the structure of the TextGrid.

        A TextGrid object contains tiers which also contain intervals or points. By using this
        method, you can display compactly the structure of the TextGrid.
        """
        for index, tier in enumerate(self):
            print(f'{index}\t{tier.class_}\t{tier.name}\t(size = {len(tier)})')

    def get_duration(self):
        """Return the duration of the TextGrid file.

        Returns
        -------
        float
            Duration of the TextGrid.
        """
        return self.xmax - self.xmin

    def insert_interval_tier(self, name, tier_position = None):
        """Insert an interval tier into the TextGrid and return the inserted tier.

        Parameters:
        -----------
        name : str
            The name of the tier object.
        tier_position : int, default None, meaning the last position.
            The position in which the created tier object will be inserted.

        Returns:
        --------
        :class:`~mytextgrid.interval_tier.IntervalTier`
            An empty tier object.
        """
        if tier_position is None:
            tier_position = len(self)

        self._eval_tier_position(tier_position)
        self._eval_tiername(name)

        interval_tier = IntervalTier(name, self.xmin, self.xmax)
        self.tiers.insert(tier_position, interval_tier)
        return self[tier_position]

    def insert_point_tier(self, name, tier_position = None):
        """Insert a point tier into the TextGrid and return the inserted tier.

        Parameters:
        -----------
        name : str
            The name of the tier object.
        tier_position : int, default None, meaning the last position.
            The position in which the created tier object will be inserted.

        Returns:
        --------
        :class:`~mytextgrid.interval_tier.PointTier`
            An empty tier object.
        """
        if tier_position is None:
            tier_position = len(self)

        self._eval_tier_position(tier_position)
        self._eval_tiername(name)

        point_tier = PointTier(name, self.xmin, self.xmax)
        self.tiers.insert(tier_position, point_tier)
        return self[tier_position]

    def insert_boundaries(self, tier, *times):
        """Insert one or more time boundaries into the selected interval tier.

        Parameters
        ----------
        tier : int or str
            A position or name of a tier stored in the TextGrid.
        time : float or :class:`decimal.Decimal`
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
        """Insert a time boundary and a text into the selected point tier.

        Insert a :class:`point_tier.Point` in the selected ``tier``.

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
        """Set the text of one or more intervals.

        Set one or more contiguous text intervals from left to right
        given a tier and the starting interval position.

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
        tier_obj.set_text(interval_position, text_items)

    def remove_tier(self, tier):
        """Remove a tier object stored in the TextGrid.

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
        """Return a tier object.

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
        :class:`~mytextgrid.interval_tier` or ~class:`~mytextgrid.point_tier`
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

    def save_as_table(self, path, delimiter = '\t'):
        """Convert and save a TextGrid object as a delimited text file.

        By using this method, the :class:`~textgrid.TextGrid` is converted to a table where
        non-empty items (:class:`~interval_tier.Interval` and :class:`~point_tier.Point`)
        become rows. Each item (row) is stored along with the tier it belongs to and its
        timestamps. When the table is done, the items (rows) are sorted by time in ascending
        order. Finally, the table is exported as a delimited text file.

        Parameters
        ----------
        path : str
            The path where the delimited text file will be created.
        delimiter : str, default '\t', tab character
            Any character use to separate values.
        """
        table = []
        for tier in self:
            for item in tier:
                if item.text == '':
                    continue
                if isinstance(tier, IntervalTier):
                    table.append([item.xmin, tier.name, item.text, item.xmax])
                else:
                    table.append([item.time, tier.name, item.text, item.time])

        table.sort(key=lambda x:x[0])
        with open(path, 'w', encoding = 'utf8') as file:
            for row in table:
                str_line = delimiter.join([str(item) for item in row])
                file.write(str_line + '\n')

    def save_as_text_file(self, path):
        """Save a TextGrid object as a text file.

        Parameters
        ----------
        path : str
            The path where the TextGrid file will be created.
        """
        tg_header = ['File type = "ooTextFile"',
            'Object class = "TextGrid"\n',
            f'xmin = {self.xmin} ',
            f'xmax = {self.xmax} ',
            'tiers? <exists> ',
            f'size = {len(self)} ',
            'item []: ']

        with open(path, 'w', encoding = 'utf-8') as file:
            for line in tg_header:
                file.write(line + '\n')

            for tier_position, tier in enumerate(self, start = 1):
                file.write(f'    item [{tier_position}]:\n'.format())
                file.write(f'        class = "{tier.class_}" \n')
                file.write(f'        name = "{tier.name}" \n')
                file.write(f'        xmin = {tier.xmin} \n')
                file.write(f'        xmax = {tier.xmax} \n')
                class_ = 'intervals' if tier.class_ == 'IntervalTier' else 'points'
                file.write(f'        {class_}: size = {len(tier)} \n')

                if isinstance(tier, IntervalTier):
                    for item_position, item in enumerate(tier, start = 1):
                        file.write(f'        intervals [{item_position}]:\n')
                        file.write(f'            xmin = {item.xmin} \n')
                        file.write(f'            xmax = {item.xmax} \n')
                        file.write(f'            text = "{item.text}" \n')
                else:
                    for item_position, item in enumerate(tier, start = 1):
                        file.write(f'        points [{item_position}]:\n')
                        file.write(f'            number = {item.time} \n')
                        file.write(f'            mark = "{item.text}" \n')

    def _eval_tier_position(self, tier_position):
        if isinstance(tier_position, int):
            if tier_position < 0:
                raise ValueError('Tier position must be a positive integer')
        else:
            raise TypeError('Tier position must be a positive integer')

    def _eval_tiername(self, name):
        if " " in name:
            raise SyntaxError('Tier names must not contain white spaces')
