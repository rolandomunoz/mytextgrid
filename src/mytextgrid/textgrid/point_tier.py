"""Create and manipulate point tiers objects"""
import decimal
from mytextgrid._eval import EvalTimeRange
decimal.getcontext().prec = 16

class PointTier:
    """Represent a tier that contains Point objects."""

    def __init__(self, name = '', xmin = 0, xmax = 1):
        self.name = name
        self.class_ = 'TextTier'
        self.xmin = decimal.Decimal(str(xmin))
        self.xmax = decimal.Decimal(str(xmax))
        self.tier = []
        self.eval_time_range = EvalTimeRange(self.xmin, self.xmax, level = 1)

    def __len__(self):
        return len(self.tier)

    def __iter__(self):
        return iter(self.tier)

    def __getitem__(self, key):
        return self.tier[key]

    def insert_point(self, time, text = ''):
        """Insert a Point into PointTier.

        Parameters
        ----------
        time : float or decimal.Decimal
            The time in seconds where the Point will be inserted.
        text : str
            The text of the selected Point.
        """
        if not isinstance(time, decimal.Decimal):
            time = decimal.Decimal(str(time))

        if self.is_point_at_time(time):
            raise ValueError(f'Cannot insert a point at {time}')

        point = Point(time, text)
        self.tier.append(point)
        self.tier.sort(key=lambda x:x.time)

    def insert_points(self, *times):
        """Insert various empty points into PointTier.

        Parameters
        ----------
        *times : float or decimal.Decimal
            One or more time items where Point items will be inserted.
        """
        for time in times:
            self.insert_point(time)

    def remove_point(self, position):
        """Remove a Point.

        Parameters
        ----------
        position : int
            The position of the Point in PointTier. It must be 0 <= position < len(PointTier).
        """
        self.tier.pop(position)

    def set_point_text(self, position, text):
        """Set the text content of an existing Point.

        Parameters
        ----------
        position : int
            The position of the Point in PointTier. It must be 0 <= position < len(PointTier).
        text: str
            The text of the selected Point.
        """
        self.tier[position].text = text

    def get_time_of_point(self, position):
        """Return the time of a Point.

        Parameters
        ----------
        position : int
            The position of the Point in PointTier. It must be 0 <= position < len(PointTier).

        Returns
        -------
        str
            Return the time of the selected Point.
        """
        return self.tier[position].time

    def get_label_of_point(self, position):
        """Return the text content of a Point.

        Parameters
        ----------
        position : int
            The position of the Point in PointTier. It must be 0 <= position < len(PointTier)

        Returns
        -------
        str
            Return the text of the selected Point.
        """
        return self.tier[position].text

    def is_point_at_time(self, time):
        """Evaluate if a Point exists in the specified time.

        Parameters
        ----------
        time : float or decimal.Decimal
            Time in seconds.
        Returns
        -------
        bool
            Return True if a Point exists in the specified time. Otherwise, return False.
        """
        if not isinstance(time, decimal.Decimal):
            time = decimal.Decimal(str(time))

        # Check if out of range
        self.eval_time_range.check_time(time)
        for point in self:
            if point.time == time:
                return True
        return False

class Point:
    """Represent a Point object which is the minimal unit of a PointTier object"""

    def __init__(self, time, text = ""):
        self.class_ = 'Point'
        self.time = decimal.Decimal(str(time))
        self.text = text
