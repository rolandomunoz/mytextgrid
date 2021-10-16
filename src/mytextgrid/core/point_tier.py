"""Create and manipulate point tiers objects"""
import decimal
from mytextgrid.core.tier import Tier
decimal.getcontext().prec = 16

class PointTier(Tier):
    """Represent a tier that contains Point objects."""

    def __init__(self, name = '', xmin = 0, xmax = 1):
        super().__init__(name, xmin, xmax, is_interval = False)

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
        self.items.append(point)
        self.items.sort(key=lambda x:x.time)

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
        self.items.pop(position)

    def set_point_text(self, position, text):
        """Set the text content of an existing Point.

        Parameters
        ----------
        position : int
            The position of the Point in PointTier. It must be 0 <= position < len(PointTier).
        text: str
            The text of the selected Point.
        """
        self.items[position].text = text

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
        return self.items[position].time

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
        return self.items[position].text

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
