"""Create and manipulate tier objects"""
import decimal
from mytextgrid.eval import obj_to_decimal
decimal.getcontext().prec = 16

class Tier:
    """
    This is a base class for :class:`IntervalTier` and
    :class:`PointTier classes`. It represents an item's container.
    """
    def __init__(self, name = '', xmin = 0, xmax = 1, is_interval = True):
        """
        A base class to build a Interval or Point tier.

        Parameters
        ----------
        name : str, default ''
            The name of the tier.
        xmin : int, float str or decimal.Decimal
            The starting time (in seconds) of the tier.
        xmin : int, float str or decimal.Decimal
            The ending time (in seconds) of the tier.
        is_interval : bool, defaul True
            True is it is an Interval tier. False if it's a Point tier.
        """
        # Check input type
        if not isinstance(name, str):
            raise TypeError('name MUST BE a str.')
        if not isinstance(xmin, (int, float, str, decimal.Decimal)):
            raise TypeError('xmin MUST BE an int, float, str or decimal.Decimal.')
        if not isinstance(xmax, (int, float, str, decimal.Decimal)):
            raise TypeError('xmax MUST BE an int, float, str or decimal.Decimal.')
        if not isinstance(is_interval, bool):
            raise TypeError('is_interval MUST BE a boolean value.')

        xmin_ = obj_to_decimal(xmin)
        xmax_ = obj_to_decimal(xmax)

        assert xmax_ > xmin_, 'xmax MUST BE greater than xmin'

        self._name = name
        self._xmin = xmin_
        self._xmax = xmax_
        self._is_interval = is_interval
        self._items = []

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, key):
        return self._items[key]

    @property
    def name(self):
        """
        Return the `self._name` attribute.
        """
        return self._name

    @property
    def xmin(self):
        """
        Return the `self._xmin` attribute.
        """
        return self._xmin

    @property
    def xmax(self):
        """
        Return the `self._xmax` attribute.
        """
        return self._xmax

    @property
    def items(self):
        """
        Return the `self._items` attribute.
        """
        return self._items

    def get_duration(self):
        """
        Return the duration (in seconds) of the Tier instance.

        Return
        ------
            decimal.Decimal
                The duration in seconds of a Tier instance.
        """
        return self.xmax - self.xmin

    def is_interval(self):
        """"
        Check if the Tier contains interval or point items.

        Returns
        ------
        bool
            Return True if Tier contains intervals. Otherwise, return False.
        """
        return self._is_interval

    def eval_time_range(self, time):
        """
        Raise an exception if out of the tier range.
        """
        time_ = obj_to_decimal(time)

        if self._xmin > time_ > self._xmax:
            raise ValueError(f'{time_} (s) is out of range of the tier {self._name}')
        if self._xmin == time_:
            raise ValueError(f'{time_} seconds is at the left edge of the tier {self._name}.')
        if self._xmax == time_:
            raise ValueError(f'{time_} seconds is at the right edge of the tier {self._name}.')
