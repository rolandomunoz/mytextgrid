"""Create and manipulate tier objects"""
import decimal
from mytextgrid._eval import EvalTimeRange
decimal.getcontext().prec = 16

class Tier:
    """
    This is a base class for :class:`IntervalTier` and :class:`PointTier classes`. It represents an item's container.
    """
    def __init__(self, name = '', xmin = 0, xmax = 1, is_interval = True):
        self._name = name
        self._is_interval = is_interval
        self._xmin = decimal.Decimal(str(xmin))
        self._xmax = decimal.Decimal(str(xmax))
        self._items = []
        self.eval_time_range = EvalTimeRange(self._xmin, self._xmax, level = 1)

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, key):
        return self._items[key]

    @property
    def name(self):
        return self._name

    @property
    def is_interval(self):
        return self._is_interval

    @property
    def xmin(self):
        return self._xmin

    @xmin.setter
    def xmin(self, value):
        xmin = decimal.Decimal(str(value))

        if xmin > self._xmax:
            raise ValueError('xmin must be lesser than xmax.')

        # Change the object time
            self._xmin = xmin

    @property
    def xmax(self):
        return self._xmax

    @xmax.setter
    def xmax(self, value):
        xmax = decimal.Decimal(str(value))

        if xmax < self._xmin:
            raise ValueError('xmax must be greater than xmin.')

        # Change the object time
            self._xmax = xmax

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, list_):
        self.items_ = list_

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
