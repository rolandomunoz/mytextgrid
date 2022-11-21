"""Create and manipulate `Interval` and `IntervalTier` objects."""
import decimal
from mytextgrid.core.tier import Tier
from mytextgrid.eval import obj_to_decimal
decimal.getcontext().prec = 16

class IntervalTier(Tier):
    """
    A class representation for an interval tier.
    """
    def __init__(self, name = '', xmin = 0, xmax = 1):
        """
        Initialize an instance of :class:`~mytextgrid.core.interval_tier.IntervalTier`.

        Parameters
        ----------
        name : str, default ''
            The name of the tier.
        xmin : int, float str or :class:`decimal.Decimal`
            The starting time (in seconds) of the tier.
        xmin : int, float str or :class:`decimal.Decimal`
            The ending time (in seconds) of the tier.
        """
        super().__init__(name, xmin, xmax, is_interval = True)
        self._items = [Interval(self, self._xmin, self._xmax)]

    def insert_boundaries(self, *times):
        """
        Insert one or more time boundaries into a
        :class:`~mytextgrid.core.interval_tier.IntervalTier`.

        Parameters
        ----------
        *time : float or decimal.Decimal
            The times (in seconds) of the new boundaries.
        """
        for time in times:
            self.insert_boundary(time)

    def insert_boundary(self, time):
        """
        Insert a time boundary into a :class:`~mytextgrid.core.interval_tier.IntervalTier`.

        Parameters
        ----------
        time : int, float, str or :clas::`decimal.Decimal`
            The time (in seconds) of the new boundary.

        Returns
        -------
        tuple of (int, int)
            The left and right interval position at the inserted boundary.

        Raises
        ------
        ValueError
            If the specified time already exists.
        """
        time_ = obj_to_decimal(time)
        self.eval_time_range(time_) # Raise exceptions if out of the tier range

        index = self.get_index_at_time(time_)
        old_interval = self._items[index]

        if old_interval.xmin == time_:
            raise ValueError(f'There is already a boundary at {time_}')

        new_left_interval = Interval(
            self,
            xmin = old_interval.xmin,
            xmax = time_,
            text = old_interval.text
        )

        new_right_interval = Interval(
            self,
            xmin = time_,
            xmax = old_interval.xmax
        )

        # Update items
        self._items[index] = new_left_interval
        self._items.insert(index+1, new_right_interval)

        # Returns
        return (index, index+1)

    def remove_boundary(self, time):
        """
        Remove a time boundary from a :class:`~mytextgrid.core.interval_tier.IntervalTier`.

        Parameters
        ----------
        time : int, float, str or :clas::`decimal.Decimal`
            The time (in seconds) of the new boundary.

        Raises
        ------
        ValueError
            If there is there is not a boundary at the specified time.
        """
        time_ = obj_to_decimal(time)
        self.eval_time_range(time_) # Raise exceptions if out of range

        index = self.get_index_at_time_boundary(time_)
        if index is None:
            raise ValueError(f'No boundary to remove at {time}.')

        interval_left = self._items[index-1]
        interval_right = self._items[index]

        # Create and insert new interval
        new_interval  = Interval(
            self,
            xmin = interval_left.xmin,
            xmax = interval_right.xmax,
            text = interval_left.text + interval_right.text
        )

        # Update items
        self._items[index] = new_interval
        self._items.remove(interval_left)

    def move_boundary(self, src_time, dst_time):
        """
        Move a boundary to another location between the time range of the left and right intervals
        of the source location.

        Parameters
        ----------
        src_time : float or :class:`decimal.Decimal`
            The time (in seconds) of an existing boundary.
        dst_time : float or :class:`decimal.Decimal`
            The time (in seconds) where the boundary will be moved to.

        Raises
        ------
        ValueError
            If the new time location is outside of the time range of the left and right intervals.
        """
        # Normalize numbers
        src_time_ = obj_to_decimal(src_time)
        dst_time_ = obj_to_decimal(dst_time)

        # Raise exceptions.
        if src_time_ == dst_time_:
            raise ValueError('src_time and dst_time MUST NOT BE equal')
        self.eval_time_range(src_time_)
        self.eval_time_range(dst_time_)

        ## Get/Check if src boundary time exists.
        index = self.get_index_at_time_boundary(src_time_)
        if index is None:
            raise ValueError(f'No boundary found at src_time ({src_time_})')

        left_interval = self._items[index-1]
        right_interval = self._items[index]

        ## Check if dst_time is outside its neighbors boundaries.
        if left_interval.xmin >= dst_time_ >= right_interval.xmax:
            raise ValueError('Cannot move the source boundary outside its neighbors boundaries.')

        # Create intervals objects and replace them.
        new_left_interval = Interval(
            self,
            xmin = left_interval.xmin,
            xmax = dst_time_,
            text = left_interval.text
        )

        new_right_interval = Interval(
            self,
            xmin = dst_time_,
            xmax = right_interval.xmax,
            text = right_interval.text
        )

        # Update items
        self._items[index-1] = new_left_interval
        self._items[index] = new_right_interval

    def set_text_at_index(self, index, *text_items):
        """
        Set the text of one or more of intervals.

        If more than one text item is provided, intervals will be set from left to right
        counting from the starting `index`.

        Parameters
        ----------
        index : int
            The index at which text items will be inserted.
        text_items : str or iterable of str
            The text items that will be inserted.
        """
        # Raise Exception if more text items than intervals.
        if (index + len(text_items) - 1) > len(self._items):
            raise IndexError('more text items than intervals.')

        for index_, text in enumerate(text_items, start = index):
            self._items[index_].text = text

    def get_index_at_time(self, time):
        """
        Return the index of an interval at the given time.

        If time relies on the boundary between two intervals, it returns
        the index of the right interval.

        Parameters
        ----------
        time : int, float, str or :class:`decimal.Decimal`
            The time in seconds to be evaluated.

        Returns
        -------
        int or None
            Return the interval index at the specified time.
        """
        time_ = obj_to_decimal(time)

        if time_ == self._xmax:
            return len(self._items) - 1 # Returns the last index

        for index, interval in enumerate(self._items):
            if interval.xmin <= time_ < interval.xmax:
                return index
        return None

    def get_interval_at_time(self, time):
        """
        Return the interval at the specified time.

        If `time` relies on the boundary between two intervals, it returns
        the the right interval.

        Parameters
        ----------
        time : int, float, str or :class:`decimal.Decimal`
            The time in seconds to be evaluated.

        Returns
        -------
        :class:`mytextgrid.core.interval_tier.Interval` or None
            Return the interval index at the specified time.
        """
        index = self.get_index_at_time(time)
        if index is None:
            return None
        return self._items[index]

    def get_index_at_time_boundary(self, time):
        """
        Get the index of an interval at a given boundary.

        Only counts the inserted boundaries.

        Parameters
        ----------
        time : int, float, str or :class:`decimal.Decimal`
            The time to match with any boundary.

        Returns
        -------
        int or None
            Return an integer if the
        """
        time_ = obj_to_decimal(time)

        for index, interval in enumerate(self._items):
            if index == 0:
                continue
            if interval.xmin == time_:
                return index
        return None

class Interval:
    """
    A class representation for an interval.
    """
    def __init__(self, parent, xmin, xmax, text = ''):
        """
        Init an object representing a Praat interval.

        Parameters
        ----------
        parent: :class:`mytextgrid.core.IntervalTier`
            The parent tier.
        xmin : int, float str or decimal.Decimal
            The starting time (in seconds) of the interval.
        xmin : int, float str or decimal.Decimal
            The ending time (in seconds) of the interval.
        text : str, default ''
            The text content.
        """
        # Check input type
        if not isinstance(parent, IntervalTier):
            raise TypeError('parent MUST BE AN IntervalTier')
        if not isinstance(text, str):
            raise TypeError('text MUST BE a str.')
        if not isinstance(xmin, (int, float, str, decimal.Decimal)):
            raise TypeError('xmin MUST BE an int, float, str or decimal.Decimal.')
        if not isinstance(xmax, (int, float, str, decimal.Decimal)):
            raise TypeError('xmax MUST BE an int, float, str or decimal.Decimal.')

        xmin_ = obj_to_decimal(xmin)
        xmax_ = obj_to_decimal(xmax)

        assert xmax_ > xmin_, 'xmax MUST BE greater than xmin'

        # Assign attributes
        self.parent = parent
        self._xmin = xmin_
        self._xmax = xmax_
        self._text = text

    @property
    def xmin(self):
        """
        Return _xmin attribute.
        """
        return self._xmin

    @property
    def xmax(self):
        """
        Return _xmax attribute.
        """
        return self._xmax

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

    def get_duration(self):
        """
        Return the duration of the interval.

        Return
        ------
        :class:`decimal.Decimal`
            The duration of the interval.
        """
        return self._xmax - self._xmin
