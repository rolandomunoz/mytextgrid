"""Create and manipulate tier objects"""
import decimal
from mytextgrid._eval import EvalTimeRange
decimal.getcontext().prec = 16

class Tier:
    """Tier is the base class for IntervalTier and PointTier classes. It represents an item's container."""

    def __init__(self, name = '', xmin = 0, xmax = 1, is_interval = True):
        self.name = name
        self._is_interval = is_interval
        self.xmin = decimal.Decimal(str(xmin))
        self.xmax = decimal.Decimal(str(xmax))
        self.items = []
        self.eval_time_range = EvalTimeRange(self.xmin, self.xmax, level = 1)

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def __getitem__(self, key):
        return self.items[key]

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
