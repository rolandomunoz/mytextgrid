"""Create and manipulate `Interval` and `IntervalTier` objects."""
import decimal
from mytextgrid._eval import EvalTimeRange
decimal.getcontext().prec = 16

class IntervalTier:
    """A class representation for a interval tier."""

    def __init__(self, name = '', xmin = 0, xmax = 1):
        self.name = name
        self.class_ = 'IntervalTier'
        self.xmin = decimal.Decimal(str(xmin))
        self.xmax = decimal.Decimal(str(xmax))
        self.tier = [Interval(self.xmin, self.xmax)]
        self.eval_time_range = EvalTimeRange(self.xmin, self.xmax, level = 1)

    def __iter__(self):
        return iter(self.tier)

    def __len__(self):
        return len(self.tier)

    def __getitem__(self, key):
        return self.tier[key]

    def insert_boundaries(self, *times):
        """Insert one or more time boundaries into IntervalTier.

        Parameters
        ----------
        *time : float or decimal.Decimal
            The times (in seconds) of the new boundaries.
        """
        for time in times:
            self.insert_boundary(time)

    def insert_boundary(self, time):
        """Insert a time boundary into IntervalTier.

        Parameters
        ----------
        time : float or decimal.Decimal
            The time (in seconds) of the new boundary.
        """
        if not isinstance(time, decimal.Decimal):
            time = decimal.Decimal(str(time))

        # Check if out of range
        self.eval_time_range.check_time(time)

        interval_position = self.get_interval_at_time(time)
        interval_left = self.tier[interval_position]
        if time == interval_left.xmin:
            error_msg = (f'Cannot add a boundary at {time} seconds,'
            'because there is already a boundary there. Boundary not inserted.')
            raise ValueError(error_msg)

        # Split interval
        interval_right = Interval(time, interval_left.xmax)
        interval_left.xmax= time

        # Insert interval
        self.tier.insert(interval_position+1, interval_right)

    def remove_boundary(self, time):
        """Remove a time boundary from IntervalTier.

        Parameters
        ----------
        time : float or decimal.Decimal
            The time (in seconds) of an existing boundary.
        """
        if not isinstance(time, decimal.Decimal):
            time = decimal.Decimal(str(time))

        self.eval_time_range.check_time(time)

        interval_position = self.get_interval_at_time(time)
        interval_left = self.tier[interval_position]
        if not time == interval_left.xmin:
            error_msg = f'There is no boundary at {time} seconds'
            raise ValueError(error_msg)

        interval_left = self.tier[interval_position-1]
        interval_right = self.tier[interval_position]

        interval_left.xmax = interval_right.xmax
        interval_left.text += interval_right.text

        # Remove right interval
        self.tier.pop(interval_position)

    def move_boundary(self, src_time, dst_time):
        """Move the selected boundary to another time.

        Parameters
        ----------
        src_time : float or decimal.Decimal
            The time (in seconds) of an existing boundary.
        dst_time : float or decimal.Decimal
            The time (in seconds) where the boundary will be moved to.
        """
        # Normalize numbers
        if not isinstance(src_time, decimal.Decimal):
            src_time = decimal.Decimal(str(src_time))

        if not isinstance(dst_time, decimal.Decimal):
            dst_time = decimal.Decimal(str(dst_time))

        # Check
        self.eval_time_range.check_time(src_time)
        self.eval_time_range.check_time(dst_time)

        position = self.get_interval_at_time(src_time)

        interval_left = self.tier[position-1]
        interval_right = self.tier[position]

        if not interval_right.xmin == src_time:
            raise ValueError(f'There is no boundary at {src_time} seconds')

        if not dst_time > interval_left.xmin or not dst_time < interval_right.xmax:
            raise ValueError(f'Cannot move boundary to {dst_time}')

        # Do
        interval_left.xmax = dst_time
        interval_right.xmin = dst_time

    def set_text(self, position, *text_items):
        """Set the text of one or more of intervals.

        If more than one text item is provided, intervals will be set from left to right
        counting from the starting `position`.

        Parameters
        ----------
        position : int
            The start position where text items will be inserted in the ``position``.
        *text_items
            The text items that will be inserted.
        """
        for tier_position, text in enumerate(text_items, start = position):
            self.tier[tier_position].text = text

    def get_interval_at_time(self, time):
        """Search the IntervalTier for an interval position at the specified time.

        Parameters
        ----------
        time : float or decimal.Decimal
            The time in seconds to be evaluated.

        Returns
        -------
        int
            Return the interval position of the specified time.
        """
        self.eval_time_range.check_time(time)
        if not isinstance(time, decimal.Decimal):
            time = decimal.Decimal(str(time))
        for position, interval in enumerate(self):
            if interval.is_in_range(time):
                return position
        return None

class Interval:
    """A class representation for an interval."""

    def __init__(self, xmin, xmax, text = ""):
        self.class_ = 'Interval'
        self.xmin = decimal.Decimal(str(xmin))
        self.xmax = decimal.Decimal(str(xmax))
        self.text = text

    def is_in_range(self, time):
        """Evaluate if the specified time is between the interval boundaries.

        Parameters
        ----------
        time : float or decimal.Decimal
            The time in seconds to be evaluated.

        Returns
        -------
        bool
            True is the specified tier is Interval range, that is (xmin >= time < xmax).
            Otherwise, False.
        """
        time = decimal.Decimal(str(time))
        if self.xmin <= time < self.xmax:
            return True
        return False

    def is_left_boundary(self, time):
        """Evaluate if the specified time is equal to the left boundary time.

        Parameters
        ----------
        time : float or decimal.Decimal
            The time in seconds to be evaluated.

        Returns
        -------
        bool
            True is the specified tier is equal to the left boundary. Otherwise, False.
        """
        time = decimal.Decimal(str(time))
        if self.xmin == time:
            return True
        return False

    def is_right_boundary(self, time):
        """Evaluate if the specified time is equal to the right boundary time.

        Parameters
        ----------
        time : float or decimal.Decimal
            The time in seconds to be evaluated.

        Returns
        -------
        bool
            True is the specified tier is equal to the right boundary. Otherwise, False.
        """
        time = decimal.Decimal(str(time))
        if self.xmax == time:
            return True
        return False
