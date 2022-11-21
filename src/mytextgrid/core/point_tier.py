"""Create and manipulate point tiers objects"""
import decimal
from mytextgrid.core.tier import Tier
from mytextgrid.eval import obj_to_decimal
decimal.getcontext().prec = 16

class PointTier(Tier):
    """
    Represent a tier that contains Point objects.
    """
    def __init__(self, name = '', xmin = 0, xmax = 1):
        super().__init__(name, xmin, xmax, is_interval = False)

    def insert_point(self, time, text = ''):
        """
        Insert a Point into PointTier.

        Parameters
        ----------
        time : int, float, str or :class:`decimal.Decimal`
            The time in seconds where a Point object will be inserted.
        text : str
            The text of the selected Point.
        """
        time_ = obj_to_decimal(time)
        self.eval_time_range(time_) # Check if out of range

        index = self.get_index_at_time(time_)
        if not index is None:
            raise ValueError(f'Cannot insert a Point at {time}.')

        point = Point(self, time_, text)
        self._items.append(point)
        self._items.sort(key=lambda x:x.time)

    def insert_points(self, *times):
        """Insert various empty points into PointTier.

        Parameters
        ----------
        *times : float or decimal.Decimal
            One or more time items where Point items will be inserted.
        """
        for time in times:
            self.insert_point(time)

    def remove_point(self, index):
        """
        Remove a Point.

        Parameters
        ----------
        index : int
            The index of the Point in PointTier. It must be 0 <= index < len(PointTier).
        """
        self._items.pop(index)

    def get_index_at_time(self, time):
        """
        Get the index of an existing `Point`.

        Parameters
        ----------
        time : int, float, str or :class:`decimal.Decimal`
            The position in seconds of the :class:`mytextgrid.core.point_tier.Interval`.

        Returns
        -------
        int or None
            Return the index of the point. If not found, return `None`.
        """
        time_ = obj_to_decimal(time)
        self.eval_time_range(time_) # Check if out of range

        for index, point in enumerate(self._items):
            if point.time == time_:
                return index
        return None

    def get_point_at_time(self, time):
        """
        Get the point at the specified time in the PointTier.

        Parameters
        ----------
        time : int, float, str or :class:`decimal.Decimal`
            The position in seconds of the :class:`mytextgrid.core.point_tier.Interval`.

        Returns
        -------
        :class:`mytextgrid.core.point_tier.Point` or None
            Return the index of the point. If not found, return `None`.
        """
        index = self.get_index_at_time(time)
        if index is None:
            return None
        return self._items[index]

class Point:
    """Represent a Point object which is the minimal unit of a PointTier object"""

    def __init__(self, parent, time, text = ''):
        """
        Init a Point.

        Parameters
        ----------
        parent: :class:`mytextgrid.core.PointTier`
            The parent tier.
        xmin : int, float str or decimal.Decimal
            The starting time (in seconds) of the interval.
        xmin : int, float str or decimal.Decimal
            The ending time (in seconds) of the interval.
        text : str, default ''
            The text content.
        """
        # Check input type
        if not isinstance(parent, PointTier):
            raise TypeError('parent MUST BE A PointTier')
        if not isinstance(time, (int, float, str, decimal.Decimal)):
            raise TypeError('time MUST BE an int, float, str or decimal.Decimal.')
        if not isinstance(text, str):
            raise TypeError('text MUST BE a str.')

        self.parent = parent
        self._time = obj_to_decimal(time)
        self._text = text

    @property
    def time(self):
        """
        Return _time attribute.
        """
        return self._time

    @property
    def xmin(self):
        """
        Return _time attribute.
        """
        return self._time

    @property
    def xmax(self):
        """
        Return _time attribute.
        """
        return self._time

    @property
    def text(self):
        """
        Return _text attribute.
        """
        return self._text

    @text.setter
    def text(self, value):
        """
        Modify _text attribute.
        """
        if not isinstance(value, str):
            raise TypeError('text MUST BE a str')
        self._text = value
